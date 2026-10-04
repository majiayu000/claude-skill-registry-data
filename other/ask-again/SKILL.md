---
name: ask-again
description: ถามใหม่เมื่อผู้ใช้ไม่เข้าใจคำถาม โดย rephrase สั้นกระชับและให้ตัวอย่าง
argument-hint: "[scope]"
related:
  - ask-me
  - dont-ask-me
  - follow-my-persona
  - continue
  - ask-project-requirement

---

## Goal

ถามผู้ใช้ใหม่เมื่อคำถามเดิมไม่เข้าใจ โดย rephrase ให้สั้น ลด jargon เพิ่ม context ตัวอย่าง หรือแบ่งเป็นข้อเล็ก

## Scope

ใช้เมื่อผู้ใช้ตอบ "ไม่เข้าใจ", "ถามใหม่", "ask again", "repeat", "explain" หรือเลือก `Suggest another` ครั้งที่ 2 ใน `/ask-me`

ไม่ใช้เก็บ requirements (ใช้ `/ask-project-requirement`) หรือสัมภาษณ์ preferences (ใช้ `/follow-my-persona`)

## Execute

### 1. Detect Confusion

> Goal: รู้ว่าผู้ใช้ไม่เข้าใจคำถาม

1. จับสัญญาณ confusion: "ไม่เข้าใจ", "ถามใหม่", "ask again", "repeat", "explain", "confused", "ไม่รู้เรื่อง"
2. ดู context คำถามล่าสุดที่ถามไป
3. ถ้าไม่มีคำถามก่อนหน้า → หยุดและ report ว่าไม่มีคำถามให้ถามใหม่

### 2. Analyze Why Unclear

> Goal: หาสาเหตุที่คำถามไม่เข้าใจ

1. ประเมินว่าคำถามยาว/ซับซ้อนเกินไปหรือไม่
2. ประเมินว่ามี jargon หรือ terminology ที่ผู้ใช้อาจไม่รู้หรือไม่
3. ประเมินว่าขาด context หรือ background หรือไม่
4. ประเมินว่าตัวเลือกมากเกินไป หรือ labels ไม่ชัดเจนหรือไม่
5. เลือกกลยุทธ์ rephrase ที่เหมาะสม

### 3. Rephrase

> Goal: ทำให้คำถามเข้าใจง่ายขึ้น

1. ลดความยาวของ `question` เหลือประโยคสั้นๆ 1-2 ประโยค
2. ลบหรือแทนที่ jargon ด้วยคำทั่วไป
3. เพิ่ม context สั้นๆ ที่บอกว่าทำไมถาม เช่น "เพื่อเลือก runtime ที่เหมาะกับโปรเจกต์"
4. ให้ตัวอย่างหรือเปรียบเทียบสั้นๆ ใน `description`
5. ถ้าตัวเลือกมากเกินไป ให้ลดเหลือ 2-3 ตัวเลือกที่สำคัญที่สุด
6. ถ้าซับซ้อน ให้แบ่งเป็น 2 คำถามย่อยแทนการถามทีเดียว

### 4. Ask With `ask_user_question`

> Goal: ส่งคำถามใหม่ให้ผู้ใช้

1. ใช้ `ask_user_question` tool เท่านั้น
2. เก็บ `options` เดิมไว้โดยมากที่สุด แต่ reword `label` และ `description`
3. รักษาตัวเลือกที่แนะนำ (recommended) ไว้
4. ตั้ง `multi_select` ให้ตรงกับคำถามเดิม
5. บอกผู้ใช้ว่านี่คือการถามใหม่ เช่น "ขอถามใหม่อีกครั้งนะครับ — ..."

### 5. Handle Re-Ask Loop

> Goal: ไม่ถามวนเกิน 2 รอบ

1. นับจำนวนครั้งที่ re-ask แล้ว
2. ถ้าครั้งที่ 2 → ถามแบบ open-ended หรือลดเหลือ 2 ตัวเลือกชัดเจนที่สุด
3. ถ้าครั้งที่ 3 ขึ้นไป → ใช้ `/dont-ask-me` หรือ default โดยไม่ถามต่อ
4. ถ้าผู้ใช้บอกว่าไม่ต้องการถามอีก → ใช้ `/dont-ask-me`

### 6. Process Response

> Goal: ประมวลผลคำตอบ

1. คู่คำถามกับคำตอบจาก mapping ที่ `ask_user_question` return
2. ถ้าผู้ใช้ตอบเอง (custom_text) ให้วิเคราะห์และปรับแผน
3. ถ้าผู้ใช้ยังไม่เข้าใจอีก → กลับไป Step 2 โดยนับ re-ask count
4. ถ้าผู้ใช้ตอบได้แล้ว → ดำเนินการต่อตามคำตอบ

## Rules

### 1. No Exact Repeat

- ห้ามถามเหมือนเดิมเป๊ะ ต้อง rephrase หรือเพิ่ม context
- ต้องเปลี่ยนแปลง `question`, `label`, หรือ `description` อย่างน้อย 1 จุด

### 2. Preserve Intent

- รักษาโจทย์/คำตอบที่ต้องการไว้
- ไม่เปลี่ยน `single` เป็น `multiselect` โดยไม่จำเป็น
- ไม่เพิ่มตัวเลือกที่ไม่เกี่ยวข้อง

### 3. Loop Limit

- ถามใหม่ได้สูงสุด 2 ครั้ง
- ครั้งที่ 3 ให้ใช้ `/dont-ask-me` หรือ open-ended
- ถ้าผู้ใช้บอกให้หยุดถาม → หยุดทันที

### 4. Tool Discipline

- ใช้ `ask_user_question` tool เท่านั้น
- ไม่ใช้ chat text ทั่วไปถาม

### 5. Escalation

- ถ้าผู้ใช้ไม่เข้าใจเพราะข้อมูลไม่พอ → ใช้ `/ask-project-requirement`
- ถ้าผู้ใช้ต้องการอธิบายความชอบ → ใช้ `/follow-my-persona`
- ถ้าผู้ใช้บอกไม่ต้องการถาม → ใช้ `/dont-ask-me`

- ใช้ /continue ถ้าจำเป็น
## Expected Outcome

- ผู้ใช้เข้าใจคำถามใหม่และตอบได้
- ลดการถามวนซ้ำ
- รักษา flow ของ conversation
- ถ้ายังไม่เข้าใจหลัง 2 รอบ ให้มีทางออกชัดเจน (default / open-ended / ส่งต่อ skill อื่น)
