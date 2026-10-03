---
name: thai-cashflow-survival
description: กางปฏิทิน 90 วันของ cashflow สำหรับ SME ไทย โดย lock timing ที่ฝรั่งไม่รู้ — credit term 30/60/90, VAT refund 3-6 เดือน, PND.1 (วันที่ 7), SSO (15), ภพ.30 (15), ภงด.50/51, เงินเดือน
when_to_use:
  - User บอก "cashflow", "กระแสเงินสด", "เงินจะหมุนทันไหม"
  - User mention credit term / "ลูกค้าจ่ายช้า" / "ภพ.30"
  - User เตรียม banking facility / ขอ LC / ขอ OD
  - User เจอ cash crunch ใกล้ตึง
when_not_to_use:
  - คำถาม long-term financial projection — ใช้ thai-financial-projection
  - คำถาม fundraising — ใช้ thai-vc-fundraising
version: 0.1.0
last_verified: 2026-05-19
tier: validator
---

# Thai Cashflow Survival — 90-day calendar

SME ไทยที่ไม่ตายเพราะตัวเลขแต่ตายเพราะ **timing**:
- ลูกค้าใหญ่จ่าย credit 60 วัน, supplier ให้ credit 30 วัน → จ่ายก่อน 30 วัน
- VAT refund (case ส่งออก) ใช้เวลา 3-6 เดือน → อย่าคิดเป็น receivable ระยะสั้น
- PND.1 (WHT พนักงาน) ต้องยื่นวันที่ 7 ของเดือนถัดไป
- SSO ต้องส่งวันที่ 15 ของเดือนถัดไป
- ภพ.30 (VAT) วันที่ 15 ของเดือนถัดไป
- ภงด.51 ครึ่งปี
- เงินเดือนสิ้นเดือนหรือกลางเดือน

`cashflow.py` ใน skill นี้สร้างปฏิทิน 90 วันที่ lock event เหล่านี้ลงไป.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ร้านอาหาร revenue 600k/เดือน เงินเดือนพนักงาน 8 คน รวม 180k
ค่าเช่า 95k, วัตถุดิบ 35% — ทำ 90-day cashflow

