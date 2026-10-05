---
name: working-backwards
description: >-
  Write an Amazon-style PR-FAQ (mock press release + FAQ) to pressure-test a product idea
  customer-first and kill weak ideas on paper. Use when someone says "write a PR-FAQ", "PRFAQ",
  "press release", "working backwards", "start from the customer", "draft the launch announcement",
  "is this idea clear enough to build", or has a fuzzy idea and wants clarity on what and why.
  NOT for testing risky assumptions with experiments (product-discovery) or build plans
  (shaping-work / write-plan).
---

# Working Backwards

Start from the customer and the desired end-state, write it down, and iterate on
the *document* until the thinking is clear — long before any engineering. The
artifact is a **PR-FAQ**: a one-page mock press release + an FAQ of the hard
questions. Most PR-FAQs are never built — **killing a weak idea cheaply on paper
is the point, not a failure.**

Why writing: prose forces clarity that slides and good intentions can't. If you
can't write a compelling, honest press release for it, you don't understand it
yet — and neither will the customer.

References:
- `references/pr-faq-template.md` — the press-release + FAQ structure, section by section.
- `references/six-page-narrative.md` — the prose-memo / silent-read discipline (for proposals & reviews beyond a launch).
- `references/input-metrics.md` — input-vs-output metrics, DMAIC, the WBR (how you'd *measure* it once live).

## When to use this vs. its neighbors

- **product-thinker** decided *should we?* → use Working Backwards to force the *customer end-state* into focus.
- Idea is fuzzy / stakeholders disagree on what it even is → write the PR-FAQ; the draft surfaces the disagreement.
- The risk is "will this technically/behaviorally work?" → that's **product-discovery** (experiments), not this.
- The PR-FAQ is approved and clear → hand to **shaping-work** to define the work.

## The method

1. **Write the press release first** (customer-benefit-first, < 1 page). Use the
   template. Write it as if it already launched. The customer's *problem* and the
   *benefit* lead — not the technology.
2. **Write the FAQ** (≤ 5 pages). Put the *hard* questions in, the ones that
   could kill it: market size, per-unit economics, dependencies & third-party
   risk, feasibility, what has to be true. The FAQ is a **pre-mortem on your own
   idea** — if you skip the uncomfortable questions, the document is dishonest.
3. **Iterate as a document.** Circulate; open the meeting with a **silent read**;
   take general feedback first, then line-by-line; **seniors speak last** (no
   anchoring). Expect 10+ drafts. Revise from the criticism, not around it.
4. **Decide: build / kill / keep iterating.** A PR-FAQ that can't be made
   compelling and honest is a *cheap save* — kill it here, not after a quarter of
   engineering.

## Output

A **PR-FAQ** (press release + FAQ, from the template) and a clear **verdict**.
Close with the signature block:

```
`★ Working Backwards View ────────────────────────`
- Customer + benefit: [who, and the one-line win]
- Verdict: [build / kill / iterate] — [why in one line]
- Biggest hole: [the FAQ question most likely to kill it]
`─────────────────────────────────────────────────`
```

## Handoffs

- Verdict = build, but a key assumption is unproven → `product-discovery` (test it cheaply first).
- Verdict = build, and it's clear → `shaping-work` (define the work), then `write-plan`.
- Verdict = build, and this is a direction rather than a one-off → offer to record it as a bet in `.tap/product.md` via `/tap-skills:curate-product-context`. The press release already states the customer end-state; the FAQ's most dangerous question is usually the kill condition.
- Need to re-litigate *whether* to build at all → `product-thinker`.
- Offer to publish the PR-FAQ for team review: `/tap-skills:render-doc` then `/tap-skills:dossier-publish` (md stays source of truth; republish after edits).
