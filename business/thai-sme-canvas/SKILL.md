---
name: thai-sme-canvas
description: วาด Business Model Canvas สำหรับ SME ไทย โดยมีช่องที่ template ฝรั่งไม่มี — family-stakeholder map, ทุนจดทะเบียน vs ทุนชำระแล้ว, MOU vs registered partner, informal employee, "พี่/น้อง/หลาน" guarantor มาแทนที่ "co-founder equity vesting"
when_to_use:
  - User บอก "วาด Business Model Canvas", "BMC", "Lean Canvas"
  - User เริ่มธุรกิจใหม่ / pivoting / re-strategizing
  - User มี stakeholder ในครอบครัวที่ template ฝรั่งไม่มีช่องให้
  - User อยากสรุปโมเดลธุรกิจให้ที่ปรึกษา/พาร์ทเนอร์/ธนาคารดู
when_not_to_use:
  - User ต้องการ financial projection — ใช้ thai-financial-projection
  - User ต้องการ market size — ใช้ thai-market-sizing
version: 0.1.0
last_verified: 2026-05-19
tier: reference
---

# Thai SME Business Model Canvas

Strategyzer Business Model Canvas (BMC) ออกแบบมาสำหรับธุรกิจที่ co-founder vesting, VC funding, employee stock option — assumption แบบ Silicon Valley. SME ไทยส่วนใหญ่ไม่มีของพวกนี้ มี:

- **พี่/น้อง/พ่อแม่เซ็นค้ำเงินกู้** แทน VC equity
- **ทุนชำระแล้ว ≠ ทุนจดทะเบียน** (จดเยอะ ชำระน้อย)
- **พนักงานนอกระบบ** (รายวัน/ฟรีแลนซ์/ครอบครัว) ที่ไม่มี SSO
- **MOU กับพันธมิตร** ที่ไม่ได้จดเป็น partner
- **พึ่งช่องทางเดียว** (Shopee 80% / TikTok 70%) ที่ฝรั่งไม่ถือเป็น risk

Skill นี้ให้ Claude วาด BMC ที่มีช่องเพิ่มเฉพาะ Thai context — เถ้าแก่อ่านแล้วเข้าใจตรงๆ.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ทำ Business Model Canvas ให้ร้านกาแฟทองหล่อ ทุนจดทะเบียน 2.5M
พี่ชายค้ำเงินกู้แบงค์ 800k
```

## โครงสร้าง 11-box ที่ใช้ (ขยายจาก BMC 9-box)

```
┌──────────────────────┬───────────────────┬──────────────────────┐
│ พันธมิตรหลัก          │ กิจกรรมหลัก       │ Value Proposition    │
│ (Key Partners)       │ (Activities)      │                      │
│ - MOU vs จดทะเบียน    │                   │                      │
│ - supplier credit    │                   │                      │
│ ★ Family-stakeholder │ ★ Informal team   │ ★ Channel-specific   │
│   พี่/น้อง/พ่อแม่ค้ำ    │   พนักงาน นอก/ใน    │   value (online vs   │
│                      │   ระบบ            │   offline)           │
├──────────────────────┼───────────────────┴──────────────────────┤
│ ทรัพยากรหลัก          │ ★ ทุนจดทะเบียน vs ทุนชำระแล้ว              │
│ (Key Resources)      │   - paid-up:              บาท             │
│                      │   - registered:           บาท             │
│                      │   - guarantor:            (ใคร / จำนวน)    │
├──────────────────────┼───────────────────────────────────────────┤
│ ลูกค้าสัมพันธ์          │ ลูกค้ากลุ่มเป้าหมาย                          │
│ (Relationships)      │ (Customer Segments)                       │
│                      │                                           │
├──────────────────────┴───────────────────────────────────────────┤
│ ช่องทาง (Channels)                                                │
│   ★ Channel concentration risk (ถ้า single >60% → flag)            │
│   ★ Marketplace dependency (Shopee/Lazada/TikTok Shop)              │
├──────────────────────────────────────┬───────────────────────────┤
│ โครงสร้างต้นทุน                          │ กระแสรายได้                  │
│ (Cost Structure)                      │ (Revenue Streams)         │
│ - ★ fixed: เช่า, เงินเดือน, dev cost      │ - subscription / one-time │
│ - ★ variable: COGS, marketplace fee   │ - VAT-inclusive / exclusive│
└──────────────────────────────────────┴───────────────────────────┘

★ Compliance & Cash Notes (ช่องที่ 10-11)
  - VAT status (จด/ไม่จด, trigger ที่ 1.8M)
  - บริษัทประเภทไหน (sole prop / หจก. / บริษัทจำกัด / BOI)
  - Critical timing (เช่า: ต่อยังไง, supplier: credit term)
