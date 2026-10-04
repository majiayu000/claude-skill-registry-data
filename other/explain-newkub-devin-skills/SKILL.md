---
name: explain
description: อธิบาย concept, code, skill, term หรือกลไกการทำงานที่ user สงสัยอย่างชัดเจน
argument-hint: "<target> [level|mechanism]"
related:
  - summarize
  - dont-understand
  - write-how-to
  - learn
  - deep-research
  - scan-codebase
  - deep-trace
  - report-flow

---

## Goal

อธิบาย concept, code, skill, term ที่ user สงสัยอย่างสั้นชัดเจน พร้อมตัวอย่าง — และอธิบายกลไกการทำงานของระบบ, tool, library หรือ concept เป็นลำดับขั้นตอนเมื่อ user ถาม "ทำงานอย่างไร"

## Scope

ใช้เมื่อ user ถาม:
- "X คืออะไร", "explain X", "Y คือ" → concise explanation
- "X ทำงานอย่างไร", "how does X work", "mechanism ของ X" → mechanism explanation ลงลึกกลไกภายใน ไม่ใช่คู่มือทำตาม

## Execute

### 1. Identify Target, Level And Mode

> Goal: Identify Target, Level And Mode

1. อ่าน `<target>` จาก argument หรือ context
2. อ่าน `[level]` ถ้ามี เช่น `beginner`, `intermediate`, `advanced` — default `beginner`
3. เลือก mode: ถ้าคำถามเน้น "ทำงานอย่างไร"/mechanism → `mechanism` mode; ถ้าถาม "คืออะไร" → `concise` mode
4. ระบุประเภท target: `system`, `tool`, `library`, `code`, `concept`, `skill`
5. ถ้า target ไม่ชัด → ถาม user กลับสั้นๆ

### 2. Gather Context

> Goal: Gather Context

1. ถ้า target อยู่ใน project ปัจจุบัน → อ่านไฟล์ที่เกี่ยวข้อง; ถ้าเป็น mechanism mode → ทำ `/scan-codebase` หรือ `/deep-trace`
2. ถ้า target เป็น skill ใน repo → อ่าน `SKILL.md` ด้วย `/read` หรือ `/read-related`
3. ถ้า target เป็น tool/library ภายนอก → ใช้ `/learn` หรือ `/learn-from-web` ดู official docs
4. เก็บ snippets, source paths, docs และ examples ที่ช่วยอธิบาย

### 3. Provide Explanation

> Goal: อธิบายตาม mode ที่เลือก

#### Concise Mode

1. ให้ definition หรือ one-sentence summary ก่อน
2. อธิบาย why it matters หรือเมื่อไหร่ใช้
3. ให้ key points 3-5 ข้อ
4. ให้ example หรือ analogy ที่เหมาะสม
5. ถ้าเป็น code → อธิบาย key lines และผลลัพธ์

#### Mechanism Mode

1. ระบุ inputs และ outputs, key components/modules
2. วางแผน data flow หรือ execution flow รวม state changes, lifecycle, edge cases
3. เริ่มด้วย overview สั้นๆ แล้วแบ่งการทำงานเป็น 3-7 ขั้นตอน
4. แต่ละขั้นตอนระบุ what happens, why, และ how
5. ใช้ `/report-flow`, `/report` หรือ `/draw-tldraw` ถ้าช่วยให้เห็นภาพ

### 4. Suggest Next Steps

> Goal: Suggest Next Steps

1. ถ้าต้องการลงลึกกว่านี้ → แนะนำ `/deep-research`
2. ถ้าต้องการทำตาม → แนะนำ `/write-how-to`
3. ถ้าต้องการสรุป → แนะนำ `/summarize`
4. ถ้ายังไม่เข้าใจ → ส่งต่อ `/dont-understand`

## Rules

### 1. Concise

- คำตอบ 3-5 ประโยคหรือ bullets สำหรับ concise mode
- mechanism mode ยาวได้แต่ 1 step = 1 idea
- ถ้าต้องการลงลึกกว่า scope → ส่งต่อ skill อื่น

### 2. Focus On Mechanism

- mechanism mode เน้น "how" ไม่ใช่ "what" หรือ "how-to"
- อธิบาย cause และ effect ของแต่ละขั้นตอน
- หลีกเลี่ยงรายละเอียดที่ไม่จำเป็นจนกระทบความเข้าใจ

### 3. Beginner Friendly

- ลด jargon หรืออธิบายศัพท์เทคนิค
- ใช้ analogies ที่คุ้นเคย
- ให้ตัวอย่าง concrete ไม่ใช่ abstract

### 4. Accurate

- ไม่เดาข้อมูล — อ้างอิง official docs, code หรือ reliable sources
- ถ้าไม่แน่ใจ → บอกและแนะนำวิธี verify
- ใช้ backticks สำหรับ code, skill names, tools, ชื่อ components

- ใช้ /run-program ถ้าจำเป็น

## Expected Outcome

- คำอธิบาย target ที่ชัดเจนตาม mode — concise เข้าใจใน 3-5 bullets; mechanism เข้าใจ "why" และ "how" เป็นขั้นตอน
- มี example หรือ analogy ที่ช่วยให้เข้าใจ
- ระบุแหล่งอ้างอิงหรือ next skill ถ้าต้องการลงลึก
