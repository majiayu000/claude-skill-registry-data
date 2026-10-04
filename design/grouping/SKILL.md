---
name: grouping
description: จัดกลุ่ม items ตามหมวดหมู่หรือคุณลักษณะ
argument-hint: "[scope]"
related:
  - follow-best-practice
  - suggest-next-action
  - resolve-errors
  - idea-grouping
---

## Goal

จัดกลุ่ม items ตามหมวดหมู่หรือคุณลักษณะที่เกี่ยวข้อง

## Scope

ใช้สำหรับจัดกลุ่ม code, files, workflows, หรือ data structures ใน project

## Execute

### 1. Identify Groups

> Goal: Identify Groups

ระบุหมวดหมู่ที่เหมาะสม

1. วิเคราะห์ items ที่มี
2. ระบุคุณลักษณะที่เหมือนกัน
3. กำหนด criteria สำหรับการจัดกลุ่ม

### 2. Create Groups

> Goal: Create Groups

สร้าง groups ตาม criteria

1. จัดกลุ่ม items ตาม criteria
2. ตั้งชื่อ groups ให้ชัดเจน
3. จัดเรียง items ภายในแต่ละ group

### 3. Organize Structure

> Goal: Organize Structure

จัดโครงสร้างตาม groups

1. สร้าง directories หรือ modules สำหรับแต่ละ group
2. ย้าย items ไปยัง groups ที่เหมาะสม
3. ตรวจสอบ structure ถูกต้อง

## Rules

- จัดกลุ่มตามความสัมพันธ์
- ใช้ criteria ที่ชัดเจน
- ถ้า folder มีไฟล์มากเกินไป ให้ grouping
- หลีกเลี่ยง groups ที่ซ้อนทับ
- รักษา consistency ทั่วทั้ง project
- จัดกลุ่มตาม domain หรือ feature
- จัดกลุ่มตาม layer (ui, logic, data)
- จัดกลุ่มตาม type (components, utils, types)
- ใช้ barrel exports สำหรับ groups

- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Items ถูกจัดกลุ่มอย่างเหมาะสม
- Structure ที่ชัดเจนและ maintainable
- ง่ายต่อการค้นหาและ navigate