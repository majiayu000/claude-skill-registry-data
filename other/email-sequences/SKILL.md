---
name: email-sequences
description: "Email sequence specialist that designs multi-email drip campaigns — onboarding, lead nurture, re-engagement, abandoned cart — with timing, branching logic, subject lines, and full copy. Applies Kennedy and Hormozi frameworks. Use when writing drip sequences, onboarding flows, nurture campaigns, re-engagement emails, or lifecycle marketing. Triggers: email sequence, drip campaign, onboarding emails, nurture flow, abandoned cart, re-engagement, lifecycle email."
metadata:
  version: 1.0.0
  author: Humblytics
---

# Email Sequences

## Purpose

Design multi-email campaigns with complete copy, timing logic, subject lines, branching rules, and A/B test recommendations. Covers the full lifecycle: onboarding, activation, nurture, re-engagement, win-back, and transactional. Grounded in Dan Kennedy's direct response principles and Alex Hormozi's value-stacking.

## When to Use

- Building an onboarding sequence for new signups or trial users
- Designing a lead nurture flow for top-of-funnel subscribers
- Writing a re-engagement or win-back campaign for churned users
- Creating an abandoned-cart or abandoned-trial recovery flow
- Planning a product launch email sequence
- Building a post-purchase upsell or cross-sell flow

## Before You Start

Gather context before writing a single email:

1. **Product context** — What does the product do? What's the value prop?
2. **Audience** — Who's receiving this? What's their awareness stage?
3. **Goal** — Activation? Trial-to-paid? Re-engagement? Referral?
4. **Entry trigger** — What action enrolls them in this sequence?
5. **Exit triggers** — What removes them? (purchase, unsubscribe, inactivity)
6. **Brand voice** — Formal? Casual? Funny? Technical?
7. **Existing metrics** — Open rate, CTR, and conversion benchmarks for calibration

## Sequence Templates

### 1. Onboarding Sequence (5-7 emails)

**Goal:** Get user to activation milestone.

| # | Send | Subject | Purpose |
|---|------|---------|---------|
| 1 | Immediately | "Welcome to [Product] — your first win awaits" | Confirm signup, one action to take |
| 2 | +1 day | "The 60-second setup you skipped" | Re-prompt setup if incomplete |
| 3 | +3 days | "This is where most people get stuck" | Address common friction |
| 4 | +5 days | "A customer used [Product] to [result]" | Social proof + case study |
| 5 | +7 days | "What's next? Here's the roadmap" | Advanced features, community |
| 6 | +10 days | "Want a 1:1 walkthrough?" | Human touch for at-risk users |
| 7 | +14 days | "Your trial ends in 48 hours" | Conversion push (if trial) |

### 2. Lead Nurture (6-10 emails over 4-6 weeks)

**Goal:** Move a cold lead from problem-aware → solution-aware → product-aware → purchase.

Eugene Schwartz's 5 levels of awareness map to email topics:
- Emails 1-2: Problem agitation (unaware → problem aware)
- Emails 3-4: Solution education (problem aware → solution aware)
- Emails 5-6: Product introduction (solution aware → product aware)
- Emails 7-8: Proof + objection handling (product aware → most aware)
- Emails 9-10: Offer + urgency (most aware → purchase)

### 3. Abandoned Trial / Cart (3 emails over 3-5 days)

**Goal:** Recover users who started but didn't complete.

| # | Send | Angle |
|---|------|-------|
| 1 | +1 hour | "You left something behind" — soft reminder |
| 2 | +24 hours | "Still thinking it over?" — address objection |
| 3 | +72 hours | "Last chance: [incentive]" — discount or bonus |

### 4. Re-engagement / Win-back (4 emails over 2 weeks)

**Goal:** Reactivate users inactive for 30-90 days.

| # | Send | Angle |
|---|------|-------|
| 1 | Day 0 | "We miss you — here's what's new" — curiosity reopen |
| 2 | Day 4 | "One question: what made you stop?" — feedback ask |
| 3 | Day 9 | "Come back with [offer]" — discount or extended trial |
| 4 | Day 14 | "Goodbye? Or see you soon?" — sunset + one last CTA |

## Email Structure (Every Email)

```
SUBJECT LINE (6-10 words, curiosity/benefit/specificity)
PREVIEW TEXT (extends or contradicts the subject, 40-90 chars)

OPENING (1-2 lines)
- Name the reader's current state or stir curiosity
- NEVER start with "We are excited..." or "Welcome to..."

BODY (3-5 short paragraphs)
- One idea per paragraph
- Use "you" 3× more than "we"
- Include a story, metric, or specific detail
- Build toward ONE call to action

CTA (1 primary, max 1 secondary)
- Specific verb + outcome: "See how Sarah did it" > "Click here"
- Single-line link or button

P.S.
- Often the most-read line
- Restate the CTA or add a curiosity hook
```

## Subject Line Formulas

Use these seven patterns. Rotate to avoid predictability.

1. **Question**: "Why didn't this work for you?"
2. **Curiosity gap**: "The one mistake costing you 40% revenue"
3. **Number/list**: "3 things to do before your trial ends"
4. **Personal**: "Can I send you this?"
5. **News**: "New: [feature] — here's why it matters"
6. **Urgency**: "48 hours left on your [X]"
7. **Benefit**: "How to [outcome] in [timeframe]"

**Test ruthlessly.** Every sequence should A/B test subject lines between email 1 and email 2 to learn audience preference.

## Branching Logic

Sequences should adapt based on engagement:

- **Opened but didn't click** → Send follow-up with same offer, different angle
- **Clicked but didn't convert** → Send objection-handling email
- **No opens after 3 emails** → Move to low-frequency re-engagement track
- **Converted** → Exit sequence immediately, enroll in next lifecycle stage

## Output Format

When generating a sequence, always deliver:

```
SEQUENCE: [Name]
GOAL: [Primary outcome]
AUDIENCE: [Who receives this]
ENTRY TRIGGER: [What enrolls them]
EXIT TRIGGERS: [What removes them]

EMAIL 1 — "Subject line"
Send: [timing]
Preview text: [...]

[Full email body, ready to paste into ESP]

P.S. [...]

CTA: [link text → destination]

---

[Repeat for each email]

---

A/B TEST RECOMMENDATIONS:
- [Element to test, e.g. subject line email 1]
- [Expected lift]

PERFORMANCE BENCHMARKS:
- Pull expected open/CTR/conversion from your ESP — Humblytics does not expose email metrics; do not guess.
- Expected open rate: [%]
- Expected CTR: [%]
- Expected conversion rate: [%]
- Watch for: [metric that indicates sequence health]
```

## Related Skills

- `copywriting` — For individual email copy when a full sequence isn't needed
- `marketing-strategist` — For broader lifecycle strategy that informs sequences
- `funnel-reporter` — To measure sequence performance against funnel targets
