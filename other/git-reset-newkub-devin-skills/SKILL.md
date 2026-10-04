---
name: git-reset
description: git reset อย่างปลอดภัย — soft/mixed/hard modes เข้าใจผลกระทบก่อนทำ
argument-hint: "[--soft|--mixed|--hard] [ref|paths]"
related:
  - git-restore
  - git-revert
  - git-stash
  - check-git-logs
  - ask-me
  - resolve-errors
---

## Goal

ใช้ `git reset` ย้อน HEAD/index/working tree ถูก mode — เข้าใจว่าแต่ละ mode แตะอะไรก่อนรัน

## Scope

- `--soft` (ย้าย HEAD เท่านั้น), `--mixed` (default — unstage), `--hard` (ลบทิ้ง — destructive)
- reset ไป ref เดิม, uncommit, unstage — ไม่ครอบคลุม `git restore` per-file (ใช้ `/git-restore`)

## Execute

### 1. Know The Modes

> Goal: เลือก mode ที่ตรง intent — reset ผิด mode ทำงานหาย

| Mode | HEAD | Index | Working tree | Use case |
|------|------|-------|--------------|----------|
| `--soft` | ย้าย | เก็บ | เก็บ | รวม commits ล่าสุดเป็น commit เดียว |
| `--mixed` | ย้าย | reset | เก็บ | uncommit แต่เก็บ changes เป็น unstaged |
| `--hard` | ย้าย | reset | reset | ลบทุกอย่างกลับไป ref — **destructive** |

### 2. Safety Check

> Goal: ไม่ทำงานหายและไม่ rewrite shared history

1. `git status` + `git stash list` — ถ้ามี uncommitted work ที่อาจต้องการ → `/git-stash` ก่อน
2. ตรวจว่า commits ที่จะ reset ทิ้ง push ไปแล้วหรือยัง — pushed → ใช้ `/git-revert` แทน
3. บันทึก sha ปัจจุบัน: `git rev-parse HEAD` — reflog กู้ได้แต่มี sha ชัดกว่า

### 3. Reset

> Goal: HEAD ไปถูก ref และ state ตรง mode

```bash
git reset --soft HEAD~1      # uncommit ล่าสุด เก็บทุกอย่าง staged
git reset HEAD~1             # uncommit + unstage (--mixed default)
git reset --hard HEAD~2      # ลบ 2 commits + changes ทิ้ง — confirm ก่อน
git reset --hard origin/main # sync local กับ remote — destructive
```

1. `--hard` ต้อง confirm เสมอ — แจ้งว่าอะไรจะหาย (commits + working changes)
2. reset ไฟล์เดียว: `git reset <path>` (unstage) หรือ `/git-restore` สำหรับ per-file

### 4. Verify And Recover Path

> Goal: state ตรง intent และรู้ทางกลับ

1. `git log --oneline -5` + `git status` — HEAD และ working tree ตรงที่ตั้งใจ
2. กู้กลับ: `git reflog` หา sha เดิม → `git reset --hard <sha>` — reflog เก็บ ~90 วัน
3. ทำ `/run-check` ถ้า reset เปลี่ยน code state

## Rules

- `--hard` = destructive เสมอ — preview + confirm ไม่มีข้อยกเว้น
- pushed commits ห้าม reset — ใช้ `/git-revert` (reset = rewrite public history)
- บันทึก `git rev-parse HEAD` ก่อน reset ทุกครั้ง — recovery path ชัดเจน
- ไม่แน่ใจ → `--soft`/`--mixed` ก่อน (non-destructive) ค่อยขยับ
- ใช้ /ask-me ถ้าจำเป็น

## Expected Outcome

- HEAD/index/working tree อยู่ state ที่ตั้งใจตาม mode ที่เลือก
- ไม่มี committed work หายโดยไม่มี recovery path (sha บันทึกแล้ว)
