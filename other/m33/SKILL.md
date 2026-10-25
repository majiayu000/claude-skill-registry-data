---
name: m33
description: Superagent skill m33 — Pre-TGE Alpha Radar (deteksi airdrop SEBELUM diumumkan)
category: superagent/trading
---

# m33 — Pre-TGE Alpha Radar (deteksi airdrop SEBELUM diumumkan)
# Load ONLY when: alpha airdrop, airdrop baru, proyek belum ada token, pre-TGE, points program, testnet incentivized, cari airdrop potensial, proyek worth difarming, radar airdrop, kandidat airdrop

---

## DOCTRINE — discovery, bukan eligibility
m31 jawab "wallet gue layak gak buat airdrop X?" — **m33 jawab "proyek mana yang worth difarming SEKARANG?"** sebelum token-nya ada. Ini alpha mentah: jualan utama komunitas.

Murni logika scoring (offline, deterministik). Pengumpulan sinyal mentah (funding, deploy kontrak, points program, GitHub, governance) didelegasi ke m6/m22/m10.

## TOOL (v4.2, net-new)
- `tools/alpha_radar.py` — `ProjectSignal` → `score_project()` → skor 0-100 + tier (cold/watch/warm/hot) + alasan konkret + estimasi effort. `rank(list)` urutkan banyak proyek.

## SINYAL YANG DINILAI
points program (paling kuat) · testnet incentivized · governance tanpa token · backing VC tier-1 · besar funding · momentum dev (commit/kontrak) · pertumbuhan sosial · timing TGE (6-18 bln sejak raise). **Token udah ada → skor di-cap 30** (peluang airdrop utama lewat).

## ALUR STANDAR
```python
from alpha_radar import ProjectSignal, rank
sigs = [ProjectSignal("ZkProtoX", funded_usd=30e6, points_program=True,
        testnet_live=True, github_commits_30d=80, backed_by_tier1=True,
        days_since_last_round=300, social_growth_pct=60)]
for r in rank(sigs, top=10):
    print(r.report())   # 📡 ZkProtoX: 78/100 (hot) · effort high
```

## SCOPE & DELEGATION
| Butuh | m33 | Delegasi |
|---|---|---|
| Data funding/sosial/GitHub | konsumsi `ProjectSignal` | m6 (API) / m22 (riset) |
| Aktivitas on-chain (deploy/testnet) | konsumsi sinyal | m10 + hermes |
| Cek wallet sendiri layak | — | m31 eligibility |
| Eksekusi farming | hasilkan watchlist | m30 + airdrop_runner (governor) |

## SAFETY RAILS
- Skor = **probabilitas + estimasi**, BUKAN jaminan ada airdrop/cuan. Sampaikan apa adanya.
- Effort tinggi = modal/waktu besar — pasangkan sama m34 (ROI) sebelum all-in.

🔧 Upgrade: combo m34 buat hitung ROI kandidat, m35 buat auto-bikin panduan begitu masuk tier hot.
