---
name: talent-crm
description: Use when managing talent pipeline with candidate tracking, outreach automation,
  and interview scheduling. Use for recruiting CRM.
domain: sales
author: oyi77
license: Apache-2.0
subdomain: sales
tags:
- business-development
- crm
- pipeline
- revenue
- sales
- talent
version: 1.0.0
category: sales
---



# talent-crm
## When to Use

**Trigger phrases:**
- "talent crm"
- "Help me with talent crm"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


---
name: talent-crm
description: >
  BerkahKarya Talent Agency CRM — manage talent scouting, contracts, commissions,
  client deals, and performance analytics for Indonesian creator-affiliate campaigns.
  Covers TikTok, Instagram, YouTube. Niches: digital products, lifestyle, business,
  education. AI GM: Vilona. Owner: Coder $String$ (Paijo).
---

## Overview

BerkahKarya's Talent Agency division previously peaked at **IDR 5B/month** Shopee
affiliate revenue. This skill rebuilds that division with a structured CRM pipeline:
scout → onboard → contract → activate → track → pay → scale.

**Team:**
| Role | Person | Contact |
|------|--------|---------|
| AI GM / Orchestrator | Vilona | (AI) |
| Owner | Coder $String$ (Paijo) | @codergaboets |
| Ads Master | Veris | @alwayscuanbos |
| Ops Manager | Sony | (internal) |
| Trading Master | Nuno | @oens77 |

---

## 1. Talent Database

- Configure crm, domain, relevant, talent, this settings before first use


### Scouting Criteria (Minimum Bar)

| Platform | Min Followers | Min ER | Niche Fit |
|----------|--------------|--------|-----------|
| TikTok   | 10,000       | ≥ 3%   | ✅ Required |
| Instagram | 5,000       | ≥ 2%   | ✅ Required |
| YouTube  | 2,000 subs   | ≥ 4% (views/subs) | ✅ Required |

**Target Niches:**
- `digital_products` — online courses, ebooks, templates, SaaS
- `lifestyle` — daily vlog, OOTD, beauty, food
- `business` — entrepreneur, side hustle, finance tips
- `education` — tutorial, how-to, skill building, career

**Disqualifiers:**
- Fake/bought followers (check ratio spikes)
- Inactive >30 days
- Niche mismatch (pure gaming, pure politics)
- Prior brand conflicts with BerkahKarya clients

### Talent Profile Fields

```yaml
talent:
  id: "TLT-YYYYMMDD-###"
  name: ""
  username: ""                     # @handle
  platform: [tiktok, instagram, youtube]
  niche: [digital_products, lifestyle, business, education]
  followers: 0
  engagement_rate: 0.0             # percentage, e.g. 4.5
  avg_views_per_post: 0
  contact_wa: ""                   # WhatsApp number
  contact_ig_dm: ""
  contact_email: ""
  region: "Indonesia"
  city: ""                         # e.g. Jakarta, Surabaya, Bandung
  contract_status: draft           # draft | negotiating | signed | active | expired | churned
  commission_rate: 0.0             # percentage of deal value, e.g. 15.0
  monthly_revenue_idr: 0           # last 30 days revenue generated
  total_revenue_idr: 0             # all-time
  onboarded_at: ""                 # ISO date
  contract_expiry: ""              # ISO date
  notes: ""
  manager: ""                      # Vilona / Sony / Veris
```

### Talent Status Flow

```
PROSPECT → CONTACTED → NEGOTIATING → SIGNED → ACTIVE → RENEWAL / EXPIRED / CHURNED
```

---

## 2. Client Database

- Configure crm, domain, relevant, talent, this settings before first use


### Client Profile Fields

```yaml
client:
  id: "CLT-YYYYMMDD-###"
  company_name: ""
  pic_name: ""                     # Person In Charge
  pic_contact_wa: ""
  pic_contact_email: ""
  industry: ""                     # e.g. digital product, fashion, F&B
  deal_stage: prospecting          # prospecting | proposal | negotiating | closed_won | closed_lost | active | completed
  contract_value_idr: 0            # total deal value
  commission_to_talents_idr: 0     # portion allocated to talents
  agency_margin_idr: 0             # contract_value - commission_to_talents
  deliverables:
    - type: ""                     # e.g. TikTok video, IG reel, YouTube review
      quantity: 0
      platform: ""
      deadline: ""
      status: pending              # pending | in_progress | submitted | approved | rejected
  campaign_start: ""
  campaign_end: ""
  assigned_talents: []             # list of talent IDs
  assigned_manager: ""
  kpi_target_views: 0
  kpi_target_conversions: 0
  actual_views: 0
  actual_conversions: 0
  client_satisfaction_score: 0     # 1-10
  notes: ""
```

