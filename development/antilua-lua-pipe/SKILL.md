---
name: antilua-lua-pipe
description: Use when controlling a running Antilua client via the named pipe IPC, sending Lua commands, interacting with the game world, crafting items, or manipulating player inventory. Also use when the client is running but has no visible window (detached/headless mode).
---

# Antilua Lua Pipe Control

## Overview

The Antilua client exposes a named pipe (FIFO) at `/tmp/antilua_lua` (configurable via `pipe_lua_path` setting, requires `pipe_lua_enable = true`). Write JSON lines to send Lua code and read responses from an output file.

## Protocol

Request is a JSON line (one per line, `\n` terminated):

```json
{"code":"return 1+1", "file":"/tmp/resp"}
```

Response file format:
```
ok
2
```
On error, first line is `error` followed by the Lua error message.

## Basic Commands

Always use unique response files to avoid races — and **delete the response
file before writing the request**, otherwise a stale file from the previous
request looks like an instant reply:

```bash
rm -f /tmp/r1
echo '{"code":"return 1+1", "file":"/tmp/r1"}' > /tmp/antilua_lua
sleep 0.3 && cat /tmp/r1
```

Better: use `util/mcp/antilua_client.py` (or the MCP server), which does
this per request, retries transient timeouts and paces writes for you.

### Agent API (clientmods/ANTILUA/agent)

The `agent` clientmod exposes the building blocks for autonomous play over
the same pipe — prefer these over hand-rolling digs/places:

```lua
return agent.ctx(16)                       -- orientation snapshot
return agent.events(since_id, {"chat"})    -- event feed
return agent.go_to({x=1,y=2,z=3}, "walk")  -- walk|sprint|fly|rtp|tp
return agent.dig({x,y,z})                  -- verified dig (auto tool)
return agent.place({x,y,z}, "item:name")   -- verified place
return agent.survival(true)                -- survival preset
return agent.mem("note", "text")           -- persistent memory
```

## What NOT to do from a pipe chunk

- **Don't `core.register_globalstep(...)`** — there is no unregister API, so
  the callback runs for the rest of the session (a stray `set_autojump`
  pulse will fly the player to the sky). Long-lived behaviour belongs in a
  clientmod with a guard flag.
- **Don't chain steps with `core.after(...)`** — timers registered from a
  one-shot pipe chunk don't reliably fire. Do **one action per request** and
  let the caller (or a clientmod) sequence them.
- **Don't busy-wait** (`while os.clock() ...`) — the pipe runs on the
  client's main thread; the client freezes and every later request times out.
- **Don't write invalid enum cheat settings** (e.g.
  `killaura.target_mode = "true"`) — a globalstep error is fatal and shuts
  the client down. Stick to documented values / `toggle_cheat`.

### Position & Movement

```lua
core.localplayer:get_pos()                    -- returns {x,y,z}
core.localplayer:set_pos({x=0, y=10, z=0})   -- teleport
core.localplayer:get_yaw() / get_pitch()
core.localplayer:set_yaw(90) / set_pitch(0)   -- degrees
core.pos_to_string(pos, 0)                    -- "(X,Y,Z)"
```

### Looking & Pointing

```lua
core.camera:get_look_dir()         -- unit vector
core.camera:get_look_horizontal()  -- radians
core.get_pointed_thing()           -- raycast result
core.get_node_or_nil(pos)          -- node at position
```

### World Interaction

```lua
core.dig_node(pos)                 -- punch/dig a node
core.place_node(pos)               -- place wielded item
core.find_nodes_near(pos, radius, nodenames, search_center)
```

### Inventory

```lua
local inv = core.get_inventory("current_player")
inv.main     -- 36-slot array of ItemStack objects
inv.craft    -- 9-slot craft grid (server-dependent size)
inv.craftpreview    -- 1-slot recipe preview (shapeless for 2x2, full for crafting table)
inv.craftresult     -- 1-slot output
list[i]:get_name() -- item name
list[i]:get_count()-- stack count
```

### Server Commands

```lua
core.run_server_chatcommand("cmd", "args")  -- run /cmd args
core.get_privilege_list()                    -- {priv1=true, ...}
core.get_player_names()                      -- online player names
core.get_server_info()                       -- {address, ip, port, protocol_version}
```

