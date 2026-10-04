---
name: plan
description: alias → /deep-plan (analyze + plan — วิเคราะห์ลึกแล้ววางแผน implementation-ready)
argument-hint: "[scope]"
related:
  - deep-plan
---

## Goal

Alias ของ `/deep-plan` — วิเคราะห์ปัญหา/context อย่างลึกซึ้งแล้ววางแผน implementation-ready ในขั้นตอนเดียว

## Scope

ใช้เมื่อ user เรียก `/plan` — skill นี้เป็น alias stub เท่านั้น workflow จริงอยู่ใน `deep-plan`

## Execute

ทำ `/deep-plan` เต็ม workflow

## Rules

- ห้าม duplicate workflow ของ `/deep-plan` ในไฟล์นี้
- ถ้า alias ขาด steps → อ่าน `deep-plan/SKILL.md` เสมอ

## Expected Outcome

- `/deep-plan` ถูก execute ครบทุก step จนได้ implementation-ready plan