### Deal Stage Flow

```
PROSPECTING → PROPOSAL SENT → NEGOTIATING → CLOSED (WON/LOST) → ACTIVE → COMPLETED
```

---

## 3. Talent Scouting

- Configure crm, domain, relevant, talent, this settings before first use


### Search Process

**Step 1 — Define Campaign Requirements**
```
Campaign niche: [digital_products | lifestyle | business | education]
Platform: [tiktok | instagram | youtube]
Min followers: [10K | 50K | 100K | 500K | 1M+]
Budget range: IDR ___
Deliverables: ___ posts/videos in ___ days
```

**Step 2 — Source Channels**
- TikTok Creator Marketplace (Indonesia filter)
- Instagram brand search by hashtag: `#affiliateindonesia`, `#kontendigital`, `#jualdigital`
- YouTube search by topic + subscriber filter
- Internal talent database (`scripts/talent_scout.py`)
- Referrals from existing active talents
- Competitor agency rosters (reverse-engineer via hashtag tracking)

**Step 3 — Qualify (Manual or Scripted)**
Use `scripts/talent_scout.py` to score candidates:
```bash
python3 scripts/talent_scout.py \
  --niche digital_products \
  --platform tiktok \
  --min-followers 10000 \
  --min-er 3.0 \
  --output scouting_results.csv
```

**Step 4 — Shortlist & Prioritize**
Score formula:
```
Scout Score = (ER × 0.4) + (Niche Fit × 0.3) + (Content Quality × 0.2) + (Growth Rate × 0.1)
```
- ER: normalized 0-10 (10 = ER >10%)
- Niche Fit: 0 or 1 (manual assessment)
- Content Quality: 1-10 (manual)
- Growth Rate: % follower growth last 30 days, normalized 0-10

**Minimum Score to Proceed:** 6.0 / 10

**Step 5 — First Contact**
Use outreach templates in Section 7.

### Key Indonesian Hashtags to Monitor

**TikTok:**
`#affiliatetiktok`, `#digitalprodukindonesia`, `#jualbuku`, `#kursusdigital`,
`#tipsbisnisid`, `#penghasilantambahan`, `#kontenindonesia`

**Instagram:**
`#affiliateindonesia`, `#digitalmarketerindonesia`, `#jualdigital`,
`#edukasibisnis`, `#contentcreatorid`

**YouTube:**
Search: `"affiliate shopee Indonesia"`, `"jualan digital Indonesia"`,
`"bisnis online pemula Indonesia"`

---

## 4. Contract Lifecycle

- Configure crm, domain, relevant, talent, this settings before first use


### Stages & Actions

#### `DRAFT`
- Generate contract from template (see `references/contract_template.md`)
- Fill: talent name, niche, platform, deliverables, commission rate, payment terms
- Internal review by Vilona / Sony

#### `NEGOTIATE`
- Send draft via WhatsApp or email
- Track objections and counter-offers in notes field
- Max 3 negotiation rounds; escalate to Paijo if stalled

#### `SIGN`
- Collect signed contract (PDF via WhatsApp or email scan)
- Store in `contracts/{talent_id}_{date}_signed.pdf`
- Update `contract_status: signed`
- Set `onboarded_at` and `contract_expiry`

#### `ACTIVE`
- Talent receives campaign briefs
- Deliverables tracked per client deal
- Commission tracked per post/deal via `scripts/commission_calc.py`

#### `RENEWAL` (30 days before expiry)
- Auto-alert via Telegram notification
- Review performance (ROI, revenue generated)
- Negotiate new terms if applicable
- If top performer: offer improved commission (+2-5%)

#### `EXPIRY / CHURN`
- Update `contract_status: expired` or `churned`
- Log churn reason: `low_performance | personal | competitor | inactive | price`
- Trigger win-back template if churn within first 90 days

### Standard Contract Terms

