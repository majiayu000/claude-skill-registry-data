---
name: thai-channel-strategy
description: เลือก channel mix (LINE OA / FB Shop / Shopee Mall / Lazada / TikTok Shop / offline) ตามคุณสมบัติของ product (AOV, repeat rate, margin) — ไม่ใช่ "ขึ้น Shopee เลย" ที่ที่ปรึกษาทั่วไปแนะนำ
when_to_use:
  - User บอก "ขายช่องไหนดี", "channel strategy", "go-to-market"
  - User mention multi-channel decision
  - User เปรียบเทียบ marketplace
when_not_to_use:
  - User ต้องการ pricing ของแต่ละช่อง — ใช้ thai-pricing-strategy
  - User ต้องการ CAC ของช่อง — ใช้ thai-unit-economics
version: 0.1.0
last_verified: 2026-05-19
tier: reference
---

# Thai Channel Strategy — Mix decision matrix

ที่ปรึกษาส่วนใหญ่แนะนำ "ขึ้น Shopee เลย" หรือ "build website เอง" โดยไม่ดู product fit. จริงๆ แต่ละช่องมี **economics ต่างกันชัดเจน** ตาม AOV (average order value), repeat rate, และ margin ที่ตัวสินค้าเหลือให้.

## Channel economics 2026 (TH market)

| Channel | AOV ที่ตลาดเล่น | Conversion ของ traffic | Customer type | Fee | Best for |
|---|---|---|---|---|---|
| LINE OA (broadcast) | 800-3,000฿ | 8-15% (warm list) | Repeat / VIP | flat fee | High repeat, high margin, urgent push |
| FB Shop / Shop on FB | 500-1,500฿ | 3-6% | Intent + chat | 0% (just FB ads spend) | Mid-AOV, chat-commerce, female-skew |
| Shopee Mall | 200-800฿ | 1-3% | Cold / hunters | 9-10% | Low AOV, broad reach, price-comparable |
| Lazada Mall | 250-900฿ | 1-3% | Cold / older demo | 8-9% | Slightly older demographic, electronics |
| TikTok Shop | 80-300฿ | 0.5-2% (cold) / 3-7% (live) | Impulse | 4-7% | Low AOV, impulse buy, video-first |
| Own website (direct) | 600-3,500฿ | 0.5-2% (cold) | Brand-loyal | 2-3% (gateway only) | High AOV, brand-led, repeat |
| หน้าร้าน (offline) | depends | 30-60% (walk-in) | Walk-in / local | 0-2.5% | Localized, experiential, urgent |

## Decision rules of thumb

```
AOV < 200฿  → TikTok Shop (impulse, video-driven)
AOV 200-500฿ → Shopee Mall + Lazada (volume/comparison)
AOV 500-1,500฿ → FB Shop + LINE OA (intent + chat)
AOV > 1,500฿ → Direct website + LINE OA (brand-led)
AOV > 5,000฿ → Direct + offline appointment

Repeat rate >30% → LINE OA + email/owned channels
Repeat rate <10% → marketplace (capture transactions)
Margin headroom <20% → ไม่ควรขึ้น marketplace ที่หัก 9-10%
```

## เมื่อ Claude เห็นคำขอแบบนี้

```
ครีมหน้าใส AOV 350฿ ขายช่องไหนดี
มี product 2 ตัว: skincare 250฿ + serum 1,200฿ — strategy แยกหรือรวม
ร้านอาหารกลางเมือง ทำ delivery ผ่านอะไรดี
```

## ขั้นตอน

1. **เก็บ input**
   - Product description + AOV
   - Margin headroom (after COGS, packaging, shipping)
   - Repeat rate / frequency (รายเดือน / รายไตรมาส / ปีละครั้ง)
   - Target demographic (age, gender, income, geography)
   - Current channels และ % rev breakdown

2. **Apply decision matrix**

3. **คืน output**
   - **Recommended channel mix** with target % per channel
   - **Sequencing** — ขึ้นช่องไหนก่อน, ขึ้นช่องไหนหลัง
   - **3 ข้อสังเกต** — concentration risk, margin pressure, unique value per channel

## ตัวอย่าง

