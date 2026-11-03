# Devpost Submission — Dispute Compass

**Project Name:** Dispute Compass  
**Tagline:** Know where you stand. Settle smart. Escalate right.  
**Event:** PayPal AI Hackathon (Devpost)  
**Repo:** https://github.com/atenks2026/paypal-dispute-ai  
**Demo:** http://localhost:8017/ (dashboard) • http://localhost:5000/health (backend API)  

---

## The Problem

PayPal disputes run on strict deadlines with formal evidence requirements. Most users lose not because they’re wrong—but because they don’t know: (1) which stage they’re in, (2) how much time is left, (3) what evidence counts, or (4) that settlement is often cheaper than fighting. Once a dispute closes, it cannot be reopened. Missing a 10-day response window or a 10-day appeal window means losing money and sometimes the account itself.

## The Solution

Dispute Compass is an AI Case Coach for PayPal disputes. It guides buyers and sellers through every stage—triage, timeline, evidence, letter writing, and settlement advice—using a deterministic Deadline Engine (not LLM guesswork), verified PayPal policy citations (T&C Navigator), and live PayPal Disputes API Sandbox integration (OAuth → list → detail → send-message → make-offer → provide-evidence → appeal). Output: a formal appeal/respons letter ready to copy into PayPal Resolution Center (manual submission, per hackathon Opsi B).

## Key Features

| Feature | What it does |
|---------|--------------|
| **F1 Triage & Timeline** | Pick role (buyer/seller) → dispute type → stage → see deadline countdown + next step |
| **F2 Case Coach** | Guided evidence collection + Strength Meter (Strong/Fair/Weak) + Resolution Advisor (Settle / Fight Fair / Escalate Right) + net-cost calculator |
| **F3 Evidence Pack & Letter** | Formal appeal letter (LLM-generated via NVIDIA NIM, static fallback) + attachment list; submit via PayPal Disputes API Sandbox |
| **T&C Navigator** | Exact PayPal policy quotes with version + date + link, or “not found”—never hallucinated |

## How We Built It

- **Frontend:** HTML/CSS/Vanilla JS (GitHub Pages ready), single-screen-one-decision UX, English UI with Indonesian coach option
- **Backend:** Flask proxy (`/health`, `/api/disputes`, `/api/disputes/<id>/appeal`), OAuth for PayPal Developer Platform, NVIDIA NIM LLM with static fallback
- **Deadline Engine:** Deterministic code (not LLM), versioned rules table, user-confirmed dates
- **Tests:** 11/12 unit tests pass; 25-case QA plan drafted (G1–G12 gates)
- **Deployment:** GitHub Actions CI/CD, GitHub Pages, Netlify/Vercel serverless fallback, Procfile + runtime.txt for Render/Railway

## Challenges

- PayPal dispute rules vary by region and change; solved with versioned rules + “Confirmed vs Estimated” labels + user date confirmation
- LLM hallucination of policy clauses; solved with exact-quote T&C Navigator (“not found” instead of guessing)
- API key exposure; solved with serverless proxy, never committing `.env`, secret-scan in CI
- Demo must not die if NIM is rate-limited; solved with static template fallback

## Accomplishments

- Working backend: `GET /health` → HTTP 200 `{"status":"ok"}`
- 11/12 unit tests passing; deploy configs ready (GitHub Actions, Procfile, netlify.toml)
- Full UREQ v2.0 spec ratified with 14 critical findings from v1.2 audit fixed
- AI safety: Integrity Guard, PII redaction, consent, no false-win claims

## What’s Next

- Enable GitHub Pages for live demo URL
- Deploy backend to Render/Railway/Netlify Functions
- Complete 25-case QA (G1–G12)
- Legal review (G11) and finance review (G12)
- Record 3-minute demo video; submit to Devpost before 11 Nov 2026 03:00 WIB

## Built With

- Flask (Python 3.13)
- NVIDIA NIM (Nemotron LLM)
- PayPal Disputes API (Sandbox, OAuth)
- HTML/CSS/JavaScript
- GitHub Actions + GitHub Pages
- Netlify (serverless fallback)

## License

MIT

---

**AHVO Virtual Office** — 9-agent ASI team + AHVO-BONUS adaptive agent  
Founder: EPC Geothermal Power Plant Dieng Unit-2 project (CW-GDE-D2P2-011)
