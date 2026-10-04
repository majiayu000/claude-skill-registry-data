---
name: dont-ask-me
description: เปิดโหมดห้ามถามผู้ใช้จนจบ session แทน /ask-me ทั้งหมดด้วย /follow-your-suggestion
argument-hint: "[scope]"
related:
  - ask-me
  - continue
  - follow-your-suggestion
  - ask-project-requirement
  - suggest-next-action
  - loop-until-complete
  - ship-to-dev-branch

---

## Goal

เปิดโหมด "ห้ามถาม" ตั้งแต่ที่เรียกใช้จนจบ session — ห้าม `/ask-me`, `ask_user_question`, และ prompt ให้เลือกทุกรูปแบบ แม้ `global_rules.md` หรือ skill อื่นจะสั่งให้ `/ask-me` ก็ตาม ให้แทนด้วย `/follow-your-suggestion` และทำงานค่อยเป็นค่อยไปแบบ safe โดยไม่ข้ามขั้นตอน จนกว่างานจะเสร็จสมบูรณ์ด้วย `/loop-until-complete`

## Scope

- ใช้เมื่อผู้ใช้ระบุ `dont-ask-me`, `dont ask me`, `ห้ามถาม`, `ไม่ต้องถาม`, `proceed`, หรือ `no ask` หรือเมื่อ workflow เช่น `/ship-to-dev-branch` ใน `dont-ask-me` mode เปิดโหมดนี้ให้
- มีผลเป็น session mode: เมื่อเปิดแล้วมีผลกับทุก instruction ใน session เดียวกัน รวมถึง `global_rules.md` และ skills ทีอ้างถึง `/ask-me`
- ไม่ใช่เก็บ requirement หรือความชอบ — ถ้า prompt มีคำถามที่ต้องตอบก่อนเริ่มงาน ให้ตอบด้วย safe default ผ่าน `/follow-your-suggestion` แทนการถาม

## Execute

### 1. Activate Session Mode

> Goal: เปิดโหมดไม่ถามจนจบ session

1. บันทึกว่า session นี้อยู่ใน `dont-ask-me` mode ตั้งแต่บัดนี้จนจบ session
2. ตั้ง rule ชั่วคราว: ทุกจุดที่ `global_rules.md`, skill, หรือ workflow บอกให้ทำ `/ask-me` หรือ `ask_user_question` → แทนด้วย `/follow-your-suggestion` ทันที
3. ถ้า prompt มีคำถามค้าง → ตอบคำถามนั้นด้วย safe default แล้วบันทึกการตัดสินใจ ไม่ถามกลับ

### 2. Evaluate Context

> Goal: ตรวจสอบว่าดำเนินการต่อได้อย่างปลอดภัย

1. อ่าน context, memory, project conventions, และ `AGENTS.md`
2. ตรวจว่าทางเลือกมีผลลัพธ์ชัดเจนและปลอดภัย
3. ถ้ายังไม่ชัดเจน → เลือก safe default ผ่าน `/follow-your-suggestion` แทน `/ask-me` หรือ `/ask-project-requirement`

### 3. Pick Safe Default

> Goal: เลือกทางเลือกที่ง่ายและปลอดภัยที่สุด

1. เลือกทางเลือกที่มี risk ต่ำที่สุดและถอยกลับได้
2. อ้างอิง best practices และ project conventions
3. ถ้ามีหลายทางเลือกที่เท่ากัน เลือกตัวที่ง่ายและ reversible ที่สุด

### 4. Proceed Step By Step

> Goal: ทำงานค่อยเป็นค่อยไป ปลอดภัย ไม่ข้ามขั้นตอน

