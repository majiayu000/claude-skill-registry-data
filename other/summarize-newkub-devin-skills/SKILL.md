---
name: summarize
description: สรุปเนื้อหาตาม context ทั่วไป
argument-hint: "<context>"
related:
  - scan-codebase
  - report
  - list-git
  - report-git-diff

---
## Goal

สรุปเนื้อหาตาม context ทั่วไป เช่น project, chat, code, files, หรือ topic ที่ระบุ

## Scope

ใช้เมื่อ user ต้องการสรุปเนื้อหาโดยไม่ระบุ skill ย่อย โดย `summarize` จะเลือกหรือ delegate ไปยัง skill ทีเหมาะสม

## Execute

### 1. Identify Context

> Goal: ระบุ context ทีต้องสรุป

1. อ่าน argument `<context>` หรือ context จาก task
2. ระบุประเภท: `project`, `chat`, `code`, `file`, `topic`, `conversation`, `changes`
3. ถ้า context ไม่ชัด → ถาม user
4. ระบุ output format: bullet, paragraph, table, flow

### 2. Select Summarizer

> Goal: เลือก skill สรุปทีเหมาะสม

1. ถ้า `project` → สรุป scope project ตาม flow ของ skill นี้
2. ถ้า `chat` หรือ `conversation` → สรุป scope chat/session ตาม flow ของ skill นี้
3. ถ้าต้องการ bullet/numbered list → ทำ `/report`
4. ถ้า `code` → ทำ `/scan-codebase` แล้ว `/report`
5. ถ้า `file` → อ่านไฟล์แล้วสรุป
6. ถ้า `changes` → ทำ `/list-git-commit` หรือ `/report-git-diff`
7. ถ้าไม่ตรงกับ skill ย่อย → สรุปตรงจุดด้วย `/report`

### 3. Summarize

> Goal: สรุปเนื้อหา

1. ส่ง input ทั้งหมดให้ skill ย่อยทีเลือก
2. ถ้าต้องการสรุปเอง:
   - อ่านเนื้อหาต้นฉบับ
   - ระบุ main points และ key takeaways
   - ลบรายละเอียดทีไม่จำเป็น
   - จัดลำดับตาม priority
3. รักษา context และไม่ distort ความหมาย

### 4. Format And Report

> Goal: นำเสนอสรุป

1. ใช้รูปแบบตามที user ต้องการ (bullet, paragraph, table)
2. ใช้ `/report` ถ้ามีหลายหมวด
3. ระบุสิ่งทีขาดหรือต้องทำต่อ
4. ทำ `/suggest-next-action`

## Rules

### 1. Context Aware

- ไม่เดาเนื้อหานอก context
- ถาม user ถ้าข้อมูลไม่พอ
- เลือก skill ย่อยตาม context

### 2. Concise

- หนึ่ง bullet = หนึ่ง idea
- ใช้ภาษากระชับ
- เก็บเฉพาะสาระสำคัญ

### 3. Accuracy

- ไม่ตัดความหมายผิด
- รักษา context
- ระบุข้อจำกัดถ้ามี

## Expected Outcome

- สรุปตรงกับ context ทีระบุ
- รูปแบบตรงตามทีขอ
- เนื้อหาครบถ้วนและกระชับ
- ระบุ next action ถ้ามี