```
Commission Rate:     10-20% of deal value (default: 15%)
Payment Cycle:       Monthly (payout by 5th of following month)
Exclusivity:         Non-exclusive (unless premium deal > IDR 50M)
Content Ownership:   Client owns content for 1 year post-publication
Minimum Deliverable: As per campaign brief
Early Termination:   30-day notice required
```

---

## 5. Commission Tracking

- Configure crm, domain, relevant, talent, this settings before first use


### Commission Structure

| Tier | Monthly Revenue Generated | Commission Rate |
|------|--------------------------|-----------------|
| Starter | < IDR 5M | 10% |
| Regular | IDR 5M – 20M | 15% |
| Pro | IDR 20M – 50M | 18% |
| Elite | > IDR 50M | 20% |

### Deal Commission Formula

```
deal_commission = deal_value × (commission_rate / 100)
talent_payout = deal_commission × talent_share  # talent_share default: 0.7
agency_margin = deal_commission × (1 - talent_share)
```

**Example:**
```
Client deal value:  IDR 10,000,000
Agency commission:  15% → IDR 1,500,000
Talent share:       70% → IDR 1,050,000
Agency margin:      30% → IDR 450,000
```

### Monthly Payout Calculation

Use `scripts/commission_calc.py`:
```bash
python3 scripts/commission_calc.py \
  --month 2026-03 \
  --output payout_march_2026.csv
```

Output columns:
```
talent_id | talent_name | deals_count | total_deal_value | commission_earned | payout_amount | payout_status
```

Payout statuses: `pending | approved | paid | disputed`

### Payout Schedule

```
1st–5th of month:    Compile commission report
6th–7th:             Talent review & dispute window
8th:                 Paijo approves payouts
10th:                Bank transfers executed (BCA / BRI / DANA / OVO)
```

---

## 6. Performance Analytics

- Configure crm, domain, relevant, talent, this settings before first use


### Talent KPIs

```yaml
talent_analytics:
  talent_id: ""
  period: "YYYY-MM"
  posts_published: 0
  total_views: 0
  total_clicks: 0
  total_conversions: 0
  revenue_generated_idr: 0
  commission_earned_idr: 0
  roi: 0.0                         # revenue / payout to talent
  content_quality_avg: 0.0         # 1-10 average from client ratings
  on_time_delivery_rate: 0.0       # % deliverables submitted on time
  client_satisfaction_avg: 0.0     # 1-10 average from clients
```

### Creator ROI Formula

```
creator_roi = revenue_generated / payout_to_talent

Example:
Revenue generated: IDR 50,000,000
Payout to talent:  IDR 3,000,000
ROI = 16.7x (excellent — keep, grow)

Threshold:
< 2x  → Review / consider offboarding
2-5x  → Standard performer
5-10x → Strong performer (priority campaigns)
>10x  → Elite (offer exclusivity deals)
```

### Client Satisfaction Tracking

After each campaign completion:
```
Survey (WhatsApp/form):
1. Content quality (1-10)
2. Talent professionalism (1-10)
3. Deliverable timeliness (1-10)
4. Results vs expectations (1-10)
5. Likelihood to rebook (1-10)

Average ≥ 8: ✅ Happy client → push for repeat deal
Average 6-7: ⚠️ Okay client → address friction points
Average < 6: 🚨 At-risk client → immediate Sony escalation
```

### Agency Revenue Dashboard

```
Monthly GMV:         Total client deal values signed that month
Active Campaign GMV: Total deal value currently in-flight
Commission Revenue:  Agency margin accumulated
Pipeline Value:      Deals in prospecting + proposal + negotiating stages
Talent Count:        Active signed talents
Client Count:        Active campaigns
Avg Deal Size:       Total GMV / deals count
```

---

## 7. Outreach Templates

Reusable templates for talent-crm.

Standard config:
```yaml
name: talent-crm_standard
mode: production
output: results/
format: json
```

Test config:
```yaml
name: talent-crm_test
mode: development
dry_run: true
verbose: true
```


### Template 1: Standard talent-crm
```yaml
name: talent-crm_standard
mode: production
output: results/
format: json
```

### Template 2: Quick Test
```yaml
name: talent-crm_test
mode: development
dry_run: true
verbose: true
```


### 7.1 Initial DM to Creator (TikTok/IG)

