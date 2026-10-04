---
name: marshal-plan-consensus
description: >
  Reach a consensus on the APPROACH before committing a fleet to build it. Spawn several biased,
  independent solvers that each propose a plan for the same question, then an independent judge that
  converges them into one concrete plan (or narrows the question and re-runs). Use when the approach
  is contested - multiple valid designs, ambiguous scope, or a costly wrong turn - not for obvious
  work. The engine runs the agents; this playbook is the judgment. Hand the converged plan to
  marshal-orchestrate to build it.
---

# Reaching a consensus plan before you build

> **Related:** this skill *produces* a plan. To have one **judged** by a declared panel before you
> commit to it, `run_team(name, target="plan", text=...)` - see `marshal-adversarial-review`. Use
> that when the question is "is this plan sound?"; use the loop below when the question is still
> "what should the plan even be?"

When *what to do* is clear you just decompose and delegate (`marshal-orchestrate`). When *how to do
it* is contested - several plausible designs, fuzzy scope, an expensive-to-undo direction - you first
turn the question into an **evidenced plan** that survived independent scrutiny. The loop is **frame
-> solve (in isolation) -> judge -> converge or build.**

This is not one agent's plan. It is biased, independent, multi-angle convergence: each solver starts
from a different prior, proposes without seeing the others, and an independent judge arbitrates - it
never authors a fourth plan of its own.

## When to use
- A non-trivial goal where the approach is genuinely contested, or a wrong turn is costly (a schema,
  a public API, a migration strategy, a refactor boundary).
- Not for obvious tasks - reaching for consensus on a clear change is wasted spend; just orchestrate.

## The three rules that make it work
- **Biased.** Each solver holds ONE prior (below) and argues it. Don't ask one agent for "the best
  plan" - that collapses to a single opinion.
- **Independent.** Solvers must not see each other's plans. Spawn them together so they run in
  parallel isolation; only the judge reads all of them.
- **Sealed.** Each solver ends with one parseable line: `PLAN: propose|abstain - <one-line
  approach>`, above a short plan body (scope, files, key decisions, what it explicitly will NOT do).

## 1. Frame the question
Write ONE concrete, narrow question, plus the constraints/rules that govern it and the minimal files
or context a solver needs to answer. Vague questions produce vague plans.

## 2. Spawn the solvers (no-peek, read-only)
Route to read-only clients (they inspect the repo and produce a *plan*, not edits) and give each the
same question + its prior + the required `PLAN:` line. Run them together so they cannot see each
other:

```
run_many([
  {client: <read-only>, goal: MINIMAL_PRIOR    + question, task_id: "plan.<id>"},
  {client: <read-only>, goal: STRUCTURAL_PRIOR  + question, task_id: "plan.<id>"},
  {client: <read-only>, goal: DELETE_PRIOR      + question, task_id: "plan.<id>"},
])
```

Share one `task_id` so `usage()` / `report()` group the round. The priors:
- **minimal** - the smallest viable change that resolves the goal; explicitly do NOT over-engineer.
- **structural** - the structurally clean design; accept higher cost (a helper, an abstraction, an
  extra handoff) to land something an architecture review won't reject later.
- **delete** - question the necessity. Can this be solved by deleting or collapsing, or not built at
  all? If it must be built, `abstain` and let minimal/structural win.

## 3. Judge - converge, don't author
Feed the three sealed plans to one independent judge agent. It **arbitrates between the proposals**;
it must not invent a fourth design not present in any solver (that means it's solving, not judging).
It emits exactly one:
- `consensus` - the proposals agree (same boundary, same files, no contradictory choices). Output the
  one concrete converged plan.
- `converge` - they disagree but are close: narrow the question to the open disagreement and re-run
  step 2.
- `escalate` - genuinely stuck or the goal is ill-posed. Stop and bring it to a human.

Even when a direction looks obvious, run the gate: it turns a hunch into a plan with stated scope,
files, and non-goals.

## 4. Converge loop
On `converge`, re-run the solvers with the narrowed question. Cap at ~3 rounds. If a round makes no
progress (same split twice), `escalate` to a human or drop the goal - never loop forever.

## 5. Build
On `consensus`, the converged plan is your spec: hand it to `marshal-orchestrate` (decompose into
independent tasks -> spawn -> review -> integrate), and gate the result with `marshal-review-gate`
when the change warrants a quorum.

## Invariants to respect
- Solvers and judge are headless - the question + prior in the prompt is all they get; no questions.
- Independent means parallel + isolated; only the judge sees all plans, never a solver.
- The judge converges among the proposals; it never authors a new plan of its own.
- An obvious direction still passes the gate; cap the rounds and escalate - never loop forever.
