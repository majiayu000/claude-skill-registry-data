---
name: bd-screening
description: >
  7-phase BD screening pipeline for crypto exchange listing.
  From HOT token detection through verified lead to outreach execution.
  Dual-source verification (DexScreener + DexTools), security deep dive,
  contact discovery, email-first outreach with trust-gated automation.
  Permanent process for every token scoring 85+.
tags: [crypto, bd, exchange, listing, outreach, pipeline]
---

# BD Screening Workflow — Buzz BD Agent

> 7 phases. Dual-source verification. Email-first outreach.
> Activates for every HOT token (score 85+) and Top 20 candidates.

## Pipeline Overview

```
Token Discovery → Score (11 rules) → HOT? → 7-Phase Screen → Outreach
      ↑                                              ↓
  32 Intel Sources                          Email-first (Gmail OAuth)
  ARIA v2 cron (06:00 UTC)                  Trust-gated automation
  Manual /scan command                      CC: Ogie always
```

## The 7 Phases

### Phase 1: Dual-Source Verification

Pull from BOTH DexScreener API AND DexTools browser scrape.
Cross-reference: price, market cap (circulating vs FDV), volume, liquidity.
If FDV gap > 5x → flag and apply FDV_GAP_PENALTY scoring rule.

### Phase 2: Security Deep Dive

Check 4 security sources: Go+ Security, Quick Intel, Token Sniffer, Honeypot.is
Any critical flag → CONTRADICTORY_AUDIT_HOLD (manual review required)
Pass = green across all 4 sources.

### Phase 3: BD Readiness Classification

| Classification | Criteria                                  | Action                       |
| -------------- | ----------------------------------------- | ---------------------------- |
| BD Sweet Spot  | Score 85+, security clean, team reachable | Proceed to outreach          |
| BD Watch       | Score 70-84, minor flags                  | Monitor, re-screen in 7 days |
| BD Pass        | Score < 70 or security critical           | Archive, auto-learn patterns |

### Phase 4: Contact Screening

3-source contact discovery:

1. Token website → team page, contact links
2. Twitter/X bio → DM (DEPRECATED — email only now)
3. GitHub/Discord → contributor emails

Valid targets: team@, info@, contact@, hello@, founders@
NEVER send to personal emails.

### Phase 5: Outreach Execution

4 email templates (template-only, no LLM-generated bodies):

1. **Initial (dual-funnel)**: listing opportunity + HSaaS audit offer
2. **Follow-up 48h**: gentle reminder with new data point
3. **Breakup 7d**: final touch, respect their time
4. **HSaaS audit**: standalone security audit pitch

Rules:

- Max 10 emails/day (spam prevention)
- CC always: dino@solcex.cc + ogie.solcexexchange@gmail.com
- HTML signature with Buzz logo
- Dynamic cron follow-ups (48h + 7d, maxRuns:1, self-deactivating)

### Phase 6: Reporting

- Sunday Listing Intelligence Report (Top 20 + pipeline stats)
- Per-token screening receipts in outreach_queue table
- Trust audit trail in trust_audit table

### Phase 7: Auto-Learning

Failed outreach → pattern extraction → new scoring rules.
Example: LOL token override session → 3 new permanent rules
(GHOST_VOLUME, CTO_FLAG, VOLUME_LIQUIDITY_RATIO).

## Usage

### Via Claude Code

```
/screen PEPE                    # Full 7-phase screening
/screen 0x... --phase 1-2       # Verification + security only
/screen --report                # Generate Sunday report
```

## Pipeline Stats (v9.2)

- 363 tokens in pipeline
- 66 scored
- 0 HOT (honest — triple verification catches the fakes)
- 11 permanent scoring rules
- $200 revenue from AIBTC signal factory
