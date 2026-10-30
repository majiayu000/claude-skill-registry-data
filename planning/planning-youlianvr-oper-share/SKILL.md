---
name: planning
description: >-
  Plan multi-step or multi-session work with acceptance criteria, coherent units,
  verification and resumable checkpoints. Discuss consequential goal/product/
  architecture forks; update ordinary implementation details without a permission
  ceremony. Use for explicit planning or work too large for the everyday cycle.
---

# Planning — enough structure to finish the work

> Home branch in Memora: `root/skill/planning`. The live contract is `AGENTS.md`.

## Choosing a part

Planning itself runs inline on this page; the parts cover the two ends.

| Situation | Part |
|---|---|
| The outcome itself is still vague | `parts/define-goal/` |
| Intent is fuzzy and wants exploring before a plan | `parts/brainstorming/` |
| Decomposition and handoff templates wanted | `parts/writing-plans/` |

## Rules

- **Plan of record is `write_todos` plus one Memora node.** A plan file appears
  only when the owner asks for one: no `PLAN.md` by default, and
  `projects/<name>/docs/PLAN.md` is not a required source. Memora is the source.
- **Questions only on forks with consequences**: goal, architecture, cost, data
  risk, external effects. Newly discovered files, technical details and root
  causes already understood are updates to the plan, not owner decisions.
- **Checkpoint = a Memora node + 1–3 lines in chat**: what is done, what was
  checked, which unit comes next.
- **After a compaction**, read the plan node and `write_todos` first, then
  resume — never re-derive work that is already recorded.
- Understand the outcome, the existing base and the exact delivery constraints
  before proposing anything; show the approach with real alternatives where they
  matter, and never manufacture options for routine commands.
- Finish coherent units with evidence and exit conditions; an unresolved branch
  stays labeled in the node rather than silently decided later.

## Related

`grill-me` for the full interrogation of a plan, `brainstorming`,
`relevance-scan`, `sessions`, `dev`.
