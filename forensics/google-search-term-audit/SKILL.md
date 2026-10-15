---
name: google-search-term-audit
description: |
  Forensic Google Ads Search-term waste audit. Pareto-filters down to the 80% of spend that matters (campaign-level, then search-term-level), then flags wasteful terms using campaign-relative triggers: low engagement (CTR ≥40% below campaign avg) and low conversion (CVR ≥40% below campaign avg, including zeros). Surfaces a "Red List" with suggested negative-keyword exclusions and identifies common "waste words" for root-level negatives. Read-only — proposes exclusions, never executes them. Use weekly for waste cleanup.
---

# Google Search Term Audit — Waste Forensics (Read-Only)

For the Google Ads account the user names, run a forensic search-term waste audit. **Read-only — produces a suggested-exclusion list, never executes mutations.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Phase 1 — Data selection + Pareto filtering

1. **Campaign filter**: Search campaigns only (exclude Shopping, PMax, Display).
2. **Campaign Pareto**: Identify the campaigns that account for **80% of total Search spend**.
3. **Search-term Pareto (per campaign)**: Within each selected campaign, pull the search terms that account for **80% of that campaign's spend**.

This focuses the audit on the spend that actually matters.

## Phase 2 — Waste identification (the "Red List")

For each high-spend search term, compare against its **own campaign's** averages (not account averages — relativity matters).

### Trigger 1 — Low Engagement Red Flag
- Search term spend ≥ 5% of campaign total, **AND**
- Search-term CTR ≥ 40% **lower** than the specific campaign's average CTR

### Trigger 2 — Low Conversion Red Flag
- Search term spend ≥ 8% of campaign total, **AND**
- Search-term CVR ≥ 40% **lower** than the specific campaign's average CVR (zero conversions counts)

Any term hitting either trigger goes on the **Red List**.

## Phase 3 — Root-cause analysis

Review the Red List for common "waste words" — patterns that appear across multiple flagged terms. Examples:
- `"free [product]"`, `"how to [verb]"`, `"diy [thing]"`, `"jobs"`, `"salary"`, `"reviews of [competitor]"`

If 3+ Red List terms share a common waste word, recommend a single **root negative** that covers them all instead of a list of individual negatives. Saves ad-group bloat.

## Output

### Section 1 — Red List table

| Search term | Campaign | Term spend | % of camp spend | Term CTR | Camp avg CTR | Term CVR | Camp avg CVR | Trigger | Suggested negative |
|---|---|---|---|---|---|---|---|---|---|

Sort by term spend descending. Cap at top 30.

### Section 2 — Root negative recommendations

For each common waste word found:
- `Suggested root negative: "[word]" (phrase match) — covers N terms on the Red List, $X total wasted spend`

### Section 3 — Per-campaign exclusion summary

For each campaign with Red List terms:
- Total Red List spend
- Total Red List conversions
- Estimated monthly savings if all suggested negatives applied
- One-line take: `Recommend adding NN exact negatives + N phrase root negatives to [campaign]`

End with: `_All recommendations — no negatives added. Use the `google-ads-search-execution` skill to enact any subset of these exclusions._`
