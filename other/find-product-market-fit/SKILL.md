---
name: find-product-market-fit
description: >-
  The product-market-fit loop that drafts `BUSINESS_PLAN.md` and interrogates its weakest
  assumption until the 8-point readiness gate passes, called by
  ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Find product-market fit

Produce a **validated business plan** — one whose product-market fit has been pressure-tested,
not asserted. The deliverable is a single living `BUSINESS_PLAN.md` (schema and PMF gate in
`${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`), revised in place across an interview loop until it passes
the 8-point PMF readiness gate and the user confirms.

The reason this skill exists: a business plan written in one pass is a wish list. Real
product-market fit is found by repeatedly attacking the plan's weakest assumption — the one that,
if wrong, kills the business — and revising until the load-bearing claims are evidenced or have a
cheap test attached. This skill is that loop, made disciplined.

The core stance: **draft proactively, then interrogate**. Infer a v0 from what already exists and
interview against it. A concrete draft gives the user something to react to, and correction is faster and sharper than composition.

---

## The Loop

```
Phase 0  Intake      → find/read app plans or provided material
Phase 1  Draft v0    → write BUSINESS_PLAN.md from what's known; score the PMF gate
Phase 2  Interview   → attack the lowest-scoring, highest-leverage gate criterion (one question)
Phase 3  Revise      → fold the answer in; re-tag confidence; re-score the gate
         ↑___________ repeat Phase 2–3 until gate = 8/8 AND user confirms
Phase 4  Validate    → flip status to validated; hand off next steps
```

Each loop closes one gap. The gate score **chooses the next question**, so the interview is never
a fixed questionnaire.

---

## Phase 0 — Intake (read before asking)

Before any question, gather everything that already constrains the plan.

