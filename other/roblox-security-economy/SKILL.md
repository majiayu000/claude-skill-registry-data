---
name: roblox-security-economy
description: Build and review Roblox security-sensitive economy systems. Use for currency, inventory, DataStores, trading, purchases, rewards, anti-dupe logic, RemoteEvent validation, server authority, receipt handling, and exploit-resistant progression.
---

# Roblox Security Economy

## Goal

Protect valuable game state while keeping the player loop fair. Anything that grants, spends, trades, saves, or purchases value must be server-authoritative.

## High-Risk Surfaces

- Currency and premium currency.
- Inventory, pets, skins, tools, boosts, and quest rewards.
- Trading, gifting, crafting, upgrades, prestige, and loot rolls.
- Developer product receipts and game pass checks.
- Daily rewards, streaks, event rewards, and group rewards.
- Client remotes that request grants, damage, teleport, placement, or progression.

## Server Authority Rules

- Calculate rewards on the server.
- Validate player eligibility on the server.
- Store canonical balances and inventory on the server.
- Treat client UI as display and intent only.
- Use idempotency for purchases and valuable grants.
- Reject malformed, replayed, impossible, or too-frequent remote requests.

## DataStore And Receipt Patterns

- Save compact canonical state, not UI state.
- Use versioned data schemas and migration guards.
- Queue or debounce saves during active sessions.
- Bind saves to player leaving and server shutdown paths.
- For developer products, grant through receipt processing and record processed purchase IDs before considering the transaction complete.

## Trading And Gifting

- Use server-owned trade sessions.
- Lock offered items while a trade is pending.
- Require both parties to confirm the exact final offer.
- Revalidate ownership immediately before commit.
- Commit atomically from server state where possible.
- Log valuable trades and grant paths for later investigation.

## MCP Review Workflow

1. Use `script_grep` for remotes, currency names, DataStore usage, receipt handlers, and grant functions.
2. Read every script that touches value with `script_read`.
3. Inspect relevant instances with `search_game_tree` and `inspect_instance`.
4. Patch with `multi_edit` only after mapping source-to-sink flow.
5. Playtest purchase-free paths and console errors with `start_stop_play` and `get_console_output`.

## Output

Report:

- Assets or values protected.
- Trust boundary.
- Server validation rules.
- Abuse cases prevented.
- Remaining risks or manual Roblox purchase tests.

## Next

Verify the protected flows in a playtest with `roblox-playtest-qa`, and confirm the save path is safe with `roblox-datastore-persistence`.

