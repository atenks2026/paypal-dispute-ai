# PayPal Dispute AI Appeal (AHVO-4 Lead Developer deliverable)

AI-generated PayPal appeal letter via LLM (NVIDIA NIM), integrated with the
PayPal Disputes API Sandbox. Backend proxy — PayPal and LLM credentials never
reach the browser.

## What it does
1. Fetches a dispute from the PayPal Sandbox Disputes API (OAuth client-credentials).
2. Generates a formal English appeal letter with an LLM (NVIDIA NIM, OpenAI-compatible).
3. Falls back to a static template when NIM is unavailable.
4. Sends the appeal letter to the counterparty via `send-message`, and submits
   the decision appeal via `/appeal` (best-effort; ineligible states are skipped).

## Project structure
```
app.py                  Flask proxy + appeal routes
paypal_client.py        PayPal Sandbox client (OAuth, disputes, message, appeal)
llm_client.py           NVIDIA NIM appeal-letter generator
appeal_service.py       Orchestration + fallback template
templates/appeal_fallback.txt   Static appeal letter template
tests/                  Unit tests (mocked PayPal + LLM)
.env.example            Variable names only — copy privately, never commit
requirements.txt
```

## Setup
```
pip install --user -r requirements.txt
cp .env.example .env
# fill .env with your PayPal Developer Sandbox Client ID/Secret and NIM API key
python app.py
# http://localhost:5000/health
```

## HOW TO TEST (under 3 minutes)
```
python -m pytest tests/ -q   # mocked: no network, no credentials needed
# 1. Start app: python app.py
# 2. curl http://localhost:5000/health            -> {"status":"ok"}
# 3. curl http://localhost:5000/api/disputes      -> sandbox dispute list (needs .env)
# 4. curl -X POST http://localhost:5000/api/disputes/<DP_ID>/appeal
#    -> appeal letter generated (LLM or fallback) + sent to PayPal
```

## Environment variables (.env, never committed)
- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET` — from developer.paypal.com Sandbox app
- `PAYPAL_BASE_URL` — default https://api-m.sandbox.paypal.com
- `NIM_API_KEY`, `NIM_BASE_URL`, `NIM_MODEL` — LLM for appeal letter generation

## Security
- `.env` and `05-rahasia/` are never committed (`.gitignore`).
- No API keys in frontend code; all PayPal/NIM calls are server-side.
