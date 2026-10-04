---
name: improve
description: หาสิ่งที่ improve ใน scope รวม findings แล้วแก้ผ่าน review-* หลัง user confirm
argument-hint: "[scope]"
related:
  - simplify
  - deep-review
  - review
  - report
  - suggest-next-action
  - ask-me
---

## Goal

ตอบคำถาม "improve อะไรได้บ้าง" สำหรับ scope ที่ user ระบุ — รวม findings จาก reviews เป็น prioritized list แล้วส่งต่อไปแก้ที่ section `## Fix` ของ `review-*` ที่ตรง domain หลัง user confirm

## Scope

ใช้เมื่อ user ถามว่า scope นี้ "ควร improve อะไร" — เป็น thin entry point ที่ delegate การ review ไป `/deep-review` ไม่ทำ review เองและไม่แก้ไขโดยตรง

## Execute

### 1. Review Gaps

> Goal: ได้ prioritized improvement list

1. รับ `scope` จาก argument — ถ้าไม่มี → ใช้ project ปัจจุบัน ถ้าไม่ชัด → `/ask-me`
2. ถ้า scope เป้น issue หรือ GitHub issue → ทำ `/deep-review` เพื่อรวบรวม findings ของ issue
3. ทำ `/deep-review` กับ scope นั้น — ถ้ายังไม่มี findings ให้ใช้ `deep-review/SKILL.md` ของ `/deep-review` สแกนกว้างก่อน
4. รวบรวม prioritized list พร้อม severity และ evidence

### 2. Present And Confirm

> Goal: แสดงผลและให้ user เลือกสิ่งที่จะแก้

1. ทำ `/report` แสดง improvements: No., Finding, Severity, Fix Skill
2. ถาม user ว่าจะแก้ข้อไหน — รอการยืนยันก่อนลงมือ

### 3. Fix Confirmed Items

> Goal: แก้เฉพาะสิ่งที่ user เลือก

1. ส่งแต่ละ finding ที่ confirm ไปยัง section `## Fix` ของ `review-*` skill ที่ตรง domain
2. ทำ `/suggest-next-action` หลังแก้ครบ

## Rules

- ไม่ทำ review เอง — delegate ไป `/deep-review` หรือ `/deep-review` ถ้าเป้น issue
- ไม่แก้ไขโดยไม่ได้ user confirm
- ทุก improvement ต้อง map ไปยัง skill ที่ทำได้จริง

## Expected Outcome

- Prioritized improvement list จาก `/deep-review` หรือ `/deep-review` ถ้าเป้น issue
- User เลือกสิ่งที่จะแก้
- Findings ที่ confirm ถูกส่งไปแก้ที่ `## Fix` ของ `review-*` ที่ถูกต้อง
