---
name: rewrite
description: rewrite ไฟล์หรือหลายไฟล์ใหม่ทั้งหมดโดยไม่อ้างอิง context ก่อนหน้า
argument-hint: "[scope]"
related:
  - reset-context
  - deep-validate
  - scan-codebase
  - review-devin-global-harness
  - follow-best-practice
  - use-scripts
  - update-references
---

## Goal

rewrite ไฟล์หรือหลายไฟล์ใหม่ทั้งหมด โดยไม่อ้างอิง context ก่อนหน้า และส่งมอบเนื้อหาที่สมบูรณ์

## Scope

ใช้เมื่อ user ขอให้ rewrite ไฟล์ หรือหลายไฟล์ โดยต้องการให้เขียนเนื้อหาใหม่ทั้งหมดจากไฟล์เปล่า

## Execute

### 1. Reset Context

> Goal: Reset Context

เริ่มต้นด้วย `/reset-context` เพื่อล้าง context ก่อนหน้า

1. เรียก `/reset-context` ก่อนแก้ไขทุกครั้ง
2. ไม่อ้างอิงข้อสรุป การวิเคราะห์ หรือ decisions จากการสนทนาก่อนหน้า
3. ถือว่าไฟล์เป้าหมายเป็นไฟล์ใหม่ที่ต้องเขียนใหม่ทั้งหมด

### 2. Identify Targets

> Goal: Identify Targets

ระบุไฟล์ที่ต้อง rewrite ให้ชัดเจน

1. ถามหรือตรวจสอบ target files จาก user request
2. ใช้ `scan-codebase` เพื่อหาไฟล์ที่เกี่ยวข้อง
3. ตรวจสอบ dependencies และ references ของ target files

### 3. Read Targets Fresh

> Goal: Read Targets Fresh

อ่านไฟล์เป้าหมายและ references ทั้งหมดใหม่

1. อ่าน target files ทั้งไฟล์
2. อ่าน imports, exports, และ dependencies
3. อ่าน reverse dependencies
4. ทำ `review-devin-global-harness` สำหรับ workflows ที่เกี่ยวข้อง

### 4. Analyze Requirements

> Goal: Analyze Requirements

วิเคราะห์ requirement ใหม่ทั้งหมด

1. ระบุว่าไฟล์ทำหน้าที่อะไร
2. ระบุ public API, interfaces, และ contracts
3. ระบุ standards, conventions, และ best practices ที่ต้องรักษา
4. ทำ `follow-best-practice` สำหรับ topic ที่เกี่ยวข้อง

### 5. Rewrite From Scratch

> Goal: Rewrite From Scratch

เขียนไฟล์ใหม่ทั้งหมดจากไฟล์เปล่า

1. ไม่ merge หรือ append กับเนื้อหาเดิม
2. ไม่อ้างอิง context ก่อนหน้า
3. ใช้ `write` เพื่อ overwrite ไฟล์เดิมด้วยเนื้อหาใหม่
4. ถ้ามีหลายไฟล์ ใช้ `use-scripts` สำหรับ automation
5. ทำ `update-references` หากชื่อไฟล์หรือ path เปลี่ยน

### 6. Validate

> Goal: Validate

ตรวจสอบผลลัพธ์

1. ทำ `/deep-validate` เพื่อตรวจสอบความถูกต้อง
2. ทำ `run-verify` เพื่อรัน lint, typecheck, scan
3. อ่านไฟล์ใหม่อีกครั้งเพื่อ verify

## Rules

### 1. Always Reset Context

- ต้องเรียก `/reset-context` ก่อน rewrite ทุกครั้ง
- ห้ามอ้างอิง conclusions หรือ analysis จากการสนทนาก่อนหน้า
- ห้ามสมมติว่า code เดิมถูกต้อง

### 2. Full Rewrite

- ไฟล์ถูกเขียนใหม่ทั้งหมด ไม่ merge กับเนื้อหาเดิม
- ห้าม copy-paste จากเนื้อหาเดิมโดยไม่ตรวจสอบ
- ห้ามทิ้งส่วนที่ไม่ได้ใช้งานจากเดิมไว้

### 3. Evidence-Based

- ทุกการตัดสินใจต้องอ้างอิงจากไฟล์จริงที่อ่านใหม่
- ทุก assumption ต้องมี evidence
- ไม่เดาจาก context หรือ memory

### 4. Preserve Contracts

- รักษา public API และ interfaces ที่ผู้ใช้กำหนด
- รักษา file paths และ naming conventions
- ถ้าต้องเปลี่ยน contract ให้ทำ `update-references` อัปเดท references ทั้งหมด

### 5. Complete Delivery

- ไฟล์ทั้งหมดต้องสมบูรณ์ ไม่มี TODO, MOCK, STUB ที่ไม่จำเป็น
- ตรวจสอบว่า references ทั้งหมดมีอยู่จริง
- ทำ `run-verify` ก่อนส่งมอบ

## Expected Outcome

- ไฟล์เป้าหมายถูก rewrite ใหม่ทั้งหมด
- ไม่มี context เก่าหลงเหลือในการตัดสินใจ
- เนื้อหาใหม่สอดคล้องกับ requirement ปัจจุบัน
- ผ่าน validation และ run-verify
- references ทั้งหมดอัปเดทถูกต้อง