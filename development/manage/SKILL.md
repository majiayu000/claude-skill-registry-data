---
name: manage
description: จัดการ context และ tasks หลายรายการ โดย rethink, จัดลำดับ, และ dispatch งานต่อไป
argument-hint: "[context-or-tasks]"
related:
  - rethink
  - suggest-next-action
  - report-todo
  - continue
  - ship-to-dev-branch
  - follow-parallel
  - follow-enter-dot
  - report
  - ask-me
  - refactor
  - edit-only
  - move-to
  - rename
  - all-this-patterns
---

## Goal

จัดการ context และ tasks หลายรายการให้เป็นระเบียบ โดย rethink, จัดลำดับ priority, และ dispatch งานต่อไปให้ถูกต้อง

## Scope

ใช้เมื่อมี context หรือ tasks หลายรายการจนไม่รู้ว่าควรทำอะไรก่อน หรือต้องการให้ agent จัดการแทน ไม่แก้ไข code หรือไฟล์โดยตรง เป็น orchestrator เท่านั้น

## Execute

### 1. Gather Context

> Goal: รวบรวมสิ่งที่ต้องจัดการ

1. อ่าน todo list ปัจจุบัน
2. อ่าน `git status` และ open files
3. อ่านข้อความ/คำสั่งล่าสุดของ user
4. ทำ `/report` สรุป context ทั้งหมด

### 2. Rethink And Prioritize

> Goal: รู้ว่าอะไรสำคัญก่อน

1. ทำ `/rethink` เพื่อวิเคราะห์ context หลายรายการ
2. จัดลำดับ priority: urgent → high impact → blocking → low risk
3. ระบุ dependencies ระหว่าง tasks
4. ถ้า context ทับซ้อนหรือขัดแย้ง → ทำ `/ask-me`

### 3. Decide File Operation Mode

> Goal: ถ้ามี file operations ให้เลือกรูปแบบทีเหมาะสม

1. ถ้างานไม่เกี่ยวกับ file operations → ข้ามไป step ถัดไป
2. ทำ `/rethink` โดยถามว่าควรใช้ file op แบบไหน:
   - `/edit-only` — แก้ไขเฉพาะจุด
   - `/refactor` — refactor code โดยรักษา behavior
   - `/refactor` structure scope — ย้าย/จัดโครงสร้างไฟล์
   - `/move-to` — ย้ายไฟล์/โฟลเดอร
   - `/rename` — เปลี่ยนชื่อ identifier/ไฟล์ รวม batch rename
   - `/all-this-patterns` — แก้หลายจุดตาม pattern
3. เลือกตามผล `/rethink` โดย user confirm ถ้ามีหลายทางเลือกใกล้เคียงกัน

### 4. Dispatch Next Actions

> Goal: ส่งงานไปยัง skill ที่ถูกต้อง

1. ถ้ามีงานค้างให้ทำต่อ → `/continue`
2. ถ้าหลายงานอิสระให้ทำขนาน → `/follow-parallel`
3. ถ้างานเสร็จแล้วให้ ship → `/ship-to-dev-branch`
4. ถ้าต้อง planning → `/report-todo` แล้วทำตามลำดับ
5. ถ้างานยาวหรือต้องวนซ้ำ → `/loop-until-complete`

### 5. Track And Report

> Goal: ติดตามความคืบหน้า

1. ทำ `/report-todo` อัปเดต status
2. ทำ `/suggest-next-action` เมื่อจบแต่ละรอบ
3. ถ้า user กด `.` → `/follow-enter-dot`

## Rules

- ไม่แก้ไขไฟล์โดยตรง เป็น orchestrator เท่านั้น
- ทำ `/rethink` เสมอก่อนตัดสินใจเมื่อ context หลายรายการ
- ถ้างานมีความเสี่ยงสูง → ขอ user ยืนยันก่อน
- เก็บ todo list ให้อัปเดตตลอด
- ไม่ข้าม validation หรือ `/report-progress`

## Expected Outcome

- Context หลายรายการถูกจัดลำดับและเข้าใจ
- งานถูก dispatch ไปยัง skill ทีเหมาะสม
- Todo list อัปเดตและชัดเจน
- User ทราบ action ถัดไป