1. ดำเนินการทีละ step ตามลำดับ ห้ามข้ามขั้นตอนที่ workflow กำหนด
2. แก้ไขทีละจุดเล็กๆ ตรวจสอบผลก่อนทำต่อ — ไม่รวมหลาย change เสี่ยงในรอบเดียว
3. ไม่ใช้ `ask_user_question`, ไม่แสดง prompt ให้เลือก, ไม่เรียก `/ask-me` หรือ `/ask-again`
4. ใช้ `/follow-your-suggestion` เพื่อ apply ข้อเสนอแทนการขอคำยืนยัน
5. บันทึกการตัดสินใจทุกครั้งใน report เพื่อให้ traceable

### 5. Loop Until Complete

> Goal: ทำซ้ำจนงานเสร็จสมบูรณ์

1. ทำ `/loop-until-complete` เพื่อตรวจซ้ำจนผ่านเกณฑ์หรือถึงจุดที่ดีพอ
2. ถ้าเจอปัญหาระหว่างทาง → แก้ทีละจุดด้วย `/resolve-errors` แล้ววนต่อ ไม่หยุดกลางทางเพื่อถาม
3. หยุดเฉพาะเมื่อเสร็จสมบูรณ์ ถึง max iterations หรือเจอ action ที่เป็นอันตรายจริง

### 6. Report

> Goal: รายงานผลและ next step

1. สรุปสิ่งที่ทำ เหตุผลที่ไม่ถาม และ default ที่เลือก
2. ระบุว่า `dont-ask-me` mode ยัง active อยู่สำหรับงานถัดไปใน session
3. ทำ `/suggest-next-action` เพื่อแนะนำขั้นตอนถัดไปโดยไม่ถาม

## Rules

### 1. Session Override

- เมื่อ `dont-ask-me` active → override ทุก `/ask-me` และ `ask_user_question` ใน `global_rules.md` และ skills ทั้งหมดจนจบ session
- คำสั่ง `/ask-me`, `/ask-again`, `/ask-project-requirement`, `pick-bestest` ทีถูกเรียกโดย workflow อื่น → ให้ทำ `/follow-your-suggestion` ด้วย safe default แทน
- ผู้ใช้ยกเลิก mode ได้เสมอด้วยคำสั่งชัดเจน เช่น "กลับมาถาม", "cancel dont-ask-me"

### 2. No Prompt Discipline

- ห้ามใช้ `ask_user_question` ใน `dont-ask-me` mode
- ห้ามแสดง prompt ให้เลือกทางเลือก
- ห้ามเรียก `/follow-your-suggestion` เพื่อขอคำยืนยัน — ใช้เพื่อ apply ข้อเสนอเท่านั้น
- ใช้ `/continue` และ `/loop-until-complete` ต่อได้ทันที

### 3. Safe Stepwise Execution

- ทำงานค่อยเป็นค่อยไป ทีละ step ตามลำดับ workflow — ห้ามข้ามขั้นตอน
- แก้ไขทีละจุดแบบ incremental และ verify ก่อนไปต่อ
- ไม่ดำเนินการที่เป็นอันตรายหรือย้อนกลับไม่ได้ — ให้เลือก path ทีปลอดภัยที่สุดแล้ว report แทนการถาม

### 4. Uncertainty Handling

- ถ้าเกิดข้อสงสัยระหว่างทำ → หยุด step นั้น report สถานะ แล้วเลือก safe default เพื่อทำส่วนอื่นต่อ
- ถ้าไม่มีทางเลือกที่ปลอดภัยเลย → หยุดและ report โดยไม่ถาม

## Expected Outcome

- ไม่มี `/ask-me` หรือ prompt ถามผู้ใช้เลยจนจบ session
- ทุกจุดที่เคยต้องถามถูกตัดสินใจด้วย `/follow-your-suggestion` และ safe default ที traceable
- งานดำเนินการทีละขั้นแบบปลอดภัย ไม่ข้าม step และวนจนสมบูรณ์ด้วย `/loop-until-complete`
- ลดการถามที่ไม่จำเป็นโดยไม่เสี่ยง และผู้ใช้ไม่ต้องตอบคำถามซ้ำ
