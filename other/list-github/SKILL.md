---
name: list-github
description: List GitHub resources — branches, issues, PRs, projects, releases ผ่าน top-level skills
argument-hint: "[domain]"
related:
  - all-github-repo
  - report
  - ask-me

---

## Goal

Dispatch ไป top-level skill ตาม GitHub resource ที่ต้อง list — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### List Skills

| Domain | Skill |
|---|---|
| `branch` | /list-github-branch — branches ใน repo |
| `issue` | /list-github-issue — issues พร้อม filter |
| `pr` | /list-github-pr — pull requests พร้อม status |
| `project` | /list-github-project — GitHub projects |
| `release` | /list-github-release — releases |
| `repo` | /list-github-repo — repositories |
| `star` | /list-github-star-latest — starred repos |

1. ระบุ domain จาก argument (เช่น `/list-github-pr`)
2. ถ้า domain รองรับ → เรียก `/list-<parent>-<domain>` skill แล้วทำตาม flow นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ skill ปลายทาง
- ใช้ `gh` CLI หรือ GitHub MCP tools ตามที่ available

- ใช้ /all-github-repo ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น

## Expected Outcome

- caller ถูก Dispatch ไป top-level skill ที่ตรง domain แล้ว list ตาม flow นั้น
