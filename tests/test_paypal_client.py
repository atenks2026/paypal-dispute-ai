"""Unit tests for PayPalClient — fully mocked, no network, no credentials."""

from __future__ import annotations

from unittest.mock import patch
import pytest

from paypal_client import PayPalClient, PayPalError

FAKE_TOKEN = {"access_token": "fake-token", "expires_in": 3600}

DISPUTE_LIST = {
    "dispute_details": [
        {
            "dispute_id": "DP-123",
            "case_type": "CHARGEBACK",
            "reason": "NOT_RECEIVED",
            "status": "WAITING_FOR_SELLER_RESPONSE",
            "amount": {"value": "120.00", "currency_code": "USD"},
            "create_time": "2026-10-25T10:00:00Z",
        }
    ],
    "total_items": 1,
}

DISPUTE_DETAIL = {
    **DISPUTE_LIST["dispute_details"][0],
    "evidence": [{"type": "TRACKING_INFO", "description": "Tracking number 1Z999"}],
}


class FakeResponse:
    def __init__(self, status_code: int, json_data: dict | None = None, text: str = "") -> None:
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def json(self) -> dict:
        return self._json


def _fake_session(method, url, **kwargs):
    from urllib.parse import urlparse

    path = urlparse(url).path
    if path == "/v1/oauth2/token":
        return FakeResponse(200, FAKE_TOKEN)
    if path == "/v1/customer/disputes" and method == "GET":
        return FakeResponse(200, DISPUTE_LIST)
    if path.startswith("/v1/customer/disputes/") and method == "GET":
        if path.rsplit("/", 1)[-1] != DISPUTE_DETAIL["dispute_id"]:
            return FakeResponse(404, text="not found")
        return FakeResponse(200, DISPUTE_DETAIL)
    if path.endswith("/send-message") and method == "POST":
        return FakeResponse(202, {"status": "queued"})
    if path.endswith("/appeal") and method == "POST":
        return FakeResponse(200, {"status": "accepted"})
    return FakeResponse(404, text="not found")


@patch("paypal_client.requests.Session.request", side_effect=_fake_session)
def test_get_access_token_and_caching(_mock):
    client = PayPalClient(client_id="cid", client_secret="csecret")
    t1 = client.get_access_token()
    t2 = client.get_access_token()
    assert t1 == "fake-token" and t1 == t2


@patch("paypal_client.requests.Session.request", side_effect=_fake_session)
def test_list_and_get_dispute(_mock):
    client = PayPalClient(client_id="cid", client_secret="csecret")
    listed = client.list_disputes()
    assert listed["total_items"] == 1
    detail = client.get_dispute("DP-123")
    assert detail["dispute_id"] == "DP-123"


@patch("paypal_client.requests.Session.request", side_effect=_fake_session)
def test_send_message_and_appeal(_mock):
    client = PayPalClient(client_id="cid", client_secret="csecret")
    msg = client.send_message("DP-123", "please review evidence")
    assert msg["status"] == "queued"
    appeal = client.appeal("DP-123")
    assert appeal["status"] == "accepted"


@patch("paypal_client.requests.Session.request", side_effect=_fake_session)
def test_missing_credentials(_mock):
    client = PayPalClient(client_id=None, client_secret=None)
    try:
        client.get_access_token()
    except PayPalError as exc:
        assert "not configured" in str(exc)
    else:
        raise AssertionError("expected PayPalError")


@patch("paypal_client.requests.Session.request", side_effect=_fake_session)
def test_dispute_not_found(_mock):
    client = PayPalClient(client_id="cid", client_secret="csecret")
    try:
        client.get_dispute("NOPE")
    except PayPalError as exc:
        assert "not found" in str(exc)
    else:
        raise AssertionError("expected PayPalError")
