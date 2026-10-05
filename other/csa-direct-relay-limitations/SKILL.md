---
name: csa-direct-relay-limitations
description: |
  Use this skill to explain to customers/sales prospects why FMCSA CSA scores are not available in real-time. Covers the SAFER refresh cycle and what 'real-time' actually means for CSA data.
---

# Why There Is No Real-Time CSA Score Relay

A common question: "Why doesn't [vendor] show real-time CSA scores?" Answer: FMCSA doesn't publish them that way. Period.

## SAFER refresh cycle
FMCSA recalculates and republishes SMS data monthly, typically around the 15th of each month:
- Inspections from past 24 months
- Crashes from past 24 months
- Peer group reassignments
- BASIC percentile recalculation
- Public display update

There is NO real-time API. Vendor "real-time CSA" claims are either:
1. Reading the same monthly SAFER feed
2. Estimating based on individual inspection events (predictive, not actual)
3. Pure marketing

## What IS available faster than monthly
- **Individual inspection results** — appear in FMCSA database within 1-3 business days of inspection
- **Crash reports** — within 5-10 business days
- **Carrier operating status changes** — same day

These individual events are not your "CSA score" — they're the data feeding into your eventual recalculation.

## What Compass does
- Pulls your individual inspection + crash data daily (within 1-3 business days of FMCSA recording)
- Estimates score trajectory using current methodology
- Refreshes your official BASIC scores monthly when SAFER updates
- Alerts you when an inspection arrives with violations that may push you into alert

## What Compass does NOT do
- Claim real-time CSA scores
- Pretend to have advance knowledge of FMCSA recalculations
- Sell "predictive CSA" as if it's the same as actual scores

## Honest customer messaging
"FMCSA publishes CSA monthly via SAFER. We pull the moment it refreshes (~15th of each month) and surface your delta. Between refreshes, we track inspections + crashes that will affect your next recalculation, so you have 4-6 weeks of warning instead of finding out the day FMCSA publishes."

## Why this matters for sales conversations
Prospects ask "do you do real-time CSA?" Wrong answer: "yes!" (deceptive). Right answer: "FMCSA doesn't publish real-time CSA — no one has it. We pull the monthly refresh and show you the delta plus the in-flight inspections that will affect your next recalculation." This positions Compass as honest + transparent vs. competitors making false claims.

## CFR citations
- **FMCSA SAFER public website**
- **FMCSA SMS Methodology Refresh Schedule**

## How Compass surfaces this
Searchable in Compass Ask. Runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=csa-direct-relay-limitations

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
