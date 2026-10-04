---
name: researchforge-plan
description: Design experiment variants for a hypothesis — write patches, import the plan for validation, and get it approved. Use after a baseline exists, when the user wants to plan or implement experiments.
---

# Plan experiments

You author the plan and patches; the engine validates every layer before
anything can run. One plan targets one hypothesis.

## 1. Export planning context

```bash
researchforge experiment plan <hypothesis-id> --json
```

This writes `.researchforge/experiments/context.json`: the hypothesis, the
approved contract (metric, constraints, **editable and protected paths**,
limits), baseline metrics, repository scan, and the embedded schema for the
plan file. Read it fully before writing anything.

## 2. Write the plan and patches

- `.researchforge/experiments/plan.yaml` conforming to the embedded schema:
  `hypothesis_id`, `approach_summary`, and one entry per experiment
  (`key`, `title`, `change_summary`, `patch_file`).
- One unified diff per variant under `.researchforge/experiments/patches/`,
  applying cleanly to the frozen baseline commit.

Hard constraints the engine enforces (do not fight them):

- patches may only touch `permissions.editable_paths`; a patch touching a
  protected path is recorded as **rejected** at import and will never run —
  never edit benchmarks, evaluation code, or `.researchforge/` to make a
  metric look better;
- changed files are extracted by git from the patch itself, never from your
  description;
- keep variants small and single-idea: the funnel measures one change at a
  time;
- to BUILD ON a prior result, set `parent:` on an entry (another key in this
  plan or an `exp-NNN` from the context's `prior_experiments`) — the
  parent's patch chain is applied first and your diff must be written
  against that combined state. A branched child's improvement is still
  measured against the baseline; report its increment over the parent
  separately and honestly.

## 3. Import (engine validates, six layers)

```bash
researchforge experiment import .researchforge/experiments/plan.yaml --json
```

On failure, the `--json` payload lists exactly what to fix (schema fields,
unknown hypothesis, patch that does not apply, protected-path violations).
Fix the plan or patch files and re-import.

## 4. Approval — the user's decision

Show the user the imported plan (`researchforge experiment show <plan-id>
--json`), including worst-case wall time, then ask them to run:

```bash
researchforge experiment approve <plan-id>
```

Only use `--yes` if the user explicitly approved this plan in this
conversation. Next: the researchforge-run skill executes the funnel.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
