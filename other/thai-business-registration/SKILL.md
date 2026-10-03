---
name: thai-business-registration
description: Decision tree เลือกประเภทจดทะเบียนธุรกิจในไทย — ทะเบียนพาณิชย์ (sole prop) vs หจก. vs บริษัทจำกัด vs BOI — flag VAT trigger (1.8M฿), SSO trigger (พนักงาน 1+ คน), ภาระบัญชี/ตรวจสอบ
when_to_use:
  - User บอก "จดบริษัท", "ตั้งบริษัท", "เปิดธุรกิจ"
  - User สงสัย sole prop vs หจก. vs บริษัทจำกัด
  - User mention BOI / ส่งเสริมการลงทุน
  - User mention VAT registration timing
when_not_to_use:
  - User ต้องการ tax projection — ใช้ thai-financial-projection
  - User ต้องการ Foreign Business License — ต้องคุยทนายเฉพาะทาง
version: 0.1.0
last_verified: 2026-05-19
tier: reference
---

# Thai Business Registration — Decision Tree

Mistake ที่ที่ปรึกษามือใหม่ทำบ่อยที่สุด: แนะนำ "จดบริษัทเลย" ทุกเคส. จริงๆ ลูกค้าที่รายได้ปีแรก 800k-1.6M ควรอยู่ **ทะเบียนพาณิชย์ (sole proprietorship)** — ประหยัดค่าทำบัญชี + ผู้สอบบัญชี 60-80k/ปี.

`thai-business-registration` ให้ Claude เดิน decision tree ตาม revenue, จำนวนหุ้นส่วน, และความต้องการ limited liability.

## เมื่อ Claude เห็นคำขอแบบนี้

```
จดบริษัทดีไหม รายได้ปีนี้จะแตะ 1.6M ทำคนเดียว
ตั้งร้านอาหารกับเพื่อน 2 คน คนละทุน 800k — รูปแบบไหนเหมาะ
อยากได้ BOI exemption ตอน export — เริ่มยังไง
```

## Decision tree

```
                     ┌──────────────────────────┐
                     │ Q1: หุ้นส่วน 1 คน หรือมากกว่า │
                     └────────────┬─────────────┘
                                  │
                  ┌───────────────┼────────────────┐
                  │                                │
              คนเดียว                          2+ คน
                  │                                │
                  ▼                                ▼
        ┌──────────────────┐               ┌───────────────────┐
        │ Q2A: รายได้/ปี    │               │ Q2B: ต้องการ      │
        │  ≤ 1.8M?         │               │ limited liability? │
        └─────┬────────────┘               └───────┬───────────┘
              │                                    │
        ┌─────┴─────┐                       ┌──────┴──────┐
       Yes          No                     No           Yes
        │           │                       │             │
        ▼           ▼                       ▼             ▼
  ทะเบียนพาณิชย์   บริษัทจำกัด                  หจก.       บริษัทจำกัด
  (sole prop)    (Co., Ltd.)              (limited      (Co., Ltd.
                                          partnership)   2+ shareholders)

  *** ถ้าได้สิทธิ BOI (ส่งออก / tech / R&D) → บริษัทจำกัด + ยื่น BOI แยก
```

## ประเภทธุรกิจในไทย — comparison table

| ประเภท | จดที่ | ทุนขั้นต่ำ | Liability | ภาระบัญชี | VAT trigger | Tax rate |
|---|---|---|---|---|---|---|
| ทะเบียนพาณิชย์ (sole prop) | สำนักงานเขต/อบต. | 0 | unlimited | บัญชีรายรับรายจ่ายอย่างง่าย | 1.8M | PIT (5-35% step) |
| ห้างหุ้นส่วนสามัญ (ไม่จดทะเบียน) | ไม่ต้องจด | 0 | unlimited ทุกหุ้นส่วน | ไม่บังคับ | 1.8M | PIT (each partner) |
| ห้างหุ้นส่วนสามัญนิติบุคคล | DBD | 0 | unlimited managing + limited silent | บัญชีตรวจสอบ | 1.8M | CIT 0/15/20% (SME tier) |
| ห้างหุ้นส่วนจำกัด (หจก.) | DBD | 0 | limited (silent partners) | บัญชีตรวจสอบ | 1.8M | CIT 0/15/20% |
| บริษัทจำกัด (Co., Ltd.) | DBD | 5,000 จดทะเบียน (paid-up ≥25%) | limited | บัญชีตรวจสอบ + audit | 1.8M | CIT 0/15/20% (SME) |
| บริษัท + BOI | BOI | ตาม activity | limited | + BOI report | 1.8M | tax holiday 3-13 ปี |
| Foreign-owned (FBL/BOI) | DBA/BOI | ตาม activity | limited | + report + work permit | 1.8M | varies |

## ขั้นตอน

1. **เก็บ input**
   - จำนวนหุ้นส่วน
   - รายได้คาดการณ์ปีแรก/2 ปี
   - ต้องการ limited liability ไหม
   - ส่งออกหรือมี R&D / tech / target BOI หรือไม่
   - คาดจ้างพนักงานปีแรกกี่คน

2. **เดิน decision tree**

