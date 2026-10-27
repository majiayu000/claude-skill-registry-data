---
name: mineclonia-pr-review
description: |
  Review and test Mineclonia pull requests (Codeberg). Use when the user gives
  a Mineclonia PR number and wants the PR branch checked out in games/mineclonia,
  smoke-tested with the Antilua engine, and reviewed for exploits such as
  coordinate leaks, item duplication, memory leaks, and other game-breaking bugs.
---

# Mineclonia PR Review & Test

Review Mineclonia PRs from https://codeberg.org/mineclonia/mineclonia/pulls.
The game checkout lives at `games/mineclonia` (remote `origin`). Testing uses
the **Antilua engine** (`./bin/antilua`, run-in-place) — never the system
`luanti`.

## Workflow

The review runs in two phases:

1. **Automated review (you):** the user gives you a PR number, several PRs, or
   criteria to look for PRs. For each PR: fetch it, smoke-test + lint it,
   review its diff against the checklist below, and drive its behavior with
   the **antilua MCP tools** (they reach a running client on the PR branch).
2. **Manual testing (the user):** they go through the PRs one by one. For each
   one: `mcla_pr_open.sh` opens the PR page in the browser and
   `mcla_pr_launch.sh` checks out the branch, creates the
   `mcla_test_pr_<PR>_<branch>` world, and launches the game interactively
   (pipe live, so MCP works while they test).

Always finish with `mcla_pr_restore.sh` — it kills any running client and
restores the pre-review branch + any backed-up uncommitted changes.