1. **Build plans in the repo** — the `ceh-build-planning` plans in `product/plans/*.md` (or the
   plans folder the repo's `CLAUDE.md` names). If found, read them. Their Goal (what it does,
   who it's for, the key flow), Scope, and Design carry your product, target-user hint, and
   solution detail. A plan whose Goal points to a `BUSINESS_PLAN.md` was written from this plan:
   read it for its Scope and Design only. Record their paths in `derived_from`. Built plans stay in
   the folder with `status: built`: read them too, and `product/ARCHITECTURE.md` Overview and Key
   Decisions when it exists.
2. **Anything the user provided** — a PRD, pitch deck, spec, README, landing page, a pasted
   description. Read it directly. A GitHub URL: fetch the README.
3. **Other plan-shaped files** — `PRD.md`, `BRIEF.md`, `docs/` product notes. Use them as input,
   not gospel.

Extract without asking: what the product does, who it seems to be for, the core flow, the stage
(idea / prototype / launched / revenue), and any pricing or competitor hints already written down.
If `BUSINESS_PLAN.md` already exists, you are **continuing the loop** — read it, re-score the gate,
resume at the lowest-scoring criterion.

**If nothing exists** (no plans, nothing provided): skip the draft-from-source path and open with
a single grounding question — _"In one or two sentences: what's the product, and who is it for?"_
— then draft v0 from that answer. Still draft before interrogating.

---

## Phase 1 — Draft v0 proactively

Write a complete `BUSINESS_PLAN.md` per the schema — all 13 sections, even the thin ones. Fill
what the source material supports; for everything else, **write your best-guess hypothesis and tag
it `[assumption]`**, not "TBD". A wrong, specific assumption is useful — it gives the interview a
target. A blank is not.

Tag every load-bearing claim: `[evidence]`, `[assumption]`, or `[hypothesis-to-test]`. Then score
the PMF gate (N/8) in frontmatter and identify the **lowest-scoring, highest-leverage** criterion
— that is where the interview starts.

Show the user the draft (or, for a long plan, the executive summary + the gate scorecard with
which criteria are open). Then begin the interview. Do not wait for permission to draft.

---

## Phase 2 — The PMF Interview

Rigorous means **adversarial toward assumptions, not toward the user**. You are hunting the claim
most likely to be wrong and most expensive if it is. The gate scorecard picks the target; you ask
the one question that would most move it.

### Rules

1. **One question per turn.** Never dump a list. Ask the single highest-leverage thing you don't
   yet know. Wait for the answer.
2. **The gate drives the order.** Attack the lowest-scoring criterion first; within it, the claim
   whose failure is most fatal. Re-pick after every answer — the target moves.
3. **Offer a hypothesis to react to, not an open void.** Instead of _"What's your pricing?"_ ask
   _"I've assumed $49/seat/month because that undercuts [competitor]'s $79 — does that match what
   you think they'll pay, or is the real anchor their current spend on [alternative]?"_ Correcting
   a concrete guess is faster and sharper than composing from scratch.
4. **Push past abstractions to a real instance.** "SMBs want this" → _"Name one. Who specifically
   told you, or who's a real candidate, and what do they do today instead?"_ The first sign of a
   weak plan is a population where there should be a person.
5. **Separate evidence from belief, out loud.** When an answer is a hope, say so and re-tag it
   `[assumption]`; when it's a real signal (a quote, a transaction, a comparable spend), tag it
   `[evidence]`; when it's a belief with a cheap test, make the test concrete and tag it
   `[hypothesis-to-test]`. The tags are the honesty mechanism.
6. **Capture the customer's words verbatim.** A real quote ("I'd pay anything to stop doing this
   in Excel") is the strongest asset a plan has — store it word-for-word in §02 or §10.
7. **Steelman the alternative.** For differentiation, force the question: _"Why doesn't the
   customer just keep doing nothing / using the spreadsheet?"_ Inertia is the default competitor
   and beats most products.
8. **Know when to stop asking on a point.** Once a criterion is evidenced or has a named test,
   move on — don't gold-plate a passing criterion while others sit at zero.

### The criteria as an agenda (see the 8-point gate in the schema)

| Gate criterion                   | The question it demands an answer to                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------- |
| 1 Problem real & acute           | Who feels this, how often, how badly — and what does it cost them now?                |
| 2 Beachhead narrow & reachable   | One nameable segment — where are the first 10 customers, physically?                  |
| 3 Differentiation defensible     | Why you over the real alternative (incl. doing nothing), and why can't it be copied?  |
| 4 Willingness to pay             | What signal says they'll pay _this_ price — a quote, a pre-order, a comparable spend? |
| 5 Market math bottom-up          | SOM = customers × price with stated assumptions — does the arithmetic clear the bar?  |
| 6 Unit economics can work        | Is there a believable path to LTV > CAC with a sane payback?                          |
| 7 First channel credible         | One channel where they already are, with a first-10 plan?                             |
| 8 Riskiest assumption has a test | What single wrong assumption kills this — and the cheapest test for it?               |

---

## Phase 3 — Revise

After each answer (or a small batch), fold it into `BUSINESS_PLAN.md`:

- Update the affected sections; **re-tag** the confidence on every claim the answer touched.
- Regenerate §01 Executive Summary and §12 Risks ranking — they shift as the plan firms up.
  Leave every specialist subsection and tagged line as it is (see "Specialist subsections" in the
  schema): the premortem's kill criteria in §12 are fixed in advance on purpose.
- Re-score `pmf_gate: N/8` in frontmatter and bump `updated`.
- Tell the user, in one or two lines, what just moved (e.g. _"Criterion 4 went from assumption to
  evidence — you have two LOIs at $49. Lowest now is criterion 5: the market math is still
  top-down. Next question is about that."_).

Then return to Phase 2 on the new lowest-scoring criterion. **This is the loop the goal demands:
draft → interview → revise, repeated until satisfiable.**

### When a criterion can't be evidenced yet

At idea stage, most criteria will not have evidence — that is expected. Do not stall the loop
waiting for data that requires building or selling first. Instead, convert the bare `[assumption]`
into a `[hypothesis-to-test]`: name the cheapest experiment that would settle it (a landing-page
smoke test, 5 customer interviews, a concierge MVP, a pre-sale) and schedule it in §13. A
criterion with a real, cheap, scheduled test **passes the gate**. Hand-waving does not.

---

## Phase 4 — Validate & Hand Off

When all 8 criteria are met (evidenced or test-attached) **and** the user confirms they are
satisfied:

- Flip frontmatter `status: validated`, set `pmf_gate: 8/8`, stamp `updated`.
- Give a one-paragraph verdict: the sharpest version of who pays, for what, why you, and the one
  experiment that most de-risks the whole thing next.
- Point onward: if the validation surfaced product changes, the build plan
  (`ceh-build-planning`) should absorb them in a new plan; the §13 milestones become the
  build/validation backlog.
- Name the plan's softest remaining area (edge, numbers, first customers, risks, or the next 90
  days). The gate proves a fit exists, not that the business is sound, and
  `ceh-business-plan:develop-business-plan` routes that area to the specialist that owns it.

**Do not flip to validated to end the loop early.** If the user wants to stop before the gate
passes, leave `status: draft`, record the open criteria honestly, and say plainly which
assumptions remain untested — an honest draft beats a plan that claims a fit it hasn't found.

---

## Stop Conditions

- **The idea fails a gate criterion with no path to a test** — e.g. the problem isn't real, or no
  reachable customer exists. Say so directly. A plan's most valuable output can be "don't build
  this, here's why." Don't manufacture a fit.
- **The product is fundamentally different from the app plan it derives from** — flag the
  mismatch; the business plan may be pointing at a pivot the app plan hasn't caught up to.

---

## Edge Cases

**App plans exist but are sparse** (skeleton only): draft from the §01 Concept and treat §02–§13
as mostly `[assumption]` — the interview has more to do, which is fine.

**User has real traction already** (launched/revenue): start the gate from evidence, not guesses.
Many criteria may pass on intake; the loop focuses on the few still soft (often §07 channel
scaling or §06 defensibility).

**User resists a question / answers a different one:** keep the answer — it's real material —
re-tag what it informs, and re-ask the original once at most, rephrased. Don't interrogate.

**"Just write me a business plan, no questions":** draft v0, score the gate, and hand it over with
the open criteria flagged as the assumptions they're betting on — but say once that the plan is
unvalidated until those are tested.

**No product idea at all, just "I want to start something":** the problem comes before the
product. Interview for an acute problem the user has standing or insight to attack, then draft.

**No human to answer** (a headless run, or called by another agent): take the "no questions" path
above. Draft v0, score the gate, leave `status: draft`, and end with the open criteria as the
questions a person must answer, in gate order, each with the assumption the draft used. When nothing
exists to draft from, stop and report that the plan needs a product and a customer from a person.
