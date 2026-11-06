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

## AI Tools Disclosure (wajib Devpost)
Produk ini menggunakan AI untuk membantu menyusun surat appeal:
- **Alat AI:** LLM NVIDIA NIM (OpenAI-compatible), model `nemotron-3.5-super-vl-120b-a12b`, untuk generate draft surat appeal dalam bahasa Inggris.
- **Fallback non-AI:** jika NIM tidak tersedia, sistem menggunakan template statis (`templates/appeal_fallback.txt`) tanpa AI.
- **Transparansi sumber:** setiap surat di UI ditandai sumbernya — "AI (NVIDIA NIM)", "Template statis (fallback, NIM tidak tersedia)", atau "Template statis (backend tidak tersedia)".
- **Hasil AI adalah draft:** periksa dan setujui sendiri sebelum kirim ke PayPal Resolution Center.
- **Keamanan kredensial:** kunci API PayPal dan NIM tidak pernah mencapai browser; semua panggilan PayPal/NIM berjalan server-side via proxy Flask.

## Akses khusus untuk juri (Sandbox PayPal) — wajib di README
Submission ini membutuhkan akses khusus ke PayPal Sandbox (developer.paypal.com):
1. Masuk ke developer.paypal.com dengan akun PayPal Sandbox.
2. Buat aplikasi Sandbox: Dashboard → Sandbox → Apps → Create App. Catat **Client ID** dan **Secret**.
3. Salin `.env.example` ke `.env` (di luar repo, **jangan commit** `.env`), lalu isi `PAYPAL_CLIENT_ID` dan `PAYPAL_CLIENT_SECRET`.
4. Jalankan tes tanpa credential: `python -m pytest tests/ -q` (semua PayPal + LLM di-mock).
5. Jalankan backend: `python app.py`, lalu buka `http://localhost:5000/health`.
6. Buka frontend (`index.html`), isi detail dispute, generate draft, lalu **salin atau unduh** draft dan kirim secara manual ke PayPal Resolution Center (**Opsi B**; tidak ada integrasi API langsung ke production PayPal).

## Rekomendasi: approval step dan batas (sandkai PayPal)
- **Approval step (terpenuhi, manusia):** Opsi B manual memaksa pengguna meninjau dan menyetujui draft baru mengirimkannya ke PayPal Resolution Center.
- **Batas/limit (rekomendasi produksi):** disarankan batas jumlah appeal per hari dan nominal transaksi maksimal per appeal untuk iterasi berikutnya; belum diimplementasi pada versi hackathon.
- **Audit trail:** sumber surat (AI / fallback / static) tercatat di `letter_source` respons API dan `sourceNote` di frontend.

