---
name: tc-tracker
description: >-
  Track a technical change as a Memora node: what changed, why, how it was
  tested, and where the work stands so a later session can resume. Use when the
  owner asks to track a change, keep an audit trail, hand work off, or produce
  release notes beyond commit subjects.
---

# TC tracker — a change record that lives in the tree

> Part of the `ship` router. The record is a Memora node, not a JSON registry:
> the retired `docs/` layer is never recreated, and there is no second source of
> truth next to the graph.

## The record

One node under `root/project/<name>` (or `root/skill/ship` for workspace-wide
work), written with `_scripts/memory.py branch`:

| Part of the record | Field |
|---|---|
| What and where | `content` first line: `<area>: <change in one imperative line>` |
| Why | the reason in `outcome`, including the rejected alternative |
| Status | `--status active` while open, `promoted` for a finished, verified change; `pruned` when it was abandoned |
| Evidence | tests run, commands, links — referenced, not pasted |
| Where it stands | the last line of `content`: the next concrete step |
| Lineage | `--parent` for the change it belongs to, `--supersedes` when it replaces an earlier record |

Tags carry the surface (`api`, `db`, `ci`, `ui`) so the tree can be walked by
area. A record that changes nothing observable is not worth a node.

## Lifecycle

`planned → in progress → implemented → verified → shipped`, and `blocked` off any
step. The transitions are the node's `status` plus the closing line, not a state
machine in a script:

- **planned / in progress** — `active`, with the next step in the last line.
- **blocked** — `active`, first line says what is missing and from whom.
- **verified** — `promoted`, with the check that proved it.
- **shipped** — `promoted`, with the version, deploy target or commit hash.

## Resume

Read the newest node on the branch (`rsi_tree.py walk --root root/project/<name>`)
plus `write_todos`, then continue from its last line. Never re-derive a decision
the node already records.

## Forks

Ask the owner before recording a change as shipped when the deploy, tag or push it
describes has not happened yet — a record that claims more than reality is worse
than no record.
