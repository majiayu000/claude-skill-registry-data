---
name: idea-merge
description: สร้างไอเดีย merge หรือ consolidate สิ่งทีซ้ำซ้อนตาม context
argument-hint: "[target]"
related:
  - scan-codebase
  - follow-single-of-source
  - review-devin-global-harness
  - dont-over-engineer
  - report
  - suggest-next-action
  - merge
  - rename
---

## Goal

สร้างไอเดียการ merge หรือ consolidate สิ่งทีซ้ำซ้อนให้เป็นหน่วยเดียว โดย context-aware และ continuous numbering

## Scope

ใช้เมื่อต้องการวิเคราะห์ว่าควร merge อะไรเข้าด้วยกัน:
- files, skills, folders, workflows, configs
- code modules, libraries, services
- หรือ repository artifacts ใด ๆ ทีซ้ำซ้อน

ไม่ลงมือ execute merge — ส่งต่อ `/merge` ต่อเมื่อได้ไอเดียและ user confirm

## Execute

### 1. Analyze Context

> Goal: รวบรวม context ก่อนสร้างไอเดีย merge

1. ระบุ target จาก argument หรือ context ปัจจุบัน
2. ถ้า target เป็น repo/โฟลเดอร → ทำ `/scan-codebase`
3. ถ้า target เป็น skills → ทำ `/review-devin-global-harness` หรือ `/review-devin-global-harness`
4. อ่านไฟล์/artifacts ของแต่ละ candidate เพื่อเปรียบเทียบ Goal, Scope, Execute
5. ตรวจสอบ line counts, references, และ section overlap

### 2. Identify Merge Candidates

> Goal: ระบุคู่หรือกลุ่มทีควร merge

1. ระบุสิ่งทีมี description, purpose, หรือ behavior ทับซ้อน
2. ระบุสิ่งทีอยู่ในกลุ่มเดียวกันและถูกเรียกใช้คู่กันบ่อย
3. ระบุสิ่งทีอ้างถึงกันอย่างหนาแน่น (references, imports, calls)
4. ระบุสิ่งทีมี line count น้อยและเป็นส่วนย่อยของสิ่งทีใหญ่กว่า
5. ระบุ spelling inconsistencies หรือชื่อทีควร rename พร้อม merge

### 3. Evaluate Merge Options

> Goal: ประเมินวิธีทีเหมาะสม

1. ประเมินแต่ละ opportunity ตามเงื่อนไข:
   - `merge` — ถ้าซ้ำซ้อนหรือ changes together
   - `rename` — ถ้าชื่อผิดหรือไม่สื่อความหมาย
   - `keep` — ถ้า cohesion สูงและไม่มี benefit ชัดเจน
2. ทำ `/dont-over-engineer` เพื่อกรองไอเดียทีซับซ้อนเกินไป
3. พิจารณา target (ตัวรับ) และ source(s) (ตัวทีจะลบ/ยุบ)
4. ตรวจสอบว่า merged output จะไม่เกิน 250 บรรทัด/จำกัดทีกำหนด

### 4. Plan Merge Strategy

> Goal: วางแผนการ merge สำหรับแต่ละคู่/กลุ่ม

1. ระบุ target และ source(s) ชัดเจน
2. ระบุ sections, files, หรือ config ทีจะย้าย
3. ระบุ references, imports, links ทีต้องอัปเดต
4. วางแผนการลบ source หลัง merge เสร็จ
5. ระบุลำดับการ merge ถ้ามีหลายคู่

### 5. Generate Ideas

> Goal: สร้างไอเดีย merge แบบ actionable

1. สร้างไอเดียสำหรับแต่ละ opportunity
2. ใช้ continuous numbering ต่อจากไอเดียเดิมถ้ามี
3. ระบุ scope: `quick win`, `short-term`, `long-term`
4. ระบุ impact, effort และ action: `merge`, `rename`, `keep`
5. ระบุ target, source(s), และสิ่งทีจะย้าย

### 6. Report

> Goal: รายงานไอเดียและ next action

1. ทำ `/report table`
2. คอลัมน์: No., Source(s), Target, Issue, Idea, Action, Scope, Impact, Effort
3. จัดลำดับตาม impact/effort ratio
4. ถ้ามี action ต่อเนื่องจาก idea ก่อนหน้า → ใช้ `/follow-your-suggestion`
5. ทำ `/suggest-next-action`
6. ถ้าพร้อม execute → แนะนำให้ทำ `/merge` หรือ `/rename`

## Rules

### 1. Context-Aware

- ไม่จำกัดเฉพาะ files หรือ skills — รองรับทุก artifact ตาม context
- ระบุประเภทของ target และ source ในแต่ละไอเดีย
- ใช้ `/ask-me` ถ้า target ไม่ชัด
- ใช้ `/follow-single-of-source` ถ้าจำเป็น

### 2. Evidence-Based

- ทุกไอเดียต้องมาจาก analysis จริง
- ระบุ file path, skill name, section overlap, หรือ references ทีเกี่ยวข้อง
- อ้างอิง line counts, duplicates, หรือ description overlap

### 3. Actionable And Numbered

- ใช้ continuous numbering
- ระบุ action ชัดเจน: `merge`, `rename`, `keep`
- ระบุ target, source(s), และเนื้อหาทีจะย้าย

### 4. No Over-Engineering

- ไม่เสนอ merge ทีไม่มี benefit ชัดเจน
- ไม่ merge เพื่อลดจำนวนอย่างเดียว
- ทำ `/dont-over-engineer`

### 5. Line Count Safety

- ตรวจสอบว่า merged output จะไม่เกิน 250 บรรทัด
- ถ้าเกิน → แนะนำ trim หรือ split ก่อน merge
- ระบุ estimated line count หลัง merge

## Expected Outcome

- รายการไอเดีย merge แบบ continuous numbering
- ทุกไอเดียมี source(s), target, action, scope, impact, effort
- ตาราง `/report` พร้อม next action
- ไอเดียพร้อม execute ด้วย `/merge`

