---
name: optimize
description: หา optimization opportunities ใน scope — baseline → /deep-review-codebase → fix → re-measure ตาม scope-map
argument-hint: "[scope]"
related:
  - deep-optimize
  - deep-review-codebase
  - deep-review-codebase-then-fix
  - improve
  - run-bench
  - report
  - suggest-next-action
  - ask-me
---

## Goal

ตอบคำถาม "optimize อะไรได้บ้าง" สำหรับ scope ที่ user ระบุ — เป็น thin entry ที่ route scope ผ่าน `references/scope-map.md` (SSOT: signal → review domain) เข้า `/deep-review-codebase` แล้วทำ Measure → optimize → re-measure ตาม convention ใน skill นี้ ไม่ทำ optimization เอง

## Scope

ใช้เมื่อ user สั่ง optimize ทั้ง scope โดยยังไม่เจาะ domain — เดิม route ไป `optimize-*` ตัวใดตัวหนึ่ง ตอนนี้ทุกมิติรวมที่นี่:

- scope/metric ชัด (bundle, ci, cost, llm, docker, memory, network, perf, queries, startup, api-latency, cache, concurrency, images, mobile, storage, test-suite, web-vitals) → ใช้ `/optimize <scope>` ตรงๆ ตาม `references/scope-map.md`
- scope กว้าง หรือ bottleneck ไม่ชัด → `/deep-optimize` fan-out ทุกมิติ แล้วรวม prioritized plan
- ต้องการ improve คุณภาพทั่วไป ไม่ใช่ performance/cost → `/improve` แทน
- ทุกรายการต้องผ่าน measure-first convention ของ skill นี้: ห้าม optimize แบบไม่วัด baseline

## References

- `references/scope-map.md` — ตาราง SSOT: signal → `/optimize <scope>` → `/deep-review-codebase` domain (รวมจาก `/follow-optimize` เดียวที่ถูกยุบเข้า skill นี้ — ครอบครบ 18 สัญญาณ)

## Execute

### 1. Route And Baseline

> Goal: เลือกมิติที่ถูก + มี evidence ก่อนแก้

1. รับ `scope` จาก argument — ถ้าไม่มี → ใช้ project ปัจจุบัน ถ้าไม่ชัด → `/ask-me`
2. Lookup signal ใน scope จาก `references/scope-map.md` → ได้ `/deep-review-codebase` domain ที่ตรง
3. เก็บ baseline metrics ตาม dimะนั้น (เวลา, size, cost, hit rate, p50/p95/p99) ผ่าน `/run-bench`/profiler เท่าที่มี — ห้ามข้าม

### 2. Review

> Goal: findings มี baseline รองรับ

1. ทำ `/deep-review-codebase` กับ scope นั้นใน domains จาก scope-map — report ผ่าน `/report-review`
2. คัดเฉพาะ finding ที่วัดผลได้ (metric เปลี่ยนจริง) — ไม่มี evidence = ไม่แก้

### 3. Fix And Re-Measure

> Goal: ผลลัพธ์วัดได้จริง

1. ทำ `/report` แสดง improvements: No., Finding, Metric ก่อน/หลัง, Fix domain แล้วดำเนินการแก้ต่อทันที
2. ส่งแต่ละ finding ไป `/deep-review-codebase-then-fix` per domain
3. re-measure เทียบ baseline ทุก fix — ไม่ดีขึ้น → revert; ทำ `/suggest-next-action` หลังแก้ครบ

## Rules

- ไม่ทำ optimization เอง — route ผ่าน scope-map เข้า `/deep-review-codebase` หรือใช้ `/deep-optimize` เมื่อไม่ชัด — thin entry ไม่ hold domain logic
- Measure → optimize → re-measure เสมอ — ห้าม premature optimization
- ทุก plan/finding ต้อง prioritized ด้วย impact/effort พร้อม baseline evidence — ไม่มี evidence = ไม่แก้
- metric-driven findings ที่หลุดมาจาก `/improve` รับ route ต่อที่นี่ — ไม่แก้ perf ใน improve path

## Expected Outcome

- Prioritized optimization list พร้อม baseline/หลังแก้เปรียบเทียบ
- Fixes ทั้งหมด route ผ่าน `/deep-review-codebase-then-fix` ตาม domain ของ scope-map
- Metric ไม่ดีขึ้นถูก revert — จบด้วย `/suggest-next-action`
