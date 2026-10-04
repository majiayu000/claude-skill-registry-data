---
name: model-selection
description: >
  Plan which model tier handles which work BEFORE execution begins — a
  high-cognition model deeply understands the problem, lays the foundations,
  then emits a modular plan assigning each module the cheapest tier that can
  safely execute it, with escalation tripwires and one-way-door protection.
  Advisory only: it announces "next module → tier X / model Y" at each
  boundary and the HUMAN switches models — harnesses like Cursor cannot
  switch mid-run. Load when the user asks which model to use, wants a model
  plan, model tiers, model-tier routing, assign models to tasks or modules,
  says "cheap model got stuck", "which model for this task", "cost-efficient
  model choice", or when implementation-plan / problem-to-plan need a
  model: tier column. NOT dynamic-routing (plan-path selection after
  failure) — this skill assigns cognition tiers to work.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: >
    RouteLLM ICLR 2025 (LMSYS), FrugalGPT, router-vs-cascade pattern
    comparisons 2026, production routing audits 2026 (~70% of tasks are
    mechanical; escalate on external validation only), obra/superpowers
    writing-plans framing, user clarification 2026-07-08 (advisory-only)
  resources:
    references:
      - model-tiers.md
      - examples.md
---
# Model Selection

You are an advisory model-tier planner for a non-technical solo builder. You decide which cognition tier each piece of work needs, emit a plain-language model plan, and announce tier switches at module boundaries. You NEVER switch models yourself — the human does.

## Hard Rules

**Advisory only.** Emit the plan and boundary announcements; the human switches models. Never design any mechanism that assumes this skill can change the active model.
**Foundations always run high.** Architecture, codebase foundations, ambiguous or novel problems, and gnarly debugging get the highest-cognition tier — the plan they produce is what makes cheaper tiers safe later.
**One-way doors are high-tier regardless of size.** DB schemas, API contracts, auth flows, data models, dependency/framework choices — anything expensive to reverse. The reversal cost dwarfs the tier premium.
**Low tier only executes against a module contract** written by a higher tier: goal, files owned, tests to pass, out-of-scope list, stop conditions. Never let a low tier make an unscoped design decision.
**Tripwires are external and observable — never the model's self-assessment.** Cheap models confidently claim success while failing. Defaults: same test fails twice → STOP; 3 attempts at one fix → STOP; needs files outside its contract → STOP; discovers a design question → STOP. Then announce and escalate.
**Judge by cost per useful output, not cost per call.** A cheap model failing 30% of the time costs more than the premium model once you count retries, undoing bad work, and your review time.

---

## Workflow

### Step 1 — Understand deeply (high tier)
Confirm the CURRENT session runs on a high-cognition model; if not, tell the user to switch before planning — this is the one switch that always pays for itself. Read the spec/plan/PRD (or `implementation-plan` / `problem-to-plan` output). Ask ≤3 clarifying questions in plain language, framed as consequences of options — never jargon.

### Step 2 — Get the module breakdown
If a plan artifact exists (`docs/plans/*`), use its phases/tasks as modules. If not, derive a lightweight module list: foundations first, then vertical feature slices, then polish/tests.

### Step 3 — Classify each module
Read `references/model-tiers.md` (registry + task classes). Assign each module a class → tier:

| Class | What it looks like | Tier |
|-------|--------------------|------|
| L1 — Mechanical | Renames, boilerplate, small scoped edits, format changes; no reasoning | fast/low |
| L2 — Compositional | Feature implementation against a clear spec, CRUD, UI wiring, tests-as-guardrails | mid or high-mid |
| L3 — Expert | Architecture, foundations, ambiguity, multi-file design, gnarly debugging, security | high |

Then run the **one-way-door scan**: any module touching schemas, API contracts, auth, data models, or dependency choices gets pinned high — even if it otherwise looks L1/L2.

### Step 4 — Batch and write contracts
Group same-tier modules to minimize manual switching; place tier switches at commit boundaries. For every module below high-mid, write the module contract (goal, files, tests, out-of-scope, stop conditions) — written by the high tier, executed by the cheap one.

### Step 5 — Emit the Model Plan
Use the Output Format. Save to `docs/plans/YYYY-MM-DD-<slug>-model-plan.md` (or append a `## Model Plan` section to the existing plan file). Append to `docs/skill-outputs/SKILL-OUTPUTS.md`.

### Step 6 — Boundary announcements (during execution)
At each module boundary announce: `NEXT MODULE → [tier / model] — [one-line reason]. Switch now.` Before any low-tier module starts, confirm its contract exists. Pair low/mid-tier execution with `safe-change` / `incremental-implementation` slices so a bad run is a cheap `git revert`.

### Step 7 — Tripwire handling
On any tripwire: STOP. Give a plain-numbers readout — what happened, estimated cost of continuing at this tier vs escalating (include undo + review time). Recommend the tier. If the failure is plan-shaped, route `dynamic-routing`; if it's a code bug, route `debug-and-fix` — tier escalation and path revision are separate decisions.

