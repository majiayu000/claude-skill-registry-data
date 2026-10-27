---
name: oysterity
description: Play Oysterity (oy.edgy1.net:30420), the oldest anarchy server in Luanti — a 2b2t-style Mineclonia world with no resets and a persisted per-server map. Covers connecting as the standard ophelia account, the one-time greeting, the mob-dangerous spawn, the saved-map scouting workflow, base siting, verified gathering and crafting loops, the opt-in raider playbook, and session state. Use when the task mentions Oysterity, oy.edgy1.net, port 30420, or the anarchy server.
---

# Playing Oysterity

Server-specific playbook. The mechanics live in `skills/playing-the-game`
(tools) and `skills/antilua-mcp` (pipe); this file is only what is true *about
this server*.

## The server says this about itself

MOTD, verbatim (it arrives in chat on join, and `probe.lua` pulls it back out
of the `mcp_chat` buffer):

> The oldest anarchy server in luanti! dating, hacking, griefing, killing
> allowed. No moderation, no rules except don't mess with server operation.
> Runs mineclonia. Much like minecraft's 2b2t with no world resets and almost
> no admin intervention.

- Discord `discord.gg/dmXPU9prKV`, Matrix `#oysterity-anarchy`
- Spiritual successor of **Clamity** anarchy
- `/ignore add <playername>` and `/help ignore` are advertised — use them for
  spammers instead of fighting them
- Announces itself on every join: `version: 5.14.0 | game: Mineclonia |
  uptime: … | clients: <list>`, plus the running mineclonia commit
- "Expect visual issues with mobs on clients < 5.9" (mobs render wrong on old
  clients — a client bug, not a sign you are being trolled)
- Population observed 15–25 players; expect real people, not an empty world
- **No world resets**: what you build stays until someone destroys it, and
  your own map coverage keeps growing between sessions

## Accounts

- Standard account: **`ophelia`**. It is the identity in
  `scripts/agent_play.sh` and the default for the state file.
- Fresh accounts use Shakespearean names (`horatio`, `falstaff`, `prospero`, …).
  Register a second name only when a second perspective genuinely helps — the
  main case is checking the spawn region from a "stranger" without your own
  reputation skewing the read.
- **Greet exactly once per account**, from the pool in
  `scripts/greetings.json` (friendly but cynically robotic). `state.py greet`
  prints the next line this account has never used and records it; send that
  text with the MCP `send_chat` tool. Do not read chat back to check it
  arrived — the queue is enough. When the pool is exhausted it says so; stay
  quiet rather than repeating one.
