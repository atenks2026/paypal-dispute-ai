# T-20 Finance & Tax Checklist — Dispute Compass

**Project:** Dispute Compass — PayPal AI Hackathon (Devpost)  
**Repo:** `paypal-dispute-ai` (`finance/` folder)  
**Checklist:** T-20 Finance & Tax (AHVO-9 FI)  
**Owner:** AHVO-9 FI (finance)  
**Status:** SELESAI — 100%  
**Deadline:** 7 Nov 2026, 23:00 WIB  
**Tanggal selesai:** 06 Nov 2026  
**Kalkulator pendukung:** `finance/finance-calculator.xlsx` (biaya operasional, prize tracker, tax compliance US–Indo, ringkasan)

---

## A. Estimasi Biaya Operasional (Operational Cost Estimates)

Kurs USD → IDR = 16.000 (asumsi, dapat disesuaikan di kalkulator).

| Item | Kategori | USD/bulan | USD/tahun | IDR/bulan | IDR/tahun | Status | Keterangan |
|------|----------|-----------|-----------|-----------|-----------|--------|------------|
| Domain (.com / custom, tahunan dibagi 12) | Infrastruktur | 1,25 | 15,00 | 20.000 | 240.000 | Estimasi | Biaya tunggal tahunan |
| Hosting backend (Render/Railway free tier) | Infrastruktur | 0,00 | 0,00 | 0 | 0 | Konfirmasi | Gratis tier; upgrade ~$7–25/bln jika perlu |
| Frontend hosting (GitHub Pages / Netlify) | Infrastruktur | 0,00 | 0,00 | 0 | 0 | Konfirmasi | Gratis |
| PayPal Sandbox API | API Pembayaran | 0,00 | 0,00 | 0 | 0 | Konfirmasi | Sandbox gratis, tidak ada biaya transaksi |
| NVIDIA NIM API (LLM surat appeal) | AI/LLM | 0,00 | 0,00 | 0 | 0 | Estimasi | Free tier / kredensial hackathon; produksi pakai-berdasarkan-pakai |
| GitHub (repo + CI/CD) | Alat Pengembang | 0,00 | 0,00 | 0 | 0 | Konfirmasi | Gratis (open source / individu) |
| Email/notifikasi (belum aktif) | Operasional | 0,00 | 0,00 | 0 | 0 | Estimasi | Belum diimplementasikan |
| Kontingensi 10% | Kontingensi | 0,13 | 1,50 | 2.000 | 24.000 | Estimasi | 10% dari subtotal |
| **TOTAL ESTIMASI** | | **1,38** | **16,50** | **22.000** | **264.000** | | |

**Kesimpulan biaya operasional:** sangat rendah (~USD 1,38/bulan ≈ Rp 22.000; ~USD 16,50/tahun ≈ Rp 264.000) karena hampir semua komponen pakai free tier.

---

## B. Prize Tracker

| Hadiah | Kategori | Jumlah (USD) | Status | Tanggal Target | Pajak AS (%) | Pajak AS (USD) | Bersih (USD) | Keterangan |
|--------|----------|--------------|--------|----------------|--------------|----------------|--------------|------------|
| Grand Prize PayPal AI Hackathon | Utama | 5.000 | Target | 11 Nov 2026 | 30 | 1.500 | 3.500 | Asumsi, belum diumumkan |
| Best Use of PayPal API | Kategori | 1.000 | Target | 11 Nov 2026 | 30 | 300 | 700 | Asumsi |
| Best AI/ML Integration | Kategori | 1.000 | Target | 11 Nov 2026 | 30 | 300 | 700 | Asumsi |
| **TOTAL** | | **7.000** | | | | **2.100** | **4.900** | |

**Total target hadiah kotor:** USD 7.000  
**Estimasi pajak AS dipotong:** USD 2.100 (asumsi 30%, sebelum konvensi pajak ganda)  
**Total hadiah bersih estimasi:** USD 4.900  
*Catatan: semua status "Target" karena hadiah belum diumumkan; akan diupdate setelah pengumuman lomba.*

---

## C. Tax Compliance US–Indonesia

| # | Item | Referensi | Status | Keterangan |
|---|------|-----------|--------|------------|
| 1 | NPWP (Nomor Pokok Wajib Pajak) Indonesia aktif | UU KUP / PP No. 7/2022 | Siap | Pelapor pribadi/badan Indonesia |
| 2 | Form W-8BEN (sertifikat status warga asing AS) | Konvensi Pajak Indonesia–AS 1988 / IRS | Siap | Turunkan withholding US dari 30% ke tarif konvensi |
| 3 | Form 1042-S / 1099-NEC dari pemberi hadiah AS | IRS | Belum | Diterima & diverifikasi setelah hadiah diterima |
| 4 | Lapor hadiah dalam SPT Tahunan Indonesia | SPT 1770 (orang pribadi) | Belum | Penghasilan luar negeri dilaporkan setelah diterima |
| 5 | Kredit pajak asing (hindari bitunggalan ganda) | Konvensi pajak ganda Indonesia–AS | Belum | Lampirkan bukti potong pajak AS |
| 6 | Simpan dokumen pajak 5–10 tahun | UU KUP | Siap | Prosedur arsip siap |
| 7 | Klasifikasi hadiah: "hadiah lomba" vs "jasa profesional" | UU PPh / konvensi | Siap | Diklasifikasikan sebagai hadiah lomba |
| 8 | Konsultasi konsultan pajak Indonesia sebelum claim hadiah | — | Belum | Direkomendasikan sebelum klaim |

**Catatan pajak:** PayPal adalah pemberi hadiah berbasis AS. Tanpa W-8BEN, withholding AS biasanya 30% (FDAP). Pajak Indonesia progresif 5–35% (orang pribadi). Gunakan W-8BEN + kredit pajak asing untuk mengelola bitunggalan ganda.

---

## D. Ringkasan Estimasi Keuangan Submission

| Indikator | Nilai | Keterangan |
|-----------|-------|------------|
| Total biaya operasional estimasi | ~USD 16,50/tahun (≈ Rp 264.000) | Sangat rendah, hampir semua free tier |
| Total estimasi hadiah kotor | USD 7.000 | Target, belum resmi |
| Estimasi pajak AS dipotong | ~USD 2.100 | Asumsi 30% before treaty |
| Estimasi hadiah bersih | ~USD 4.900 | Setelah pajak AS |
| Status kepatuhan pajak US–Indo | Lengkap | NPWP & W-8BEN siap; SPT setelah terima hadiah |
| Kesimpulan | Aman | Biaya operasional minimal; risiko pajak terkelola |

**Kesimpulan:** Keuangan submission Dispute Compass aman untuk diajukan. Biaya operasional minimal, dan risiko pajak US–Indonesia terkelola dengan formulir W-8BEN serta kredit pajak asing.

---

**Tanda tangan:** AHVO-9 FI — 06 Nov 2026  
**Deadline submission:** 7 Nov 2026, 23:00 WIB (deadline lomba: 11 Nov 2026, 03:00 WIB)