**Indonesian — Short Version:**
```
Halo [Nama Creator]! 👋

Saya [Nama] dari BerkahKarya Talent Agency.

Kami notice konten [niche] kamu di [platform] — bagus banget, engagement-nya solid!

Kami lagi nyariin kreator untuk campaign [produk digital / lifestyle / bisnis] 
dengan brand-brand pilihan. Rate komisi kompetitif (10-20% per deal).

Tertarik diajak ngobrol 15 menit soal peluangnya? 

Balas DM ini atau WA: [nomor Sony/Vilona]

Cheers,
[Nama] | BerkahKarya Talent Agency
```

**Indonesian — Full Version (for email):**
```
Subject: Kolaborasi Talent Agency — BerkahKarya x [Username Creator]

Halo [Nama Creator],

Perkenalkan, saya [Nama] dari tim BerkahKarya Talent Agency.

Kami adalah talent agency yang fokus menghubungkan kreator konten Indonesia 
dengan brand-brand digital berkualitas. Klien kami bergerak di niche digital 
products, lifestyle, bisnis, dan edukasi.

Kenapa kami tertarik dengan kamu:
✅ Engagement rate [X%] — di atas rata-rata industri
✅ Niche [digital/lifestyle/bisnis/edukasi] — sangat relevan dengan klien kami
✅ Konten berkualitas dengan audiens yang engaged

Yang kami tawarkan:
💰 Komisi 10-20% per deal (bergantung performa & tier)
📋 Campaign management penuh dari kami — kamu fokus bikin konten
🚀 Akses ke brand-brand premium Indonesia
📊 Monthly report performa & payout rutin setiap bulan

Tidak ada eksklusivitas (kamu bebas kolaborasi dengan brand lain).

Kami hanya butuh 15 menit call untuk kenalan dan jelaskan sistemnya.

Bisa kita set up? Balas email ini atau WA ke: [nomor]

Salam,
[Nama] | BerkahKarya Talent Agency
[email] | [wa]
```

### 7.2 Follow-up DM (Day 3, no reply)

```
Halo [Nama] 👋 Just checking — sempet lihat DM saya sebelumnya?

Kalau timing-nya belum pas, no worries. 
Kalau ada pertanyaan atau mau tahu lebih lanjut, tinggal balas aja ya!

BerkahKarya | Talent Agency
```

### 7.3 Client Proposal Template

```
PROPOSAL KAMPANYE KONTEN
BerkahKarya Talent Agency

---
KLIEN:          [Nama Brand]
TANGGAL:        [Tanggal]
CAMPAIGN:       [Nama Campaign]
PERIODE:        [Tanggal Mulai] – [Tanggal Selesai]
---

OVERVIEW
BerkahKarya menyediakan kreator konten terseleksi untuk campaign [brand].
Kami memiliki [X] talents aktif dengan total reach [X juta] followers di 
TikTok, Instagram, dan YouTube.

TALENT YANG DIREKOMENDASIKAN
| No | Nama | Platform | Followers | ER | Niche |
|----|------|----------|-----------|-----|-------|
| 1  | ...  | TikTok   | 50K       | 5% | Bisnis |
| 2  | ...  | IG       | 30K       | 4% | Digital |

DELIVERABLES
| Platform | Tipe Konten | Jumlah | Timeline |
|----------|-------------|--------|----------|
| TikTok   | Video (60s) | 3      | 7 hari   |
| Instagram | Reels (30s)| 2      | 7 hari   |

INVESTASI
Package [X]:         IDR [nilai]
- Includes: [deliverables]
- Excludes: paid promotion (optional add-on)

TIMELINE
Day 1-2:    Brief & approval konten
Day 3-5:    Produksi konten
Day 6:      Review & revisi
Day 7:      Publish

TERMS
- DP 50% sebelum produksi
- Pelunasan 50% setelah konten diapprove
- Revisi: 2x per konten
- Konten copyright 1 tahun untuk [Brand]

[Tanda tangan / digital signature]
Vilona | AI GM, BerkahKarya Talent Agency
```

---

## 8. Integration

- Configure crm, domain, relevant, talent, this settings before first use


### 8.1 Telegram Notifications (telegram-userbot)

Configure alerts for:

