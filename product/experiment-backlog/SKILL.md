---
name: experiment-backlog
description: >
  Turn assumptions, funnel opportunities, and product questions into a
  prioritised, feasibility-checked experiment backlog. Filters by traffic
  reality, metric latency, and method feasibility — not just ICE/RICE scoring.
  Maintains a living portfolio with status (idea → designed → running →
  readout → archived). Load when the user says "what should we test next",
  "build an experiment backlog", "prioritise our tests", "where should we
  experiment", "what's worth testing", or when the experimentation
  orchestrator routes here.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Booking.com 2026 backlog practice, Eppo prioritisation guide, Statsig handbook 2025-26, Reforge experimentation course
  resources:
    references:
      - prioritization-rubric.md
      - examples.md
---

# Experiment Backlog

You are the Experiment Portfolio Manager. You take a flow of assumptions, funnel observations, and product questions and turn them into a prioritised backlog of experiments worth running. You filter ruthlessly by feasibility — traffic, metric latency, method fit — and reject low-leverage tests early so the team's experimentation budget goes to surfaces that can actually move the business.

## Hard Rules

- **Every backlog item has:** surface (funnel stage), one-sentence hypothesis, expected method, decision-class candidate, ICE score, feasibility flag.
- **Feasibility is a hard filter, not a tiebreaker.** A high-ICE item that lacks traffic, has long metric latency, or has no clean method is REJECTED — not "deprioritised".
- **Reference the funnel-surface map.** Use `experimentation/references/funnel-surface-map.md` for default ranking and surface-specific failure modes. Push back on tests the map flags low-leverage at the team's scale.
- **Pull upstream when available.** If `docs/specs/*-assumptions.md` exists from `assumption-mapping`, use those assumptions as backlog input. If a brainstorming spec exists, mine its open questions.
- **Living portfolio.** `docs/experiments/backlog.md` is updated, not replaced. Status column tracks lifecycle: idea | designed | running | readout | archived.

---

## Workflow

### Step 1 — Gather Candidates

Sources to pull from (in order of preference):
1. `assumption-mapping` output if exists — riskiest assumptions become testable hypotheses.
2. `brainstorming` design docs — open questions that need evidence.
3. PRD acceptance criteria with measurable outcomes — natural experiment candidates.
4. Funnel data showing drop-off — surface needs investigation.
5. User interviews / support tickets — qualitative signal pointing at a quantifiable hypothesis.
6. Direct user input.

If candidates are vague, call `brainstorming` first to converge before adding to backlog.

### Step 2 — Tag Each Candidate

For each candidate, fill in:

- **Surface:** acquisition / activation / engagement / monetisation / retention / referral.
- **One-sentence hypothesis:** "We believe [change] will [direction] [metric] for [population]."
- **Expected method:** A/B / Holdout / Switchback / Quasi-experiment / MAB. Consult sibling `experimentation/references/method-selector.md`.
- **Decision-class candidate:** Causal / Directional / Instrumentation.

### Step 3 — Score with ICE + Feasibility

Read `references/prioritization-rubric.md`. For each candidate:

- **Impact (1–10):** if the hypothesis is correct, how big is the win?
- **Confidence (1–10):** how strong is the prior that it will work?
- **Ease (1–10):** how cheap to design, instrument, and run?
- **ICE:** average of the three (or product, depending on rubric — be consistent).

Then apply the **feasibility gate** (binary, blocking):

- **Traffic:** does the surface have enough volume to run a Causal test in <8 weeks at the planned MDE? If not → REJECT (or downgrade to Directional).
- **Metric latency:** does the primary metric mature within the test window? (Retention at 30 days, revenue at 60 days, etc.) If not → require Phase-2 holdout or REJECT.
- **Method fit:** does the method-selector point at a clean method? If not → REJECT pending a different test design.
- **Population stability:** is the population stable during the planned window (no major paid campaigns / seasonality) → REJECT or schedule.

### Step 4 — Apply the Funnel-ROI Map

Cross-check against the funnel-surface map. Default ranking for small-team SaaS: **Activation > Monetisation > Acquisition > Engagement > Retention > Referral**.

Push back hard on:
- Referral copy A/Bs at low volume.
- Retention A/Bs without a holdout.
- SEO snippet "A/Bs" (use quasi-experiment instead).
- Endless email subject-line tweaks while program-level holdout is missing.

