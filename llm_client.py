"""LLM client for generating PayPal appeal letters (NVIDIA NIM primary).

NVIDIA NIM exposes an OpenAI-compatible chat completions endpoint:
  POST {NIM_BASE_URL}/chat/completions
  Header: Authorization: Bearer <NIM_API_KEY>

If no NIM_API_KEY is configured, or the NIM call fails, generate_appeal()
returns None and the caller falls back to the static template.
See AHVO model verification: NVIDIA NIM primary, OpenRouter fallback.
"""

from __future__ import annotations

import os
from typing import Any

import requests


class LLMError(Exception):
    pass


class NIMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or os.getenv("NIM_API_KEY")
        self.base_url = (base_url or os.getenv("NIM_BASE_URL") or "https://integrate.api.nvidia.com/v1").rstrip("/")
        self.model = model or os.getenv("NIM_MODEL", "nvidia/nemotron-3.5-super-vl-120b-a12b")
        self.timeout = timeout
        self._session = requests.Session()

    def available(self) -> bool:
        return bool(self.api_key)

    def generate_appeal(self, dispute: dict[str, Any], evidence: list[dict[str, Any]]) -> str | None:
        """Return a professional English appeal letter, or None if LLM unavailable."""
        if not self.available():
            return None

        system_prompt = (
            "You are writing a formal appeal letter to PayPal Merchant Customer "
            "Service on behalf of a seller. Language: American English. Tone: "
            "professional, factual, concise. Use only the case data below — do "
            "not invent amounts, dates, names, or policies. Structure: (1) case "
            "reference and dispute ID, (2) summary of the issue, (3) seller's "
            "position with evidence reference, (4) requested resolution, "
            "(5) closing. Max 250 words."
        )
        evidence_lines = "\n".join(
            f"- {e.get('type', 'evidence')}: {e.get('description', '')}" for e in evidence
        ) or "(no evidence attached)"
        user_prompt = (
            "Dispute ID: {dispute_id}\n"
            "Case type: {case_type}\n"
            "Reason: {reason}\n"
            "Status: {status}\n"
            "Amount: {amount} {currency}\n"
            "Created: {create_time}\n"
            "Evidence:\n{evidence}\n\n"
            "Write the appeal letter now."
        ).format(
            dispute_id=dispute.get("dispute_id", "unknown"),
            case_type=dispute.get("case_type", "unknown"),
            reason=dispute.get("reason", "unknown"),
            status=dispute.get("status", "unknown"),
            amount=dispute.get("amount", {}).get("value", "-") if isinstance(dispute.get("amount"), dict) else dispute.get("amount", "-"),
            currency=dispute.get("amount", {}).get("currency_code", "-") if isinstance(dispute.get("amount"), dict) else "-",
            create_time=dispute.get("create_time", "-"),
            evidence=evidence_lines,
        )

        try:
            resp = self._session.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
                timeout=self.timeout,
            )
        except requests.RequestException:
            return None

        if resp.status_code != 200:
            return None
        try:
            letter = resp.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, ValueError):
            return None
        return letter.strip() or None
