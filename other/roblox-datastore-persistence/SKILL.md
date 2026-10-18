---
name: roblox-datastore-persistence
description: Design, implement, and review Roblox DataStore persistence. Use for save/load schemas, migrations, autosave, retries, player leave saves, server shutdown saves, rollback-safe state, profile locking, and data-loss debugging.
---

# Roblox DataStore Persistence

## Goal

Save player progress reliably without corrupting or losing valuable state.

## Schema Rules

- Store compact canonical state, not UI state.
- Include `schemaVersion`.
- Keep defaults centralized.
- Validate loaded data before using it.
- Write migrations that can handle old, missing, or partial data.
- Keep transient match/session state separate from permanent profile state.

## Save Strategy

- Load once when the player joins.
- Keep an in-memory authoritative profile on the server.
- Save on meaningful intervals and player leave.
- Save on server shutdown with a bounded timeout.
- Debounce rapid save requests.
- Retry transient failures with backoff.
- Mark dirty profiles and avoid unnecessary writes.

## Valuable State

Treat these carefully:

- Currency and premium currency.
- Inventory, pets, cosmetics, boosts, quest progress, achievements.
- Purchases and receipt-granted items.
- Trading or gifting results.
- Daily streaks and time-gated rewards.

## MCP Review Workflow

1. Use `script_grep` for `DataStore`, `UpdateAsync`, `SetAsync`, `GetAsync`, profile, save, and load.
2. Read all persistence scripts with `script_read`.
3. Map load, mutation, save, and shutdown flow.
4. Patch with `multi_edit`.
5. Playtest join/change/leave-like paths where possible and check `get_console_output`.

## Output

Return:

- Profile schema.
- Save/load flow.
- Migration plan.
- Failure modes handled.
- Manual tests still needed in published or multi-server conditions.

## Next

Harden the save path against exploits with `roblox-security-economy`, then verify saves survive rejoin and shutdown with `roblox-playtest-qa`.

