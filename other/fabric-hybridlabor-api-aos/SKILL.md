---
name: fabric
description: >-
  Master entry for the fabric family. Use for /fabric or when you must pick a
  multi-agent mode: reads the task, picks one mode, says why in one line, then
  follows that skill.
category: bdb-core
---

# `/fabric` — pick the mode, then run it

`fabric` has no pipeline of its own. It reads the task, chooses one mode from the table, prints one line (`fabric: <mode> — <reason>`), and then follows that skill's contract. Ask the human only if two modes fit equally well.

| Mode | Pick it when | Skill |
|---|---|---|
| `fabric-graph` | An approved plan should be built and correctness beats speed: durable `production_artifacts/state.json`, Reviewer repair loop, automated quality gate, human escalation. | `fabric-graph` |
| `fabric-multigraph` | A small throwaway fan-out (2-4 nodes, nothing persistent) in any project. | `fabric-multigraph` |
| `fabric-teamwork` | The brief is still vague and needs 9-step prompt crafting before delegation to a team. | `fabric-teamwork` |
| `fabric-swarm` | Many similar workers on one pool of items. Arrives in 5.4.1; routes to `fabric-multigraph` meanwhile. | `fabric-swarm` |
| `fabric-loop` | A repeating cycle until a condition holds (CI green, review rounds). Arrives in 5.4.1; routes to `loop-templates` meanwhile. | `fabric-loop` |

## Choosing

1. The task needs resumable state, a review loop or a quality gate before anything ships: `fabric-graph`.
2. The task splits into a few independent slices and nothing has to survive the session: `fabric-multigraph`.
3. The goal is unclear and a team will receive it: `fabric-teamwork` first, then one of the above.
4. Repeat-until-done: `fabric-loop`. Many near-identical slices: `fabric-swarm`.
5. A small task needs no mode at all: do it yourself.

Flags such as `--skill=<name>`, `--profile=` and `--workstreams` are handled by `fabric-graph`; pass the goal text through verbatim.

**Agents never invoke each other.** The dispatcher (the main session or the workflow script) decides every next step. Independent sub-tasks go to subagents; only work whose members must react to each other needs a team.

## Safety

`git push`, `npm publish` and `npm version` stay behind the go-gate. Choosing a mode never grants a GO.
