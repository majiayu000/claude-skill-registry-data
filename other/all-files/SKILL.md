---
name: all-files
description: รัน task หรือ workflow เดียวกันกับทุก file ใน project จนครบทุกไฟล์
argument-hint: "[scope]"
related:
  - deep-analyze
  - deep-validate
  - resolve-errors
  - refactor-all-files-in-workspace
---

## Goal

ทำงานกับแต่ละ file ใน project จนครบทั้งหมดตาม workflow ที่กำหนด

## Scope

ใช้ `all-files` สำหรับ tasks และ workflows เฉพาะที่กำหนด

## Execute

### 1. Discover Files

> Goal: Discover Files

1. ทำ `/deep-analyze` เพื่อดูโครงสร้าง
2. ใช้ `find_by_name` หรือ `list_dir` เพื่อค้นหา files ตาม pattern

### 2. Process Each File

> Goal: Process Each File

1. อ่าน files แบบ parallel ด้วย `read_file`
2. แก้ไข files แบบ sequential ด้วย `edit` หรือ `multi_edit`
3. ทำตาม workflow ที่เกี่ยวข้องกับแต่ละ file

### 3. Verify

> Goal: Verify

1. ตรวจสอบว่าทุก file ได้รับการประมวลผลแล้ว
2. ทำ `/deep-validate` เพื่อตรวจสอบความถูกต้อง

## Rules

### 1. Processing Order

- ทำ files ที่เป็น foundation ก่อน (config, types, utilities)
- ทำ files ที่มี dependencies ซับซ้อนทีหลัง

### 2. Batch Operations

- อ่าน files แบบ parallel
- แก้ไข files แบบ sequential เพื่อหลีกเลี่ยง conflicts

### 3. Error Handling

- บันทึก files ที่มีปัญหา
- ทำ `/resolve-errors` สำหรับ files ที่มี issues

## Expected Outcome

- ทุก file ใน scope ได้รับการประมวลผลครบถ้วน