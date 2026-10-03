---
name: standup
description: >-
  Session-scoped triage: what did I leave open, what is rotting, and is the plan still right —
  answered in under a screen. Runs in seconds over the session, the working tree, open PRs, and the
  two ledgers (ROADMAP + RELEASES DB), then emits a ranked list capped at 7 items plus a capped
  strategic read. Use when the operator says "/standup", "what's open", "what did I leave hanging",
  "where are we", "what should I do next", or is closing out a long working session. Not for
  long-window defect analysis (that is /radar), not for closing one branch (/finish-line), not for
  cutting one task's drip (/rabbit-hole), and it never executes the work it recommends.
---

# /standup

Two failure modes make long agent sessions expensive: a wall of text, and a rabbit hole where the
original focus quietly got diverted six times. This skill answers one question in under a screen —
**what did I leave open, what is about to rot, and is the plan still right?**

**Status: partial. The deterministic half is built; the collector is partially built.** `triage.py` (ranking,
tiering, suppression, parking, rendering) is implemented and pinned by `test/gh77-standup-triage.sh`
(92 assertions). `collect.sh` — currently implements lenses 2, 3, and 7. The remaining offline lenses and network-dependent lenses are not yet written, so this
skill cannot run completely end-to-end today. `collect.sh` requires **`jq`** in addition to git and
python3; without it every lens degrades to `D5` and the collector exits 3 rather than emitting nothing. Design and remaining work:
[PROJECT/3-COMPLETED/GH-77-STANDUP-SESSION-TRIAGE.md](https://github.com/HiQS-Labs/XYZ-forge/blob/development/PROJECT/3-COMPLETED/GH-77-STANDUP-SESSION-TRIAGE.md)
· [#77](https://github.com/HiQS-Labs/XYZ-forge/issues/77).

## The division of labour, and why it is drawn here

Everything mechanical lives in `triage.py`. This file chooses **only** two things: the `what`
phrasing of each item, and one optional clause appended to a fixed verdict sentence. Nothing else is
model-authored.

That line is not stylistic. The PRD for this skill went four review rounds across two independent
models and escalated at the cap with a **flat** finding rate — 11 → 13 → 10 → 10. A converging review
goes 11 → 5 → 2. It stayed flat because a state machine was being specified in prose, where every gap
needs a human reader to find it. Four separate times, a fix faithful to a finding re-broke the same
property through a new route. `triage.py` exists so those properties are asserted by a test run
instead of argued in Markdown.

## Invariants — these are enforced in code, not by instruction

- **A tier-1–3 item is never silent.** It is rendered, or counted as `K critical beyond cap` with a
  `--page` escape hatch. Never suppressed, never parked, never merely absent.
- **Writes stay inside `PARKED/`.** Session state lives at `PARKED/.standup-session-<id>.json`, not
  under `.git/` — `.git` is a *file* in a linked worktree, and this repo uses them.
- **General PARKED notes remain human intake.** Lens 8 parses only lines with its explicit
  `— check:` machine field; Markdown checklists and other agent observations in root `PARKED/`
  do not become standup records. Triage may promote those notes under `PARKED/README.md`.
- **A park file is never itself emitted as an item.** Untracked paths under `PARKED/` are excluded;
  a *modified tracked* one still surfaces, because it cannot loop.
- **`close` is never executed.** Only a park record's read-only `check` probe runs during collection.
- **An unchanged rerun writes nothing** — no new park file, no touch.
- **Output is capped at 15 rendered lines**, enumerated: 1 opening + 1 heading + ≤7 items + ≤1
  notices + 1 heading + ≤4 body.

## Usage

```bash
skills/1-hourly/standup/collect.sh > /tmp/lenses.json   # Partially built (lenses 2, 3, 7 only)
python3 skills/1-hourly/standup/triage.py --lenses /tmp/lenses.json --dry-run
python3 skills/1-hourly/standup/triage.py --lenses /tmp/lenses.json --apply --session-state PARKED/.standup-session-$$.json
python3 skills/1-hourly/standup/triage.py --lenses /tmp/lenses.json --dry-run --page 2   # beyond the cap
```

Exit `0` clean · `2` usage or a contract violation · `3` one or more lenses degraded.

Verdict codes are a finite set — `no-contradiction`, `ledger-behind`, `release-overdue`,
`insufficient-evidence` — chosen with `--verdict`; `--verdict-clause` adds at most one newline-free
clause of ≤120 characters. An unbounded clause is a wall of text with extra steps, so it is refused.

## Reporting the result

Print `triage.py`'s output as-is. Do not summarise it, do not add a preamble, and do not narrate what
you did to produce it — narration of the agent's own recent work is the single most common
wall-of-text source and is the thing this skill exists to remove.

If a tier-1–3 item appears, say so in your first sentence. If `K` is non-zero, name the `--page`
command; the operator must be able to reach every critical item.

## Degrading

Say which lens was unavailable and what it costs the verdict. `gh` missing means the PR and
issue-state lenses did not run — report that, never an implied clean sweep. A skill that degrades
quietly reports a sweep it never performed, which is the defect class this repo has spent the month
removing.
