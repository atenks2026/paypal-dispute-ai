"""Unit tests for Flask app — mocked service, test client, no network."""

from __future__ import annotations

from unittest.mock import patch
import json

import app as app_module


def test_health():
    client = app_module.app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_appeal_endpoint_returns_service_result():
    fake_result = {
        "dispute_id": "DP-T1",
        "letter_source": "llm",
        "letter": "PayPal appeal letter body.",
        "message_sent": {"status": "queued"},
        "appeal_submitted": {"status": "accepted"},
        "errors": [],
    }
    with patch.object(app_module.service, "run_appeal", return_value=fake_result):
        client = app_module.app.test_client()
        resp = client.post("/api/disputes/DP-T1/appeal")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["letter_source"] == "llm"
        assert body["appeal_submitted"]["status"] == "accepted"


def test_appeal_endpoint_propagates_errors():
    with patch.object(
        app_module.service,
        "run_appeal",
        return_value={"dispute_id": "DP-X", "errors": ["fetch_dispute: down"]},
    ):
        client = app_module.app.test_client()
        resp = client.post("/api/disputes/DP-X/appeal")
        assert resp.status_code == 502
