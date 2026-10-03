---
name: thai-unit-economics
description: คำนวน CAC / LTV / payback period ด้วย benchmark Thai marketing channels 2026 (Meta, TikTok, LINE OA push, KOC/nano/mid-tier KOL ของ Tellscore/AnyMind/MEDIA Z) — ไม่ใช้ตัวเลข US
when_to_use:
  - User บอก "CAC", "LTV", "ROAS", "payback"
  - User สงสัยว่า "ลงทุน ad ขนาดนี้คุ้มไหม"
  - User เปรียบเทียบ channels: Meta vs TikTok vs LINE OA vs KOL
  - User บอก "หา customer acquisition cost"
when_not_to_use:
  - คำถาม pure pricing (ไม่เกี่ยว acquisition) — ใช้ thai-pricing-strategy
  - คำถาม brand awareness / reach (ไม่เกี่ยว conversion) — ตอบตรงๆ
version: 0.1.0
last_verified: 2026-05-19
tier: validator
---

# Thai Unit Economics — CAC/LTV/Payback

ปัญหา: ที่ปรึกษาเอา benchmark SaaS US มาใช้กับ SME ไทยที่ขายของกินของใช้ — CAC ที่ Meta จริง TH 2026 ห่างจาก US 5-10x. payback period ของ Thai e-commerce ไม่ใช่ 18 เดือนแบบ SaaS แต่เป็น 1-4 transactions.

Skill นี้ใช้ `unit_econ.py` ที่มี Thai 2026 benchmarks baked in: CPM Meta TH (subdivided by category), TikTok TH, LINE OA push cost at scale, และ KOL fees ตามขนาด tier.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ลง ad Meta 30k/เดือน ขายเครื่องสำอาง ROAS เท่าไหร่ถึงคุ้ม
KOC nano 5k-50k followers ราคา 1,200 บาท/โพสต์ — net new 12 คน CAC เท่าไหร่
LTV ของลูกค้าร้านชาบู ซื้อซ้ำเดือนละครั้ง average 800฿
```

## ขั้นตอน (Claude ทำตามนี้)

1. **เก็บ input**
   - Channel — Meta / TikTok / LINE OA / KOL nano / KOL mid / KOL macro
   - Spend ต่อแคมเปญหรือเดือน
   - Conversion rate ของ user (ถ้ารู้) — ถ้าไม่รู้ ใช้ default ตาม channel
   - AOV (average order value)
   - Repeat purchase: ความถี่/เดือน + retention 12-เดือน
   - Gross margin หลังหัก channel fee

2. **เรียก `unit_econ.py`**
   ```python
   from unit_econ import cac, ltv, payback_periods
   ```

3. **คืน output 3 ส่วน**
   - **CAC** ต่อ channel
   - **LTV** = AOV × frequency × retention × gross margin
   - **Payback period** = CAC / (AOV × gross margin) — เป็นจำนวน transactions

4. **ข้อสังเกต**
   - LTV:CAC ratio < 3 → unhealthy, ต้องลดต้นทุน acquisition หรือเพิ่ม retention
   - Payback > 4 transactions → cash-flow trap สำหรับ SME (ต้องดู `thai-cashflow-survival`)
   - ถ้า single-channel เกิน 60% ของ acquisition → concentration risk

## ตัวอย่าง

### Input
```
แบรนด์ครีม cost 85 ขาย 250 หน้าร้าน + Shopee Mall
ลง Meta ads 30,000/เดือน
ลูกค้าซื้อซ้ำเฉลี่ย 1.4 ครั้ง/ปี (60% หายไปหลังครั้งแรก)
ตอนนี้ ad ได้ลูกค้าใหม่ ~38 คน/เดือน
```

### Output
```
CAC (Meta TH, beauty, 2026 benchmark): 30,000 / 38 = 789 บาท/คน
AOV: 250฿
Gross margin: (250 - 85 - fee 10%) / 250 = 60% → 150฿/คน
LTV: 150 × 1.4 ครั้ง = 210฿
LTV:CAC = 0.27 ← unhealthy (ควร > 3)

Payback: 789 / 150 = 5.3 transactions ← เกิน 4, ตึงมือสำหรับ SME

ข้อสังเกต:
- Meta CPM ปี 2026 หมวด beauty TH = 180-320฿/1000 impressions. CAC 789฿ อยู่ในช่วงปกติ แต่ LTV ต่ำเกินไป.
- 60% churn หลังครั้งแรกคือปัญหาใหญ่กว่า CAC — ลอง LINE OA broadcast เพื่อขาย batch 2 (cost ต่อ message ต่ำกว่า Meta 8-10x)
- ถ้าแบรนด์มี subscription / repeat tier ที่ดึง frequency เป็น 4-6 ครั้ง/ปี LTV:CAC จะกลายเป็น 1.1-1.6 ยังไม่ถึง 3 แต่ดีขึ้น
```

## Thai 2026 benchmarks (ใน `unit_econ.py`)

| Channel | Cost basis | TH 2026 typical |
|---|---|---|
| Meta (beauty/personal care) | CPM | 180-320฿/1000 imp |
| Meta (fashion) | CPM | 120-220฿/1000 imp |
| Meta (food delivery) | CPM | 80-180฿/1000 imp |
| TikTok Spark Ads (beauty) | CPM | 150-280฿ |
| TikTok Spark Ads (fashion) | CPM | 100-200฿ |
| LINE OA push (broadcast) | per message | 0.20-0.30฿/recipient |
| LINE OA push (rich menu trigger) | flat OA fee | 1,200-9,000฿/mo |
| KOC (nano, 5k-50k) | flat per post | 800-3,000฿ |
| KOL (micro, 50k-200k) | flat per post | 8,000-35,000฿ |
| KOL (mid, 200k-1M) | flat per post | 50,000-250,000฿ |
| KOL (macro, 1M+) | flat per post | 300,000-1,500,000฿ |

ดู `benchmarks.md` ใน folder นี้สำหรับ source.

## Common mistakes

- ใช้ Meta CPM US ($8-15) — TH ต่ำกว่าครึ่ง
- ลืม KOL post มี VAT 7% + WHT 3% ทำให้ total spend สูงกว่า nominal fee
- คำนวน LTV เป็น "อายุการเป็นลูกค้า" ตัวเลขดูสวยแต่ใน SME ไทยส่วนใหญ่ลูกค้า churn ใน 6-12 เดือน
- ลืมว่า KOC nano-tier บางครั้งรับเป็น product-only (ไม่ต้องจ่ายเงินสด) — ทำให้ CAC ดูถูกแต่ scale ไม่ได้

## ข้อจำกัด

- Benchmarks เป็น guide — actual CPM ของแบรนด์ใหม่จะสูงกว่า benchmark 2-3 เดือนแรก
- ไม่รวม organic / SEO / direct — ส่วนนี้ต้องคำนวนแยก
- KOL fees ขยับเร็ว — เช็คอัปเดตทุกครึ่งปีกับ Tellscore/AnyMind
