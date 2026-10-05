---
name: onboarding-flow
version: 1.2.0
author: Personify Labs
description: >
  Design new onboarding flows or evaluate/critique existing ones — signup sequences, setup
  checklists, first-run wizards, personalization quizzes, permission priming, paywalls — for
  SaaS/web products or consumer/mobile apps. Use this whenever someone asks to design, build,
  spec, improve, review, audit, or critique onboarding, a first-run experience, a getting-started
  flow, a signup sequence, an account setup wizard, or "the first thing users see," whether
  starting from scratch or from screenshots/a description of an existing flow.
  Pulls current visual reference from Mobbin, routes all UI copy to righter, and routes all
  structure/styling to the vois skills (vois-patterns → vois-components → vois-tokens).
tags:
  - design
  - ux
  - onboarding
  - product
  - mobbin
---

# Onboarding Flow

A skill for designing onboarding for two very different contexts. SaaS/web onboarding and
consumer/mobile onboarding fail for opposite reasons if you cross the patterns: block a SaaS
user behind a linear wizard and they bounce before seeing the product; let a consumer app skip
the personalization quiz and you lose the sign-up's whole reason for existing. Pick the right
one before you design or evaluate anything.

This skill defines the *sequence and screen types*. It is not a copywriting or styling skill:

- **Every word that appears on screen** (headlines, button labels, quiz questions, permission
  copy, checklist item text) routes to the **righter** skill. Don't guess at wording here.
- **Every structural/visual decision** (spacing, components, tokens, animation, accessibility)
  routes to **vois-patterns → vois-components → vois-tokens**, in that order.
- This skill sits *above* both: it tells you which screens exist and in what order (or should);
  righter tells you what words go on them; vois tells you how they're built.

---

## Two Modes

### Mode 1: Evaluate an Existing Flow
1. **Get the flow in front of you.** Screenshots, a Figma/Mobbin link, or a plain description of
   the screen-by-screen sequence. If it's incomplete, say what's missing rather than guessing at
   unseen screens.
2. **Determine the shape** using the decision tree below — SaaS companion checklist or consumer
   linear sequence. An existing flow that uses the wrong shape for its product type is itself a
   finding, not something to route around.
3. **Read the matching reference file** and walk the flow screen by screen against every rule
   `id` in `data/onboarding-rules.json` for that shape, plus the five `UNIV-*` rules. If the
   flow states or implies its activation event (see Mode 2 step 2), treat any screen that
   doesn't move toward it as a candidate cut even when it doesn't fail a specific numbered rule.
4. **Output in the Review format below.** Don't rewrite copy or restyle components yourself —
   flag copy issues for righter and structural issues for vois-patterns, cite what should be
   checked there, and stop.

### Mode 2: Generate a New Flow
1. **What kind of product is this?** Walk the decision tree below — it determines the whole
   shape of the flow, not just the visual style.
2. **Name the activation event.** Before sequencing any screens: what does this user need to
   accomplish for onboarding to have worked? What's the one activation event (first workflow
   run, first save, first invite sent, first personalized result shown), and what information is
   strictly necessary to reach it? Anything that doesn't materially move the user toward that
   event is friction, not onboarding — cut it rather than including it "just in case."
3. **Pull current reference, don't rely on memory.** If the `mcp__Mobbin__search_flows` or
   `mcp__Mobbin__search_screens` tools are available, use them to pull 3–5 real examples for the
   *specific* product category (e.g. "fintech app onboarding," "B2B analytics tool setup guide")
   before finalizing screens — patterns date fast, and a competitor-specific pull beats the
   general patterns catalogued here. If Mobbin isn't available, use `references/` as the
   fallback baseline. Treat what you pull as evidence of current practice, not proof that a
   pattern is correct — weigh it against `data/onboarding-rules.json`, which is this skill's
   durable baseline. A competitor doing something doesn't override a rule here without a stated
   reason ("Apple does X" is not itself an argument for X).
4. **Read the matching reference file** for the full screen-by-screen breakdown.
5. **Route copy to righter and structure to vois** as you build each screen — don't batch this
   at the end.
6. **Output in the New Flow format below.**

