---
name: run-watch
description: รัน watch mode สำหรับ build, test หรือ typecheck เพื่อตรวจ errors อย่างต่อเนื่อง
argument-hint: "<build|test|typecheck> [scope]"
related:
  - deep-review
  - resolve-errors
  - deep-debug

---

## Goal

รัน watch mode ของ task ที่ระบุ (build, test, typecheck) เพื่อตรวจ errors/regressions อย่างต่อเนื่องระหว่างพัฒนา

## Scope

- ใช้ระหว่าง active development เมื่อต้องการ feedback loop ต่อเนื่อง
- เลือก command ตาม package manager และ monorepo tool ที่ตรวจพบ

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (watch)

### 1. Detect Command

> Goal: เลือก watch command ที่ถูกต้อง

1. ตรวจ `package.json` scripts และ tool ที่ใช้ (bun, turbo, moon, vitest, tsc, cargo)
2. เลือกตาม task:
   - `build` → `bun run build --watch` หรือ tool equivalent (`tsc --watch`, `cargo watch`)
   - `test` → `bun test --watch` / `vitest` (watch เป็น default) / `cargo watch -x test`
   - `typecheck` → `tsc --noEmit --watch` หรือ equivalent
3. Monorepo → ใช้ run command ของ monorepo ก่อน (`turbo run <task> --watch`)

### 2. Run Watch Mode

> Goal: watch process ทำงานและ capture output

1. รัน command แบบ background process
2. ตรวจ initial output — errors, warnings, baseline status
3. รายงานว่า watch ทำงานอยู่และกำลัง monitor อะไร

### 3. Monitor And Report

> Goal: ติดตาม errors ที่เกิดระหว่าง watch

1. ตรวจ output เป็นระยะเมื่อมีการแก้ไขไฟล์
2. ถ้าพบ errors → ทำ `/resolve-errors` หรือ `/deep-debug`
3. หยุด watch เมื่อ task เสร็จหรือ user สั่ง

## Rules

- รันเป็น background process เสมอ ไม่ block session
- รายงาน baseline status ทันทีหลังเริ่ม
- อย่าลืมหยุด watch process เมื่อจบงาน

## Expected Outcome

- Watch mode ทำงานอยู่พร้อมรายงาน errors ต่อเนื่อง
- สถานะเริ่มต้นชัดเจน (pass/fail baseline)
