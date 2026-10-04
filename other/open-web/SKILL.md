---
name: open-web
description: เปิด website ด้วย native OS command
argument-hint: "[scope]"
related:
  - use-agent-browser
  - watch-browser
  - run-dev
---

## Goal

เปิด website ด้วย native OS command

## Scope
- สำหรับ skills ที่เกี่ยวข้อง: `open-files-in-web`, `use-agent-browser`, `watch-browser-and-fix`

ใช้ `open-web` เมื่อต้องเปิด URL ใน external browser หรือ integrated browser

## Execute

### 1. Open Website

> Goal: Open Website

เปิด website ด้วย native OS command

1. รับ URL จาก user
2. ตรวจสอบ URL ว่าถูกต้อง
3. พิจารณาเปิดใน integrated browser หรือ external browser:
   - integrated: ถ้า user ขอหรือ context รองรับ `browser_preview` tool → เรียก `browser_preview`
   - external: ใช้ default browser ของระบบ
4. ใช้ native OS command สำหรับ external browser:
   - Windows: `start <url>`
   - macOS: `open <url>`
   - Linux: `xdg-open <url>`
5. ตรวจสอบว่า website เปิดถูกต้อง

## Rules

- ไม่ใช้ `open` CLI tool แบบ standalone; ใช้ native OS command เท่านั้น
- ตรวจสอบ URL ก่อนเปิด
- ใช้ `browser_preview` tool สำหรับ integrated browser เมื่อ context รองรับ
- ใช้ default browser ของระบบสำหรับ external browser
- ใช้ /run-dev ถ้าจำเป็น

## Expected Outcome

- Website เปิดใน browser ที่เลือก
- URL ถูกต้อง