3. **ตอบด้วย recommendation ที่ชี้ตัดสินใจ + เหตุผล**
   - ระบุ "ทำไม ไม่จดบริษัท" หรือ "ทำไม จด"
   - flag triggers ที่จะมาในอนาคต (VAT 1.8M, ออกจาก SME tier 30M)
   - คาด cost ของแต่ละ structure (ค่าจดทะเบียน, accounting, audit)

## ตัวอย่าง

### Input
```
จดบริษัทดีไหม ทำธุรกิจขายของออนไลน์คนเดียว
รายได้ปีนี้คาดว่าแตะ 1.6M ปีหน้าตั้งเป้า 3M
ไม่ได้จ้างใคร ทำเองทั้งหมด
```

### Output (sample)
```
แนะนำ: **ตอนนี้ทะเบียนพาณิชย์ (sole prop)** — แต่เตรียมข้อมูลให้พร้อมจดบริษัทตอนปีหน้า

ที่มา:
1. รายได้ปีนี้ 1.6M ยังไม่ถึง VAT trigger 1.8M — ไม่ต้องยื่น ภพ.30 รายเดือน
2. คนเดียว ไม่มีหุ้นส่วน — ไม่จำเป็นต้อง limit liability ผ่านนิติบุคคล
3. ภาระบัญชีถูกกว่ามาก:
   - sole prop: เก็บใบเสร็จ + บัญชีรายรับรายจ่าย ~6,000-12,000฿/ปี (DIY หรือ outsource เล็ก)
   - Co., Ltd.: ต้องมีผู้สอบบัญชี + auditor → 40,000-80,000฿/ปี
4. รายได้ปีนี้ 1.6M ในฐานะ sole prop เสีย PIT (เลือก method "หักค่าใช้จ่ายเหมา 60%" ได้ถ้าธุรกิจซื้อมาขายไป) — net taxable ~640k → PIT ประมาณ 15-25k. ใกล้เคียง CIT ที่ 15% บน 300k = 45k

แต่ปีหน้า (3M) จะ trigger:
- ★ VAT registration บังคับ (>1.8M) → start ก้าวเข้า ภพ.30 รายเดือน
- ★ CIT tier ที่ 3M จะใกล้ 15% upper bound — เริ่มมีเหตุผลจดบริษัท

แผนเชิงปฏิบัติ:
1. ปีนี้: คงเป็น sole prop, เริ่มเก็บใบกำกับภาษีของ supplier (เผื่อจะขึ้น VAT ปีหน้าได้ใช้เป็น VAT input credit)
2. Q3 ปีนี้: ติดต่อสำนักงานบัญชีคุยเรื่องโครงสร้างปีหน้า
3. Q1 ปีหน้า: ยื่นจดบริษัทถ้า revenue trend ยืนยัน

ข้อแม้ (ที่ต้องเฝ้า):
- ★ ถ้ามีลูกค้ารายใหญ่ B2B 1-2 ราย — บริษัทจำกัดอาจดูน่าเชื่อถือกว่า sole prop. weigh trade-off
- ★ ถ้า product เป็น category ที่ต้อง อย./TISI (cosmetic, food, electronics) — จดทะเบียน อย. ในนาม sole prop ได้ แต่บางหมวด นิติบุคคลผ่านง่ายกว่า
```

## VAT trigger — สำคัญที่สุด

```
1.8M฿/ปี — รายได้รวม VAT-able (ไม่นับ exempt sales)

เมื่อ trigger:
  - ยื่น ภ.อ.01 ภายใน 30 วันที่เกิน
  - เริ่มออกใบกำกับภาษีให้ลูกค้า (VAT 7%)
  - ยื่น ภพ.30 ทุกเดือน (วันที่ 15 ของเดือนถัดไป)
  - ขอ VAT input credit จากใบกำกับ supplier
```

## Common mistakes

- จดบริษัทตั้งแต่ revenue 500k — เปลือง 60-80k/ปี ค่าตรวจสอบบัญชี
- ใช้ "ห้างหุ้นส่วนสามัญ" (ไม่จดทะเบียน) คิดว่าง่าย — จริงๆ liability เต็มของทุกหุ้นส่วน ไม่มี separation
- BOI ขอตอน revenue 5M ทั้งที่เพิ่งเริ่ม — BOI สมัครได้ตั้งแต่ก่อนเริ่มกิจกรรม
- ลืม VAT trigger 1.8M — สรรพากรเรียกย้อนหลังถ้าไม่ยื่น

## ขอบเขต

- ไม่ครอบ Foreign Business License (FBL) / Foreign Business Operation — ต้องคุยทนายเฉพาะ
- ไม่ครอบ Partnership Investment Conditions (PIC, FBA) — กฎหมายเฉพาะ
- ไม่ทำขั้นตอน BOI application — ขั้นนี้ต้องเขียน application+ feasibility study

## แหล่งอ้างอิง

- DBD — Companies Registration: `dbd.go.th`
- กรมสรรพากร — VAT: `rd.go.th/268.html`
- กรมสรรพากร — บุคคลธรรมดา (PIT): `rd.go.th/272.html`
- BOI — Investment Promotion: `boi.go.th`
- SSO — บังคับเข้าระบบเมื่อจ้างพนักงาน 1+ คน
