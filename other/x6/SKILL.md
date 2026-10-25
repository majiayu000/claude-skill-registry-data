---
name: x6
description: Debug terstruktur 4-fase + loop hipotesis otomatis. x3 = pustaka pola error (cepat, lookup). x6 = metode buat bug yang gak ada di pustaka — yang aneh, intermittent, atau dalam. Load x6 saat x3 men
category: superagent/meta
---

# x6 — Systematic Debugging & Auto-Debug Loop (NEW in v4.1)

Debug terstruktur 4-fase + loop hipotesis otomatis. x3 = pustaka pola error (cepat, lookup). x6 = metode buat bug yang **gak ada di pustaka** — yang aneh, intermittent, atau dalam. Load x6 saat x3 mentok atau bug non-trivial.

---

## 4 fase (urut — jangan loncat ke Fix)

```
1. RCA        → Root Cause Analysis: reproduce → isolasi → cari akar, BUKAN gejala
2. PATTERN    → cocokin ke pola dikenal (x3 library, error sebelumnya di memory/x4)
3. HYPOTHESIS → rumuskan dugaan yang TESTABLE, ranking by likelihood × cheapness-to-test
4. FIX        → uji hipotesis #1; benar → patch + regression test (x5); salah → hipotesis #2
```

Anti-pattern fatal: langsung nebak fix tanpa reproduce. "Coba restart / tambah try-catch" tanpa tau akar = nutup gejala, bug balik lagi.

## Fase 1 — RCA

```
- Reproduce dulu. Gak bisa reproduce → kumpulkan kondisi (input, env, timing, state).
- Isolasi: bisect (komentari setengah / git bisect), minimal repro case.
- Tanya "kenapa" sampai akar: error X → karena Y → karena Z. Akar = Z, bukan X.
- Bukti, bukan tebakan: log, stack trace, state dump, KQL (m21), eth_call revert reason.
```

## Fase 2 — PATTERN

Cocokin ke yang udah dikenal sebelum mikir dari nol:
- Pustaka x3 (nonce too low, RPC timeout, duplicate webhook, dll).
- Memory/x4 — "error ini pernah ketemu?" (lesson reinforced).
- Gejala klasik: race (intermittent), off-by-one (boundary), stale cache (kadang benar kadang salah), env drift (jalan di lokal, gagal di prod).

## Fase 3 — HYPOTHESIS (inti auto-debug)

```python
from eval import variance   # reuse buat flaky bug
# Susun hipotesis sebagai pernyataan testable + cara uji termurah
hypotheses = [
  {"h":"RPC ankr rate-limit di burst", "test":"swap ke llamarpc, retry 20×", "cost":"low", "p":0.6},
  {"h":"nonce race antar wallet paralel", "test":"serialize 1 wallet, ulang", "cost":"low", "p":0.3},
  {"h":"gas estimate kurang saat spike", "test":"naikin buffer 2×, ulang", "cost":"med", "p":0.1},
]
# urut by p × (1/cost) → uji termurah-paling-mungkin dulu
```

Auto-debug loop:
```
WHILE bug belum terjelaskan:
  pick hipotesis dengan (likelihood × murah-diuji) tertinggi
  jalankan test → observasi
  konfirm → ke FIX
  bantah → buang, update prior hipotesis lain, lanjut
  semua habis → generate hipotesis baru dari bukti terbaru (jangan ngotot ke yang udah dibantah)
```

Untuk bug **intermittent**: pakai `variance()` (x5) — jalanin N kali, lihat distribusi mode kegagalan. Bug yang 2/10 muncul = sinyal race/timing/rate-limit.

## Fase 4 — FIX

```
- Fix akar, bukan gejala. Kalau cuma bisa gejala → tandai + log alasannya (jangan diam).
- Tambah regression test (x5 Eval) — bug yang sama gak boleh balik diam-diam.
- Reversible & operasional (RPC/retry/cache) → boleh auto-fix (x4 SAFE_AUTO_ACTIONS).
- Nyentuh skill/dana/rail → proposal (frozen-paths), operator acc + re-lock.
- Catat ke memory (x4): gejala → akar → fix. Next time jadi entry x3.
```

---

## Output ke operator

```
🔬 x6 mass-mint flaky (3/50 gagal "AlreadyMinted")
  RCA: gagal hanya di wallet yang udah mint epoch lalu — bukan bug, state on-chain
  HYP#1 (p .7): checker eligibility skip cache stale → CONFIRMED (cache 1h, mint 40m lalu)
  FIX: invalidate eligibility cache sebelum batch → regression test added (x5)
  auto-fix? NO (logic skill m13) → 📝 proposal ditulis
```

x6 = metode. Pustaka cepat tetap x3; bukti kuantitatif tetap x5; lesson disimpan x4.
