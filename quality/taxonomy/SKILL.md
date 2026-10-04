---
name: taxonomy
description: สร้าง taxonomy หรือจัดหมวดหมู่ items ตาม context ปัจจุบัน
argument-hint: "[items-or-domain]"
related:
  - grouping

  - report
---

## Goal

สร้าง taxonomy ที่ชัดเจนและครอบคลุมสำหรับ items, concepts, หรือ domain ที่กำหนด

## Scope

ใช้เมื่อต้องการจัดกลุ่ม, จัดลำดับ, หรือสร้างโครงสร้างหมวดหมู่จากรายการ items, concepts, หรือข้อมูลที่มีอยู่

## Execute

### 1. Define Taxonomy Purpose

> Goal: ระบุ purpose และ scope ของ taxonomy

1. ระบุ domain หรือชุด items ทีต้องการจัดหมวดหมู่
2. ระบุ audience และวัตถุประสงค์ของ taxonomy
3. กำหนดระดับความลึก (flattened, 1-level, multi-level)
4. เลือก criteria หลักสำหรับการแบ่งหมวดหมู่

### 2. Collect And Inspect Items

> Goal: รวบรวมและตรวจสอบ items ที่จะจัด taxonomy

1. ลิสต์ items ที่มีอยู่ทั้งหมด
2. ระบุ attributes สำคัญของแต่ละ item
3. ตรวจหา items ทีอาจซ้ำซ้อนหรือขาดหาย
4. บันทึก source ของข้อมูล

### 3. Group Items

> Goal: จัดกลุ่ม items ตาม criteria

1. วิเคราะห์ attributes และ relationships
2. สร้าง categories ตาม criteria ที่เลือก
3. ตั้งชื่อ category ให้ชัดเจนและไม่ซ้อนทับ
4. จัด items ให้อยู่ใน category ที่เหมาะสม (อนุญาต cross-category ถ้าจำเป็น)

### 4. Build Hierarchy

> Goal: สร้างโครงสร้างลำดับชั้น

1. ระบุ top-level categories
2. แบ่ง sub-categories ถ้ามีความจำเป็น
3. วาง items ใน leaf nodes
4. ระบุ relationships ระหว่าง categories (parent-child, sibling, dependency)

### 5. Label And Document

> Goal: ทำให้ taxonomy ใช้งานได้ง่าย

1. เขียน label และ description ให้แต่ละ category
2. เลือกรูปแบบ output: tree, table, tags, หรือ markdown list
3. ระบุ examples สำหรับ category ที่สำคัญ
4. บันทึก conventions สำหรับการเพิ่ม item ใหม่

### 6. Validate And Refine

> Goal: ตรวจสอบความสมบูรณ์

1. ตรวจว่าทุก item ถูกจัดอยู่ใน category
2. ตรวจว่า categories ไม่ซ้อนทับกันมากเกินไป
3. ตรวจความสอดคล้องกับ purpose
4. ปรับ refine taxonomy จาก feedback หรือ gaps ทีพบ

## Rules

### 1. Clarity And Non-Overlap

- Taxonomy ต้องชัดเจน, ไม่ซ้ำซ้อน, ครอบคลุม
- ใช้ criteria ทีวัดผลได้ในการแบ่งหมวดหมู่
- หลีกเลี่ยง categories ทีกว้างเกินไปหรือ narrow เกินไป

### 2. Flexibility

- รองรับ multi-parent หรือ cross-cutting ถ้าจำเป็น
- เอกสาร label, description, และ examples ให้ครบ
- ทำ version หรือ timestamp ถ้า taxonomy เปลี่ยนแปลงบ่อย

### 3. Output Quality

- Output ต้องอ่านง่ายและนำไปใช้ต่อได้
- ระบุรูปแบบ output ตามความเหมาะสมของ audience
- รายงาน gaps หรือ items ที่ยังจัดหมวดหมู่ไม่สมบูรณ์

- ใช้ /grouping ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น

## Expected Outcome

- Taxonomy ทีสมบูรณ์และใช้งานได้
- Items ทุกตัวถูกจัดอยู่ใน category ที่เหมาะสม
- Categories มี labels และ descriptions ชัดเจน
- Output อยู่ในรูปแบบที่เลือก (tree, table, tags, markdown)
- มี guidance สำหรับเพิ่ม/แก้ไข item ในอนาคต
