---
name: run-dev
description: รัน development server และแก้ไขข้อผิดพลาด
argument-hint: "[scope]"
related:
  - check-open-ports
  - resolve-errors
  - watch-terminal
  - watch-browser
  - test-usage
  - run-verify
  - report

---

## Goal

รัน development server และแก้ไขข้อผิดพลาดที่เกิดขึ้น พร้อม watch terminal และ browser

## Scope

ใช้สำหรับรัน development server ของ project ใดๆ พร้อมตรวจสอบและแก้ไข errors

## Execute

> Pre-Run: ทำ `/check-open-ports` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (dev)

### 1. Check Configuration

> Goal: Check Configuration

1. ตรวจสอบ main config และ dev script ว่ามีการกำหนดไว้หรือไม่
2. ถ้าไม่มี dev script ใน main config ต้องกำหนดให้
3. ตรวจสอบว่า dependencies ที่จำเป็นถูกติดตั้งแล้ว
4. ตรวจสอบว่า environment variables ที่จำเป็นถูกกำหนดแล้ว

### 2. Run Dev Server

> Goal: Run Dev Server

1. รัน dev server ด้วยคำสั่งที่เหมาะสม (bun dev, npm run dev, cargo run)
2. ถ้ามี errors ให้ทำ `/resolve-errors` เพื่อแก้ไข
3. ติดตามและแก้ไขข้อผิดพลาดทันทีจนกว่าจะผ่าน
4. ตรวจสอบว่า dev server เริ่มต้นสำเร็จ

### 3. Watch Terminal

> Goal: Watch Terminal

1. ทำ `/watch-terminal` เพื่อ watch terminal ทุก 5 วินาที
2. ตรวจจับ errors และ warnings ใหม่ๆ อัตโนมัติ
3. ถ้าพบ errors ให้ทำ `/resolve-errors` ทันที

### 4. Open Web (ถ้าเป็น web)

> Goal: Open Web (ถ้าเป็น web)

1. ถ้าเป็น web project ให้ทำ `/open-web` เพื่อเปิด browser ที่ dev server URL
2. ตรวจสอบว่า website เปิดได้และแสดงผลถูกต้อง

### 5. Watch Browser (ถ้าเป็น web)

> Goal: Watch Browser (ถ้าเป็น web)

1. ถ้าเป็น web project ให้ทำ `/watch-browser-and-fix` เพื่อตรวจสอบ browser
2. ตรวจสอบว่า dev server ทำงานได้จริงผ่าน browser
3. ทดสอบ features หลักทำงานได้

### 6. Test Usage

> Goal: ทดสอบ flow การใช้งานสำคัญ

1. ทำ `/test-usage` เพื่อทดสอบ features หลัก
2. ถ้าพบปัญหา → ทำ `/watch-browser-and-fix` หรือ `/resolve-errors`
3. ยืนยันว่า user flow สำคัญทำงานได้

### 7. Verify

> Goal: Verify

1. ทำ `/run-verify`
2. ยืนยันว่าไม่มี critical errors ที่ขัดขวางการทำงาน
3. ตรวจสอบว่า services ที่เกี่ยวข้องทำงานปกติ
4. ยืนยันว่าไม่มี runtime errors ใน console

### 8. Report

> Goal: Report

1. ทำ `/report` เพื่อแสดง terminal output
2. สรุปสถานะ dev server และ issues ที่เหลือ

## Rules

### 1. Runtime Selection

- ใช้คำสั่งที่เหมาะสมกับ runtime (bun dev, npm run dev, cargo run)
- ตรวจสอบ ecosystem จาก package manifest ก่อนเลือกคำสั่ง

### 2. Error Resolution

- ทำ `/resolve-errors` เมื่อพบ error
- แก้ที่ root cause ไม่ใช่ symptoms
- ตรวจสอบว่า dev server เริ่มต้นสำเร็จก่อน watch

### 3. Watch Strategy

- ทำ `/open-web` เฉพาะ web project เพื่อเปิด browser ที่ dev server URL
- ทำ `/watch-terminal` สำหรับทุก project
- ทำ `/watch-browser-and-fix` เฉพาะ web project
- ถ้าพบ errors ระหว่าง watch ให้ทำ `/resolve-errors` ทันที

## Expected Outcome

- Development server ทำงานได้
- ไม่มี critical errors
- Terminal ถูก watch ต่อเนื่อง
- Browser แสดงผลถูกต้อง (ถ้าเป็น web)
- Features หลักทำงานได้