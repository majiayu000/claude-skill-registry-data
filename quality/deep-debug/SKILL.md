---
name: deep-debug
description: Debug อย่างละเอียดหลายมิติ ตั้งแต่ reproduce จนถึง prevent recurrence
argument-hint: "[scope]"
related:
  - validate-then-apply
  - check-git-logs
  - analyze-root-cause-analysis
  - resolve-errors
  - deep-thinking
  - report
  - report-progress
  - suggest-next-action
  - run-check
  - run-test-all
  - run-until-pass
---

## Goal

ปฏิบัติตามหลักการ debug ที่เป็นระบบ เพื่อหา root cause ได้เร็วและแม่นยำ ลดการเดา และป้องกันปัญหาซ้ำ

## Scope

ใช้สำหรับทุก debugging session — runtime errors, test failures, build errors, deployment issues, performance problems

## Execute

### 1. Reproduce Consistently

> Goal: สร้าง reproduction case ที่ trigger ปัญหาได้สม่ำเสมอก่อนเริ่ม debug

1. สร้าง minimal reproduction case ที่ trigger ปัญหาได้ทุกครั้ง
2. ระบุ exact steps, input, environment ที่ทำให้เกิดปัญหา
3. ถ้า reproduce ไม่ได้ ให้เก็บ logs, screenshots, และ environment info ไว้ก่อน
4. ใช้ `/use-bun-shell` เพื่อรัน reproduction script ซ้ำจนกว่าจะ stable

### 2. Define Problem Clearly

> Goal: กำหนดปัญหาแบบ Expected vs Actual พร้อม scope และ impact ชัดเจน

1. เขียนปัญหาแบบ Expected vs Actual
2. ระบุ scope: file, function, module, API endpoint, หรือ system level
3. ระบุ frequency: always, intermittent, หรือ under specific conditions
4. ระบุ impact: blocking, degraded, หรือ cosmetic

### 3. Gather Evidence

> Goal: เก็บ error messages, logs, และ context ที่เกี่ยวข้องทั้งหมด

1. เก็บ error messages, stack traces, และ logs ทั้งหมด
2. ใช้ `/run-test` เพื่อดูว่า tests ไหน fail
3. ตรวจสอบ recent changes ด้วย `git log` และ `git diff`
4. ตรวจสอบ environment: runtime version, dependencies, config
5. ถ้ามี monitoring ให้เก็บ metrics และ traces ด้วย

### 4. Form Hypotheses

> Goal: สร้างและจัดลำดับ hypotheses ตาม evidence ไม่ใช่ความรู้สึก

1. สร้าง 3-5 hypotheses ที่เป็นไปได้
2. จัดลำดับตาม probability และ ease of testing
3. ทำ `/deep-thinking` เพื่อใช้ Bayesian approach ในการจัดลำดับ
4. เลือก top 1-2 hypotheses ที่ test ง่ายและมี probability สูงสุด

### 5. Test And Eliminate

> Goal: ทดสอบทีละ hypothesis เปลี่ยนทีละ variable เพื่อตัดที่ไม่ใช่

1. ทดสอบทีละ hypothesis — เปลี่ยนทีละ variable เท่านั้น
2. ใช้ `/use-bun-shell` เพื่อ execute test แต่ละ hypothesis
3. บันทึกผลลัพธ์ทุกครั้ง: pass, fail, หรือ inconclusive
4. ตัด hypothesis ที่ไม่ใช่ แล้วไปถัดไป
5. ถ้าทดสอบหมดแล้วไม่ตรง ให้กลับไปสร้าง hypotheses ใหม่

### 6. Isolate Root Cause

> Goal: ยืนยัน root cause ที่ reproduce ได้ แก้แล้วหาย ถอนแล้วกลับมา

1. ทำ `/analyze-root-cause-analysis` เพื่อวิเคราะห์หาสาเหตุหลัก
2. ใช้ 5 Whys เพื่อ trace จาก symptom ไป root cause
3. ยืนยัน root cause ด้วย 3 เงื่อนไข: reproduce ได้, fix แล้วหาย, กลับมาถ้าถอน fix
4. ตรวจสอบว่าไม่ใช่ symptom ของปัญหาที่ลึกกว่า

### 7. Validate And Fix

> Goal: แก้น้อยที่สุดที่จบ root cause แล้ว verify ว่าไม่ทำลายอย่างอื่น

