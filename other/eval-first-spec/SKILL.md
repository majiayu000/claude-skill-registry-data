---
name: eval-first-spec
description: Turn a validated wedge into the scope you can SCORE — a one-sentence job, 20 pass/fail golden cases drawn from real artefacts, an L0–L4 autonomy level with a failure taxonomy and a derived acceptable failure rate per mode, and a cost-per-outcome budget to the cent. Fires on "spec the build", "define scope", "scope the v1", "write the spec", "how do we know it works". Not for the component pipeline or effort split (use compound-system-architecture), not for pilot price / terms / commercial success metrics (use pilot-six-term-sheet), not for whether the thing gets adopted at all (use wedge-five-questions).
type: generator
supersedes: none
---

## What it does

Converts a validated wedge into a v1 spec that a judge — human or harness — can run and score. It forces four parts, in order: (1) a one-sentence job with the clause that says how a single outcome is judged pass or fail; (2) 20 golden cases, each a real input paired with a binary pass/fail contract, composed to a fixed spread so the number is not gamed on happy paths; (3) one chosen autonomy level L0–L4, its failure taxonomy, and an acceptable failure rate per mode that is *derived* from the cost of one failure, not chosen to look safe; (4) a cost-per-outcome budget to the cent, checked against the value of one outcome. The artefact is the filled `template.md`. A spec that cannot be scored is not shipped; it is an opinion with a template around it.

## The Icarus reframe

A generic PM spec writes one acceptance criterion per feature and calls it testable, which works for deterministic software and fails for an AI product, where the same input can pass Tuesday and fail Wednesday. So this skill reframes the two disciplines it absorbs from the user-story family: acceptance criteria become a scoreable **golden set** of 20 real-input pass/fail cases spanning the distribution, and vertical slicing becomes **autonomy slicing** — ship the lowest autonomy level L0–L4 that still delivers the job, then earn each level up with a measured pass rate. The number that turns a spec from a wish into a commitment is cost-per-outcome to the cent, checked against value-per-outcome; if cost meets or beats value, no eval score can save it.

## When to use / When NOT

Use once a fellow has a validated wedge (adoption evidence in hand) and needs to define what building it means and what "working" means, before code. Trigger phrases: "spec the build", "define scope", "scope the v1", "write the spec", "how do we know it works".

Do not use when:

| Request | Belongs to |
|---|---|
| "How should we architect the AI system / what's the component pipeline / what's the effort split" | `compound-system-architecture` (sibling, 07). It designs *how* to build; this defines *what working means* and the budget. Route the architecture there. |
| "What are the pilot terms / how do we price it / what's the commercial success metric" | `pilot-six-term-sheet` (sibling, 07). Its success metric is the business KPI the customer buys; this skill's golden cases are the engineering pass/fail underneath it. Name the boundary, do not merge them. |
| "Is this even a wedge / will it get adopted / is it sharp enough" | `wedge-five-questions` (06). Run that first. This skill assumes the wedge already passed. |
| "Score the whole idea / give me the so-what" | `problem-quality-scorecard` / `so-what-stress-test` (00–01). Those judge the idea; this specs the build. |

Do not use it to invent a spec from nothing. If there are no real artefacts to draw golden cases from, the input is not ready. Say so and send the fellow back to probes and data sourcing. Never fabricate cases to reach 20.

## Method

Fill in `template.md`. Four parts, then the kill-line check.

### Part 1 — The job line

One sentence, this shape: **who** gets **what single output**, on **what recurring trigger**, judged pass by **what observable condition**. The judged-by clause is the part fellows skip and the part that makes everything downstream scoreable.

Good: "At each shift handover, the outgoing line supervisor gets a ranked list of the ≤5 machines most likely to cause an unplanned stop this shift — judged correct if the machine that actually caused a stop was in the list, or the shift was clean and the list said so."

Not a job line: "An AI copilot for factory managers." No single output, no trigger, no way to score one instance. That is an engine, not a job. Name the gap and ask for the sentence. Do not invent the missing pieces.

### Part 2 — The 20 golden cases

