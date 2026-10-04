---
name: git-amend
description: Amend commit ล่าสุดอย่างปลอดภัย — เช็ค pushed ก่อน, staged changes และ message edit
argument-hint: "[--no-edit|message]"
related:
  - git-commit
  - git-push
  - git-rebase
  - check-git-logs
  - ask-me
---

## Goal

แก้ commit ล่าสุดด้วย `git commit --amend` — เพิ่ม changes หรือแก้ message — โดยไม่ rewrite pushed history

## Scope

- amend staged changes เข้า commit ล่าสุด, แก้ commit message, `--no-edit`
- ครอบคลุมเฉพาะ HEAD commit — แก้ commit เก่ากว่านั้น → `/git-rebase` (autosquash)

## Execute

### 1. Safety Check

> Goal: ยืนยันว่า amend ไม่ rewrite public history

1. `git status` — commit ล่าสุด push ไปแล้วหรือยัง (`git status` บอก ahead/behind, หรือ `git log origin/<branch>..HEAD`)
2. pushed แล้ว → ห้าม amend — สร้าง commit ใหม่ หรือ `/git-revert` ถ้าต้องย้อน
3. ถ้ามีคนอื่นอาจ pull branch นี้แล้ว → ห้าม amend เช่นกัน

### 2. Stage And Amend

> Goal: change/message ที่แก้รวมเข้า commit เดิม

```bash
git add <files>
git commit --amend --no-edit      # เพิ่ม changes ไม่แก้ message
git commit --amend -m "new msg"   # แก้ message
git commit --amend                # แก้ทั้งคู่ (เปิด editor)
```

1. stage เฉพาะ changes ที่เป็นของ commit นั้น — amend รวม staged ทั้งหมด
2. amend เปลี่ยน sha — commits ที่ depend on sha เดิม (cherry-picks, notes) อ้างอิงเก่า

### 3. Verify

> Goal: commit ถูกต้องและ history สะอาด

1. `git show HEAD` — เนื้อหา + message ตรง intent
2. `git log --oneline -3` — ไม่มี duplicate/broken commits
3. ถ้า branch push อยู่แล้วและจำเป็นต้อง amend (เช่น local-only branch ที่ push preview) → `git push --force-with-lease` เท่านั้น

## Rules

- amend เฉพาะ commit ที่ยังไม่ push เท่านั้น — pushed = rewrite public history
- `--force-with-lease` เท่านั้นถ้าต้อง push หลัง amend — ห้าม `--force`
- อย่า amend เพื่อแก้ change ที่ควรเป็น commit ใหม่ — amend คือแก้ commit เดิม ไม่ใช่หลบ history ใหม่
- amend ขณะ rebase/merge กำลังค้าง → resolve state นั้นก่อน
- ใช้ /ask-me ถ้าจำเป็น

## Expected Outcome

- HEAD commit มี changes/message ที่ถูกต้อง sha ใหม่
- ไม่มี shared history ถูก rewrite
