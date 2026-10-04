---
name: git-clean
description: git clean อย่างปลอดภัย — dry-run ก่อนเสมอ, ลบ untracked/ignored files ตาม scope
argument-hint: "[-fd|-fdx|paths...]"
related:
  - git-restore
  - git-stash
  - check-uncommit
  - cleanup-files-in-project
  - ask-me
---

## Goal

ลบ untracked files ด้วย `git clean` — dry-run ก่อนเสมอ เพราะ untracked files ไม่มีใน git history กู้ไม่ได้

## Scope

- `git clean -fd` (untracked files+dirs), `-fdx` (รวม ignored — build output), `-n` dry-run
- เติม gap ของ `/git-restore` ที่ไม่แตะ untracked files
- cleanup build artifacts/dependency caches ทั่วไป → `/cleanup-files-in-project`

## Execute

### 1. Preview (Dry-Run เสมอ)

> Goal: เห็นทุกไฟล์ที่จะหายก่อนลบจริง

```bash
git clean -nd        # preview untracked files+dirs
git clean -ndx       # preview รวม ignored files (node_modules, dist, ...)
git clean -nd <path> # preview เฉพาะ path
```

1. `-n` (dry-run) ก่อนทุกครั้ง ไม่มีข้อยกเว้น
2. review list — untracked files อาจเป็นงานที่ยังไม่ได้ add (`.env.local`, scratch files, งานใหม่)
3. ไฟล์ที่อาจต้องการ → `git add -N` (intent-to-add ป้องกัน clean) หรือ `/git-stash -u`

### 2. Choose Scope

> Goal: ลบเฉพาะที่ตั้งใจ

| Flag | ลบอะไร |
|------|--------|
| `-fd` | untracked files + dirs |
| `-fdx` | + ignored files (build output, `.env*` ที่ถูก ignore — ระวัง) |
| `-fdX` | เฉพาะ ignored files (เคลียร์ build artifacts โดยเก็บ untracked sources) |
| `<path>` | จำกัดเฉพาะ path |

1. เริ่มจาก scope แคบสุด (`<path>` หรือ `-fdX`) ก่อนขยาย
2. `-fdx` เสี่ยงสุด — ignored files รวม `.env`, local config, IDE files ที่ setup ยาก

### 3. Execute And Verify

> Goal: ลบตรง preview และ repo ยังทำงาน

1. รัน clean ตาม scope ที่เลือก
2. `git status` verify — tracked files ไม่ถูกแตะเสมอ (clean แตะเฉพาะ untracked/ignored)
3. ถ้าลบ ignored deps → reinstall/build ใหม่ (`bun install` ฯลฯ)

## Rules

- `git clean` ไม่มี undo — untracked files ไม่อยู่ใน object store หายถาวร
- `-n` dry-run ก่อนเสมอ + แจ้ง user list ไฟล์ที่จะลบเมื่อ scope กว้าง
- `-x` flag คิดซ้ำสองครั้ง — มันกิน ignored files รวม secrets/config local
- tracked changes ไม่เกี่ยวกับ clean — ใช้ `/git-restore` discard หรือ `/git-stash`
- ใช้ /ask-me ถ้าจำเป็น

## Expected Outcome

- Untracked/ignored files ถูกลบตาม scope ที่ preview แล้ว
- ไม่มีไฟล์สำคัญหายโดยไม่ตั้งใจ
