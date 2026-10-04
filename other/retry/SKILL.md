---
name: retry
description: ทำตาม user prompt ล่าสุดอีกครั้ง เพื่อแก้ไขปัญหาหรือลองใหม
argument-hint: "[prompt]"
related:
  - ask-again
  - follow-best-practice
  - suggest-next-action
  - loop-until-complete
  - resolve-errors
  - run-until-pass
---

## Goal

ทำตาม user prompt ล่าสุดอีกครั้ง เพื่อแก้ไขปัญหาหรือลองใหม โดยเน้นที root cause

## Scope

ใช้เมื่อต้องการทำงานซ้ำตาม user prompt ล่าสุด เช่นหลังจากพบ error, ผลไม่ผ่าน หรือต้องการลอง approach ใหม

## Execute

### 1. Identify Latest Prompt

> Goal: รู้ prompt ล่าสุดทีต้องทำซ้ำ

1. อ่าน user prompt ล่าสุดจาก conversation history
2. ถ้าไม่พบ ให้ถามผู้ใช้
3. ระบุสถานะปัจจุบันว่าไปถึงไหนแล้ว

### 2. Re-Execute

> Goal: ทำซ้ำและแก้ไขให้ดีขึ้น

1. ทำตาม user prompt ล่าสุดอีกครั้ง
2. แก้ไขปัญหาที root cause ไม่ใช่ symptoms
3. ใช้ minimal changes เสมอ
4. ถ้ายังไม่ผ่าน → ทำ `/loop-until-complete` หรือ `/resolve-errors` ตาม context

## Rules

- ทำตาม user prompt ล่าสุดเท่านั้น
- แก้ที root cause ไม่ใช่ symptoms
- ใช้ minimal changes เสมอ
- ถ้าทำซ้ำหลายครั้ง ให้บันทึกสิ่งทีลองแล้วไม่ได้ผล

- ใช้ /ask-again ถ้าจำเป็น
- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น
- ใช้ /run-until-pass ถ้าจำเป็น

## Expected Outcome

- งานที่ทำซ้ำเสร็จสมบูรณ์
- ปัญหาถูกแก้ไขที root cause
- ไม่เกิด regression จากการทำซ้ำ
