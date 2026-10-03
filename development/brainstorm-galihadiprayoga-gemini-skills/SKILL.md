---
name: brainstorm
description: >
  Gunakan untuk sesi ideation terstruktur sebelum memulai fitur baru, debugging kompleks, atau refactor besar.
  Trigger: "brainstorm fitur X", "kita mau bikin Y gimana", "ada masalah dengan Z", "/brainstorm".
  Output: keputusan pendekatan + asumsi + open questions — bukan kode.
---

# brainstorm

## Overview
Sesi **ideation terstruktur** yang menghasilkan clarity sebelum implementasi. Mencegah coding yang salah arah, mengidentifikasi risiko lebih awal, dan memastikan semua pertanyaan penting dijawab sebelum baris kode pertama ditulis.

Berlaku untuk: **fitur baru**, **debugging kompleks**, **refactor signifikan**, **keputusan arsitektur**.

## Prosedur

### 1. Terima & Klarifikasi Problem
Baca deskripsi dari user. Jika belum jelas, tanyakan (satu pesan):
- **Scope**: apa yang masuk dan yang keluar dari scope ini?
- **Constraints**: ada batasan teknis, waktu, atau bisnis?
- **Definition of Done**: seperti apa hasil yang dianggap selesai?
- **Urgency**: apakah ini blocker atau nice-to-have?

Jangan tanya lebih dari 4 pertanyaan. Kalau sudah cukup jelas dari konteks, langsung lanjut.

### 2. Baca Konteks Project
Lakukan **cheap reads** dulu:
```bash
git status --short --branch
```
Baca secara selektif: `CLAUDE.md` (stack, arsitektur), `AGENTS.md` (constraints), file yang kemungkinan terpengaruh.

### 3. Identifikasi Impact Area
Petakan:
- **Files yang kemungkinan terpengaruh** — list spesifik, bukan "banyak file"
- **Shared-file risks** — apakah ada file yang sedang dikerjakan pihak lain?
- **Security surfaces** — apakah menyentuh auth, payment, webhook, input, DB schema?
- **Dependencies** — apakah membutuhkan library baru atau perubahan schema?
- **Breaking changes** — apakah ada behavior yang berubah untuk user/sistem lain?

### 4. Generate Opsi Solusi
Sajikan **2–3 opsi konkret** dengan format:

```
## Opsi A: [Nama Pendekatan]
**Cara kerja:** [1-2 kalimat]
**Keuntungan:** [bullet points]
**Kekurangan / risiko:** [bullet points]
**Kompleksitas:** Rendah / Sedang / Tinggi
**Estimasi effort:** [rough estimate]
```

Jangan hanya satu opsi kecuali memang hanya ada satu pendekatan yang masuk akal.

### 5. Berikan Rekomendasi
Setelah sajikan semua opsi, berikan rekomendasi yang jelas:
```
## Rekomendasi
Pilih **Opsi X** karena: [alasan 2-3 poin, bukan hanya "lebih baik"].
```

### 6. Definisikan Asumsi & Open Questions
```
## Asumsi yang Dibuat
- [asumsi 1] — jika salah, akan mempengaruhi [dampak]
- [asumsi 2]

## Open Questions (perlu dijawab sebelum spec)
- [ ] [pertanyaan yang perlu keputusan user/bisnis]
- [ ] [pertanyaan teknis yang belum bisa dijawab dari codebase]
```

### 7. Output Summary
Tutup dengan:
```
## Next Step
Jika kamu setuju dengan pendekatan ini, jalankan `/spec-writer` untuk membuat
spec formal dari hasil brainstorm ini.

Atau: [alternatif jika ada open question yang perlu dijawab dulu]
```

## Aturan Brainstorm
- **Jangan menulis kode** di fase ini — hanya analisis dan keputusan
- **Jangan langsung implementasi** — output harus berupa keputusan + dokumen
- **Jangan skip open questions** — lebih baik terlambat karena diskusi daripada salah arah
- Jika ada security surface yang terlibat, flag dengan **⚠️ Security surface** dan sertakan pertanyaan security yang relevan

## Output Format
Satu respons terstruktur dengan section:
1. Problem Understanding
2. Impact Area
3. Opsi Solusi (2–3)
4. Rekomendasi
5. Asumsi & Open Questions
6. Next Step
