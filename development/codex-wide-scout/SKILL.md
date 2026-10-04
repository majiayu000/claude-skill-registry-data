---
name: codex-wide-scout
description: Use when Codex should run a broad, same-layer, parallel scouting pass over a fuzzy problem before choosing a direction to deepen. Triggers include "广度优先", "同层并行撒网", "wide scout", "parallel sweep", "try many directions first", early-stage ambiguous research/design/debugging, or cases where each lane may use multiple subagents to surface surprising leads. Do not use for known implementation tasks, final cleanup, review-only work, or deep frontier search after a lead has already been selected; route those to codex-completion-loop, review skills, or codex-exploration-loop.
---

# Codex Wide Scout

Run a bounded breadth-first scouting sweep. The goal is a map of plausible directions, surprising leads, dead zones, and a recommendation for what to deepen next.

## Quick Start

1. Restate the fuzzy target as a scouting question.
2. Choose defaults when unspecified:
   - `waves`: 2
   - `lanes_per_wave`: 4
   - `subagents_per_lane`: 1
   - `lane_timebox_minutes`: 8
   - `max_total_lane_probes`: 8
3. Gate risky actions:
   - Allowed by default: read/search, local commands, public web, local skills, scratch edits in isolated worktrees.
   - Ask first: paid/authenticated calls, credentials, destructive edits, commit/push, merge, production systems.
4. Create a run directory. Prefer reusing `codex-exploration-loop`'s `scripts/explore_ledger.py init` so later handoff can reuse the same ledger.
5. For each wave:
   - generate independent same-layer lanes;
   - assign each lane a distinct hypothesis and probe;
   - dispatch lane scouts in parallel only when subagents or workers are authorized;
   - collect all lane briefs before deciding the next wave.
6. Between waves, revise lane taxonomy:
   - keep promising families;
   - split only families that need internal breadth;
   - drop dead zones;
   - add at most one "wildcard" lane for surprising alternatives.
7. Stop when the wave or lane budget is used, the opportunity map is stable, or one or more leads are ready for deepening.
8. End with a scout map and an explicit handoff:
   - `codex-exploration-loop` for deep branch search;
   - `codex-completion-loop` for implementation;
   - a review/eval skill for adversarial checking;
   - human decision if the map changes priorities rather than tasks.

## Breadth Semantics

Wide scout is not a beam-search loop.

- A `wave` is one same-layer scouting pass across several lanes.
- A `lane` is one independent direction or hypothesis family.
- A `lane probe` is one concrete investigation inside a lane.
- `subagents_per_lane` means internal parallel checks for the same lane, not extra top-level lanes.
- Selection happens after each wave, but the default is "map and compare", not immediate pruning to one best branch.

Use this skill before `codex-exploration-loop` when the problem space itself is unclear. Use `codex-exploration-loop` after a lead or frontier structure exists.

## Lane Design

Lanes should be mutually informative, not minor wording variants.

Good lane families:

- mechanism hypotheses;
- data/source routes;
- implementation architectures;
- failure causes;
- user-value frames;
- benchmark/evaluation angles;
- contrary or adversarial interpretations;
- cheap baseline versus ambitious route.

Avoid:

- eight lanes that differ only by phrasing;
- scheduling every future turn as a fresh top-level wave;
- letting lane scouts modify the same files;
- turning a lane scout into the lead controller.

## Resource Routing

Read only what is needed:

- `references/wave-protocol.md`: wave lifecycle, scoring, and final scout map.
- `references/lane-prompts.md`: native subagent and worker prompt templates.
- `references/exploration-loop-handoff.md`: how to reuse `codex-exploration-loop` ledger, worktrees, workers, and digest.

If you need deterministic run-dir, worktree, worker, or ledger commands, use the installed `codex-exploration-loop` helper rather than copying scripts into this skill.

## Minimal Commands

Initialize a compatible ledger:

```powershell
python <codex-exploration-loop-dir>\scripts\explore_ledger.py init `
  --root <workspace> `
  --slug <slug> `
  --question "<wide scout question>" `
  --max-rounds 8 `
  --round-timebox-minutes 8 `
  --mode standard
```

Create lane branches for a wave:

```powershell
python <codex-exploration-loop-dir>\scripts\explore_ledger.py fanout `
  --run-dir <run-dir> `
  --parent-branch b001 `
  --candidate "Lane A hypothesis ||| Lane A probe" `
  --candidate "Lane B hypothesis ||| Lane B probe" `
  --candidate "Lane C hypothesis ||| Lane C probe" `
  --candidate "Lane D hypothesis ||| Lane D probe" `
  --beam-width 4 `
  --keep-parent-active
```

For edit-heavy lanes, create worktrees before dispatch:

```powershell
python <codex-exploration-loop-dir>\scripts\explore_ledger.py prepare-worktree `
  --run-dir <run-dir> `
  --branch-id b002 `
  --repo-root <git-repo>
```

## Output Contract

Final response:

```text
Wide scout complete
- Waves:
- Lane probes:
- Run dir:
- Isolation:

Scout map
1. Lane/family:
   - Evidence:
   - Surprise:
   - Confidence:
   - Suggested next:

Dead zones
- ...

Recommended handoff
- Deepen with codex-exploration-loop / implement with codex-completion-loop / review / human decision

Not done
- ...
```