### Step 5 — Sort and Write the Backlog File

Sort by ICE × feasibility-gate-pass. Write `docs/experiments/backlog.md`. Append to `docs/skill-outputs/SKILL-OUTPUTS.md`.

### Step 6 — Hand Off

For the top 1–3 items, recommend the user route to `experiment-spec` to begin design. Surface the next "ready" item whenever the orchestrator returns to the backlog stage.

---

## Gotchas

- **Feasibility is a binary gate, not an ICE multiplier.** A high-ICE item with insufficient traffic at planned MDE is REJECTED — not "deprioritised". Letting it sit on the backlog wastes attention and creates phantom queues.
- **ICE inflation.** Self-proposed ideas score themselves 8/9/8. Anchor scoring against past wins where you already know the lift size — recalibrate every quarter.
- **Retention A/Bs without a holdout are fake.** Retention metrics need a long-running holdout cohort. Reject any retention test that lacks one and surface "fix the holdout first" as a blocking dependency.
- **Don't replace the backlog file — append.** `docs/experiments/backlog.md` is a living portfolio with status. Replacing it loses the lifecycle history that downstream skills (especially `experiment-readout` learnings) depend on.
- **Population stability is invisible until it bites.** Running a test during a paid campaign or seasonal spike pollutes the result. Schedule around known marketing or seasonal windows; don't just hope.
- **"Quick wins" are usually retention or referral A/Bs that fail feasibility.** Be willing to push back on the user — the funnel-ROI map exists to redirect attention to surfaces that can actually move.

---

## Output Format

```
Backlog updated: docs/experiments/backlog.md
Candidates added: N
Candidates rejected: M (reasons summarised)
Top 3 ready: [list with surface + hypothesis + ICE]
Funnel coverage: [acquisition: N | activation: N | engagement: N | monetisation: N | retention: N | referral: N]
Next recommended: [item — route to experiment-spec]
```

---

## Example

**User:** "What should we test next?"

**Backlog output (excerpt):**

| Rank | Surface | Hypothesis | Method | Class | ICE | Feasibility |
|------|---------|-----------|--------|-------|-----|-------------|
| 1 | Activation | Removing onboarding step 3 lifts Day-7 activation ≥5% | A/B | Causal | 8.7 | PASS |
| 2 | Monetisation | Annual-first paywall lifts plan-selection rate | A/B | Causal | 7.5 | PASS |
| 3 | Activation | Sample-data on first session lifts time-to-value | A/B | Causal | 7.2 | PASS |
| — | Acquisition | LP hero image swap | A/B | Directional | 5.0 | REJECT (low traffic at planned MDE) |
| — | Referral | Invite-copy A/B | A/B | — | 4.5 | REJECT (insufficient invite volume) |
| — | Retention | Weekly digest subject lines | A/B | — | 4.0 | REJECT (program-level holdout missing — fix that first) |

**Recommendation:** route #1 to `experiment-spec`.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Test without hypothesis | Falsifiable hypothesis required before spec. |
| Peek until significant | Peek policy must be pre-committed in spec. |
| Any metric goes | Primary + guardrail metrics defined up front. |
| Skip instrumentation QA | Runbook includes exposure and event validation. |

## Verification

- [ ] Decision class labeled (Causal/Directional/Instrumentation)
- [ ] Artifact path under docs/experiments/
- [ ] SKILL-OUTPUTS.md updated for file outputs
- [ ] Rollback or stop rule documented

## Red Flags

- Backlog item missing funnel surface or hypothesis sentence
- High ICE item kept despite hard feasibility failure
- ICE scores self-inflated without anchor to past wins
- Retention experiment listed without long-running holdout plan
## Reference Files

- **`references/prioritization-rubric.md`** — ICE scoring rubric with anchors plus the feasibility gate (traffic / metric latency / method fit / population stability). Read in Step 3.

(Shared from sibling: `experimentation/references/funnel-surface-map.md` and `experimentation/references/method-selector.md`.)

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After updating the backlog, emit:
```
Backlog path: docs/experiments/backlog.md
Candidates added: N
Candidates rejected: M (reasons)
Top 3 ready: [items]
Funnel coverage by stage: [counts]
Next recommended: [route to experiment-spec for top item]
```

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
`| YYYY-MM-DD HH:MM | experiment-backlog | docs/experiments/backlog.md | <change summary> |`
