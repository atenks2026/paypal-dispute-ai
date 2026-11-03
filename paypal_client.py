"""PayPal Disputes API client — Sandbox (server-side only).

All PayPal calls happen here, on the backend. The browser never talks to
PayPal directly, so Client ID/Secret are never exposed and CORS is avoided.

Endpoints (sandbox base: https://api-m.sandbox.paypal.com/v1/customer/disputes/):
  GET    /v1/customer/disputes                    list disputes
  GET    /v1/customer/disputes/{dispute_id}       dispute details
  POST   /v1/customer/disputes/{dispute_id}/send-message   send message to counterparty
  POST   /v1/customer/disputes/{dispute_id}/appeal         appeal a decision

OAuth: POST /v1/oauth2/token  (grant_type=client_credentials, Basic auth)

See: references/paypal-disputes-api.md (AHVO hackathon-execution skill)
"""

from __future__ import annotations

import os
import base64
import time
from typing import Any

import requests

SANDBOX_BASE = "https://api-m.sandbox.paypal.com"


def base64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


class PayPalError(Exception):
    """Raised when the PayPal API returns an error after retries."""


class PayPalClient:
    def __init__(
        self,
        base_url: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        timeout: int = 20,
        max_retries: int = 3,
    ) -> None:
        self.base_url = (base_url or os.getenv("PAYPAL_BASE_URL") or SANDBOX_BASE).rstrip("/")
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("PAYPAL_CLIENT_SECRET")
        self.timeout = timeout
        self.max_retries = max_retries
        self._access_token: str | None = None
        self._token_expires_at: float = 0.0
        self._session = requests.Session()

    # ------------------------------------------------------------------ auth

    def _basic_auth(self) -> str:
        token = f"{self.client_id}:{self.client_secret}".encode()
        return "Basic " + base64_encode(token)

    def get_access_token(self) -> str:
        """OAuth client-credentials token, cached until near expiry."""
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        if not self.client_id or not self.client_secret:
            raise PayPalError("PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET not configured")

        resp = self._session.post(
            f"{self.base_url}/v1/oauth2/token",
            headers={"Authorization": self._basic_auth(), "Accept": "application/json"},
            data={"grant_type": "client_credentials"},
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise PayPalError(f"OAuth failed HTTP {resp.status_code}: {resp.text[:200]}")
        payload = resp.json()
        self._access_token = payload["access_token"]
        self._token_expires_at = time.time() + float(payload.get("expires_in", 3600))
        return self._access_token

    # --------------------------------------------------------------- requests

    def _bearer(self) -> str:
        return "Bearer " + self.get_access_token()

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        headers.setdefault("Accept", "application/json")
        headers["Authorization"] = self._bearer()
        headers.setdefault("Content-Type", "application/json")

        last_error: str = ""
        for attempt in range(self.max_retries + 1):
            resp = self._session.request(method, url, headers=headers, timeout=self.timeout, **kwargs)
            # Exponential backoff on 429 / 5xx (PayPal rate-limit guidance).
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                last_error = f"HTTP {resp.status_code}"
                time.sleep(0.5 * (2**attempt))
                continue
            return resp

        raise PayPalError(f"PayPal request failed after retries (last: {last_error})")

    # --------------------------------------------------------------- disputes

    def list_disputes(self, status: str | None = None, limit: int = 10) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": min(limit, 100)}
        if status:
            params["status"] = status
        resp = self._request("GET", "/v1/customer/disputes", params=params)
        if resp.status_code != 200:
            raise PayPalError(f"List disputes failed HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()

    def get_dispute(self, dispute_id: str) -> dict[str, Any]:
        resp = self._request("GET", f"/v1/customer/disputes/{dispute_id}")
        if resp.status_code == 404:
            raise PayPalError(f"Dispute not found: {dispute_id}")
        if resp.status_code != 200:
            raise PayPalError(f"Get dispute failed HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()

    def send_message(self, dispute_id: str, text: str) -> dict[str, Any]:
        body = {"sender": "MERCHANT", "message": text}
        resp = self._request("POST", f"/v1/customer/disputes/{dispute_id}/send-message", json=body)
        if resp.status_code in (200, 201, 202):
            return resp.json() if resp.text.strip() else {"status": "queued"}
        raise PayPalError(f"Send message failed HTTP {resp.status_code}: {resp.text[:200]}")

    def appeal(self, dispute_id: str) -> dict[str, Any]:
        resp = self._request("POST", f"/v1/customer/disputes/{dispute_id}/appeal")
        if resp.status_code in (200, 201, 202):
            return resp.json() if resp.text.strip() else {"status": "accepted"}
        # A dispute that isn't in an appealable state is not a hard failure.
        if resp.status_code in (400, 403, 409):
            return {"status": "skipped", "reason": f"not appealable (HTTP {resp.status_code})"}
        raise PayPalError(f"Appeal failed HTTP {resp.status_code}: {resp.text[:200]}")


def base64_encode(data: bytes) -> str:
    import base64

    return base64.b64encode(data).decode("ascii")
