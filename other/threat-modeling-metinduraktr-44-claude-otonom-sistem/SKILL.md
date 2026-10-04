---
name: threat-modeling
description: "STRIDE/LINDDUN ASSESS threat model. Defense-only. Use for holding automation surfaces."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# threat-modeling

## Trigger
Threat model, STRIDE, saldırı yüzeyi ASSESS, DFD, risk önceliklendirme.

## Hybrid
`references/holding-stride.md` + `references/dfd-checklist.md`

## MODE
ASSESS-ONLY. Saldırı adımı / exploit senaryo detayı YASAK — tehdit **sınıfı** + **kontrol**.

## Procedure
1. Varlık listesi (`SECURITY_CONTEXT/`)
2. Trust boundary çiz
3. STRIDE satırları → kontrol motoru map
4. Risk: olasılık×etki (kaba) → P0–P2
5. Çıktıyı `SECURITY_RESEARCH/` veya assessment dosyasına yaz

## Output
Tablo: varlık | tehdit sınıfı | kontrol | öncelik

## Depth TODO
~20k hedef; kalan: LINDDUN privacy, abuse-case şablonları, diagram örnekleri.

## Depth status
Bu tur ~5030 karakter (SKILL+references). **Kalan ~20k hedefe:** ~14970. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
