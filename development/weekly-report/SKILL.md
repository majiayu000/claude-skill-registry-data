---
name: weekly-report
description: Use when generating a weekly product and development progress report for stakeholders, clients, or management across a specific date range, explaining features, business impact, blockers, and next week's plan in accessible non-technical language.
---

# SKILL — WEEKLY PRODUCT & DEVELOPMENT REPORT

## NAMA SKILL
`weekly-report`

## TUJUAN
Skill ini digunakan untuk menyusun **laporan mingguan produk dan pengembangan software (Weekly Product & Development Report)** berdasarkan rentang waktu tertentu (`Tanggal A → Tanggal B`).

Laporan ini dirancang khusus untuk dibaca oleh **pemangku kepentingan non-teknis** (Product Owner, C-Level, Manajemen, Klien, atau Tim Bisnis). Fokus laporan bukan pada kode atau commit, melainkan pada **nilai bisnis (business value), kegunaan fitur (user experience), transparansi kendala, dan rencana strategis ke depan**.

> **ATURAN UTAMA:**
> **JANGAN PERNAH membuat laporan seperti changelog developer atau dump git commit!** 
> Hindari jargon seperti `refactored regex in auth middleware`, `fixed null pointer exception on line 42`, dsb. Terjemahkan setiap aktivitas teknis ke dalam fungsi fitur, manfaat bagi pengguna, dan dampaknya terhadap operasional bisnis.

---

## WHEN TO USE

### Gunakan Ketika:
- Pengguna meminta laporan mingguan / pekanan: *"buatkan weekly report dari tanggal X sampai Y"*, *"bikin laporan mingguan project"*, *"rekap pekerjaan minggu ini"*, atau trigger command `/weekly-report`.
- Menjelang rapat evaluasi mingguan (Weekly Sprint Review / Management Sync / Client Update).
- Membutuhkan dokumentasi kemajuan project yang komunikatif dan profesional untuk stakeholder non-teknis.

### JANGAN Gunakan Ketika:
- Pengguna meminta technical changelog atau release notes teknis (gunakan format Git release / changelog konvensional).
- Pengguna meminta audit performa kode murni atau code review diff antar branch.

---

## 1. INPUT SPECIFICATION

Skill menerima input utama:

```text
Tanggal Mulai: YYYY-MM-DD (atau format tanggal yang jelas)
Tanggal Selesai: YYYY-MM-DD (atau format tanggal yang jelas)
Project: <nama project> (opsional: jika tidak diisi, otomatis deteksi dari workspace aktif)
```

*Catatan:*
- Jika tanggal tidak disebutkan secara spesifik, asumsikan rentang 7 hari terakhir (atau tanyakan konfirmasi tanggal awal dan akhirnya).
- Jika nama project tidak disebutkan, deteksi otomatis dari file konfigurasi repository (seperti `package.json`, `README.md`, atau nama folder root).

---

## 2. PROSEDUR EKSEKUSI (WORKFLOW)

Ikuti 6 langkah terstruktur berikut saat menjalankan skill ini:

```
[1. Parse Input & Target] 
       ↓
[2. Kumpulkan Bukti Pekerjaan (Git & Docs)] 
       ↓
[3. Ekstraksi & Kategorisasi Fitur] 
       ↓
[4. Terjemahkan ke Narasi Non-Teknis] 
       ↓
[5. Analisis Kendala & Kondisi Project] 
       ↓
[6. Susun & Simpan Laporan]
```

### Langkah 1: Identifikasi Parameter & Konteks Project
1. Tentukan tanggal mulai (`A`) dan tanggal selesai (`B`).
2. Tentukan nama project dan baca ringkasan konteks project dari `README.md` atau `CLAUDE.md` untuk memahami produk dan target penggunanya.

### Langkah 2: Kumpulkan Data & Bukti Pekerjaan (Evidence Gathering)
Jalankan perintah pengumpulan data tanpa mengubah kode:
```bash
# 1. Cek commit log pada rentang tanggal
git log --since="YYYY-MM-DD 00:00:00" --until="YYYY-MM-DD 23:59:59" --pretty=format:"%h | %ad | %s" --date=short

# 2. Cek file-file apa saja yang banyak berubah
git log --since="YYYY-MM-DD 00:00:00" --until="YYYY-MM-DD 23:59:59" --stat --summary

# 3. Periksa apakah ada dokumen spec/plan/RFC yang dibuat dalam periode ini
# (misal di folder docs/, specs/, atau task tracking)
```

### Langkah 3: Kategorisasi Pekerjaan
Kelompokkan commit dan perubahan file ke dalam domain fungsional produk:
- **Fitur Baru (New Features):** Penambahan kapabilitas baru yang bisa dinikmati user.
- **Penyempurnaan Fitur (Enhancements & UX):** Tampilan lebih nyaman, proses lebih cepat, atau alur yang dipermudah.
- **Perbaikan Kualitas & Keandalan (Bug Fixes & Stability):** Masalah yang berhasil diatasi agar sistem berjalan tanpa kendala.
- **Pondasi Sistem & Keamanan (Infrastructure & Security):** Kesiapan server, keamanan data transaksi/akun, atau efisiensi sistem.

