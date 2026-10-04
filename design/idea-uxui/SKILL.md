---
name: idea-uxui
description: สร้างไอเดีย UX/UI improvements และ features ใหม่ ตอบกลับในแชท ไม่สร้างไฟล์
argument-hint: "[topic-or-url]"
related:
  - idea
  - deep-review
  - follow-design-system
  - report-uxui
  - watch-browser
  - watch-browser-and-fix
  - deep-analyze
  - report
  - enhance-prompt
  - reframe

---

## Goal

สร้างไอเดีย UX/UI — improvements ต่อของเดิมและ features ใหม่ด้าน visual/interaction/usability — สรุปผลกลับในแชททันที โดยไม่สร้างไฟล์

## Scope

- วิเคราะห์ project context, routes/pages ที่มี และ prompt
- สร้างไอเดีย `Extends` (ปรับ UX/UI ของเดิม) และ `New` (UX/UI feature ใหม่) พร้อมระบุ impact/effort/risk
- ครอบคลุมมิติ: visual polish, layout/responsive, interaction/feedback, accessibility, design system consistency, empty/error/loading states
- ตอบกลับในแชทด้วย markdown tables และ bullets
- ไม่สร้าง report/plan ไฟล์ ไม่ implement
- ถ้าต้องการ visual review ของ routes จริงก่อนคิดไอเดีย → ใช้ `/deep-review` (domain `review-uxui`)
- ถ้าต้องการ implement → ส่งต่อ `/implement-features-to-mvp`

## Execute

### 1. Understand Context

> Goal: เข้าใจ topic และ UX/UI ปัจจุบัน

1. รับ `<topic-or-url>` จาก argument หรือ conversation context
2. ทำ `/deep-analyze` แบบ lightweight ถ้าต้องการ — ดู routes, components, design system ที่มี
3. ถ้ามี web รันอยู่และต้องการ evidence → ใช้ `/deep-review` หรือ `/report-uxui` ก่อนคิดไอเดีย
4. ถ้า topic ไม่ชัด → ใช้ `/suggest-next-action` ถาม user

### 2. Generate Ideas

> Goal: สร้างไอเดีย UX/UI

1. สร้างไอเดีย `Extends` (ปรับหน้า/component/flow ที่มี) และ `New` (pattern/feature UX ใหม่ เช่น command palette, skeleton states, onboarding, dark mode, shortcuts)
2. แต่ละกลุ่มไม่เกิน 10 ไอเดีย รวมไม่เกิน 20
3. แต่ละ idea ระบุ: idea, description, ux dimension (visual/interaction/a11y/responsive/consistency), impact, effort, risk, mvp score (1-10)
4. ลำดับเลขต่อเนื่อง: `Extends` เริ่ม 1, `New` ต่อจาก `Extends`

### 3. Rank And Format

> Goal: จัดลำดับและจัดรูปแบบตอบกลับ

1. จัดลำดับตาม MVP score สูง → ต่ำ
2. สร้าง markdown tables ด้วย `/report table`
3. ถ้ามี action ต่อเนื่องจาก idea ก่อนหน้า → ใช้ `/follow-your-suggestion`
4. สรุป top 3-5 ideas สั้นๆ ด้วย bullets
5. ระบุ phase: quick win, short-term, long-term

### 4. Reply In Chat

> Goal: ตอบกลับ user ทันที

1. แสดง summary 1-2 บรรทัด
2. แสดง tables ในแชท
3. บอกว่าเป็นไอเดียสำหรับพิจารณา
4. ถ้าต้องการ implement → แนะนำ `/implement-features-to-mvp`
5. ถ้าต้องการถามต่อ → ใช้ `/suggest-next-action`

## Rules

### 1. Chat Only

- ตอบกลับในแชทเท่านั้น — ไม่สร้างไฟล์ใน `.devin/temp/report/` หรือ `.devin/temp/plan/` ไม่สร้าง web app ถาวร ไม่เรียก `/ship-to-dev-branch`

### 2. Lightweight

- ไม่ต้อง `/learn` (web) ลึก ยกเว้น user บอก — ใช้เวลาไม่เกิน 5-10 นาที
- ไม่ต้องวิเคราะห์ codebase ละเอียด ถ้า context พอ

### 3. UX Dimension Coverage

- ทุก run ต้อง cover อย่างน้อย 3 มิติ: visual, interaction, a11y (ตาม `/deep-review` checklist)
- ไอเดียต้อง actionable และอิง design system ที่มี (`/follow-design-system`) — ไม่เสนอ pattern ที่ขัดกันโดยไม่มีเหตุผล

### 4. Suggest Deep Workflow

- ถ้า user บอก "ทำ" หรือ "do now" → แนะนำ `/implement-features-to-mvp`
- ถ้า user ต้องการ plan หรือ report → แนะนำ `/plan`
- เมื่อ idea ใดถูก implement → ต้องทำ `/run-test-all` เสมอ

### 5. Format

- ทุก table ต้องมีคอลัมน์ `No.` เป็นคอลัมน์แรก เรียง 1, 2, 3, ...
- ใช้ `/report` สำหรับ tables — ไม่ตอบยาวเกินความจำเป็น
- ใช้ `/enhance-prompt` ถ้า prompt คลุมเครือ
- ใช้ /reframe ถ้าจำเป็น


## Expected Outcome

- User ได้รับไอเดีย UX/UI ในแชททันที ครบหลายมิติ
- มี tables สรุป Extends, New, ลำดับความสำคัญพร้อม ux dimension
- ไม่มีไฟล์ถูกสร้าง ไม่มี implementation เกิดขึ้น
- มีคำแนะนำถัดไปชัดเจน

