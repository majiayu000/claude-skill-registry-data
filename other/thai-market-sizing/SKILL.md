---
name: thai-market-sizing
description: ประเมินขนาดตลาดไทย TAM/SAM/SOM ด้วย source pointer ทางการ (NSO, BOT, DBD, ETDA, NESDC) — ไม่ใช้ Statista global ที่ตัวเลขมั่ว หรือ McKinsey report ที่ data ฝรั่ง
when_to_use:
  - User mention "ขนาดตลาด", "market size", "TAM", "SAM", "SOM", "market opportunity"
  - User เตรียม pitch deck / investor presentation
  - User สงสัยว่ามี demand เท่าไหร่ก่อนเข้าตลาด
when_not_to_use:
  - User ต้องการ competitor breakdown — ใช้ thai-competitor-scan
  - User ต้องการ customer interview / qual research — ตอบตรงๆ
version: 0.1.0
last_verified: 2026-05-19
tier: prose
---

# Thai Market Sizing — สิทธิเข้าถึงข้อมูลฟรี

ที่ปรึกษาส่วนใหญ่ตอบ TAM/SAM/SOM แบบโยน Statista global × % Thailand population ออกมาเป็น "อัตราพร้อมพิมพ์". ปัญหา: ตัวเลขห่างจริง 2-5x.

ประเทศไทยมีข้อมูลทางการเปิด public ฟรีเยอะมาก — แต่ที่ปรึกษาส่วนใหญ่ไม่รู้ว่าอยู่ที่ไหน:

| สิ่งที่จะวัด | แหล่งทางการ | URL |
|---|---|---|
| จำนวนครัวเรือน, การใช้จ่ายต่อหัว | สำรวจภาวะเศรษฐกิจสังคมครัวเรือน, NSO | `nso.go.th` (annual SES report) |
| GDP รายอุตสาหกรรม | สำนักงาน สศช. (NESDC) | `nesdc.go.th` |
| Online retail GMV | ETDA E-Commerce Statistics | `etda.or.th` |
| Banking + payment volume | BOT Statistics | `bot.or.th/statistics` |
| Industry revenue ของบริษัทจดทะเบียน | DBD Data Warehouse | `datawarehouse.dbd.go.th` |
| Import/Export by HS | Trade Report กระทรวงพาณิชย์ | `tradereport.moc.go.th` |
| Demographic | Statbureau ทะเบียนราษฎร์ | `stat.bora.dopa.go.th` |

Skill นี้ทำให้ Claude **ไม่เดาตัวเลข** — มันต้อง point ไปที่แหล่งทางการเสมอ.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ตลาดเครื่องสำอางออนไลน์ในไทยใหญ่แค่ไหน
TAM/SAM/SOM ของ co-working space ในกรุงเทพ
```

## ขั้นตอน

1. **ระบุ category ให้ชัด** — ถาม user 2-3 คำถาม
   - กลุ่มลูกค้า: B2C / B2B / B2G
   - geography: ทั่วประเทศ / Bangkok+ปริมณฑล / regional
   - online / offline / blended
   - segment ของ category (skincare ≠ makeup ≠ haircare)

2. **TAM** — ตลาดทั้งหมดของ category ในไทย
   - ใช้ NESDC / ETDA / industry association report
   - **ระบุปี + source ทุกครั้ง** (e.g., "ETDA 2025 E-Commerce Report: B2C online retail GMV = 1.04 ล้านล้านบาท")

3. **SAM** — กลุ่มที่ business นี้ targetable ได้จริง
   - filter ด้วย: geography, demographics (age, income), channel
   - ใช้ NSO SES filtering

4. **SOM** — ส่วนที่ realistic ภายใน 12-24 เดือน
   - benchmark กับ competitor market share (ถ้ารู้ — ใช้ DBD financial filings)
   - rule of thumb: new entrant ปกติ 0.1-2% ของ SAM ภายใน 12 เดือน

5. **คืน output**
   - **3 ตัวเลข + source + confidence**
   - **ข้อสมมุติฐาน 3-5 ข้อ** ที่ทำให้เลขเป็นแบบนี้
   - **ตัวเลขที่เปลี่ยน 10% แล้ว SOM เปลี่ยน >20%** (sensitivity)

## ตัวอย่าง

### Input
```
ตลาด skincare ออนไลน์ในไทย — เราจะขายผ่าน Shopee + TikTok Shop
target audience: ผู้หญิง 22-40, รายได้ 20k-60k/เดือน
```

### Output (sample)
```
TAM — Online skincare retail ในไทย
  มูลค่า ~ 35,000-42,000 ล้านบาท/ปี (2025)
  Sources:
    - ETDA E-Commerce Statistics 2025 (`etda.or.th`): Beauty & Personal Care
      online ~6.3% ของ B2C GMV = 65,500M฿; ของ skincare ~55% = 36,000M฿
    - GroupM Thailand Beauty Industry Report H2 2025 (cross-check): 38-42B฿
  Confidence: medium — ตัวเลขใกล้กันสองแหล่ง

