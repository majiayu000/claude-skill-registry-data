---
name: researchforge-baseline
description: Set up the experiment contract and run the frozen baseline benchmark. Use when an improve-repository project needs its evaluation defined, the contract approved, or the baseline measured.
---

# Contract and baseline

The contract (`researchforge.yaml` at the repository root) freezes the
evaluation: primary metric + direction, hard constraints, editable vs
protected paths, commands, resource limits, network mode, shipping flags.
Approval hashes it; later edits are detected as drift and refused until
re-approved. **The contract is the boundary — experiments can only change
`editable_paths` and are judged only by the contracted benchmark.**

## 1. Draft the contract

```bash
researchforge contract generate --json
```

Then edit `researchforge.yaml` **with the user** — these are their choices,
not yours: the benchmark command (`execution.full_command`) must print or
write a machine-readable result (`execution.result_file`), the primary
metric must match a key in that result, and `permissions.editable_paths` /
`protected_paths` decide what experiments may touch. Benchmarks and
evaluation code belong in `protected_paths`.

## 2. Validate and approve

```bash
researchforge contract validate --json
```

Fix any of the semantic errors it reports (they are field-level and
actionable). Then show the user a summary of what they are approving —
metric, constraints, commands, limits, paths — and ask them to run:

```bash
researchforge contract approve
```

The approval is a typed confirmation. Only run it with `--yes` yourself if
the user has explicitly said in this conversation to approve this contract.

## 3. Run the baseline

```bash
researchforge baseline run --json
researchforge baseline show --json
```

The baseline runs in an isolated detached worktree; the user's checkout is
never touched. Report the recorded baseline metrics from the JSON. All
future experiments are compared against this frozen measurement.

Next: the researchforge-plan skill designs experiments against a hypothesis.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