จะเสีย VAT 84k เดือนนี้ + ภงด.51 ตุลา 1.2M — เงินทันไหม
```

## ขั้นตอน

1. **เก็บ input**
   - Revenue ต่อเดือน + credit term (B2C cash / B2B 30/60/90)
   - Opex breakdown: เงินเดือน, เช่า, utilities, marketing, อื่นๆ
   - COGS / วัตถุดิบ + supplier credit
   - Tax obligations รู้: VAT รายเดือน, ภงด.50 ปลายปี, ภงด.51 กลางปี
   - Cash starting balance
   - Date of analysis

2. **เรียก `cashflow.py`**
   ```python
   from cashflow import build_90_day_calendar
   calendar = build_90_day_calendar(start_date, opening_balance, monthly_events)
   ```

3. **คืน output**
   - ตารางรายสัปดาห์: opening, inflows, outflows, closing
   - Cash low point (วันใดยอดต่ำสุด)
   - Critical events ที่ต้องเตรียม (จ่าย VAT, SSO, PND.1, ภงด.51)

4. **ข้อสังเกต**
   - ถ้า closing balance ใดติดลบ → แจ้ง "ต้อง OD / supplier extension / pre-payment"
   - ถ้า VAT refund รอ >60 วัน → flag "อย่าใช้เป็น cash source"
   - ถ้า client 1 รายเป็น >40% receivable → concentration risk

## Standard Thai timing events

| Event | When | Default amount |
|---|---|---|
| เงินเดือน | ปลายเดือนหรือ 25 | จำนวนพนักงาน × เงินเดือนเฉลี่ย |
| PND.1 (WHT พนักงาน) | วันที่ 7 ของเดือนถัดไป | ~3% ของฐานเงินเดือนที่เกิน threshold |
| SSO (5%+5%) | วันที่ 15 ของเดือนถัดไป | ฐานเงินเดือน × 10% (cap @15k base) |
| ภพ.30 (VAT) | วันที่ 15 ของเดือนถัดไป | VAT ขาย - VAT ซื้อ |
| ภงด.3, 53 (WHT supplier) | วันที่ 7 ของเดือนถัดไป | 3% ของค่าบริการที่หัก |
| ภงด.51 (ครึ่งปี) | สิงหาคม (ภายใน 2 เดือนหลังครึ่งปี) | ประมาณการ income tax |
| ภงด.50 (ปลายปี) | พฤษภาคม (ภายใน 150 วันหลังปิดบัญชี) | จริง - ที่จ่ายไปแล้ว |
| ค่าเช่า | ต้นเดือน 1-5 | คงที่ |

## ตัวอย่าง

### Input
```
ร้านอาหารกลางเมือง
Revenue 600k/month (cash B2C)
Opex: เงินเดือน 180k + ค่าเช่า 95k + ค่าน้ำไฟ 25k + marketing 30k
COGS: 35% ของ revenue (วัตถุดิบ, จ่าย supplier net 30 วัน)
ขึ้น VAT แล้ว
Opening cash: 250k
Start date: 2026-05-19
```

### Output (sample)
```
| สัปดาห์ | Opening | Inflows  | Outflows  | Closing  | Key events    |
|--------:|--------:|---------:|----------:|---------:|---------------|
| W1      | 250,000 | 150,000  |  290,000  |  110,000 | เงินเดือน, ค่าเช่า |
| W2      | 110,000 | 150,000  |  154,000  |  106,000 | PND.1, SSO, ภพ.30 |
| W3      | 106,000 | 150,000  |  210,000  |   46,000 | จ่าย supplier (เดือนก่อน) |
| W4      |  46,000 | 150,000  |   30,000  |  166,000 | (ไม่มี event ใหญ่) |
| ...

Low point: 2026-06-08 — เหลือ 46,000฿ (8% ของ revenue เดือน)
Critical: ภงด.51 due 2026-08-31 ≈ 180,000฿ — ต้องเก็บไว้

ข้อสังเกต:
- W3 cash หล่นเข้าใกล้ low — supplier จ่าย net 30 รวมกันก้อนใหญ่ ลองเจรจาเป็น net 45 ลดความเสี่ยง
- VAT W2 ก้อนหนึ่ง — supplier ส่วนใหญ่เป็น B2C ไม่ให้ใบกำกับ ทำให้ VAT input น้อย พึ่งเก็บใบให้ครบ
- ภงด.51 สิงหาคม 180k — ตอนนี้ยังไม่เริ่ม set-aside, ควรกัน 60k/เดือน 3 เดือนข้างหน้า
```

## Common mistakes

- คิด credit term ลูกค้าเป็น "วันเฉลี่ย" ทั้งที่ที่แท้คือ "วันที่ลูกค้าจ่ายจริง" (มี delay 5-15 วันบนสัญญา)
- ลืม VAT จ่ายปลายเดือน — มาเจอ surprise ต้นเดือน
- ใส่ revenue เต็มจำนวนทั้งที่ออก credit 60 วัน — cash ยังไม่เข้า
- ลืมว่า ภงด.51 ครึ่งปี ต้องประมาณ 25% ภายใน — ถ้าประมาณต่ำเกินโดนปรับ
- คิดว่า VAT refund (case ส่งออก) เป็น receivable ใน 30 วัน — จริง 3-6 เดือน

## ข้อจำกัด

- ปฏิทินสมมุติ 30 วัน/เดือน — ใน production calculator ใช้ datetime จริง
- ไม่รวม BOI tax exemption — ถ้ามี BOI ลด tax line
- ไม่รวม OD / loan repayment — เพิ่ม manual

## แหล่งอ้างอิง

- กรมสรรพากร — กำหนดเวลายื่นแบบ: `rd.go.th/49830.html`
- สำนักงานประกันสังคม — กำหนดเวลานำส่ง: `sso.go.th`