```python
# Notification triggers (add to scripts/commission_calc.py and talent_scout.py)

NOTIFICATIONS = {
    "new_talent_signed": "🎉 New talent signed: {name} ({platform}, {followers} followers)",
    "contract_expiring": "⚠️ Contract expiring in 30 days: {name} — Renewal check needed",
    "contract_expired": "🚨 Contract EXPIRED: {name} — Update status immediately",
    "payout_ready": "💰 Monthly payout ready for approval — {count} talents, total IDR {amount}",
    "client_deal_closed": "✅ Deal closed: {client} — IDR {value} | Assigned talents: {talents}",
    "low_performance_alert": "📉 Low ROI alert: {name} — ROI {roi}x (below 2x threshold)",
    "new_prospect_scored": "🔍 New talent prospect scored: {name} — Score {score}/10",
}

TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Set in env or config.json
```

Send via:
```bash
# Using openclaw message tool (in skill context)
# Or via telegram-userbot CLI if configured
python3 scripts/notify_telegram.py --event new_talent_signed --data '{"name": "Creator X"}'
```

### 8.2 Notion Database (Primary CRM)

**Recommended Notion Setup:**
```
Database 1: Talents
  - All talent profile fields (see Section 1)
  - Views: All | Active | By Niche | By Platform | Expiring Soon

Database 2: Clients
  - All client profile fields (see Section 2)
  - Views: Pipeline | Active Campaigns | By Deal Stage

Database 3: Deals
  - Links: Talent(s) + Client
  - Fields: deal_value, commission, status, deliverables

Database 4: Payouts
  - Monthly payout records per talent
  - Status: pending | approved | paid

Automations:
  - Contract expiry → remind 30 days before
  - New deal closed → create deliverables checklist
  - Monthly trigger → generate payout draft
```

### 8.3 Google Sheets (Backup / Reporting)

Export monthly reports:
```bash
python3 scripts/commission_calc.py --month 2026-03 --format sheets
# Outputs: payout_2026-03.csv → manual upload to Google Sheets
```

**Recommended Sheets:**
```
Sheet 1: Talents Master List
Sheet 2: Clients Master List
Sheet 3: Monthly Commission Report
Sheet 4: KPI Dashboard (auto-calculated)
```

---

## 9. Scripts

- Configure crm, domain, relevant, talent, this settings before first use


### `scripts/talent_scout.py`

**Purpose:** Search and score talent candidates by niche, platform, followers, and engagement rate.

