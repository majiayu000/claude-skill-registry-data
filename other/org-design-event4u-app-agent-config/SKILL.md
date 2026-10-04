---
model_tier: inherit
name: org-design
description: "Use when shaping team structure — functional vs squad, span-of-control, reorg cost, Conway-aware boundaries. Triggers on 'should we reorg', 'how do we split this team'."
status: active
tier: senior
domain: process
context_spine: [org-stage, product, customer-segment]
workspaces:
  - ops
packs:
  - ops-people
trust:
  level: professional
install:
  removable: true
---

# org-design

## When to use

- Team shape is becoming a bottleneck — handoffs are slow, decisions stall, the same conversations repeat across teams — and the question is *what structure unblocks*.
- A reorg is being proposed (often for a different stated reason) and the question is *what does this actually buy* and *what does it cost*.
- A new product line, segment, or geography is being added and the question is *fold it into existing teams* vs *spin a new team* vs *embed people across teams*.

Do NOT use as a hiring-plan substitute (route to forthcoming hiring-loop / comp skills for headcount and band shape), as a performance / individual-feedback surface (route to Q4 `perf-feedback-craft`), or for org-chart software / HRIS configuration.

## Cognition cluster

- **Mental model — Theory of constraints.** Org bottlenecks live in one or two places at a time; reorging everywhere else is theatre. Find the constraint (decision queue, dependency hub, single-threaded role), reshape around it, leave the rest. See [`mental-models.md`](../../../docs/contracts/mental-models.md).
- **Mental model — Conway's law.** Systems mirror the communication structure that shipped them. If two services must integrate cleanly, the two teams must communicate cleanly. Org boundary = future architecture boundary. Use the inverse: pick the architecture you want, then draw the org to match.
- **Mental model 28 — Inversion.** *"What problem does the proposed structure prevent us from solving?"* Every structure trades one class of problem for another. The honest question is which trade is acceptable, not which structure is best.
- **Mental model 26 — Optionality.** Reorgs cost 3–6 months of throughput; the reorg is worth it only if the new shape preserves more optionality than the old shape forecloses. Reorging for short-term symptoms usually destroys optionality.
- **Context-spine — org-stage + product + customer-segment.** Read **org-stage** for which problems are real (10-person co: structure barely matters; 50-person co: functional silos start; 150-person co: span-of-control breaks; 500+: Conway dominates). Read **product** for natural boundaries (modular product = squads work; tightly-coupled product = functional teams work better). Read **customer-segment** for whether segment-aligned teams pay off.

## Cross-wing handoff

- Composes P1 `build-buy-partner` for the insource-vs-outsource shape that affects whether a capability needs a team at all.
- Hands off to Q2 `comp-banding` for the level / band design that the new shape implies.
- Hands off to Q3 `onboarding-program` for the time-to-productivity shape that the new structure requires.
- Hands off to S-block EM skills for the team-level mechanics within the chosen structure.

## Procedure

### Step 0: Identify the real problem before redesigning anything

Most "we need to reorg" requests are misdiagnosed. Run three checks first:

1. *Is the symptom a structure problem, a leadership problem, or a strategy problem?* Reorgs solve only the first; the other two get worse with structural churn.
2. *Has the bottleneck been named with file:line precision?* (which decision, which handoff, which dependency, which role). Un-named bottlenecks = no real constraint identified.
3. *Has the smallest local fix been tried?* (move one role, redraw one boundary, add one decision-rights doc). A reorg is the heaviest tool; reach for it last.

If checks 1–3 don't justify a structural change, route the request elsewhere and stop.

### Step 1: Frame the structural options honestly

Four canonical shapes; each has trade-offs:

1. **Functional** — eng, design, PM, ops as separate orgs. Best for: deep specialisation, small co, shared platform. Cost: cross-functional handoff overhead.
2. **Cross-functional squad** — eng + design + PM bundled per product area. Best for: product-led shipping cadence, autonomous outcomes. Cost: duplicated capability, harder craft-leveling.
3. **Matrix** — functional reporting + squad allocation. Best for: balancing specialisation and outcome ownership. Cost: dual-reporting confusion, decision ambiguity.
4. **Segment-aligned** — teams own a customer segment end-to-end. Best for: deeply different segments with different jobs. Cost: code / platform divergence.

Hybrid shapes exist (squads inside functions; functional platforms under segment-aligned product teams); name them explicitly, don't hide them.

### Step 2: Read Conway, both directions

For the option in scope, draw the implied future architecture:

1. *Which interfaces become team-boundary interfaces?* (these calcify as contracts).
2. *Which integrations cross team boundaries?* (these slow down, gain meetings, accrete bureaucracy).
3. *Is the implied architecture the architecture we want?* If yes, the structure is honest; if no, redraw.

Inverse Conway: if the desired architecture has clean modules A, B, C, draw teams around A, B, C — not around skill specialisations that will fight the architecture.

### Step 3: Span-of-control and decision-rights audit

For each manager / lead in the proposed shape:

