---
name: layers-engine
description: "Defense-in-depth layer controls (LAY-xxx). Network→identity→app→data. ASSESS-ONLY."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# layers-engine

## Trigger
Katmanlı savunma, defense-in-depth, LAY kontrol üretimi.

## Hybrid
`references/layer-model.md` + `references/control-template.md`

## MODE
ASSESS-ONLY. Batch üretim `/kontrol-uret` ile; exploit yok.

## Procedure
1. Katman seç (L0 Perimeter … L5 Data)
2. Holding varlık ile eşle
3. Kontrol yaz → `LAYERS/`
4. Matrix satırı
5. secret_scan + ethics_check

## TODO
20k: D3FEND teknik map derinliği, katman diyagram SVG/md, 100 kontrol tamamı (şimdi 001–020).

## Depth status
Bu tur ~3434 karakter (SKILL+references). **Kalan ~20k hedefe:** ~16566. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
