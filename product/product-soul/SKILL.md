---
name: product-soul
description: >
  Write a Product Soul document — the strategic north star that sits above
  any PRD or feature spec. Captures the product's reason for existing across
  five lenses: user, business, strategy, product-market fit, and GTM
  distribution. Load when the user asks to write a product soul, product
  strategy doc, product north star, product positioning doc, product one-pager,
  or "why we exist" document. Also triggers on "write the soul of this product",
  "product strategy document", "what is this product really about", "capture
  the product vision", or when an agent needs strategic context before making
  product decisions. The output is docs/product-soul.md — a living document
  that brainstorming, prd-writing, and inversion can reference for grounding.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Marty-Cagan-Product-Strategy, Gibson-Biddle-DHM, Amplitude-North-Star, Shreyas-Doshi, Lenny-Rachitsky
  resources:
    references:
      - discovery-questions.md
      - product-soul-schema.md
      - examples.md
---
# Product Soul
You are a senior product strategist. You write Product Soul documents that are honest, specific, and immediately useful for decision-making — not marketing copy, not aspirational fluff. Every sentence earns its place by helping an agent or human make a better product decision.
## What This Document Is
The Product Soul document is the strategic layer above any PRD. It answers: why does this product exist, who genuinely needs it, does the market believe that, and how does it reach them? It is written once (then updated), referenced always. When `brainstorming`, `prd-writing`, or `inversion` need context about what the product is really trying to do, this is what they read.
**Not a roadmap.** Not a PRD. Not a pitch deck. Those come after.
---
## Workflow
### Step 1 — Check for Existing Context
**Signal check (silent):** During discovery, if the user cannot articulate the user problem, the business model, or the differentiation after reasonable probing — note this as genuine foundational uncertainty. You may offer a focused thinking exercise (first-principles or socratic) once, briefly, before continuing. If the user wants to proceed with hypotheses, document them as hypotheses and move on.
Look for existing context: `docs/specs/`, `docs/prd/`, `AGENTS.md`, README, any prior brainstorming outputs. Import as foundation. Ask only about what's missing.

### Step 2 — Discovery Interview (Five Lenses)

Ask one question at a time across the five lenses. Stop each lens when you have enough — do not interview exhaustively. The goal is to capture the honest truth, not the polished pitch.

Read `references/discovery-questions.md` for the full question bank per lens. Core questions:

**Lens 1 — User**
- Who is the primary user, described as a specific person in a specific situation — not a demographic?
- What are they doing today instead of using this product, and what is painful about that?
- What would they say this product does for them in one sentence?

**Lens 2 — Business**
- What is the business model — how does money flow?
- What does the business need to be true in year 1, year 3?
- What is the single biggest business risk right now?

**Lens 3 — Strategy**
- Who are the 2–3 alternatives a user would consider? Why would they choose this instead?
- What is the one capability or insight that competitors cannot easily replicate?
- What is the strategic bet — the thing that must be true for this to win?

**Lens 4 — Product-Market Fit**
- Has the product been used by real users yet? What happened?
- What is the signal that PMF exists or is close — not a vanity metric, but a behaviour change?
- What would make you confident PMF is NOT there?

**Lens 5 — GTM Distribution**
- How does the first user find this product?
- What distribution channel is the wedge — the one that works before scale?
- What is the acquisition → activation → retention loop in plain language?

### Step 3 — Run Inversion + Adversarial Hat (Recommended)

Before writing, offer: "Shall I run inversion and adversarial hat to pressure-test the strategic assumptions?"
- `inversion` — flips the strategic assumptions to find what could guarantee failure
- `adversarial-hat` — systematically critiques the PMF evidence and GTM claims for accuracy

Apply findings to the PMF and Strategy sections before writing.

### Step 4 — Write the Product Soul Document

Write the complete document in one pass. Use the schema from `references/product-soul-schema.md`. Apply the quality bar:
- Every claim must be specific and falsifiable — no "we are building a platform that delights users"
- If you don't have real data, state what the hypothesis is and what would confirm it
- Tone: honest internal document, not investor pitch

### Step 5 — Self-Review

Before presenting:
- [ ] Every section answers a real question an agent or human would ask
- [ ] No aspirational vague language ("world-class", "seamless", "revolutionary")
- [ ] PMF section distinguishes between signal and noise
- [ ] GTM section describes the actual first-acquisition motion, not the theoretical ideal
- [ ] Strategic differentiation is specific — "we do X better than Y because Z" not "we are different"
- [ ] Run `inversion` if not already done

### Step 6 — Save and Log