---

## Decision Tree: Which Onboarding Shape?

```
START: What is the user signing up for?

├─ SaaS / web product — used repeatedly at a desk, ongoing account, often paid seat-by-seat
│  └─ → read references/saas-onboarding.md                                  [SHAPE-SAAS]
│     Pattern: drop into the real product immediately, companion checklist alongside it.
│     Never a full-screen linear wizard that blocks the product.
│
└─ Consumer / mobile app — short sessions, one person, often a subscription decision up front
   └─ → read references/consumer-onboarding.md                             [SHAPE-CONSUMER]
      Pattern: linear full-screen sequence (value prop → personalize → permissions →
      account → paywall → confirmation → home). The wizard IS the experience before home.
```

If a product genuinely straddles both (e.g. a mobile companion app for a web SaaS product),
default to the shape of the surface you're designing or evaluating *this* flow for — a mobile
app onboarding still follows the consumer shape even if the parent product is B2B SaaS.

A second edge case: a single surface that blends both, like Notion, Figma, Slack, or a
ChatGPT-style prosumer tool — used repeatedly at a desk like SaaS, but with real upfront value
in a personalization choice (a workspace type, a template, a use case). Default to the SaaS
shape as the base — these are still ongoing accounts used repeatedly, not short sessions — and
borrow at most one consumer-style screen for the single highest-leverage personalization
question, only if the product's early value genuinely depends on it. Treat CONSUMER-004's
payoff rule as binding on that screen. Never let this turn into a multi-screen quiz gating
access to the product — that's the SaaS shape's whole point (`SAAS-001`).

---

## Reference Files

| File | Covers | Shape ID |
|---|---|---|
| `references/saas-onboarding.md` | Setup guides, onboarding checklists, empty states, in-product companion patterns | `[SHAPE-SAAS]` |
| `references/consumer-onboarding.md` | Value prop screens, personalization quizzes, permission priming, paywalls, confirmation | `[SHAPE-CONSUMER]` |

Read only the one file that matches your shape. Each is self-contained.

---

## Output Formats

### Review format (Mode 1)
Use this for each screen or moment reviewed. Group by screen in flow order.

---
**Screen:** [name/position, e.g. "Screen 3 of 6 — interest picker"]

**Shape:** [SaaS companion checklist | Consumer linear sequence] — flag here if the flow is
using the wrong shape for its product type.

**Rules checked:** [list every rule `id` from `data/onboarding-rules.json` that applies to this
screen type, whether it passed or failed]

**Violations found:** For each one:
- `[rule id]` (MUST | SHOULD, from `data/onboarding-rules.json`)
  - Observed: [what's actually on this screen in the supplied flow — point at it, don't assert
    without something to point at]
  - Expected: [what the rule's `outcome` requires]
  - Fix: [what to do instead, in one sentence]

If none, write "None found." A `MUST` violation is always a violation. A `SHOULD` violation with
a stated, legitimate reason isn't one — note the reasoning in place of a fix instead of flagging it.

**Route to righter:** [any copy on this screen worth a pass — labels, headlines, error states —
or "Nothing flagged."]

**Route to vois:** [any structural/spacing/component concern worth a vois-patterns/vois-components
pass, or "Nothing flagged."]
---

After all screens: one summary line — total violations (call out `MUST` violations separately,
since those are non-negotiable), and the single highest-leverage fix (usually a
`CONSUMER-004`/personalization-payoff issue, a `SAAS-001`/blocking-wizard issue, or any `MUST`
violation, if present).

### New Flow format (Mode 2)
Use the screen sequence itself as the deliverable — a numbered list of screens in order, each
with: screen purpose, primary action, what's collected or shown, and which rule `id`s it
satisfies. Follow with the Checklist Before Handing Off below, completed, not just shown blank.

---

## Universal Rules (apply regardless of shape or mode)

These held across every real flow pulled for this skill, SaaS and consumer alike. Every rule
below carries a stable `id` in backticks — cite the id, not the bullet position, when referencing
a rule from outside this file. Each is also tagged `MUST` or `SHOULD` in
`data/onboarding-rules.json`: `MUST` rules address coercion, deception, or dark patterns and
have no legitimate exception; `SHOULD` rules are strong defaults with real exceptions — deviate
from them only with a stated reason, not by default.

- **One primary action per screen** `id: UNIV-001` (SHOULD). For a screen presenting a single
  decision, give it exactly one primary action — if a screen has two competing CTAs for the same
  decision, one is winning by accident. Make the secondary action visually and verbally
  subordinate (text link, not a second button of equal weight). This doesn't apply to a
  checklist's per-item CTAs (`SAAS-003` — each item is its own independent action, not
  competitors) or a legally required consent screen's equal-weight buttons (`CONSUMER-007`).
