---
name: secret-hygiene
description: "Secret tarama, redaksiyon, vault pattern. Defense-only Security OS skill. Use for ASSESS-ONLY gap/control work."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# secret-hygiene

## Trigger
Secret tarama, redaksiyon, vault pattern, dry-run matris, CI log mask.

## Hybrid note
Skill yüklenmezse: bu dosya + `references/holding-secret-policy.md` + `references/scan-runbook.md`.

## MODE
**ASSESS-ONLY** varsayılan. Secret: `${VAR}` / `vault://` / `<REDACTED>`. Gerçek değer yazma/yazdırma YASAK.

## Procedure
1. `STATE.md` Security OS oku
2. Envanter: `SECURITY_CONTEXT/inventory.md` + `docs/SECRETS-DRYRUN-MATRISI.md`
3. Tarama: `python3 scripts/secret_scan.py <paths>`
4. Gap: konum+tip only; değer yok
5. Ethics: `python3 scripts/ethics_check.py <paths>`
6. AUDIT / BILGI tek satır

## Output contract
Türkçe sinyal · dosya yolu · GECTI|KALDI · 1 satır öğrenim

## Depth
`references/` — politika + runbook. **TODO ~20k:** vault sağlayıcı matrisleri, GHA mask örnekleri, false-positive katalog (kalan ~12k).

## Depth status
Bu tur ~5945 karakter (SKILL+references). **Kalan ~20k hedefe:** ~14055. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
