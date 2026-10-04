---
name: daily-trello-summary
description: >
  Produce a daily summary of a Trello board's Doing and Done lists for an
  executive assistant: what's been completed since the last summary, what's
  newly active, what's still in flight (with stale-item flags), and recent
  completions for context. Reads the user's work-mgt config and persists a
  last-run timestamp so each run's "since" window picks up where the
  previous left off.
argument-hint: "[board name]"
user-invocable: true
allowed-tools: Read, Write, mcp__trello__list_boards, mcp__trello__list_lists, mcp__trello__get_cards
skills:
  - trello-board-resolver
  - trello-list-snapshot
---

# daily-trello-summary

The v1 user-facing feature of the work-mgt plugin.

## Argument

- Optional board name (quoted if it contains spaces). When omitted, use
  `trello.default_board` from the user's config.

## Flow

### 1. Load config

Read `~/.claude/work-mgt/config.json`. If missing, stop with: *"No work-mgt
config found at ~/.claude/work-mgt/config.json. Copy config.example.json
from the plugin repo and edit it."*

Expand `~` in `state_dir` to the user's home directory. Defaults if absent:

- `trello.stale_days` → `5`
- `trello.done_head` → `10`
- `state_dir` → `~/.claude/work-mgt/state`

Ensure `state_dir` exists (create it if not).

### 2. Resolve board and list IDs

Invoke the `trello-board-resolver` skill with the board name (argument or
default) and `roles: ["doing", "done"]`. Abort with the resolver's error
message if the board can't be found or either role is unresolved.

Capture `board_id` from the resolver output — `since` is keyed per board,
so the resolution has to happen before we can read the last-run state.

### 3. Compute `since`

The last-run state is **per board** so that running `/daily-summary "A"`
and `/daily-summary "B"` doesn't mix their windows. Schema of
`<state_dir>/last-run.json`:

```json
{
  "boards": {
    "<board_id>": {
      "last_run_at": "2026-05-19T08:00:00Z",
      "board_name": "Personal Ops"
    }
  }
}
```

- If `<state_dir>/last-run.json` exists and `boards[<board_id>].last_run_at`
  is present, use that as `since`.
- Otherwise (file missing or no entry for this board), set `since` to
  "now − 24h" and remember that this is a first run *for this board* so
  the report can include a one-line note.

Capture the current timestamp as `run_at` *before* making the MCP calls;
it will be written back to `last-run.json` at the end.

### 4. Fetch four snapshots via `trello-list-snapshot`

| # | List  | `since` | `label`   | `format`   | Purpose |
|---|-------|---------|-----------|------------|---------|
| a | Doing | (none)  | `"Doing"` | `detailed` | Full in-progress snapshot |
| b | Doing | `since` | `"Doing"` | `compact`  | Cards active since last summary |
| c | Done  | (none)  | `"Done"`  | `compact`  | Full done snapshot (for `done_head` and run-rate) |
| d | Done  | `since` | `"Done"`  | `detailed` | Cards completed/touched since last summary |

Call the skill four times, passing the same `list_id` with and without
`since` for each role. Always pass `label` so the rendered markdown gets
a meaningful `### Doing (n cards)` / `### Done (n cards)` heading instead
of the default `"List"`.

### 5. Render the report

Output a single markdown document with these sections in order:

```
# Daily summary — <board name> — <run_at, local date>

_Since last summary at <since>_  (or _First run: showing last 24h_)

## Completed since last summary
<markdown block from snapshot (d). If empty: "_nothing yet_".>

## Started or active since last summary
<markdown block from snapshot (b). If empty: "_nothing yet_".>

## In flight (full Doing list)
<custom render of snapshot (a) sorted by date_last_activity ASCENDING so
 stale items float to the top. Cards with date_last_activity older than
 `stale_days` are prefixed with `⚠️ Attention:` and grouped above the rest.>

## Recently completed (head <done_head>)
<custom render of snapshot (c): first `done_head` cards sorted by
 date_last_activity DESCENDING, compact format.>
```

### 6. Persist last-run

Read-modify-write `<state_dir>/last-run.json`, updating only this board's
entry and leaving other boards' entries untouched:

```json
{
  "boards": {
    "<board_id>": {
      "last_run_at": "<run_at ISO 8601 UTC>",
      "board_name": "<resolved board name>"
    }
  }
}
```

If the file does not exist, create it with the `boards` map containing
just this entry. If it exists but has the old flat shape
(`{ last_run_at, board }`), discard it and start fresh with the new
schema — the cost is one extra first-run window, which is acceptable.

Only persist on a successful run (i.e. after the report is rendered). If
any step before #5 fails, leave the previous `last-run.json` untouched so
the next run still picks up from the correct point.

## Notes

- The "Completed since last summary" section relies on `date_last_activity`
  on Done cards. Moving a card into Done bumps that timestamp, so this is a
  high-fidelity proxy for "newly completed." It will also include Done
  cards that were merely edited (e.g. label change) in the window — the EA
  can see the timestamp and decide.
- Snapshots (a) and (c) are full lists; they're needed for stale-item
  detection and run-rate context that `since` queries can't provide.
- All four MCP calls can be issued in parallel — the four `get_cards`
  invocations are independent and do not affect server state.
