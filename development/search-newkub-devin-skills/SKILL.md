---
name: search
description: ค้นหาข้าม sources — files, GitHub stars, npmx, Raindrop, MCP, skills, drive D ผ่าน search-* skills
argument-hint: "[domain]"
related:
  - follow-tool-crw
  - learn
  - use-astgrep
  - ask-me
  - report

---

## Goal

Dispatch ไป skill ตาม search source — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### Search Skills

| Domain | Skill |
|---|---|
| `files-patterns` | `/search-files-patterns` — ค้นไฟล์ตาม pattern/glob |
| `github-star` | `/search-github-star` — ค้นใน GitHub starred repos |
| `mcp` | `/search-mcp` — ค้น MCP servers |
| `npmx` | `/search-npmx` — ค้น/เปรียบเทียบ npm packages บน npmx.dev |
| `project-in-drive-d` | `/search-project-in-drive-d` — ค้น project ใน drive D |
| `raindrop` | `/search-raindrop` — ค้น bookmarks ผ่าน raindrop CLI |
| `similar` | `/search-similar` — ค้น code/files ที่คล้ายกัน |
| `skills` | `/search-skills` — ค้น skills ที่เกี่ยวข้อง |

1. ระบุ domain จาก argument (เช่น `/search npmx`)
2. ถ้า domain รองรับ → เรียก skill ตามตารางแล้วทำตาม flow ของ skill นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ target skill
- ถ้าต้อง research เชิงลึกหลังเจอ source → ต่อด้วย `/learn-from-web` หรือ `/deep-research`

- ใช้ /follow-tool-crw ถ้าจำเป็น
- ใช้ /use-astgrep ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น

## Expected Outcome

- caller ถูก dispatch ไป skill ที่ตรง source แล้วค้นตาม flow นั้น
