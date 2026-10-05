---
name: abm-ops
description: "Account-based marketing for B2B SaaS. Use this skill to build a target account list, tier it 1:1 / 1:few / 1:many, size it against sales capacity, turn intent and engagement signals into plays, write the multi-channel orchestration contract each tier runs on, and measure the program in account coverage, penetration and pipeline instead of MQLs. Also triggers on: ABM, account-based marketing, target account list, TAL, named accounts, account tiering, 1:1 ABM, one-to-few, programmatic ABM, account selection, ideal customer profile fit, intent data, buying signals, 6sense, Bombora, Demandbase, account penetration, account coverage, sales and marketing alignment on accounts, enterprise account program."
---

# Account-Based Marketing Operations

## Step 0 (always first): Load brand context

**Before producing any deliverable, look for a `brand-context.md` file** in the user's project root (also check `./.claude/brand-context.md` and `./docs/brand-context.md`). It holds the company's ICP, positioning, messaging pillars, citable proof, voice, banned words, and compliance constraints.

- **If it exists:** read it in full and treat it as binding for this run. Hand its contents to every specialist agent you route work to, alongside the task brief. Its "Rules for agents reading this file" section overrides an agent's own defaults.
- **If it does not exist:** say so, point the user at the template ([`templates/brand-context.md`](../../templates/brand-context.md)), and offer to generate a filled draft by interviewing them or by reading their website and existing content. Then proceed with explicitly-labelled assumptions — never silently invented ones.

**Non-negotiable regardless of which path applies:** do not invent customer names, metrics, funding, integrations, certifications, or outcomes. Only proof recorded in `brand-context.md` (or supplied directly in the request) may be used as fact. Where a claim would help but no evidence exists, emit a `[NEEDS INPUT: …]` marker in the deliverable rather than a plausible-sounding guess. **Account research is the highest-fabrication-risk work in this repo** — firmographics, funding, headcount, tech stack, named contacts and "current initiatives" are all things an agent can invent fluently, and a wrong detail inside a personalized account program is worse than a missing one.

---

## What This Is

Account-Based Marketing Operations owns the **named account list itself** — the artifact that paid media, outbound, events and content all execute into, and the one thing in a B2B SaaS marketing org that is usually assumed to exist and is nobody's job. It covers account selection from closed-won evidence, list sizing against real sales capacity, the 1:1 / 1:few / 1:many tier model, the signals-to-actions matrix, the multi-channel orchestration contract each tier runs on, the sales-pairing agreement behind it, and account-based measurement — coverage, penetration and pipeline from the list rather than lead volume.

## The Team: 1 Specialist Agent

| # | Agent | File | What They Do |
|---|-------|------|-------------|
| 1 | Account-Based Marketing Strategist | `agents/abm-account-based-strategist.md` | Owns the target account list and its selection evidence, the capacity-and-coverage model that sizes it, the 1:1 / 1:few / 1:many tier model and its service levels, the signals-to-actions matrix (intent, product usage, engagement, commercial state, external events), the per-tier orchestration contract, Tier 1 account plans and buying-committee coverage, the sales-pairing agreement, and the account scoreboard with a credit rule that does not double-count other channels' pipeline. |

## How to Use

### Routing User Requests

**Building or fixing the account list** → Account-Based Marketing Strategist
- "Build our target account list and tier it"
- "We have 400 target accounts and a 6-person sales team — is that real?"
- "Which accounts should come off the list this quarter?"

**Program design & orchestration** → Account-Based Marketing Strategist
- "Design a 1:1 ABM program for our top 15 accounts"
- "Turn our intent data into a signals-to-actions matrix"
- "Write the multi-channel touch plan per tier, with owners"

**Measurement** → Account-Based Marketing Strategist
- "How should we report on ABM without using MQLs?"
- "Our ABM and paid dashboards both claim the same pipeline — fix the credit rule"
- "What does good account coverage look like for us?"

### Working Method

1. **Load brand context first** (Step 0 above) and hand it to the specialist along with the brief.
2. **Route to the specialist** whose remit matches the request. Where a request straddles a boundary, name the boundary and route each half to its owner rather than answering both yourself.
3. **Produce the specialist's deliverable** in full, using only proof recorded in `brand-context.md` or supplied in the request. Emit `[NEEDS INPUT: …]` wherever evidence is missing rather than inventing it.
4. **Name the handoffs.** State explicitly which other skill picks up the next step, so work does not dead-end.

**Boundaries this skill respects.** This skill publishes the account set and the contract; it never executes the touches. Sequences and cold-outreach mechanics belong to `sales-enablement` (`sales-outbound-strategist`); audience construction and delivery to `paid-media-ops`; the value narrative and per-persona messaging to `product-marketing-ops`; strategy inside an open opportunity to `sales-deal-strategist`, so an account in a live sales conversation is handed over rather than sequenced; expansion into paying accounts to `growth-ops` (`growth-customer-marketing-lead`); event-specific target lists to `events-ops`, which consumes this list rather than sourcing its own; field schema, scoring implementation and CRM routing to `marketing-analytics`; attribution modelling to `paid-media-attribution-analyst`; and the single cross-channel suppression record to `client-operations` (`ops-legal-compliance`), which every ABM touch queries before it fires.

## Output Standards

- Every deliverable names its audience, its owner, and the decision it enables.
- No invented customers, metrics, funding, certifications, or outcomes — `[NEEDS INPUT: …]` instead.
- Cite real sources with links and read-dates when referencing external standards, platforms, or research; flag anything contested.
- Where a recommendation depends on a number the company has not supplied (budget, headcount, sales capacity, current coverage), state the assumption in-line rather than burying it.
- No coverage, penetration, win-rate or spend-per-account benchmark is asserted as a target — baseline from the company's own first cycles.
