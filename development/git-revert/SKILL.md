---
name: git-revert
description: Revert commits อย่างปลอดภัยด้วย inverse commit ใหม่ — ไม่ rewrite history
argument-hint: "[sha|range|merge-sha]"
related:
  - git-commit
  - git-push
  - check-git-logs
  - git-file-history
  - check-merge-conflicts
  - run-check
  - resolve-errors
---

## Goal

ย้อนผลของ commit(s) ด้วย `git revert` — สร้าง inverse commit ใหม่แทนการ rewrite history ปลอดภัยสำหรับ commits ที่ push แล้ว

## Scope

- revert commit เดียว, range ของ commits หรือ merge commit
- ใช้เมื่อต้องย้อน change ที่ push ไปแล้ว — ถ้ายังไม่ push และต้องการลบ commit จริง → พิจารณา `/restore-files` หรือ reset (ต้อง confirm)
- ไม่ครอบคลุมการย้อน uncommitted changes — ใช้ `/git-restore` แทน

## Execute

### 1. Identify Target

> Goal: หา commit(s) ที่จะ revert ชัดเจน

1. ถ้า user ให้ sha/range → ใช้ตรงๆ; ถ้าไม่ → ทำ `/check-git-logs` หา commit เป้าหมาย
2. ดูเนื้อหาด้วย `git show <sha>` — ยืนยันว่าเป็น change ที่ต้องย้อนจริง
3. ตรวจว่า commit เป็น merge commit หรือไม่ (`git show` ดู `Merge:` header) และว่า commits ถัดมาแตะไฟล์เดียวกันหรือไม่ (conflict risk)

### 2. Dry-Run Preview

> Goal: รู้ผลลัพธ์ก่อนเขียน commit ใหม่

1. `git revert --no-commit <sha>` แล้ว `git diff --cached` ดู inverse change
2. ถ้า conflict → `git revert --abort` แล้ววางแผนใหม่ หรือ resolve ตาม step 3
3. `git reset` เพื่อล้าง staged state หลัง preview (ถ้ายังไม่พร้อม commit)

### 3. Revert

> Goal: สร้าง inverse commit ที่ถูกต้อง

1. commit เดียว: `git revert <sha>` — message auto-generated, แก้ได้ตาม conventional commits ของ project
2. range: `git revert <oldest>^..<newest>` หรือ `--no-commit` ทีละตัวแล้ว squash message เดียวถ้าเป็น change ชุดเดียว
3. merge commit: `git revert -m 1 <merge-sha>` (parent 1 = mainline) — ระบุ mainline ให้ถูก ไม่เดา
4. ถ้า conflict: แก้ไฟล์, `git add`, `git revert --continue` — ยกเลิกด้วย `git revert --abort` เสมอได้

### 4. Verify And Report

> Goal: working tree กลับสู่ state ก่อน commit นั้น และ build ผ่าน

1. `git show HEAD` ตรวจ inverse diff; เทียบ tree กับ `git diff <sha>^ HEAD` ถ้า revert ล่าสุดพอดี
2. ทำ `/run-check` — revert ทำให้ build/test แตกได้ (commits ถัดมาอาจพึ่ง code ที่ถูกย้อน)
3. รายงานด้วย `/report`: commits ที่ revert, conflicts, ไฟล์ที่แตะ

## Rules

- ห้าม `git reset`/`rebase` เพื่อย้อน commits ที่ push ไปแล้ว — ใช้ revert เสมอ (history เป็น public)
- merge commit ต้อง `-m 1` (หรือ parent ที่ถูกต้อง) — ห้าม revert merge โดยไม่ระบุ parent
- revert commits ถัดกันหลายตัว → revert จากใหม่ไปเก่าเพื่อลด conflicts
- ถ้า revert แตก test/build → ทำ `/resolve-errors` — ห้าม commit revert ที่ทำให้ main พังเงียบๆ
- revert ของ revert = re-apply — ถ้าจะนำ change กลับมา ให้ revert ตัว revert commit ไม่ cherry-pick เดิมซ้ำ
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Inverse commit(s) ถูกสร้าง — history เส้นตรงไม่ถูก rewrite
- Working tree กลับไป state ก่อน change เป้าหมาย และผ่าน `/run-check`
