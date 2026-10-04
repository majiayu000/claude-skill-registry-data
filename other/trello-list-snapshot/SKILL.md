---
name: trello-list-snapshot
description: >
  Fetch the cards in a single Trello list (optionally filtered by activity
  date with `since`) and return them as both a structured array and a
  markdown-formatted view. Use this whenever a skill needs the contents of a
  specific Trello list by ID.
user-invocable: false
allowed-tools: mcp__trello__get_cards
---

# trello-list-snapshot

Single-list fetch + format. Reusable building block for any Trello reporting
skill.

## Inputs

- `list_id` (required) — Trello list ID.
- `since` (optional) — ISO 8601 UTC timestamp. When provided, only cards
  whose `date_last_activity` is `>= since` are returned (server-side filter
  via the Trello-MCP `since` parameter).
- `format` (optional, default `detailed`) — `compact` or `detailed`. Controls
  the markdown rendering; the structured array is unaffected.
- `label` (optional) — a short label for the list (e.g. "Doing") used in the
  markdown heading. Defaults to "List".

## Output

Return both:

1. A structured array of cards, each with:
   `id`, `name`, `desc`, `due`, `due_complete`, `labels`, `url`,
   `member_ids`, `date_last_activity`.
2. A markdown block. Sort by `date_last_activity` descending (most recent
   first). If the list is empty after filtering, render `_(no cards)_`.

## Behavior

1. Call `mcp__trello__get_cards(list_id=<list_id>, since=<since>?)`. Omit
   `since` from the call when it is not provided — do not pass empty string
   or null.
2. Sort the returned cards by `date_last_activity` descending.
3. Render markdown:

   **detailed:**
   ```
   ### <label> (<n> cards)
   - **<name>** — _<date_last_activity>_
     - Due: <due> · Labels: <label-names>
     - Members: <member_ids joined>
     - <url>
     - <first line of desc, truncated to 200 chars> (if non-empty)
   ```

   **compact:**
   ```
   ### <label> (<n> cards)
   - <name> · <date_last_activity> · <url>
   ```

4. Return the structured array and the markdown string to the caller.

## Notes

- The Trello-MCP `since` filter is inclusive (`>=`). Callers that want a
  strict "after" should pass `since` one millisecond past the cutoff.
- `date_last_activity` is "any activity," not specifically a list move. The
  daily-summary skill explains why this is an acceptable proxy for
  "completed since" when reading the Done list.
- Do not call `list_boards` or `list_lists` from this skill; the caller is
  expected to have resolved the `list_id` already (e.g. via
  `trello-board-resolver`).