```

## ขั้นตอน

1. **เก็บ input ทีละ box** — ไม่ต้องครบทุกช่องในรอบแรก, focus 3-4 ช่องที่ user ห่วงสุด
2. **ขยายช่อง ★ ด้วยคำถามเฉพาะ**
   - ทุนจดทะเบียน vs ทุนชำระ — ถ้าต่างกัน ระบุ paid-up จริง
   - Family-stakeholder — ใครค้ำ, เท่าไหร่, มี contract เป็นลายลักษณ์อักษรไหม
   - Informal employee — จ่ายเป็นรายวัน/รายชั่วโมง? ไม่มี SSO? เสี่ยงโดน labor inspection
   - Channel concentration — ถ้า Shopee >60% → flag
3. **คืน output เป็น markdown** ที่ paste ลง Notion/Excalidraw ได้
4. **flag 3 อย่างที่จะทำให้ business fragile**

## ตัวอย่าง

### Input
```
ร้านกาแฟทองหล่อ ทุนจดทะเบียน 2.5M
พี่ชายค้ำเงินกู้แบงค์ 800k ดอกเบี้ย 8%/yr
บาริสตา 3 คน + 1 ผู้ช่วย (รายวัน)
ขายหน้าร้าน 70% + delivery (Robinhood/Grab/Line Man) 30%
```

### Output (sample)
```markdown
## Business Model Canvas — ร้านกาแฟทองหล่อ

### พันธมิตรหลัก
- Supplier เมล็ดกาแฟ (Doi Tung) — credit net 15
- Robinhood / Grab / Line Man (commission 25-30%)
- ★ พี่ชายค้ำเงินกู้ 800k — informal agreement, ไม่มี shareholder ตอบแทน

### ทุน (Capital)
- ทุนจดทะเบียน: 2,500,000
- ทุนชำระแล้ว: ____ (ต้องระบุ — ปกติ 25% = 625k)
- เงินกู้แบงค์: 800,000 (พี่ชายค้ำ)
- ★ ดอกเบี้ย 8%/ปี = 64,000/yr ต้นทุนคงที่

### กิจกรรมหลัก / ทรัพยากร
- ชง, จัดการ inventory, social media
- บาริสตา 3 คน (ใน SSO) + 1 รายวัน (★ ★ ไม่อยู่ใน SSO — ถ้าทำงานเกิน 12 ชม./เดือน ต้องเข้า SSO ตามกฎหมาย)

### ลูกค้า / Value Proposition
- demographic: ทำงานออฟฟิศ 25-40
- VP: specialty coffee + ความเร็ว (ไม่เกิน 4 นาที)

### ช่องทาง
- หน้าร้าน 70%
- Delivery 30% (★ concentration risk ต่ำ, ผ่าน 3 platforms, ไม่ tied)

### โครงสร้างต้นทุน
- Fixed: เช่า (มี?), เงินเดือน 3 คน × 22k = 66k, ดอกเบี้ย 5,333/เดือน
- Variable: COGS เมล็ดกาแฟ ~25%, นม ~10%, vendor commission delivery ~28%

### กระแสรายได้
- หน้าร้าน cash 70%
- Delivery แต่ละแอป hold 7-14 วันก่อนโอน — ★ ส่งผลต่อ cashflow weekly

### 3 อย่างที่ทำให้ fragile
1. ★ ทุนชำระแล้วยังไม่ระบุ — ถ้า 25% (625k) + เงินกู้ 800k = ทุนเริ่มต้น 1.4M, runway ที่ break-even เดือนไหน
2. ★ ดอกเบี้ย 8% = 64k/yr ที่ paid-up 625k → 10% ของทุน. ถ้า revenue ไม่ทันต้องโอนพี่ชายเป็น shareholder แทนค้ำ
3. ★ พนักงานรายวัน 1 คน — ถ้าทำงานเกิน 12 ชม./เดือน ต้องเข้า SSO. labor inspection สุ่มเจอ ปรับ 5,000-50,000
```

## ขอบเขต

- ไม่สร้าง financial projection — ใช้ `thai-financial-projection`
- ไม่ทำ market sizing — ใช้ `thai-market-sizing`
- BMC เป็น snapshot — review ทุก 6 เดือน หรือเมื่อ pivot

## แหล่งอ้างอิง

- Strategyzer Business Model Canvas — `strategyzer.com/canvas/business-model-canvas`
- Ash Maurya Lean Canvas — `leanstack.com/lean-canvas`
- DBD — ทุนจดทะเบียน vs ทุนชำระ: `dbd.go.th/news_view.php?nid=___`
- กระทรวงแรงงาน — กฎหมายแรงงาน: `labour.go.th`
