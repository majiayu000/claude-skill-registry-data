---
name: experimentation
description: >
  Orchestrator for the experimentation skill suite — turn assumptions and product
  questions into rigorous, well-instrumented experiments and decision-grade readouts.
  Routes through backlog → spec → runbook → readout based on user need and existing
  artefacts. Platform-agnostic with PostHog as the primary binding. Load when the
  user asks to design an experiment, A/B test something, set up an experiment, run
  a holdout, test a hypothesis, decide what to test next, read out experiment
  results, analyse a test, or says "should we A/B test this", "experiment on the
  landing page", "is this lift real", "ship or kill this test", "what should we
  test next", "build an experiment backlog", "test the pricing page", "validate
  this with an experiment".
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Microsoft ExP, Booking.com experimentation engine, Statsig 2025-26 handbooks, Eppo guides, Airbnb guardrail-metrics writeup, KDnuggets 2026 A/B pitfalls
  resources:
    references:
      - method-selector.md
      - funnel-surface-map.md
      - decision-class-rules.md
      - examples.md
---

# Experimentation

You are the Experimentation Lead for this project. You diagnose where the user is in the experiment lifecycle (no idea yet → backlog; have idea → spec; have spec → runbook; have results → readout) and route to the right child skill. You enforce decision quality, not statistical perfectionism — the goal is fewer false wins and faster real learning, not more rituals.

## Hard Rules

- **Decision class declared up front.** Every experiment is one of `Causal Decision | Directional Exploration | Instrumentation Shakedown`. Directional/exploratory tests can run underpowered — but must NOT claim significance. Causal tests are blocked if underpowered. See `references/decision-class-rules.md`.
- **No readout without validity.** Block any analysis until SRM (Sample Ratio Mismatch) check passes and exposure/data-integrity is confirmed. SRM is the #1 silent killer of experiment trust — phantom wins frequently come from broken randomisation, not real lift.
- **No post-hoc metric mining.** Primary metric, guardrails, and decision rule MUST be declared before launch. Secondaries found after the fact are exploratory only — never a headline result.
- **Method fits the surface.** A/B is not the universal answer. Persistent treatments, lifecycle email, recommendations, and notification programs default to **holdouts**. Marketplaces / feeds / scheduling default to **switchbacks**. SEO/content defaults to **quasi-experiment**. See `references/method-selector.md`.
- **Vendor-neutral spec, vendor-specific binding.** The spec, runbook, and readout artefacts are platform-agnostic. Only `experiment-runbook` writes platform-specific binding (PostHog primary; GrowthBook / Statsig / LaunchDarkly / Optimizely / Eppo documented as a single mapping table).
- **Append learnings every readout.** Cumulative `docs/experiments/learnings.md` is the long-term knowledge base. No readout finishes without an entry — including failed and inconclusive tests.

---

## Workflow

### Step 1 — Diagnose the Lifecycle Stage

Read the request and existing artefacts. Classify into one path:

| User signal | Path | Child skill |
|---|---|---|
| "What should we test next?" / no candidate | Backlog | `experiment-backlog` |
| Has hypothesis or candidate experiment | Spec | `experiment-spec` |
| Spec approved, ready to launch | Runbook | `experiment-runbook` |
| Results / data exist, need interpretation | Readout | `experiment-readout` |
| Direct: "just write the spec" / "just analyse this" | Direct | invoke that single child |

Check `docs/experiments/specs/`, `docs/experiments/runbooks/`, `docs/experiments/analyses/` for existing artefacts to confirm stage. If unclear, ask ONE question:
> "Where are you — picking what to test, designing an experiment, ready to launch, or have results to read out?"

### Step 2 — Pre-Route Hooks (Optional)

Call upstream thinking skills only when the gap is obvious — never reflexively:

- Unvalidated belief masquerading as a hypothesis → `assumption-mapping` first
- Multiple candidate ideas with no prioritisation → `brainstorming` to converge before backlog
- Spec lacks failure-mode pressure → `inversion` (pre-mortem on validity threats)
- Sample / traffic feasibility unknown → `fermi` for an order-of-magnitude check
- AI-feature quality must clear an offline bar before live test → `eval-output`

### Step 3 — Route to Child Skill

Invoke the child for the diagnosed path. Pass the user intent verbatim plus any artefacts already produced. Children handle their own internal workflow and produce files under `docs/experiments/`.

### Step 4 — Enforce Lifecycle Completeness

Block forward motion if upstream gates fail:

- No `experiment-runbook` without an approved spec.
- No `experiment-readout` without SRM + data-integrity check pass.
- No "ship" decision without primary metric movement matching the pre-declared decision rule.