```python
#!/usr/bin/env python3
"""
talent_scout.py — BerkahKarya Talent Agency
Scores and filters talent candidates from CSV/JSON input or manual entry.

Usage:
  python3 scripts/talent_scout.py --niche digital_products --platform tiktok \
    --min-followers 10000 --min-er 3.0 --input prospects.csv --output shortlist.csv

Input CSV columns:
  name, username, platform, niche, followers, engagement_rate,
  avg_views, contact_wa, contact_ig, region, notes
"""

import argparse
import csv
import json
import sys
from datetime import datetime

NICHES = ["digital_products", "lifestyle", "business", "education"]
PLATFORMS = ["tiktok", "instagram", "youtube"]

PLATFORM_THRESHOLDS = {
    "tiktok":    {"min_followers": 10000, "min_er": 3.0},
    "instagram": {"min_followers": 5000,  "min_er": 2.0},
    "youtube":   {"min_followers": 2000,  "min_er": 4.0},
}


def normalize_er(er: float) -> float:
    """Normalize ER to 0-10 scale. ER >= 10% = 10."""
    return min(er, 10.0)


def score_talent(row: dict, niche_filter: str = None) -> dict:
    """Calculate scout score for a talent row."""
    platform = row.get("platform", "").lower()
    er = float(row.get("engagement_rate", 0))
    niche = row.get("niche", "").lower()
    followers = int(row.get("followers", 0))
    growth_rate = float(row.get("growth_rate_30d", 0))  # optional

    # Niche fit
    niche_fit = 1 if (niche_filter is None or niche == niche_filter) else 0

    # Content quality — default 7 if not provided (manual override encouraged)
    content_quality = float(row.get("content_quality", 7))

    # Scout score
    er_score = normalize_er(er)
    growth_score = min(growth_rate, 10.0)
    scout_score = (er_score * 0.4) + (niche_fit * 10 * 0.3) + (content_quality * 0.2) + (growth_score * 0.1)

    # Tier
    if followers >= 1_000_000:
        tier = "mega"
    elif followers >= 100_000:
        tier = "macro"
    elif followers >= 50_000:
        tier = "mid"
    elif followers >= 10_000:
        tier = "micro"
    else:
        tier = "nano"

    # Platform minimum check
    thresholds = PLATFORM_THRESHOLDS.get(platform, {})
    meets_minimum = (
        followers >= thresholds.get("min_followers", 0) and
        er >= thresholds.get("min_er", 0)
    )

    return {
        **row,
        "tier": tier,
        "niche_fit": niche_fit,
        "scout_score": round(scout_score, 2),
        "meets_minimum": meets_minimum,
        "qualified": meets_minimum and scout_score >= 6.0,
        "scored_at": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="BerkahKarya Talent Scout")
    parser.add_argument("--niche", choices=NICHES, help="Filter by niche")
    parser.add_argument("--platform", choices=PLATFORMS, help="Filter by platform")
    parser.add_argument("--min-followers", type=int, default=0)
    parser.add_argument("--min-er", type=float, default=0.0)
    parser.add_argument("--min-score", type=float, default=6.0)
    parser.add_argument("--input", "-i", help="Input CSV file (optional)")
    parser.add_argument("--output", "-o", default="shortlist.csv", help="Output CSV file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    rows = []

    # Load from file or stdin
    if args.input:
        with open(args.input, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    elif not sys.stdin.isatty():
        rows = list(csv.DictReader(sys.stdin))
    else:
        print("No input file provided. Run with --input prospects.csv")
        print("Or pipe CSV data via stdin.")
        sys.exit(1)

    # Score all rows
    scored = [score_talent(r, args.niche) for r in rows]

    # Apply filters
    filtered = [
        r for r in scored
        if r["qualified"]
        and int(r.get("followers", 0)) >= args.min_followers
        and float(r.get("engagement_rate", 0)) >= args.min_er
        and r["scout_score"] >= args.min_score
        and (args.platform is None or r.get("platform", "").lower() == args.platform)
    ]

    # Sort by score descending
    filtered.sort(key=lambda x: x["scout_score"], reverse=True)

    print(f"\n✅ Qualified talents: {len(filtered)} / {len(scored)} candidates")
    print(f"   Min score: {args.min_score} | Niche: {args.niche or 'all'} | Platform: {args.platform or 'all'}")

    for r in filtered[:10]:
        print(f"   [{r['scout_score']:.1f}] {r.get('name','?')} (@{r.get('username','?')}) "
              f"— {r.get('platform','?')} | {r.get('followers',0):,} followers | ER {r.get('engagement_rate',0)}%")

    if args.json:
        with open(args.output.replace(".csv", ".json"), "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON output: {args.output.replace('.csv', '.json')}")
    else:
        if filtered:
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=filtered[0].keys())
                writer.writeheader()
                writer.writerows(filtered)
            print(f"\n📄 CSV output: {args.output}")


if __name__ == "__main__":
    main()
```

---

### `scripts/commission_calc.py`

**Purpose:** Calculate monthly commission payouts for all active talents.

