---
name: thai-sourcing-landed-cost
description: คำนวน landed cost ของสินค้าที่ import จาก 1688/Alibaba/global supplier — รวม import duty ตาม HS code, VAT 7% on CIF, flag FDA/TISI/มอก. registration requirement
when_to_use:
  - User mention "นำเข้า" / "import" / "1688" / "Alibaba" / "Taobao" / "ของจีน"
  - User ถาม "ราคาขึ้นเรือเท่าไหร่" / "landed cost"
  - User mention HS code, FDA, TISI, มอก., อย.
  - User สงสัยภาษีนำเข้าของหมวดใด
when_not_to_use:
  - คำถาม pricing ส่งออก — ไม่อยู่ในขอบเขต
  - คำถาม transfer pricing — ต้องคุยทนายภาษี
version: 0.1.0
last_verified: 2026-05-19
tier: validator
---

# Thai Sourcing — Landed Cost + Compliance Flag

ปัญหา: เถ้าแก่ดู 1688 เห็นราคา 180 หยวน → คูณ 5 ได้ "900 บาท" คิดว่าต้นทุนนี้. จริงๆ ต้องบวก: shipping (10-25% ของ CIF), import duty (ตาม HS code, อาจ 0-30%), VAT 7% on CIF + duty, ใบอนุญาตหมวด (FDA cosmetic ใช้เวลา 1-6 เดือน, TISI/มอก. electronics บังคับ).

`landed_cost.py` ทำ HS-based calculation + flag compliance ที่ต้องดำเนินการก่อน import.

## เมื่อ Claude เห็นคำขอแบบนี้

```
นำเข้าหูฟัง bluetooth จาก 1688 ราคา 180 หยวน/ชิ้น — landed cost ต่อชิ้นเท่าไหร่
สั่งครีมจากเกาหลี FOB 8 USD ต่อชิ้น — ต้องขึ้น อย. ไหม
```

## ขั้นตอน

1. **เก็บ input**
   - ราคา FOB / EXW (ต้นทาง) + สกุล
   - Shipping cost (รวมประกัน) — ถ้าไม่บอก default 12% ของ FOB
   - HS code / หมวดสินค้า (electronics / cosmetic / food / fashion / etc.)
   - จำนวนต่อ shipment

2. **ระบุ HS รหัสและ duty rate**
   - ถ้า user รู้ HS — ใช้ตรงๆ
   - ถ้าไม่รู้ — ดูจาก `hs_codes` lookup ใน `landed_cost.py` (มี common categories) หรือชี้ให้ดู `tariff.customs.go.th`

3. **เรียก `landed_cost.py`**
   ```python
   from landed_cost import compute_landed_cost, compliance_flags
   ```

4. **คืน output**
   - Cost breakdown per unit (FOB → CIF → +duty → +VAT)
   - Compliance flags (FDA / TISI / มอก. / etc.)
   - Estimated timeline ของ registration

5. **ข้อสังเกต**
   - ถ้า FDA flag → flag timeline 1-6 เดือน ห้าม import ก่อนได้ใบ
   - ถ้า TISI flag → ต้องมี มอก. หรือ ของส่งคืน
   - หมวด < 1,500฿/shipment ผ่าน CN22 อาจ duty-free แต่ commercial import ไม่ใช้ exemption นี้

## Common HS categories (built-in to `landed_cost.py`)

| หมวด | ตัวอย่าง HS | Duty rate 2026 | Compliance |
|---|---|---:|---|
| Cosmetics (skincare) | 3304 | 20% | **FDA registration บังคับ** (1-6 เดือน) |
| Food supplement | 2106 | 10-30% | **FDA registration + อย. label** |
| Electronics consumer | 8517, 8518 | 0-20% | **TISI/มอก. บางหมวด** (audio, charger) |
| Fashion clothing | 6109, 6204 | 20-30% | ไม่มี |
| Toys | 9503 | 0-20% | **TISI 685-2540** (บังคับ) |
| Books | 4901 | 0% | ไม่มี |
| Mobile accessories (case) | 3926 | 5-20% | ไม่มี |
| Sports equipment | 9506 | 0-20% | บางหมวด TISI |

> Duty rate ขยับตามประเทศต้นทาง (FTA): ASEAN = 0%, จีน FTA ลด 0-50%, USA = MFN rate

## ตัวอย่าง

### Input
```
นำเข้าหูฟัง bluetooth จาก 1688 ราคา 180 CNY/ชิ้น สั่ง 500 ชิ้น
shipping ทางบก 5,500 CNY ทั้ง batch
```

### Output
```
ต่อชิ้น:
  FOB: 180 CNY × 5.0 (rate 2026) = 900 ฿
  Shipping per unit: 5,500 / 500 × 5.0 = 55 ฿
  CIF (cost-insurance-freight): 955 ฿
  Import duty (HS 8518, audio, MFN 20%): 191 ฿
  VAT 7% on (CIF + duty): 80.22 ฿
  Total landed: 1,226 ฿/ชิ้น

Compliance flags:
  ⚠ TISI/มอก. — audio products หมวด 8518 บางรุ่นต้อง มอก.2274-2549 (อิเล็กทรอนิกส์เสียง)
  ⚠ Bluetooth → ต้อง NBTC type approval (กสทช.) สำหรับการแพร่คลื่น

Timeline ที่ต้องรู้:
  - มอก. ถ้าจำเป็น: 60-120 วัน ผ่านห้องแล็บที่ได้รับรอง
  - NBTC type approval: 30-60 วัน
```

## แหล่งอ้างอิง

- กรมศุลกากร — Tariff lookup: `tariff.customs.go.th`
- อย. — registration timeline: `fda.moph.go.th`
- TISI — รายการ มอก. บังคับ: `tisi.go.th`
- กสทช. — NBTC type approval: `nbtc.go.th`

## ข้อจำกัด

- HS code lookup ใน `landed_cost.py` เป็น common categories — ของแปลก/หมวดย่อย ต้องตรวจ tariff.customs.go.th ตรง
- Duty rate FTA (ASEAN, ACFTA, JTEPA, AKFTA) ต้องระบุ origin certificate (Form D, E, JT, AK) — ตัวเลขใน calculator ใช้ MFN rate (ไม่ใช้ FTA discount)
- ไม่รวม Customs broker fee + port handling — เพิ่ม 1,500-3,500฿ ต่อ shipment ปกติ
