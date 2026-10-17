---
name: trace
description: Turn one recorded run of a flow (a trace file of steps - who called whom, with what values) into a sequence diagram, or compare two runs and mark what changed (added, removed and changed steps). Use when a reader must understand a flow from a real run instead of from code, when checking whether a change altered a flow (before vs after, golden run vs branch run), or when placing a bug report on a flow (expected run vs the failing run). Draws through diagrams:flow, so the output is chat text or a picture page.
---

# Trace: a real run as a sequence diagram

A diagram drawn from a real run shows what happened, with real values. A diagram drawn from code shows what should happen. Use this skill when the real run matters.

```
trace file ─► trace run.json ─────────► Mermaid ─► flow (fd / pic)
two traces ─► trace a.json b.json ────► Mermaid with [+] [-] [~] marks
```

## The trace file

One JSON object. Only `steps` is required, and each step needs `from`, `to` and `label`.

```json
{
  "title": "Checkout",
  "participants": [{"id": "api", "label": "Orders API"}],
  "ignore": ["orderId"],
  "steps": [
    {"from": "app", "to": "api", "label": "POST /orders", "t": "2026-10-11T09:00:00Z", "values": {"orderId": 1041}},
    {"from": "api", "to": "queue", "label": "order.created", "kind": "async", "note": "fires after commit"}
  ]
}
```

| Field | Meaning |
|---|---|
| `kind` | `sync` (default, solid arrow), `reply` (dashed), `async` (dotted) |
| `t` | ISO time or epoch milliseconds; used by `--time` |
| `values` | what the step carried; shown on the arrow and compared in a diff |
| `note` | a note box under the arrow |
| `participants` | optional order and display names; others appear in order of first use |
| `ignore` | value keys that change every run (ids, times); left out of the diff |

A bare array of steps, or JSONL with one step per line, also works. JSONL suits a recorder that appends steps as they happen.

**Rule for anyone who writes a recorder:** keep the `label` stable between runs (`update order`, not `update order 1041`). Put anything that changes every run in `values`, and list it in `ignore`. The diff matches steps on `from`, `to` and `label`, so a label that holds an id never matches.

## Commands

```bash
"${CLAUDE_SKILL_DIR}/trace" run.json --text              # one run as chat text
"${CLAUDE_SKILL_DIR}/trace" run.json --time --text       # with +120ms before each arrow
"${CLAUDE_SKILL_DIR}/trace" a.json b.json --text         # b compared with a
"${CLAUDE_SKILL_DIR}/trace" a.json b.json --context 2    # fold unchanged steps, keep 2 around each change
"${CLAUDE_SKILL_DIR}/trace" a.json b.json --json         # diff rows for other tools
```

- Without `--text`, the output is Mermaid. Pipe it into `diagrams:flow`: `trace a.json b.json | fd -`, or save it and run `pic` for a picture page.
- A diff prints one summary line to stderr: `trace: 1 added, 0 removed, 1 changed, 5 same`. The exit code is 0 when the runs match, 1 when they differ, and 2 on an error, so scripts can use it as a check.
- Marks on the arrows: `[+]` only in the second run, `[-]` only in the first, `[~]` the same step with other values (`status: PAID → FAILED`).
- `--ignore id,time` adds keys to the file's own `ignore` list. `--values none|short|all` sets how many values an arrow shows (default: the first 3).

## Fit

- Each participant is one column, and a long label widens the gap between two lifelines. Five participants with values often pass 90 columns. Then use `--values none`, `--context`, or a picture page: `trace a.json b.json > d.mmd && pic d.mmd -o d.html`.
- `fd` notes a lifeline that a label covers. This is a layout limit of the text renderer; the picture page has no such limit.

## Example

`examples/order.a.json` and `examples/order.b.json` are two runs of one checkout. In run B, the payment fails and the worker queues a retry:

```bash
"${CLAUDE_SKILL_DIR}/trace" examples/order.a.json examples/order.b.json --context 1
```

Tests: `node --test skills/trace/*.test.mjs` from the plugin root.