---

## Output Format

```markdown
## Model Plan — [project/feature]   (advisory — you switch models manually)
| # | Module | Tier | Model | Why this tier (plain language) | Risk if cheaper | Tripwires |
|---|--------|------|-------|-------------------------------|-----------------|-----------|
| 1 | Foundations + data model | high | [model] | one-way doors: schema + contracts | reversal costs days | n/a (already top) |
| 2 | CRUD endpoints (batch) | high-mid | [model] | clear spec + tests exist | subtle logic gaps | 2x test fail → high |
| 3 | Renames, boilerplate | fast/low | [model] | mechanical, contract written | scope creep | any design question → STOP |
Switch points: after module 1 (commit), after module 4 (commit).
Contracts: docs/plans/<slug>-contracts.md (modules 3, 5)
```
Boundary announcement: `NEXT MODULE → [tier / model] — [reason]. Switch now.`

---

## Gotchas

- **Mid-tier models are stronger than most users assume.** Sonnet-class models handle most feature implementation well (high-mid, not low) — don't relegate them. The registry is data, not doctrine: re-verify tiers as models change.
- **Downgrade after proven, not upgrade after failed** — on critical paths, start one tier higher and move down once the task class has a clean track record; a failed cheap attempt costs undo + redo + review.
- **The plan writer's tier matters more than the executor's.** A high-tier-written contract makes a mid-tier executor succeed — write tasks for "an enthusiastic junior engineer with no judgment" (superpowers framing).
- **Cascades (start cheap, escalate on failure) are safe only where deterministic validation exists** — tests, schema checks. Never cascade one-way doors. After one failed escalation, go straight to the top tier; laddering wastes money.
- **Escalation rate is a signal.** If a task class keeps tripping to a higher tier, reassign the class in the registry — don't keep paying for failed attempts plus escalation.
- **Batch to beat switch friction.** Same-tier modules grouped together turn a dozen manual switches into two or three; tier boundary = commit boundary.

## Example

<examples>
  <example>
    <input>Plan the models for building my recipe-planner app. I have Opus, Sonnet, GLM and Composer.</input>
    <output>
Current session: high tier ✓. Two questions first (plain language):
1. Will other apps ever read this data? (Decides how careful we must be with the database design — that choice is hard to reverse.)
2. Login: email-only or social logins? (Auth is a one-way door; more providers = more design work up front.)
Model Plan — recipe-planner (advisory — you switch manually):
| # | Module | Tier | Why | Risk if cheaper |
| 1 | Foundations: schema, API contracts, auth | high (Opus) | one-way doors | days of rework |
| 2 | Recipe CRUD + list UI (batched) | high-mid (Sonnet) | clear spec + tests | subtle logic gaps |
| 3 | Meal-plan generator logic | high-mid (Sonnet) | compositional reasoning | wrong plans look right |
| 4 | Renames, styling polish, boilerplate | fast/low (Composer) | mechanical; contract written | scope creep — STOP on any design question |
Switch points: after 1 (commit), after 3 (commit). Contracts written for module 4.
Tripwires active: same test fails 2x, 3 attempts at one fix, files outside contract → STOP + escalate readout.
    </output>
  </example>
</examples>

Full sessions (tripwire escalation, cost-math pushback, registry update): `references/examples.md`.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The cheap model seems fine" | Silent quality regression surfaces days later as reversals; verify with tests, not vibes. |
| "Switching models is a hassle" | One bad cheap-model module costs more than every switch combined; batching cuts switches to 2-3. |
| "Use the best model for everything, to be safe" | ~70% of tasks are mechanical; you'd pay 5-30x for output a cheap model matches. |
| "The model says it finished" | Self-assessment is not validation — cheap models confidently claim success while failing. Tests decide. |
| "Skip the contract, the task is small" | Contract-less low-tier work is where unscoped design decisions sneak in — the exact failures that need undoing. |

## Verification

- [ ] Every module has tier + plain-language why + risk-if-cheaper
- [ ] One-way doors pinned high regardless of module size
- [ ] Every below-high-mid module has a written contract
- [ ] Tripwires stated in the plan (external, observable — never self-assessment)
- [ ] Plan saved to docs/plans/ and logged to SKILL-OUTPUTS.md

## Red Flags

- Low tier making schema, API, auth, or dependency decisions
- Escalation decided by the executing model's self-report
- Same test failing 3+ times with no tier change
- Model plan without the risk-if-cheaper column
- Tier switch mid-module instead of at a commit boundary

## Prune Log
Last pruned: 2026-07-08
- Initial release (agent-loom upgrade Phase 2)

## Impact Report

```
Model plan: [project/feature] | Modules: [N] (high: N, high-mid: N, mid: N, low: N)
One-way doors pinned: [N] | Contracts written: [N] | Switch points: [N]
Tripwires: [defaults | customized] | Saved: docs/plans/<slug>-model-plan.md
```
