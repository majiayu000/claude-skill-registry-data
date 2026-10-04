---
name: run-format
description: ฟอร์แมตโค้ดและแก้ไขปัญหาจาก formatter
argument-hint: "[scope]"
related:
  - deep-review
  - convert
  - follow-best-practice
  - suggest-next-action
  - run-check
  - run-verify
  - resolve-errors
  - run-lint
  - run-drizzle-studio
---

## Goal

ฟอร์แมตโค้ดและแก้ไขปัญหาจาก formatter ให้ผ่านทั้งหมด

## Scope

รัน format สำหรับทุก project types และจัดการ errors/warnings จาก formatter

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (format)

### 1. Check Formatter Config

> Goal: Check Formatter Config

ตรวจสอบ formatter ที่ใช้ใน project

1. ตรวจสอบ `biome.jsonc` สำหรับ Biome
2. ตรวจสอบ `dprint.jsonc` สำหรับ dprint
3. ตรวจสอบ `.prettierrc` สำหรับ Prettier
4. ตรวจสอบ scripts ใน `package.json`

### 2. Run Format Command

> Goal: Run Format Command

รัน formatter command ตามที่ตั้งค่าไว้

1. ถ้าใช้ Biome: รัน `biome format --write` (ห้ามใช้ `--unsafe` flag)
2. ถ้าใช้ dprint: รัน `dprint fmt`
3. ถ้าใช้ Prettier: รัน `prettier --write`
4. ใช้ script จาก `package.json` ถ้ามี
5. รอให้ format เสร็จสิ้นก่อนดำเนินการต่อ

### 3. Analyze Format Issues

> Goal: Analyze Format Issues

วิเคราะห์ปัญหาที่เกิดจาก formatter

1. ตรวจสอบ output จาก formatter
2. ตรวจสอบประเภทของ issues:
   - syntax errors
   - config-related errors
   - unsupported files
   - format violations
3. ระบุ files ที่มีปัญหา

### 4. Fix Config Issues

> Goal: Fix Config Issues

แก้ไขปัญหาที่เกี่ยวกับ config

1. ถ้าเป็น config-related errors ให้ทำ `formatter` เพื่อแก้ config
2. ปรับ formatter config ให้เหมาะสมกับ codebase
3. ปรับ rules ที่เหมาะสมกับ project
4. รัน format อีกครั้งเพื่อทดสอบ

### 5. Fix Code Issues

> Goal: Fix Code Issues

แก้ไขปัญหาที่เกิดใน code

1. แก้ syntax errors ก่อน format
2. แก้ format violations ตามลำดับความสำคัญ
3. จัดการ files ที่ไม่รองรับ
4. รัน format ซ้ำจนไม่มี errors

### 6. Verify

> Goal: Verify

ตรวจสอบผลลัพธ์

1. รัน format อีกครั้งเพื่อยืนยัน
2. ตรวจสอบว่าไม่มี format errors เหลือ
3. ตรวจสอบว่าทุก files ถูก format แล้ว
4. รัน lint ตามด้วยเพื่อยืนยัน

## Rules

### 1. Config Adjustments

พยายามแก้ config ก่อนแก้ code เสมอ

- ปรับ formatter config ให้เหมาะสมกับ codebase
- ปรับ rules ที่เหมาะสมกับ project
- ใช้ `formatter` เพื่อแก้ config อย่างถูกต้อง
- หลีกเลี่ยงการปิด rules โดยไม่จำเป็น

### 2. Syntax Errors

แก้ syntax errors ก่อน format เสมอ

- ตรวจสอบ syntax errors ก่อนรัน format
- แก้ syntax errors ให้ครบถ้วน
- ใช้ linter ช่วยตรวจสอบ syntax
- รัน format หลังจาก syntax ถูกต้อง

### 3. Format Scope

กำหนด scope สำหรับการ format

- Format ทั้ง project โดย default
- ใช้ glob patterns สำหรับ specific files
- ใช้ `--write` flag สำหรับ auto-fix
- ใช้ `--check` flag สำหรับ CI

### 4. Verification

ตรวจสอบว่า code ทำงานได้ปกติ

- รัน format อีกครั้งเพื่อยืนยัน
- รัน lint ตามด้วย
- ตรวจสอบว่าไม่มี regressions
- ห้ามใช้ `--unsafe` flag กับ biome commands

- ใช้ /convert-files-format ถ้าจำเป็น
- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /run-check ถ้าจำเป็น
- ใช้ /run-verify ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น
- ใช้ /run-lint ถ้าจำเป็น
- ใช้ /run-drizzle-studio ถ้าจำเป็น

## Expected Outcome

โค้ดที่ผ่าน format โดยไม่มี format errors พร้อมรายงานผลลัพธ์การรัน format
