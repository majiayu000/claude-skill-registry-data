---
name: spec-writer
description: >
  Gunakan untuk membuat dokumen spec/design formal dari hasil brainstorm atau deskripsi fitur.
  Trigger: "buat spec untuk X", "tulis design doc", "spec fitur Y", "/spec-writer".
  Output: file spec di docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md — bukan kode.
---

# spec-writer

## Overview
Membuat **dokumen spesifikasi teknis formal** yang menjadi source of truth untuk sebuah fitur atau perubahan. Spec ini menjadi input untuk `/plan-writer` dan referensi selama implementasi.

## When to Use
- Setelah `/brainstorm` menghasilkan keputusan pendekatan
- Saat user meminta design doc / spec formal
- Sebelum memulai implementasi fitur yang menyentuh banyak file atau surface sensitif
- **BUKAN** untuk coding — output hanya dokumen

## Prosedur

### 1. Kumpulkan Input
Baca salah satu (prioritas urut):
1. Output `/brainstorm` dari sesi yang sama (jika baru selesai brainstorm)
2. Deskripsi fitur yang diberikan user
3. Issue / ticket reference yang disebut user

Jika input kurang jelas, tanyakan (max 3 pertanyaan, satu pesan).

### 2. Baca Konteks Project
```bash
git status --short --branch
```
Baca secara selektif:
- `CLAUDE.md` — stack, arsitektur, aturan, pattern yang sudah ada
- `prisma/schema.prisma` atau file ORM — data model existing
- File-file yang kemungkinan terkena dampak
- Spec-spec sebelumnya di `docs/superpowers/specs/` — ikuti format yang konsisten

### 3. Tentukan Nama File
Format: `docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md`

Contoh:
```
docs/superpowers/specs/2026-06-11-dp-down-payment-design.md
docs/superpowers/specs/2026-06-11-reseller-tier-engine-design.md
```

Slug harus deskriptif, lowercase, kebab-case.

### 4. Tulis Spec dengan Struktur Berikut

```markdown
# {Nama Fitur} — Design Spec

**Tanggal:** YYYY-MM-DD
**Status:** Draft | Review | Approved
**Author:** Agent + User

---

## 1. Overview
Ringkasan 2-3 kalimat: apa yang dibangun, mengapa, dan untuk siapa.

## 2. Goals & Non-Goals

### Goals
- [goal 1]
- [goal 2]

### Non-Goals (explicitly out of scope)
- [non-goal 1] — alasan kenapa di-exclude

## 3. User Stories / Use Cases
- Sebagai [role], saya ingin [action], agar [outcome].
- (Gunakan format yang paling cocok — bisa juga scenario-based)

## 4. Technical Design

### 4.1 Data Model
Perubahan schema yang diperlukan. Gunakan format Prisma-style atau table:
```prisma
model NamaModel {
  id        String   @id @default(cuid())
  // ... fields
}
```
Atau: "Tidak ada perubahan schema."

### 4.2 API / Route Contract
| Method | Path | Auth | Request | Response |
|---|---|---|---|---|
| POST | /api/xxx | required | `{ field: type }` | `{ field: type }` |

Atau: Server Actions yang akan dibuat/dimodifikasi.

### 4.3 Business Logic
Aturan bisnis utama, kalkulasi, state transitions. Jelaskan logic yang harus server-side.

### 4.4 UI / UX (jika ada)
Deskripsi flow user. Bisa berupa:
- Step-by-step flow
- State diagram sederhana (mermaid jika perlu)
- Component hierarchy

## 5. Security Considerations
- [ ] Area sensitif apa yang terpengaruh?
- [ ] Validasi apa yang diperlukan?
- [ ] Auth/authorization model?
- [ ] Data exposure risk?

## 6. Testing Strategy
- **Unit tests:** apa yang harus ditest
- **Integration tests:** flow apa yang harus diverifikasi
- **Manual QA:** scenario yang harus dicek browser/device

## 7. Migration & Rollback
- Apakah perlu DB migration? Jika ya, apakah reversible?
- Apakah ada breaking changes? Backward compatibility plan?
- Rollback procedure jika deploy gagal?

## 8. Open Questions
- [ ] [pertanyaan yang perlu dijawab sebelum implementasi]

## 9. Dependencies
- Package baru yang dibutuhkan (jika ada) + justifikasi
- External service yang perlu dikonfigurasi
- File/fitur lain yang jadi dependency

---

## Referensi
- Link ke brainstorm output (jika ada)
- Link ke spec/plan terkait
```

### 5. Adaptasi ke Stack Project
- Jika project menggunakan Prisma → tulis data model dalam format Prisma
- Jika project menggunakan Server Actions → dokumentasikan sebagai Server Actions, bukan REST API
- Jika project menggunakan Zod → contohkan validation schema
- Gunakan naming convention yang sudah ada di project

### 6. Simpan & Report
Simpan spec ke path yang sudah ditentukan di step 3. Jika folder `docs/superpowers/specs/` belum ada, buat.

Tutup dengan:
```
## Next Step
Spec tersimpan di: `docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md`

Untuk lanjut ke implementation plan, jalankan `/plan-writer` dan referensikan spec ini.
```

## Hard Limits
- **Jangan menulis kode implementasi** — hanya spec dokumen
- **Jangan run migrations** — hanya dokumentasikan schema changes yang dibutuhkan
- **Jangan overwrite** spec yang sudah ada — tanyakan user apakah update atau buat baru
- **Jangan skip Security Considerations** — section ini wajib terisi

## Common Mistakes
- **Terlalu abstrak** — spec harus cukup detail untuk agent lain bisa mengimplementasikan tanpa bertanya lagi
- **Skip data model** — selalu definisikan perubahan schema, walau "tidak ada perubahan"
- **Tidak menyebutkan edge cases** — pikirkan: data kosong, concurrent access, error states, partial failure
- **Lupa migration plan** — terutama untuk perubahan schema yang tidak reversible