1. **Span** — how many direct reports. >7 is high-cost coaching; <4 is over-managed. Target 5–7 for engineering; varies for ops / design.
2. **Depth** — layers between IC and CEO. Above 4 layers in a sub-150 org = excess.
3. **Decision rights** — what does this role own vs need approval for? Un-named decision rights = stalls.
4. **Single-threaded role check** — is there exactly one owner per significant outcome? (Amazon's STO principle).

Span and decision-rights gaps are usually the actual fix, not a wholesale restructure.

### Step 4: Reorg cost sizing

For any structural change, name:

1. **Disruption window** — 3–6 months of degraded throughput is typical for non-trivial reorgs. Larger structural changes can take 9–12 months to settle.
2. **Attrition risk** — every reorg loses 5–15 % of impacted ICs to voluntary attrition; senior people more than juniors.
3. **Re-platforming cost** — if Conway implies architecture change, the eng cost of that change.
4. **Customer-facing disruption** — relationship continuity for account-aligned segments.

A reorg whose stated benefit is smaller than these costs = don't do it. Force the sizing before approving.

### Step 5: Validate the org-design read before emitting

Before producing the artifact, verify three things:

1. **Real-problem confirmation** — confirm Step 0 named the bottleneck with precision; un-named bottlenecks mean the reorg is theatre and must be re-run or abandoned.
2. **Trade-off honesty** — assert each proposed shape names what it foreclose s, not just what it enables; structures sold as pure upside fail the check.
3. **Cost sizing present** — verify Step 4 disruption / attrition / re-platforming / customer costs are sized in calendar units and % terms; un-sized reorgs are unrealistic and must be re-run.

All three must pass. If any fails, return to the failing step.

### Step 6: Emit the org-design read

Produce the org-design artifact for the leadership decision-maker. The artifact frames the bottleneck, the candidate shapes, the Conway implications, the span / decision-rights audit, and the sized cost. The decision stays human.

## Related Skills

**WHEN to use this**

- Reorg proposals (real or implied).
- Adding a new product line, segment, or geo and choosing fold-vs-spin-vs-embed.
- Span-of-control / decision-rights audits.

**WHEN NOT to use this**

- Hiring-plan / headcount shape — out of scope here; this skill answers *what shape*, hiring answers *how many of each*.
- Performance / individual-feedback work — route to [`perf-feedback-craft`](../perf-feedback-craft/SKILL.md) (Q4).
- Team-level engineering management — route to S-block EM skills.
- Compensation banding — route to [`comp-banding`](../comp-banding/SKILL.md) (Q2).

## When the agent should load this

- "Should we reorg?"
- "How do we split this team?"
- "Functional vs squad?"
- "Span-of-control read on engineering."
- "Wie strukturieren wir das Team neu?"

## Output

1. **`bottleneck-diagnosis.md`** — named constraint, evidence, smallest-local-fix check.
2. **`shape-options.md`** — candidate structures × what each enables × what each forecloses × Conway implications.
3. **`span-and-decision-rights.md`** — manager span audit, decision-rights mapping, single-threaded-role check.
4. **`reorg-cost-sizing.md`** — disruption window, attrition risk, re-platforming cost, customer-facing impact.

## Gotcha

- "We need a reorg" is usually a strategy or leadership problem in disguise. Diagnose first.
- Conway's law cuts both ways — pick the architecture, draw the org. Don't pick the org and hope the architecture follows.
- Matrix structures sound balanced and run terribly without explicit decision-rights docs.
- Reorgs done in <6-month cycles destroy more value than they create; structural change is a multi-quarter commitment.

## Do NOT

- Do NOT propose a reorg as the first response to a velocity / quality complaint; smaller fixes usually exist.
- Do NOT design a structure whose Conway-implied architecture you'd reject if drawn directly.
- Do NOT skip the cost sizing; un-sized reorgs are wishful.

## Runnable example

100-person SaaS, eng leadership claims "we need to move to squads because shipping is slow".

- Step 0 — Diagnose: shipping-slow is the symptom; bottleneck inspection shows two PMs serving 8 engineers each, decision queue at the PM layer, not the eng-design boundary. Smallest local fix: hire 2 PMs. Reorg not yet justified.
- Step 1 — Frame anyway as sanity check: functional vs cross-functional squad vs matrix.
- Step 2 — Conway read: current platform is modular by domain (billing / scheduling / reporting); squad-by-domain is Conway-aligned; squad-by-customer-segment would fight architecture.
- Step 3 — Span audit: VP Eng spans 9 direct reports (too wide); 1 EM has 11 reports (too wide); decision rights for "ship a public-API change" undefined.
- Step 4 — Reorg cost sizing: 4-month throughput drop, 8–12 % attrition risk on senior eng who joined for current shape, no re-platforming needed.
- Step 5 — Validate: bottleneck was misdiagnosed at the start; trade-off honest (squads cost shared-platform leveling); cost sizing present. Pass.
- Step 6 — Emit org-design read: recommend (a) hire 2 PMs to clear the actual bottleneck, (b) shrink VP Eng span by promoting an Eng Director, (c) write decision-rights doc for public-API changes, (d) revisit squad question in 6 months with fresh data. Net: smallest-fix path beats reorg by a wide margin.
