---
name: plan-writer
description: >
  Gunakan untuk membuat implementation plan dari spec dokumen. Memecah spec menjadi task list 
  yang executable dengan dependency order, file manifest, dan validation steps.
  Trigger: "buat implementation plan", "planning untuk spec X", "breakdown task", "/plan-writer".
  Output: file plan di docs/superpowers/plans/YYYY-MM-DD-{slug}.md — bukan kode.
---

# plan-writer

## Overview
Mengkonversi **spec/design doc** menjadi **implementation plan** yang executable — task list terurut, dependency-aware, dengan file manifest yang jelas. Plan ini adalah kontrak eksekusi: agent (atau developer) bisa mengikutinya tanpa perlu bertanya lagi.

## When to Use
- Setelah `/spec-writer` menghasilkan spec yang sudah di-approve user
- Saat user meminta breakdown implementasi dari deskripsi fitur
- Sebelum implementasi fitur yang menyentuh > 3 file
- **BUKAN** untuk coding — output hanya dokumen plan

## Prosedur

### 1. Baca Spec & Konteks
Baca:
1. Spec dokumen di `docs/superpowers/specs/` yang relevan
2. `CLAUDE.md` — stack, arsitektur, aturan, pattern existing
3. File-file yang akan terpengaruh (quick read, bukan deep dive)

```bash
git status --short --branch
```

Jika tidak ada spec yang dirujuk, tanya user spec mana yang jadi dasar. Jika user mau langsung plan tanpa spec, lakukan mini-spec inline (4-5 poin scope + data model + API contract) sebelum lanjut ke plan.

### 2. Tentukan Nama File
Format: `docs/superpowers/plans/YYYY-MM-DD-{slug}.md`

Slug harus sama atau mirip dengan slug spec (jika ada).

### 3. Tulis Plan dengan Struktur Berikut

```markdown
# {Nama Fitur} — Implementation Plan

**Tanggal:** YYYY-MM-DD
**Spec:** `docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md`
**Status:** Draft | Approved | In Progress | Done

---

## Scope Summary
Ringkasan 3-5 poin dari spec: apa yang akan diimplementasikan.

## Task Breakdown

Urutkan berdasarkan **dependency order** — task yang jadi prerequisite duluan.

### Task 1: {Nama Task — layer paling dasar}
**Files:**
- `[NEW] path/to/new-file.ts` — deskripsi singkat
- `[MODIFY] path/to/existing-file.ts` — apa yang berubah

**Detail:**
- [langkah implementasi 1]
- [langkah implementasi 2]

**Validation:**
```bash
npx tsc --noEmit
```

**Depends on:** — (tidak ada dependency / task N)

---

### Task 2: {Nama Task}
...

---

### Task N: {Nama Task — layer paling atas}
...

---

## File Manifest (Complete)

Ringkasan semua file yang terpengaruh, grouped by component:

### {Component/Feature Name}
| Action | File | Description |
|---|---|---|
| NEW | `path/to/file.ts` | deskripsi |
| MODIFY | `path/to/file.ts` | apa yang berubah |
| DELETE | `path/to/file.ts` | alasan |

### {Component/Feature Name 2}
...

## Shared-File Risks
File-file yang mungkin sedang dikerjakan pihak lain atau dipakai banyak fitur:
- `path/to/shared-file.ts` — risiko: [deskripsi]
- "Tidak ada shared-file risk." (jika memang tidak ada)

## Validation Plan

### Automated
```bash
npx tsc --noEmit        # type safety
npm run lint             # code style
npm run build            # production build
npm test                 # unit tests (jika ada)
```

### Manual QA
- [ ] [scenario yang harus dicek manual]
- [ ] [flow end-to-end yang harus diverifikasi]

## Security Review Checklist
- [ ] Dispatch `security-reviewer` agent setelah task yang menyentuh surface sensitif
- [ ] Dispatch `typescript-reviewer` setelah semua task TS selesai
- [ ] [checklist spesifik fitur ini]

## Rollback Notes
- Migration reversible? Jika tidak, apa fallback-nya?
- Perlu feature flag? Jika ya, nama flag dan default value.
- Rollback steps jika deploy gagal: [langkah konkret]

## Estimated Order of Execution
1. Task 1 → commit: `feat(scope): ...`
2. Task 2 → commit: `feat(scope): ...`
3. ...
4. Final validation → dispatch reviewers → commit: `chore(scope): ...`
```

### 4. Tentukan Dependency Graph
Untuk setiap task, tentukan:
- **Depends on:** task mana yang harus selesai dulu
- **Blocks:** task mana yang menunggu ini selesai

Jika ada task yang bisa diparallelkan, tandai:
```
Task 2 dan Task 3 bisa dikerjakan paralel setelah Task 1 selesai.
```

### 5. Adaptasi ke Project Conventions
- Gunakan naming convention commit dari `CLAUDE.md` (Conventional Commits)
- Ikuti folder structure yang sudah ditetapkan (`server/repositories/`, `server/services/`, dll)
- Jika project punya konvensi test (vitest, jest, playwright), sebutkan di validation

### 6. Simpan & Report
Simpan plan ke path yang sudah ditentukan. Jika folder `docs/superpowers/plans/` belum ada, buat.

Tutup dengan:
```
## Next Step
Plan tersimpan di: `docs/superpowers/plans/YYYY-MM-DD-{slug}.md`

Setelah kamu approve plan ini, saya akan mulai implementasi dari Task 1.
Atau: ada yang perlu diubah/dipecah lebih detail?
```

## Prinsip Plan yang Baik
1. **Setiap task bisa di-commit sendiri** — jangan buat task yang terlalu besar untuk satu commit
2. **File manifest harus lengkap** — tidak boleh ada file yang "muncul tiba-tiba" saat implementasi
3. **Validation di setiap task** — bukan hanya di akhir
4. **Dependency order yang benar** — schema/migration dulu, lalu repository, lalu service, lalu UI
5. **Jangan gabung concern yang berbeda** — misalnya migration + UI dalam satu task

## Hard Limits
- **Jangan menulis kode implementasi** — hanya plan dokumen
- **Jangan run migrations atau build** — hanya dokumentasikan
- **Jangan overwrite** plan yang sudah ada tanpa konfirmasi
- **Jangan skip validation plan** — setiap plan harus punya cara verifikasi

## Common Mistakes
- **Task terlalu besar** — jika task butuh > 5 file changes, pecah lagi
- **Lupa dependency order** — migration harus sebelum repository, repository sebelum service
- **File manifest tidak lengkap** — review sebelum finalize, pastikan semua file tercantum
- **Tidak menyebutkan commit message** — setiap task harus punya suggested commit message
- **Skip security review** — selalu sertakan kapan dispatch `security-reviewer`
