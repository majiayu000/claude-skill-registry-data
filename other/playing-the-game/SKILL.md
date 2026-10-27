---
name: playing-the-game
description: Guide for playing MineClonia/MineClone2 through a running Antilua client — gathering resources, crafting tools, mining, and surviving. Prefers the antilua MCP server's agent tools (agent_ctx/agent_events/walk/fly/goto, verified dig/place/use, inventory, crafting, chat, screenshots); falls back to the raw Lua pipe. Use when you need to automate gameplay tasks, craft items, or interact with the world programmatically.
---

# Playing The Game via the Antilua MCP Server

## Overview

Control a running Antilua client through its MCP server (`util/mcp/`), which
exposes structured tools over the client's Lua pipe. Requires the client
running with `pipe_lua_enable = true` (the `antilua-mcp` server connects via
`ANTILUA_PIPE_PATH`, default `/tmp/antilua_lua`).

Prefer MCP tools over raw pipe writes — they handle JSON serialization,
response files, and pacing for you, and `screenshot()` gives you eyes on the
world. Use the raw Lua pipe (`skills/antilua-lua-pipe/SKILL.md`, or the
`run_lua` escape hatch) only for things the curated tools don't cover.

### Quick Start

0. **No client running?** Launch one: `scripts/agent_play.sh` (defaults to the
   Oysterity anarchy server as `ophelia`; `--headless` for xvfb, `--world W` for
   local, `--server HOST:PORT` to override). Use Shakespearean names for fresh
   accounts. On Oysterity, read `skills/oysterity/SKILL.md` first — it has the
   server's own rules, the greeting flow and the saved-map workflow.
1. Orient: `agent_ctx()` (one call: pos/look/hp/inventory/objects/ping) →
   `screenshot()` if the client is rendering.
