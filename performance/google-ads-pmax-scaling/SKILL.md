---
name: google-ads-pmax-scaling
description: "Use when scaling Google Ads Performance Max campaigns: budget scaling rules, pause triggers, location/audience/asset expansion. Loads PMax evaluation first."
metadata:
  source: "prompts/skills/google_ads/pmax-scaling"
---

# Google Ads PMax — Scaling & Expansion

Rules for scaling PMax campaigns that have passed evaluation. Only load after confirming profitability via `google-ads-pmax-evaluation`.

## Scaling Prerequisites

ALL must be true before scaling:
- Campaign profitable for 14–30 consecutive days
- ROAS ≥ target (default 300% if not specified)
- CPA ≤ target
- Performance trends stable or improving WoW

---

## Budget Scaling

**Increase daily budget by 20–50% every 14–30 days.**

| Scenario | Action |
|----------|--------|
| Profitable 14+ days, trends stable | Increase 20–50% |
| Post-scaling CPA > 1.2× target | PAUSE scaling, optimize assets/negatives, reassess after 30 days |
| Post-scaling ROAS < 0.8× target | PAUSE scaling, optimize, reassess after 30 days |
| Consistently profitable 90+ days | Can exceed 2–3× initial budget cap |

**Hard cap**: Do not exceed 2–3× initial monthly budget until 90+ days of consistent profitability.

Tool: `google_ads_propose_update_campaigns` with the new daily `budget_micros` in account currency (not micros). Dry-run first; apply only after the user approves.

---

## Location Expansion

- Only after core locations profitable for 30+ days
- Expand to similar/adjacent markets
- Create separate asset groups for new locations if targeting differs
- Monitor new locations independently for 30 days before further expansion

---

## Audience Expansion

- Start with **Observation** mode for new audience signals
- Monitor performance for 14+ days
- Switch to **Targeting** mode only if performance holds
- Do NOT force audience preferences without data

---

## Asset Expansion

Based on BEST-performing assets from evaluation:

| Asset Type | Expansion Rule |
|-----------|---------------|
| Images | Add 5–10 total, similar style to BEST. Different angles/contexts. |
| Headlines | Create variations of BEST. Same theme, different wording. Test different CTAs. |
| Descriptions | Variations of BEST. Same value props, different framing. |
| Videos | Test 30-second formats if shorter videos are BEST. |
| New asset groups | Create for high-performing audience segments identified in Insights. Use targeted messaging. |

---

## Prohibitions

- Never scale before 14 days of profitability
- Never increase budget > 50% in one step
- Never scale beyond 2–3× initial budget before 90 days profitable
- Never continue scaling if CPA > 1.2× target OR ROAS < 0.8× target
- Never remove BEST or GOOD performing assets
- Never force device/location exclusions without checking for technical issues first