SAM — Targetable (ผู้หญิง 22-40, รายได้ 20-60k, urban)
  Filter:
    - ผู้หญิง 22-40 = 21% ของประชากร (NSO 2024) ≈ 14.6M คน
    - รายได้ 20-60k/เดือน = 39% ของ working population (NSO SES 2024) ≈ 5.7M คน
    - online shopper ของ beauty category = 73% (ETDA 2025) ≈ 4.2M คน
  ค่าใช้จ่าย skincare เฉลี่ย 320฿/เดือน (Kantar Worldpanel 2024)
  SAM ≈ 4.2M × 320 × 12 = 16,128M฿/ปี
  Confidence: medium-low — Kantar number paywalled, ใช้ค่าเฉลี่ยที่ public

SOM — ภายใน 12-24 เดือน
  Rule of thumb new entrant: 0.3% - 1.5% ของ SAM
  SOM = 48-242M฿/ปี
  Confidence: low — ขึ้นอยู่กับ marketing budget, conversion rate, retention

ข้อสมมุติฐาน
1. Beauty share ของ online B2C ตาม ETDA 2025 ใกล้เคียงปี 2026 (อาจขยับ ±2%)
2. ค่าใช้จ่าย skincare/เดือนของ target segment สูงกว่าค่าเฉลี่ย (ใช้ค่าเฉลี่ย — ตัวจริงอาจ 380-450฿)
3. กลุ่ม age 22-40 มี penetration online beauty 73% เท่ากันทุก segment (จริงน้อยกว่า 22-30)

Sensitivity
- ถ้า penetration online สูงกว่า 73% เป็น 82% (เพิ่ม 12%) → SAM เพิ่ม 12%, SOM เพิ่ม ~15%
- ถ้า ค่าใช้จ่าย/เดือนเพิ่มจาก 320 เป็น 400 (เพิ่ม 25%) → SAM เพิ่ม 25%

แนะนำขั้นถัดไป
- หา exact spend per cohort ที่ Kantar (paid report) หรือสำรวจเอง 50-100 คน
- ดู Shopee Mall + TikTok Shop top-sellers ใน category ปริมาณรายเดือนของ top-50 sellers (Brandtag, Wisesight)
- คุย founder ของ skincare brand ที่ exit ได้ ~50M ใน 18 เดือน
```

## Common mistakes

- Quote "ตลาดเครื่องสำอางไทย 200,000M฿" จาก Statista แล้วใช้เป็น TAM — ตัวเลขนี้รวม offline + import + B2B + cross-border ไม่ใช่ที่ target
- ใช้ Thailand population (66M) × % เป็น addressable — ลืม filter income, channel, age
- claim SOM 5-10% ของ SAM ใน 12 เดือน — ความจริงคือ 0.1-2% สำหรับ new entrant ไม่มี brand
- ไม่ระบุปีของ source — data 2020 ใช้ predict 2026 จะคลาด

## ขอบเขต

- ตัวเลขใน demo เป็น **synthetic illustration** — ถ้าเอาไปใช้กับลูกค้าจริง ต้อง re-verify จาก source ตรง
- ไม่ทำ qualitative market research — เครื่องมือนี้คือ desk research only
- Cross-border (Shopee SG/MY/PH) ไม่อยู่ในขอบเขต — ใช้ Singapore reports แทน
