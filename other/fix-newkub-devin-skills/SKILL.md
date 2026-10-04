---
name: fix
description: แก้ไขปัญหาตาม context ทั่วไปด้วย root cause analysis และ validate
argument-hint: "[scope]"
related:
  - resolve-errors
  - analyze-root-cause-analysis
  - follow-your-suggestion
  - deep-validate
  - run-check
  - ask-me
  - scan-codebase
  - run-test-all
  - run-until-pass
---

## Goal

แก้ไขปัญหา, error หรือข้อบกพร่องตาม context ทั่วไป ด้วยการวิเคราะห์ root cause และแก้ไขอย่างปลอดภัย

## Scope

ใช้เมื่อพบ error หรือต้องการแก้ไขอะไรบางอย่าง โดยไม่จำกัด domain หรือ technology

## Execute

### 1. Understand Problem

> Goal: เข้าใจปัญหาที่ต้องการแก้

1. รับ error, symptom, หรือ issue จาก user
2. ถ้ามี stack trace หรือ logs → อ่านและสรุป
3. ถ้าไม่ชัด → ทำ `/ask-me` ขอข้อมูลเพิ่ม

### 1.5 Choose Fix Mode

> Goal: ตัดสินใจว่าจะ fix อย่างไร

1. ถ้า user พิมพ์ `fix` โดยไม่ระบุ scope หรือ `fix all` → แก้ทุก issue ทีพบใน context ปัจจุบัน
2. ถ้ามีข้อเสนอจากการวิเคราะห์ก่อนหน้า → ทำ `/follow-your-suggestion`
3. ถ้า user ระบุ scope เฉพาะ → แก้เฉพาะ scope นั้น

### 2. Analyze Context

> Goal: หา root cause

1. ทำ `/analyze-root-cause-analysis` ถ้าเป็นปัญหาซับซ้อน
2. อ่านไฟล์และ config ทีเกี่ยวข้อง
3. ใช้ `/scan-codebase` หา call sites และ consumers
4. ระบุ root cause พร้อม evidence

### 3. Plan Fix

> Goal: วางแผนการแก้ไข

1. ระบุไฟล์ทีต้องแก้
2. เลือก fix ที minimal และถูกต้อง
3. ประเมิน impact
4. ถ้าเสี่ยงสูง → ขอ user confirm ก่อน

### 4. Apply Fix

> Goal: แก้ไขอย่างปลอดภัย

1. สร้าง checkpoint ด้วย `git stash` หรือ branch
2. แก้ไข code หรือ config ตาม plan
3. ตรวจสอบว่าไม่แก้นอก scope
4. ถ้าแก้หลายไฟล์ → ทำเป็นชุดเล็กๆ

### 5. Validate

> Goal: ยืนยันว่า fix ถูกต้อง

1. รัน `/run-check` (lint, typecheck, scan)
2. รัน tests ถ้ามี
3. ทำ `/deep-validate` สำหรับ project
4. ถ้าไม่ผ่าน → ทำซ้ำขั้นตอน 2-4 (max 3 ครั้ง)

### 6. Report

> Goal: สรุปผล

1. รายงานสิ่งทีแก้ไข
2. ระบุ root cause และวิธี fix
3. รายงาน validation result
4. ถ้ายังไม่สำเร็จ → ระบุสิ่งค้าง

## Rules

- หา root cause ก่อนแก้ไข
- ใช้ minimal fix
- ไม่เดาสาเหตุถ้าไม่มี evidence
- ทำ checkpoint ก่อนแก้
- ไม่แก้ไขนอก scope ที่ตกลง
- ถ้าค้างใช้ TODO → ระบุชัดเจนใน `TODO.md`

- ใช้ /follow-your-suggestion ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น
- ใช้ /run-test-all ถ้าจำเป็น
- ใช้ /run-until-pass ถ้าจำเป็น

## Expected Outcome

- ปัญหาถูกแก้ไข
- Code ผ่าน validation
- รายงาน root cause และวิธีแก้ไขชัดเจน
