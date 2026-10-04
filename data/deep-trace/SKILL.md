---
name: deep-trace
description: Trace ลึกตาม execution flow, logs, metrics, หรือ distributed trace
argument-hint: "[scope]"
related:
  - deep-debug
  - analyze-root-cause-analysis
  - run-profiler
  - watch-browser-and-fix
  - use-astgrep
  - search
  - report
  - follow-tool-git

---

## Goal

Trace ลึกตามทางเดินของ execution, data flow, request lifecycle, logs, metrics, หรือ distributed traces เพื่อหาจุดทีผิดปกติ

## Scope

ใช้เมื่อต้องการรู้ว่า code ทำงานยังไง, ข้อมูลไหลไปไหน, request ผ่านอะไรบ้าง, หรือ error เกิดตรงไหน
เหมาะสำหรับ async timing, race condition, distributed system, data pipeline, หรือ request path
ไม่ใช้สำหรับหา root cause ทั่วไป — ใช้ `/deep-debug`
ไม่ใช้สำหรับดู performance ล้วนๆ — ใช้ `/run-profiler`

## Execute

### 1. Define Trace Target

> Goal: ระบุสิ่งทีต้อง trace

1. ระบุ target: function, request, event, variable, error, latency spike
2. ระบุ entry point และ expected exit point
3. ระบุ boundaries ทีต้องข้าม: process, network, database, queue, service
4. ทำ `/deep-thinking` ถ้า trace target ซับซ้อน

### 2. Choose Trace Source

> Goal: เลือกแหล่งข้อมูลทีเหมาะสม

1. ถ้ามี logs → ใช้ structured logs หา correlation id หรือ request id
2. ถ้ามี metrics → ดู dashboard หา spike หรือ pattern
3. ถ้ามี distributed traces → ใช้ trace id เพื่อตาม path
4. ถ้าไม่มี telemetry → ใช้ code reading: `/search-files-patterns`, `/use-astgrep`
5. ถ้าต้องดู runtime → เพิ่ม temporary instrumentation

### 3. Instrument If Needed

> Goal: เพิ่ม visibility ถ้า trace ไม่ชัด

1. เพิ่ม structured logs ชั่วคราว: function name, input, output, state
2. เพิ่ม metrics ชั่วคราว สำหรับ duration หรือ count
3. เพิ่ม trace span ถ้าใช้ OpenTelemetry หรือ observability tool
4. ระบุว่า instrumentation เป็นชั่วคราว ต้องลบหลัง trace เสร็จ
5. ไม่เพิ่ม `console.log` ถาวร

### 4. Reproduce And Capture

> Goal: สร้าง trace data ที repeat ได้

1. สร้าง reproduction case สำหรับ target
2. รันและ capture logs, metrics, traces
3. ใช้ correlation id หรือ request id เดียวกัน
4. บันทึก timestamp, environment, input
5. ถ้า trace ไม่เสถียร → ทำซ้ำ 3-5 ครั้ง

### 5. Follow The Path

> Goal: ตามทางเดินของ execution หรือ data

1. เริ่มจาก entry point ไปจนถึง exit point
2. บันทึกทุก step: function, service, database, queue, external API
3. ตรวจสอบ state/variable ทีเปลี่ยนแปลงในแต่ละ step
4. ระบุ async point, await, callback, event loop cycle
5. ใช้ `/use-astgrep` หรือ `/search-files-patterns` เพื่อหา call graph

### 6. Identify Boundary Crossings

> Goal: หาจุดทีข้อมูลหรือ control ข้าม boundary

1. ระบุ network call: HTTP, gRPC, message queue
2. ระบุ database operations: query, transaction, migration
3. ระบุ process boundaries: microservices, workers, edge functions
4. ตรวจสอบ serialization/deserialization, encoding, timeout, retry
5. ระบุ clock, ordering, concurrency boundary

### 7. Pinpoint Anomaly

> Goal: หาจุดทีผิดปกติใน trace

1. เปรียบเทียบ expected flow กับ actual flow
2. หาความล่าช้า, missing event, duplicated event, unexpected error
3. หา state ทีไม่ตรงกับ expectation
4. ใช้ diff หรือ side-by-side ของ flow ทีเคยทำงาน กับ flow ทีเสีย
5. ทำ `/analyze-root-cause-analysis` ถ้าต้องการ causal chain

### 8. Fix And Verify

> Goal: แก้ปัญหาและยืนยันว่า trace กลับมาถูกต้อง

1. ทำ `/resolve-errors` สำหรับ fix เฉพาะจุด
2. ถ้าแก้โครงสร้าง flow → ทำ `/deep-impact` ก่อน
3. ลบ instrumentation ชั่วคราว
4. รัน reproduction case ซ้ำและ capture trace ใหม
5. ตรวจสอบว่า flow กลับมาตรงกับ expected
6. รัน test suite ทั้งหมดเพื่อยืนยัน

## Rules

### 1. One Trace At A Time

- ติดตาม target เดียวในแต่ละ trace session
- ไม่ trace หลายสิ่งพร้อมกัน
- บันทึกทุก step เพื่อ reproducibility

### 2. Structured Telemetry

- ใช้ structured logs ไม่ใช่ ad-hoc print
- ใช้ correlation id / request id / trace id
- อย่าเพิ่ม telemetry ถาวรโดยไม่จำเป็น

### 3. Tool First

- ใช้ existing observability ก่อนเพิ่ม log
- ใช้ `/search-files-patterns` และ `/use-astgrep` เพื่อ trace in code
- ใช้ `/run-profiler` ถ้าต้องการ latency breakdown

### 4. Boundary Aware

- ให้ความสำคัญกับ boundary crossings
- ตรวจสอบ network, database, serialization, concurrency
- ไม่มองข้าม async หรือ event-driven flow

- ใช้ /watch-browser-and-fix ถ้าจำเป็น
- ใช้ /report ถ้าจำเป็น
- ใช้ /follow-tool-git ถ้าจำเป็น

## Expected Outcome

1. รายการ step-by-step ของ execution หรือ data flow
2. จุดทีผิดปกติและ evidence
3. Causal chain ของปัญหา
4. Fix ทีเป้าหมายชัดเจน
5. Trace data ที reproduce ได้
6. Regression tests ป้องกัน flow ผิดซ้ำ
