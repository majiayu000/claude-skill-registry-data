---
name: move-to
description: ย้ายไฟล์และอัพเดท reference
argument-hint: "[source] [target]"
related:
  - follow-best-practice
  - suggest-next-action
  - resolve-errors
  - update-references
---

## Goal

ย้ายไฟล์ไปยังตำแหน่งใหม่และอัพเดท reference

## Scope

ใช้ `move` สำหรับ tasks และ workflows เฉพาะที่ครอบคลุม (to)

## Execute

### 1. Move File

> Goal: Move File

ย้ายไฟล์ไปยังตำแหน่งใหม่

1. ระบุไฟล์ที่ต้องย้าย
2. ย้ายไฟล์ไปยังตำแหน่งใหม่
3. ตรวจสอบว่าย้ายถูกต้อง

### 2. Update Reference

> Goal: Update Reference

อัพเดท reference

1. รัน `/update-references`
2. ตรวจสอบว่า references ถูกอัพเดท

## Rules

- ใช้ git สำหรับ file operations ถ้าเป็นไปได้
- ตรวจสอบว่าไม่มี data loss
- อัพเดท references หลังจากย้ายไฟล์

- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- ไฟล์ถูกย้ายไปยังตำแหน่งใหม่
- References ถูกอัพเดท
- ไม่มี data loss
