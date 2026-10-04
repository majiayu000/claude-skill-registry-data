---
name: cleanup
description: ล้าง resources ที่ไม่ใช้ — branches, worktrees, docker, github issues ผ่าน top-level skills
argument-hint: "[domain]"
related:
  - cleanup-files-in-project
  - cleanup-files-in-computer
  - run-cleanup
  - ask-me

---

## Goal

Dispatch ไป skill ปลายทาง ตาม domain ของ cleanup — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### Skills

| Domain | Skill |
|---|---|
| `artifact` | /cleanup-artifact — build artifacts + dependency caches (Rust CLI, dry-run ก่อน) |
| `branches-merged` | /cleanup-branches-merged — local branches ที่ merge แล้ว |
| `docker` | /cleanup-docker — images, containers, volumes ที่ไม่ใช้ |
| `git-branch` | /cleanup-git-branch — stale/orphan branches |
| `github-issue` | /cleanup-github-issue — issues ที่เก่าหรือ resolve แล้ว |
| `worktree` | /cleanup-worktree — git worktrees ที่ไม่ใช้ |

1. ระบุ domain จาก argument (เช่น `/cleanup-worktree`)
2. ถ้า domain รองรับ → ทำตาม `/cleanup-<domain>` ทั้ง flow
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ skill ปลายทาง
- ทุก cleanup ต้อง dry run + user confirm ก่อนลบจริง (ตาม rule ของ skill ปลายทาง)

- ใช้ /cleanup-files-in-project ถ้าจำเป็น
- ใช้ /cleanup-files-in-computer ถ้าจำเป็น
- ใช้ /run-cleanup ถ้าจำเป็น

## Expected Outcome

- caller ถูก dispatch ไป skill ปลายทาง ที่ตรง domain แล้ว cleanup ตาม flow นั้น