2. Prep: `survival(true)` (autoeat, autototem, autojump, autorespawn,
   autotool) — on hostile servers the agent will die otherwise, and deaths
   scatter the inventory (Oysterity's spawn is creeper-infested).
3. Act: `goto` / `dig_at` / `place_at` / `use_node` / `move_item` / `craft`.
4. Verify: `get_inventory()` / `agent_events(since)` / `screenshot()`.

`agent_ctx()` replaces the old `get_player_pos` + `get_player_look` +
`get_inventory` triple for orientation; the older tools still work.

## Player Info

| MCP tool | Notes |
|----------|-------|
| `get_player_pos()` | `{x, y, z}` node coords |
| `get_player_look()` | `{yaw, pitch}` (deg), `roll` (rad) |
| `teleport({x, y, z})` | Move the player; returns new pos |
| `set_look(yaw, pitch)` | Aim the camera (deg) |
| `set_time("noon")` / `"6"` / `"midnight"` | Server time of day (needs settime priv) |
| `get_client_status()` | `{connected, joined, player_name, chat_buffer}` — check first when tools fail |
| `run_lua("return core.localplayer:get_hp()")` | HP (0-20); also `get_name()`, `get_wielded_item()`, `get_wield_index()` |

## World Interaction

| MCP tool | Notes |
|----------|-------|
| `get_node({x,y,z})` | `{node: {name, param1, param2}}` or `{node: null}` if unloaded (client map — can lag; cross-check with `screenshot()`) |
| `dig_node({x,y,z})` | Punch/dig a block `{digged: true/false}` |
| `place_node({x,y,z})` | Places the *wielded* item |
| `interact(action, pointed)` | Real right-click/`use`/`activate`/`place`/`dig` — `use` opens node formspecs (`pointed` from `get_pointed_thing()`) |
| `find_nodes_near(pos, radius, [names])` | `{count, positions}` |
| `find_nodes_near_under_air(pos, radius, [except])` | `{count, positions}` — solid surfaces with air above (placement spots) |
| `get_objects_near(pos, radius)` | `{objects: [{id, pos, name, is_player}]}` |
| `get_pointed_thing()` | `{type: node\|object\|nothing, ...}` |

Note: `place_node` places whatever is wielded — use `give_and_wield(item)`
or `wield_item(item)` (substring match) instead of the old
move-then-`set_wield_index` dance.

## Waiting for sync

Client state (inventory, wield, node meta) lags a beat behind the server.
Don't hand-roll polling — `wait_until(code, timeout, interval)` runs a Lua
expression repeatedly and returns `{ok, value}` when truthy:

```lua
-- run via wait_until's `code`:
return core.get_inventory("current_player") and find_stack_name() ~= nil
```

Server chat commands report their result through the chat log:
`run_server_chatcommand("giveme", "mcl_core:stone 1")` returns the server's
reply lines in `chat` (e.g. "…added to inventory."), and `get_chat_log(20)`
reads recent lines at any time.

## Inventory

`get_inventory(location?)` returns `{list: [{slot, name, count}, ...]}` for
`main` (36; 1-9 hotbar), `craft` (9), `craftresult` (1), `craftpreview` (1),
`armor`, `hand` — and, with a location, other inventories: `player:<name>`,
`nodemeta:x,y,z` (chests/furnaces), `detached:<name>` (creative). Use
`move_item(from_list, from_slot, to_list, to_slot, count)` (or
`move_items([...])` for batches) — `count` 0 = whole stack.

## Crafting System

Crafting uses inventory moves + the `craft` action. Without a crafting table
only 2x2 recipes work (`craft` list indices **1,2,4,5** — it has width 3
internally); place a crafting table for 3x3.

| Step | MCP tools |
|------|-----------|
| Move items into grid | `move_item("main", slot, "craft", grid, 1)` |
| Trigger craft | `craft(1)` |
| Take result | `take_craft_result(main_slot)` (moves `craftresult` → `main`) |

## Complete: Get a Stone Pickaxe

Orient first (`agent_ctx()`, `screenshot()`), then — the verified-tool
version of the classic progression (fall back to the raw tools noted inline
if a tool is unavailable):

1. **Wood**: `find_nodes_near(pos, 20, ["mcl_trees:tree_pale_oak"])` → `goto`
   to within ~4 nodes of the log (`run_lua` `agent.open_target(4)` if the
   destination is unknown) → `dig_at(log)` (returns `{ok, state: "done"}` once
   the server confirms removal) → **collect the drop immediately**: walk/tp
   onto the item entity, then check `get_inventory()`. Drops despawn after a
   few minutes, and picking up requires being within ~1.5 nodes.
2. **Planks**: `move_item("main", log_slot, "craft", 1, 1)` → `craft()` →
   `take_craft_result(slot)` — `mcl_trees:wood_pale_oak` x4.
3. **Crafting table**: planks into `craft` 1,2,4,5 → `craft()` → take —
   `mcl_crafting_table:crafting_table`; `place_at(<air next to the player>,
   "mcl_crafting_table")` (3x3 grid needs the table nearby — and remember
   `place_at` wants the **air node above the surface**, not the surface).
4. **Sticks**: planks vertical at `craft` 1,4 → `craft()` → take —
   `mcl_core:stick` x4.
5. **Wooden pickaxe**: planks across `craft` 1,2,3 + sticks at 5,8 → `craft()` →
   take — `mcl_tools:pick_wood`.
6. **Stone**: `dig_at` auto-selects the best tool in the inventory, so no
   manual wield is needed; `find_nodes_near(pos, 20, ["mcl_core:stone"])`,
   `goto` into reach, `dig_at`, collect.
7. **Stone pickaxe**: 3 cobble across 1,2,3 + 2 sticks at 5,8 → `mcl_tools:pick_stone`.

Verify each step with `get_inventory()` (and `screenshot()` for placement).
When `dig_at` reports `timeout`, the node is still there: the tool was too
weak (bare-hand stone ≈ 7 s, and the server's dig pool can reject very fast
digs), out of reach, or a mob interrupted the dig.

## Respawning

If dead (HP 0), interacts silently do nothing. Respawn via the death screen:

```lua
-- run_lua:
core.send_inventory_fields("__builtin:death", {quit = "true"})
```

Or prevent death during automated play: `set_setting("enable_damage", "false")`
or keep to a safe area. (`core.send_respawn()` is a dead legacy packet.)

## Cheats & Settings

`toggle_cheat(name, enabled)` / `set_setting(name, value)`:
`jetpack`, `fullbright`, `fastdig`, `autojump`, `fly`, `noclip`, …

See `doc/al_csm_api.md` for the full cheat list. `survival(true)` enables the
survival preset at once (autoeat, autototem, autojump, autorespawn, autotool).

## Agent tools (preferred for autonomous play)

The `agent` clientmod adds verified, non-blocking tools — prefer them over
raw dig/place once a session is running:

| Tool | Notes |
|------|-------|
| `agent_ctx()` | One-call orientation: pos/look/hp/flags/wielded/inventory summary/objects near/ping |
| `agent_events(since)` / `wait_event(type)` | Event feed: chat, death, damage, dig/place confirmations, inventory changes, formspecs |
| `goto(pos, mode)` | `walk` (A* + lua controls, default), `sprint`, `fly` (free_move flight), `rtp` (burst teleports), `tp`; returns `{ok, state, dist}` |
| `dig_at(pos)` / `place_at(pos, item)` | Verified with hold-to-dig timing, auto tool selection and server-side confirmation |
| `use_node(pos)` | Right-click a node (chests/doors/furnaces); returns the opened formspec name |
| `punch_object(id)` / `aim_at(pos, velocity, gravity)` | Aim (gravity-compensated for projectiles) and attack an entity |
| `survival(true)` / `eat()` / `respawn()` / `agent_mem(key, value?)` | Survival preset, persistent memory |

Movement note: `open_target(4)` (via `run_lua`) returns a nearby genuinely
walkable target — use it to avoid cliffs when the destination is unknown.

### Real-server findings (oy.edgy1.net, mineclonia anarchy)

- **`rtp` is throttled by the server's anticheat** — burst teleports get the
  position reset (effective ~1 node/s). Use `walk`, or `fly` on servers that
  tolerate flight.
- **Flight recipe** (works when the server grants no `fly` priv, because
  `priv_bypass` defaults to true and `checkPrivilege()` honours it):
  `priv_bypass = true`, `free_move = true`, plus `noclip = true` to avoid
  terrain collision, then drive `core.localplayer:set_velocity(dir * speed)`
  every step. `agent.go_to(pos, "fly")` does everything except `noclip` —
  set `set_setting("noclip", "true")` yourself when the path may cross
  terrain (flight still collides with blocks, and progress then stalls with
  `stuck: no progress`). `free_move` is turned off automatically when the
  flight ends.
- **`free_move` alone does not lift** — the client's `applyControl` only maps
  `control.jump` to upward motion, and that field is rebuilt from real keys
  every frame. `set_lua_control` from a pipe call lasts one frame;
  `set_autojump(true)` is the only Lua path that survives (it is OR-ed into
  `control.jump` in `Game::updatePlayerControl`).
- **Never register a `globalstep` from a pipe chunk** — there is no
  unregister API, so it keeps running forever (a stray autojump pulse will
  fly the player to the sky). Long-lived behaviour belongs in a clientmod
  (like `agent`) with a guard flag.
- **Timers (`core.after`) registered from a pipe chunk may not fire** — chain
  one action per pipe call instead of scheduling the next step from Lua.
- **Deaths scatter the inventory** and respawn points are far apart; a
  `goto` in progress reports `failed: no progress` when a respawn teleport
  happens mid-walk. With `survival(true)` (autorespawn) the loop recovers, but
  expect to re-gather resources after a death.
- **Node-level verification is the only reliable one.** For your own
  placements the server skips `AddNode` (it assumes the client predicted), so
  `on_node_add` may not fire — the agent's action sweep therefore confirms
  placements by reading the actual node state, not by waiting for the event.
- **Enum cheat settings are crash-fatal when invalid.** Writing e.g.
  `killaura.target_mode = "true"` used to kill the client through a nil lookup
  in a globalstep; `resolve_mode()` now falls back to a valid mode. Prefer
  `toggle_cheat` and documented enum values.

## Screenshots

`screenshot()` returns a scene-only PNG (no HUD). Needs a client that is
rendering — fails if detached/hidden (reattach first). Invaluable for
verifying placements the client map misreports.

## Item Names (MineClonia)

| Item | Name |
|------|------|
| Pale Oak Log | `mcl_trees:tree_pale_oak` |
| Pale Oak Planks | `mcl_trees:wood_pale_oak` |
| Stick | `mcl_core:stick` |
| Crafting Table | `mcl_crafting_table:crafting_table` |
| Wooden Pickaxe | `mcl_tools:pick_wood` |
| Stone Pickaxe | `mcl_tools:pick_stone` |
| Stone | `mcl_core:stone` |
| Cobblestone | `mcl_core:cobble` |
| Dirt | `mcl_core:dirt` |
| Dirt with Grass | `mcl_core:dirt_with_grass` |
| Pale Oak Leaves | `mcl_trees:leaves_pale_oak` |

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| New MCP tools don't appear in your tool list | The host caches the tool list at MCP-server start — restart the `antilua-mcp` server (or the host) after editing `util/mcp/server.py`. Until then, drive the same API with `run_lua("return agent.…")` |
| `place_at` says `not buildable` | You targeted a *solid* node. `find_nodes_near_under_air` returns the surface — build at `surface + {0,1,0}` |
| `dig_at` times out | Tool too weak (bare hand on stone ≈ 7 s), out of reach, or a mob interrupted. `dig_at` picks the best tool in the inventory automatically; re-run it or get a better one |
| `goto` ends `failed: no progress`/`stuck` | Cliffs/water you can't walk up, a respawn teleport mid-walk, or anticheat throttling. Use `agent.open_target(n)`, retry, or switch to `fly`/`tp` |
| `goto` on `rtp` crawls at ~1 node/s | The server's anticheat resets burst teleports. Prefer `walk` or `fly` |
| Everything is ignored after death | Dead players' interacts are dropped. `survival(true)` auto-respawns; otherwise `respawn()` |
| Inventory empty after a risky trip | You died — deaths scatter items as drops. Expect to re-gather |
| `place_node` puts the wrong block | It places the *wielded* item — use `place_at(pos, item)`, or `give_and_wield(item)` / `wield_item(item)` |
| `get_node` disagrees with reality | Client map lags/predicts; confirm with `dig_at`/`place_at` results, `screenshot()` or re-sync |
| Craft grid indices wrong for 2x2 | Use 1,2,4,5 (not 1,2,3,4) — craft list has width=3 internally |
| Crafting a 3x3 recipe fails | Needs a placed crafting table nearby |
| Items missing after digging | Walk/tp onto the item entity (pickup radius ~1.5) and re-check `get_inventory()`; drops despawn |
| Server command fails | `{ok:false, error:...}` — inspect the error, don't assume success |
| Screenshot fails | Client detached/hidden — reattach; needs a rendering frame |
| Setting an enum cheat to a bogus value | Can kill the client (fatal globalstep error). Use documented values / `toggle_cheat` |
| Need raw Lua | `run_lua(code)` — same client state, JSON results; see `skills/antilua-lua-pipe/SKILL.md` |
| Pipe stops responding | Don't delete/recreate the FIFO — the client keeps the old inode; restart the client. One client per pipe path |

## Helper Scripts

Gameplay Lua snippets live in `skills/playing-the-game/scripts/` (kept for
`run_lua` / raw-pipe use):

| Script | Purpose |
|--------|---------|
| `send_lua.py` | Send a .lua file to the pipe and print response |
| `check_inv.lua` | Show all inventory contents |
| `check_hp.lua` | Show HP |
| `where.lua` | Show position + surrounding blocks |
| `craft_table.lua` | Craft a crafting table from planks |
| `craft_sticks.lua` | Craft sticks from planks |
| `craft_pick.lua` | Craft a wooden pickaxe |
| `place_table.lua` | Place the crafting table |
| `dig_stone.lua` | Mine stone with equipped pickaxe |
| `find_trees.lua` | Find nearby trees |
| `gather_wood.lua` | Gather wood from nearest tree |
| `consolidate.lua` | Stack item stacks in inventory |
