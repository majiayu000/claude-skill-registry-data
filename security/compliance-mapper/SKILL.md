---
name: compliance-mapper
description: "Map controls to NIST CSF 2.0, 800-53 R5, ISO 27001:2022, CIS v8.1, ASVS 5.0. Defense-only."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# compliance-mapper

## Trigger
Crosswalk, matris satırı, compliance pack, kanıt indeksi.

## Hybrid
`references/crosswalk-seed.md` + `references/evidence-index.md`

## MODE
ASSESS-ONLY. Ücretli standart metni kopyalama YOK — ID + URL + doğrulama yöntemi.

## Procedure
1. Kontrol ID al (LAY/FW/ENC/CHG/TC/COND)
2. `SECURITY_RESEARCH/standards-currency.md` sürüm teyit
3. Kolon doldur: CSF · 800-53 · ISO · CIS · OWASP/ASVS
4. `doğrulama_yöntemi` yaz (komut/gözlem)
5. Matrix + kanıt yolu güncelle

## Output
Tek satır crosswalk veya tablo; GECTI|KALDI

## TODO ~20k
SOC2 CC mapping, Tam CIS IG1 checklist, FedRAMP düşük profil ASSESS.

## Depth status
Bu tur ~4796 karakter (SKILL+references). **Kalan ~20k hedefe:** ~15204. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
