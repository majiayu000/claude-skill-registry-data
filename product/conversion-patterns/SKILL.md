---
name: conversion-patterns
version: 1.0.0
author: Personify Labs
description: Condition-gated paywall, checkout, retention, referral, and monetization-awareness patterns sourced from published A/B test case studies (abtest.design / Mobbin). Routes structure to vois-patterns, copy to righter, and instrumentation to metrics-tagging. Use when a ticket touches paywalls, trials, checkout, upsells, streaks/habit loops, or referral flows. Not a rulebook — every entry is a single validated hypothesis, not a universal law.
---

# conversion-patterns

## What this skill actually is

Every rule in `data/conversion-rules.json` is a real, published result — but each one is a single case study from one company, on one audience, at one funnel stage. None of them are controlled multi-trial findings, and the source only publishes winners, never the losing variants. Several of the rules in this file directly contradict each other (require a credit card vs. remove all friction; gate the paywall immediately vs. let users taste the product first) because they assume opposite starting conditions, not because one is right and one is wrong.

**This skill's job is not to hand you a lever. It's to force you to name your condition before you're allowed to pick one.** If you skip the condition-check and just grab the highest-lift rule, you're using this skill wrong.

## When this skill triggers

Use this skill whenever a ticket touches: paywalls, trial structure or length, checkout flow, cart abandonment, upsell/upgrade prompts, streaks or habit loops, referral flows, or pricing-page/CTA display. If the ticket is about onboarding sequencing instead, that's `onboarding-flow`'s job, not this one — check there first if you're not sure which one owns the ticket.

For pricing pages specifically, `vois-patterns` (PATH-F, `references/pricing-pages.md`) owns layout and structure. This skill owns the test-backed levers: whether to show a billing timeline, how to frame the CTA, whether to gate immediately. Use both: structure from vois-patterns, levers from here.

## Mode 1: Diagnose a Ticket (new feature or screen being planned)

Before touching `data/conversion-rules.json`, answer these against the actual ticket:

1. **Funnel stage** — is the user a cold visitor, an engaged free user, a paying user about to lapse, or a referred user? (This alone rules out most of the contradicting pairs.)
2. **Trust/intent level already present** — has the user already decided to act (picked a plan, added to cart) or are they still evaluating?
3. **Product type** — is the value experiential (needs to be used/tasted to be believed) or legible up front (obvious from a screenshot or description)?
4. **Is this actually a bug?** — before reaching for a psychological lever, check CHECKOUT-07 and RETENTION-04's `check_first` flag: rule out that the current flow is just broken or confusing.
5. **What would disprove this?** — every rule you pick needs a metric that would show it failed, not just one that would show it worked.

Then:
- Filter `data/conversion-rules.json` by category and condition match. Surface only rules whose `condition` field actually matches what you found in steps 1-3.
- If two candidate rules appear in each other's `contradicts` list, that's a sign you haven't pinned the condition down yet — go back to step 1-2, don't average the two.
- Hand the picked lever's structural implications (placement, gating type, modal vs. full-screen) to **vois-patterns**.
- Hand the picked lever's copy implications (framing, tone, badge text) to **righter**, along with the `mechanism` field so righter is writing copy in service of a specific effect, not generic UI text.
- Always close with **metrics-tagging**: whatever lever is shipped gets tagged as an experiment with a defined success metric and a defined kill condition, not shipped as settled fact. This step is mandatory, not optional — the case studies in this file only became "proven" because someone measured them in their own context, and yours is the only context that counts for your product.

## Mode 2: Audit an Existing Screen

Use when reviewing something already built, not proposing something new.

1. Identify which rule(s), if any, the current design already resembles.
2. Check whether the *condition* for that rule actually holds for this product/audience — flag mismatches explicitly (e.g. "this screen gates immediately like PAYWALL-05, but the product's value isn't legible without hands-on use, which is PAYWALL-05's stated failure condition").
3. If the design doesn't match any rule and conversion is a known problem, run Mode 1 against it as if it were a new ticket.
4. Output a short table: current pattern → matching/mismatched rule ID → recommended test, not a redesign. This skill proposes experiments, it doesn't declare winners.

## Output format

Both modes end in the same shape:

```
Condition: <funnel stage, trust level, product type — one line>
Candidate rule(s): <rule ID(s) + one-line lever>
Rejected rule(s) and why: <any contradicting rule ruled out, and the condition mismatch that ruled it out>
Structure → vois-patterns: <what's being handed off>
Copy → righter: <what's being handed off, plus the mechanism it needs to serve>
Instrumentation → metrics-tagging: <success metric + kill condition>
```

## Rule index (quick reference — full detail lives in the JSON)

**Paywall:** PAYWALL-01 billing timeline · PAYWALL-02 trial tied to annual · PAYWALL-03 single-tap gain-framed start · PAYWALL-04 yearly-only default · PAYWALL-05 immediate paywall · PAYWALL-06 vivid cost-of-inaction · PAYWALL-07 credit-card-required trial · PAYWALL-08 taste-before-gate · PAYWALL-09 pre-expiry reminder · PAYWALL-10 badge/framing on unchanged offer · PAYWALL-11 review over marketing copy · PAYWALL-12 identity-tuned visuals/copy

**Checkout:** CHECKOUT-01 remove mandatory account creation · CHECKOUT-02 single point-estimate price · CHECKOUT-03 restate incentive at decision point · CHECKOUT-04 benefit copy/reviews above the fold · CHECKOUT-05 countdown discount for cart abandoners · CHECKOUT-06 values/storytelling panel · CHECKOUT-07 (check_first) rule out a plain bug before testing a lever

**Retention:** RETENTION-01 decouple streak from full goal · RETENTION-02 ambient social proof mid-use · RETENTION-03 concrete per-item numbers over aggregate · RETENTION-04 (check_first) test icon/interaction choices against your own audience

**Referral:** REFERRAL-01 real-time referral progress · REFERRAL-02 longer trial for referred users

**Monetization awareness:** MONETIZE-01 badges on gated features · MONETIZE-02 gate what power users already hit

**CTA / pricing display:** CTA-01 reframe CTA toward trial value · CTA-02 monthly-equivalent price · CTA-03 distinctive button in a crowded layout · CTA-04 contrast + emphasis across pricing tiers · CTA-05 (check_first) "simplify" is not a guaranteed win

## Rule data

`data/conversion-rules.json` is the single source of truth. Categories: `paywall`, `checkout`, `retention`, `referral`, `monetization-awareness`, `cta-pricing`. Each rule has `lever`, `mechanism`, `condition`, `evidence`, `routes_to`, and `contradicts`. A `check_first: true` flag means this rule is a caution/verification step, not a lever to apply — always check it before applying anything else in its category.

Run `scripts/check-rule-sync.mjs` after any edit to this file or the JSON — it verifies every rule ID mentioned here exists in the JSON and vice versa, matching the consistency-check convention used in `onboarding-flow` and the Righter/Vois skills.
