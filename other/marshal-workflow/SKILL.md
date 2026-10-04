---
name: marshal-workflow
description: >
  Author and run declarative YAML workflows on the Marshal fleet - reusable orchestration recipes
  (fan a goal out across clients, collect the diffs, then merge the good ones) that you run by name
  instead of re-planning each time. Use when the same multi-agent shape recurs (review, compare,
  fix-across-clients). For a one-off decomposition, use marshal-orchestrate instead. The engine runs
  the recipe by sequencing safe primitives; the judgment - which recipe, and which diff to keep -
  stays with you.
---

# Running Marshal workflows

A **workflow** is a named recipe stored as YAML under `<repo>/workflows/`. It captures an
orchestration you'd otherwise rebuild by hand each time: fan a goal out across several clients,
surface the resulting diffs, and (optionally) merge them. You run it by name with inputs; Marshal
executes the phases in order.

This is the repeatable cousin of **marshal-orchestrate**. Reach for a workflow when the *shape* is
stable and only the target changes ("review X", "implement Y across these models"). Reach for
marshal-orchestrate when the decomposition is bespoke to this one goal.

## The safety model (read this first)
A workflow **adds no new execution path**. Each phase is exactly a call you could make yourself -
`run_many` / `run_agent` / `collect_run` / `integrate` - so every run still gets an isolated git
worktree, a hard timeout + kill, and a usage-ledger entry. **Integration is gated off by default**:
an `integrate` phase with `auto: false` (the default) does *not* merge - it returns the candidate
runs in `next_actions` for you to review and merge yourself. `succeeded` is not `correct`; the merge
decision stays human.

## 1. Discover & validate
- `list_workflows` (MCP) returns `{workflows, errors, workspace}` — each recipe's name, inputs,
  and phases; malformed files land in `errors`.
- `marshal workflows` (CLI) lists them **and validates** each against your `fleet.config.yaml` -
  unknown client names, missing inputs, and unresolvable phases fail here, before any agent spawns.

## 2. The recipe schema
```yaml
name: review
description: Review a target across two clients; surface diffs to merge.
inputs: [target]                 # names usable as {target} in goals; must be supplied at run time
phases:
  - name: review
    run: fan_out                 # one run per client, in parallel
    clients: [reviewer-a, reviewer-b]
    goal: "Review {target} for bugs; apply fixes scoped to {target}."
  - name: gate
    run: collect                 # read-only: gather the prior phase's diffs
  - name: merge
    run: integrate               # auto: false (default) -> report candidates, never auto-merge
```
Phase kinds:
- `fan_out` - `goal` across `clients` (parallel). `agent` - `goal` on one `client`.
- `collect` - surface a prior generative phase's diffs (read-only; never stops the run).
- `integrate` - merge succeeded runs **only if `auto: true`**; default reports candidates.

`collect`/`integrate` source the **most recent preceding** `fan_out`/`agent` phase, or set
`from_phase: <name>` to point at a specific earlier named phase. Goals substitute `{input}` tokens
only (literal braces must be doubled: `{{`).

## 3. Run it
`run_workflow(name, inputs)` - e.g. `run_workflow("review", {"target": "src/auth.py"})`. It validates
the whole recipe first, then runs each phase. The result carries `workflow_run_id`, per-phase
records/diffs, a `status`, and `next_actions`.

## 4. Read the gate, then merge
- `status`: `completed` (nothing left), `awaiting_review` (diffs and/or gated integrate candidates
  to act on), or `error` (the workflow did not do what it was asked - an agent run failed or timed
  out, its work could not be read, or an auto-integrate hit a state needing a human). `completed`
  means every phase did its job: a run that failed makes the workflow an `error`, never a quiet
  success.
- Work the `next_actions` list. For each candidate, read its diff (`collect_run`) - you are the
  reviewer - then `integrate(run_id)` the ones worth keeping, **one at a time**. Reject the rest by
  simply not integrating; their worktrees stay isolated and main is untouched.
- A fan_out shares one `task_id` per phase, so `report(task_id)` / `usage()` compare what each client
  cost on the same task.

## Authoring tips
- Keep clients in a `fan_out` working on the **same** target - they're alternatives to compare, or a
  review you'll merge once. Independent *parallel* edits to different files belong in
  marshal-orchestrate (or separate phases), to avoid merge collisions.
- Start templates from `examples/workflows/` (`review.yaml`, `compare.yaml`); copy into
  `<repo>/workflows/` and swap in your client names.
- Default to gated integrate. Only set `auto: true` when the recipe is trusted and the runs are
  genuinely independent - and even then, expect `awaiting_review` on any conflict/blocked outcome.
