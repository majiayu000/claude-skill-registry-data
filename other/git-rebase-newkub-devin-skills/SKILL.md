---
name: git-rebase
description: Rebase branch อย่างปลอดภัย — onto main, autosquash fixups, conflict flow ครบ
argument-hint: "[onto-branch|abort|continue]"
related:
  - git-commit
  - git-push
  - check-merge-conflicts
  - check-git-logs
  - resolve-errors
  - run-check
---

## Goal

Rebase commits ไปบน base ใหม่หรือจัดเรียง history ให้สะอาด โดยไม่ทำ shared history พัง

## Scope

- `git rebase <base>` (linearize), `git rebase --onto`, autosquash (`--autosquash` กับ `fixup!`/`squash!` commits)
- conflict resolution flow: continue/abort/skip
- ไม่ครอบคลุม interactive rebase (`-i`) — ใช้ non-interactive equivalents: autosquash, `--onto`, `git reset` + recommit

## Execute

### 1. Safety Check

> Goal: ยืนยันว่า rebase ปลอดภัยก่อนเริ่ม

1. `git status` — working tree ต้องสะอาด (หรือ `/git-stash` ก่อน)
2. ตรวจว่า branch ถูก push/shared หรือยัง — rebase pushed branch = rewrite public history → ต้อง confirm + force-push เท่านั้น และแจ้ง collaborators
3. บันทึก backup ref: `git branch backup/<name>-<date>` ก่อน rebase เสมอ
4. ทำ `/check-merge-conflicts` ประเมิน conflict risk ถ้ามี

### 2. Rebase

> Goal: commits ถูก replay บน base ใหม่

```bash
git fetch origin
git rebase origin/main                    # linearize บน main ล่าสุด
git rebase --onto main <old-base> <branch> # ย้าย commits ข้าม base
git rebase --autosquash origin/main       # รวม fixup!/squash! commits (ต้องตั้ง rebase.autoSquash)
```

1. fetch base ล่าสุดก่อนเสมอ — rebase บน stale base = ทำซ้ำ
2. ไม่แน่ใจ → `--onto` ทีละช่วงเล็กกว่า rebase ทั้ง branch

### 3. Handle Conflicts

> Goal: conflict ถูก resolve ต่อ commit อย่างถูกต้อง

1. conflict → แก้ไฟล์, `git add`, `git rebase --continue`
2. commit นั้นไม่จำเป็นแล้ว → `git rebase --skip`
3. ทุกอย่างพัง → `git rebase --abort` กลับไป pre-rebase state เสมอได้
4. rebase นาน/conflict เยอะ → พิจารณา merge แทน (conflict resolve ครั้งเดียว)

### 4. Verify

> Goal: history สะอาดและ code ไม่แตก

1. `git log --oneline origin/main..HEAD` — commits เรียงตรง ไม่มี merge commit ปน
2. ทำ `/run-check` — semantic conflicts ไม่โผ่ใน `git status`
3. ถ้า branch push แล้ว → `git push --force-with-lease` เท่านั้น (ห้าม `--force`)

## Rules

- ห้าม rebase commits ที่คนอื่น base งานอยู่ (public history) — golden rule of rebasing
- backup branch ก่อน rebase เสมอ — reflog มีแต่ backup ชัดกว่า
- `--force-with-lease` เท่านั้นเมื่อ push หลัง rebase — ป้องกัน overwrite งานคนอื่น
- rebase = rewrite — ถ้า PR กำลัง review อยู่และ reviewers ดู history → แจ้งก่อน
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Branch linear บน base ล่าสุด history สะอาด
- ไม่มี lost commits (backup ref + reflog) และผ่าน `/run-check`