### Langkah 4: Terjemahkan Teknis ke Bahasa Bisnis & Produk
Gunakan **Kamus Transformasi Narasi** (lihat bagian 3) untuk mengubah istilah teknis menjadi penjelasan yang bernilai bagi bisnis dan user.

### Langkah 5: Analisis Kondisi & Kendala Mingguan
Jawab pertanyaan kunci berikut:
1. Apa kendala paling krusial yang dihadapi minggu ini?
2. Bagaimana solusi yang diambil oleh tim?
3. Bagaimana kondisi stabilitas dan kesiapan project di akhir minggu?
4. Apa target prioritas dan rencana mitigasi untuk pekan berikutnya?

### Langkah 6: Tulis dan Simpan Laporan
1. Format laporan sesuai template standar pada Bagian 4.
2. Simpan file ke direktori dokumentasi project:
   `docs/reports/weekly-report-YYYY-MM-DD-to-YYYY-MM-DD.md`
   *(Buat direktori jika belum tersedia)*.
3. Berikan output di chat berupa ringkasan eksekutif dan lampirkan link dokumen lengkapnya.

---

## 3. PANDUAN TRANSFORMASI BAHASA (TEKNIS → NON-TEKNIS)

Gunakan prinsip padanan berikut agar stakeholder non-teknis langsung memahami inti nilainya:

| Istilah Teknis Developer | Padanan Bahasa Produk / Bisnis | Contoh Kalimat Non-Teknis |
|---|---|---|
| `Refactor state management Zustand/Redux` | Optimalisasi responsivitas halaman | "Memperbarui sistem penyimpanan data sementara agar perpindahan antar halaman terasa instan dan tidak memuat ulang data berulang kali." |
| `Fix SQL injection & CSRF vulnerability` | Penguatan keamanan akun & transaksi | "Meningkatkan proteksi keamanan pada formulir pendaftaran dan pembayaran guna mencegah kebocoran data pengguna." |
| `Index database on foreign key` | Peningkatan kecepatan pencarian & akses | "Mempercepat proses pencarian data tamu dan transaksi hingga 3x lebih cepat saat diakses bersamaan." |
| `Fix null pointer exception / 500 error` | Perbaikan kendala sistem berhenti mendadak | "Memperbaiki gangguan di mana pengguna sempat mengalami layar kosong/gagal memuat saat mengisi form bertanda khusus." |
| `Setup webhook handler retry mechanism` | Otomasi kepastian status pembayaran | "Memastikan sistem secara otomatis memverifikasi ulang pembayaran dari payment gateway sehingga pesanan user tidak tertunda statusnya." |
| `Implement mobile-first responsive CSS` | Penyempurnaan tampilan di smartphone | "Menata ulang tampilan halaman undangan agar nyaman dibaca dan tidak terpotong di berbagai tipe layar HP." |
| `Migrate schema / alter table` | Penyesuaian struktur data fitur baru | "Mempersiapkan sistem database untuk mendukung opsi paket diskon dan down payment baru." |

---

## 4. TEMPLATE LAPORAN STANDAR

Gunakan struktur dokumen markdown berikut sebagai standar baku:

