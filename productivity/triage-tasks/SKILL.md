---
name: triage-tasks
description: Interactive triage of the approval gate. Walks each block in inbox/tasks_pending.md and routes it — approve / reject / attach-as-follow-up / edit / skip. See workflows/task_tracking.md for the why.
allowed-tools:
  - Bash
  - Read
---

# triage-tasks — Approval gate for automation-generated tasks

Walks each pending block in `inbox/tasks_pending.md` interactively. Automations (mail ingestion, opus crons) write candidates there; this skill is how they become live tasks.

## Usage

```
/triage-tasks             # interactive triage of all pending items
/triage-tasks count       # just print the count
/triage-tasks list        # list pending titles without triaging
```

## Per-item actions

- `[a]` approve as suggested (new or follow-up per matcher)
- `[n]` force new (skip matcher's follow-up suggestion)
- `[f]` force follow-up under a specific parent `path:line`
- `[e]` edit the title before writing
- `[s]` skip (leave this item in the queue)
- `[r]` reject (remove from queue, do not write anywhere)
- `[q]` quit (remaining items stay in queue)

## Execute now

**Default: manual, one item at a time, Claude-driven.** The `tools/tasks_review.py`
REPL cannot receive the user's keystrokes inside Claude Code, so Claude itself is
the gate. **Never** drive the REPL with piped / `yes` input to bulk auto-approve —
that destroys the per-item human judgment the gate exists for, even when every
item looks legitimate. Authoritative procedure: `workflows/tasks_triage.md`
("Execution mode (authoritative)").

Per-item loop:

1. `python3 tools/tasks_review.py --list` to load the queue.
2. For **each** block, in order, present: `[N/total]`, `area`, `title`,
   `source`, `captured`, the **full** `raw` excerpt, matcher `suggested-action`
   + `match-score`.
3. **Stop and wait** for the user's explicit decision on that one item
   (`a` / `n` / `f path:line` / `e <new title>` / `s` / `r`). Do not advance,
   pre-decide, or batch.
4. Apply exactly what the user said via the shared writer
   (`python3 tools/task_add.py --area <area> --title "…" [--due …] [--section …]`;
   `--parent path:line` for follow-up), then remove the handled block from
   `inbox/tasks_pending.md`. Reject = remove block, write nothing. Skip = leave
   block in place.
5. Next block. Repeat to the end, then report what landed where and the
   remaining queue count.

`count` / `list` stay non-interactive:

```bash
python3 tools/tasks_review.py --count   # if the user said `count`
python3 tools/tasks_review.py --list    # if the user said `list`
```

After completion, show the user the final count line and remind them that approved items were written directly to area files (skipping the gate, since approval is the gate).

## See also

- [workflows/tasks_triage.md](../../../workflows/tasks_triage.md) — step-by-step SOP
- [workflows/task_tracking.md](../../../workflows/task_tracking.md) — system-wide why
- [tools/tasks_review.py](../../../tools/tasks_review.py) — implementation
