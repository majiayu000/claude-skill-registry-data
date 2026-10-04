---
name: list-git
description: List git resources — branches, commits, releases, submodules, tags, worktrees ผ่าน top-level skills
argument-hint: "[domain]"
related:
  - follow-tool-git
  - report
  - ask-me

---

## Goal

Dispatch ไป top-level skill ตาม git resource ที่ต้อง list — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### List Skills

| Domain | Skill |
|---|---|
| `branch` | /list-git-branch — branches + merge status |
| `commit` | /list-git-commit — commit history |
| `release` | /list-git-release — releases |
| `submodules` | /list-git-submodules — submodule status |
| `tags` | /list-git-tags — tags |
| `worktree` | /list-git-worktree — worktrees |

1. ระบุ domain จาก argument (เช่น `/list-git-branch`)
2. ถ้า domain รองรับ → เรียก `/list-<parent>-<domain>` skill แล้วทำตาม flow นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ skill ปลายทาง

- ใช้ /follow-tool-git ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น

## Expected Outcome

- caller ถูก Dispatch ไป top-level skill ที่ตรง domain แล้ว list ตาม flow นั้น
