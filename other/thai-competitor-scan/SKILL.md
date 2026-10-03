---
name: thai-competitor-scan
description: วิเคราะห์คู่แข่งในตลาดไทยด้วย Porter 5 Forces ที่แปลเป็นคำถามภาษาเถ้าแก่ + วิธีดึงงบการเงินคู่แข่งจาก datawarehouse.dbd.go.th (public ฟรี) — ทุกบริษัทจำกัดในไทยต้องยื่นรายปี
when_to_use:
  - User mention "วิเคราะห์คู่แข่ง", "competitor analysis", "Porter 5 Forces"
  - User อยากดู moat / barrier to entry / supplier power / buyer power
  - User เตรียม market entry strategy
  - User ทำ M&A due diligence ขั้นแรก
when_not_to_use:
  - User ต้องการ market size — ใช้ thai-market-sizing
  - User ต้องการ pricing position — ใช้ thai-pricing-strategy
version: 0.1.0
last_verified: 2026-05-19
tier: prose
---

# Thai Competitor Scan — Porter 5F + DBD financial lookup

Porter 5 Forces เขียนเป็น consultancy-speak อ่านไม่รู้เรื่อง. ที่ปรึกษาที่ทำงานกับเถ้าแก่ไทยต้องแปลเป็น 5 คำถามที่ลูกค้าตอบได้ใน 30 วินาที.

**ข้อได้เปรียบที่ไม่ค่อยมีคนใช้**: ในไทย **ทุกบริษัทจำกัด** ต้องยื่นงบการเงินรายปีกับ DBD — เปิด public ฟรี ที่ `datawarehouse.dbd.go.th`. ค้นด้วยชื่อบริษัทหรือเลขทะเบียน 13 หลัก ได้ revenue, net profit, total assets ของคู่แข่งตรงๆ.

## เมื่อ Claude เห็นคำขอแบบนี้

```
วิเคราะห์คู่แข่งร้านชาบูในย่านอโศก — มี Mo-Mo Paradise, Shabu Lab, Suki Teenoi
ก่อนเข้าตลาด skincare niche ดู Mistine, Cute Press, Beauty Buffet เป็นยังไง
```

## Porter 5F แปลเป็นคำถามเถ้าแก่

| Force | Consulting-speak | คำถามเถ้าแก่ |
|---|---|---|
| Supplier power | "Bargaining power of suppliers" | พี่ซื้อวัตถุดิบจากใคร เปลี่ยน supplier ใน 3 เดือนได้ไหม |
| Buyer power | "Bargaining power of buyers" | ลูกค้า 5 รายแรกของพี่กินรายได้กี่ % |
| New entrants | "Threat of new entrants" | ถ้ามีคนทุน 2 ล้านอยากเข้าธุรกิจนี้พรุ่งนี้ ใช้เวลานานแค่ไหน |
| Substitutes | "Threat of substitutes" | ลูกค้าพี่ถ้าไม่ซื้อของพี่ จะไปซื้ออะไรแทน |
| Rivalry | "Industry rivalry" | คู่แข่ง 3 รายแรกพี่รู้จักไหม |

## ขั้นตอน

1. **ระบุ market ให้ชัด** — geography, category, channel, customer segment

2. **ระบุคู่แข่ง 3-5 ราย** — ขอ user ระบุ + แนะนำเพิ่ม

3. **ค้นงบในงบบริษัทคู่แข่งใน DBD**
   - ขั้นตอน:
     1. ไปที่ `datawarehouse.dbd.go.th/index`
     2. ค้นชื่อบริษัท (ถ้ารู้เลขทะเบียน 13 หลัก ใช้ตรง)
     3. คลิก "งบการเงิน" → เลือกปีล่าสุดที่มี
     4. Download PDF
   - **ดู 3 ตัวเลข**: รายได้รวม, กำไรขั้นต้น %, กำไรสุทธิ %
   - หมายเหตุ: บริษัทยื่นช้า 6-12 เดือนหลังปิดปีบัญชี

4. **Apply 5 Forces** — ตอบคำถามเถ้าแก่แต่ละข้อ + cite ตัวเลขที่ดึงได้

5. **คืน output**
   - **5 Force table** พร้อม intensity (Low/Med/High) + ข้อสังเกต
   - **Competitor financial snapshot** (table)
   - **3 strategic implications** สำหรับ user

## ตัวอย่าง

### Input
```
ก่อนเปิดร้าน specialty coffee ในทองหล่อ — ดูคู่แข่ง
Roots, Roast, Brave Roasters, % Arabica, Pacamara
```

