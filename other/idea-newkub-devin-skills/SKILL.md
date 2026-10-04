---
name: idea
description: สร้างไอเดียตาม user context วิเคราะห์ gaps และ opportunities
argument-hint: "[topic]"
related:
  - deep-review
  - reframe
  - report
  - suggest-next-action
  - implement-to-production
  - idea-grouping

---
## Goal

สร้างไอเดียตาม user context วิเคราะห์ gaps, needs และ opportunities แล้วรายงานเป็นตาราง

## Scope

ใช้เมื่อผู้ใช้บอกว่า "ขอ idea" หรือต้องการไอเดียสำหรับงานใดๆ ครอบคลุม features, UX/UI, refactor, และ improvements

## Execute

### Idea Skills

| Topic | Skill |
|-------|-------|
| ไอเดีย features ใหม่/ขยาย | `/idea-features` |
| ไอเดีย improve scope ใดๆ (quick wins, strategic, Extends/New/Remove) | `/idea-improve` |
| ตั้งชื่อไฟล์/directory สำหรับ idea | `/idea-naming` |
| ไอเดีย merge/consolidate สิ่งที่ซ้ำซ้อน | `/idea-merge` |
| ไอเดียจัดกลุ่ม items ตาม criteria/themes | `/idea-grouping` |
| ไอเดียจาก review findings/reports ที่มีอยู่ | `/idea-review` |
| ไอเดีย UX/UI improvements และ features | `/idea-uxui` |
| ไอเดีย refactor workspace ใน monorepo | `/idea-refactor-workspace` |
| ไอเดีย devin global skills ใหม่/ปรับปรุง | `/idea-new-devin-global-skills` |
| skill candidates จาก session ปัจจุบัน | `/idea-devin-global-skills-from-session` |
| แปลง CLI tools เป็น Devin skills | `/idea-convert-my-global-cli-to-skills` |

### 1. Analyze Context

> Goal: Analyze Context

วิเคราะห์ context จาก user request:

1. ระบุประเภทไอเดียที่ต้องการ (features, UX/UI, refactor, improvements)
2. ระบุ scope จาก user context (project, module, file, workflow)
3. ระบุ pain points และ gaps จาก context

### 2. Generate Ideas

> Goal: Generate Ideas

สร้างไอเดียตาม context:

1. ถ้าเป็นไอเดีย features ให้ทำ `/idea-features` สร้างไอเดีย features ใหม่และปรับปรุง features ที่มีอยู่
2. ถ้าเป็นไอเดีย UX/UI ให้ทำ `/deep-review` สร้างไอเดีย UX/UI improvements
3. สร้างไอเดียปรับปรุงจากเดิม (Extends)
4. สร้างไอเดียใหม่ที่ยังไม่มี (New)
5. ระบุ problem ที่แต่ละไอเดียจะ solve
6. จัดกลุ่มตาม topics

### 3. Prioritize And Report

> Goal: Prioritize And Report

จัดลำดับและรายงาน:

1. จัดลำดับตาม value vs effort
2. ระบุ quick wins และ strategic ideas
3. ทำ `/report table` แสดงผลเป็นตาราง: `No.`, `Idea`, `Type`, `Problem`, `Impact`, `Effort`
4. ถ้ามี action ต่อเนื่องจาก idea ก่อนหน้า → ใช้ `/follow-your-suggestion`
4. ใช้ Impact: 🔴 สูง → 🟡 ปานกลาง → 🟢 ต่ำ
5. ทำ `/suggest-next-action` เพื่อแนะนำ action ถัดไป

## Rules

### 1. Context-Based

- สร้างไอเดียตาม user context ไม่ใช่ generic
- ทุกไอเดียต้อง solve real problem
- ไม่สร้างไอเดียเพราะเท่ห์อย่างเดียว

### 2. Direct Execution

- ถ้าผู้ใช้บอกว่า "ทำ ... ให้" ให้ทำตาม `/implement-to-production` เลย
- ไม่ต้องทำตาม workflow ปกติถ้าผู้ใช้สั่งโดยตรง
- ใช้ /reframe ถ้าจำเป็น

## Expected Outcome

- ไอเดียตาม user context พร้อมจัดลำดับตาม Impact
- รายงานเป็นตารางตาม `/report`
- ทุกไอเดีย solve real problem