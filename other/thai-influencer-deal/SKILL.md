---
name: thai-influencer-deal
description: คำนวน net payout ของดีล KOL/KOC ที่ถูกกฎหมาย WHT ไทย (3% talent fee ในประเทศ, 5%/15% non-resident, affiliate revenue share หัก WHT แยก) — output รวมโครงสร้างสัญญา KOL ที่ใช้ได้จริง
when_to_use:
  - User mention "KOL", "KOC", "influencer", "อินฟลู", "ดีลค่าตัว"
  - User ถาม "หัก WHT เท่าไหร่" / "withholding tax" สำหรับ talent fee
  - User เปรียบเทียบ flat fee vs revenue share
  - User เตรียม contract กับ KOL
when_not_to_use:
  - คำถาม ROI ของแคมเปญ — ใช้ thai-unit-economics
  - WHT ของ employee salary — ใช้ thai-financial-projection
version: 0.1.0
last_verified: 2026-05-19
tier: validator
---

# Thai Influencer Deal — WHT-safe structure

ผมเคยทำเคสที่ client ดีลกับ KOL macro 800k/post โดยไม่หัก WHT — สรรพากรเรียกตรวจปีถัดมา ต้องจ่ายเองทั้งก้อน + เบี้ยปรับ 1.5x. เคสนั้นเสียเงิน 1.2M รวมเบี้ย.

`commission.py` ทำให้แน่ใจว่า output ของ Claude ระบุ WHT rate ถูกตามประเภท (talent fee / affiliate revenue share) และคำนวน net payout ที่ KOL จะได้รับจริง + total cost ที่ brand ต้องจ่าย.

## เมื่อ Claude เห็นคำขอแบบนี้

```
ดีลกับ KOL macro ค่าตัว 350k/โพสต์ + revenue share 10% — หัก WHT ยังไง
KOC nano รับเป็น product-only ราคา 800฿/โพสต์ ต้องหัก WHT ไหม
```

## ขั้นตอน

1. **เก็บ input**
   - ประเภทดีล — flat talent fee, affiliate revenue share, hybrid (มีทั้งสอง)
   - มูลค่าก่อน WHT (gross)
   - สัญชาติ + tax residence ของ KOL (ไทย / ต่างชาติ resident / non-resident)
   - VAT status (KOL จด VAT ไหม)

2. **เรียก `commission.py`**
   ```python
   from commission import compute_payout
   payout = compute_payout(
       talent_fee=D("350000"),
       affiliate_revenue=D("0"),
       gmv=D("3500000"),
       commission_rate=D("0.10"),
       residence="thai",
       kol_vat_registered=True,
   )
   ```

3. **คืน output 3 ตาราง**
   - **Cost breakdown** (brand pays)
   - **Net payout** (KOL receives)
   - **Tax filing** (ภงด.3 ที่ brand ยื่น)

4. **ข้อสังเกต**
   - ถ้า KOL จด VAT — brand ต้องจ่าย gross + 7% VAT แล้วเอา VAT มาเครดิตในภพ.30
   - ถ้า KOL ไม่จด VAT — brand จ่าย gross เฉยๆ ไม่มี VAT credit
   - product-only deals < 1,000฿ — โดยทั่วไปไม่ต้องหัก WHT (3% threshold) แต่ยังต้องบันทึก gift expense
   - affiliate revenue share ที่จ่ายเป็น % ของ GMV → เป็น "ค่าบริการ" ไม่ใช่ "ค่าจ้างทำของ" — WHT rate เหมือนกัน 3% ในประเทศ

## WHT rates 2026

| ประเภทผู้รับ | rate (อ้างอิงประมวลรัษฎากร) |
|---|---:|
| บุคคลธรรมดาในประเทศ (Thai PIT) | **3%** ของค่าบริการ/ค่าจ้าง |
| นิติบุคคลในประเทศ (ค่าบริการ) | **3%** |
| บุคคลธรรมดา non-resident (มาตรา 50 / DTA) | **5%** หรือ **15%** ตาม DTA |
| KOL จด VAT → brand ออกใบหัก ณ ที่จ่าย | 3% ของจำนวนก่อน VAT |

> **Threshold**: ค่าบริการ/ค่าจ้าง <1,000 บาท ต่อครั้งโดยทั่วไปไม่หัก แต่ถ้าจ่ายซ้ำให้ผู้รับเดียวกันรวมกันเกิน 1,000 ต้องหักย้อนหลัง.

## Common mistakes

- ลืมหัก 3% WHT — brand รับผิดชอบเองถ้าโดนตรวจ + เบี้ยปรับ
- หัก 5% สำหรับ Thai resident — สูงเกิน, 3% เท่านั้น
- รวม VAT 7% เข้ากับ talent fee แล้วหัก WHT 3% บน gross + VAT — ผิด, ต้องหัก 3% บน base ก่อน VAT
- ระบุใน contract ว่า "net of WHT" แต่ไม่ define ว่าใครออก — ตีความผิดกันทุกครั้ง
- affiliate revenue share จ่ายผ่าน marketplace (Shopee Affiliate) → marketplace อาจหักให้แล้ว แต่ไม่ออก 50ทวิ ทำให้ KOL claim credit ไม่ได้

## ขอบเขต

- ไม่ครอบ international contract (cross-border) ที่ต้องใช้ DTA
- ไม่ครอบ in-kind compensation (product-only) ที่มี FMV >1,000฿ — ปกติต้องบันทึกเป็น expense + ออก 50ทวิ
- Contract template ใน folder นี้เป็น starter — ทนายต้องตรวจก่อนเซ็น

## แหล่งอ้างอิง

- กรมสรรพากร — มาตรา 50: `rd.go.th/5937.html`
- กรมสรรพากร — มาตรา 70 (non-resident): `rd.go.th/3380.html`
- Tellscore — published rate cards
