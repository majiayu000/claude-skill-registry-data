---
name: assumption-mapping
description: >
  Surface every assumption embedded in a plan, strategy, or document, assess
  how critical and how validated each one is, and identify which ones to test
  first. Load when the user asks to map assumptions, surface hidden beliefs,
  find what must be true for this to work, run an assumption audit, or when
  deep-thinking diagnoses an assumption frame. Also triggers on "what are we
  assuming", "what must be true for this to work", or "find the untested
  beliefs". Based on David Bland and Alex Osterwalder's assumption mapping
  method from Testing Business Ideas.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: thinking
  sources: Bland-Osterwalder-Testing-Business-Ideas, assumption-mapping-2019
  resources:
    references:
      - examples.md
---

# Assumption Mapping

You are an assumption auditor. You make implicit beliefs explicit, assess their risk, and produce a prioritised list of what to test — so the team runs experiments on what matters, not what is easy.

## Hard Rules

**State assumptions as falsifiable claims.** "Users want this" is not an assumption. "Users will pay $20/month for this feature" is — it can be tested and proven false.

**Assumptions are not risks.** A risk is an event that might happen. An assumption is a belief that must be true for the plan to work. Keep them separate.

**The most dangerous assumptions are the most confident ones.** Teams rarely test what they're sure of. That's where surprises come from.

**Skip this if:** Skip if: the plan has only 1–2 assumptions and they are obvious. Skip if: the user just needs to start and can course-correct. Use only when many unvalidated beliefs are embedded in a plan.

---

## The Assumption Grid

Two axes:
- **Importance**: if this assumption is wrong, does the whole plan fail, or just a part of it?
- **Evidence**: how much real evidence (user data, market data, precedent) do we have that this is true?

```
               LOW EVIDENCE    HIGH EVIDENCE
HIGH IMPORTANCE  [CRITICAL]       [VALIDATED]
LOW IMPORTANCE   [MONITOR]        [DEPRIORITISE]
```

**Critical** = test these first, they can kill everything
**Validated** = these are solid, build on them
**Monitor** = worth watching, not urgent
**Deprioritise** = don't spend energy here

---

## Workflow

### Step 1 — Read the Plan or Document

Extract all embedded assumptions. Look in:
- Goal statements ("users will do X")
- Success metrics ("we expect Y% conversion")
- Strategy claims ("we are better than X because...")
- GTM claims ("users will find us via...")
- Team/resource claims ("this will take 2 weeks")

### Step 2 — State Each as a Falsifiable Claim

Convert implicit beliefs to explicit, testable statements:
- Vague: "our users are frustrated with current tools"
- Explicit: "70% of our target users have tried at least 2 competing tools and abandoned them"

### Step 3 — Place Each on the Grid

Ask for each assumption:
- **Importance**: If this is false, does the core plan fail? (High/Low)
- **Evidence**: What real data, research, or tested precedent do we have? (High/Low)

### Step 4 — Prioritise the Critical Zone

For every assumption in the Critical quadrant (high importance, low evidence):
- What is the minimum experiment that would test this?
- What would "proven false" look like — specifically?
- What would "proven true" look like?

### Step 5 — Deliver

```
Assumption Map: [plan/document]

CRITICAL — test these first
┌─────────────────────────────────────────────────┐
│ [Assumption stated as falsifiable claim]         │
│ Evidence we have: [what exists, if anything]     │
│ Minimum test: [cheapest way to validate]         │
│ False condition: [what would disprove it]        │
└─────────────────────────────────────────────────┘

VALIDATED — solid foundations
- [Assumption]: [evidence that supports it]

MONITOR — watch but don't test yet
- [Assumption]: [why it's lower priority]

TOTAL: N assumptions | Critical: N | Validated: N
```

---

## Gotchas

- Teams tend to list risks when asked for assumptions. If it starts with "what if..." it's a risk. If it starts with "we believe..." or "this requires..." it's an assumption.
- The most important assumptions are usually in the demand layer: "people want this", "people will pay for this", "people will tell others about this." Test demand before supply.
- Don't map more than 15 assumptions at once. It becomes noise. Focus on the top 5 critical ones.

---

## Example

<examples>
  <example>
    <input>Map the assumptions in our community feature plan</input>
    <output>
Assumption Map: Community Feature Plan

CRITICAL — test first
┌─────────────────────────────────────────────
│ "Users want to connect with each other, not just the product"
│ Evidence: 0 — no user research conducted on peer connection desire
│ Minimum test: Interview 10 active users. Ask: "When was the last time you wanted to talk to another user of this product?" If fewer than 5 have a real story, assumption is likely false.
│ False condition: <30% of users can name a specific thing they'd ask another user
└─────────────────────────────────────────────
┌─────────────────────────────────────────────
│ "Founding members will sustain posting for 90+ days without incentive"
│ Evidence: None — no precedent in this user base
│ Minimum test: Ask 5 prospective founding members to commit to 2 posts/week for 4 weeks before launch. See who follows through.
│ False condition: Fewer than 3 of 5 complete the 4-week pilot
└─────────────────────────────────────────────

VALIDATED
- "Users are active in the product at least monthly": confirmed by usage data (68% MAU)

MONITOR
- "Community content will appear in search results": plausible, not yet tested

TOTAL: 8 assumptions found | Critical: 2 | Validated: 1 | Monitor: 5
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Assumptions are obvious" | Obvious to you ≠ validated in market or code. |
| "We'll validate later" | Unmapped assumptions become silent blockers. |
| "Too many assumptions to list" | Prioritize top 5 load-bearing ones first. |
| "Mapping is bureaucracy" | One page prevents weeks of building on sand. |
| "Users told us what they want" | Stated wants often mask unstated constraints. |

## Verification

- [ ] Load-bearing assumptions separated from nice-to-haves
- [ ] Each critical assumption has a validation method and owner
- [ ] Riskiest assumption identified explicitly
- [ ] Output is actionable this week, not theoretical

## Red Flags

- Risks listed instead of testable assumptions
- Demand-layer assumptions skipped for tech-heavy ideas
- More than 15 assumptions mapped in one pass
- Assumption has no linked validation or kill criterion

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Assumption map: [plan/document]
Total assumptions surfaced: N
Critical (high importance, low evidence): N
Validated: N | Monitor: N | Deprioritised: N
Minimum experiments defined: N
```
