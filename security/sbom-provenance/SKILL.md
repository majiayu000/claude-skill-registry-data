---
name: sbom-provenance
description: "CycloneDX/SPDX/SLSA kanıt yolu. Defense-only Security OS skill. Use for ASSESS-ONLY gap/control work."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# sbom-provenance

## Trigger
CycloneDX/SPDX/SLSA kanıt yolu

## Hybrid note
Skill Cursor’da yüklenmezse: bu dosyayı oku + inline **Bölüm 9** prosedürünü uygula; uydurma 20k içerik üretme.

## MODE
Varsayılan **ASSESS-ONLY**. Exploit/PoC/phishing **YASAK**. Secret: `${VAR}` / `vault://` / `<REDACTED>`.

## Procedure (kısa)
1. `STATE.md` Security OS oku
2. Girdi: `SECURITY_CONTEXT/` + ilgili motor klasörü (`TRANSPARENT_CODE/`)
3. Çıktı: gap/kontrol stub veya assessment — savunma dili
4. `scripts/secret_scan.py` + `ethics_check.py` ile doğrula (ilgili yollar)
5. AUDIT / BILGI_TABANI tek satır

## Output contract
- Türkçe özet (sinyal)
- Dosya yolu
- Denetim: GECTI|KALDI
- Öğrenim 1 satır

## TODO (fazlı derinlik)
Hedef ~20k karakter referans; şimdi iskelet. Genişletme: `references/` altına kanonik standart özetleri (NIST/D3FEND/CIS) — kopyala-yapıştır exploit yok.
