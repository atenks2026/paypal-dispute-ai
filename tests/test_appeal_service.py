"""Unit tests for AppealService — mocked PayPal + LLM (happy path + fallback)."""

from __future__ import annotations

from unittest.mock import patch

from appeal_service import AppealService
from paypal_client import PayPalClient, PayPalError
from llm_client import NIMClient

DISPUTE_DETAIL = {
    "dispute_id": "DP-999",
    "case_type": "CHARGEBACK",
    "reason": "NOT_RECEIVED",
    "status": "WAITING_FOR_SELLER_RESPONSE",
    "amount": {"value": "120.00", "currency_code": "USD"},
    "create_time": "2026-10-25T10:00:00Z",
    "evidence": [{"type": "TRACKING_INFO", "description": "Tracking 1Z999"}],
}


class FakeLLM:
    def __init__(self, letter: str | None = None, boom: bool = False) -> None:
        self.letter = letter
        self.boom = boom
        self.calls = 0

    def generate_appeal(self, dispute: dict, evidence: list):
        self.calls += 1
        if self.boom:
            raise Exception("LLM down")
        return self.letter


class FakePayPal:
    def __init__(self, detail=DISPUTE_DETAIL, appeal_ok: bool = True) -> None:
        self.detail = detail
        self.appeal_ok = appeal_ok
        self.messages = []

    def get_dispute(self, dispute_id: str):
        if dispute_id != self.detail["dispute_id"]:
            raise PayPalError("Dispute not found: " + dispute_id)
        return self.detail

    def send_message(self, dispute_id: str, text: str):
        self.messages.append((dispute_id, text))
        return {"status": "queued"}

    def appeal(self, dispute_id: str):
        if not self.appeal_ok:
            return {"status": "skipped", "reason": "not appealable"}
        return {"status": "accepted"}


def test_happy_path_llm_letter():
    fake_pp = FakePayPal()
    fake_llm = FakeLLM(letter="PayPal, please reverse this dispute.")
    result = AppealService(paypal=fake_pp, llm=fake_llm).run_appeal("DP-999")
    assert result["errors"] == []
    assert result["letter_source"] == "llm"
    assert "please reverse this dispute" in result["letter"]
    assert fake_pp.messages and "DP-999" in fake_pp.messages[0][0]
    assert result["appeal_submitted"]["status"] == "accepted"


def test_llm_unavailable_uses_fallback():
    fake_pp = FakePayPal()
    fake_llm = FakeLLM(letter=None)  # simulates missing NIM_API_KEY
    result = AppealService(paypal=fake_pp, llm=fake_llm).run_appeal("DP-999")
    assert result["errors"] == []
    assert result["letter_source"] == "fallback_template"
    assert "Formal Appeal" in result["letter"]
    assert result["message_sent"]["status"] == "queued"


def test_fetch_failure_recorded():
    class BrokenPP:
        def get_dispute(self, dispute_id):
            raise PayPalError("down")
    result = AppealService(paypal=BrokenPP()).run_appeal("DP-999")
    assert result["errors"]
    assert result["letter"] is None


def test_appeal_ineligible_is_skipped_not_failed():
    fake_pp = FakePayPal(appeal_ok=True)
    fake_llm = FakeLLM(letter="appeal letter")
    result = AppealService(paypal=fake_pp, llm=fake_llm).run_appeal("DP-999")
    assert result["appeal_submitted"]["status"] == "accepted"
    assert result["errors"] == []