```markdown
# 📊 LAPORAN MINGGUAN PRODUK & PENGEMBANGAN
**Project:** {Nama Project}  
**Periode:** {Tanggal Mulai} — {Tanggal Selesai}  
**Status Keseluruhan:** 🟢 ON TRACK / 🟡 PERLU PERHATIAN / 🔴 MENGALAMI KENDALA  

---

## Executive Summary (Ringkasan Eksekutif)
*Tuliskan 1-2 paragraf ringkas yang merangkum pencapaian terbesar minggu ini, nilai yang berhasil dihantarkan ke produk, serta fokus utama tim selama sepekan.*

---

## 🚀 Fitur & Pekerjaan yang Diselesaikan

### 1. {Nama Fitur / Modul A}
- **Apa yang Dikerjakan:** {Jelaskan dengan bahasa umum apa yang dibuat atau ditingkatkan}
- **Tujuan Fitur:** {Mengapa fitur ini dibuat? Masalah apa yang diselesaikan untuk user?}
- **Dampak & Manfaat:** 
  - Bagi Pengguna: {Misal: lebih mudah memesan, tidak bingung saat isi data}
  - Bagi Bisnis: {Misal: mengurangi churn rate, meningkatkan konversi pembelian, otomasi operasional}
- **Hasil Akhir:** {Siap diuji coba di Staging / Sudah live di Production / Menunggu integrasi pihak ketiga}

### 2. {Nama Fitur / Modul B}
- **Apa yang Dikerjakan:** ...
- **Tujuan Fitur:** ...
- **Dampak & Manfaat:** ...
- **Hasil Akhir:** ...

---

## 🛠️ Perbaikan & Peningkatan Kualitas Sistem
*(Jelaskan perbaikan kendala atau bug tanpa menyebut baris kode/commit)*
- **{Nama Masalah/Area}:** Sebelumnya {deskripsi masalah yang dirasakan user}. Tim telah memperbaikinya sehingga sekarang {kondisi setelah perbaikan yang membuat user nyaman}.
- **{Optimalisasi Performa}:** {Misal: Mempercepat waktu buka halaman hingga 40% lebih ringan di koneksi mobile}.

---

## ⚠️ Kendala yang Dihadapi & Solusi Penanganan

| Kendala / Hambatan | Dampak terhadap Pekerjaan | Langkah Penanganan yang Diambil | Status Solusi |
|---|---|---|---|
| {Deskripsi kendala non-teknis} | {Apakah menunda timeline atau membatasi fungsi} | {Bagaimana tim mengatasi atau mencari jalan keluar} | ✅ Selesai / ⏳ Dalam Pemantauan |
| {Contoh: Keterlambatan verifikasi akun pihak ketiga} | {Fitur pembayaran sempat tertahan} | {Menggunakan akun sandbox alternatif untuk pengujian alur} | ✅ Terselesaikan |

### 💥 Kendala Terbesar Pekan Ini:
> **Kendala Utama:** {Jelaskan 1 kendala paling signifikan selama pekan ini}  
> **Akar Permasalahan:** {Penjelasan sederhana penyebabnya}  
> **Penyelesaian / Mitigasi:** {Langkah nyata yang telah dieksekusi agar tidak terulang}

---

## 📌 Kondisi Project pada Akhir Periode
- **Kesiapan Sistem:** {Stabil / Perlu Uji Lanjutan / Dalam Tahap Finalisasi}
- **Progres Rencana Kerja:** {Sesuai jadwal / Sedikit tertunda / Lebih cepat dari target}
- **Area yang Siap Direview Stakeholder:** {Sebutkan halaman/fitur yang sudah bisa langsung dicoba oleh tim produk/klien}

---

## 🎯 Kesimpulan & Evaluasi Minggu Ini
*Tuliskan evaluasi obyektif terhadap performa minggu ini. Apakah target tercapai? Pelajaran apa yang didapatkan tim dalam pengembangan sepekan ini?*

---

## 📋 Rencana Perbaikan & Target Pekan Berikutnya

### Prioritas Pengembangan Produk:
1. **{Target 1}:** {Deskripsi singkat target dan manfaatnya}
2. **{Target 2}:** {Deskripsi singkat target dan manfaatnya}
3. **{Target 3}:** {Deskripsi singkat target dan manfaatnya}

### Rencana Perbaikan Proses & Kualitas:
- {Langkah antisipasi agar kendala minggu ini tidak terulang di minggu depan}
- {Peningkatan alur testing / komunikasi / koordinasi teknis}
```

---

## 5. FORMAT RINGKAS UNTUK CHAT / MEMO (WHATSAPP / SLACK)

Selain dokumen lengkap, sediakan selalu versi ringkas 1 layar yang siap di-copypaste ke grup chat stakeholder:

```markdown
📢 *WEEKLY HIGHLIGHT: [Nama Project]*
🗓 *Periode:* [Tgl A] — [Tgl B]
🚦 *Status:* 🟢 On Track

✨ *Pencapaian Utama Pekan Ini:*
• *[Fitur A]:* [1 kalimat manfaat untuk pengguna]
• *[Fitur B]:* [1 kalimat dampak ke operasional/bisnis]
• *[Kualitas]:* Perbaikan stabilitas pada modul [Area] agar alur transaksi lancar.

⚠️ *Tantangan & Solusi:*
• [Tantangan utama] → Berhasil diatasi dengan [solusi singkat].

🎯 *Fokus Pekan Depan:*
1. [Target prioritas 1]
2. [Target prioritas 2]

📄 *Laporan lengkap tersimpan di:* `docs/reports/...`
```

---

## 6. CHECKLIST KUALITAS LAPORAN

Sebelum menyajikan laporan kepada pengguna, pastikan:
- [ ] Tidak ada hash commit mentah (contoh: `abc123f`) di teks utama laporan.
- [ ] Tidak ada nama variabel kode mentah tanpa konteks fungsional (contoh: `isUserActiveFlag`).
- [ ] Setiap fitur yang disebutkan memiliki **tujuan** dan **dampak nyata bagi user/bisnis**.
- [ ] Kendala dijelaskan secara jujur beserta langkah penanganan yang diambil (menunjukkan akuntabilitas).
- [ ] Terdapat kejelasan kondisi project saat ini dan rencana konkret minggu berikutnya.
- [ ] Menggunakan bahasa Indonesia yang lugas, profesional, dan nyaman dibaca oleh level manajerial.
