---
name: prioritize
description: จัดลำดับความสำคัญของ tasks และ improvements ตาม impact และ effort
argument-hint: "[scope]"
related:
  - follow-best-practice
  - suggest-next-action
  - resolve-errors
  - deep-thinking
---

## Goal

จัดลำดับความสำคัญของ tasks และ improvements ตาม impact และ effort เพื่อให้ทำงานได้อย่างมีประสิทธิภาพ

## Scope

ใช้สำหรับจัดลำดับความสำคัญของ tasks ทั้งใน development, maintenance, และ improvement

## Execute

### 1. Assess Impact

> Goal: Assess Impact

ประเมินผลกระทบของ task

1. ประเมิน `business impact`: revenue, user experience, compliance
2. ประเมิน `technical impact`: performance, security, maintainability
3. ประเมิน `user impact`: จำนวนผู้ใช้ที่ได้รับผลกระทบ
4. ประเมิน `urgency`: deadline, dependencies, blocking issues

### 2. Estimate Effort

> Goal: Estimate Effort

ประเมินความยากและเวลาที่ต้องใช้

1. ประเมิน `complexity`: ความซับซ้อนของงาน
2. ประเมิน `time`: เวลาที่คาดว่าจะใช้
3. ประเมิน `resources`: ทีม, skills, tools ที่ต้องการ
4. ประเมิน `risk`: ความเสี่ยงของการทำงาน

### 3. Calculate Priority

> Goal: Calculate Priority

คำนวณ priority จาก impact และ effort

1. ทำ `/deep-thinking` เพื่อทบทวนมุมมองหลายด้านก่อนตัดสินใจ priority

| Impact | Effort | Priority | Rationale |
|--------|--------|----------|-----------|
| High   | Low    | P0       | Quick win, high value |
| High   | Medium | P1       | High value, moderate effort |
| High   | High   | P2       | High value, needs planning |
| Medium | Low    | P1       | Quick win, moderate value |
| Medium | Medium | P2       | Moderate value and effort |
| Medium | High   | P3       | Low priority, high effort |
| Low    | Low    | P2       | Quick win, low value |
| Low    | Medium | P3       | Low priority |
| Low    | High   | P4       | Defer or skip |

### 4. Consider Dependencies

> Goal: Consider Dependencies

พิจารณา dependencies ระหว่าง tasks

1. ระบุ tasks ที่ block tasks อื่น
2. ระบุ tasks ที่ blocked โดย tasks อื่น
3. ปรับ priority ตาม dependencies
4. จัดลำดับ tasks ที่เป็น prerequisites ก่อน

### 5. Validate With Stakeholders

> Goal: Validate With Stakeholders

ตรวจสอบ priority กับ stakeholders

1. แสดง priority list พร้อม rationale
2. ขอ feedback จาก stakeholders
3. ปรับ priority ตาม feedback
4. ยืนยัน priority สุดท้าย

## Rules

### Impact Assessment

ประเมิน impact อย่างครบถ้วน

- ประเมิน `business impact` ก่อนเสมอ
- ประเมิน `technical impact` สำหรับ long-term health
- ประเมิน `user impact` สำหรับ immediate value
- ประเมิน `urgency` สำหรับ time-sensitive tasks
- ใช้ quantitative metrics เมื่อเป็นไปได้

### Effort Estimation

ประเมิน effort อย่าง realistic

- ประเมิน `complexity` อย่างถูกต้อง
- ประเมิน `time` รวม buffer
- ประเมิน `resources` ที่จำเป็น
- ประเมิน `risk` ของการทำงาน
- ใช้ historical data เมื่อเป็นไปได้

### Priority Matrix

ใช้ matrix ในการกำหนด priority

- P0: High impact + Low effort (quick wins)
- P1: High impact + Medium effort หรือ Medium impact + Low effort
- P2: High impact + High effort หรือ Medium impact + Medium/Low effort
- P3: Medium impact + High effort หรือ Low impact + Medium effort
- P4: Low impact + High effort (defer or skip)

### Dependencies

พิจารณา dependencies อย่างเหมาะสม

- Tasks ที่ block อื่นต้องทำก่อน
- Tasks ที่ blocked ต้องรอ prerequisites
- ปรับ priority ตาม dependency chain
- พิจารณา parallel execution เมื่อเป็นไปได้

### Stakeholder Validation

ตรวจสอบ priority กับ stakeholders

- แสดง rationale อย่างชัดเจน
- ขอ feedback จากทุก stakeholders
- ปรับ priority ตาม business needs
- ยืนยัน priority สุดท้ายก่อนเริ่มทำ

- ใช้ /follow-best-practice ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น
- ใช้ /resolve-errors ถ้าจำเป็น

## Expected Outcome

- Tasks ถูกจัดลำดับความสำคัญอย่างถูกต้อง
- Priority สอดคล้องกับ business goals
- Resources ถูกจัดสรรอย่างมีประสิทธิภาพ
- Dependencies ถูกจัดการอย่างเหมาะสม
- Stakeholders เห็นด้วยกับ priority decisions