```python
#!/usr/bin/env python3
"""
commission_calc.py — BerkahKarya Talent Agency
Calculates monthly commission payouts from deals data.

Usage:
  python3 scripts/commission_calc.py --month 2026-03 --input deals.csv --output payout.csv
  python3 scripts/commission_calc.py --month 2026-03 --format sheets

Input CSV columns (deals.csv):
  deal_id, talent_id, talent_name, client_name, deal_value_idr,
  commission_rate, talent_share, deal_date, status

Status filter: only processes status = 'completed' or 'approved'
"""

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime


TALENT_SHARE_DEFAULT = 0.70   # 70% of commission goes to talent
AGENCY_SHARE_DEFAULT = 0.30   # 30% stays with BerkahKarya

TIER_THRESHOLDS = [
    (50_000_000, "elite",   0.20),
    (20_000_000, "pro",     0.18),
    (5_000_000,  "regular", 0.15),
    (0,          "starter", 0.10),
]


def get_tier(monthly_revenue: float) -> tuple:
    for threshold, tier, rate in TIER_THRESHOLDS:
        if monthly_revenue >= threshold:
            return tier, rate
    return "starter", 0.10


def calc_payout(deal: dict) -> dict:
    deal_value = float(deal.get("deal_value_idr", 0))
    commission_rate = float(deal.get("commission_rate", 15)) / 100
    talent_share = float(deal.get("talent_share", TALENT_SHARE_DEFAULT))

    deal_commission = deal_value * commission_rate
    talent_payout = deal_commission * talent_share
    agency_margin = deal_commission * (1 - talent_share)

    return {
        **deal,
        "deal_commission_idr": round(deal_commission),
        "talent_payout_idr": round(talent_payout),
        "agency_margin_idr": round(agency_margin),
    }


def main():
    parser = argparse.ArgumentParser(description="BerkahKarya Commission Calculator")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    parser.add_argument("--input", "-i", default="deals.csv")
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--format", choices=["csv", "json", "sheets"], default="csv")
    parser.add_argument("--notify", action="store_true", help="Send Telegram notification on completion")
    args = parser.parse_args()

    output_file = args.output or f"payout_{args.month}.csv"

    # Load deals
    try:
        with open(args.input, newline="", encoding="utf-8") as f:
            deals = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"❌ Input file not found: {args.input}")
        print("   Create deals.csv with columns: deal_id, talent_id, talent_name,")
        print("   client_name, deal_value_idr, commission_rate, talent_share, deal_date, status")
        return

    # Filter by month and valid status
    valid_statuses = {"completed", "approved", "paid"}
    month_deals = [
        d for d in deals
        if d.get("deal_date", "").startswith(args.month)
        and d.get("status", "").lower() in valid_statuses
    ]

    print(f"\n📊 Commission Report — {args.month}")
    print(f"   Total deals loaded: {len(deals)} | This month (valid): {len(month_deals)}")

    # Calculate per deal
    calculated = [calc_payout(d) for d in month_deals]

    # Aggregate by talent
    talent_summary = defaultdict(lambda: {
        "talent_id": "",
        "talent_name": "",
        "deals_count": 0,
        "total_deal_value_idr": 0,
        "total_commission_idr": 0,
        "payout_amount_idr": 0,
        "agency_margin_idr": 0,
        "payout_status": "pending",
    })

    for deal in calculated:
        tid = deal["talent_id"]
        talent_summary[tid]["talent_id"] = tid
        talent_summary[tid]["talent_name"] = deal.get("talent_name", "")
        talent_summary[tid]["deals_count"] += 1
        talent_summary[tid]["total_deal_value_idr"] += float(deal.get("deal_value_idr", 0))
        talent_summary[tid]["total_commission_idr"] += deal["deal_commission_idr"]
        talent_summary[tid]["payout_amount_idr"] += deal["talent_payout_idr"]
        talent_summary[tid]["agency_margin_idr"] += deal["agency_margin_idr"]

    # Apply tier upgrade
    for tid, summary in talent_summary.items():
        tier, _ = get_tier(summary["total_deal_value_idr"])
        summary["tier"] = tier

    summaries = list(talent_summary.values())
    summaries.sort(key=lambda x: x["payout_amount_idr"], reverse=True)

    # Print summary
    total_payout = sum(s["payout_amount_idr"] for s in summaries)
    total_margin = sum(s["agency_margin_idr"] for s in summaries)
    total_gmv = sum(s["total_deal_value_idr"] for s in summaries)

    print(f"\n{'='*60}")
    print(f"  MONTHLY GMV:            IDR {total_gmv:>15,.0f}")
    print(f"  Total Talent Payouts:   IDR {total_payout:>15,.0f}")
    print(f"  Agency Margin:          IDR {total_margin:>15,.0f}")
    print(f"  Talents to Pay:         {len(summaries)}")
    print(f"{'='*60}")

    for s in summaries:
        print(f"  [{s['tier'].upper():8}] {s['talent_name']:<25} "
              f"{s['deals_count']} deals | "
              f"IDR {s['payout_amount_idr']:>12,.0f}")

    # Export
    if summaries:
        if args.format in ("csv", "sheets"):
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=summaries[0].keys())
                writer.writeheader()
                writer.writerows(summaries)
            print(f"\n📄 Payout report: {output_file}")

        elif args.format == "json":
            json_file = output_file.replace(".csv", ".json")
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump({
                    "month": args.month,
                    "generated_at": datetime.now().isoformat(),
                    "summary": {
                        "total_gmv_idr": total_gmv,
                        "total_payout_idr": total_payout,
                        "agency_margin_idr": total_margin,
                        "talents_count": len(summaries),
                    },
                    "payouts": summaries,
                }, f, ensure_ascii=False, indent=2)
            print(f"\n📄 JSON payout report: {json_file}")

    if args.notify:
        print(f"\n📲 [Telegram] Payout ready for {args.month}: "
              f"{len(summaries)} talents | IDR {total_payout:,.0f} total")
        # TODO: integrate telegram-userbot notification here


if __name__ == "__main__":
    main()
```

