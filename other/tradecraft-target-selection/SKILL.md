---
name: tradecraft-target-selection
description: >
  Choose where to spend effort for the best return — which program, which asset, which surface.
  Load at the start of bug-bounty work or when a scope is broad and time is limited, on "which
  program", "where should I hunt", "prioritize these targets". Signals: a big scope list, many
  in-scope domains, a new program, limited time.
domain: tradecraft
type: methodology
stability: learning
modes: [bugbounty, pentest]
schema_version: 1
---

# Target selection & prioritisation

## When it applies
You have more scope than time. Whether picking a bug-bounty program or ordering assets inside one
authorized engagement, the choice of *where to look* usually matters more than how hard you look.

## Why it works
Vulnerabilities cluster where code is new, complex, or neglected, and payout/impact clusters where
the asset is important. Spending your first hours choosing well beats grinding a hardened, picked-over
target — most reports come from a minority of assets.

## Method
1. **Size the attack surface**: prefer programs/assets with lots of subdomains, APIs, and
   functionality over a single static site — more surface, more bugs.
2. **Favour freshness**: newly added scope, a recent acquisition, a just-launched feature, or a
   product the crowd hasn't saturated. Watch changelogs and scope-change feeds.
3. **Match your strengths**: pick tech you know (a stack, a language, a vuln class) — depth compounds.
4. **Weigh the economics** (bounty): payout table, response/triage speed, resolution rate, and how
   crowded the program is. A fast, fair program at medium bounty often beats a slow flagship.
5. **Prioritise assets inside scope**: rank by likely impact (auth, payments, admin, PII) × likely
   softness (obscure subdomain, legacy app, thin JS) and start at the top.
6. **Timebox and re-evaluate**: if an asset yields nothing after a set budget, rotate — don't sink.

## Gotchas
- Big brand ≠ easy: flagship domains are the most hunted. The soft spots are usually the
  forgotten subdomains and new features, not `www`.
- Confirm the asset is actually **in scope** before investing (load `tradecraft-scope-roe`).
- Don't chase payout alone — a program that never triages wastes more time than a lower bounty.

## Verify success
You can state, in one line each, why you picked this program/asset and what the highest-value
surface is — and you're working that surface, not a random one.

## References
Bug-bounty program statistics/leaderboards; disclosed-report patterns; the `tradecraft-attack-scenarios` skill.
