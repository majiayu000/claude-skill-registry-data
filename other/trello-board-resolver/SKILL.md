---
name: trello-board-resolver
description: >
  Resolve a Trello board name and one or more "role" names (e.g. doing, done)
  into concrete Trello board_id and list_id values, using the user's
  work-mgt config and a local cache. Use this whenever a skill needs to act
  on a board/list by friendly name rather than by ID.
user-invocable: false
allowed-tools: Read, Write, mcp__trello__list_boards, mcp__trello__list_lists
---

# trello-board-resolver

Translate friendly names into Trello IDs. Reusable across any skill that
talks to Trello.

## Inputs

- `board_name` (optional) — board to resolve. If omitted, use
  `trello.default_board` from the user's `~/.claude/work-mgt/config.json`.
- `roles` — array of role keys to resolve to list IDs (e.g.
  `["doing", "done"]`). Each role's list name is looked up by matching the
  board's actual list names against the aliases in
  `trello.lists.<role>` from the config (case-insensitive, first match wins).

## Output

Return a JSON object of the form:

```json
{
  "board_id": "abc123",
  "board_name": "Personal Ops",
  "lists": {
    "doing": { "id": "list1", "name": "Doing" },
    "done":  { "id": "list2", "name": "Shipped" }
  }
}
```

If a role has no matching list on the board, set its value to `null` and
include the attempted aliases in the error message.

## Behavior

1. **Load config** from `~/.claude/work-mgt/config.json`. Expand `~` in
   `state_dir` to the user's home directory. If the file does not exist,
   stop and tell the user to create one from `config.example.json` in the
   plugin repo.

2. **Load cache** from `<state_dir>/board-cache.json` if it exists. The cache
   is a JSON object keyed by board name:

   ```json
   {
     "Personal Ops": {
       "board_id": "abc123",
       "resolved_at": "2026-05-20T08:00:00Z",
       "lists": {
         "doing": { "id": "list1", "name": "Doing" },
         "done":  { "id": "list2", "name": "Shipped" }
       }
     }
   }
   ```

   Treat cache entries older than 7 days as stale and re-resolve.

3. **On cache hit** for the requested board *and* all requested roles, return
   the cached value immediately. Do not call any MCP tool.

4. **On cache miss**:
   - Call `mcp__trello__list_boards()` to find the board whose `name` equals
     `board_name` (case-insensitive). If none, abort with a message listing
     the boards that *were* returned.
   - Call `mcp__trello__list_lists(board_id=<resolved>)`.
   - For each requested role, walk `trello.lists.<role>` in order and pick
     the first list whose `name` matches an alias (case-insensitive). Record
     `null` if none match.
   - Merge the new entry into the cache and write `board-cache.json` back,
     creating `state_dir` if needed.

5. **Return** the resolved object.

## Errors

- Config missing → "No work-mgt config found at ~/.claude/work-mgt/config.json. Copy config.example.json from the plugin repo and edit it."
- Board not found → "Couldn't find board 'X'. Available boards: A, B, C."
- Role unresolved → in the returned object set `lists.<role>` to `null` and
  include `"unresolved_roles": [{"role": "doing", "tried": ["Doing", "WIP"]}]`
  so callers can produce a clear message.
