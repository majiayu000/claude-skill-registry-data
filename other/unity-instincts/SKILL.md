---
name: unity-instincts
description: "How the atomic instinct learning system works — observations, distillation, confidence scoring, project vs global scope, and promotion/evolution workflows."
alwaysApply: false
globs: [".claude/hooks/instinct-*.sh", ".claude/state/instincts/**/*", ".claude/commands/unity-instincts.md"]
---

# Unity Instinct Learning System

A lightweight pattern-learning layer that turns tool-use observations into reusable project-local knowledge without any LLM calls.

## Why it exists

Our static rules in `.claude/rules/` encode *universal* Unity truths (serialization safety, lifecycle order, perf golden rules). But every project has its own conventions the rules can't know:

- This project stores Models in `Runtime/Domain/`, not `Scripts/Models/`.
- Editing *View.cs reliably triggers quality-gate warnings here because developers hand-roll input handling.
- VContainer scopes are nested by feature, not by scene.

The instinct system captures these project-specific patterns automatically. Universal patterns remain owned by rules.

## Data model

```
.claude/state/instincts/
├── observations.jsonl         # raw PostToolUse events
├── project/<project-hash>/    # project-scoped instincts
│   └── <instinct-id>.json
└── global/                    # promoted instincts
    └── <instinct-id>.json
```

Each instinct:

```json
{
  "id": "h1-view-warning-hotspot",
  "trigger": "before editing *View.cs",
  "action": "expect quality-gate warnings; read Model first; avoid Update-loop allocations",
  "confidence": 0.7,
  "domain": "mvs",
  "scope": "project",
  "project_id": "a1b2c3d4e5f6",
  "evidence_count": 9,
  "first_seen": "2026-04-24T10:00:00Z",
  "last_seen":  "2026-04-24T17:45:00Z",
  "source": "auto-distill"
}
```

## Pipeline

```
Tool use (every Edit/Write/Read/Bash/Grep/...)
        │
        ▼   instinct-capture.sh  (PostToolUse, ~10ms)
observations.jsonl
        │
        ▼   instinct-distill.sh  (Stop hook, heuristic, ~100ms)
project/<hash>/*.json  (confidence bumped by 0.1 per evidence, capped 0.9)
        │
        ▼   /unity-instincts evolve       (manual)
Draft SKILL.md for review
        │
        ▼   /unity-instincts promote      (manual, cross-project check)
global/*.json
```

## Heuristics currently emitted

**H1 — Warning hotspot by path tag.** If observations with a given `path_tag` (view/system/model/sobject/mono/editor/scene/prefab) accumulate >=2 new warnings across >=3 tool-uses in a session, an instinct is emitted or bumped.

**H2 — Tool-sequence affinity.** If `*View.cs` edits are frequently preceded by `*Model.cs` reads, emit the "read Model before editing View" instinct.

**H3 — Hook-specific recurrence.** A hook (warn-serialization, warn-filename, warn-platform-defines, quality-gate, gateguard) that fires >=3 times in one session becomes a project-level instinct.

All three are cheap string/count operations in the Stop hook — no LLM, no background agent.

## Confidence ladder

| Evidence count | Confidence | Treatment |
|---|---|---|
| 1 | 0.3 | tentative — do not surface |
| 2–3 | 0.4–0.5 | medium — include in `status` |
| 4–6 | 0.6–0.7 | strong — surface during workflow planning |
| 7+ | 0.8–0.9 | near-certain — candidate for `evolve` to skill |

## Scope rules

- Default scope on creation: `project`.
- `/unity-instincts promote` requires the same trigger to appear in another project hash, OR `--force`.
- Global instincts are loaded on session start for every project (TODO: wire into session-restore).

## Interaction with static rules

Rules win on conflict. If a rule exists covering the same pattern, the instinct is redundant and should be discarded during `evolve`. `/unity-instincts evolve` output is intentionally a *draft* — the user reviews before promoting learning into a codified rule.

## When NOT to use

- For enforcing known Unity correctness (e.g., FormerlySerializedAs on rename) — that's a **rule**, not an instinct.
- For one-shot migration learnings — those belong in the migration PR description.
- For cross-cutting project decisions (architecture, pipeline choice) — those belong in CLAUDE.md.

Instincts fill the gap between "obvious universal" and "deliberate project policy".

## Commands

All user-facing operations are in `/unity-instincts` (see `.claude/commands/unity-instincts.md`). Hooks are automatic and silent.
