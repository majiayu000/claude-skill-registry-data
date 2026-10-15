---
name: "speckit-doctor"
description: "Check that the harness itself still works: hook registry and fingerprints, settings wiring, feature pointer, stale traceability exemptions, skill and agent frontmatter, npm scripts, permissions, Python helpers and templates. Reports what drifted and fixes only what you name. Use when a gate seems not to fire, after editing hooks or settings, or before trusting an unattended run."
argument-hint: "Optional: 'fix' to apply the safe repairs, 'bless' to re-record hook fingerprints after reviewing a gate change."
compatibility: "Node 18+. Reads .claude/ and .specify/; writes nothing unless you ask for a repair."
metadata:
  author: "speckit-demo"
  source: "adapted from ECC's doctor/repair pair and hooks.metadata.json fingerprints (github.com/affaan-m/ECC)"
user-invocable: true
disable-model-invocation: false
model: sonnet
---

## User Input

```text
$ARGUMENTS
```

## Why this exists

A gate that fails is loud. A gate that stopped *firing* is silent — a renamed
hook script, a settings entry pointing at an id nobody registered, an exemption
in `.specify/trace-baseline.json` for a feature that was deleted a month ago.
Every one of those leaves the suite green and the rule unenforced. This command
is the periodic check for that class of failure.

## Phase 1 — Report (always)

Run:

```bash
node .claude/scripts/doctor.mjs
```

Read the output and report it to the user grouped by severity, **not** as a
transcript dump:

- `✗ fail` — a gate is broken or unenforced right now. Say which rule is not
  being applied, in plain words ("edits to src/ are no longer test-gated"), not
  just the check name.
- `! warn` — drift that is not yet a hole: stale permissions, dead exemptions,
  unregistered hook scripts, missing Python.
- `✓ ok` — summarise as a count. Do not list them.

If every check passes, say so in one line and stop. Do not invent work.

## Phase 2 — Repair (only when asked, one at a time)

Only when the user asks for a fix (or passes `fix`). For each finding, propose
the smallest change and name what it affects:

| Finding | Repair |
|---|---|
| `hooks/fingerprints` stale | **Read the diff of that gate script first** (`git diff -- .claude/hooks/<script>`). A change that weakens a gate is a finding to report, not a fingerprint to bless. Only when the change is legitimate: `node .claude/scripts/doctor.mjs --bless-hooks` |
| `hooks/wiring` mismatch | Add the missing id to `.claude/settings.json`, or delete the entry that names an unknown id |
| `hooks/scripts` missing | Restore the script from git, or remove its registry entry if the gate was retired on purpose |
| `hooks/orphans` | Register the script, or delete it — an unregistered hook script runs from nowhere |
| `feature/pointer` broken | Rewrite `.specify/feature.json` to the real feature directory, or delete the file |
| `feature/baseline` dead entries | Delete them from `.specify/trace-baseline.json`. Never add one to make a gate pass |
| `skills/frontmatter`, `agents/frontmatter` | Fix the frontmatter so `name` matches the directory or filename |
| `commands/permissions` stale | Remove the allow-list entry for the deleted script |
| `commands/python` missing | Report it; installing Python is the user's call, not an edit to make |

Re-run `node .claude/scripts/doctor.mjs` after the repairs and show the new counts.

## Rules

- Never bless a fingerprint you have not read the diff for. The whole point of
  the fingerprint is that weakening a gate requires editing its script.
- Never "fix" a failure by deleting the check, relaxing a threshold, or adding
  a baseline exemption. Those are the moves this command exists to detect.
- `--check` (exit 1 on any failure) and `--json` are for
  `.specify/scripts/bash/routine-verify.sh` and unattended runs.