---

## 10. KPIs

- Configure crm, domain, relevant, talent, this settings before first use


### Primary KPIs (Monthly)

| KPI | Formula | Target (Month 1) | Target (Month 6) |
|-----|---------|-----------------|-----------------|
| **Talents Signed** | Count (status=signed+active) | 5 | 50 |
| **Active Clients** | Count (deal_stage=active) | 2 | 20 |
| **Monthly GMV** | Sum of active deal values | IDR 50M | IDR 500M |
| **Commission Revenue** | Agency margin total | IDR 7.5M | IDR 75M |
| **Talent ROI Avg** | Avg(revenue/payout) | 5x | 8x |
| **Client Satisfaction** | Avg post-campaign score | 7.5 | 8.5 |
| **Contract Renewal Rate** | Renewals / Expiries | 60% | 80% |
| **Time to First Deal** | Days from sign to first active deal | 14 | 7 |

### Secondary KPIs

| KPI | Description |
|-----|-------------|
| **Pipeline Value** | Total deal value in prospecting + proposal + negotiating |
| **Conversion Rate** | Prospects contacted → talents signed (target: 20%) |
| **Avg Deal Size** | Total GMV / deals count |
| **Churn Rate** | Churned talents / total talents |
| **Content Delivery Rate** | % deliverables submitted on time |
| **Revenue per Talent** | Monthly GMV / active talent count |

### KPI Review Cadence

```
Daily:    Check new prospects scored, deals closed
Weekly:   Pipeline review (Sony), active campaign status
Monthly:  Full KPI report (Vilona → Paijo), payout execution
Quarterly: Strategy review, tier adjustments, churn analysis
```

---

## 11. Quick Reference — Workflow Summary

```
SCOUT        → talent_scout.py → shortlist.csv
OUTREACH     → DM template → WhatsApp/IG
ONBOARD      → contract_template.md → sign → update DB
CAMPAIGN     → brief → produce → review → publish
TRACK        → commission_calc.py → monthly payout.csv
PAY          → approve → transfer → mark paid
ANALYZE      → ROI, satisfaction score, renewal decision
SCALE        → top performers → more campaigns → tier upgrade
```

---

## 12. File Structure

```
skills/1ai-skills/sales/talent-crm/
├── SKILL.md                          ← This file
├── scripts/
│   ├── talent_scout.py               ← Scout & score candidates
│   └── commission_calc.py            ← Monthly payout calculator
└── references/
    ├── contract_template.md          ← Standard contract (fill per talent)
    ├── prospect_template.csv         ← Empty CSV for data entry
    └── deals_template.csv            ← Empty CSV for deals tracking
```

---

*BerkahKarya Talent Agency — rebuild, scale, dominate. 🔥*
*Last updated: 2026-03-13 | AI GM: Vilona*

## How to Use

1. Define ideal customer profile (ICP) and buyer personas
2. Build lead list from qualified sources
3. Craft personalized outreach sequences
4. Track engagement and follow up on signals
5. Qualify leads through discovery calls
6. Present solution tailored to pain points
7. Handle objections with value reframing
8. Close and hand off to onboarding

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Lead response time > 5 minutes**: Conversion drops 80% after 5 min. Automate instant response.
- **Pipeline has stale deals**: Deals stuck 30+ days need re-qualification or disqualification.
- **Low email reply rates (<3%)**: Messaging is too generic. Personalize with research.
- **High churn in first 90 days**: Onboarding gap. Fix handoff from sales to success.
- **Discounting above 20%**: Value perception problem. Reframe ROI, don't cut price.

## Verification

- Test email sequences with seed accounts before full send
- Verify CRM data integrity (no duplicates, correct stages)
- Check lead scoring model against actual conversion data
- Confirm proposal/contract templates are current and branded
- Validate payment links and checkout flow end-to-end

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Cold outreach does not work" | It works when personalized and targeted. Generic spam does not. |
| "I will follow up later" | 80% of sales require 5+ follow-ups. Follow up consistently. |
| "Price is the only factor" | Value, trust, and timing matter more than price. Sell outcomes. |