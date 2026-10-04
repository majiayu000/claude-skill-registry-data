---
name: deep-plan
description: Canonical analyze + plan — วิเคราะห์ลึกแล้ววางแผน implementation-ready ในคำสั่งเดียว
argument-hint: "[scope]"
related:
  - plan
  - deep-analyze
  - deep-thinking
  - deep-research
  - refactor
  - implement-to-production
  - deep-validate
  - prioritize
  - use-astgrep
  - search-npm-libraries
  - deep-review
  - alternative
  - report
  - ask-me
  - suggest-next-action
---

## Goal

วิเคราะห์ปัญหา/context อย่างลึกซึ้งแล้ววางแผน implementation-ready ในขั้นตอนเดียว — canonical skill สำหรับทุก analyze+plan — ผลลัพธ์คือ plan ที่ระบุ deps, ไฟล์, APIs, risks และ acceptance ครบจน implement ได้โดยไม่ถามเพิ่ม

## Scope

ใช้กับงานที่ต้องเข้าใจ codebase ก่อนวางแผน — refactors, features, migrations, extractions — ครอบคลุม analysis findings, dependency decisions, file architecture, task graph, risks และ test strategy

- Output: ตอบ plan ในแชทเท่านั้น — ห้ามสร้างไฟล์ใดๆ (รวมถึง `.devin/tasks/`, `.devin/temp/plan/`)
- Boundary: `/plan` เป็น alias ของ skill นี้ (canonical เดิม `deep-analyze-and-plan` merge แล้ว); persist plan จริงๆ user ต้องสั่ง `/create-plan-in-dot-devin` เอง
- อ่านก่อนทำงานเสมอ: `refactor/SKILL.md` (patterns + safety) และ `implement-to-production/SKILL.md` (production checklist) — plan ต้องออกแบบให้ผ่านทั้งสองมาตรฐาน

## Execute

### 1. Deep Thinking

> Goal: เฟรมปัญหาก่อนสำรวจ

1. ทำ `/deep-thinking` — กำหนด objectives, sub-problems, assumptions, success criteria
2. ถ้า scope คลุมเครือ → `/ask-me` ก่อนสำรวจ

### 2. Deep Analyze

> Goal: มี findings จริงจาก code ก่อนเขียนแผน

1. ทำ `/scan-codebase` — structure, patterns, conventions ของ scope
2. ใช้ `Grep`/`ast-grep` (ตาม `/use-astgrep`) หา symbols, call sites, consumers, duplications
3. อ่านไฟล์เป้าหมายจริง — ห้ามเดา APIs/paths
4. scope ใหญ่ → dispatch `review-*` เฉพาะ domains ที่เกี่ยว (ดู `deep-analyze` domain table)
5. สรุป findings พร้อม evidence (file:line)

### 3. Deep Research

> Goal: decisions มี external validation เมื่อจำเป็น

1. ทำ `/deep-research` เมื่อต้องเลือก deps ใหม่, pattern ใหม่, หรือ API ที่ไม่แน่ใจ — ทำ parallel กับ Step 2 ได้ (independent)
2. official docs เป็นแหล่งหลัก; cross-check ≥2 sources สำหรับ high-risk choices
3. ทำ `/alternative` สำหรับทุก dep ใหม่ — บันทึกตัวเลือกที่ปฏิเสธพร้อมเหตุผล; ใช้ `/search-npm-libraries` หา candidates (TypeScript+ESM)
4. เช็ค compatibility กับ versions ใน manifest + publish age (≥7 วัน)

### 4. Write Plan

> Goal: ระบุ deps + ไฟล์ + API + acceptance + risk ครบทุก task

ทุก task ต้องระบุ:

1. `File`: path เต็ม — action: create / edit / delete / move
2. `What`: public API signatures, exported types, data structures, config keys
3. `How`: pattern/approach — library, convention ใน codebase, code sketch ถ้าจำเป็น
4. `Deps`: existing (`name@version`) หรือ new (`name@version` + เหตุผล + อายุ publish)
5. `Why`: เหตุผล + alternatives ที่ปฏิเสธ
6. `Acceptance`: เงื่อนไขผ่านที่วัดได้ — test case, command, expected output
7. `Risk`: impact ถ้าผิด + rollback/mitigation

