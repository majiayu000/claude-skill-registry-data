---
name: execute-plan
description: Execute a plan from .agentic/specs/ with per-step test gating, evidence-based quality gates, and spec lifecycle handling through to an MR.
user-invocable: true
disable-model-invocation: false
argument-hint: "[plan file — defaults to most recently modified plan-*.md in .agentic/specs/]"
---

# Execute a plan

## Step 0 — Branch

- Fresh context first: if this session already carries a long unrelated
  conversation, suggest the user `/clear` (or open a new session) and re-invoke
- Start from the plan's base, not from wherever the session happens to sit: switch
to the branch named in the spec's `planned-against:` header, pull it, then create `feature/<plan-slug>` from there. 
- Never build on a protected branch (the `protect-main` hook blocks it anyway) — and never on an
unrelated feature branch: that silently merges its in-flight work into this
plan's diff. If `feature/<plan-slug>` already exists, you're resuming — switch
to it and continue.

## Step 1 — Load & announce

Load the plan from `.agentic/specs/`. Read its **Context & constraints** and
**Review** sections first. Do not re-litigate a rejected
finding without new evidence.

**Drift check:** compare the spec's `planned-against:` ref with HEAD. If they
differ, `git diff --name-only <ref>..HEAD` — when that diff touches the plan's
affected areas, stop and flag it to the user (re-plan or confirm) before executing;
a plan against moved code is wrong on arrival. A missing `planned-against:` line
(older spec) just means: say so and proceed with eyes open.

Post a short table of its steps and the verification command for each, so the
user sees the roadmap before work starts.

## Step 2 — Per-step loop (the core discipline)

For every step:
1. Re-read the exemplar for the shape you're about to write (`.agentic/gotchas.md`
   exemplars table). Copy the shape; don't invent.
2. Implement the step.
3. **Immediately run the narrowest matching test** — the test file for the changed
   file, or a filtered run (e.g. `dotnet test --filter <Handler>`, `npx vitest run <file>`).
   Do not batch validation to the end; a broken step found 5 steps later costs 5 steps.
4. If a shared helper/utility changed, run the full suite now, not later.
5. Write the step's tests alongside the implementation, per the plan's AC→test
   mapping table. Tests are part of the step, never a trailing phase.

**Parallel subagents:** dispatch parallelizable steps to `step-implementer`
subagents (`.claude/agents/step-implementer.md`). Dispatching ≥2
write-capable subagents concurrently requires worktree isolation
(`isolation: "worktree"`) or sequentialize — parallel writers in one checkout
corrupt each other's edits. They report `/decide`/`/gotcha`/doc-debt candidates
back to you; only this session edits knowledge files and git.

## Step 3 — Full validation

Run the full test, lint, and type-check commands from CLAUDE.md's Commands table.

## Step 4 — Quality gate (evidence, not estimates)

Read thresholds from `.agentic/quality-gates.yaml` and render a PASS/FAIL table.
Every "Actual" value must come from **real command output produced this session**
(coverage report, lint summary, duplication tool) — never estimated, never
self-reported from memory. A gate with no measuring tool in this repo shouldn't
exist (onboarding deletes them); if you find one, report it as SKIPPED (no tooling)
and flag it for removal — do not estimate a number for it. On FAIL, follow the
`enforcement.local` policy in quality-gates.yaml (default: show the table, ask
proceed/abort).

Add the quality gate table to the MR description, so reviewers see the evidence and
can verify it themselves. If the gate fails, do not proceed to MR creation until is passes

## Step 5 — Close the loop

- Dispatch a `critic` subagent (`.claude/agents/critic.md`) on the full diff for
  template compliance: exemplar-shape violations, tripped gotchas, undocumented
  decisions, unpaid doc debt. Fix findings before committing. (For bug-hunting
  review, the native `/code-review` skill covers it — don't duplicate that here.)
- Update the spec, add a new section that tells where the implementation has diverged from the plan.
- Move the spec to `.agentic/specs/completed/`.
- Decisions made along the way → `/decide`. Traps discovered → `/gotcha`.
  Diff invalidates an existing doc claim → fix it now (see `/sync-docs`).
- Commit (conventional format), push the branch, and create the MR/PR using the
  repo's platform command: <!-- onboard:mr-command -->`TODO e.g. glab mr create --target-branch develop --fill`<!-- /onboard -->
