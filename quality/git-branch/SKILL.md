---
name: git-branch
description: สร้าง/สลับ/rename branch ตาม convention — upstream tracking และ cleanup local branches
argument-hint: "[create|switch|rename|cleanup] [name]"
related:
  - git-commit
  - git-push
  - cleanup-git-branch
  - delete-git-branch
  - check-unpush
  - ask-me
---

## Goal

จัดการ branches ตาม convention — naming ชัดเจน, upstream tracking ถูกต้อง, local branches ไม่สะสม

## Scope

- create (`git switch -c`/`branch`), switch, rename (`-m`), upstream (`-u`), list/prune local
- delete → `/delete-git-branch`; merged cleanup → `/cleanup-git-branch` (skill นี้ครอบคลุม create/manage)
- worktree branches → `/git-worktree`

## Execute

### 1. Choose Name

> Goal: branch name สื่อ scope และตาม convention

1. convention ทั่วไป: `<type>/<scope>-<short-desc>` — `feat/`, `fix/`, `chore/`, `refactor/` เช็ค `git branch -a` ดู convention ของ repo ก่อน
2. lowercase + hyphens, ไม่มี spaces/special chars, สั้นแต่อ่านรู้เรื่อง
3. ถ้า repo มี lint rules สำหรับ branch names (CI checks) → ทำตามนั้น

### 2. Create And Switch

> Goal: branch ใหม่ branch จาก base ที่ถูกต้อง

```bash
git switch -c <name>                    # จาก HEAD ปัจจุบัน
git switch -c <name> origin/main        # จาก main ล่าสุด — fetch ก่อนเสมอ
git switch <name>                       # สลับไป branch ที่มีอยู่
```

1. `git fetch origin` ก่อน branch จาก remote base — ห้าม branch จาก stale local
2. ยืนยัน starting point ถูก — branch จาก feature branch อื่นโดยไม่ตั้งใจ = dependency ซ่อน

### 3. Track And Push

> Goal: upstream ตั้งถูกและ push ครั้งแรกถูกต้อง

1. `git push -u origin <name>` ครั้งแรก — ตั้ง upstream ทำให้ `git push`/`git status` ทำงานถูก
2. `/check-unpush` ตรวจ branches ที่ยังไม่มี upstream
3. ชื่อ remote branch ตรง local — ห้าม push ไปชื่ออื่นยกเว้นมีเหตุ

### 4. Rename And Prune

> Goal: แก้ชื่อผิดและเคลียร์ local refs

1. `git branch -m <old> <new>` — rename; ถ้า push แล้วต้อง push ชื่อใหม่ + ลบ remote เก่า + reset upstream
2. `git fetch --prune` — เคลียร์ remote-tracking refs ที่ remote ลบไปแล้ว
3. local branches ที่ merged → `/cleanup-git-branch`; ที่ไม่ใช้ → `/delete-git-branch` (dry-run ก่อน)

## Rules

- branch จาก base ล่าสุดเสมอ — `git fetch` ก่อน `switch -c`
- rename pushed branch = สร้างใหม่ + ลบเก่า — แจ้ง collaborators
- ไม่ทำงานบน `main`/`master` โดยตรง — สร้าง feature branch เสมอ
- local branches ค้าง >สัปดาห์ → review ด้วย `/cleanup-git-branch`
- ใช้ /ask-me ถ้าจำเป็น

## Expected Outcome

- Branch ตาม naming convention, track upstream ถูกต้อง
- ไม่มี stale local refs สะสม
