"""PayPal Dispute AI Appeal — serverless-style proxy (Flask).

Backend proxy so PayPal Client ID/Secret and NIM API key never reach the
browser. All PayPal Disputes API sandbox calls and LLM appeal generation run
server-side.

Routes:
  GET  /health
  GET  /api/disputes?status=&limit=
  GET  /api/disputes/<dispute_id>
  POST /api/disputes/<dispute_id>/appeal   generate letter + send appeal

Run:  python app.py        (needs .env with PAYPAL_* and NIM_API_KEY)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from appeal_service import AppealService
from llm_client import NIMClient
from paypal_client import PayPalClient, PayPalError

load_dotenv()  # reads .env next to this file if present (never committed)

app = Flask(__name__)
paypal = PayPalClient()
service = AppealService(paypal=paypal, llm=NIMClient())


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "paypal-dispute-ai"})


@app.get("/api/disputes")
def list_disputes():
    try:
        data = paypal.list_disputes(status=request.args.get("status"), limit=int(request.args.get("limit", 10)))
        return jsonify(data)
    except PayPalError as exc:
        return jsonify({"error": str(exc)}), 502


@app.get("/api/disputes/<dispute_id>")
def get_dispute(dispute_id: str):
    try:
        return jsonify(paypal.get_dispute(dispute_id))
    except PayPalError as exc:
        status = 404 if "not found" in str(exc).lower() else 502
        return jsonify({"error": str(exc)}), status


@app.post("/api/disputes/<dispute_id>/appeal")
def appeal(dispute_id: str):
    result = service.run_appeal(dispute_id)
    if result["errors"]:
        return jsonify(result), 502
    return jsonify(result), 200


@app.errorhandler(Exception)
def handle_unexpected(exc):
    return jsonify({"error": "internal server error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
