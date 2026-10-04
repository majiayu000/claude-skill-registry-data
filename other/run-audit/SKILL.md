---
name: run-audit
description: Audit dependencies และ security เพื่อตรวจสอบ vulnerabilities
argument-hint: "[scope]"
related:
  - deep-review
  - follow-best-practice
  - suggest-next-action
  - resolve-errors
  - run-check
  - run-verify

---

## Goal

Audit dependencies และ security เพื่อตรวจสอบ vulnerabilities

## Scope

ใช้ `run-audit` สำหรับ tasks และ workflows เฉพาะที่ครอบคลุม (audit)

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (audit)

### 1. Audit Dependencies

> Goal: Audit Dependencies

1. รัน `npm audit` หรือ `bun audit`
2. ตรวจสอบ vulnerabilities ใน dependencies
3. ดู severity levels ของ vulnerabilities

### 2. Audit Licenses

> Goal: Audit Licenses

1. ตรวจสอบ licenses ของ dependencies
2. ระบุ licenses ที่ไม่เหมาะสม
3. ตรวจสอบ compliance requirements

### 3. Audit Code

> Goal: Audit Code

1. สแกน code หา security vulnerabilities
2. ตรวจสอบ hardcoded secrets
3. ตรวจสอบ insecure patterns

### 4. Review Findings

> Goal: Review Findings

1. จัดลำดับ priorities ของ issues
2. วิเคราะห์ impact ของแต่ละ issue
3. กำหนด action items

### 5. Fix Issues

> Goal: Fix Issues

1. อัพเดท dependencies ที่มี vulnerabilities
2. แก้ไข security issues ใน code
3. ทดสอบหลังแก้ไข

### 6. Generate Report

> Goal: Generate Report

1. สร้าง audit report
2. แชร์ findings กับทีม
3. ติดตาม remediation progress

## Rules

### 1. Audit Frequency

- Audit dependencies เป็นระยะ
- Audit หลังเพิ่ม dependencies ใหม่
- Audit ก่อน releases สำคัญ

### 2. Severity Handling

- Critical/High: แก้ไขทันที
- Medium: แก้ไขใน sprint ถัดไป
- Low: แก้ไขเมื่อมีเวลา

### 3. License Compliance

- ตรวจสอบ license compatibility
- ระบุ copyleft licenses
- ติดตาม license obligations

- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น
- ใช้ /run-check ถ้าจำเป็น
- ใช้ /run-verify ถ้าจำเป็น

## Expected Outcome

- Dependencies ถูก audit
- Vulnerabilities ถูกระบุและแก้ไข
- License compliance ถูกตรวจสอบ
- Security issues ถูกแก้ไข
- Audit report ถูกสร้าง
- Remediation progress ถูกติดตาม