Each case is one **real input** plus the **binary pass condition** for that input. Draw inputs from artefacts the wedge already produced: probe logs, historical data, real documents. Tag each case's source `[Fact]` (a real observed input) or `[Assumption]` (a plausible input you constructed). Compose the 20 to this fixed spread — a set of 20 happy paths is a vanity metric:

| Band | Count (floor) | What it is |
|---|---|---|
| Typical | ≥ 6 | Common real inputs the system meets most cycles. |
| Edge | ≥ 7 | Rare-but-real: boundary values, messy or partial input, the unusual-but-legitimate case. |
| Adversarial | ≥ 4 | Inputs engineered to trigger the worst failure mode in the taxonomy. |
| Must-refuse | ≥ 3 | Inputs where the correct output is "I can't / not enough signal / out of scope." |

Two hard rules on the set:

- **Coverage.** Every failure mode named in Part 3's taxonomy must be reachable by at least one case. You cannot measure a mode's rate with no case that can fail into it.
- **Reality floor.** At least **14 of 20** must be `[Fact]` — real inputs. If you cannot find 14 real inputs, you have not run enough discovery to spec this. That is the finding; report it, do not paper over it with invented cases.
- **One artefact is not many cases.** A sub-input sliced from a single artefact counts toward the 14-`[Fact]` floor only if it is independently checkable against its own ground truth; otherwise the artefact is one case, not many. No slicing one document into ten to reach the floor.

### Part 3 — Autonomy level and derived failure rates

Pick one level. Ship the lowest that still delivers the job line.

| Level | System does | Human does | Failure that reaches production | Sets cost-of-one-failure |
|---|---|---|---|---|
| L0 Informs | Surfaces information | Interprets and acts on all of it | Wrong/missing info the human doesn't catch | A glance; human is full backstop |
| L1 Drafts | Proposes the output | Reviews and commits every one | A bad draft the human approves | Bounded; 100% reviewed |
| L2 Acts on approval | Prepares the action | Approves per item or batch | A wrong action the human rubber-stamps | Rises with batch size |
| L3 Acts, reviews exceptions | Executes; flags low-confidence | Reviews only flagged cases | A wrong action that was *not* flagged | The un-flagged bad case |
| L4 Autonomous | Executes and self-monitors | Sees aggregates only | A silent wrong action at scale | Full blast radius |

Then build the failure taxonomy for THIS product. Name the modes, not just "it failed". A starting set to adapt:

| Mode | What it is |
|---|---|
| Miss | Should have acted, didn't (false negative). |
| False alarm | Acted when it shouldn't (false positive). |
| Confidently wrong | Right shape, wrong content, stated with confidence. |
| Wrong format | Right content, unusable form. |
| Too slow / too dear | Correct but past the deadline or over budget. |
| Silent failure | Failed without signalling; no output, no flag. |

For each mode, set the acceptable rate by **derivation, not vibes**:

> acceptable_rate(mode) ≤ tolerable_cost_per_cycle(mode) ÷ cost_of_one_failure(mode)

A Miss in gas safety has a near-infinite cost-of-one-failure, so its acceptable rate collapses toward zero; a Wrong-format case costs a shrug, so its rate can be loose. Higher autonomy raises cost_of_one_failure (the human backstop is gone), which tightens every rate — that is why you do not start at L4. State the **gate to earn the next level**: the measured golden-case pass rate over N real cycles that must hold before autonomy goes up.

### Part 4 — Cost-per-outcome budget

Define the outcome as one completed unit of the job line — not one API call, not one token. Then fill to the cent:

> cost_per_outcome = (C_attempt × A) + C_human + C_remediation
>
> - C_attempt — model + infra cost of one attempt
> - A — mean attempts per outcome, retries included
> - C_human — reviewer minutes × loaded rate, at the chosen autonomy level
> - C_remediation — Σ over modes of accepted_rate(mode) × cost_of_one_failure(mode) that survives to production

Then the economic gate: **cost_per_outcome must be below value_per_outcome with margin.** If it is not, the spec fails here regardless of eval scores; lower the autonomy's human cost, tighten retries, or the wedge is not economic. Tag every dollar `[Fact]` (from a probe/quote) or `[Assumption]` (illustrative). The autonomy choice and this number are linked: lower autonomy adds human minutes, higher autonomy adds remediation cost — pick the level that *minimises* cost_per_outcome at an acceptable rate, not the one that sounds most advanced.

