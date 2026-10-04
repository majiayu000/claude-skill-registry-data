---
name: convert
description: แปลง format/structure — esm, files, git submodules, scripts, svg ผ่าน convert-* skills
argument-hint: "[domain]"
related:
  - refactor
  - migration-with-astgrep
  - update-references
  - run-format
  - ask-me

---

## Goal

Dispatch ไป skill ตาม domain ของ conversion — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### Convert Skills

| Domain | Skill |
|---|---|
| `esm` | `/convert-esm` — CJS → ESM migration |
| `files-format` | `/convert-files-format` — แปลง file format (json/yaml/toml ฯลฯ) |
| `git-submodules` | `/convert-git-submodules` — directory → git submodule |
| `scripts` | `/convert-scripts` — แปลง commands เป็น runnable scripts |
| `svg` | `/convert-svg` — image → SVG conversion |
| `lang-en` | `/convert-to-lang-en` — แปลง output/report เป็นภาษาอังกฤษ |
| `lang-th` | `/convert-to-lang-th` — แปลง output/report เป็นภาษาไทย |

1. ระบุ domain จาก argument (เช่น `/convert esm`)
2. ถ้า domain รองรับ → เรียก skill ตามตารางแล้วทำตาม flow ของ skill นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ target skill
- conversion ที่แตะไฟล์ที่มี references → `/update-references` เสมอ

- ใช้ /refactor ถ้าจำเป็น
- ใช้ /migration-with-astgrep ถ้าจำเป็น
- ใช้ /run-format ถ้าจำเป็น

## Expected Outcome

- caller ถูก dispatch ไป skill ที่ตรง domain แล้วแปลงตาม flow นั้น