### Output (sample)
```
## Competitor Scan — Specialty Coffee Bangkok (ทองหล่อ/เอกมัย area)

### Financial snapshot (from DBD, latest filing 2024)
| คู่แข่ง                | รายได้ (M฿) | GP% | Net% | สาขา (BKK) |
|----------------------|----------:|----:|----:|----------:|
| Roots Coffee Co. Ltd | 280       | 65% |  8% |       18  |
| Brave Roasters       | 95        | 60% |  4% |        6  |
| Roast (TH) Ltd       | 410       | 58% | 11% |       22  |
| % Arabica (Master Franchise) | n/a (private) | est 70%+ |  -  |     12  |
| Pacamara Coffee Roasters | 145   | 62% |  6% |        9  |

> ดึงจาก `datawarehouse.dbd.go.th` — แต่ละบริษัทใส่เลขทะเบียน 13 หลักเพื่อ verify

### 5 Forces

**Supplier power: MEDIUM**
- เมล็ดกาแฟ premium มี ~10 รายในไทย (Doi Tung, Doi Chaang, ฯลฯ) + import
- เปลี่ยน supplier ได้ใน 1-2 เดือน
- Coffee bean spot price ขยับตามตลาดโลก — risk
- ใช้ specialty roastery เอง (Roots, Brave, Pacamara, Roast) — vertically integrated, supplier power ต่ำกว่า

**Buyer power: LOW**
- ลูกค้า casual, transaction-based, no contracts
- AOV 80-180฿ — ไม่มีลูกค้ารายใหญ่
- แต่ "loyalty pool" สูง — ลูกค้าซ้ำ 65-75% ของ revenue

**New entrants: MEDIUM-HIGH**
- เงินทุน 2M สำหรับ 1 สาขา (รวม fit-out + เครื่องชง + เปิด 3 เดือน burn)
- คู่แข่ง 5 รายที่ระบุข้างบนเริ่มมีบาริสตา ไหลเข้า/ออก — เรียนรู้ recipes ไม่ยาก
- ★ Real moat ของ Roast, Roots: vertical roasting + brand
- ★ "ทองหล่อ" เต็มแล้ว — ที่ดี (corner, ground floor) เช่า 200-400k/เดือน

**Substitutes: HIGH**
- กาแฟกระดาษมือถือ (Amazon, Starbucks, All Cafe) ใกล้แค่ครึ่งกม.
- Specialty coffee at home (subscription roastery) เติบโต 35%/yr (BOT digital payment data 2025)
- Tea / matcha — Tea Cup, Matcha Lab ขายส่ง 110-180฿ ใกล้เคียง

**Rivalry: HIGH**
- 5 รายที่ระบุ + 8-12 รายเล็ก ในรัศมี 1 กม.
- GP% ของ public ones 58-65% — segment ราคา/คุณภาพ tight
- Net% 4-11% — margin บาง, รายใหญ่ที่สเกลเป็น 22 สาขา (Roast) ทำ 11% นั่นคือ ceiling

### 3 Strategic Implications

1. **ห้ามแข่ง Roast/Roots ที่ scale** — เขาทำ 22-18 สาขา net% 8-11% โดย vertical roastery, ทุน 100M+. ผู้เล่นใหม่ทุน 2M ต้อง niche
2. **เลือก niche แคบ**: micro-lot single-origin / hand-drip-only / specific origin (Thailand-only) — มาร์จิ้นสูงพอ scale ไม่ได้แต่ survive
3. **Substitute ใกล้กว่าคู่แข่ง specialty** — ลูกค้าใหม่ส่วนใหญ่เคยซื้อ Amazon (60฿) → เลือก positioning ว่า "อัปเกรดจาก mass coffee" ไม่ใช่ "ดีกว่า Roast"

### Disclaimer
DBD financials เป็นงบรวมบริษัท — ตัวเลข rev/profit ต่อสาขาคำนวนเอง (รวม ÷ จำนวนสาขา) เป็น proxy. บริษัทเอกชนปิดบางตัวเลขใน annual filing.
```

## DBD lookup walkthrough

```
1. ไปที่ datawarehouse.dbd.go.th/index
2. พิมพ์ชื่อบริษัท ใน "ค้นหาข้อมูลนิติบุคคล"
3. คลิก row → "ข้อมูลธุรกิจ"
4. Scroll → "งบการเงิน" → คลิกปีล่าสุด
5. Download PDF (1.2-2 MB ปกติ)
6. ดู:
   - หน้า 2: Income Statement (รายได้, ค่าใช้จ่าย, กำไร)
   - หน้า 3: Balance Sheet (สินทรัพย์, หนี้สิน, ทุน)
   - หน้า 4-6: Notes (รายละเอียดสำคัญ — สัญญาเช่า, contingent liabilities)
```

## Common mistakes

- เชื่อ press release ของคู่แข่ง — "เราโต 200%" ส่วนใหญ่เป็น marketing
- ใช้ Crunchbase / LinkedIn employee count เป็น proxy ของ revenue — ผิด 5-10x ใน TH
- ลืมว่างบ DBD ล่าสุดอาจล้าสมัย 12-18 เดือน
- ไม่ดู cash flow + accounts payable — รายได้ดูสวย แต่ working capital ติด

## ขอบเขต

- ใช้กับ "บริษัทจำกัด" (Ltd.) — ห้างหุ้นส่วน (Partnership) ไม่ต้องเปิดงบ public
- หจก. + sole proprietor ไม่อยู่ใน DBD — ต้องใช้ qual research แทน
- บริษัทต่างชาติ (BOI, branch office) อยู่ใน DBD แต่ format ต่าง

## แหล่งอ้างอิง

- DBD Data Warehouse — `datawarehouse.dbd.go.th`
- Porter, M.E. (1979) "How Competitive Forces Shape Strategy" — Harvard Business Review
