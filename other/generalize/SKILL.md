---
name: generalize
description: แปลง how-to หรือ instructions เป็น solution patterns ทั่วไปที่ใช้ซ้ำได้
argument-hint: "[scope]"
related:
  - write-explicit
  - deep-validate
  - check-reference
---

## Goal

แปลง skill หรือเอกสารที่เขียนแบบ how-to step-by-step เป็น solution patterns ทั่วไป ที่ระบุปัญหา เงื่อนไข ทางเลือก และ criteria ตัดสินใจ โดยไม่ผูกกับ tool/library/context เฉพาะ

## Scope

ใช้เมื่อต้อง rewrite skill หรือข้อความให้: 
- ไม่ใช่ how-to สำหรับ tool ตัวเดียว
- ใช้ได้หลาย context ด้วยการปรับเล็กน้อย
- อ่านแล้วรู้ว่าต้องแก้ปัญหาอย่างไร มากกว่าแค่ทำตามลำดับขั้น

## Execute

### 1. Detect How-To Patterns

> Goal: หาจุดที่เขียนเป็น step-by-step เฉพาะเจาะจง

1. อ่าน target `SKILL.md` หรือเอกสาร
2. ทำเครื่องหมายทุกข้อที่เริ่มด้วย `ติดตั้ง`, `รัน`, `เพิ่ม`, `แก้ไข`, `ตั้งค่า` โดยไม่มีเงื่อนไข
3. หาชื่อ tool/library ที่ปรากฏบ่อย และถามว่าเป็นตัวอย่างหรือเป้าหมายจริง
4. บันทึก patterns ที่พบ เป็นรายการ

### 2. Extract Problem And Context

> Goal: ระบุปัญหาทั่วไปที่ skill แก้

1. ถาม: "ถ้าไม่มี tool/library เฉพาะนี้ ปัญหาคืออะไร?"
2. ระบุ problem ในรูป: `เมื่อ <สถานการณ์> เกิด <ผลเสีย>`
3. ระบุ context ทั่วไปที่ทำให้วิธีแก้ต่างกัน
4. ลบชื่อ tool/library ออกจาก problem statement

### 3. Define Solution Pattern

> Goal: เปลี่ยนขั้นตอนเป็น pattern ทั่วไป

1. เปลี่ยนลำดับขั้นตอนเป็นรูปแบบ: `เมื่อ <condition> → <solution pattern> → <expected result>`
2. แทนชื่อ tool ด้วยประเภท: `package manager`, `bundler`, `linter`, `database`, `runner`, `registry`
3. ระบุ criteria ตัดสินใจระหว่าง solution ทางเลือก
4. ถ้ามีหลาย solution → ใช้ decision tree หรือ bullet `เลือก X ถ้า Y`

### 4. Generalize Step Instructions

> Goal: แต่ละ step ไม่ผูก tool/technology

1. เปลี่ยนคำสั่งเฉพาะ เช่น `bun add` เป็น `install package ด้วย package manager ที่ project ใช้`
2. ใช้ generic verbs: `prepare`, `configure`, `run`, `verify`, `fallback`, `isolate`
3. ระบุ condition ก่อน command เสมอ
4. ห้ามคัดลอก official docs ของ tool เข้า skill

### 5. Add Concrete Examples

> Goal: ให้เห็นภาพ โดยไม่ผูก skill กับ tool ใด tool หนึ่ง

1. ใส่ตัวอย่าง 2-3 กรณี ทีแตกต่างกัน (เช่น web, CLI, mobile, backend)
2. ตัวอย่างต้องมี่ `given → when → then`
3. ถ้ามี code ตัวอย่าง → ระบุว่าเป็นตัวอย่างเท่านั้น และแทนด้วย type name

### 6. Validate Generalization

> Goal: ตรวจว่า skill ใช้ซ้ำได้จริง

1. อ่านทั้้ง skill แล้วถาม: "ถ้า tool เปลี่ยน ต้องแก้ไขกี่จุด?" ถ้ามากเกินไป → กลับไป generalize ต่อ
2. ทำ `/write-explicit` เพื่อตรวจความชัดเจน
3. ทำ `/deep-validate` เพื่อตรวจ structure และ references
4. ทำ `/check-reference` เพื่อยื่นยันว่า `related` ถูกต้อง

## Rules

### 1. Problem First

- เริ่มจากปัญหา ไม่ใช่ขั้นตอน
- ทุก solution pattern ต้องอธิบายว่าแก้ปัญหาอะไร

### 2. Conditional Not Prescriptive

- ใช้ `ถ้า X → ทำ Y` แทน `ทำ Y` อย่างเดียว
- ระบุข้อจำกัด/edge case ทีทำให้ solution ต่างกัน

### 3. Tool-Agnostic

- ไม่ผูก skill กับ tool/library ตัวใดตัวหนึ่ง
- ถ้าต้องระบุ tool จริง → ใช้เป็นตัวอย่าง ไม่ใช่ default

### 4. Reusable Patterns

- แต่ละ pattern ต้องใช้ซ้ำได้ใน context อื่น
- หลีกเลี่ยง project-specific details หรือ commit hashes

### 5. Explicit And Concise

- ทุก instruction มี action, condition, expected result
- ไม่ใช้ how-to filler หรือ generic advice ลอยๆ

## Expected Outcome

- Skill หรือเอกสารไม่เขียนเป็น how-to อีกต่อไป
- ทุก section ระบุปัญหา เงื่อนไข ทางเลือก และ criteria ตัดสินใจ
- สามารถนำไปใช้กับหลาย tool/library โดยปรับเล็กน้อย
- ผ่าน `/deep-validate` และ `/check-reference`
