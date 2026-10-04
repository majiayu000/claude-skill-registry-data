---
name: archive-loop
description: Kampanya/LATOS arşiv döngüsü — ARCHIVE manifest + READ→DELTA→DIFF→WRITE→DIGEST; audit zinciri.
---

# Archive Loop

## When to use
`/arsivle`, `/latos-arsivle`, `/latos-aylik-dongu` veya kampanya/kart kapanışı.

## Steps (Agency)
1. BRIEFS + SCENARIOS + CANVA_OPS + QA topla
2. `ARCHIVE/{YYYY-MM}/{slug}/` oluştur
3. manifest.md yaz
4. BILGI_TABANI + AUDIT_LOG satırı
5. STATE.md aktif iş sıfırla

## Steps (LATOS — additive)
1. Eski sürümü oku (READ)
2. Değişimi tespit et (DELTA)
3. Farkı hesapla (DIFF)
4. Yeni sürüm yaz (WRITE) — timestamp'li
5. Digest üret (DIGEST) → `MEMORY/`, `REPORTS/`
6. Snapshot: `ARCHIVE/YYYY-MM-DD_HHMM/` — silme yok

## Performance Notes
- İnsan onay: self-modification, reward hacking savunması
- Disk büyümesi → compress arşiv, silme yok
