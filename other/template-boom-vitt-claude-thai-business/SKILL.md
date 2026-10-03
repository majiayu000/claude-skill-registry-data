---
name: thai-skill-slug
description: หนึ่งบรรทัด — Claude เอาไปจับ intent ของ user
when_to_use:
  - เคสที่ skill นี้ตอบโจทย์ (1)
  - เคสที่ skill นี้ตอบโจทย์ (2)
  - เคสที่ skill นี้ตอบโจทย์ (3)
when_not_to_use:
  - เคสที่ skill นี้ไม่เหมาะ — ชี้ไปที่ skill อื่นแทน
version: 0.1.0
last_verified: 2026-05-19
tier: validator  # หรือ reference / prose
---

# {{Skill Name}}

หนึ่งย่อหน้าอธิบายว่า skill นี้คืออะไร — ผู้ใช้จะได้อะไรกลับมา.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ตัวอย่าง prompt ที่ควรหยิบ skill นี้
```

## ขั้นตอน (Claude ทำตามนี้)

1. **เก็บ input จาก user** — list ตัวแปรที่ต้องถาม
   - ตัวแปร 1 (ประเภท, ตัวอย่าง)
   - ตัวแปร 2

2. **ตรวจ edge case**
   - ถ้า input ไม่ครบ — ถามต่อหรือใช้ default ที่ระบุไว้
   - ถ้า input ขัดกับกฎ (เช่น VAT trigger) — flag ก่อนคำนวน

3. **เรียก calculator** (ถ้ามี)
   ```python
   from <thing> import calculate
   result = calculate(...)
   ```

4. **format output** ให้ user — ตารางสั้น + bullet "ข้อสังเกต" ไม่เกิน 5 ข้อ

## ตัวอย่าง

### Input
```
prompt ตัวอย่าง
```

### Output
```
output ที่ดี
```

## Common mistakes ที่ Claude ทำ (ก่อนมี skill นี้)

- ใช้ benchmark US แทน TH
- ลืม VAT 7% / WHT
- format ตัวเลขเป็น USD

## แหล่งอ้างอิง

- [ทางการที่ 1] — `https://...`
- [ทางการที่ 2] — `https://...`

## ข้อจำกัด

- ระบุข้อจำกัดที่รู้
- เคสที่ skill นี้แก้ไม่ได้
