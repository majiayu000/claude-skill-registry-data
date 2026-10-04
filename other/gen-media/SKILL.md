---
name: gen-media
description: สร้าง media ด้วย AI — images, videos, character consistency, 3D models ผ่าน gen-media-* skills
argument-hint: "[domain]"
related:
  - report-prompt-from-image
  - draw-svg-image
  - convert
  - ask-me
  - report

---

## Goal

Dispatch ไป skill ตาม media domain — parent ทำ routing เท่านั้น

## Scope

- argument คือ domain; ถ้าไม่ระบุ → `/ask-me` เลือก domain

## Execute

### Gen Media Skills

| Domain | Skill |
|---|---|
| `ai-images` | `/gen-media-ai-images` — สร้างรูปภาพด้วย AI ผ่าน bunx CLI |
| `ai-videos` | `/gen-media-ai-videos` — สร้างวิดีโอด้วย AI ผ่าน bunx CLI |
| `image-character` | `/gen-media-image-character` — สร้าง character ที่ consistency |
| `3d-model` | `/gen-media-3d-model` — สร้าง 3D model จาก prompt ด้วย AI CLI |

1. ระบุ domain จาก argument (เช่น `/gen-media ai-images`)
2. ถ้า domain รองรับ → เรียก skill ตามตารางแล้วทำตาม flow ของ skill นั้น
3. ถ้าไม่ระบุหรือไม่รู้จัก domain → `/ask-me` เลือก domain

## Rules

- parent ทำ dispatch เท่านั้น — ห้าม duplicate workflow ของ target skill
- ทุก prompt ที่สร้างต้อง confirm output path ก่อน generate

- ใช้ /report-prompt-from-image ถ้าจำเป็น
- ใช้ /draw-svg-image ถ้าจำเป็น
- ใช้ /convert ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น

## Expected Outcome

- caller ถูก dispatch ไป skill ที่ตรง domain แล้วสร้าง media ตาม flow นั้น
