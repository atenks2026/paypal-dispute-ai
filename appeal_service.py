"""Orchestration: fetch dispute → generate appeal letter via LLM → send to PayPal.

Fallback: if the LLM is unavailable, a static template letter is used
(see templates/appeal_fallback.txt). PayPal appeal endpoint is best-effort —
a dispute not yet in an appealable state is recorded as skipped, not failed.
"""

from __future__ import annotations

import os
from typing import Any

from llm_client import NIMClient, LLMError
from paypal_client import PayPalClient, PayPalError

FALLBACK_PATH = os.path.join("templates", "appeal_fallback.txt")


class AppealService:
    def __init__(self, paypal: PayPalClient, llm: NIMClient | None = None) -> None:
        self.paypal = paypal
        self.llm = llm or NIMClient()

    def run_appeal(self, dispute_id: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "dispute_id": dispute_id,
            "letter": None,
            "letter_source": None,
            "message_sent": None,
            "appeal_submitted": None,
            "errors": [],
        }

        # 1) Fetch dispute details from PayPal sandbox.
        try:
            dispute = self.paypal.get_dispute(dispute_id)
        except (PayPalError, Exception) as exc:  # noqa: BLE001 — surface to API layer
            result["errors"].append(f"fetch_dispute: {exc}")
            return result

        # 2) Generate appeal letter via LLM, fallback to static template.
        evidence = dispute.get("evidence", []) or []
        letter = None
        try:
            letter = self.llm.generate_appeal(dispute, evidence)
        except LLMError:
            letter = None
        if not letter:
            letter = _load_fallback(dispute, evidence)
            result["letter_source"] = "fallback_template"
        else:
            result["letter_source"] = "llm"
        result["letter"] = letter

        # 3) Deliver the appeal letter to the counterparty via PayPal.
        try:
            result["message_sent"] = self.paypal.send_message(dispute_id, letter)
        except PayPalError as exc:
            result["errors"].append(f"send_message: {exc}")

        # 4) Appeal the decision (best-effort; ineligible states are skipped).
        try:
            result["appeal_submitted"] = self.paypal.appeal(dispute_id)
        except PayPalError as exc:
            result["errors"].append(f"appeal: {exc}")

        return result


def _load_fallback(dispute: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "templates", "appeal_fallback.txt")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            template = fh.read()
    except OSError:
        template = "PayPal appeal for dispute {dispute_id}.\nCase: {case_type}\nReason: {reason}\n"
    return template.format(
        dispute_id=dispute.get("dispute_id", "unknown"),
        case_type=dispute.get("case_type", "unknown"),
        reason=dispute.get("reason", "unknown"),
        status=dispute.get("status", "unknown"),
        amount=(dispute.get("amount") or {}).get("value", "-") if isinstance(dispute.get("amount"), dict) else dispute.get("amount", "-"),
        currency=(dispute.get("amount") or {}).get("currency_code", "-") if isinstance(dispute.get("amount"), dict) else "-",
        create_time=dispute.get("create_time", "-"),
        evidence="\n".join(f"- {e}" for e in evidence) or "(none)",
    )
