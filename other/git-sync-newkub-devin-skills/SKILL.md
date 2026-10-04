---
name: git-sync
description: Sync local repo กับ remote — fetch/pull strategy, submodules และ fork sync
argument-hint: "[pull|fetch|fork] [remote/branch]"
related:
  - git-branch
  - git-rebase
  - git-submodule
  - check-unpush
  - check-uncommit
  - resolve-errors
---

## Goal

Sync local repository กับ remote(s) อย่างปลอดภัย — เลือก pull strategy ถูกต้อง, sync submodules และ forks

## Scope

- `git fetch`/`pull` strategies (merge, rebase, ff-only), `--prune`, `--all`
- submodule sync (`--recurse-submodules`), fork sync (upstream remote)
- push direction → `/git-push`; conflicts → `/check-merge-conflicts`

## Execute

### 1. Assess State

> Goal: รู้ก่อน pull ว่า local ต่างจาก remote ยังไง

1. `git status` — uncommitted changes? → `/git-stash` หรือ commit ก่อน sync
2. `git fetch --all --prune` — เสมอ fetch ก่อนตัดสินใจ (ไม่แตะ working tree)
3. `git log --oneline HEAD..@{u}` และ `@{u}..HEAD` — ดู incoming/outgoing commits
4. diverged (มีทั้งสองฝั่ง) → เลือก strategy ใน step 2

### 2. Choose Pull Strategy

> Goal: เลือกวิธีรวมที่ตรงกับ team convention

| Situation | Command |
|-----------|---------|
| local ไม่มี commits ใหม่ | `git pull --ff-only` — fast-forward เท่านั้น ปลอดภัยสุด |
| diverged, team ใช้ linear history | `git pull --rebase` (ดู `/git-rebase`) |
| diverged, team ใช้ merge commits | `git pull` (merge) |
| ไม่แน่ใจ | `git pull --ff-only` — fail แล้วค่อยเลือก ไม่ auto-merge |

1. `--ff-only` เป็น default ที่ปลอดภัย — fail = diverged จริง ให้เลือก rebase/merge ตาม convention
2. เช็ค `git config pull.rebase` / branch convention ของ project ก่อน

### 3. Sync Extras

> Goal: submodules และ refs อื่นตามไปด้วย

1. `git pull --recurse-submodules` หรือ `git submodule update --init --recursive` หลัง pull (ดู `/git-submodule`)
2. `git fetch --tags` ถ้า release ใช้ tags
3. fork: `git fetch upstream && git merge upstream/main` (หรือ rebase) — upstream remote ต้องมีอยู่ (`git remote -v`)

### 4. Verify

> Goal: local ตรง remote และไม่มีของหาย

1. `git status` — ahead/behind = 0 เทียบ upstream
2. `/check-unpush` — commits local ที่ตั้งใจยังอยู่
3. `git stash list` — ถ้า stash ไว้ก่อน sync → `git stash pop` กลับมา

## Rules

- fetch + inspect ก่อน pull เสมอ — pull ตาบอด = merge conflict ที่ไม่จำเป็น
- uncommitted changes + pull = risky — stash/commit ก่อนเสมอ
- `--ff-only` เมื่อสงสัย — merge commits ที่ไม่ตั้งใจทำ history เลอะ
- `git pull` บน branch ที่ rebase ไว้แล้ว → ต้อง `--rebase` ไม่ใช่ merge
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Local sync กับ remote ด้วย strategy ที่ตรง convention
- Submodules/tags ตามไปครบ ไม่มี uncommitted work เสียหาย
