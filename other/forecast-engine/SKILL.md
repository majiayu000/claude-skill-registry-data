---
name: forecast-engine
description: Günlük tahmin motoru — FORECASTS/{title}/, Brier kalibrasyonu, Tetlock pratikleri. Faz 9.
---

# Forecast Engine

## Instructions
1. `FORECASTS/{title}/YYYY-MM-DD.md` günlük dosya
2. Hedef 200 tahmin/gün — fazlı (tek günde tamamlanmaz)
3. Olasılıkla ifade; gerçekleşince Brier score
4. `FORECASTS/CALIBRATION.md` güncelle

**Hibrit:** `/tahmin` inline.

## Examples
- `FORECASTS/hq-ceo/2026-08-27.md` — seed 3 tahmin skeleton

## Performance Notes
- Cloud Agent + Automations ile zamanlı tetikleme

## Troubleshooting
- Kalibrasyon kötüleşirse recalibrate notu