1. ทำ `/validate-then-apply` เพื่อ validate ก่อนแก้
2. ทำ `/resolve-errors` เพื่อแก้ไข error ที่พบ
3. แก้น้อยที่สุด — minimal change ที่แก้ root cause ไม่ใช่ symptom
4. ทำ `/run-test` เพื่อยืนยันว่า fix ใช้งานได้
5. ทดสอบว่า fix ไม่ทำลาย functionality อื่น
6. ทำ `/run-lint` และ `/run-typecheck` เพื่อตรวจสอบ code quality

### 8. Prevent Recurrence

> Goal: เพิ่ม test case และปรับปรุง debuggability เพื่อป้องกันปัญหาซ้ำ

1. เพิ่ม test case สำหรับป้องกัน regression — ทำ `/follow-tool-vitest` หรือ `/follow-tool-playwright`
2. ทำ `/deep-review` ถ้าพบว่า debug ยากเพราะ logging ไม่พอ
3. อัปเดท documentation ถ้าปัญหาเกี่ยวกับ config หรือ setup
4. บันทึก root cause และ solution ใน `docs/` หรือ commit message

### 9. Report

> Goal: สรุปผล debug และ next action

1. ทำ `/report table` คอลัมน์: `No.`, `Step`, `Hypothesis`, `Result`, `Status`
2. สรุป root cause, fix, regression tests, preventive measures
3. ทำ `/report-progress` ถ้ามีหลาย step
4. ทำ `/suggest-next-action`

## Rules

### 1. Core Principles

- ห้ามเดา — ทุก hypothesis ต้องมี evidence สนับสนุน
- ห้ามแก้หลายอย่างพร้อมกัน — เปลี่ยนทีละ variable
- ห้ามแก้ symptom — ต้องถึง root cause
- ห้าม bypass — ไม่ใช้ `@ts-ignore`, `eslint-disable`, หรือ try-catch ซ่อน error
- ต้อง reproduce ได้ก่อนแก้
- ทุก fix ต้องผ่าน `/validate-then-apply` ก่อน apply

### 2. Debug Strategy

- ไล่จากบนลงล่าง: UI → API → Database → Infrastructure
- ไล่จาก narrow ไป broad: specific function → module → system
- ใช้ binary search สำหรับ large codebase
- ถ้า intermittent ให้เก็บ log ทุกครั้งจนกว่าจะ pattern ชัด
- ถ้า environment-specific ให้เปรียบเทียบ working vs broken environment

### 3. Logging For Debug

- ใช้ structured logging ไม่ใช่ `console.log`
- ใส่ context: function name, input values, state
- ใช้ log levels: `debug`, `info`, `warn`, `error`
- หลัง fix ให้ลบ debug logging ที่ไม่จำเป็น

### 4. Tool Selection

- Runtime errors → `/resolve-errors` + `/deep-thinking`
- Test failures → `/run-test` + `/follow-tool-vitest`
- E2E failures → `/follow-tool-playwright`
- Build errors → `/run-build` + `/resolve-errors`
- Type errors → `/run-typecheck` + `/follow-lang-typescript`
- Performance → `/run-profiler` + `/deep-review`
- Git issues → `/follow-tool-git` + `/check-git-logs`

### 5. Time Budget And Escalation

- ปัญหาเล็ก: ≤ 5 นาที | กลาง: ≤ 15 นาที | ใหญ่: ≤ 30 นาที
- ถ้าเกินเวลา → ทำ `/deep-thinking` หรือ `/deep-research`
- ถ้าหา root cause ไม่ได้หลังพยายาม 3 รอบ → ทำ `/deep-thinking` หรือขอความช่วยเหลือ
- ใช้ /run-check ถ้าจำเป็น
- ใช้ /run-test-all ถ้าจำเป็น
- ใช้ /run-until-pass ถ้าจำเป็น
- alias stub: `/follow-debugging` — forward มาที่ skill นี้

## Expected Outcome

- Root cause หาได้เร็วและแม่นยำ
- ไม่มีการเดาหรือแก้หลายอย่างพร้อมกัน
- Fix แก้ที่ root cause ไม่ใช่ symptom
- มี test case ป้องกัน regression
- Debugging experience ดีขึ้นเรื่อยๆ
