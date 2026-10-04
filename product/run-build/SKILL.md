---
name: run-build
description: รัน build process อย่างเป็นระบบเพื่อสร้าง production-ready artifacts
argument-hint: "[scope]"
related:
  - deep-review
  - run-typecheck
  - resolve-errors
  - run-clean

  - report
---

## Goal

รัน build process อย่างเป็นระบบเพื่อสร้าง production-ready artifacts

## Scope

ใช้กับ project ที่มี build script ใน package manifest โดย optimize build configuration ก่อน build

## Execute

### 1. Optimize Build

> Goal: ปรับปรุง build configuration และลดขนาด output ก่อน build

1. ทำ `/deep-review` เพื่อวิเคราะห์ bundle size, build config, manual chunks, และ externalization
2. ทำ `/deep-review` เพื่อปรับปรุง build configuration, dependencies, imports และ assets
3. ถ้า `/deep-review` หรือ `/deep-review` ล้มเหลว → stop และ report

### 2. Typecheck

> Goal: ตรวจสอบ TypeScript types ก่อน build

1. ทำ `/run-typecheck` เพื่อตรวจสอบ TypeScript types
2. ถ้ามี type errors → ทำ `/resolve-errors` แล้ว retry ตั้งแต่ `/run-typecheck` (max 3 → stop)

### 3. Install Dependencies

> Goal: ติดตั้ง dependencies ที่จำเป็น

1. รัน `bun install`
2. ตรวจสอบว่า dependencies ติดตั้งครบถ้วน

### 4. Clean Build Artifacts

> Goal: ลบ artifacts เก่าเพื่อ build ใหม่

1. ทำ `/run-clean` เพื่อลบ build artifacts และ cache เก่า

### 5. Execute Build

> Goal: รัน build command ตาม package manifest

1. รัน `bun run build` หรือ build script ที่กำหนด
2. บันทึกเวลาที่ใช้
3. จับ output และ error แยกกัน

### 6. Verify Output

> Goal: ตรวจสอบ build artifacts

1. ตรวจสอบว่า build artifacts ถูกสร้าง
2. ตรวจสอบ file size และจำนวน output files ที่เหมาะสม

### 7. Report

> Goal: สรุปผล build

1. รัน `/report` เพื่อแสดง build metrics (time, size, files)
2. รัน `/report` เพื่อแสดงสรุปผลลัพธ์

## Rules

### 1. Build Order

- Optimize: ทำ `/deep-review` ก่อน แล้วทำ `/deep-review`
- Typecheck: ทำ `/run-typecheck` ก่อน build
- Install: ติดตั้ง dependencies
- Clean: ทำ `/run-clean` เพื่อลบ artifacts เก่า
- Build: รัน build command
- Verify: ตรวจสอบ output

### 2. Error Handling

- Typecheck ล้มเหลว: ทำ `/resolve-errors` ก่อน build
- Build ล้มเหลว: ทำ `/resolve-errors` เพื่อแก้ไข
- Warning: บันทึกและพิจารณาแก้ไข

### 3. Reporting

- ใช้ `/report` สำหรับ metrics
- ใช้ `/report` สำหรับสรุปข้อความ
- ไม่รายงานซ้ำซ้อน

## Expected Outcome

- Build สำเร็จไม่มี errors
- Typecheck ผ่านทั้งหมด
- Build artifacts ถูกต้อง
- Output size และ build time ถูกปรับปรุง

## Example Template

```markdown
---
title: Run Build
description: รัน build process สำหรับ production-ready artifacts
auto_execution_mode: 3
related:
  - /deep-review
  - /run-typecheck
  - /run-clean
  - /resolve-errors
---

### Goal

รัน build process สำหรับ production-ready artifacts

### Scope

ใช้กับ project ที่มี build script

### Execute

#### 1. Optimize Build

> Goal: build config พร้อม

1. ทำ `/deep-review`

#### 2. Typecheck

> Goal: ไม่มี type errors

1. ทำ `/run-typecheck`
2. ถ้ามี errors → ทำ `/resolve-errors`

#### 3. Build

> Goal: build สำเร็จ

1. ทำ `/run-clean`
2. รัน build command

#### 4. Report

> Goal: สรุปผล

1. ทำ `/report`
2. ทำ `/report`

### Rules

#### 1. Order

- Optimize ก่อน build

### Expected Outcome

- Build สำเร็จ
```
