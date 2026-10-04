---
name: deep-build
description: รัน build แบบลึก ครอบคลุมหลาย target, platforms, bundle analysis, และ performance smoke test
argument-hint: "[target]"
related:
  - run-build
  - run-check
  - run-verify
  - run-test
  - deep-review
  - resolve-errors
  - deep-validate
  - report
---

## Goal

Build project อย่างละเอียด ครอบคลุมทุก target ทีจำเป็น และหา build-time issues ทีซ่อนอยู่

## Scope

- ใช้กับ project ทีมี build step
- รองรับหลาย ecosystems: Node/bun, Rust, Go, Python, Docker
- ไม่ใช่แค่ `bun run build` แต่ต้อง verify outputs และ performance impact

- ดูเพิ่มเติม: /run-verify

## Execute

### 1. Detect Build Targets

> Goal: รู้ว่าต้อง build อะไรบ้าง

1. อ่าน `package.json`, `Cargo.toml`, `Dockerfile` หรือ build config ทีเกี่ยวข้อง
2. ระบุ targets: dev, prod, ssr, static, docker, mobile, desktop
3. ถ้าไม่ชัด → ทำ `/ask-me`

### 2. Clean Build

> Goal: เริ่ม build จาก clean state

1. ทำ `/run-clean` ถ้ามี
2. รัน `bun install` หรือ package manager install เพื่อ lockfile fresh
3. ลบ `dist/`, `build/`, `.next/`, `target/` ถ้าจำเป็น

### 3. Run Build

> Goal: build ทุก target

1. ทำ `/run-build` สำหรับ default target
2. ถ้ามี production build → รัน `bun run build:prod` หรือ equivalent
3. ถ้ามี SSR / SSG → รัน target นั้น
4. ถ้ามี Docker → ทำ `/run-build` แล้ว `docker build` dry-run
5. ถ้ามี Rust → รัน `cargo build --release`

### 4. Analyze Output

> Goal: หา build-time issues

1. ตรวจขนาด output / bundle size
2. ตรวจ source maps, assets, chunks
3. ตรวจ warnings / errors ที build อาจข้าม
4. ใช้ `/deep-review` ถ้า bundle ใหญ่ หรือ `/deep-optimize` ถ้ามี performance issue
5. ใช้ `/deep-review` ถ้าจำเป็น

### 5. Smoke Test

> Goal: ยืนยันว่า build ใช้งานได้

1. รัน `/run-test` หรือ `/deep-test e2e` ถ้ามี
2. ถ้า build ใช้ไม่ได้ → ทำ `/resolve-errors`
3. ทำ `/run-check` เพื่อ lint/typecheck

### 6. Report

> Goal: สรุปผล build

1. ทำ `/report` พร้อม targets, outputs, issues, bundle size
2. ทำ `/deep-validate`
3. ทำ `/suggest-next-action`

## Rules

- ต้อง clean build ก่อนรัน
- ไม่ ignore build warnings
- ต้อง smoke test หลัง build
- ถ้ามี multiple targets ต้อง build ทั้งหมดที user ระบุ
- ใช้ `/resolve-errors` ถ้า build fail

## Expected Outcome

- Build ผ่านทุก target
- Bundle / output ถูก analyze
- ไม่มี build-time issues ซ่อน
- รายงานผล build พร้อม next action
