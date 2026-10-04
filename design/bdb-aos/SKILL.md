---
name: bdb-aos
category: bdb-core
description: >-
  Entry point for the BDB Agent OS suite installed as a Claude Code plugin.
  Use to find out which of the 200+ AOS skills, the seven startcycle subagents,
  or the pipeline workflows apply to a task, and where their contracts live.
  Reach for a specific skill directly when you already know its name — this
  skill only routes.
---

# BDB Agent OS

The full AOS suite: 200+ skills, 13 subagents, and the startcycle pipelines.

## Where things live

| Component | Location |
|---|---|
| Skills | `skills/<category>/<name>/SKILL.md` |
| Subagents | `agents/<name>.md` (mirrors `.claude/agents/`) |
| Pipeline contract | `.agents/graph.md`, node registry in `.agents/nodes.json` |
| State schema | `.agents/state.schema.json` |

## Pipelines

Three variants, differing only in how much machinery the task needs:

| Skill | Shape |
|---|---|
| `startcycle` | Linear chain: Architect → TechLead → parallel build → Reviewer. |
| `startcycle-graph` | Dispatcher graph: durable `state.json`, Reviewer repair loop, automated quality gate, human escalation. |
| `startcycle-graph-user` | Throwaway 2–4 node fan-out, nothing persistent left behind. |

**Agents never invoke each other.** A dispatcher — the main session or the
workflow script — decides every next step. Routing lives in the graph contract,
never inside an agent's prompt.

## Skill categories

`design-ui-ux`, `engineering-method`, `media-eventtech`, `bdb-core`, `library`,
`engineering-hardware`. Pick the narrowest match; a `library` skill should never
be pulled for a task a domain skill already covers.

The harness contract for every skill — required frontmatter, attribution,
`source:` for derived work — is in `AGENTS.md` at the repo root.
