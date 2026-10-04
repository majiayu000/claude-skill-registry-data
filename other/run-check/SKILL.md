---
name: run-check
description: รัน lint, typecheck และ scan เพื่อตรวจสอบคุณภาพ
argument-hint: "[scope]"
related:
  - deep-review
  - run-lint
  - run-typecheck
  - run-scan

---

## Goal

รัน lint, typecheck และ scan เพื่อตรวจสอบคุณภาพ

## Scope

ใช้ `run-check` สำหรับ tasks และ workflows เฉพาะที่ครอบคลุม (check)

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (check)

### 1. Run Lint

> Goal: Run Lint

1. ทำ `/run-lint` เพื่อตรวจสอบ code style
2. แก้ไข lint errors ถ้ามี
3. ยืนยันว่า lint ผ่าน

### 2. Run Typecheck

> Goal: Run Typecheck

1. ทำ `/run-typecheck` เพื่อตรวจสอบ types
2. แก้ไข type errors ถ้ามี
3. ยืนยันว่า typecheck ผ่าน

### 3. Run Scan

> Goal: Run Scan

1. ทำ `/run-scan` เพื่อตรวจสอบ code patterns
2. แก้ไข scan issues ถ้ามี
3. ยืนยันว่า scan ผ่าน

## Rules

### 1. Check Order

- Lint: ตรวจสอบ code style ก่อน
- Typecheck: ตรวจสอบ types
- Scan: ตรวจสอบ code patterns

### 2. Failure Handling

- Lint ล้มเหลว: แก้ไข lint errors
- Typecheck ล้มเหลว: แก้ไข type errors
- Scan ล้มเหลว: แก้ไข scan issues

### 3. Parallel Execution

- รัน lint, typecheck และ scan แบบ parallel เมื่อเป็นไปได้
- ใช้ cache เพื่อเพิ่มความเร็ว
- รัน checks ใน CI environment

- ใช้ /deep-optimize ถ้าจำเป็น

## Expected Outcome

- Lint ผ่านทั้งหมด
- Typecheck ผ่านทั้งหมด
- Scan ผ่านทั้งหมด
- Code พร้อมสำหรับ commit/deploy