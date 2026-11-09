---
name: work-graph
description: The work graph format that plan-work creates and execute-work runs. Load it when you have to read, validate, hand-edit or archive a work graph (graph.md, nodes/<id>.md, history.md, backlog.md), map a graph to another ledger, or run scripts/work_graph.py (check, ready, status, archive).
---

# Work graph

A work graph is the resumable state of a program of work: `graph.md` holds
the header, the node table and the Log; `nodes/<id>.md` holds one node's
contract and plan; `history.md` holds archived rows and Log entries. The
format is normative in `references/graph-format.md`; the templates
`references/graph-template.md` and `references/node-template.md` start a new
graph or node; `references/ledgers.md` maps the graph's operations onto
another ledger when the operator uses one.

Use `scripts/work_graph.py <command> <path to graph.md>`:

- `check`: validate the graph (cycles, unknown edges, contract fields,
  Consumes resolved to Produces, Files overlap without a dependency path,
  archive caps). Exit 1 with one line per defect.
- `ready`: list the nodes whose dependencies are all done.
- `status`: counts per state, the ready set, the schedule and the stuck nodes.
- `archive`: move closed rows and old Log entries to `history.md` (`--dry-run`
  reports the moves). With `--rows <json>` the commands read a custom ledger's
  export instead of the table.

Planning a graph is the plan-work skill; running one is the execute-work
skill. This skill only describes the files and the script they share.
