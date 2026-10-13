---
name: tradecraft-bugbounty-platforms
description: >
  Understand how the major bug-bounty platforms differ — scope rules, disclosure, triage, and
  reputation — so you play each correctly. Load when working a program on HackerOne, Bugcrowd,
  Intigriti, YesWeHack, or Immunefi, on "platform rules", "safe harbor", "VDP vs paid", or before
  submitting. Signals: a program URL on one of these platforms, a policy/scope page.
domain: tradecraft
type: reference
stability: learning
modes: [bugbounty]
schema_version: 1
---

# Bug-bounty platform intelligence

## When it applies
You're operating inside a platform's program. The technical work is the same everywhere, but scope
enforcement, disclosure, payout, and reputation mechanics differ — and getting them wrong loses
bounties or violates the rules.

## Why it works
Each platform encodes its own contract. Reading the program's policy through the lens of that
platform's conventions tells you what's actually in scope, what proof triage expects, and how your
report will be judged — before you spend effort.

## Key points per platform
- **Common to all**: the program's policy page is authoritative — read scope, **out-of-scope**,
  accepted vuln types, testing rules (rate limits, no-DoS, test accounts), and **safe-harbor** terms
  before touching anything. VDP (no bounty) vs paid changes your time investment.
- **HackerOne**: reputation/signal/impact affect invitations; structured severity (CVSS); private
  programs reward good signal. Watch the "eligible for bounty" vs "known issue" distinctions.
- **Bugcrowd**: uses the **VRT** (Vulnerability Rating Taxonomy) — map your finding to it and expect
  payout by the program's reward range for that VRT entry.
- **Intigriti**: clear in-scope/out-of-scope tiers; researcher-friendly triage; watch domain
  wildcards and the severity matrix.
- **YesWeHack**: EU-centric; strict scope; good for fresh European targets.
- **Immunefi (web3)**: smart-contract/DeFi focus; payouts tied to **funds at risk** (often huge);
  PoC on a fork/testnet, never mainnet exploitation; primacy/known-issue rules are strict. Pair with
  `code-review-solidity`.

## Method
1. Read the policy end-to-end; extract scope, out-of-scope, rules, safe harbor, and the severity/
   reward model.
2. Set up isolated test accounts and honour rate limits.
3. Rate your finding by the platform's model (CVSS or VRT) — see `reporting-cvss-scoring`.
4. Submit per the platform's report format (`reporting-bug-bounty-writeup`) and engage triage
   professionally (`reporting-triage-communication`).

## Gotchas
- Out-of-scope is as important as in-scope — testing an excluded asset can void safe harbor.
- "Wildcard" scope still excludes third-party/SaaS you don't control — check.
- Platform reputation is durable; a spammy or rule-breaking submission history follows you.

## References
Each platform's program-policy and disclosure docs; Bugcrowd VRT; FIRST CVSS; program safe-harbor statements.