**Kill line.** A spec ships only with 20+ golden cases (correctly composed, ≥14 `[Fact]`, full mode coverage) AND a cost-per-outcome number to the cent checked against value. Fewer than 20 cases, or no cost-per-outcome number, is auto-fail. Report the gap; do not ship a partial spec as done.

## Evidence standard

Every Icarus skill weights behaviour and money over opinion. The ladder:

| Signal | Score |
|---|---|
| Money moved | 1.0 |
| Behaviour observed | 0.7 |
| Artefact shown | 0.5 |
| Verbal commitment | 0.3 |
| Opinion | 0.1 |

This skill applies the ladder to the golden set. A case labelled from a real input the system met — a probe log, a historical record, a live document — is `[Fact]` and scores ≥ 0.5; it earns a place in the 20. A case built from "an input a user would probably send" is `[Assumption]` (0.1–0.3) and counts against the 14-real floor. The pass/fail label itself must be checkable against ground truth (what actually happened, what the artefact actually said), never against "looks right". Cost numbers follow the same rule: a per-attempt cost measured on a probe is `[Fact]`; a projected reviewer rate is `[Assumption]` until a real pilot confirms it. Value-per-outcome argued from a customer's opinion (0.1) does not clear the economic gate; it needs behaviour or money.

## Gotchas

Twenty happy paths. The easiest way to fake this skill is 20 typical cases with a 100% pass rate and no case that can fail. The fixed spread (≥4 adversarial, ≥3 must-refuse) and the coverage rule exist to stop exactly that. A golden set with no failing cases has measured nothing.

Acceptable rate chosen to look safe. "We'll accept a 1% error rate" with no derivation is theatre. The rate is `tolerable_cost_per_cycle ÷ cost_of_one_failure`. If a fellow states a rate without stating cost-of-one-failure, the rate is unfounded — name it.

Autonomy inflation. Picking L3/L4 because it demos better, when a Miss at that level is catastrophic and no golden pass rate has earned it yet. Ship the lowest level that delivers the job; the ladder is climbed with measured evidence, not ambition.

Cost-per-call smuggled in for cost-per-outcome. "$0.02 per call" is not the budget. One outcome may take several attempts plus human review minutes plus remediation of the accepted failure rate. If the number ignores human time and retries, it is not cost-per-outcome and the kill line is not cleared.

Cases invented to reach 20. If the reality floor can't be met, the honest output is "you have 9 real inputs; go get 5 more from the next probe cycle," not 11 fabricated ones. Fabricated cases score a `[Assumption]` and, worse, teach the build to pass tests that describe no real user.

## Examples

`examples/sample.md` — a full worked eval-first spec for Mentix v1 (the shift-handover machine-risk digest): the job line with its judged-by clause, all 20 golden cases composed across the four bands and tagged for source, an L1 autonomy choice with a six-mode failure taxonomy and rates derived from cost-of-one-failure, and a cost-per-outcome budget of ~$3.55/shift checked against value-per-outcome — including one band that started under-real and forced a "go get more inputs" finding.

## Related skills

`wedge-five-questions` (06) — proves the wedge gets adopted. This skill specs the build of that wedge. Run wedge test first; this second.

`compound-system-architecture` (07, sibling) — the component pipeline and 40/20/30/10 effort split that *implements* this spec. This skill hands it the job line, the golden set, and the budget as constraints; it hands back the design. They compose; neither restates the other.

`pilot-six-term-sheet` (07, sibling) — carries this spec's success bar into the paid pilot as the "success metrics" term. The term sheet states the commercial KPI; this states the engineering pass/fail beneath it. Keep the boundary: pricing and conversion belong to the term sheet, not here.

Absorbs and beats `skills/concept/user-story` and `skills/concept/user-story-splitting`. It lifts their bones — testable acceptance criteria, vertical slices that each deliver value — and reframes them for probabilistic AI products: acceptance criteria become a 20-case scoreable golden set, vertical slices become an earned autonomy ladder, and a cost-per-outcome number is added that neither generic skill carries. Use this, not those, when specing an AI build.

Supersedes: none. New skill; no prior eval-first spec exists in the pack to replace.
