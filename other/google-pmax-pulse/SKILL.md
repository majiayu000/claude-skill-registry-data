---
name: google-pmax-pulse
description: |
  PMax morning anomaly check — compares last 3 days vs prior 3 days across spend, conversions, and CPA/ROAS for every Performance Max campaign. Flags CPA spikes (over 25%), conversion drops (over 25%), and spend spikes without conversions. Read-only — no changes applied. Disciplined: does NOT recommend major changes unless the issue is severe, since PMax is a black box and overcorrection is the #1 killer.
---

# PMax Pulse — 3-Day Anomaly Check (Read-Only)

For the Google Ads account the user names, scan every active **Performance Max** campaign and detect anomalies between the last 3 days and the prior 3 days. **Read-only — never modify PMax campaigns from a daily pulse, the black-box dynamics mean knee-jerk reactions cost more than they fix.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Inputs (per PMax campaign, both 3d windows)

- Spend
- Conversions
- CPA / ROAS

## Anomaly triggers

| Signal | Trigger |
|---|---|
| **CPA spike** | > 25% increase vs prior 3d |
| **Conversion drop** | > 25% decrease vs prior 3d |
| **Spend without conversions** | Spend 3d up > 20%, conversions flat or down |

## Severity tiers

- **🚨 Critical** — multiple triggers fire on the same campaign AND the campaign represents > 15% of account spend. ONLY here should the recommendation include action language.
- **⚠️ Alert** — single trigger fires. Surface and watch.
- **👀 Monitor** — soft signal, < trigger threshold, but trend worth tracking.

## Output format

Three sections, each a vertical list:

### 🚨 Critical (recommend immediate review)
- `[Campaign] — CPA ↑42%, conversions ↓30% over 3d. Spend $X (NN% of account). Consider pausing or moving to manual asset review.`

### ⚠️ Alerts (surface, no action recommended yet)
- `[Campaign] — CPA ↑28% over 3d. Single signal. Watch for 3 more days before acting.`

### 👀 Monitor (soft signals only)
- `[Campaign] — Spend ↑15% with conversions flat. Trend, not anomaly.`

## Disciplined rules

- Do NOT suggest scaling on a 3d positive blip
- Do NOT suggest budget cuts on a single-trigger alert
- Do NOT suggest asset edits — PMax automatically rebalances
- For Critical: state "consider pausing OR moving to manual asset review" — those are the only two safe responses to a true PMax crisis

End with: `_All findings — no changes applied. Investigate Critical items first._`