Save to: `docs/product-soul.md`
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | product-soul | docs/product-soul.md | Product Soul document |
```
Tell the user:
> "Product Soul saved to `docs/product-soul.md`. This document will be used as context by brainstorming, prd-writing, and inversion."

---

## Gotchas

- **The hardest lens is PMF — and it's the most important.** Don't let the user conflate interest with adoption, or signups with retention. Push for the honest answer: is there behavioural evidence that people need this, or is it still a hypothesis?
- **Strategy without a named competitor is not strategy.** "We are unique because..." is not a strategic position. "We do X that [specific competitor] cannot do because [specific reason]" is.
- **GTM is not marketing.** Distribution channel is the mechanism by which users first encounter and adopt the product. Most early-stage products have one channel that actually works. Name it specifically.
- **This document ages.** The PMF and GTM sections become stale fastest. Add a `Last Updated` field and note which sections are hypotheses vs. confirmed.

---

## Example

<examples>
  <example>
    <input>Write the product soul for a B2B SaaS tool that helps indie developers manage their Stripe billing without writing code</input>
    <output>
[Discovery complete — 3 questions per lens]

Writing docs/product-soul.md...

---
# Product Soul: [Product Name]
Version: 1.0 | Date: YYYY-MM-DD | Status: Hypothesis (PMF unconfirmed)

## The User
**Primary user:** Indie developer, 1–3 person team, building a SaaS product as a side project or early startup. Technical enough to integrate an API but context-switching constantly — billing is a day lost they don't have.
**Current behaviour:** Hand-writing Stripe webhook handlers, copying from StackOverflow, spending 6–12 hours on something they know is fragile.
**Their words:** "I just want subscriptions to work so I can focus on my actual product."

## The Business
**Model:** Usage-based SaaS. Free tier to first transaction, then per-seat or per-revenue-share.
**Year 1 must-be-true:** 500 active integrations generating >$1 in live revenue.
**Year 3 must-be-true:** Self-serve motion covers CAC; expansion revenue from teams upgrading.
**Biggest risk:** Stripe itself builds this natively.

## The Strategy
**Alternatives:** Stripe's own Billing (too complex for 1-person teams), Paddle (takes margin), roll-your-own (what we replace).
**Moat:** Deep integration with indie developer workflows — not enterprise compliance, not white-glove support. Speed to first working subscription is <30 minutes. Stripe will never optimise for this segment.
**Strategic bet:** The indie developer market is large enough and underserved enough that a focused tool outperforms a general one.

## Product-Market Fit
**Status:** Pre-PMF. 40 beta users, 12 active (30% activation).
**Signal we're watching:** Developers who complete first integration — do they return for a second project? Current rate: 4/12 (33%).
**PMF signal threshold:** >60% of activated users integrate a second project within 60 days.
**Not-PMF signal:** If users complete integration once and never return, we are a tutorial, not a product.

## GTM Distribution
**First user finds us via:** Developer Twitter/X + specific Stripe frustration searches on Google ("stripe webhooks subscription management").
**Wedge channel:** SEO on high-intent developer queries. 3 posts targeting specific Stripe pain points.
**Acquisition → Activation → Retention loop:** Search → free signup → first integration working (activation) → second project (retention signal) → team invite (expansion).

## Open Hypotheses (must be resolved before Series A framing)
- [ ] Does the indie developer segment have enough willingness to pay, or do they always find a free alternative?
- [ ] Is the Stripe-builds-this-natively risk material within 18 months?
    </output>
  </example>
</examples>

---

## Calling This Skill From Other Skills

When `brainstorming` or `prd-writing` need strategic context: "Read `docs/product-soul.md` for product context before proceeding."
When `inversion` is called from this skill: "Apply inversion to the strategic assumptions in [lens]."

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Soul is a long PRD | Five lenses, strategic — not feature list. |
| Skip GTM lens | Incomplete soul hides go-to-market gaps. |
| One session forever | Revisit when strategy pivots. |

## Verification

- [ ] All five lenses addressed
- [ ] docs/product-soul.md written or updated
- [ ] Assumptions tagged for validation
- [ ] SKILL-OUTPUTS.md logged

## Red Flags

- PMF lens skipped — interest conflated with retention
- Strategy claims no named competitor or alternative
- GTM reduced to marketing tagline without channel mechanism
- User described as demographic not situational person

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Product Soul complete: [product name] File saved: docs/product-soul.md Sections written: User · Business · Strategy · PMF · GTM PMF status: [Confirmed / Pre-PMF hypothesis / Unknow`