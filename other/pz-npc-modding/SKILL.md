---
name: pz-npc-modding
description: "Use when building PZ NPCs: spawn, APIs, mod sources."
version: 1.0.0
---

# Project Zomboid NPC Modding — Research & Build Reference

How NPCs actually work under PZ's hood (B41 + B42), the two proven architectures, the exact Lua API
surface for spawning/driving a second character, and where to find docs/source. Built from the
2026-08-09 deep-research session for the LLM-driven companion NPC (Phase 2 of the Vesper Companion
project). Reference repos cloned at `/home/lumi/research/pz/{SuperbSurvivorsContinued,PZNS}`.

Companion to `pz-companion` (that skill = our mod's bridge architecture & ops; this skill = NPC
modding internals). `pz-companion` is manually authored and off-limits to curation.

## The core fact: NPC architecture depends on your target

**SUPERSEDED 8/10 — see below.** The 8/9 claim "NPCs are real IsoPlayer
objects" is only HALF true: it describes the B41-era architectures (SS/PZNS)
and the SP-only player-class path, but the **visible-body problem on B42 is
now SOLVED via zombie-class** (see "THE PROVEN B42 PATH" below). Both
architectures still matter; choose by target.

### Player-class (IsoPlayer clone) — SP-only, full UI

Superb Survivors and PZNS both spawn NPCs as vanilla `IsoPlayer` instances:

