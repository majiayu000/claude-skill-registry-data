---
name: thai-pricing-strategy
description: ตั้งราคาแบบ waterfall ที่หัก marketplace fee, payment gateway, shipping ของ Thai channels (Shopee/Lazada/TikTok Shop/LINE Shopping/หน้าร้าน) เพื่อให้ได้ margin จริงที่ user ต้องการ
when_to_use:
  - User บอก "ตั้งราคาขาย" / "คำนวนราคาขาย" / "pricing"
  - User บอก margin หรือกำไรขั้นต้นที่ต้องการ
  - User mention Shopee / Lazada / TikTok Shop / LINE Shopping / หน้าร้าน / multi-channel
  - User สงสัยว่า "ขายช่องไหนกำไรเท่าไหร่"
when_not_to_use:
  - คำถาม pricing strategy เชิงตลาด (luxury vs commodity, price anchoring) — ตอบตรงๆ ไม่ต้องใช้ calculator
  - คำถาม VAT pricing (VAT-inclusive vs exclusive) — ใช้ skill thai-financial-projection ถ้ามี
version: 0.1.0
last_verified: 2026-05-19
tier: validator
---

# Thai Pricing Strategy — Waterfall

ที่ปรึกษา SME ไทยพลาดบ่อยที่สุดในการตั้งราคาคือ: **"ต้นทุน × 2.5 = ราคาขาย"** โดยไม่หัก marketplace fee, payment gateway, packaging, shipping subsidy ของแต่ละช่อง. เปอร์เซนต์มาร์จิ้นจริงเหลือ 8-12% ไม่ใช่ 60% ที่คำนวนในใจ.

Skill นี้บังคับให้ Claude คำนวน waterfall ต่อช่อง โดยใช้ `pricing.py` ที่มี marketplace fees ปี 2026 baked in.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ต้นทุน 85 บาท ขายที่ Shopee Mall อยากได้ margin 35% — ตั้งราคาเท่าไหร่
ครีมหน้าใส cost 120 จะขายหลายช่อง อยากเทียบกำไรแต่ละ marketplace
```

## ขั้นตอน (Claude ทำตามนี้)

1. **เก็บ input**
   - COGS (ต้นทุนสินค้า ต่อชิ้น) — บังคับ
   - Packaging (ค่ากล่อง/ฉลาก ต่อชิ้น) — default 5-10฿
   - Shipping ที่จ่ายเอง (subsidy ที่ตลาดบังคับ — Shopee Mall อาจ 30-50฿) — default 0
   - Target margin (เป็น % — เช่น 0.30 สำหรับ 30%) — บังคับ
   - Channels ที่อยากขาย — default คือเสนอทุกช่อง

2. **เรียก `pricing.py`**
   ```python
   from pricing import required_price, CHANNELS
   for ch in chosen_channels:
       price = required_price(cogs, packaging, shipping_out, target_margin, ch)
   ```

3. **คืน output เป็นตาราง markdown**

   | ช่อง | ราคาขั้นต่ำ (฿) | กำไรขั้นต้น (฿) | margin |
   |---|---:|---:|---:|
   | Shopee Mall | ___ | ___ | 35% |
   | ...

4. **ข้อสังเกต (ไม่เกิน 3 ข้อ)**
   - ถ้า channel มี margin หายไปมากกว่า 15% เทียบหน้าร้าน — flag "channel นี้กินมาร์จิ้นเยอะ พิจารณาขายเฉพาะ slow-mover"
   - ถ้า target margin > 50% — flag "ตลาดไทยทั่วไป margin เกิน 50% หลัง fee คือ luxury / niche — แน่ใจไหม"
   - ถ้า COGS ต่ำเกินไป (<20฿) — flag "ราคาขายอาจดูถูกเกินจนลูกค้าไม่เชื่อถือ — ลอง price anchoring"

## ตัวอย่าง

### Input
```
ตั้งราคาครีมหน้าใส ต้นทุน 85 บาท packaging 8 อยากได้ margin 35%
ขายที่ Shopee Mall กับหน้าร้าน
```

### Output (sample)
```
| ช่อง           | ราคาขั้นต่ำ | กำไรขั้นต้น | margin |
|----------------|-----------:|-----------:|-------:|
| Shopee Mall    |    192฿    |     67฿    |  35%   |
| หน้าร้าน        |    194฿    |     68฿    |  35%   |

ข้อสังเกต:
- Shopee Mall กับหน้าร้านราคาต่างกัน <2฿ — ตั้งราคาเท่ากันได้ ไม่ต้อง multi-tier
- COGS 85฿ + packaging 8฿ = 93฿ ต้นทุนจริง; ที่ราคา 192฿ มาร์จิ้นจริงต่อชิ้นคือ ~67฿
- ถ้าโดน free shipping subsidy 30฿ บน Shopee → margin หลือ 19% ต้องบวกราคาขึ้นอีก 50฿
```

## Common mistakes ที่ Claude ทำ (ก่อนมี skill นี้)

- คิดราคา cost × markup โดยไม่หัก fee
- ลืม payment gateway / transaction fee
- ใช้ Shopee commission ของ US (10-15%) — TH อยู่ที่ 5-8%
- ไม่แยก Mall vs non-Mall — fee ต่างกัน 1-3%

## แหล่งอ้างอิง

- Shopee Seller Center TH — `seller.shopee.co.th/edu/category/130`
- Lazada Seller Center TH — `sellercenter.lazada.co.th/seller-center-fees`
- TikTok Shop Seller TH — `seller-th.tiktok.com/university`
- ดู `benchmarks.md` ใน folder นี้สำหรับตัวเลขปี 2026 ที่ baked เข้า `pricing.py`

## ข้อจำกัด

- Marketplace ปรับ fee บ่อย — `pricing.py` มี config ที่ด้านบน แก้ตรงๆ ได้ ไม่ต้อง refactor
- ไม่รวม VAT — ถ้า user ต้อง VAT-inclusive pricing ใช้ skill `thai-financial-projection`
- ไม่รวม credit term — ถ้าขาย wholesale credit 60 วัน ต้องคิด financing cost แยก (ดู `thai-cashflow-survival`)
