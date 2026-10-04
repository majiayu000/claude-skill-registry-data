---
name: deep-retro
description: ทำ post-incident retrospective ลึก หา root cause ระดับ process และ action items
argument-hint: "[scope]"
related:
  - follow-incident-triage
  - deep-debug
  - analyze-root-cause-analysis
  - deep-thinking
  - report
  - update-tests
  - follow-tool-git

---

## Goal

ทำ post-incident / post-project retrospective อย่างลึกซึ้ง เพื่อหา root cause ระดับ process สร้าง learnings ที actionable และกำหนด action items ทีป้องกันปัญหาซ้ำ

## Scope

ใช้หลัง incident, failed deployment, major bug, project milestone, หรือเมื่อทีมต้องการทบทวนว่าทำไมสิ่งทีเกิดขึ้นถึงเกิดขึ้นได้
ไม่ใช้สำหรับ debug ปัญหาเฉพาะหน้า — ใช้ `/deep-debug` ก่อน
ไม่ใช้สำหรับทบทวนงานทีไม่มี incident — ใช้ `/deep-review` แทน

## Execute

### 1. Define Retro Scope

> Goal: ระบุว่าทบทวนเรื่องอะไร เพื่ออะไร

1. ระบุ incident หรือ event ที่ต้อง retro: อาการ, ระยะเวลา, ผลกระทบ
2. ระบุ stakeholder ที่ควรเข้าร่วมหรือให้ข้อมูล
3. กำหนด timebox: เล็ก ≤ 30 นาที | กลาง ≤ 1 ชั่วโมง | ใหญ่ ≤ 2 ชั่วโมง
4. เก็บ context เบื้องต้น: logs, metrics, timeline, การแจ้งเตือน

### 2. Build Timeline

> Goal: สร้าง timeline ทีละเอียดตั้งแต่ก่อน incident ถึงหลัง resolve

1. รวบรวมเหตุการณ์ทีเกิดขึ้นตามลำดับเวลา
2. ระบุ trigger, detection, response, mitigation, resolution
3. ทำ `/report` เพื่อแสดง timeline: Time, Event, Actor, Evidence
4. ตรวจสอบ gap หรือความล่าช้าในแต่ละช่วง

### 3. Gather Evidence

> Goal: รวบรวมข้อมูลให้ครบก่อนวิเคราะห์

1. ทำ `/deep-debug` ถ้ายังไม่มี root cause ทีชัดเจน
2. ทำ `/analyze-root-cause-analysis` เพื่อหา causal graph
3. เก็บ logs, traces, metrics, screenshots, error messages
4. เก็บการตัดสินใจและการสื่อสารระหว่างทีม
5. ตรวจสอบ git history: `/follow-tool-git` หรือ `/check-git-logs`

### 4. Identify Contributing Factors

> Goal: หาปัจจัยทีมีส่วนให้เกิด incident ไม่ใช่แค่ root cause เดียว

1. ใช้ 5 Whys หรือ Fishbone diagram เพื่อหา contributing factors
2. แยกเป็น categories: people, process, tools, environment, communication
3. ระบุ factors ที control ได้ และไม่ control ได้
4. หลีกเลี่ยง blame โฟกัสที system และ process

### 5. Assess Impact

> Goal: วัดผลกระทบอย่างเป็นรูปธรรม

1. ระบุผลกระทบต่อ user: จำนวน, ระยะเวลา, severity
2. ระบุผลกระทบต่อทีม: time to detect, time to resolve, context switching
3. ระบุผลกระทบต่อ business: revenue, reputation, compliance
4. ทำ `/report` แสดง impact ตามมิติ

### 6. Extract Learnings

> Goal: สรุปสิ่งทีเรียนรู้ทีเป็นจริงและ actionable

1. ระบุสิ่งทีทำงานได้ดี (keep)
2. ระบุสิ่งทีควรหยุดหรือปรับ (stop)
3. ระบุสิ่งทีควรเริ่มทำ (start)
4. เชื่อม learnings กับ contributing factors โดยตรง
5. ถ้า learnings ไม่ชัดเจน → ทำ `/deep-thinking`

### 7. Define Action Items

> Goal: สร้าง action items ทีลดโอกาสเกิดซ้ำ

1. สร้าง action item เป็นลิสต์พร้อม owner, due date, success criteria
2. แบ่ง action items ตามระดับ: immediate (≤ 1 สัปดาห์), short-term (≤ 1 เดือน), long-term (≤ 3 เดือน)
3. ทุก action item ต้องเชื่อมกับ contributing factor ทีระบุ
4. ถ้าต้องแก้ code → ทำ `/update-tests` เพื่อสร้าง regression test
5. ถ้าต้องแก้ process → เขียน runbook หรือ checklist

### 8. Communicate And Follow Up

> Goal: สื่อสารผล retro และติดตาม action items

1. ทำ `/report` สรุป timeline, root cause, impact, learnings, action items
2. บันทึก retro ลงไฟล์บันทึกหรือ wiki ของ project
3. ติดตาม action items ตาม due date
4. ทบทวนใน retro ครั้งต่อไปว่า action items ทำงานจริงหรือไม

## Rules

### 1. Blameless Culture

- ไม่กล่าวโทษบุคคล โฟกัสที system, process, context
- ใช้ข้อมูลและ evidence ไม่ใช่ความรู้สึก
- สร้าง psychological safety สำหรับทีม

### 2. Process-Level Root Cause

- หา root cause ในระดับ process ไม่ใช่แค่ technical
- ถามว่า "ทำไม process ถึงปล่อยให้เกิดขึ้นได้"
- ระบุ contributing factors หลายมิติ

### 3. Actionable Outcome

- ทุก finding ต้องมี action item หรือ explicit decision ทีบันทึกไว้
- ไม่จบที "รู้แล้ว" ต้องมีการติดตาม
- action items ต้องมี owner และ due date

### 4. Time Bound

- ไม่ใช้เวลานานเกินไปกับการพูดคุย
- ถ้า issue ซับซ้อน → แบ่งเป็นหลาย retro session
- จบที action plan ไม่ใช่แค่ discussion

- ใช้ /follow-incident-triage ถ้าจำเป็น

## Expected Outcome

1. Timeline ของ incident ทีละเอียดและตรงตาม facts
2. Contributing factors และ root cause ระดับ process
3. Impact assessment ทีอธิบายได้
4. Action items ที actionable มี owner และ due date
5. Learnings ที reduce โอกาสเกิดซ้ำ
6. Retro document ทีสื่อสารให้ stakeholder เข้าใจ
