---
name: rethink
description: ทบทวนและ re-evaluate การตัดสินใจ แผน หรือ implementation เมื่อติดหรือมีข้อมูลใหม
argument-hint: "[topic]"
related:
  - deep-thinking
  - reframe
  - plan
  - deep-analyze
  - deep-research
  - deep-review
  - deep-validate
  - refactor
  - deep-review-then-fix
  - ask-me

---

## Goal

ทบทวนและ re-evaluate การตัดสินใจ แผน หรือ implementation ทีมีอยู่ เมื่อเจอ dead end ผลลัพธ์ไม่ตรงเป้า หรือมีข้อมูลใหม่ที่ชี้วว่าควรเปลี่ยนแนวทาง

## Scope

ใช้เมื่องานดำเนินไปแล้ว แต่ต้องการถอยกลับมาทบทวน ไม่ใช่การคิดครั้งแรก (ใช้ `/deep-thinking`) และไม่ใช่การครุ่นคิดก่อนตัดสินใจ (ใช้ `/deep-thinking`)

## Execute

### 1. Pause And State Current Position

> Goal: ระบุสถานะปัจจุบันก่อนทบทวน

1. ระบุ decision, plan, หรือ implementation ทีกำลัง rethink
2. สรุปสิ่งที่ทำไปแล้วและผลลัพธ์ทีได้
3. ระบุ assumptions และ constraints เดิม
4. บันทึก evidence ทีใช้ตัดสินใจครั้งแรก

### 2. Identify Rethink Triggers

> Goal: หาเหตุผลว่าทำไมต้อง rethink

1. ตรวจสอบว่ามีข้อมูลใหม่หรือ context เปลี่ยนหรือไม่
2. ตรวจสอบว่าผลลัพธ์ตรงกับ success criteria หรือไม่
3. ระบุจุดที่ติดหรือ failure ที่เกิดขึ้น
4. ประเมินว่าเป็น technical block, assumption wrong, หรือ scope drift

### 3. Challenge Assumptions

> Goal: ทดสอบ assumptions ทีเคยใช้

1. รายการ assumptions ทั้งหมดทีเกี่ยวข้อง
2. ถามย้อนกลับ: ถ้า assumption นี้ผิด จะเกิดอะไรขึ้น
3. หา evidence สนับสนุนหรือโต้แย้งแต่ละ assumption
4. ระบุ assumptions ที่ invalid หรือ outdated

### 4. Generate Alternatives

> Goal: คิดทางเลือกใหม่ทีเป็นไปได้

1. สร้างอย่างน้อย 2-3 alternatives นอกเหนือจากแผนเดิม
2. รวมถึงทางเลือกง่ายๆ เช่น do nothing, simplify, pivot, stop
3. ประเมิน effort, risk, และ expected outcome ของแต่ละทาง
4. เปรียบเทียบ trade-offs อย่างชัดเจน

### 5. Compare And Decide

> Goal: เลือกแนวทางทีดีทีสุด

1. ประเมินแต่ละ alternative ตาม success criteria
2. ระบุทางเลือกที reversible และ irreversible
3. เลือกทาง: continue, pivot, simplify, stop, หรือ gather more data
4. ระบุเหตุผลและ evidence ทีสนับสนุนการตัดสินใจ

### 6. Update And Report

> Goal: ปรับแผนและสื่อสาร

1. อัปเดต plan, skill, หรือ code ตาม decision ใหม่
2. ทำ `/update-references` ถ้ามีการเปลี่ยน path หรือชื่อ
3. บันทึกสิ่งที่เปลี่ยนและเหตุผล
4. ทำ `/suggest-next-action` เพื่อหาขั้นตอนถัดไป

## Rules

### 1. When To Rethink

ใช้ rethink เมื่อ:

- ทำไปครึ่งทางแล้วพบว่าทางเดิมไม่ไหว
- มีข้อมูลใหม่ที่ทำให้ assumption เดิมผิด
- ผลลัพธ์ไม่ตรงกับ success criteria
- มี simpler alternative ทีเพิ่งมองเห็น
- ต้องการ avoid sunk cost fallacy
- งานเกิด scope creep หรือ over-engineering

### 2. When Not To Rethink

ไม่ใช้ rethink เมื่อ:

- เป็น low-risk change ทีแก้ไขง่าย
- ยังไม่ได้เริ่มทำ หรือยังไม่มีข้อมูลพอ (ใช้ `/deep-thinking`)
- แค่ต้องการทบทวนก่อนตัดสินใจ (ใช้ `/deep-thinking`)
- ทุกอย่างดำเนินไปตามแผนและไม่มี red flag

### 3. Sunk Cost

- ไม่ยึดติดกับเวลาหรือ effort ทีใช้ไปแล้ว
- ตัดสินใจจาก expected future value ไม่ใช่ past investment
- ถ้าหยุดหรือ pivot ดีกว่า ให้แนะนำอย่างตรงไปตรงมา

### 4. Evidence Based

- ทุกการเปลี่ยนแปลงต้องมีเหตุผลจาก evidence
- ไม่เปลี่ยนแปลงเพียงเพราะความรู้สึกหรือ assumption ใหม่ไร้หลักฐาน
- ถ้าขาด evidence ให้ใช้ `/deep-research` หรือ `/ask-me` ก่อน

### 5. Timebox

- rethink เล็กไม่เกิน 3 นาที
- rethink กลางไม่เกิน 10 นาที
- rethink ใหญ่ไม่เกิน 20 นาที
- ถ้าเกินกว่านี้ ให้ใช้ `/ask-me` เพื่อขอข้อมูลเพิ่ม

### 6. Integration

- ใช้ `/deep-thinking` ถ้าต้องวิเคราะห์เชิงโครงสร้างใหม่
- ใช้ `/deep-thinking` ถ้าต้องทบทวนก่อนตัดสินใจ
- ใช้ `/plan` ถ้าต้องสร้างแผนใหม่
- ใช้ `/ask-me` ถ้าต้องการ user input
- ใช้ `/update-references` ถ้ามีการเปลี่ยน structure

- ใช้ /deep-analyze ถ้าจำเป็น
- ใช้ /deep-review ถ้าจำเป็น
- ใช้ /deep-validate ถ้าจำเป็น
- ใช้ /deep-review ถ้าจำเป็น
- ใช้ /refactor ถ้าจำเป็น
- ใช้ /deep-review-then-fix ถ้าจำเป็น
- ใช้ /reframe ถ้าจำเป็น


## Expected Outcome

- ชัดเจนว่าจะ continue, pivot, simplify, stop หรือ gather more data
- assumptions ที invalid ถูกระบุและแทนที
- แผนหรือ implementation อัปเดตตาม decision ใหม่
- รายงานสรุปเหตุผลและ next action
