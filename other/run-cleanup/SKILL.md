---
name: run-cleanup
description: รัน cleanup tasks เพื่อลบ build artifacts และ cache
argument-hint: "[scope]"
related:
  - check-long-files
  - cleanup-files-in-computer
  - cleanup-files-in-project
  - cleanup
  - run-check
  - run-verify
  - suggest-next-action
  - run-clean
---

## Goal

รันการทำความสะอาด

## Scope

ใช้ `run-cleanup` สำหรับ tasks และ workflows เฉพาะที่ครอบคลุม (cleanup)

## Execute

> Pre-Run: ตรวจ locked files ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (cleanup)

### 1. Identify Cleanup Targets

> Goal: ระบุ artifacts และ cache ที่ต้องลบ

1. อ่าน `.gitignore` เพื่อหา ignored paths ที่เป็น build artifacts
2. ระบุ targets ตาม language/stack:
   - Node.js: `node_modules/`, `dist/`, `.nuxt/`, `.next/`, `.turbo/`
   - Rust: `target/`
   - Python: `__pycache__/`, `.pytest_cache/`, `*.pyc`
   - Go: `vendor/`, `bin/`
   - General: `.cache/`, `coverage/`, `*.log`
3. ถ้ามี stale branches หรือ worktrees → ทำ `/cleanup-git-branch` หรือ `/cleanup-worktree`

### 2. Run Cleanup

> Goal: ลบ artifacts อย่างปลอดภัย

1. ลบ build artifacts ด้วย command ที่เหมาะสม (`rm -rf`, `cargo clean`, `bun pm cache rm` ฯลฯ)
2. ถ้าต้องการ system-wide cleanup → ทำ `/cleanup-files-in-computer`
3. ถ้าต้องการ project cleanup → ทำ `/cleanup-files-in-project`
4. ถ้ามี file locks → ปิด process ที่ lock แล้วลบใหม่

### 3. Verify

> Goal: ยืนยันว่า cleanup สำเร็จ

1. ตรวจสอบว่า targets ถูกลบแล้ว
2. ทำ `/run-check` เพื่อยืนยันว่า project ยังทำงานได้
3. ทำ `/run-verify` ถ้าต้องการ verify ครบวงจร
4. ทำ `/report` แสดง artifacts ที่ลบและพื้นที่ที่คืน

## Rules

- ลบเฉพาะ artifacts ที่อยู่ใน `.gitignore` หรือเป็น build output
- ไม่ลบ source files, config, หรือ user data
- ถ้ามี file locks → แก้ก่อนลบ
- ใช้ `/cleanup-files-in-computer` สำหรับ system cleanup
- ใช้ `/cleanup-files-in-project` สำหรับ project cleanup
- ใช้ `/cleanup-git-branch` สำหรับ branch cleanup
- ใช้ `/suggest-next-action` หลังเสร็จเพื่อแนะนำขั้นตอนถัดไป
- ใช้ /run-clean ถ้าจำเป็น

## Expected Outcome

- Build artifacts และ cache ถูกลบ
- Disk space ถูกคืน
- Project ยังทำงานได้หลัง cleanup
- รายงาน artifacts ที่ลบและพื้นที่ที่คืน
