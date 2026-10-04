---
name: relocation
description: ย้ายไฟล์และโฟลเดอร์ไปยังตำแหน่งที่เหมาะสมตาม domain และ responsibility
argument-hint: "[scope]"
related:
  - deep-review
  - update-references
  - use-scripts
---

## Goal

ย้ายไฟล์และโฟลเดอร์ไปยังตำแหน่งที่เหมาะสมตาม domain และ responsibility พร้อมอัปเดต import paths ทั้งหมด

## Scope

ครอบคลุมการย้ายไฟล์/โฟลเดอร์ และอัปเดต references ทั้งหมด

## Execute

### 1. Identify File Responsibilities

> Goal: Identify File Responsibilities

1. วิเคราะห์ domain หรือ responsibility ของแต่ละไฟล์:
   - `domain`: business logic และ entities
   - `ui`: components และ layouts
   - `utils`: helper functions และ utilities
   - `types`: type definitions และ interfaces
   - `api`: API endpoints และ handlers
2. ตรวจสอบ dependencies ของแต่ละไฟล์
3. ระบุไฟล์ที่อยู่ในตำแหน่งไม่เหมาะสม

### 2. Plan Relocation Strategy

> Goal: Plan Relocation Strategy

1. กำหนด target folder สำหรับแต่ละไฟล์ตาม responsibility
2. ตรวจสอบ dependency direction ก่อนย้าย:
   - high-level modules พึ่งพา low-level modules
   - domain พึ่งพา shared types ไม่ใช่กลับกัน
3. วางแผนลำดับการย้ายเพื่อหลีกเลี่ยง circular dependencies
4. บันทึก mapping ของ old path → new path

### 3. Execute File Relocation

> Goal: Execute File Relocation

1. ทำ `use-scripts` เพื่อย้ายไฟล์ไปยังโฟลเดอร์ที่เหมาะสม
2. ย้ายไฟล์ตามลำดับที่วางแผนไว้
3. ตรวจสอบว่าไม่มีไฟล์หลงเหลือในตำแหน่งเดิม
4. ทำ `/deep-review` เพื่อสร้าง barrel exports และตั้งค่า import aliases สำหรับโฟลเดอร์ใหม่ถ้าจำเป็น

### 4. Update Import Paths

> Goal: Update Import Paths

1. ทำ `/update-references` เพื่ออัปเดท references ทั้งหมด
2. ค้นหา import paths ที่อ้างอิงถึงไฟล์ที่ย้าย
3. อัปเดต import paths ให้ตรงกับตำแหน่งใหม่
4. ตรวจสอบว่า import paths ถูกต้องทั้งหมด

### 5. Validate Changes

> Goal: Validate Changes

1. รัน type check เพื่อยืนยันว่า import paths ถูกต้อง
2. รัน build เพื่อตรวจสอบว่าไม่มี errors
3. ตรวจสอบว่าไม่มี circular dependencies ใหม่
4. ทำ `check-architecture` เพื่อยืนยันโครงสร้างใหม่

## Rules

### 1. Responsibility-Based Relocation

ย้ายไฟล์ตาม domain หรือ responsibility:

- ย้ายตาม business domain ไม่ใช่ file type อย่างเดียว
- จัดกลุ่มตาม feature หรือ module ที่ชัดเจน
- รักษา dependency direction ให้ถูกต้อง
- หลีกเลี่ยงการย้ายไฟล์ข้าม layers โดยไม่จำเป็น

### 2. Dependency Direction

รักษา dependency direction ที่ถูกต้อง:

- high-level modules พึ่งพา low-level modules
- domain layers พึ่งพา shared types ไม่ใช่กลับกัน
- UI layers พึ่งพา domain layers ไม่ใช่กลับกัน
- หลีกเลี่ยง circular dependencies ระหว่างโฟลเดอร์

### 3. Import And Export Strategy

อัปเดต import paths และ barrel exports อย่างถูกต้อง:

- อัปเดต import paths ทันทีหลังย้ายไฟล์
- ใช้ barrel exports และ import aliases เพื่อ simplify import paths
- หลีกเลี่ยง deep imports ที่ซับซ้อน
- ตรวจสอบทุก import paths ที่อ้างอิงถึงไฟล์ที่ย้าย
- สร้าง `index.ts` สำหรับโฟลเดอร์ที่มีหลายไฟล์
- ใช้ `/deep-review` เพื่อจัดการ barrel exports และ import aliases

## Expected Outcome

- ไฟล์อยู่ในตำแหน่งที่เหมาะสมตาม responsibility
- import paths ที่กระชับและถูกต้อง
- dependency direction ที่ถูกต้อง
- ไม่มี circular dependencies
- โครงสร้างที่สม่ำเสมอและเป็นระเบียบ

## Common Mistakes

ข้อผิดพลาดที่พบบ่อย:

- ไม่อัปเดต import paths หลังย้ายไฟล์
- ย้ายไฟล์โดยไม่วิเคราะห์ dependencies
- สร้าง circular dependencies ระหว่างโฟลเดอร์
- ไม่ใช้ barrel exports และ import aliases สำหรับโฟลเดอร์ใหม่
- ย้ายไฟล์ข้าม layers โดยไม่จำเป็น

## Anti-Patterns

รูปแบบที่ไม่ควรทำ:

- ❌ ย้ายไฟล์โดยไม่อัปเดต import paths
- ❌ ย้ายไฟล์แบบ random โดยไม่มีเกณฑ์
- ❌ สร้าง circular dependencies ระหว่างโฟลเดอร์
- ❌ ไม่ตรวจสอบ dependencies ก่อนย้าย
- ❌ ทิ้ง orphan files ไว้หลังย้าย