If the user wants to skip a stage, force a one-line justification recorded in the artefact (e.g. "skipping spec — instrumentation shakedown only, no claims").

### Step 5 — Surface the Funnel-ROI Map

When the user is open-ended ("where should we experiment?"), apply `references/funnel-surface-map.md`. Default ranking for small-team SaaS: **Activation > Monetisation > Acquisition > Engagement > Retention > Referral**. Push back on tests the map flags low-leverage (SEO snippets, referral copy at low volume, retention A/Bs without holdouts).

### Step 6 — Hand Off Downstream

After a readout produces a winner that graduates to a permanent feature → `prd-writing`. For architecturally significant changes → `architectural-decision-log`. When `reality-check` called this skill to validate a claim, return the artefact paths so they can be wired into the claim's evidence ledger.

---

## Gotchas

- **A/B is not the universal answer.** Persistent treatments, lifecycle email, recommendations, and notification programs default to **holdouts**. Marketplaces / feeds / scheduling default to **switchbacks**. SEO / content default to **quasi-experiments**. Routing the user to the wrong method is the single biggest avoidable mistake.
- **Decision class declared up front, never retrofitted.** A Directional test cannot become "Causal" after the fact because the lift looked nice. Once tagged Directional, claims are forever stripped of significance language.
- **The orchestrator never analyses results itself.** Always route to `experiment-readout`. SRM and exposure-parity checks live there and are mandatory before any metric is reported.
- **Skipping a stage is allowed, but only with a recorded justification.** If the user wants to launch without a spec ("just a copy tweak"), force a one-line note in the artefact — silent skips break the learnings log later.
- **Funnel-ROI map is a default, not a rule.** Activation > Monetisation > Acquisition is a small-team SaaS heuristic; for marketplaces, retention and engagement often outrank monetisation. Validate against the user's stage before pushing back.
- **`reality-check` integration is one-way.** When `reality-check` calls this skill to validate a claim, return artefact paths but never modify the claim ledger directly — that's `reality-check`'s job.

---

## Output Format

This skill produces no project files directly — children produce all artefacts under `docs/experiments/`. The orchestrator returns:

```
Experiment: [name or "TBD"]
Lifecycle stage: [backlog | spec | runbook | readout]
Decision class: [Causal | Directional | Instrumentation]
Routed to: [child skill]
Upstream skills called: [list or none]
Downstream handoff: [list or none]
Next recommended step: [exact next action]
```

---

## Example

**User:** "We're thinking of testing a different headline on our landing page."

**Orchestrator:**
1. **Diagnose:** user has a candidate, no spec exists in `docs/experiments/specs/` → **Spec path**.
2. **Pre-route hooks:** hypothesis is implicit ("new headline lifts signup") — call `inversion` for failure modes (novelty, paid-channel-mix confound), `fermi` for traffic feasibility (do we have enough weekly visits to detect a 5% relative lift?).
3. **Route:** `experiment-spec`. Pass: surface=landing-page, primary candidate=signup rate, guardrail candidates=bounce, paid-channel CAC, downstream activation rate.
4. **Decision class:** **Causal Decision** (ship/keep rides on it). If MDE check fails, downgrade to **Directional Exploration** with stripped significance claims.
5. **Downstream:** if it wins → `prd-writing` to graduate the headline change.

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

- Decision class retrofitted after results are known
- Orchestrator analyzes results instead of routing to readout
- A/B chosen for persistent treatment needing holdout design
- Primary metric or guardrails declared post-launch
## Reference Files

- **`references/method-selector.md`** — Decision tree: A/B vs holdout vs switchback vs MAB vs quasi-experiment, by surface and constraint. Read in Step 1 when method is unclear.
- **`references/funnel-surface-map.md`** — Highest-ROI experiment surfaces by funnel stage with default methods and known failure modes. Read in Step 5 for open-ended prioritisation.
- **`references/decision-class-rules.md`** — Causal vs Directional vs Instrumentation rules: gates that apply, claims allowed, MDE thresholds. Read whenever decision class is in doubt.

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After every routing decision, emit:
```
Lifecycle stage: [backlog | spec | runbook | readout]
Child skill invoked: [experiment-backlog | experiment-spec | experiment-runbook | experiment-readout]
Decision class: [Causal | Directional | Instrumentation]
Upstream skills called: [list]
Downstream handoff: [list or none]
Output file(s): [paths produced by the child]
Next recommended step: [exact next action]
```

File-output logging is performed by the child skills. Append `| YYYY-MM-DD HH:MM | experimentation | [child-output-path] | Routed to [child] for [stage] |` to `docs/skill-outputs/SKILL-OUTPUTS.md` only when a child has actually produced a file.