- **Progress must be honest and visible** `id: UNIV-002` (MUST). A progress bar, step count
  ("Step 3 of 4"), or fraction ("3/8 completed") should reflect real remaining effort, not
  motivate through vagueness. Never show progress that doesn't move.
- **Never trap the user** `id: UNIV-003` (MUST). Every screen needs a way out — back arrow, X, or
  skip — except the single final confirmation screen. A flow with no exit reads as coercive, not
  confident.
- **Ask before you tell** `id: UNIV-004` (SHOULD). If you collect a preference (goal, interest,
  role), the payoff must visibly appear within one or two screens after that answer. If it
  won't, cut the question — asking without using it just adds friction for nothing.
- **Route every word to righter, every layout decision to vois-patterns** `id: UNIV-005` (MUST).
  Don't write filler copy "for now" and don't eyeball spacing. It compounds into rework.

**Structured lookup:** `data/onboarding-rules.json` holds every tagged rule from this file and
both reference files as `{ id, strength, condition, outcome, source_file }` — useful for a quick
condition/outcome check by `id` without opening the full file it lives in. This is also what
Mode 1 walks screen-by-screen against.

**Source of truth:** `data/onboarding-rules.json` is canonical for a rule's `strength`,
`condition`, and `outcome`. The `.md` files restate rules for readability and carry the worked
examples (real app names, screen-by-screen breakdowns) the JSON doesn't — but if the two ever
disagree, the JSON wins. `scripts/check-rule-sync.mjs` checks that every tagged id cited in the
`.md` files resolves to a real entry in the JSON, the reverse, and that every rule has a valid
`strength`; run it after editing rules in either place.

---

## Checklist Before Handing Off (Mode 2)

- [ ] Shape selected (SaaS companion checklist vs. consumer linear sequence) and justified
- [ ] Activation event named, and every screen either moves toward it or was cut
- [ ] Pulled current Mobbin reference for this product's specific category, if the tool is available
- [ ] Screen sequence drafted, one primary action per screen
- [ ] Progress indicator defined and honest
- [ ] Every screen has an exit except the final confirmation
- [ ] Personalization inputs (if any) visibly reflected later in the flow
- [ ] All copy drafted through righter (not placeholder text)
- [ ] All structure/spacing/components resolved through vois-patterns → vois-components → vois-tokens

---

## Maintaining This Skill

`data/onboarding-rules.json` is the canonical rule set (18 rules: 5 universal, 6 SaaS, 7
consumer). Every rule carries a `strength` of `MUST` or `SHOULD` (see Universal Rules above for
what the distinction means) alongside its `id`, `condition`, `outcome`, and `source_file`. When
you add, remove, or reword a rule, update it in both the `.md` file and the JSON, then run:

```
node scripts/check-rule-sync.mjs
```

It fails loudly if an id is tagged in markdown but missing from the JSON, listed in the JSON but
never cited in markdown, tagged in a file that doesn't match the JSON's `source_file`, or missing
a valid `strength`. Run it before publishing any edit to a rule.

`evals/cases.json` is a fixed set of worked flows (good and bad, both shapes) with the rule ids a
correct review should flag — and, for the exact false positive this skill's checklist and
consent patterns first shipped with, the ids it should explicitly *not* flag. It's a manual
regression corpus, not an automated test suite: whether a flow actually violates a rule is a
judgment call, not something a script can verify. Re-walk each case's `scenario` against the
current rules after editing `SKILL.md` or the JSON, and confirm the same ids still come out.
