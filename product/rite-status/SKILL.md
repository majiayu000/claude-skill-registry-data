---
name: rite-status
description: "User-invoked read-only active-feature report: phase, active slice, next action, evidence, open questions, drift, risks, and handoff readiness."
argument-hint: "[feature-slug]"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md"],"workspace":["state.md","tasks.md","questions.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --skill rite-status` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read.

# /rite-status: active feature status

Read-only. Report the active workspace; do not run a phase or write files.

## Load

Use the supplied slug or `.devrites/ACTIVE`; require its authoritative
`state.md` and read the cursor directly. Read question, evidence, and risk
artifacts only as needed. Never infer lifecycle state from `README.md` or chat.

If no workspace exists: when archived workspaces record an unfinished
[continuation sequence](../rite-plan/reference/slicing.md#continuation-workspaces),
list each next command (`/rite-spec <parent>-<n> "<objective>"`); otherwise
recommend `/rite-spec <feature>`. Then stop.

If `state.md` is unreadable/malformed: report a gap with the defect and stop — never infer the phase from other files; `/rite-doctor`/`/rite-upgrade` own repair.

## Report

1. feature and one-line objective;
2. phase, run mode, and active slice;
3. status from `state.md`;
4. the single `Next step` recorded in `state.md`;
5. proven versus unproven evidence;
6. open questions by gate, including the exact resolving command when awaiting
   a human; list `gate: escalating` entries separately under **Escalating:**
   with their `route:` specialist tag (do not mix with synchronous blockers);
7. unresolved drift and material risks;
8. handoff readiness;
9. tree state: `HEAD`, the `git status --short` path count, and dirty paths absent from
   `touched-files.md` (unrecorded); when `handoff.md` records `Tree at write`, whether HEAD
   and count still match it. Unrecorded paths or a mismatch go under `Open:` as
   reconcile-before-any-writer-command; status never records them itself.

A workspace is handoff-ready when it records one next action, all unresolved
questions, non-obvious decisions, load-bearing assumptions, current drift
status, and evidence for its claims. If chat contains missing durable context,
recommend `/rite-handoff` before the lifecycle command.
`devrites-engine handoff [slug]` emits the deterministic resume record (cursor,
`awaiting_human`, blocking question gates, ledger reduction, dead ends,
in-flight waves, read-next order) — cite it for items 3–6 and the handoff-readiness verdict
rather than re-deriving them. If that command is not found or exits nonzero,
report items 3–6 and `Handoff:` as `unavailable: <command> <not found | exit N>` —
never re-derive them from other files, never leave them blank — and set `Next:`
to `/rite-doctor`. When `metrics.jsonl` exists,
`devrites-engine metrics summary <slug>` rolls up dispatch/return counts and
bundle bytes per phase — cite it for dispatch accounting rather than
re-counting the ledger.

Do not derive a command from host identity or invent one from phase names. Read
the persisted `Next step`.

## Output

```text
Feature: <slug> — <objective>
Phase: <phase>; slice: <slice|n/a>; mode: <HITL|AFK>; status: <status>
Evidence: <fresh/proven summary | gaps>
Open: <questions/drift/blockers | none>
Escalating: <qid route:tag … | none>
Handoff: <ready | missing durable context | unavailable: <reason>>
Tree: HEAD <sha>; dirty <n>; unrecorded <paths | none>; record <matches | differs | none>
Next: <single persisted command>
```