### Input
```
แบรนด์เครื่องสำอาง 3 ตัว: ครีมกลางวัน 320฿, ครีมตา 580฿, เซรั่ม 1,250฿
COGS 35%, packaging 8%, target margin 35% หลัง fee
ขายผ่าน IG + LINE OA + Shopee Mall อยู่แล้ว, รายได้รวม 280k/เดือน
แบ่ง: Shopee 65%, LINE OA 25%, IG DM/DA 10%
```

### Output (sample)
```
## Channel Recommendation

### ปัญหาที่เจอตอนนี้
- Shopee 65% = **concentration risk** (>60% threshold). ถ้า Shopee ปรับ commission 1.5% margin หาย 30-40%
- LINE OA แค่ 25% — ทั้งที่ AOV ของ portfolio ค่อนข้างสูง (320-1,250฿) ควรเป็น 35-45%
- IG DM 10% — มี customer interest แต่ conversion path ไม่ smooth (DM → quote → bank transfer)

### Recommended mix 12 months ข้างหน้า
| Channel | Target % | ทำไม |
|---|---:|---|
| LINE OA + LINE Shopping | 40% | AOV 580-1,250฿ ของ eye cream + serum เหมาะ chat-commerce; repeat 35% (skincare typical) |
| Shopee Mall | 35% | คงไว้สำหรับ cold acquisition + ครีมกลางวัน (AOV 320 เหมาะ marketplace) |
| FB Shop + IG Shopping | 15% | unify with content; conversion better than DM |
| TikTok Shop | 10% | เน้น live commerce ของครีมกลางวัน (AOV ในช่วงที่ TikTok เล่น) |

### Sequencing
- **เดือน 1-3**: เปิด LINE Shopping (ใช้ LINE OA list ที่มีอยู่), set up LINE Pay
- **เดือน 4-6**: ลง TikTok Shop, เริ่ม live commerce อย่างน้อย 2 ครั้ง/สัปดาห์
- **เดือน 7-9**: optimize Shopee Mall (อย่ายุติ) — ตั้งโฆษณา Shopee Search/Discovery เน้นครีมกลางวัน, ลด investment ของ serum/eye cream บน Shopee
- **เดือน 10-12**: scale LINE OA broadcast / retargeting

### 3 ข้อสังเกต
1. **AOV per channel ต้อง match** — ลอง list serum 1,250฿ บน Shopee Mall ลูกค้าจะเทียบกับยี่ห้อ 380-450฿ ที่มาก่อน, drop conversion. ใช้ Shopee สำหรับ entry product (320฿)
2. **Margin headroom** — Shopee Mall หัก ~10%, ครีมกลางวัน margin หลัง fee ที่ราคา 320 = ดูตัวเลขใน `thai-pricing-strategy`. ของ Serum 1,250฿ บน Shopee อาจไม่ทำ margin เป้าหมาย
3. **LINE OA broadcast cost** — ที่ 12,000+ subscribers ใช้ Standard tier 1,200฿/mo (15k msgs free). ถ้า broadcast 2x/week × 12,000 = 96,000 msgs/mo เกิน tier → upgrade Premium 9,000฿/mo (100k free) — economics ก้อน 3,000 ส่วนต่างคุ้มถ้า conversion >0.4%
```

## Common mistakes

- "ขึ้น Shopee เลย" สำหรับ AOV >1,000฿ — Shopee shoppers compare-shop, AOV ตลาด 300-800, premium product struggles
- "build website" สำหรับ AOV <500฿ — direct traffic ไม่ scale, CAC สูง
- ขึ้น TikTok Shop สำหรับ serum 1,500฿ — TikTok Shop AOV เฉลี่ย <300฿, conversion drop
- กระจาย channel ทุกที่พร้อมกัน — ดูทำ 5 ช่อง แต่ไม่ทำดีสักช่อง

## ขอบเขต

- ตัวเลข economics เป็น typical industry ranges — actual fit ขึ้นกับ brand, content, audience match
- ไม่รวม wholesale / B2B distribution
- ไม่รวม cross-border (Shopee SG/MY) — ดู separately

## แหล่งอ้างอิง

- ETDA E-Commerce Statistics 2025 — `etda.or.th`
- LINE OA Pricing — `linebizapi.line.me/shopping`
- Shopee/Lazada/TikTok Shop seller centers (links ใน `docs/sources.md`)
