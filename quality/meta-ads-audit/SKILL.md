---
name: meta-ads-audit
description: |
  30-day comprehensive Meta Ads health audit. Checks pixel/CAPI integrity, scans creative fatigue across the account, profiles audience-segment spend split, surfaces ROAS/CPA outliers (top + bottom decile), evaluates budget allocation efficiency, and produces a professional written report. Read-only — no changes applied. Use for quarterly reviews, new-account onboarding, or any "what's actually happening in this account" deep dive.
---

# Meta Ads Audit — 30 Days (Read-Only)

Comprehensive health audit of the ad account the user names. **Read-only — produces analysis only, never applies changes.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Sections to cover

### 1. Tracking integrity
- Pixel events firing in the last 30d (PageView, ViewContent, AddToCart, Purchase)
- CAPI vs Pixel delta on Purchase events — flag if > 15% mismatch
- Event Match Quality score per pixel
- Recommendation: any missing events, gaps in CAPI, or low EMQ

### 2. Spend distribution
- Top 5 campaigns by spend, % of total
- Top 5 ad sets by spend within those campaigns
- Pareto check — is 80% of spend concentrated in < 20% of entities? (healthy or risky?)

### 3. Performance — ROAS / CPA outliers
- Identify campaigns in top decile of ROAS (scaling candidates)
- Identify campaigns in bottom decile of ROAS or above-target CPA (cut candidates)
- For each outlier: 30d trend (improving / declining / volatile)

### 4. Creative fatigue scan
- Per ad: hook rate, hold rate, frequency, CTR delta vs ad-set median
- Score each ad as `Healthy / Early Warning / Fatigued / Dead`
- Surface top 10 fatigued ads with specific refresh recommendations

### 5. Audience segment split
- Spend share by audience type (lookalikes, interest, broad, retargeting)
- ROAS per audience type
- Recommendation: is the mix balanced? Over-indexed on saturated audiences?

### 6. Budget allocation efficiency
- Compare budget % to revenue % per campaign
- Identify campaigns where budget % >> revenue % (over-funded)
- Identify campaigns where budget % << revenue % (under-funded relative to performance)

## Output format

A clean structured report. Use sections, tables for outliers, and a short **Top 5 priorities** section at the end.

End with: `_Audit complete — no changes applied. Use this report to plan optimization passes._`