## Crafting System

Crafting requires `InventoryAction` userdata (client-side). Items move via inventory actions sent to the server.

### Crafting Table

In MineClone2, the player has only a **2x2 craft grid** (slots 1,2,4,5 in the 3x3 `inv.craft` array). A crafting table block is needed for 3x3 recipes.

A single dark oak log (`mcl_trees:tree_dark_oak`) placed in the 2x2 grid crafts into a crafting table (`mcl_crafting_table:crafting_table`). Place it on the ground within reach to unlock the 3x3 grid.

### Moving Items

```lua
local a = InventoryAction("move")
a:from("current_player", "main", 3)     -- source location, list, slot index
a:to("current_player", "craft", 1)      -- destination
a:set_count(1)                           -- omit or 0 for entire stack
a:apply()
```

### Triggering Craft

```lua
local a = InventoryAction("craft")
a:craft("current_player")
a:set_count(1)  -- times to perform
a:apply()
```

### Taking Results

```lua
local a = InventoryAction("move")
a:from("current_player", "craftresult", 1)
a:to("current_player", "main", target_slot)
a:set_count(0)  -- 0 = move entire stack
a:apply()
```

### Recipe Flow (Dark Oak → Wooden Pickaxe)

1. **Logs → Planks**: Place 1 log in 2x2 grid → craft → take `mcl_trees:wood_dark_oak` (8 planks)
2. **Planks → Sticks**: Place 2 planks vertically (slots 1 and 4) → craft → `mcl_core:stick` (4)
3. **Planks + Sticks → Pickaxe**: Requires 3x3 grid (crafting table). 3 planks across top (slots 1,2,3) + 2 sticks down middle (slots 5,8) → `mcl_tools:pick_wood`

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Stale response file read as the answer | `rm -f` the response file **before** writing the request; use `antilua_client.py` instead |
| Multiple commands share the same response file | Use unique file paths per request |
| `InventoryAction` method chaining (`:from():to()`) doesn't return `self` | Assign to local variable, call each method separately |
| Race: commands execute out of order | Add `sleep 0.3` between pipe writes |
| Table values returned as `table: 0x...` (unserializable) | Use `dump()` or `core.write_json()`, or send `"serialize": true` in the request |
| A string like `"42"` comes back as the number `42` | The serializer coerces numeric-looking strings (Lua `lua_isnumber("42")` is true). Wrap the value in a table if the type matters |
| `set_lua_control` seems to do nothing | It is overwritten by `Game::updatePlayerControl` every frame — it only survives the frame the request ran in. Use `set_autojump(true)` for a jump pulse, or settings-based cheats |
| `globalstep` registered from the pipe keeps running forever | No unregister API — see "What NOT to do" above |
| `core.after` chains from a pipe chunk never fire | One action per request; sequence from the caller |
| Enum cheat setting with a bogus value | Fatal globalstep error kills the client — use documented values |
| Craft grid has items but craftpreview is empty | Might require server sync; check both `craftresult` and `craftpreview` |
| `core.get_wielded_item()` vs `core.localplayer:get_wielded_item()` | Use the latter (the former may not exist in some contexts) |
| `minetest.*` alias vs `core.*` | Use `core.*` (both work) |

## Cheats

Toggle settings to enable built-in cheats:

```lua
core.settings:set_bool("jetpack", true)    -- fly with jump key
core.settings:set_bool("fullbright", true)  -- max light
core.settings:set_bool("fastdig", true)     -- fast mining
core.settings:set_bool("autojump", true)    -- auto-jump obstacles
```

See `doc/al_csm_api.md` for the full list of cheat settings.

## MCP Server Alternative

If an MCP host has the `antilua-mcp` server registered, prefer its structured
tools over raw pipe writes (see `skills/antilua-mcp/SKILL.md`). It wraps this
same pipe, returns JSON, and covers player/world/inventory/server/cheat actions
plus a scene-only `screenshot()` — no response-file management or `sleep`
pacing needed. Raw pipe access remains available for anything the tools don't
cover (via `run_lua`).
