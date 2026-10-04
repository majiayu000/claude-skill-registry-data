---
name: restore
description: alias → /restore-files (คืน files/state — git log, devin history, dotfiles)
argument-hint: "[domain|verify]"
related:
  - restore-files
---

## Goal

Alias ของ `/restore-files` — คืนค่า files/state ผ่าน git log, devin history, dotfiles หรือ deleted files ของ top-level skills

## Scope

ใช้เมื่อ user เรียก `/restore` — skill นี้เป็น alias stub เท่านั้น workflow จริงอยู่ใน `restore-files`

## Execute

ทำ `/restore-files` เต็ม workflow

## Rules

- ห้าม duplicate workflow ของ `/restore-files` ในไฟล์นี้
- ถ้า alias ขาด steps → อ่าน `restore-files/SKILL.md` เสมอ

## Expected Outcome

- `/restore-files` ถูก execute ครบทุก step
