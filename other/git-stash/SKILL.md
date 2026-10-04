---
name: git-stash
description: จัดการ git stash — push/pop/apply/list อย่างปลอดภัย รองรับ untracked และ named stashes
argument-hint: "[push|pop|apply|list|drop] [name|index]"
related:
  - git-restore
  - git-commit
  - check-uncommit
  - resolve-errors
---

## Goal

จัดการ uncommitted work ด้วย `git stash` — เก็บ changes ชั่วคราว, กู้คืน, เคลียร์ working tree โดยไม่ทำของหาย

## Scope

- stash/push, pop, apply, list, show, drop, clear
- untracked files (`-u`) และ ignored files (`-a`)
- named stashes (`git stash push -m`)
- ไม่ครอบคลุม discard ถาวร → `/git-restore`; committed changes → `/git-revert`

## Execute

### 1. Assess State

> Goal: รู้ว่ามีอะไรจะ stash และมี stash ค้างอยู่ไหม

1. `git status --short` — แยก staged/unstaged/untracked
2. `git stash list` — เช็ค stash เก่าที่ยังไม่ได้ pop (stash ค้าง = debt)
3. ตัดสินใจ: งานสั้นที่จะกลับมาเร็ว → stash; งานที่ควรเก็บถาวร → commit ลง branch แทน

### 2. Stash

> Goal: เก็บ changes อย่างครบและหาได้

1. `git stash push -m "<meaningful message>"` — ตั้งชื่อเสมอ
2. untracked files ต้อง `-u`; ignored files ต้อง `-a` (ระวัง — รวม build output)
3. เฉพาะ staged: `git stash push --staged`; เฉพาะบางไฟล์: `-- <paths>`
4. `git status` verify working tree สะอาดตามที่ตั้งใจ

### 3. Restore

> Goal: เอา changes กลับมาถูก stash ถูกเวลา

1. `git stash list` + `git stash show -p stash@{n}` — ดูเนื้อหาก่อน apply
2. `git stash apply stash@{n}` — ปลอดภัยกว่า pop (stash ยังอยู่ถ้า conflict)
3. `git stash pop` เฉพาะเมื่อมั่นใจว่าไม่ conflict — pop ลบ stash ทันทีหลัง apply สำเร็จ
4. conflict → resolve แล้ว `git stash drop stash@{n}` เองหลัง merge เสร็จ
5. ต้องการ index state เดิม (staged vs unstaged) → `--index`

### 4. Cleanup

> Goal: ไม่สะสม stale stashes

1. `git stash drop stash@{n}` ทีละตัวหลัง apply สำเร็จ
2. `git stash clear` ลบทั้งหมด — ต้อง confirm และ list ก่อนเสมอ

## Rules

- `git stash push -m` เสมอ — ห้าม anonymous stash (หาไม่เจอตอนกลับมา)
- prefer `apply` over `pop` — pop ลบ stash ทันที กู้ยากถ้า conflict แย่
- stash ไม่ใช่ storage ถาวร — งานที่ค้าง >1 วันให้ commit ลง branch
- untracked files ไม่ถูก stash ถ้าไม่ใส่ `-u` — ง่ายต่อการหลงลืม
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Working tree สะอาดตาม intent โดยไม่เสีย uncommitted work
- Stash มีชื่อ หาได้ และไม่สะสม stale entries
