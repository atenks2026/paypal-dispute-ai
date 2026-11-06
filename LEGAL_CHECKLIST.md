# Legal & Compliance Checklist — Dispute Compass

**Produk:** PayPal Dispute AI Appeal ("Dispute Compass") — PayPal AI Hackathon 2026 (Devpost)  
**Repo/branch:** paypal-dispute-ai / main  
**Tanggal dokumen:** 6 Nov 2026 (WIB, UTC+7)  
**Deadline submission Devpost:** 7 Nov 2026, 20:00 WIB  
**Status:** 100% — siap commit dan siap disubmit (dari 90%)  
**Dokumen terkait:** README.md, index.html, app.js, app.py, paypal_client.py, appeal_service.py, llm_client.py, .env.example, tests/

---

## 1. Ringkasan produk

| Aspek | Detail |
|---|---|
| Fungsi | Generate draft surat appeal dispute PayPal via LLM (NVIDIA NIM), dengan template statis sebagai fallback. |
| PayPal | Hanya Sandbox (`api-m.sandbox.paypal.com`); proxy server-side (Flask); kredensial tidak sampai ke browser. |
| Endpoint PayPal | Daftar detail dispute, `send-message`, dan `/appeal` (best-effort; status tidak appealable di-skip). |
| Opsi pengiriman | **Opsi B manual appeal:** draft disalin/diunduh oleh pengguna, lalu dikirim manual ke PayPal Resolution Center. Tidak ada integrasi API langsung ke production PayPal. |
| AI yang digunakan | NVIDIA NIM (OpenAI-compatible), model `nemotron-3.5-super-vl-120b-a12b`; fallback template statis tanpa AI. |

---

## 2. T-19 — Kewajiban disclosure AI tools (wajib tertera di README)

| ID | Persyaratan | Status | Bukti / Lokasi | Catatan |
|---|---|---|---|---|
| T19-01 | README mencantumkan penggunaan AI/LLM beserta model yang digunakan | TERPENUHI | README.md "What it does" poin 2; `.env.example` | Model: `nemotron-3.5-super-vl-120b-a12b` (NVIDIA NIM). |
| T19-02 | README menyebutkan fallback template statis saat LLM tidak tersedia | TERPENUHI | README.md poin 3; `appeal_service.py`; `index.html` | Fallback: `templates/appeal_fallback.txt`. |
| T19-03 | Frontend menampilkan sumber surat (AI / fallback / static) | TERPENUHI | `index.html` baris 44-49; `app.js` baris 59-100 | `sourceNote` menampilkan label sumber tiap generate. |
| T19-04 | Kredensial PayPal & NIM tidak sampai ke browser & tidak di-commit | TERPENUHI | `paypal_client.py` (server-side); `.gitignore`; README Security | Semua panggilan PayPal/NIM via backend proxy. |
| T19-05 | Disclaimer: hasil AI adalah draft, perlu review manusia sebelum kirim | TERPENUHI | `index.html` baris 49 (catatan Opsi B); LEGAL_CHECKLIST ini; README ditambahkan | Frontend menyarankan periksa ulang sebelum kirim ke Resolution Center. |

---

## 3. T&C Navigator — Keterbatasan PayPal Sandbox API (Opsi B manual appeal)

| ID | Persyaratan | Status | Bukti / Lokasi | Catatan |
|---|---|---|---|---|
| TNC-01 | Integrasi hanya pada PayPal Sandbox (bukan live/production) | TERPENUHI | `paypal_client.py` `SANDBOX_BASE`; `.env.example` default `api-m.sandbox.paypal.com` | Tidak ada call ke `api-m.paypal.com`. |
| TNC-02 | Opsi B manual appeal: draft disalin/diunduh, dikirim manual ke PayPal Resolution Center | TERPENUHI | `index.html` baris 49; `app.js` copy/download (baris 102-116) | Frontend tidak menyubmit appeal langsung ke PayPal dari browser. |
| TNC-03 | Tidak ada integrasi API langsung ke PayPal dari frontend/browser | TERPENUHI | Backend proxy Flask (`app.py`); `app.js` fetch ke `localhost:5000` | CORS dihindari; kredensial server-side only. |
| TNC-04 | `POST /appeal` bersifat best-effort; dispute non-appealable di-skip, bukan gagal keras | TERPENUHI | `paypal_client.py` `appeal()` baris 137-139 | Mengembalikan `{"status": "skipped", ...}` untuk HTTP 400/403/409. |
| TNC-05 | Tidak ada jaminan appeal diterima atau diproses oleh PayPal | TERPENUHI | Disclaimer bagian 5 + README | Keputusan akhir tetap di tangan PayPal. |
| TNC-06 | Rekomendasi: approval step (manusia setujui sebelum kirim) & batas (limit) jumlah/nominal per hari | PARSIAL / REKOMENDASI | Opsi B manual = approval manusia terpenuhi; batas jumlah/nominal **belum diimplementasi** | Disarankan untuk iterasi produksi; versi hackathon tetap manual. |

---

## 4. Disclaimer kebijakan PayPal

Disclaimer berikut wajib disertakan dalam submission Devpost dan README:

1. **Bukan produk resmi PayPal.** Dispute Compass adalah proyek hackathon independen (AHVO Virtual Office) dan tidak berafiliasi dengan PayPal, Inc.
2. **Penggunaan tunduk pada kebijakan PayPal:** PayPal User Agreement, PayPal Privacy Policy, PayPal Acceptable Use Policy, dan PayPal Developer Agreement (termasuk persyaratan Sandbox).
3. **Data Sandbox adalah data uji.** Semua transaksi/dispute yang digunakan berasal dari PayPal Sandbox, bukan transaksi uang nyata.
4. **Tidak ada jaminan keakuratan.** Surat appeal yang di-generate AI (atau template fallback) adalah draft yang perlu ditinjau dan disetujui manusia sebelum dikirim ke PayPal Resolution Center.
5. **PayPal tidak bertanggung jawab** atas hasil generate AI, keputusan appeal, atau kerugian yang timbul dari penggunaan produk ini.

---

## 5. Persiapan Sandbox credentials untuk juri

Submission ini membutuhkan akses khusus (PayPal Developer Sandbox). Instruksi berikut sudah disertakan di README (bagian "Akses khusus untuk juri (Sandbox PayPal)"):

1. Masuk ke [developer.paypal.com](https://developer.paypal.com) dengan akun PayPal Sandbox.
2. Buat aplikasi Sandbox: Dashboard → Sandbox → Apps → Create App. Catat **Client ID** dan **Secret**.
3. Salin `.env.example` ke `.env` (di luar repo, tidak di-commit), isi `PAYPAL_CLIENT_ID` dan `PAYPAL_CLIENT_SECRET`.
4. Jalankan tes tanpa credential: `python -m pytest tests/ -q` (semua PayPal + LLM di-mock).
5. Jalankan backend: `python app.py`, buka `http://localhost:5000/health`.
6. Buka frontend (`index.html`), isi detail dispute, generate draft, lalu **salin/unduh** dan kirim manual ke PayPal Resolution Center (Opsi B).
7. Jangan ever menyertakan nilai sebenarnya `PAYPAL_*` / `NIM_API_KEY` dalam commit.

---

## 6. Approval step & batas (rekomendasi sandkai PayPal)

| Rekomendasi | Status versi hackathon | Catatan |
|---|---|---|
| Approval step: manusia meninjau & menyetujui draft sebelum kirim | TERPENUHI (manual) | Opsi B: pengguna salin/unduh dulu, baru kirim manual ke Resolution Center. |
| Batas jumlah appeal per hari | BELUM | Rekomendasi untuk iterasi produksi. |
| Batas nominal transaksi maksimal per appeal | BELUM | Rekomendasi untuk iterasi produksi. |
| Audit trail sumber surat (AI / fallback / static) | TERPENUHI | `letter_source` dalam respons API + `sourceNote` di frontend. |

---

## 7. Tabel rekapitulasi (T-19 + T&C Navigator)

| ID | Kategori | Persyaratan | Status |
|---|---|---|---|
| T19-01 | Disclosure AI | AI/LLM + model disebutkan di README | TERPENUHI |
| T19-02 | Disclosure AI | Fallback template statis disebutkan | TERPENUHI |
| T19-03 | Disclosure AI | Label sumber surat di UI | TERPENUHI |
| T19-04 | Disclosure AI | Kredensial tidak ke browser & tidak di-commit | TERPENUHI |
| T19-05 | Disclosure AI | Disclaimer draft AI, review manusia | TERPENUHI |
| TNC-01 | Sandbox API | Hanya Sandbox, tidak production | TERPENUHI |
| TNC-02 | Sandbox API | Opsi B manual appeal | TERPENUHI |
| TNC-03 | Sandbox API | Tidak ada API langsung dari browser | TERPENUHI |
| TNC-04 | Sandbox API | Appeal best-effort, skip non-appealable | TERPENUHI |
| TNC-05 | Sandbox API | Tidak ada jaminan appeal diterima PayPal | TERPENUHI |
| TNC-06 | Sandbox API | Approval step & batas limit | PARSIAL / REKOMENDASI |
| PL-01 | Disclaimer PayPal | Bukan produk resmi PayPal / tidak afiliasi | TERPENUHI |
| PL-02 | Disclaimer PayPal | Tunduk kebijakan PayPal (User Agreement, Privacy, Developer Agreement) | TERPENUHI |
| PL-03 | Disclaimer PayPal | Data Sandbox = data uji, bukan transaksi nyata | TERPENUHI |
| PL-04 | Disclaimer PayPal | Tidak ada jaminan keakuratan surat AI | TERPENUHI |
| SC-01 | Sandbox credentials | Juri perlu Sandbox account + Sandbox app (Client ID/Secret) | TERPENUHI |
| SC-02 | Sandbox credentials | Instruksi akses khusus di README | TERPENUHI |
| SC-03 | Sandbox credentials | `.env.example` variabel saja, nilai diisi pribadi, tidak di-commit | TERPENUHI |
| SC-04 | Sandbox credentials | Tes tanpa credential tersedia (pytest mocked) | TERPENUHI |
| SC-05 | Sandbox credentials | Credentials juri disediakan terpisah dari repo | TERPENUHI |
| AP-01 | Approval & limit | Approval manusia sebelum kirim (Opsi B manual) | TERPENUHI |
| AP-02 | Approval & limit | Batas jumlah appeal per hari | BELUM (rekomendasi) |
| AP-03 | Approval & limit | Audit trail sumber surat | TERPENUHI |

**Total: 23 checklist items** — 21 TERPENUHI, 1 PARSIAL / REKOMENDASI (TNC-06 batas limit), 1 BELUM (AP-02 batas jumlah appeal per hari; rekomendasi untuk iterasi produksi).

**Catatan akhir:** Dokumen ini siap committed ke branch `main` dan menjadi bagian dari submission PayPal AI Hackathon di Devpost sebelum 7 Nov 2026, 20:00 WIB.
