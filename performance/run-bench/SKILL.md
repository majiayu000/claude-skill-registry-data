---
name: run-bench
description: รัน benchmark tests เพื่อวัดประสิทธิภาพและเปรียบเทียบ performance
argument-hint: "[scope]"
related:
  - deep-review
  - run-install

  - deep-review
  - report
---

## Goal

รัน benchmark tests เพื่อวัดประสิทธิภาพของ code และเปรียบเทียบ performance ระหว่าง implementations

## Scope

ใช้สำหรับวัด performance ของ functions, เปรียบเทียบ implementations ต่างๆ, ตรวจสอบ performance regressions, และ optimize code ตามผล benchmark

## Execute

> Pre-Run: ทำ `/deep-review` ก่อนเสมอ — `run-*` ต้อง review/ประเมินก่อนลงมือหลัก ห้ามข้าม; ถ้า findings เป็น blocker ให้แก้หรือ report ก่อนรัน (bench)

### 1. Setup Environment

> Goal: Setup Environment

1. ทำ `/run-install` เพื่อติดตั้ง dependencies และ benchmark libraries (เช่น `vitest bench`, `tinybench`)
2. ตรวจสอบว่ามี benchmark files ใน project (เช่น `*.bench.ts`, `bench/` directory)
3. ตรวจสอบ benchmark script ใน `package.json` (เช่น `bun run bench`)
4. ถ้ามี baseline results ให้บันทึกไว้สำหรับการเปรียบเทียบ

### 2. Run Benchmarks

> Goal: Run Benchmarks

1. รัน `bun run bench` หรือ script ที่กำหนดใน `package.json`
2. ถ้าต้องการรันเฉพาะ benchmark ให้ระบุ pattern (เช่น `bun run bench -- --grep "pattern"`)
3. รอ benchmarks เสร็จสิ้นและบันทึกผลลัพธ์ทั้งหมด
4. ทำ `/report` เพื่อจัดรูปแบบผลลัพธ์

### 3. Analyze Results

> Goal: Analyze Results

1. ดูผลลัพธ์ของแต่ละ benchmark และระบุ slow และ fast benchmarks
2. ทำ `/deep-review` อ้างอิง `deep-review/SKILL.md` เพื่อวิเคราะห์ว่า empirical growth ตรงกับ theoretical complexity
3. หา benchmarks ที่มี variance สูงหรือ outliers
4. ระบุ potential optimizations สำหรับ slow benchmarks
5. ถ้ามี variance สูง ให้รันซ้ำเพื่อยืนยันผลลัพธ์

### 4. Compare With Baseline

> Goal: Compare With Baseline

1. เปรียบเทียบผลลัพธ์กับ baseline ถ้ามี
2. ระบุ regressions (ช้าลง) และ improvements (เร็วขึ้น)
3. บันทึกผลลัพธ์และ action items สำหรับ optimization
4. ทำ `/report` เพื่อสรุปผลลัพธ์เป็นตาราง

## Rules

### 1. Benchmark Best Practices

- แต่ละ benchmark ต้องแยกจากกัน (isolated)
- รันหลายๆ ครั้งเพื่อ consistency
- ใช้ data ที่สมจริงและเป็นตัวแทนของ use case จริง
- ลด overhead ของ test framework ให้น้อยที่สุด

### 2. Metrics To Collect

- `ops/sec` - operations per second
- `avg time` - average execution time
- `min/max` - min/max execution time
- `samples` - number of samples

### 3. Conditional Execution

- ถ้า project ไม่มี benchmark files ให้ข้ามขั้นตอนการรัน
- ถ้าไม่มี baseline results ให้ข้ามขั้นตอนการเปรียบเทียบ
- ถ้ามีหลาย workspace ใน monorepo ให้รัน benchmark ทีละ workspace

## Expected Outcome

- Benchmarks รันสำเร็จ
- Metrics ถูกบันทึกครบถ้วน (`ops/sec`, `avg time`, `min/max`, `samples`)
- Regressions และ improvements ถูกระบุ
- Action items สำหรับ optimization ถูกบันทึก