Reuse/refactor: map duplication → extraction target พร้อม evidence count; migration order = shared unit ก่อน → consumers ทีละตัว → delete dead code

Architecture: file tree + pattern table (Pattern / Description / Naming / Import), module boundaries, data contracts, error handling

Test strategy: unit/integration/e2e coverage + fixtures + regression cases

### 5. Order And Validate

> Goal: fail fast + แผนผ่าน playbooks ทั้งสอง

1. ทำ `/prioritize` — Foundation → Dependencies → High impact → Critical path → High risk
2. จัด phases: Foundation → Core → Polish → Test + task graph (parallel/block/milestones)
3. ทำ `/deep-validate` — ห้าม placeholder/TBD/decision ค้าง
4. walkthrough แผนเทียบ checklist จาก `refactor` + `implement-to-production`
5. หลายทางเลือกเสี่ยงสูง → สรุป options/risks แล้ว `/ask-me`

### 6. Report

> Goal: plan report ครบทุกมิติ — ตอบในแชทก่อนลงมือ

ทำ `/report` — ทุก table ขึ้นต้นด้วย `No.` column:

1. `## Summary` — 1-2 บรรทัด: ทำอะไร ทำไม
2. `## Analysis Findings` — `No. | Finding | Evidence | Impact`
3. `## Dependencies` — `No. | Package | Type | Version | Used By | Why | Risk` ("none" ถ้าไม่มี dep ใหม่)
4. `## File Changes` — `No. | File | Action | What | How | Acceptance | Risk`
5. `## File Structure` — tree diagram เมื่อมีการสร้าง/ย้ายไฟล์
6. `## TODOs` — numbered tasks เรียงตาม phase พร้อม effort คร่าวๆ
7. `## Task Graph` — parallel groups, blockers, milestones
8. `## Risks` — `No. | Risk | Probability | Impact | Mitigation | Rollback`
9. `## Test Strategy` — coverage target, test files, regression cases
10. `## Assumptions And Unknowns` — สิ่งที่ assume + วิธี verify
11. `## Next Action` — ขั้นตอนแรกที่ชัดเจน + `/suggest-next-action`

## Rules

### 1. No Ambiguity

- ห้ามเขียน task ที่ตีความได้หลายแบบ — ทุก task ระบุ file + what + how + deps + acceptance
- ห้าม placeholder/TBD — ตัดสินใจไม่ได้ → `/deep-research` หรือ `/ask-me` ก่อน
- ทุก finding ต้อง map เข้า task หรือระบุเหตุผลที่ตัดออก

### 2. Evidence Based

- ห้ามเดา APIs, file paths, library behavior — ตรวจจาก codebase/docs จริง
- ทุก dep ใหม่ต้องเช็ค version ที่มีอยู่ + publish age (≥7 วัน) + justification
- analysis findings ต้องมี file:line evidence

### 3. Reuse First

- ค้น existing implementations/hooks/utils ก่อนเสนอสร้างใหม่เสมอ
- เสนอ extraction เป็น shared hook/util เมื่อ pattern ซ้ำ ≥3 จุด

### 4. Chat Only

- แผนอยู่ในแชทเท่านั้น — ห้ามสร้างไฟล์ plan/tasks ใดๆ
- เขียนละเอียดระดับ subagent เอาไปทำได้โดยไม่ถามเพิ่ม

## Expected Outcome

- Analysis findings พร้อม evidence → implementation-ready plan
- Dependency table ครบ (existing + new + justification)
- File changes ครบ (create/edit/delete + what + how + acceptance)
- Task graph + phases + risks + mitigation + rollback
- Test strategy + assumptions + next action ชัดเจน
- ผ่าน `/deep-validate` — ไม่มี placeholder
