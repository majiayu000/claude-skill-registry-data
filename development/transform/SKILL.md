---
name: transform
description: Transformation dispatcher — เปลี่ยน code/data/config หลายจุดด้วย scripts, ast-grep หรือ converters ตามชนิดงาน
argument-hint: "[target|pattern]"
related:
  - use-scripts
  - edit-with-use-scripts
  - use-astgrep
  - edit-relative
  - convert-files-format
  - replace
  - refactor
  - migration-with-astgrep
  - run-verify
  - report
---

## Goal

เลือก transformation path ที่ถูกต้องสำหรับงาน "เปลี่ยน X เป็น Y หลายจุด" — AST-based, script-based หรือ format conversion — ทุก path บังคับ dry-run/preview + confirm ก่อนเขียนจริง

## Scope

- ครอบคลุมการ classify และ dispatch งาน transformation — mechanics อยู่ใน routed skills ไม่ duplicate
- ไม่ครอบคลุม rename/move ไฟล์ (`/rename`, `/move-to`) หรือ refactor semantics (`/refactor`) — ใช้เป็น route เท่านั้น

## Execute

### 1. Classify Transformation

> Goal: เลือก route ที่ตรงชนิดงาน

| งาน | Route |
|-----|-------|
| แก้ไขหลายไฟล์ผ่าน script — reproducible, audit trail | `/edit-with-use-scripts` → `/use-scripts` (`### Edit Files Via Scripts`) |
| AST pattern rewrite หลายไฟล์ (`-p`/`-r`, dry-run + confirm) | `/use-astgrep rewrite` (alias `/edit-by-astgrep`) |
| rule-YAML transforms (`transform`/`rewriters`/constraints) | `/use-astgrep transform` |
| migration ทั้ง codebase แบบ staged batches | `/use-astgrep migration` → `/migration-with-astgrep` |
| format conversion (json↔yaml, cjs→esm, svg, scripts) | `/convert-files-format` หรือ `/convert` domain |
| ไฟล์เดียว/จุดน้อยๆ ไม่ต้อง reproducible | `/edit-only` หรือ `/replace` |
| config values ตาม defaults/overrides | `/edit-manual` + `/follow-default-config` |
| semantic refactor (extract, rename symbols, architecture) | `/refactor` |

1. ระบุ intent + target scope จาก argument
2. ถ้าเข้าได้หลาย route → เลือก AST route เมื่อเป็น structural code change, script route เมื่อ logic ไม่ใช่ AST pattern, manual เมื่อจุดน้อย
3. ถ้าไม่ชัด → ทำ `/ask-me`

### 2. Run Routed Skill

> Goal: execute เต็ม workflow ของ route ที่เลือก

1. อ่าน SKILL.md ของ route แล้วทำตาม flow — ห้ามทำแบบย่อจากตารางนี้
2. ทุก route ต้อง dry-run/preview + user confirm ก่อนเขียนจริง — ถ้า route ไม่ได้บังคับให้บังคับเอง
3. เริ่ม scope แคบก่อนขยาย — fail fast ลด rework

### 3. Verify And Update References

> Goal: transformation ไม่พังและ references สอดคล้อง

1. Re-run pattern/check เดิม → 0 leftovers (ยกเว้น intentional)
2. ทำ `/run-verify` — lint/typecheck/scan ผ่าน
3. ถ้า rename/move ไฟล์หรือเปลี่ยน public API → ทำ `/edit-relative` + `/update-references`
4. ทำ `/report` table: `No.`, `Target`, `Route`, `Changes`, `Status`

## Rules

- ห้าม transform แบบเขียนทับทันที — dry-run/preview + confirm ก่อนเสมอทุก route
- Transform = เปลี่ยนเนื้อหาในไฟล์ — ถ้างานคือย้าย/rename ไฟล์ → `/rename`, `/move-to`
- ถ้า transformation ต้องรันซ้ำประจำ → promote เป็น rule (`/update-astgrep-rules`) หรือ permanent script (`.devin/scripts/`) ไม่ใช่ทำซ้ำมือ
- ใช้ `/ask-me` ถ้าจำเป็น

## Expected Outcome

- Transformation ถูก route ไป skill ที่ถูกต้องและ execute ครบ
- ทุก write ผ่าน preview + confirm; verify ผ่าน; references อัปเดตครบ
- Report ชัดเจน: route ที่ใช้, files changed, leftovers
