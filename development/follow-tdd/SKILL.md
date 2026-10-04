---
name: follow-tdd
description: พัฒนา feature ด้วย Test-Driven Development red-green-refactor
argument-hint: "[setup-coverage] [scope]"
related:
  - follow-math-concepts
  - use-related-skills
  - run-verify
  - git-commit
---

## Goal

พัฒนา software ด้วย Test-Driven Development (TDD) โดยเขียน test ก่อน implementation ทำให้ feature มั่นใจ ลด regression และ design สะอาด

## Scope

ใช้เมื่องานต้องสร้าง feature หรือแก้ไข behavior ทีต้องการ regression confidence สูง โดยเริ่มจาก test ก่อนเสมอ

## Execute

### 1. Understand Requirement

> Goal: รู้ behavior ทีต้อง implement ก่อนเขียน test

1. อ่าน spec, issue, หรือ user requirement
2. ตรวจสอบ existing tests และ test framework ที project ใช้
3. ถ้าไม่มี test framework → ทำ `/use-related-skills` เพื่อหา follow-tool-vitest, follow-jest, follow-test-api
4. ระบุ smallest behavior ทีต้อง test ก่อน

### 2. Write Failing Test

> Goal: มี test ทีบอกว่า feature ยังไม่ทำงาน

1. สร้าง test สำหรับ behavior เดียว (single responsibility)
2. ใช้ test name ทีอ่านแล้วรู้ว่า test อะไร
3. รัน test ยืนยันว่า fail (red)
4. ถ้า test ผ่านทันที → ตรวจสอบ test ว่าตรวจจริง หรือ feature มีอยู่แล้ว

### 3. Make It Pass

> Goal: ทำให้ test ผ่านด้วย implementation น้อยทีสุด

1. เขียน implementation น้อยทีสุดทีทำให้ test ผ่าน
2. ไม่ refactor ใน step นี้
3. รัน test ยืนยันว่า pass (green)
4. ถ้ามี test อื่นแตก → แก้ให้ pass ทั่งหมดก่อน

### 4. Refactor

> Goal: ล้ว code ให้สะอาดโดยไม่เปลี่ยน behavior

1. ปรับชื่อ, ลบ duplication, จัด structure
2. รัน test หลังแต่ละ refactoring ยืนยันว่า still green
3. ถ้า test แตกระหว่าง refactor → ย้อนกลับและทำทีละจุด
4. หยุด refactor เมื่อ code อ่านง่ายขึ้น ไม่ over-engineer

### 5. Repeat

> Goal: ครอบคลุม behavior ทั้งหมดทีละขั้น

1. เลือก behavior ถัดไป
2. ทำ Red-Green-Refactor loop ซ้ำ
3. แต่ละ cycle commit ได้ถ้าเหมาะสม
4. หยุดเมื่องานครบ scope

### 6. Validate And Integrate

> Goal: มั่นใจว่า feature ทำงานถูกต้องบนระบบ

1. รัน test suite ทั้งหมด
2. รัน lint และ typecheck ถ้ามี
3. ทำ `/run-verify` เพื่อตรวจ project-wide
4. ทำ `/git-commit` ถ้ามีการเปลี่ยนแปลง

### Workflows

> Goal: dispatch ไปยัง workflow ตาม topic/argument

| Topic/Argument | Workflow |
|----------------|----------|
| `setup-coverage`, `coverage` | `workflows/setup-coverage/SKILL.md` — coverage tooling ตาม ecosystem (vitest, llvm-cov, go cover) |

1. ถ้า argument ตรง topic → อ่าน `workflows/<name>/SKILL.md` แล้วทำตาม flow ในนั้น — ไม่ execute จากตารางนี้โดยตรง
2. ถ้าไม่ระบุ → ทำตาม steps 1-6 ตามลำดับ

## Rules

### 1. Test First Always

- ต้องมี failing test ก่อน implementation
- ไม่เขียน production code ถ้าไม่มี test ทีต้องให้ pass

### 2. One Behavior At A Time

- แต่ละ test ตรวจ behavior เดียว
- ห้าม test หลายเรื่องใน test เดียว

### 3. Minimal Implementation

- ทำแค่พอให้ test ผ่าน
- ไม่เพิ่ม features ทียังไม่มี test

### 4. Refactor Separately

- แยก step refactor ออกจาก step ทำให้ pass
- รัน test หลัง refactor เสมอ

### 5. Run Tests Frequently

- รัน test หลังเขียน test, หลัง implement, หลัง refactor
- ใช้ watch mode ถ้ามี

### 6. Use Real Assertions

- ไม่ใช้ placeholder assertions
- ตรวจ output/behavior จริง

- ใช้ /follow-math-concepts ถ้าจำเป็น

## Expected Outcome

- Feature ถูก cover ด้วย tests ทีเขียนก่อน
- ทุก test pass
- Code ผ่าน lint/typecheck
- ไม่มี regression
- Design สะอาดและอ่านง่ายขึ้น
