---
name: bug-discovery-phase
description: >-
  Runs AFK ClawPatch bug discovery, reporting, and triage without source
  mutation. Use for ClawPatch discovery, broad bug discovery, bug lifecycle
  triage, finding ledgers, AFK bug review, or durable bug reports.
disable-model-invocation: true
---

# Bug Discovery Phase

Readonly ClawPatch discovery. Produces reports, finding state, triage notes,
and ranked next actions. Does not prove runtime root causes or patch code.

Load [REFERENCE.md](REFERENCE.md) before running ClawPatch.

## Contract

- Owns ClawPatch setup checks, bounded discovery scope, report/state paths,
  finding IDs, branch relevance, and triage notes.
- Default scope is PR changes, highlighted diffs, supplied code portions, or
  certain paths/domains. Full-codebase scan only when no PR is open and no
  certain scope exists, or when the user explicitly asks.
- Pass that bounded scope to every ClawPatch command or prompt that accepts
  scope, path, or diff guidance.
- Allows `init`, `map`, `review`, `ci`, `report`, `show`, `next`, `triage`,
  `status`, `doctor`, and `revalidate`.
- Blocks source mutation by default, including `fix --finding` and `open-pr`.

## Steps

1. Bound the run: repo, scope, provider/model default or explicit override,
   limit, jobs, state dir, report path, dirty posture, and output format.
2. Use the current agent/launcher provider by default; add provider/model
   flags only when the user selected a ClawPatch override.
3. Inspect readiness with `doctor`, `status`, and existing `.clawpatch/` state.
4. Run discovery and report generation within the bounded scope.
5. Inspect important findings, rank them `0-10`, and route each to resolution,
   debugging, debt classification, false-positive triage, or stop.
6. Stop before mutation unless the user makes a new explicit resolution request.

## Output

Return scope, provider/model default or override, limit/jobs, report and state
paths, commands run, finding IDs/statuses, rank rationale, static-review caveat,
and next action.
