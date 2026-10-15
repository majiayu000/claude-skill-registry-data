---
name: "speckit-config-gc"
description: "Garbage-collect the harness: skills and subagents nothing invokes, unregistered hook scripts, duplicate permissions, retired instincts, stale telemetry ledgers, dead worktrees and expired trash. Proposes candidates one at a time, moves only what you approve to .specify/_gc_trash/, and logs every move with its undo. Use when the setup feels bloated, after installing a batch of skills, or as a periodic review."
argument-hint: "Optional: a channel to review (skills, agents, hooks, permissions, instincts, telemetry, worktrees, trash)."
compatibility: "Node 18+. Never deletes without a per-item yes; every move is reversible from .specify/_gc_trash/."
metadata:
  author: "speckit-demo"
  source: "adapted from ECC's config-gc skill (github.com/affaan-m/ECC)"
user-invocable: true
disable-model-invocation: false
model: sonnet
---

## User Input

```text
$ARGUMENTS
```

## Why

Configuration is append-only in practice. Skills, hooks, permission entries and
memory files only ever get added, and nothing ever reviews them — so a setup
accumulates weight that costs context on every session and confuses every gate
audit. This is the periodic sweep, borrowed from ECC's config-gc, with its rule
kept intact: **collection requires a human in the loop; never delete
autonomously.**

## Phase 1 — Scan

```bash
node .claude/scripts/gc-scan.mjs
node .claude/scripts/gc-scan.mjs --jev   # same candidates, least likely to be missed first
```

Channels it covers, and the signal each one uses:

| Channel | Candidate when |
|---|---|
| skills, agents | never invoked across the recorded sessions (`.specify/telemetry/`) |
| hooks | a script on disk that no `registry.json` entry names |
| permissions | duplicate entries, or an entry another rule already covers |
| instincts | retired, or faded below the injection floor |
| telemetry | a session ledger untouched for 90+ days |
| worktrees | a `.worktrees/` directory whose branch is gone |
| trash | something in `_gc_trash/` past its 30-day undo window |

With no telemetry recorded, the skills and agents channels stay silent on
purpose: "never invoked" and "never measured" are different claims.

## Phase 2 — Judge, then ask

Present candidates **in small batches, grouped by channel**, each with the
evidence and what you propose. Then take them **one at a time** — a per-item
`y / n / skip`. There is no "yes to all" here; a batch approval is how a setup
loses something it needed.

Before proposing any item, apply judgement the scan cannot:

- **A gate that fires rarely is not dead.** A release-time hook, a PreCompact
  flush, a reviewer subagent invoked once a feature — low counts are expected.
  Never propose deleting a gate; propose reviewing it.
- **Never propose anything a constitution principle or CLAUDE.md names.** If a
  documented thing looks unused, the finding is that the docs and reality
  disagree — report that instead.
- **Anything under `specs/` is project history**, not garbage. Out of scope.
- **A skill with a real description and no invocations may simply be new.**
  Check its git age before proposing it.

## Phase 3 — Collect what was approved

Soft delete, in this order, never a straight `rm`:

1. Move the file or directory to `.specify/_gc_trash/<ISO date>-<name>`.
2. For a permission entry, remove the line from `.claude/settings.json` and
   record the exact string in the log so it can be pasted back.
3. For a hook, remove its `registry.json` entry too, then
   `node .claude/scripts/doctor.mjs --bless-hooks` and re-run `node .claude/scripts/doctor.mjs`.
4. Append to `.specify/gc-log.md`:

   ```markdown
   ## <ISO date>
   - trashed `.claude/skills/foo` — not invoked in 12 sessions — undo: `git mv .specify/_gc_trash/2026-09-12-foo .claude/skills/foo`
   ```

Finish by running `npm test && npm run lint && node .claude/scripts/doctor.mjs` and
reporting what moved, what was kept, and where the undo lives.

## Rules

- Nothing leaves the repo. `_gc_trash/` is tracked like anything else, so an
  over-eager sweep is one `git mv` away from undone.
- Never empty the trash in the same run that filled it.
- Never treat this command as a way to silence a failing gate — deleting the
  hook that blocks you is the failure mode it is most able to cause. If a gate
  is wrong, fix or retire it deliberately through `/speckit-evolve`.
