---
name: apparel-logo-mockup
description: Bir fotoğraftaki tişört/kıyafet üzerine Projenic logosunu gerçekçi serigrafi baskı gibi uygular. Önce eski/sahte yazıyı IOPaint (LaMa) ile siler, sonra logoyu kumaş kıvrımına (displacement map), perspektife ve ışığa uydurur. "tişört mockup", "kıyafete logo bas", "üniformadaki logoyu düzelt" isteklerinde kullan.
---

# Kıyafet üzerine logo mockup

İki aşamalı, tekrarlanabilir bir işlem:

1. **Temizleme (IOPaint + LaMa, Apache-2.0):** Kumaştaki mevcut yazı/logonun maskesi otomatik çıkarılır
   (verilen kutu içinde parlak pikseller) ve LaMa modeliyle kumaş dokusu yeniden üretilir.
2. **Baskı (OpenCV):** Gerçek logo (`public/assets/images/logo-white.png`)
   - döndürme + perspektif (sırt eğimi) ile yerleştirilir,
   - kumaşın bulanıklaştırılmış parlaklığından türetilen **displacement map** ile kıvrımlara göre bükülür,
   - kumaşın ışığına göre gölgelenir (kıvrım tepeleri parlak, çukurlar koyu),
   - kumaş dokusu mürekkebin içinden hafifçe görünür, kenarlar 0,5 px yumuşatılır.

## Kurulum (proje dışı, bir kez)

```bash
uv venv --python 3.11 .mockup-venv
uv pip install --python .mockup-venv/bin/python iopaint opencv-python-headless numpy
```

## Kullanım

```bash
.mockup-venv/bin/python .claude/skills/apparel-logo-mockup/scripts/mockup.py \
  --image public/assets/images/atolye/atolye-prova-montaj.jpg \
  --erase-box 405,360,570,408 \
  --logo public/assets/images/logo-white.png \
  --center 487,388 --width 150 --rotate -1.5 --skew 0.04 \
  --out out/atolye-prova-montaj.jpg
```

- `--erase-box x1,y1,x2,y2`: silinecek eski yazının kutusu (birden çok kez verilebilir).
- `--center`, `--width`: logonun kumaş üzerindeki merkezi ve genişliği (px).
- `--rotate` (derece), `--skew` (yatay perspektif, ±0.1): sırtın duruşuna göre.
- `--strength`: kıvrım bükme şiddeti (varsayılan 3 px). `--ink`: mürekkep parlaklığı (0–255, varsayılan 228).
- `--debug-dir`: maske ve ara çıktıları kaydeder.

## Kalite kontrol

Sonucu %100 ve %300 yakınlaştırmada kontrol et: harfler kıvrımı takip etmeli, logo kumaştan parlak
"yapıştırma" gibi durmamalı, silinen bölgede leke/tekrar deseni kalmamalı. Gerekirse `--erase-box`'ı
genişlet ve tekrar çalıştır.
