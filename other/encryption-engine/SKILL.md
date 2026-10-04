---
name: encryption-engine
description: "TLS, key management, PQC agility (FIPS 203/204/205). Defense-only ENC controls."
---

# GUARDRAIL AKTİF — savunma-only, secret-redakte, exploit-yok

# encryption-engine

## Trigger
Şifreleme politikası, TLS, KMS/vault, PQC roadmap, ENC-xxx.

## Hybrid
`references/pqc-roadmap.md` + `references/tls-key-policy.md`

## MODE
ASSESS-ONLY. Weak-crypto kırma / downgrade saldırı tarifi YASAK.

## Procedure
1. Crypto envanteri (protokoller, kütüphaneler, key store)
2. TLS min sürüm politikası
3. PQC: FIPS 203/204/205 adoption ASSESS
4. ENC kontrolleri yaz
5. Tarama

## TODO
20k: algoritma allowlist tablosu, library sürüm matrisi, HNDL risk skorlama.

## Depth status
Bu tur ~4114 karakter (SKILL+references). **Kalan ~20k hedefe:** ~15886. Sonraki: ek kanonik özet + holding örnekleri (padding yok).
