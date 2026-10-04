---
name: reframe
description: ประเมินว่า content/plan เขียนจากมุมที่เหมาะสมหรือยัง หรือควร reframe เป็นมุมอื่น
argument-hint: "[target]"
related:
  - deep-thinking
  - deep-validate
  - deep-research
  - rethink
  - idea
  - ask-me
  - report
  - suggest-next-action
---

## Goal

ตรวจว่า content, plan, idea หรือ skill ที่กำลังเขียนอยู่ใน `frame ที่เหมาะสม` — audience, verb/lifecycle prefix, level of abstraction, mental model — หรือควร reframe เป็นมุมอื่นก่อน commit

## Scope

ใช้เมื่อเขียนหรือออกแบบ content ใหม่ (skill, doc, plan, prompt, idea) และต้องการ challenge framing ก่อนส่งมอบ — ไม่ใช่ correctness check (ใช้ `/check-reference`) หรือ freshness check (ใช้ `/deep-review`)

## Execute

### 1. Identify Current Frame

> Goal: เข้าใจมุมที่ content เขียนอยู่ตอนนี้

1. ระบุ target (skill, doc, plan, idea) และอ่านเนื้อหา
2. ระบุ frame ปัจจุบัน:
   - `Audience`: เขียนให้ใคร (user, model, future-self, reviewer)
   - `Lens`: เขียนจากมุมไหน (tool-centric, task-centric, outcome-centric, lifecycle)
   - `Level`: abstraction ระดับไหน (how-to steps, concepts, decision guide)
   - `Boundary`: scope ครอบคลุมอะไร / ตัดอะไรทิ้ง
3. บันทึก assumptions ที่ frame นั้นพึ่งพา

### 2. Generate Alternative Frames

> Goal: คิดมุมอื่นที่เป็นไปได้

1. ทำ `/deep-thinking` เพื่อ generate frames ทางเลือก เช่น:
   - tool-centric → task-centric (เปลี่ยนจาก "ใช้ X ยังไง" เป็น "ทำ Y ด้วย X")
   - single-skill → dispatcher + domain skills
   - imperative steps → decision table / checklist
   - feature lens → user-outcome lens
   - happy path → failure-first framing
2. สำหรับแต่ละ frame: ระบุข้อดี, ข้อเสีย, ผู้ใช้ที่ได้ประโยชน์, งานที่ต้อง rework

### 3. Research Precedents

> Goal: เทียบกับ conventions และ real-world framing

1. ทำ `/deep-research` กับ official docs/community ของ domain — เขา frame เรื่องนี้ยังไง
2. เทียบกับ skills/docs อื่นใน repo ที่ domain ใกล้กัน — frame consistency
3. ถ้าเป็น skill → เทียบกับ prefix conventions (`check-*`, `run-*`, `follow-*`, `idea-*`) ว่า frame ตรง lifecycle จริงไหม

### 4. Evaluate And Decide

> Goal: เลือก frame ที่เหมาะสมสุด

1. ทำ `/deep-validate` เพื่อประเมินแต่ละ frame กับ criteria:
   - ตรง intent ของ user จริงไหม
   - audience เข้าใจ/action ได้เร็วกว่าไหม
   - maintainable และ consistent กับระบบไหม
   - rework cost คุ้มไหม
2. ตัดสินใจ: `keep` (frame ปัจจุบันเหมาะแล้ว), `reframe` (เปลี่ยนมุม), หรือ `split` (แยก content เป็น 2+ frames)
3. ถ้า decision เสี่ยง/ambiguous → ทำ `/ask-me` ให้ user เลือก

### 5. Report

> Goal: สรุปผลพร้อมเหตุผล

1. ทำ `/report` ตาราง: No, Frame, Lens, Pros, Cons, Verdict
2. ถ้า verdict = reframe/split → ระบุ frame ใหม่ + draft outline ที่ควรเป็น + skills ที่ต้องแก้ (`/rewrite`, `/refactor`, `/update-*`)
3. ถ้า verdict = keep → ระบุเหตุผลสั้นๆ ว่า frame เดิมดีสุด
4. ทำ `/suggest-next-action`

## Rules

### 1. Reframe Discipline

- challenge frame เสมอ — ห้าม default "keep" ถ้าไม่ได้ generate alternatives จริง
- reframe เฉพาะเมื่อผลลัพธ์เปลี่ยนอย่างมีนัยสำคัญ — ไม่ reframe เพื่อความสวย
- ถ้า content มีหลาย audiences → พิจารณา split ก่อน reframe

### 2. Evidence

- เลือก frame จาก evidence (usage patterns, precedents, audience need) ไม่ใช่ taste
- ระบุ assumptions ที่แต่ละ frame พึ่งพา — ถ้า assumption เปลี่ยน verdict อาจเปลี่ยน

### 3. Boundaries

- reframe ประเมินและแนะนำ — ไม่ rewrite เอง (rewrite ผ่าน `/rewrite` หรือ `update-*`)
- ใช้ก่อน finalize content ใหม่ หรือเมื่อสงสัยว่าเอกสาร "เขียนมุมผิด"
- ไม่ใช้กับ trivial content — cost ของ analysis ต้องน้อยกว่าความเสี่ยงของ frame ผิด

- ใช้ /deep-thinking ถ้าจำเป็น
- ใช้ /deep-validate ถ้าจำเป็น
- ใช้ /deep-research ถ้าจำเป็น
- ใช้ /rethink ถ้าจำเป็น
- ใช้ /suggest-next-action ถ้าจำเป็น

## Expected Outcome

- รู้ว่า frame ปัจจุบันเหมาะสมหรือควรเปลี่ยน พร้อม alternatives ที่เทียบกันแล้ว
- Verdict ชัดเจน: keep / reframe / split พร้อมเหตุผลและ rework scope
- ถ้า reframe → มี outline ของมุมใหม่พร้อมลงมือผ่าน skill ที่เหมาะ
