---
name: list-devin
description: List Devin resources — hooks, MCP, skills, subagents, sessions ผ่าน top-level skills
argument-hint: "[domain]"
related:
  - update-devin-global-skills
  - follow-devin-global-skills
  - report
  - ask-me

---

## Goal

Dispatch ไป top-level skill ตาม Devin resource ที่ต้อง list — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### List Skills

| Domain | Skill |
|---|---|
| `global-hooks` | /list-devin-global-hooks — global hooks config |
| `global-mcp` | /list-devin-global-mcp — global MCP servers |
| `global-skills` | /list-devin-global-skills — global skills catalog |
| `global-subagents` | /list-devin-global-subagents — global subagent profiles |
| `session` | /list-devin-session — Devin sessions |
| `user-requests` | /list-request-devin-session — user request history |

1. ระบุ domain จาก argument (เช่น `/list-devin-global-skills`)
2. ถ้า domain รองรับ → เรียก `/list-<parent>-<domain>` skill แล้วทำตาม flow นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ skill ปลายทาง
- output ต้องเป็นตารางผ่าน `/report` ตาม convention ของ skill ปลายทาง

- ใช้ /update-devin-global-skills ถ้าจำเป็น
- ใช้ /follow-devin-global-skills ถ้าจำเป็น

## Expected Outcome

- caller ถูก Dispatch ไป top-level skill ที่ตรง domain แล้ว list ตาม flow นั้น
