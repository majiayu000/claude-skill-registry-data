---
name: cm-sprint-bus
description: "Use to run the full sprint pipeline: brainstorm → plan → design → tdd → build → review → qa → security → ship → monitor → retro."
token_budget: 1500
compressed: true
deprecated: false
---
# cm-sprint-bus — opinionated pipeline + artifacts

## TL;DR
- **Use to** drive the full sprint: brainstorm → ship → retro
- **Phases**: brainstorm, plan, design, tdd, build, review, qa, security, ship, monitor, retro
- **Each phase**: writes Markdown artifact + handoff JSON
- **CLI**: cm sprint init|status|complete|skip|dry-run

## Pipeline

`brainstorm → plan → design → tdd → build → review → qa → security → ship → monitor → retro`

## CLI

```bash
cm sprint init --project .
cm sprint init --from plan --project .    # jump in mid-pipeline
cm sprint status --project .
cm sprint complete plan -m "$(cat plan-notes.md)" --project .
cm sprint dry-run --project .
```

## Artifacts

- `.cm/sprint/state.json`
- `.cm/sprint/artifacts/<step>.md`
- `.cm/sprint/events.jsonl`

## Skill mapping (hints)

Each step maps to existing CodyMaster skills (see `skillMappingForStep` in `src/sprint-pipeline.ts`). Use `cm sprint status` for the **next** recommended skill.

## Context bus

This complements `.cm/context-bus.json` (skill-chain). Prefer **sprint files** for linear release trains; use **context bus** for ad-hoc chains.