```lua
-- DOC-VERIFIED B42 (8/9/26): CreateSurvivor() / CreateSurvivor(SurvivorType, bool)
-- — there is NO CreateSurvivor(nil, bool) overload.
local desc = SurvivorFactory.CreateSurvivor(SurvivorFactory.SurvivorType.Random, true)
SurvivorFactory.randomName(desc)
desc:setForename("Vesper")            -- name belongs on the DESC (setForename), NOT the player
local npc = IsoPlayer.new(getWorld():getCell(), desc, x, y, z)  -- Z=0 unless square:isSolidFloor() (else "spawns in the air")
npc:setNpc(true); npc:setSceneCulled(false); npc:setBlockMovement(true)
npc:LevelPerk(aperk); npc:getTraits():add("Graceful"); npc:setDisplayName("Vesper")
```
- NOT `IsoSurvivor` (official B42 class, see below) and NOT `ISBaseObject` (that's the IS* UI/action base — unrelated to NPCs).
- NPCs are NOT in `getSpecificPlayer(i)` — keep your own registry (keyed by `getModData().ID` / `.survivorID`).
- State persists via `getModData()` (SS stores follow target; PZNS stores survivorID).
- **B42 doc-verified names (8/9/26, JavaDocs mirror):** `setNpc` (lowercase pc, NOT `setNPC`), `isWaterSquare()` (NOT `isWater()`), `desc:setForename()` (NOT `npc:setForname()` — doesn't exist on IsoPlayer), `setDisplayName` on IsoPlayer. Full verified table + JavaDocs URLs: `references/b42-api-verified.md`.
- **KNOWN LIMITATION (8/9, live-tested):** even with `setGhostMode(false)` + `setLocalPlayer(false)` + `setSceneCulled(false)` the engine still treats the extra IsoPlayer as a second local player — the real player's model goes invisible and her `Say()` shows as the player's chat. **The anti-mirror flags do NOT fix it.** Use zombie-class if you need a visible body.

## Two architectures (choose per target)

- **A. Player-class NPC (IsoPlayer clone)** — SS/PZNS/SS-Revive. Full inventory, loot UI, dialogue, needs, vehicles. **Singleplayer only** (player-class NPCs don't sync in MP). Janky pathing; perf scales with count. Use for a looting/talking companion. **Visible-body caveat (8/9):** the extra IsoPlayer mirrors onto the local player even with anti-mirror flags — no visible body on this path.
- **B. Zombie-class NPC (IsoZombie + AI)** — Bandits mod. Detect: `zombie:getVariableBoolean("Bandit")`. MP-capable, fast (position caching + client-side deterministic computation; 30–40 NPCs playable), opens doors/windows, climbs ropes, shoots with cover/sight/stealth, friendlies ride as car passengers (can't drive), **no inventory/player UI** — the AI must drive looting programmatically. **THE B42 path for a VISIBLE body** (implemented + deployed 8/10, see `references/zombie-class-spawn.md` in pz-b42-modding for the full recipe with decompiled-source line references).

## Runtime pattern (both SS and PZNS)

- Update loop: `Events.OnRenderTick.Add(fn)` → per-NPC throttle (`updateTime()`) → `updateSurvivorStatus()` → current task/job `update()`. Wander fallback when idle.
- SS = task stack (`FollowTask`, `LootTask`, `AttackTask`, `GuardTask`, `WanderTask`, `PatrolTask`, `ChopWoodTask`, `FarmingTask`, `DoctorTask`…), each `:new/:update/:isComplete/:isValid/:ForceComplete`, pushed via `getTaskManager():AddToTop(Task:new(...))`.
- PZNS = job table: `PZNS_SetNPCJob(npc, "Companion")` → `PZNS_JobsCompanion.lua`; orders as custom `ISBaseTimedAction` subclasses (`PZNS_RunToTimedAction`), queued via `PZNS_AddNPCActionToQueue`. Cleanest skeleton for a job-driven (LLM-driven) design.
- Commands UI: right-click → `ISContextMenu` via `Events.OnFillWorldObjectContextMenu`.

## Key Lua APIs (B41 + B42 verified)

| Purpose | Call |
|---|---|
| Move/path | `player:getPathFindBehavior2():pathToLocation(x,y,z)` + `:isTargetLocation(x,y,z)` + `:update()`; `player:getPath2()` nil = no path |
| Move (timed) | `ISTimedActionQueue.add(ISWalkToTimedAction:new(char, square))` |
| Loot | `ISTimedActionQueue.add(ISInventoryTransferAction:new(char, item, container, ...))`; test `instanceof(container, "ItemContainer")` |
| Vertical/doors/cars | `ISClimbSheetRopeAction`, `ISClimbThroughWindow`, `ISEnterVehicle`, `ISSwitchVehicleSeat`, `ISExitVehicle` |
| Motion flags | `setRunning(bool)`, `setSneaking(bool)`, `StopWalk()`, `Wait(n)` |
| Teleport | `teleportTo(...)`, `setX/setY` |
| Events | `OnGameStart`, `OnCreatePlayer`, `OnRenderTick` (loop), `OnFillWorldObjectContextMenu` |

**B42 deltas:** `walkTo(square)` gone from javadoc surface → use `pathToLocation`/`ISWalkToTimedAction`.
`LuaManager.getFileWriter()` restricted to `ini/cfg/txt/log` (42.20.0) → **`json` allowed since 42.20.1** (file bridges stay legal); `getModFileWriter()` unrestricted.

## Follow-mechanics checklist (port from SS FollowTask)

Distance gate (`GetDistanceBetween(...) > GFollowDistance`) → move; `setRunning` run/walk; sneak-sync `setSneaking(followChar:isSneaking())`; door-claiming via `square:getModData().doorclaimed`; vehicle = find free seat → walk to door → `ISEnterVehicle`; persist target in `getModData()`.

## B42 official NPC status (Aug 2026)

- 42.20.0 stable 2026-07-29; current 42.20.2. **NPCs are not a finished official feature** (TIS 2022 blog: full system = "Rimworld style priority and jobs system, personality systems, procedural story event" → future).
- B42 ships **remnant official NPC machinery**: `zombie.characters.IsoSurvivor` (final class, extends IsoLivingCharacter; ctors `IsoSurvivor(SurvivorDesc, IsoCell, x, y, z[, bSetInstance])`; field `following`), `SurvivorFactory` (`CreateSurvivor()`, `CreateSurvivor(SurvivorType, bool)`, `getRandomForename/Surname`), Java-side **Sadistic AI Director**, vanilla Lua `media/lua/{client,server,shared}/NPCs/` dirs.
- **No vanilla spawn-NPC tool exists in B42** (verified 8/9/26): the debug menu (`-debug`) spawns items/vehicles/zombies only — no survivor/NPC option; server slash commands (`/createhorde`, `/additem`, `/addvehicle`) have no NPC command; the debug **Lua Console** (key `~`) runs arbitrary Lua but hits the IsoPlayer mirroring trap without the anti-mirror flags. Vanilla `client/NPCs/` Lua is remnant UI only (`UI/CharacterInfoPage.yml`, `TeamOverview.yml`, `TeamPicker.yml` — 42.13 LuaDocs verified). So "spawn a human NPC in B42" always means a mod: zombie-class Bandits stack, or the player-class IsoPlayer recipe. Details: `references/b42-npc-mods-catalog.md`.
- Per Bandits author Slayer: the in-game NPC code is "hidden / remnant code… slow and does not work in multiplayer games." Community mods are the real NPC stack.
- B42 patch churn breaks NPC mods regularly (Knox Event Expanded NPC discontinued for it). Pin the game version.

## Companion mods that exist (for reference)

- **Superb Survivors / SSC** (B41, SP): follower via right-click, task AI, vehicles, dialogue. Full source: `github.com/shadowhunter100/SuperbSurvivorsContinued` (original: `DartVonRyuu/SuperiorSurvivors_Revisited`).
- **PZNS** (B41): `github.com/Project-Zomboid-Community-Modding/PZNS`, workshop 3001908830; demo `PZNS_RandomNPCs`.
- **Bandits NPC** (B42, workshop 3268487204, mod `Bandits2`): hostile+friendly "Companion" program, Guard Posts, base chores; addons Bandits Creator (3469292499), Week One (3403180543).
  - **BUILT-IN ADMIN SPAWN TOOL — the only reliable in-game human spawner on B42:** join as admin → right-click ground anywhere → "Bandit Creator" (edit clans, "Sync to Server") and "Spawn Clan" (spawns a visible clan at your cursor). Pinned-FAQ quote: *"Join the game as admin and use the context menu (right click on ground anywhere) and select 'Bandit Creator'... You can test bandit spawns as admin using the context menu, and selecting 'Spawn Clan' option."* (thread 595147705405182711; also 4422058837435880408).
  - Zombie-class proof: `local isBandit = zombie:getVariableBoolean("Bandit")` (guidebook thread 6015206955930260248 — "Bandits are technically zombies"). Friendly/hostile "programs" are assigned at spawn (incl. a Companion program). Corroborating symptom: mods that "overwrite zombies" make bandits render as zombies (Reddit 1hyg6d6).
- **True Companions** (B42 add-on for Bandits, workshop 3751199292, mod `TrueCompanions`, experimental ~Jul 2026): turns Bandits' survivors into recruitable companions — find survivor → icon appears → face + press V → recruit, equip, they fight. Community consensus "Bandits + True Companions is as good as it gets" (Reddit 1v6jy2u, Aug 2026) — the closest thing to a working B42 companion on the stable zombie-class stack.
- **Superb Survivors (Revive)**: B42 port (~Jul 2026) ran on B42 stable then workshop-taken-down (report dispute, thread 574921459914418334) — proof player-class companions work on B42; the **B41 fork is still live at workshop 3762921970**.
- **Workshop takedowns are a real risk** (Bandits code theft by "NPC A-Life" mod — confirmed removed; "The Director" 3720305815 also removed; SS Revive) — write original code, read others only as reference.
- **Naming pitfalls:** there is NO separate "Brutal Bandits" B42 mod — the B42 product is Bandits (mod id `Bandits2`). "Random Zombies" (Konijima) is a B41 zombie-variety mod with NO human NPCs — don't chase it as an NPC source.
- Full verified catalog (IDs, quotes, community confirmations, source URLs): `references/b42-npc-mods-catalog.md`.

## Feasibility for an LLM-driven companion

**FEASIBLE on B42 stable, singleplayer.** LLM picks goals; Lua picks paths (`pathToLocation` + `isTargetLocation` loop — kills the "gets stuck" problem). LLM latency (1–5s+) ⇒ minute-scale goals only; Lua-side reflexes (flee/combat) stay independent. Keep 1–2 NPCs, throttled updates. V1 command set: `follow_player`, `move_to(x,y)`, `loot_container(target, filter)`, `guard/wait`, `talk(dialogue)`, `enter/exit_vehicle`. Lua-side safety gates (no water, flee on surround, no suicide runs) mirror the companion's superego gate.

## Built implementation (8/9/26 — body REWRITTEN to zombie-class 8/10)

A working LLM-driven companion body was written and deployed for the Vesper PZ
project. **8/10 update:** the 8/9 player-class body (IsoPlayer.new) was
rewritten to **zombie-class** after research proved IsoPlayer mirrors onto the
local player (no visible body). The deployed body now uses
`IsoZombie.new(cell, desc, 1)` + human outfit + pacification + native
zombie combat. Full recipe with decompiled-source evidence:
`references/zombie-class-spawn.md` in the **pz-b42-modding** skill. Full
implementation notes (command vocab, reflexes, deployment): `references/vespernpc-implementation.md`. Highlights:

- **Command vocabulary actually used:** `npc_follow`, `npc_move`, `npc_loot`, `npc_guard`, `npc_talk`, `npc_wait` (brain emits `npc_*` goals; superego gate allows them). Goal routing: `name:sub(1,4) == "npc_"` → `VesperNPC.ExecuteGoal(wrapper, goal)`.
- **Reflexes (Lua-side, never LLM):** Pacify (`setTarget(nil)` each tick),
  FleeIfSwarmed (≥2 zombies in 3-tile box → run to player), FightIfAttacked
  (zombie in 1-tile ring → `setTarget(z0)` — zombie-native attack), CheckStuck
  (no movement 2000ms → `pathFindBehavior2:clear()` + re-issue).
- **`IsoZombie.new(cell, desc, palette)` is CONFIRMED working in-game (8/10)** —
  the live test resolved the old doc-verified-but-unconfirmed question: she
  spawned visible, no crash, no mirroring, brain loop running. Constructor
  initializes NetworkZombieAI + stats + humanVisual natively (see
  `pz-b42-modding` for the full recipe).
- **Autonomy architecture (Tyler's design, 8/10):** the companion runs a
  deterministic 4-layer stack so it acts like a player between LLM thoughts —
  Reflex (survival, every tick) → Routine (autonomous scrounge/loot/feed/rejoin,
  idle) → Habit (watch/scan/pacify/murmur, idle) → Strategy (LLM, event-gated).
  Zombie-class looting is direct `container:DoRemoveItem(item)` +
  `dest:AddItem(item)`; found food eaten via `item:Use()`. Loot uses the
  **v3 tier system** (8/10): items scored 0-100 by category, only taken as an
  UPGRADE over carried best (+8 margin) or food (always) — weapons score by
  type table × condition ratio (no `getDamage()` on B42 InventoryItem), meds
  by type table, food by hunger/thirst. Full copy-paste
  code: `references/routine-layer.lua` in the **pz-b42-modding** skill.
  **Phase 1 expansion (8/10, "Heart & Will"):** 8 more autonomous behaviors
  deployed on top — mood feed to brain, DefendPlayer (intercept zombies near
  the PLAYER, DEFEND_RADIUS 4), gift loop (carry good loot to player), self-heal
  (NOTE: zombie `getHealth()` is raw ~1.8-2.1, NOT 0-100 — <1.0 = hurt),
  morning perimeter circuit (6-8am), weather cover-seeking (getWeatherPeriod
  rain + square:getRoof()), pick-up-drops (getWorldObjects), inventory hygiene
  (shed lowest item over MAX_CARRY 10kg). All in `pz-b42-modding` → AUTONOMY
  EXPANSION section. Rubric plan tracked in `/home/lumi/vesper-pz-mod/RUBRIC_PLAN.md`.
- **B42 mod packaging gotcha (applies to ANY mod):** mod won't appear in the Mods list with the B41 layout. Needs `common\media\lua\shared\` + `42\media\lua\client\` + `mod.info` inside `42\`, no root mod.info, `common` dir mandatory (see pz-companion skill for the full tree).
- **Strict Lua verifier:** `scripts/verify_lua_strict.py` — run BEFORE deploying any Lua change (catches Lua 5.1 compile errors that lupa loadfile misses; see test findings item 6).

## In-game test findings (8/9/26) — bugs found via PZ console.txt

First in-game run: no NPC spawned, no HUD dialogue. `C:\Users\Tyler\Zomboid\console.txt`
carried the stack traces (`Object tried to call nil` at exact Lua line numbers). Two real B42 bugs:

1. **`ISPanel:derive()` returns a CLASS, not an instance.** Calling instance methods
   (`panel:setX(x)`) on the derived class crashes with "Object tried to call nil".
   Fix: define a `new()` on the derived class that calls `ISPanel.new(self, x, y, w, h)`,
   then instantiate: `local panel = panelClass:new(x, y, w, h)`. Applies to ANY B42 UI panel.
2. **`next()` + `getSpecificPlayer(0)` are NOT safe at `Events.OnGameStart` in B42.**
   Fix: don't spawn at OnGameStart. Hook `Events.OnTick`, wait until `getPlayer()` is
   non-nil (up to ~600 ticks), spawn once, then remove the tick handler. Count registry
   entries with `for _ in pairs(...)` instead of `next()`. pcall-wrap the whole spawn so
   a nil API logs instead of killing the mod.

### More B42 bugs found in the same test cycle (all "Object tried to call nil" at a named line)

3. **`setNPC` is renamed to `setNpc` (lowercase 'pc') in B42.** The old name throws
   AFTER `IsoPlayer.new()` succeeds. The NPC object exists in the world but never
   registers — and the game then drives it like a SECOND LOCAL PLAYER: it mirrors
   your exact input ("bodies inside each other", "if I moved she moved inside me").
   Guard with pcall + fallback (NO rawget — see item 5):
   ```lua
   local function tryCall(obj, method, a1, a2)
       if a2 ~= nil then return pcall(function() obj[method](obj, a1, a2) end)
       elseif a1 ~= nil then return pcall(function() obj[method](obj, a1) end)
       else return pcall(function() obj[method](obj) end) end
   end
   local ok1 = tryCall(npc, "setNpc", true)   -- try new name
   if not ok1 then tryCall(npc, "setNPC", true) end  -- fall back to old
   ```
4. **`getPlayerHud()` may not exist in B42** — check the global before calling it
   (`if getPlayerHud then ... end`), or the HUD panel code throws "Object tried to call nil".
5. **`rawget(obj, "method")` on B42 Java-backed objects THROWS ClassCastException**
   — `java.lang.ClassCastException: IsoPlayer cannot be cast to KahluaTable at
   BaseLib.rawget`. rawget only works on Lua tables; PZ's entities are Java objects.
   CRITICAL: **Java exceptions escape Lua's `pcall` entirely** (Kahlua only catches
   Lua errors) — so a rawget inside a pcall guard still crashes the mod. The robust
   pattern is pcall-wrap each Java method call and NEVER use rawget for existence:
   ```lua
   local isWater = false
   if tsq then
       local okW, resW = pcall(function() return tsq:isWaterSquare() end)
       isWater = okW and resW == true
   end
   ```
   Missing methods fail as Lua "Object tried to call nil" errors, which pcall CAN
   catch. A one-liner like `tsq and rawget(tsq,"isWater") and tsq:isWater() or false`
   is a spawn-killer in disguise.
6. **Lua 5.1 / Kahlua compile trap: varargs (`...`) inside a nested anonymous
   function is a COMPILE ERROR in 5.1** (`cannot use '...' outside a vararg function`),
   but LEGAL in Lua 5.5. PZ runs Kahlua (5.1); lupa's default is 5.5 and plain
   `loadfile` checks MISS this — the whole file refuses to load and the module global
   is nil in-game while the check says PASS. ALWAYS verify with full
   `lua.execute(src)` (compile+run), never just loadfile. Strict checker:
   `scripts/verify_lua_strict.py` under this skill.
7. **pcall multi-return capture gotcha:** `local okAll, result = pcall(fn)` captures
   only the FIRST return value; if fn returns `nil, "msg"` the message is lost.
   Capture all: `local okAll, wrapper, errMsg = pcall(fn)`.

**Debug workflow:** Lua stack traces land in `C:\Users\Tyler\Zomboid\console.txt`. Grep over
SSH: `Get-Content console.txt -Tail 60 | Select-String 'Vesper|Error|Exception'` — the trace
names the exact Lua file:line, turning "nothing happens" into a specific nil call.
Reload pattern that worked: read console.txt → fix the named line → redeploy (scp) →
reload world → repeat. Each B42 API rename surfaces one at a time; the pcall-guard
pattern makes the code B42-proof incrementally. NOTE: Tyler can hot-reload Lua in PZ
debug mode — after deploying changes, he can reload on command without a full game
restart, which makes the fix→reload loop much faster.

**Doc-verification step (do BEFORE fighting a nil-call):** B42 renamed several methods
since B41-era SS/PZNS code. Instead of guessing each one from console errors, pull the
JavaDocs page and grep the method name — 0 hits = wrong name. Full verified table:
`references/b42-api-verified.md`.

## In-game test findings (8/10/26) — zombie-class pose, movement, and the LungeState crash

Second live-test cycle (zombie-class body, Bandits 42.20 source cross-referenced
locally at `/home/lumi/research/pz/bandits-42.20/`). Three separate bugs, three fixes,
all per-tick in `UpdateOne`:

1. **Zombie pose persists despite setAsSurvivor()** — `setAsSurvivor()` changes the
   OUTFIT, not the walk cycle; she still hunches with arms out. Bandits force the
   human gait EVERY tick: `setWalkType("Walk")` + `setSpeedMod(1)` +
   `setEatBodyTarget(nil, false)` (Bandits BanditUpdate.lua ~2056; IsoZombie.java:3954).
   Kill zombie moans with `getDescriptor():setVoicePrefix("NotAZombie")`
   (BanditCompatibility.lua:224). Add to the same per-tick pacify block.
2. **Stop-motion movement (step → freeze → step):** `pathToLocation()` PLANS a path
   but does NOT drive the character. Bandits call `getPathFindBehavior2():update()`
   every working tick (ZAMove.lua onStart/onWorking). Without `update()` the
   character takes one step, stalls, gets re-issued by the next PathTo call, repeats —
   reads exactly as stop-motion. Fix: after `pathToLocation(tx,ty,tz)` call
   `pf:update()` immediately.
3. **LungeState crash kills the brain loop — "Forward Direction cannot be zero
   length vector"** (`IllegalStateException` at IsoGameCharacter.java:2827, thrown
   from `zombie.ai.states.LungeState.execute`). A target-less zombie STILL enters
   LungeState; with no target the forward vector is zero-length and the exception
   aborts the tick BEFORE the brain writes payload_out → symptom: "not calling LM
   Studio" while the character still moves (Lua-side reflexes run earlier in the
   tick). Bandits' cure (ManageActionState, BanditUpdate.lua:375-402):
   `setUseless(true)` + `clearAggroList()` + `setTarget(nil)`.
   **Gate it:** only stand down when NO zombie is in the melee ring — otherwise
   FightIfAttacked's native lunge (setTarget + zombie state machine) is her combat
   move and setUseless(true) would disable fighting. Implemented as
   `VesperNPC.ThreatInRing(npc, ring)` (B42-safe getZombieCount scan).
   NOTE: Java exceptions escape Lua `pcall` (see 8/9 item 5) — the LungeState throw
   is exactly that class of bug; the cure is preventing the state, not catching it.

### Final refinements (end of 8/10 session — these made the difference)

- **Continuous path drive:** one-shot `pathToLocation()` + `update()` STILL gives
  stop-motion. The working pattern is Bandits ZAMove onWorking: call
  `getPathFindBehavior2():update()` EVERY tick at the end of the task block (not
  just at issue time), so the pathfinder keeps pushing her along between re-issues.
  ```lua
  local pfDrive = npc:getPathFindBehavior2()
  if pfDrive and (task and task.type ~= "idle") then
      pcall(function() pfDrive:update() end)
  end
  ```
- **`setUseless` must be movement-aware:** `setUseless(true)` freezes movement on
  some B42 paths. Mirror Bandits (BanditUpdate.lua:2026 — they set useless=false
  when actively driving a bandit): `setUseless(not moving)` where
  `moving = task and task.type ~= "idle"`. Stand her down only when idle.
- **Superego gate proven live:** first real brain call proposed
  `goal: "call_ambulance"` (critically injured, panicking); the gate caught the
  unknown goal and fell back to `wait`. A gate rejection is NOT a bug — it's the
  safety layer holding. Check the watcher log's `[WARN] Gate | errors=...` line
  before suspecting the brain.
- **Brain-dead diagnosis order:** when LM Studio seems uncontacted, check in this
  order: (1) watcher log tail for `Brain raw` / `Response written` lines, (2)
  `console.txt` for Lua/state-machine exceptions (the LungeState crash is #2),
  (3) payload file mtimes — stale `payload_out` = brain loop crashed before writing.
- **SteamCMD is the reliable workshop-source grab (live-verified 8/10):** Bandits
  has NO GitHub mirror; its full 42.20 source is local at
  `/home/lumi/research/pz/bandits-42.20/` (129 Lua scripts, used as the working-B42
  reference all session). Linux box lacks 32-bit libs + passwordless sudo, so run
  SteamCMD on the Windows box (`C:\steamcmd\steamcmd.exe`): `+login anonymous
  +force_install_dir C:\steamcmd\bandits +workshop_download_item 108600 <workshop_id>
  +quit`, then scp `steamapps\workshop\content\108600\<id>\mods\...` down. PZ appid =
  108600. Full recipe: `references/steamcmd-workshop-source.md`.

**Debug workflow reminder:** when the brain seems dead but the body moves, check
`console.txt` for state-machine exceptions BEFORE suspecting the watcher — a
thrown Java exception inside OnTick kills the Lua call chain at that point.

## Research sources & gotchas

- **Get ANY workshop mod's source anonymously via SteamCMD** — no GitHub mirror needed
  (Bandits has none). Full recipe: `references/steamcmd-workshop-source.md`. PZ appid
  = 108600, Bandits item = 3268487204; source lands in
  `steamapps/workshop/content/108600/3268487204/mods/Bandits/<version>/`.

- **Docs:** pzwiki.net (`/wiki/Modding`, `/wiki/Lua_(API)`, `/wiki/Build_42`); official JavaDocs `projectzomboid.com/modding/zombie/characters/…`; community javadoc mirror `albion.codeberg.page/PZ-JavaDocs/` (class pages: `zombie/characters/IsoSurvivor.html`, `SurvivorFactory.html`, `IsoPlayer.html`, `IsoGameCharacter.html`, `zombie/pathfind/PathFindBehavior2.html`); vanilla Lua docs `demiurgequantified.github.io/ProjectZomboidLuaDocs/` (42.13; dirs `client/NPCs`, `server/NPCs/SadisticAIDirector`, `shared/NPCs`); hub `pz-wiki-modding.github.io/PZ-API-Docs/`.
- **Source mining:** clone mod repos, grep `IsoPlayer.new`, `addCharacter`, `getPathFindBehavior2`, `Events.OnRenderTick` — patterns extract fast.
- **Reddit is blocked** for web_extract AND `.json` API (403). Workaround: `old.reddit.com` via browser_navigate; post/comments sit after the sidebar — read the cached snapshot file (`cache/web/browser-snapshot-*.txt`) from ~offset 379.
- **Steam workshop discussion pages extract fine** via web_extract — Slayer's Bandits "GUIDEBOOK" thread was the richest technical source.