Ready-to-go scripts live in `scripts/` (relative to this skill's directory).
Prefer them over ad-hoc commands; they encode every hard lesson so far.

| Script | Purpose |
|--------|---------|
| `mcla_pr_list.sh` | List open PRs w/ metadata; `--small --draft --author --keyword --min-rows` |
| `mcla_pr_fetch.sh <PR>…` | Refresh `origin/main`, fetch `pr/<N>` refs (use `+` + `--update-head-ok` — a ref may already be checked out) |
| `mcla_pr_checkout.sh <PR>` | Safe checkout: backs up uncommitted tracked files to `$MCLA_STATE_DIR/wip_backup/`, cleans the tree, checks out |
| `mcla_pr_restore.sh` | Kill clients, restore pre-review branch + WIP backups (verified) |
| `mcla_pr_smoke.sh <PR> [N]` | N server smokes (default 3, random load order) + luacheck changed files |
| `mcla_world_create.sh <PR>` | Idempotent `worlds/mcla_test_pr_<PR>_<head.label>` (sqlite, damage off, broad privs) |
| `mcla_pr_launch.sh <PR>` | checkout + world + launch interactively w/ MCP pipe (`--workspace N` for i3, `--headless` for xvfb) |
| `mcla_pr_open.sh <PR>` | `xdg-open` the Codeberg PR page |
| `mcla_pr_review.sh <PR>` | One-command automated pass (fetch/checkout/diff/smoke/lint; `--client` boots a headless client for MCP testing) |

### 1. Get PR metadata (Codeberg / Gitea API)

```bash
PR=<number>
curl -s "https://codeberg.org/api/v1/repos/mineclonia/mineclonia/pulls/$PR" | \
  jq '{title, state, draft, user: .user.login, head_ref: .head.ref, head_sha: .head.sha, base_ref: .base.ref, head_label: .head.label, body}'
curl -sL "https://codeberg.org/mineclonia/mineclonia/pulls/$PR.diff" -o /tmp/mcl_pr_$PR.diff
```

- Read the PR body to learn the intent.
- **PR comments/reviews MUST be read and taken into account, critically but
  seriously: treat reviewer claims and author statements as credible unless
  you can prove them wrong** (`/pulls/$PR/comments`, `/pulls/$PR/reviews`).
  They often flag exactly the edge cases to test (dupe vectors, perf notes,
  intent clarifications). Note disagreements and verify both sides.
- Note if the PR is draft/closed/merged — report that, still review if asked.

### 2. Check out the PR branch in games/mineclonia

Gitea mirrors fork heads, so `refs/pull/$PR/head` works even for fork PRs
(no fork remotes needed). Use `scripts/mcla_pr_checkout.sh` (it backs up
uncommitted tracked changes; untracked files stay). Manual equivalent:

```bash
cd games/mineclonia
CUR=$(git rev-parse --abbrev-ref HEAD)
git fetch origin main:main                     # refresh base
git fetch --update-head-ok origin "+refs/pull/$PR/head:pr/$PR"
git checkout pr/$PR
git diff main...HEAD --stat                    # PR changes (three-dot)
```

This temporarily changes the game the Antilua engine loads. Restore with
`scripts/mcla_pr_restore.sh` afterward.

### 3. Smoke-test with the Antilua engine

Run from the repo root. The world `dummy_autoquit` (gameid `mineclonia`,
`backend=dummy`, no map writes) has an `autoquit` worldmod that logs
`SERVER SUCCESSFULLY STARTED` ~5s after mods load and shuts down — a clean
automated pass/fail. Fallback world: `worlds/test_mcl` (sqlite).

Automated via `scripts/mcla_pr_smoke.sh <PR> [N]` (N smokes + luacheck). Manual
equivalent:

```bash
# Server smoke test — PASS iff log shows "SERVER SUCCESSFULLY STARTED"
timeout 120 ./bin/antilua --server \
  --world ~/var/src/MT/minetest/worlds/dummy_autoquit 2>&1 | tee /tmp/mcl_pr_$PR_server.log

# Client smoke test (headless) — singleplayer runs the embedded server,
# so autoquit also fires; check debug.txt for the marker + errors
xvfb-run -a timeout 120 ./bin/antilua --go \
  --world ~/var/src/MT/minetest/worlds/dummy_autoquit \
  --logfile /tmp/mcl_pr_$PR_debug.txt 2>&1 | tee /tmp/mcl_pr_$PR_client.log

# Error scan
grep -nE "ERROR|LuaError|stack traceback|attempt to (index|call|perform arithmetic on|concatenate).*nil|out of memory|Segmentation" \
  /tmp/mcl_pr_$PR_debug.txt /tmp/mcl_pr_$PR_server.log || echo "NO ERRORS"
```

- If the game fails to start (crash, load error, missing marker) that is a
  **Critical** finding — dig into the traceback.
- **Keep the default random mod load order ON for the smoke test** — do not
  pass `random_mod_load_order = false`. The repo's `antilua.conf` already sets
  `random_mod_load_order = true`, and that is exactly what exposes
  missing-dependency bugs (a mod calling `table.merge`, `mcl_pistons.*`,
  another mod's global, etc. at load time without declaring it in `mod.conf`).
  A PR must work under *any* load order. Run the server smoke test several
  times (each server start shuffles the order) and treat any `ModError`
  during mod load as Critical — flaky = still broken.
- **Do NOT try to override the game path** with `MINETEST_GAME_PATH` (deprecated)
  or a separate checkout: `getAvailableGamePaths()` searches the default
  run-in-place `games/` first and keeps the first match, so the checked-out
  `games/mineclonia` is always what loads. Test branches there.
- PRs only touch Lua (game mods) → no engine rebuild needed. If the binary is
  missing/stale, build via the `antilua-testing` skill.

### 4. Lint the changed mods

```bash
cd games/mineclonia
luacheck -q $(git diff main...HEAD --name-only -- '*.lua') || true   # changed files
luacheck -q mods                                                      # whole game
```

### 5. Trigger all modified code paths via the MCP server

The `antilua` MCP server (`util/mcp/server.py`, registered in the host) exposes
a running client as structured tools — use them instead of hand-writing Lua-pipe
requests. `mcla_pr_review.sh <PR> --client` boots a headless client on the PR
branch with the pipe live; then drive it:

- Orient: `get_player_pos()` → `screenshot()` → `get_player_look()`
  (or `get_client_status()` if tools misbehave).
- Setup: `give_and_wield("item", count)` / `teleport` /
  `set_setting("enable_damage", "false")` / `set_time("noon")`.
- Interact: `place_node` / `dig_node` run the **same server-side code paths as
  real player interaction** (`register_on_placenode`, `register_on_dignode`,
  `on_construct`, `on_dig`, ABM/redstone callbacks). Prefer
  `interact("place", {type="node", under, above})` when
  `place_node` mispredicts (it places the client's stale wielded item and
  `under == above == pos` breaks wall/sign `on_place`).
- Inventory: `get_inventory` / `move_item` / `craft` / `take_craft_result` and
  node inventories via `run_lua` (`core.get_inventory("nodemeta:x,y,z")`).
- Anything else: `run_lua(code)` (JSON-serialized results).

A PR review should enumerate each modified function/handler and trigger it.

This is essential for behavior-heavy PRs (node placement/update logic, dig
handlers, inventory, redstone). Prefer MCP tools; fall back to raw Lua only
for paths the tools don't cover.

#### Session setup that works (learned the hard way)

```sh
# Random mod load order is LEFT ON for the smoke test (step 3) to catch
# missing-dependency bugs. It is only disabled here, TEMPORARILY, to get a
# deterministic session for the code-path harness AFTER load-order behavior
# was already checked. The PR must still work with random order enabled.
printf 'pipe_lua_enable = true\npipe_lua_path = /tmp/antilua_lua\nrandom_mod_load_order = false\nenable_minimap = true\nprevent_natural_damage = true\n' > /tmp/mcl_pipe.conf
xvfb-run -a ./bin/antilua --go --world worlds/test_mcl --config /tmp/mcl_pipe.conf --logfile /tmp/mcl_test_debug.txt &
```

- **A dead player's interacts are silently dropped.** The death state
  persists in the world DB, so the player may connect dead (hp=0) and every
  `place_node`/`dig_node` is ignored with only an action-log line. Respawn
  and retry until `core.localplayer:get_hp() > 0`:

  ```lua
  core.send_inventory_fields("__builtin:death", {quit = "true"})
  ```

- **Disable damage during the session** so the player can't die mid-test:
  set `enable_damage = false` in the test world's `world.mt` (back it up and
  restore after), or keep the player at a safe spot. Mobs (zombies/spiders)
  will otherwise kill you and silently invalidate every placement.
- **`core.place_node` sends nothing if the client map block isn't loaded.**
  `Game::nodePlacement` reads the client map first (`map.getNode`) and bails
  (no interact, no item consumption) when the block is missing. In headless
  runs the client map only reliably loads a small radius around the player's
  *current* position — so teleporting far away makes placements fail. Build
  within ~2-4 blocks of the (alive) player.
- **Don't trust `core.get_node_or_nil` for verification** — it reads the
  client map, which lags/never syncs far areas. Use the **AlBigMap** instead:
  `core.al_bigmap:get_pixel(x,z)` returns the column's surface node from the
  server's block stream (`{node, param2, height, air_count}`). It updates
  within a few seconds of a placement, but only for columns inside the
  client's subscribed radius (again: build near the player).
- **Bigmap pixel = topmost node per column.** It masks whatever is below:
  a tree canopy hides a wall at ground level (pick tree-free cells), and
  `walkable=false` tops (torches, signs, pressure plates) may not show as
  the surface — so verify *wall variants* only on top-less columns.
- **Digging hard nodes needs the right tool.** Walls (`pickaxey`) won't
  instant-dig with a bare hand in survival; wield `mcl_tools:pick_stone`
  (or whatever the group needs) before `core.dig_node`.
- **Leftover nodes pollute results.** The test world persists between runs
  and items/nodes accumulate. `giveme` + place/dig the same cells across
  runs leaves stale walls that make new walls connect unexpectedly. Dig the
  whole rig (with the right tool) between scenarios and verify the pixels
  returned to terrain first.
- **Give items** via `give_and_wield("name", 64)` — gives via /giveme,
  waits for the client inventory to sync, moves the stack into a free hotbar
  slot and wields it, returning `{slot, name, inventory}`. For items you
  already hold, `wield_item("substring")` does the same without giving.
- **Write valid JSON to the FIFO** (python `json.dumps` or `jq -n`); a hand
  escaped `\"` in a bash string corrupts the request and you get a
  `ClientLuaPipe: JSON parse error`. Use a unique response file per request
  and `sleep` 1-2s between writes.
- **`core.place_node(pos, node)` ignores the 2nd arg** — it places the
  client's *wielded* item. To place a specific item, `give_and_wield(item)`
  then place (verify with the returned `name`). `interact("place",
  {type="node", under=..., above=...})` sends a real placement with proper
  pointed thing (needed for standing signs/walls where `under != above`).
- **The client's inventory and wield state lag a beat headless.** Instead of
  hand-rolled polling loops, use `wait_until(code, timeout)` to poll any Lua
  expression until truthy, and `give_and_wield` which already waits for the
  item to appear. `set_wield_index` does NOT reliably change what the
  *server* places: the server may place its own stale wielded item. Confirm
  what the server actually placed via the debug log
  (`ACTION[Server]: ... places node <name> at (x,y,z)`), not via client reads.
- **Server command responses are in the chat log.**
  `run_server_chatcommand("grantme", "all")` returns the server's reply lines
  in `chat` (e.g. "You don't have permission (missing privilege: give)") —
  check them instead of guessing; `get_chat_log(20)` reads recent lines.
- **The server debug log is ground truth for placements/digs.** Grep
  `places node|digs node|uses .*pointing` in the debug.txt. The client map
  (`get_node_or_nil`) shows client-side *predictions* and stale data; the
  bigmap reflects the server block stream but also lags and hides
  `walkable=false` tops (signs) and non-top nodes. Only the log tells you
  what the server really did.
- **The pipe runs in the CLIENT Lua state — game mod globals are not
  visible.** You cannot call `mcl_signs.string_to_ustring` etc. directly.
  Drive behavior instead through: chat commands (`giveme`), `core.interact`
  (place/dig/use), `core.send_nodemeta_fields(pos, formname, fields)`,
  `core.send_inventory_fields(formname, fields)`, `InventoryAction`, and read
  state via `core.get_meta(pos)` / `core.get_inventory("nodemeta:x,y,z")`
  (node meta/inventory DO sync to the client, unlike `get_node_or_nil`).
- **`core.get_meta(pos):get_inventory()` does NOT exist client-side.** Use
  `core.get_inventory("nodemeta:x,y,z")` (returns `{input={...}, output={...}}`).
- **`InventoryAction` methods must be separate statements, NOT chained.**
  `from`/`to`/`set_count`/`craft`/`apply` each return `nil`, so
  `InventoryAction("move"):from(...):to(...)` dies with `attempt to index a
  nil value`. Call them line by line:
  ```
  local a = InventoryAction("move")
  a:from("player:singleplayer", "main", N)
  a:to("nodemeta:x,y,z", "input", 1)
  a:set_count(1)
  a:apply()
  ```
  This fires the real server `on_metadata_inventory_*` handlers (e.g.
  stonecutter recompute). Prefer `player:singleplayer` over `current_player`
  (a client-internal location the server rewrites via `applyCurrentPlayer`).
  `apply()` both sends and predicts locally.
- **Your OWN placements never produce a `register_on_node_add` event.** The
  server assumes the placing client predicted the node: for items with a
  `node_placement_prediction` it calls `SetBlockNotSent` (a full block
  re-send, no `TOCLIENT_ADDNODE`), and for others `ResendBlockIfOnWire`
  (usually a no-op) — so the block arrives as `TOCLIENT_BLOCKDATA` and the
  AddNode hook never fires. Verify placements with `get_node`/bigmap pixels,
  not events. (Digs DO emit `register_on_node_remove`: the server keeps the
  block "sent" for successful digs.)
- **A Lua error inside a clientmod globalstep is FATAL** — the client shuts
  down ("Access denied. Reason: Lua: Runtime error … in callback
  environment_step()"). Invalid *enum* cheat settings reach such code (e.g.
  `killaura.target_mode = "true"` used to nil-index a check function), so
  only write documented values; `toggle_cheat`/the cheat menu are safe. After
  such a crash the pipe and window are gone — relaunch and note the world
  may need re-setup.
- **`set_lua_control` lasts a single frame** — `Game::updatePlayerControl`
  rebuilds `player->control` from the real keys before the pipe runs each
  frame, so control values set from a pipe request are consumed by that
  frame's `applyControl` and then overwritten. Long-running control changes
  (sustained forward/jump) must go through settings (`continuous_forward`,
  `free_move`, `jetpack`) or `core.set_keypress`/`set_autojump`, applied
  from a globalstep.
- **Never register a globalstep from a pipe chunk** during tests (it can
  never be removed and will fight the test's own actions), and do not chain
  steps with `core.after` from a pipe chunk — those timers do not reliably
  fire. Do one action per request, or use the `agent` clientmod
  (`agent.go_to`/`agent.dig`/`agent.place`) which owns its long-lived logic.
- **Node-formspec callbacks (`on_receive_fields`) via `core.send_nodemeta_fields`.**
  Hand-rolled raw `TOSERVER_NODEMETA_FIELDS` packets fail with `Reading
  outside packet` — use the API. Global `register_on_player_receive_fields`
  callbacks (e.g. sign text) need `core.send_inventory_fields`, but the server
  only accepts a non-empty formname if it previously SHOWED that formspec to
  the player — so rightclick the node first via
  `core.interact("use", {type="node", under, above})`. Some formspecs are
  gated by a setting (signs need `mcl_signs_editable=true`), and even then
  the embedded server may not show it — if the debug log shows no
  `uses <node>` / formspec packet, the flow is blocked; fall back to
  replicating the changed function's logic in the pipe.
- **The `--config` file gets overwritten by the client on shutdown** (it saves
  its full settings). Write the config after killing the client, not before
  restart. Prefer a fresh `dummy-v7-seed-mineclonia` world (backend=dummy,
  regenerated each run) over the heavy `test_mcl` sqlite world, which floods
  the log with ABM warnings and syncs inventory very slowly. Load time is
  ~2-4 min; poll the FIFO before sending.
- **`pkill`ing the client can hang the shell tool** (it waits on the killed
  process's inherited fds). Start clients with
  `setsid xvfb-run -a ./bin/antilua ... >log 2>&1 < /dev/null &`, and after
  killing, verify with `ps` in a fresh command.
- **Check for a stale client before launching the next one.** Only one client
  may own a pipe path, and a leftover process (or a live one you forgot about)
  makes the new run look broken: `cannot open Lua pipe … No such file or
  directory` or a client that never creates the FIFO. Do
  `pkill -9 -x antilua; pkill -9 Xvfb; ps aux | grep '[b]in/antilua'` first.
- **After a client crash (fatal Lua error) or several force-kills, a
  *windowed* launch on the real X display can hang** — the log stops after the
  first separator and no FIFO appears. `xvfb-run -a` still works, so fall
  back to headless; don't debug the mod code in that situation.
- **Always add new tricky findings / noteworthy details to this skill file.**
  If a future run surfaces a non-obvious gotcha (sync lag, API quirk, packet
  format, setting that doesn't take effect, tool hang, etc.) that isn't
  captured above, add it to this list as a bullet so it doesn't have to be
  rediscovered — the list is the accumulated hard-won knowledge of the
  workflow.
- **You CANNOT point the engine at a separate game checkout via
  `MINETEST_GAME_PATH`/`ANTILUA_GAME_PATH`.** `getAvailableGamePaths()`
  (`src/content/subgames.cpp`) searches the default run-in-place `games/` dir
  FIRST and `try_emplace` keeps the first match, so a worktree/symlinked game
  never wins. (The env var is `ANTILUA_GAME_PATH` in this fork —
  `MINETEST_GAME_PATH`/`LUANTI_GAME_PATH` are deprecated.) To test a branch you
  must check it out directly in `games/mineclonia`.
- **A broken uncommitted WIP file in the game checkout crashes EVERY smoke
  test** (syntax error → `ModError: Failed to load ...`). If the user has
  in-progress edits: `cp <file> /tmp/wip_backup`, `git checkout -- <file>`,
  test, then restore byte-identical (`diff -q` to confirm) and switch back to
  their branch.
- **Flaky random-load-order failures are Critical.** Run the server smoke ≥3-5
  times. A single failure with `attempt to index global 'X' (a nil value)` at
  mod load = missing `depends`/`optional_depends` (e.g. #4788 used
  `mcl_pistons.register_on_move` at load without declaring mcl_pistons; failed
  1/5). "Flaky = still broken" — also check runtime-only undeclared deps.
- **Verify pure-Lua logic with the system `lua5.1` binary** (no engine/client):
  replicate the changed function and compare against the old behavior — set
  membership (#4777 village squares), formula equivalence (#4645 haste/fatigue),
  or table-length quirks. Note `#({nil,2}) == 2` in Lua 5.1, so
  `unpack({nil, 2})` yields `(nil, 2)` (used by load-time test suites).
- **When a PR adds/removes an item GROUP, grep for remaining consumers.**
  `grep -rn 'get_item_group(.*"<group>"' mods/`. #4614 dropped `group:crossbow`
  from the crossbow def but `mcl_serverplayer/items.lua` and
  `mcl_mobs/combat.lua` still check it → silently broken player/mob logic even
  though the game boots fine.
- **`swap_node`-based variant transitions are NOT in the server log.**
  `update_wall` swaps wall variants silently — the log only shows the initial
  placement. After triggering a transition, force a block re-sync
  (`set_pos` far away, wait, `set_pos` back) then read `get_node_or_nil` /
  bigmap to see the current variant.
- **Engine-feature-gated PRs: verify the engine supports the feature before
  reviewing** (e.g. `step_up_mode` → `es_StepUpMode` in `src/object_properties.cpp`
  with `legacy/floaty/rigid`; `set_sky` `fog`/`auto_dim_skybox` → `l_object.cpp`).
  If the engine lacks it, note compatibility risk.
- **Refactors touching item-meta serialization / tool caps are exploit-prone:**
  verify the old↔new round-trip (shulker box `compressed` base64+zstd) and that
  formulas are equivalent, and that `set_tool_capabilities` on meta isn't
  rewritten every tick.
- **`set_wield_index` clamps to the hotbar count**
  (`min(index, getMaxHotbarItemcount())`), so put the item in a hotbar slot
  (1-9) before `interact("place")` — indices beyond the hotbar silently clamp
  and the server places its stale wielded item.
- **Only run ONE headless client at a time** — they share the `/tmp/antilua_lua`
  FIFO and conflict. Verify `ps aux | grep -c '[b]in/antilua --go'` is 1 before
  starting a session.

#### Verification pattern

```bash
# place -> poll bigmap pixel until it shows the expected node
for try in $(seq 1 10); do
  resp=$(cat /tmp/resp)
  [ "$resp" = "mcl_walls:brick_short_flat" ] && break
  sleep 3
done
```

For each modified code path, record what you triggered and what you observed
(e.g. wall placed → `_short_pillar`; 3-wall line → middle `_short_flat`; dig
end → middle reverts). Note paths that can't be verified via the pipe (e.g.
piston/observer redstone rigs need a real in-game setup) and say so in the
report rather than claiming full coverage.

### 6. Manual testing by the user

After the automated pass, the user goes through the PRs one by one manually.
For each PR:

1. **`scripts/mcla_pr_open.sh <PR>`** — opens the Codeberg PR page in the browser.
2. **`scripts/mcla_pr_launch.sh <PR>`** — checks out `pr/<PR>`, creates the
   dedicated test world `worlds/mcla_test_pr_<PR>_<head.label>` (idempotent —
   safe to re-run), and launches the game interactively with the MCP Lua pipe
   enabled. Use `--workspace N` to send the window to i3 workspace N,
   `--headless` for xvfb instead of the real display.
3. User tests in-game; MCP stays live on `/tmp/antilua_lua`, so the reviewer
   can assist (teleport, giveme, screenshots) while they play.
4. **`scripts/mcla_pr_restore.sh`** when done — kills the client and brings
   back the pre-review branch + any working-tree changes.

## Code review checklist

Review the diff (`git diff main...HEAD`) with a focus on exploits and
game-breaking bugs. Report findings by severity (Critical/High/Medium/Low)
with `file:line`. Grep for the patterns below, then read each hit in context.

### Coordinate leaks (privacy / anti-cheat)

Exposing one player's position to other players/clients:

- `get_pos()` results (esp. `get_player_by_name(...):get_pos()` or
  `object:get_pos()`) in `chat_send_player` / `chat_send_all` / `chat_send_server`,
  formspecs, `show_formspec`, or messages visible to other players.
- `pos_to_string` / `dump` / `core.serialize` of positions in player-visible
  output, chat commands, or HUD elements broadcast to clients.
- Positions leaking via `add_particlespawner`, `add_entity`/`add_item`
  visuals, `send_channel_message` (any CSM can read), or
  `on_receive_fields` echo-back of other players' coords.
- X-ray style leaks: `get_node` / `find_nodes_in_area` results (cave/ore
  data, structure contents) rendered into formspecs or chat.

```bash
grep -rnE "get_pos\(\)|pos_to_string|get_player_by_name" mods/ | grep -iE "chat_send|formspec|send_channel|hud|send_player|dump"
```

### Item duplication

Paths where items are created without removing their source, or destroyed
without dropping:

- `on_construct` / `on_destruct` / `on_blast` / `after_dig_node` /
  `handle_node_drops` / `on_dig` granting items (e.g. `add_item`) without
  consuming the source or dropping the node.
- `take_item` / `add_item` / `remove_item` / `move_item` where the return
  value (or a `nil`/failed move) is ignored, so items appear/disappear twice.
- Crafting: output count vs input, `on_craft` adding extras, 2x2 vs 3x3 grid
  mismatch, craft preview result not consumed.
- Containers: transfer logic in `on_close`, `on_metadata_inventory_*` handlers,
  hopper `_mcl_..._on_hopper_in/out` double-firing, shulker/barrel/chest races.
- Pickup logic (`item_entity` `on_punch`/`on_step`, `on_collide`, armor/offhand)
  adding a stack without removing the entity.
- Creative / `/give` / reward paths that add without checking existing stacks.
- Anything gated only by client-sent packets (inventory actions, dig/place)
  without server-side validation.

```bash
grep -rnE "add_item|take_item|remove_item|move_item|handle_node_drops|on_construct|on_destruct|after_dig_node|on_blast" mods/
```

### Memory leaks

State that grows without bound:

- Tables keyed by player/entity/pos that are never cleaned in
  `on_leaveplayer`, `on_destruct`, `on_detach_child`, `on_remove_player`.
- Caches appended in `register_globalstep` / `register_abm` without eviction;
  lookups stored per tick that only grow.
- `minetest.after` timers that reschedule themselves forever and hold
  references to players/entities.
- `minetest.register_*` called on every join (globalstep/ABM/on_joinplayer
  chains re-registering handlers or accumulating in tables).
- `mod_storage` / `storage:set_string` growth (unbounded keys or data).
- Entities / particlespawners / sounds spawned and never removed.

```bash
grep -rnE "on_joinplayer|on_leaveplayer|register_globalstep|register_abm|minetest\.after|storage:set_string" mods/
```

### Structural / behavioral regressions (no crash, silently wrong)

- **Group removed/changed:** when a PR edits an item/node's `groups`, check every
  consumer still works:
  `grep -rn 'get_item_group(.*"<group>"' mods/` and `grep -rn 'group:<group>' mods/`
  (the #4614 `group:crossbow` removal broke `mcl_serverplayer` + mob AI without
  failing the smoke test).
- **Itemstring/type changes:** craftitem→node conversion (e.g. #4168 resin_clump)
  — verify `_mcl_crafting_output`/recipes still round-trip, no code assumes
  `def.type == "craftitem"`, itemstring unchanged (renames must NOT change
  itemstrings or they break saves/crafts).
- **API signature changes:** renamed/removed args (e.g. `place_seed` lost its
  `plantname` arg) — grep all callers; a wrapper that accepts both `:` and `.`
  calls hides breakage if a caller passes positional args that shift.
- **Formula/behavior refactors:** compare old↔new math (haste/fatigue dig speed,
  punch interval, reel impulse) and verify equivalence or justify the change;
  check `register_on_player_inventory_action`/`register_allow_player_inventory_action`
  blockers (e.g. prolonged-use) don't lock the player out of inventory actions
  if state gets stuck.
- **Worldgen set changes:** replacing a hardcoded coordinate list with a
  generator — diff the resulting SETS, not just length (`#4777` added 3 cells /
  removed 2 dupes → new villages differ, despite "same logic" claim).

### Game-breaking bugs

- Nil index / nil call on objects that may be gone (`player`, `object`,
  `meta`) — especially in `on_leaveplayer`, ABMs, `minetest.after`.
- Coordinate math: off-by-one, swapped axes, using node coords where block
  coords expected (or vice versa), integer/float position confusion.
- `set_node` / `remove_node` / `add_node` on unloaded or foreign areas;
  replacing a node without dropping the old one.
- Infinite loops / unbounded recursion; `minetest.after` firing storms;
  heavy work in globalstep/ABM (perf = crash/server hang).
- Formspec injection: untrusted user input concatenated into formspec strings
  (`minetest.show_formspec`), `minetest.deserialize` on attacker-controlled
  data.
- Mapgen, portal/dimension travel, and schematic code with crashes or bad
  params.
- Privilege escalation: granting/using privs (`interact`, `give`,
  `teleport`, `fly`, `noclip`) beyond what was intended.

## Report

Summarize: PR title/author/state, base→head, changed mods/files, test results
(server + client + lint), then findings grouped by severity with `file:line`
and a one-line explanation of the exploit/bug and why.

## Cleanup

```bash
scripts/mcla_pr_restore.sh     # kills clients, restores branch + WIP
```

Manual equivalent:

```bash
cd games/mineclonia
git checkout "$CUR"            # restore original branch
git branch -D pr/$PR           # drop temp branch (when done)
rm -f /tmp/mcl_pr_$PR.diff /tmp/mcl_pr_$PR_server.log \
  /tmp/mcl_pr_$PR_client.log /tmp/mcl_pr_$PR_debug.txt
```

Per-PR test worlds (`worlds/mcla_test_pr_*`) are intentionally KEPT for
re-testing; remove them by hand if disk space matters.