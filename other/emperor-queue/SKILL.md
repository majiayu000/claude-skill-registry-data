---
name: emperor-queue
description: >-
  Pick or record work. Use when the user says find work, next, backlog,
  issues, Linear, what should I do, or hands a repo with no task. Not
  Claude-specific. Writes .emperor/queue.md. Wraps Dowsing, does not replace it.
license: MIT
metadata:
  version: 0.4.23
  part-of: emperor-time
---

# Emperor Queue — pick the next piece of software

**WIP=1** — one active task at a time. Do not start a second item while `[~]`
exists; finish or `queue done` first.

## HARD-GATE — reject multi-WIP

`queue next` already refuses promoting a second `[~]`, but agents who skip the
script have no always-fail check. Before claiming parallel / multi-ready work:

```bash
scripts/emperor queue --reject-multi-wip   # always exit 1 (iron)
scripts/emperor queue --check-wip          # exit 1 when ledger has >1 [~]
scripts/emperor queue --check-wip <queue.md>
```

`--check-wip` counts non-placeholder active `[~]` lines only. Zero or one
active → PASS. Two or more → FAIL with `REJECT MULTI WIP`.

## Local Kanban statuses

| Mark | Meaning |
|------|---------|
| `[ ]` | ready |
| `[~]` | active (at most one) |
| `[x]` | done |
| `[!]` | blocked (optional; listed, never auto-picked) |

Python core: `scripts/lib/queue.py` (thin `scripts/queue.sh` / `queue.ps1`). Always-fail `--reject-multi-wip` / `--check-wip` enforce WIP=1 on the ledger even when agents skip `next`. `queue list` shows ready / active / blocked (skips empty placeholders). `queue next` returns the existing
`[~]` if present (WIP refuse); otherwise promotes the first real ready `[ ]` → `[~]`.
Empty queue = comment-only / no checkbox lines — `(empty…)` and parentheses-only titles are never promoted.
`queue done <substring>` checks off `[ ]` / `[~]` / `[!]`.

Optional cycle time: record `started` / `finished` ISO timestamps on the task
ledger or DONE template when cheap — not required for the script.

1. If the client already named a task, do not hunt. Quote it into the ledger.
2. Else run `scripts/emperor queue next` and quote the tail.
3. Source order (first hit wins): `EMPEROR_QUEUE_SOURCE` → `gh issue list` →
   Linear (`LINEAR_API_KEY` set by client) → `.emperor/queue.md`.
4. One item (WIP=1). Write G0/G1. Out of scope: the rest of the backlog.
5. After G5 + forge, run `scripts/emperor queue next` again unless the client
   said rest.
6. If no tracker exists and the client wants one, propose the thinnest adapter
   (usually `gh`). Build it only with consent. Do not invent Linear when a
   markdown queue works.

Never open a public issue or mutate the tracker without consent.