- The account reads as a bot to players (one player opened with "I wanted to
  test if the person can difference a bot with a player"). Keep it friendly,
  keep it rare, do not argue when someone calls it out.

## Session bootstrap

```sh
pkill -9 -x antilua; pkill -9 Xvfb            # one client per pipe
scripts/agent_play.sh --name ophelia --minimap-max-blocks 500000
skills/oysterity/scripts/state.py greet       # only if greetings_used is empty
```

`--minimap-max-blocks` matters: the cap is read when the saved map loads, and
Oysterity's map is larger than the 100000 default, so without it the farthest
tens of thousands of blocks are dropped from the in-memory map on every join
(see below). Raise it in the launcher, not at runtime.

Then, through the MCP `antilua` tools:

1. `agent_ctx()` — orientation (`skills/antilua-mcp` for the tool list)
2. `survival(true)` — autoeat/autototem/autojump/autorespawn/autotool; without
   it, ophelia dies repeatedly and each death scatters the inventory
3. `screenshot()` — what the spawn looks like
4. `run_lua` the probe for the server-side facts:
   `send_lua.py skills/oysterity/scripts/probe.lua` → ground node, in water, hp,
   players/mobs within 24 nodes, the server's own status line, map coverage
5. If `state.py get greetings_used` is empty, this is a first join:
   `state.py greet` → send the line with `send_chat` (it records itself)

## The saved map is the main strategic asset

Oysterity is a permanent world, and this client keeps a per-server map of it:

- Path: `data/server/oy.edgy1.net_30420/minimap/bigmap.sqlite` (run-in-place;
  gitignored). `probe.lua` prints the live path via `al_bigmap:get_save_dir()`.
- At last check: **162,045 blocks**, coverage x −96…1456, z −361…627, y −6…143.
- The stored data already contains other players' work — `mcl_chests`,
  `mcl_colorblocks`, `mcl_torches`, `mcl_stairs`, `mcl_farming` all appear — so
  bases are visible before you walk there.
- **Cap trap**: `al_bigmap.cpp:1019` prunes the blocks farthest from the player
  whenever the map loads and exceeds `minimap_save_max_blocks` (default
  100000). The pruning only drops them from the in-memory map; the database
  rows survive, so the map *looks* intact on disk while far-field scouting data
  is gone in the session. Pass `--minimap-max-blocks 500000` and check
  `bigmap_coverage` after joining.
- Tools: `bigmap_coverage` (bounds + block count), `bigmap_pixel(x, z)`
  (`{node, height, air_count}` topmost node of the column),
  `bigmap_section({min,max})` renders a PNG for a formspec or for reading.
  Coverage only grows where the client has been, so a blank area means
  unexplored, not empty.

## Verified server behaviours

| Observation | Consequence |
|---|---|
| `hamlet was blown up by Creeper` three seconds after joining | The spawn region is mob-infested. `survival(true)` before wandering; check `mobs_near` from the probe |
| `rtp` resets the position between attempts (~1 node/s) | Server anticheat throttles burst teleports. Use `walk`, or `fly` with `noclip` for long distances |
| Flight is tolerated | `priv_bypass` (default true) + `free_move` + `set_velocity`; add the `noclip` setting or terrain stalls the run |
| `Packet quota used up for peer_id=1, was 1024 pkts` | Benign client-side warning under movement bursts; it recovers |
| Deaths scatter the inventory as drops and respawn is far from where you died | Expect to re-gather; keep a stash at the base rather than carrying everything |
| Digs are verified by reading node state, never by `on_node_add` | The server assumes client prediction and re-sends the block, so the event never fires for your own placements |
| Real players are online, including griefers | Treat other builds as scenery unless the user explicitly asks for a raid |

## Default playbook: quiet base builder

1. **Probe** (`probe.lua`) and screenshot the spawn.
2. **Scout** for a site:
   `send_lua.py skills/oysterity/scripts/find_base.lua` — scores the saved map
   for flatness, water nearby, distance from spawn and absence of player builds,
   and returns the best candidates with a first waypoint. Tune with client
   settings (the client sandbox has no `os.getenv`), e.g.
   `run_lua("core.settings:set('oysterity_base_radius','800')")`; the knobs are
   `oysterity_base_center`, `oysterity_base_radius`, `oysterity_base_step`,
   `oysterity_spawn`, `oysterity_base_avoid` (known bases to penalise) and
   `oysterity_base_top`.
3. **Walk there** — `goto({x, y, z}, "walk")`. If it stalls, take the returned
   `first_waypoint` or a fresh `run_lua` `agent.open_target(8)` instead of
   beelining.
4. **Record it**: `state.py set-base X Y Z --note "under the oak line"`.
5. **Gather with verified actions** — `find_nodes_near(pos, 24, ["mcl_trees:tree_…"])`,
   `goto` within reach, `dig_at(log)`, then walk onto the drop to collect.
   Dig state confirms the node is gone server-side; the item still has to be
   picked up physically (radius ~1.5).
6. **Craft the progression** — planks → sticks → crafting table (place it at
   `surface + {0,1,0}`, not on the surface) → wooden pickaxe → stone.
7. **Stash** — keep the valuable stack at the base and note it:
   `state.py set stash '{"location":{"x":…},"items":{"mcl_core:stone":64}}'`.
8. **Log the session**: `state.py log "base established, first oak collected"`.

## Opt-in playbook: raider

Only when the user asks for it, and ask again before anything destructive —
this is a real server with real players.

1. Find targets from the map: scan `bigmap_pixel` for `mcl_chests` clusters, or
   check `known_bases` from `state.py show`. Record what you find:
   `state.py add-base OWNER X Y Z`.
2. Approach at night or in fog (`set_time`), on foot or by flight with `noclip`.
3. Loot with `interact("use", …)` on the chest / `get_inventory("nodemeta:x,y,z")`
   and `move_item`, then leave. Do not strip a base that has not been seen with
   a player in it recently unless the user says griefing is the goal.
4. Retreat on low hp: `eat()`, `respawn()` if caught, and log the loot.
5. Never touch spawn infrastructure or grief while the user is off-session.

## Session state

`skills/oysterity/state/<account>.json` (gitignored; `_template.json` is the
schema) holds base origin and note, stash contents, `known_bases`,
`greetings_used` and a session log. `state.py` is the only writer — the client
sandbox has no `io`, so nothing in Lua can touch it:

```sh
skills/oysterity/scripts/state.py show
skills/oysterity/scripts/state.py greet --as ophelia          # next greeting
skills/oysterity/scripts/state.py get greetings_used
skills/oysterity/scripts/state.py set-base 120 12 -340 --note "cave mouth"
skills/oysterity/scripts/state.py add-base Red_line_farmer3 1450 40 600
skills/oysterity/scripts/state.py log "dug into the mesa, lost a log to lava"
```

The clientmod's `agent.mem` is per-process and dies with the client, so it is
for scratch notes only — anything that must survive a restart goes here.

## Failures and what they mean here

| Symptom | Cause | Fix |
|---|---|---|
| Client dies seconds after joining | Spawn mobs (creepers seen) | `survival(true)`, check `mobs_near`, do not idle in the open |
| `goto` reports `stuck: no progress` | Cliffs, water, or a respawn teleport mid-walk | `agent.open_target(n)`, re-`goto`, or `fly` with `noclip` |
| `rtp` crawls | Antecheat | Drop it; walk or fly |
| Inventory empty after a trip | Died, drops scattered, and nobody picked them up | `respawn()`, re-gather, stash earlier |
| Big map looks empty at a distance | Area never explored; coverage only grows where you have been | Walk/fly there once, or check `bigmap_coverage` bounds |
| Map lost its far field after joining | Over the `minimap_save_max_blocks` cap | `--minimap-max-blocks 500000` in the launcher |
| `cannot open Lua pipe` | Stale or dead client | Kill `antilua`/`Xvfb`, relaunch; never delete/recreate the FIFO |
| Greeting already used | `greetings_used` is full or a previous join sent one | `state.py greet` picks an unused line; if it reports exhausted, stay quiet |
| A Lua helper cannot read a file | The client sandbox strips `io` and `os.getenv` | Keep file access in `state.py`; pass tuning via `core.settings` |

## Key files

| Path | Purpose |
|---|---|
| `scripts/agent_play.sh` | Launcher; defaults to ophelia on Oysterity, `--minimap-max-blocks` |
| `skills/oysterity/scripts/greetings.json` | Greeting pool (32 lines, friendly but cynical robot) |
| `skills/oysterity/scripts/state.py greet` | Picks the next unused greeting and records it |
| `skills/oysterity/scripts/probe.lua` | Session/server probe |
| `skills/oysterity/scripts/find_base.lua` | Base-site scout from the saved map |
| `skills/oysterity/scripts/state.py` | Cross-session state (base, stash, greetings, log) |
| `skills/oysterity/state/_template.json` | State schema |
| `data/server/oy.edgy1.net_30420/minimap/bigmap.sqlite` | The saved map (gitignored) |
| `skills/playing-the-game/SKILL.md` | General gameplay mechanics and item names |
| `skills/antilua-mcp/SKILL.md` | MCP tool reference and agent-first workflow |
