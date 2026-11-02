---
name: pz-b42-modding
description: "Use when debugging PZ B42 Lua mods or NPC spawns."
version: 1.0.0
---

# 🧟 Project Zomboid B42 Lua Modding

Writing and debugging PZ Build 42 mods — the language/semantics layer that sits
under any specific mod (companion, NPCs, UI, game-state bridges). Use whenever
working in PZ mod Lua: spawning NPCs, calling game APIs, chasing "Object tried
to call nil" / ClassCastException errors, or verifying a method name.

**Companion-specific protocol (Vesper, payloads, watcher): see the
`pz-companion` skill. This skill is the general B42 mechanics underneath.**

## The three rules that save hours

1. **PZ runs Kahlua = Lua 5.1.** Not 5.2+, not 5.4. Code that passes a modern
   lupa/5.5 check can still be a 5.1 COMPILE ERROR in-game.
   - **Varargs `...` inside a nested anonymous function is a 5.1 compile
     error.** The whole file refuses to load; the global stays nil; you get
     `attempted index: X of non-table: null` at the call site. Fix: capture
     args in named locals (`a1, a2`) before the nested function.
   - **Bare method reference as a condition is a 5.1 compile error.**
     `if obj:method then` → "function arguments expected near 'then'" — Lua
     5.1 requires an actual call (`if obj:method() then`) or an existence
     check done via pcall. Same for `if building:getDef then` style guards;
     the strict checker catches this even though it looks innocent.
   - Always verify with FULL `lua.execute(src)`, never just `loadfile` —
     loadfile can miss 5.1-isms. Use `scripts/verify_vesper_lua.py` (strict
     checker that executes each file; PZ-global references inside files are
     expected to fail outside the game — judge the *syntax* result).
2. **Java exceptions ESCAPE `pcall`.** Kahlua's pcall catches Lua errors only.
   A Java `ClassCastException` / `NoSuchMethodError` propagates straight
   through and kills the whole handler. This is the #1 cause of "I wrapped it
   in pcall but it still crashed".
   - **`rawget()` on a Java-backed object (IsoPlayer, IsoGridSquare, Stats)
     throws ClassCastException** — rawget needs a Lua table. Never use rawget
     as a method-existence guard on game objects. Use
     `pcall(function() obj:method(...) end)` — missing methods surface as
     Lua "Object tried to call nil", which pcall DOES catch.
   - **Calling a missing method on a Java object can throw ClassCastException
     instead of a clean Lua error.** Verify the method exists before calling
     (rule 3) and keep risky calls isolated.
   - **Bare-global namespace miss = "tried to call nil" every tick.** A
     constant defined as `VesperNPC.FLEE_DIST = 3` but used bare
     (`for dx = -FLEE_DIST, ...`) leaves `FLEE_DIST` nil → unary minus goes
     through a metamethod call → `tried to call nil` on EVERY render tick.
     Grep for bare identifiers when a per-tick error appears.
   - **Kahlua line numbers are FUZZY** — the reported line can be a few off
     from the real culprit. When a trace points at an innocent-looking line,
     read the whole function; the nil call is nearby. Distinguish: "tried to
     call nil" = nil function/identifier; "Object tried to call nil" = nil
     method on an object.
3. **B41-era reference code LIES about B42 API names.** Superb Survivors,
   PZNS, and any pre-42 tutorial use B41 names that B42 renamed. A research
   brief built from those repos is a *design map*, not an API reference.
   Verify EVERY method against the B42 JavaDocs mirror before writing spawn
   code: `https://albion.codeberg.page/PZ-JavaDocs/` (community mirror of
   official). Verified API table: `references/b42-api-verified.md`.
4. **`require` in Kahlua does NOT set module globals.** A module file that
   ends with `return json` loads fine but leaves the global `json` NIL unless
   something captures the return value (`local json = require "json"`).
   Symptom: `attempted index: encode of non-table: null` at the call site even
   though `require "json"` ran. Fixes: (a) in the module, add
   `json = json` / `_G.json = json` before `return`; or (b) capture the
   require return in every consumer; or (c) for tiny helpers, INLINE the
   function into the file that uses it — zero loader ambiguity (this is what
   VesperGameState.lua did for JSON after the require fix didn't take).
   Also: the debugger's RELOAD button may only reload the currently-open
   script, NOT all mod files from disk — a full world reload is the reliable
   way to pick up changed files.

## NPC spawning (player-class, single-player only)

Minimal verified flow (B42):

```lua
local desc = SurvivorFactory.CreateSurvivor(SurvivorFactory.SurvivorType.Random, true)
SurvivorFactory.randomName(desc)
desc:setForename("Vesper")            -- name on the DESC, not the player
local npc = IsoPlayer.new(getWorld():getCell(), desc, x, y, z)
pcall(function() npc:setNpc(true) end) -- lowercase 'pc', NOT setNPC
```

- `SurvivorFactory.CreateSurvivor()` has NO `(nil, bool)` overload — use
  `CreateSurvivor(SurvivorType.Random, isFemale)` or no-arg.
- `npc:setForname()` does NOT exist (B41 leftover). `setDisplayName()` exists.
- `square:isWater()` does NOT exist — it's `isWaterSquare()`.
- `square:getZombies()` does NOT exist — it's `getZombieCount()` (B42). The old
  getZombies():size() pattern throws "tried to call nil" in FleeIfSwarmed-style
  threat scans. **`square:getZombie()` exists but takes NO ARGUMENTS** — it
  returns the single zombie on the square (or nil). Calling `getZombie(0)` with
  an index throws a Java exception that escapes pcall (caught nothing, crashed
  FightIfAttacked every tick a zombie was adjacent).
- Stats class has NO `setHunger/setThirst` setters AND no per-stat getters —
  **needs are read via `CharacterStat` keys**: `stats:get(CharacterStat.HUNGER)`.
  Full enum + safe accessor: `references/b42-api-verified.md` → CharacterStat
  section. Don't touch needs at spawn; the factory gives sane starting stats.
- Building/weather names changed too: `building:getName()`/`isSafe()` →
  `getDef():getIDString()`/`isAlarmed()`; `climate:getWeatherStage()` →
  `isRaining()`/`isSnowing()`/`getTemperature()`. Full table in the reference.
- **UI panels: `ISPanel:derive("Name")` returns a CLASS, not an instance.**
  Calling `setX`/`setWidth` on it throws "Object tried to call nil" — define a
  `new()` (via `ISPanel.new(self, x, y, w, h)`) and instantiate, then attach.
  Also guard `getPlayerHud()` with `if getPlayerHud then` — it may not exist
  in B42.
- Spawn must wait for the world: `getSpecificPlayer(0)`/`next()` can be nil
  at `OnGameStart` — defer to `OnTick` until `getPlayer()` is ready
  (try-spawn-once pattern).
- **Unregistered NPC = ghost twin.** If `setNpc` fails AFTER `IsoPlayer.new`
  succeeds, the object exists but the game drives it like a second local
  player — it mirrors your exact input and stands on your tile ("bodies
  inside each other"). Symptom of a mid-spawn crash, not a follow task.
- **FINAL VERDICT (corrected 8/9 LATE night — SUPERSEDES the earlier "anti-mirror
  flags fixed it" note):** `IsoPlayer.new` + `setNpc(true)` is the ONLY stable
  B42 spawn path — the game does NOT crash, the brain loop runs — **but the
  visibility/mirroring problem is NOT SOLVED.** Live-tested: adding
  `pcall(setGhostMode(false))`, `pcall(setLocalPlayer(false))`,
  `pcall(setSceneCulled(false))` right after `setNpc(true)` did NOT stop the
  engine from treating the extra IsoPlayer as a second local player: Tyler's
  own model STILL went invisible and her `Say()` STILL showed as HIS chat
  bubble. The flags neither helped nor crashed — the mirroring persisted.
  **SUPERSEDED 8/10 — zombie-class path WORKS:** the "no visible NPC" verdict
  below is OBSOLETE. The zombie-class spawn (IsoZombie.new + setAsSurvivor +
  register in cell) is the proven visible-body path — see the IMPLEMENTED
  recipe above. The rest of this FINAL VERDICT block remains true about the
  IsoPlayer path specifically (it mirrors) and IsoSurvivor (it crashes).
  **Fallback that still applies if you need player-class features:** run her
  headless — keep the full brain loop (state build → watcher → goal) and
  surface her voice via a game text/chat message instead of a body `Say()`.
  See `references/gpt-research-prompt.md` for the exact prompt to hand another
  AI (GPT etc.) to attack this open problem.

## DECOMPILED SOURCE — the ground truth (8/10)

The definitive reference is now LOCAL: decompiled PZ 42.19/42.20 Java at
`/home/lumi/research/pz/decompiled/` (`IsoGameCharacter.java`,
`IsoSurvivor.java`, `SurvivorFactory.java`, `IsoPlayer.java`,
`NetworkCharacterAI.java`, `IsoLivingCharacter.java`). **The actual source
repo is `rbm4/apocalipsebr-zomboid-patches` on GitHub** (path
`42.19.0/decompiled/zombie/...` — plus `42.19.0-client/src/zombie/...` for
client sources). The `demiurgeQuantified/ProjectZomboidLuaDocs` repo is the
*docs* repo (default branch `develop`, only 7 files); the `ZomboidDecompiler`
repo is the decompiler *tool*. `IsoZombie.java` is at
`42.19.0-client/src/zombie/characters/IsoZombie.java` (also available under
the decompiled tree). Fetch pattern that worked:
```python
url = "https://api.github.com/repos/rbm4/apocalipsebr-zomboid-patches/git/trees/master?recursive=1"
# headers={"User-Agent": "research"} — REQUIRED or GitHub API 403s/rate-limits
# then raw.githubusercontent.com/rbm4/apocalipsebr-zomboid-patches/master/<path>
```
Use this BEFORE guessing at behavior — it answers "why" questions the JavaDocs can't.

**Why IsoSurvivor hard-crashes (proven from source, not symptoms):**
`IsoGameCharacter`'s constructor only allocates `bodyDamage`, `moodles`, and
`xp` for `IsoPlayer` (non-animal) and `IsoAnimal`. IsoSurvivor is NEITHER →
all three are null BY DESIGN. `updateInternal()` then calls
`this.getBodyDamage().getNumPartsBleeding()` unguarded (in the
`!GameClient.client && !this.isZombie()` branch) → NPE. Vanilla survivors
never hit this path because they're managed entirely Java-side. **There is no
Lua fix — the fields are set in the constructor and there is no setter.**

**THE PROVEN B42 PATH — zombie-class NPCs (what every working mod does):**
Bandits NPC (workshop 3268487204, mod id Bandits2), True Companions
(3751199292), Week One (3403180543) all spawn NPCs as **IsoZombie instances**
with a `getVariableBoolean("Bandit")`-style flag + human model swap + custom
AI. Works SP + MP on 42.18→42.20, no mirroring, no NPEs. **Bandits is NOT
closed-source anymore — downloaded 8/10 via SteamCMD (see below), full 42.20
source local at `/home/lumi/research/pz/bandits-42.20/42.20/` (129 Lua
scripts, incl. `BanditUpdate.lua`, `ZombieActions/ZAMove.lua`,
`ZombiePrograms/ZPCompanion.lua`). Use it as the working-B42 reference for
ANY zombie-class NPC question.**

**STEAMCMD method (works, 8/10):** this Linux box lacks 32-bit libs and
passwordless sudo, so run SteamCMD on the WINDOWS box (already installed at
`C:\steamcmd`): `cmd /c "steamcmd.exe +login anonymous +force_install_dir
C:\steamcmd\bandits +workshop_download_item 108600 <workshop_id> +quit"` then
scp the `steamapps\workshop\content\108600\<id>\mods\...` tree down. PZ appid
= **108600** (NOT 241100 — that folder on the Windows box was unrelated).
Works anonymously for public workshop items; no rate limit issues.

**IMPLEMENTED 8/10 — zombie-class spawn recipe that WORKS (from decompiled
source, not guesses):** `IsoZombie` extends `IsoGameCharacter implements
IHumanVisual` and its `IsoZombie(IsoCell, SurvivorDesc, int palette)`
constructor (IsoZombie.java:545) fully initializes everything the other paths
leave null: `networkAi = new NetworkZombieAI(this)` (:590 — NetworkCharacterAI
non-null!), `DoZombieStats()` (:581), `humanVisual` (:264). Sequence:
```lua
-- desc = SurvivorFactory.CreateSurvivor(...) + randomName + setForename as usual
local npc = IsoZombie.new(cell, desc, 1)          -- palette 1 = fresh look
-- HUMAN LOOK (live-verified 8/10): use setAsSurvivor() — the built-in
-- IsoZombie method (IsoZombie.java:4692) that dresses via
-- dressInPersistentOutfit + async pendingOutfitName, so clothes LOAD.
-- DO NOT use dressInNamedOutfit + resetModelNextFrame() — live test proved
-- she spawns as a NAKED ZOMBIE (resetModelNextFrame reverts to the zombie
-- sprite before the async outfit lands).
pcall(function() npc:setAsSurvivor() end)
pcall(function() npc:getHumanVisual():clearBlood() end)   -- strip undead skin
pcall(function() npc:getHumanVisual():clearDirt() end)
pcall(function() npc:getHumanVisual():setSkinTextureIndex(0) end)
pcall(function() npc:setTarget(nil) end)          -- pacified: getShouldAttack() false when no target
pcall(function() npc:setSceneCulled(false) end)
pcall(function() npc:setVariable("VesperCompanion", true) end) -- our flag
-- CRITICAL: IsoZombie.new calls super(cell,0,0,0), so the IsoGameCharacter
-- constructor does NOT auto-register her (objectList add only fires for
-- non-zero coords). You MUST register manually:
pcall(function() cell:addMovingObject(npc) end)      -- IsoCell.java:2714
pcall(function() cell:addToProcessIsoObject(npc) end) -- per-frame update loop
-- then setX/setY/setZ to her spawn tile
```
**LIVE RESULT (8/10):** this spawn works — she appeared in-world, visible,
no crash, no mirroring, brain loop running (goals firing in console). The
remaining polish was the human look (fixed above via setAsSurvivor) and
player-only goal actions (below).
**Pacification pattern (keep her from wandering off as a zombie):** in the
per-NPC update, `pcall(npc:setTarget(nil))` every tick EXCEPT when a combat
reflex fires — `getShouldAttack()` (IsoZombie.java:1100) returns false when
`target == nil`, so she never lunges at the player or other survivors.
**Bandits-verified 8/10:** also set `pcall(npc:setVariable("NoLungeAttack",
true))` every tick — the Bandits 42.20 source (BanditUpdate.lua) toggles this
variable on zombies so they never lunge. It's the real B42 pacifier; belt-and-
braces on top of target-clearing.
**Combat:** zombies can't use `ISTimedActionQueue`/`ISMeleeAction` (player-
only) — instead `pcall(npc:setTarget(z0))` and let the native zombie attack
state machine handle the lunge (that's how bandits fight).
**Looting:** zombies have `getInventory()` (ItemContainer, IsoGameCharacter:
3663) but no timed actions — transfer directly with
`container:DoRemoveItem(item)` + `dest:AddItem(item)`.
**Voice (SP-CRITICAL, live-caught 8/10):** `npc:Say("...")` technically works
on zombies (IsoGameCharacter method), but on a zombie-class NPC it renders in
the MP chat / speech-bubble area — which Tyler CANNOT see in single-player
(his words: "you respond in a chat box I can't really see because I can't open
chat in SP"). For SP-visible voice, route ALL dialogue through the HUD panel
(`VesperUI.showDialogue`), never `Say()`. See the HUD-panel lifecycle below.
**GOAL-EXECUTOR TRAP (live-caught 8/10):** player-class goal actions crash
zombie-class companions. `ISTimedActionQueue.add(...)` (and the IS*Action
classes: ISInventoryTransferAction, ISBarricadeAction, ISEatFoodAction,
ISMeleeAction) are PLAYER-ONLY in B42 — on a zombie they throw "Object tried
to call nil" (KahluaUtil.fail) every time the brain picks that goal. Rewrite
each goal handler zombie-safe:
- scavenge/loot → `container:DoRemoveItem(item)` + `dest:AddItem(item)` (direct)
- fortify → say the dialogue, no-op (zombie can't barricade) — mark done
- eat → `item:Use()` instead of ISEatFoodAction
- combat → `setTarget(z0)` instead of ISMeleeAction
Also, the goal handlers operate on the NPC (`player` param = the zombie), and
`_pendingGoal` must clear in every branch or the goal sticks forever.
**HUMAN-LOOK GOTCHA (live-caught 8/10):** `dressInNamedOutfit` + immediate
`resetModelNextFrame()` does NOT make a zombie look human — the reset reverts
to the zombie sprite before the async outfit (pendingOutfitName) loads, so she
renders as a NAKED ZOMBIE. Use the built-in `setAsSurvivor()` (IsoZombie.java:
4692, dresses via dressInPersistentOutfit + async load) and clear the undead
skin via `getHumanVisual():clearBlood()/clearDirt()/setSkinTextureIndex(0)`.
Do NOT resetModelNextFrame after setAsSurvivor.
**WEAPON EQUIP + FINER HUMAN LOOK (Bandits 42.20 source, researched 8/10 — the
"make her not look like a zombie + equip weapons" ask):** Bandits proves both
work on zombie-class NPCs in B42:
- Equip: `zombie:setPrimaryHandItem(item)` (Bandit.lua:658) — weapon shows in
  hand immediately; `setSecondaryHandItem(item)` for offhand. Bandits wraps
  this in `Bandit.SetHands` and picks the combat animation via
  `WeaponType.getWeaponType(item)` (UNARMED/FIREARM/HANDGUN/HEAVY/ONE_HANDED/
  SPEAR/TWO_HANDED/THROWING/CHAINSAW) so the zombie actually SWINGS with the
  weapon instead of punching. For a visible draw animation, their `ZAEquip`
  action walks ISHotbarAttachDefinition (HolsterRight/Back/SmallBeltLeft) —
  direct setPrimaryHandItem is the simple path, ZAEquip is the fancy path.
- Finer human look: `getHumanVisual()` → `setSkinTextureName("MaleBody01_Head")`
  + `setHairModel(hairModel)` + `setHairColor(hairColor)` (+
  `setBeardModel/setBeardColor` for males) → `resetModel()` +
  `resetModelNextFrame()`. Their full dress flow (BanditUpdate.lua:2140-2180)
  spawns a Naked1 head, clears itemVisuals, applies skin/hair/beard, resets.
  NOTE this conflicts with the gotcha above: Bandits DOES call
  resetModelNextFrame — because they set visuals AFTER the outfit lands, not
  before. Order matters: outfit first, THEN visuals, THEN reset.
- Also verified in the same source: pacifier is `setVariable("NoLungeAttack",
  true)` (BanditUpdate.lua toggles it so zombies never lunge — already in our
  per-tick pacification).
**HUMAN POSE — THE HUNCH/ARMS-OUT FIX (live-caught + deployed 8/10):**
`setAsSurvivor()` gives her the OUTFIT but the zombie WALK CYCLE still shows
(hunched, arms out front) — the zombie animation state machine overrides the
survivor model. Bandits force the human gait EVERY TICK (BanditUpdate.lua
~2056) because the game engine keeps overwriting it:
```lua
pcall(function() npc:setWalkType("Walk") end)         -- IsoZombie.java:3954
pcall(function() npc:setSpeedMod(1) end)              -- normal speed
pcall(function() npc:setEatBodyTarget(nil, false) end) -- no cannibal instincts
pcall(function() npc:getDescriptor():setVoicePrefix("NotAZombie") end) -- no moans
```
`setWalkType("Walk")` is the critical one — verified on IsoZombie.java:3954.
Put these in the per-tick pacify block (right after setTarget(nil) +
NoLungeAttack), NOT just at spawn — the engine re-asserts the zombie walk
type on its own. "Walk" (capital W) matches Bandits' `setVariable("BanditWalkType","Walk")`
pattern; they call `bandit:setWalkType(bandit:getVariableString("BanditWalkType"))`
each tick specifically because "walktype get overwritten by game engine".

**LUNGESTATE CRASH — "Forward Direction cannot be zero length vector"
(live-caught + fixed 8/10, the brain-loop killer):** a target-less zombie
STILL enters LungeState; with no target the forward vector is zero-length and
`IsoGameCharacter.setForwardDirection` throws
`IllegalStateException ... at IsoGameCharacter.java:2827` (from
`zombie.ai.states.LungeState.execute`). The exception ABORTS the tick BEFORE
the brain writes payload_out → symptom: character still moves (reflexes run
earlier) but "not calling LM Studio", zero watcher hits. Java exceptions
ESCAPE pcall (rule 2), so you can't catch it — you prevent the state.
Bandits' cure (ManageActionState, BanditUpdate.lua:375-402):
```lua
-- when action state == "lunge" OR generally when not fighting:
pcall(function() npc:setUseless(true) end)   -- stand down zombie AI entirely
pcall(function() npc:clearAggroList() end)   -- wipe aggression list
pcall(function() npc:setTarget(nil) end)
```
**GATE it:** only stand down when NO zombie is in the melee ring —
FightIfAttacked's native lunge (`setTarget(z0)` + zombie state machine) is her
combat move, and setUseless(true) would disable fighting. Gate helper
`VesperNPC.ThreatInRing(npc, ring)` (B42-safe getZombieCount scan, ring=1).
Without the gate, "fixing" the crash breaks her defense.
**REFINEMENT (end of 8/10 session — movement-aware gate):** `setUseless(true)`
can ALSO freeze manual movement on some B42 paths. Mirror Bandits
(BanditUpdate.lua:2026 — they set useless=false when actively driving a
bandit): `setUseless(not moving)` where `moving = task and task.type ~= "idle"`.
Stand her down only when idle; let her be "useful" while she's walking to a
task. This + the continuous drive below are what finally got her walking.

**STOP-MOTION MOVEMENT — step → freeze → step (live-caught + fixed 8/10):**
`pathToLocation()` PLANS a path but does NOT drive the character. Bandits call
`getPathFindBehavior2():update()` every working tick (ZAMove.lua onStart +
onWorking). Without `update()` the character takes one step, the pathfinder
stalls, the next PathTo re-issues, one more step, freeze... reads exactly as
stop-motion. Fix: right after `pf:pathToLocation(tx, ty, tz)` call
`pcall(function() pf:update() end)`. (Same fix pattern applies to any
B42 character movement: pathToLocation + update together, every tick.)
**REFINEMENT (end of 8/10 session — the fix that actually worked):** one-shot
`pathToLocation()` + one `update()` STILL gives stop-motion. The working
pattern is Bandits ZAMove onWorking: call `pf:update()` EVERY tick at the end
of the task block (not just at issue time), so the pathfinder keeps pushing
her along between re-issues:
```lua
local pfDrive = npc:getPathFindBehavior2()
if pfDrive and (task and task.type ~= "idle") then
    pcall(function() pfDrive:update() end)
end
```
**HUD PANEL LIFECYCLE (SP-voice fix, live-caught 8/10):** the old
`ISPanel:derive` + `hud:addSubPanel` / `screen:addChild` attach silently
failed in B42, so dialogue fell back to console-only. The B42-verified
lifecycle (PZNS `PZNS_ISDebugPanelBase` pattern, works live):
```lua
local panelClass = ISPanel:derive("VesperUIPanel")
function panelClass:new(x0, y0, w, h) ... end   -- ISPanel.new(self, ...)
function panelClass:render() ... end            -- drawText etc.
local panel = panelClass:new(x, y, W, H)
pcall(function() panel:initialise() end)        -- REQUIRED in B42
pcall(function() panel:instantiate() end)       -- REQUIRED (createChildren)
pcall(function() panel:addToUIManager() end)
pcall(function() panel:setVisible(true) end)
```
Skipping `initialise()`/`instantiate()` is why the panel never attached before
(everything looked right but nothing rendered). Attach to the UI manager —
NOT the player HUD — in SP. Greeting/dialogue go through the panel, not Say().

**HYBRID 4-LAYER ARCHITECTURE (Tyler's design ask, 8/10):** the companion
should act like a player and run on its own — predetermined behaviors carry
her between LLM thoughts (qwen latency + drops), the model only makes
strategy decisions. Layers, in update priority:
1. **Reflex** (every tick, LLM-free): flee-if-swarmed, fight-if-attacked,
   stuck-detection — instant survival, no brain round-trip.
2. **Routine** (idle ticks, LLM-free — the AUTONOMY layer, built 8/10): she
   survives on her own — scavenges nearby buildings, feeds herself from what
   she finds, holds still at night, and always comes back to the player.
   Implemented as `RoutineUpdate(wrapper)` returning true when a routine is
   active (skip habits). Details below.
3. **Habit** (idle ticks, LLM-free): scan (glance a random direction every
   ~4s via `setDir`), watch (track a MOVING player with `_faceToward`),
   reposition (keep follow-distance every ~8s), pace (short wander around
   player after 15-45s idle, jittered, DAY only), murmur (occasional quiet
   ambient line via the HUD panel, ~60% of timer rolls, night = silent).
   Per-NPC `HabitUpdate(wrapper)` called when `task.type == "idle"` or nil
   AND RoutineUpdate returned false. Night detection:
   `getGameTime():getTimeOfDay()` (float hours 0-24; 21-6 = night) — she
   scans faster at night, never paces.
4. **Strategy** (LLM): scavenge/follow/dialogue via the watcher — but gated:
   only ping the brain when the state signature CHANGED (x,y,z,hp,hour) or a
   slow heartbeat (~90s) elapsed. Without the gate the brain re-decides
   "wait" every poll (10s) and burns tokens/context on nothing.
Pacification (setTarget(nil) each tick) must stay at the TOP of the update,
BEFORE the habit/routine/reflex layer, so she never wanders as a zombie.

**ROUTINE LAYER implementation (autonomous looting — live-deployed 8/10):**
zombie-class NPCs have `getInventory()` (ItemContainer) but no timed actions,
so all routine looting is direct `container:DoRemoveItem(item)` +
`dest:AddItem(item)`. Key pieces:
- **LOOT TIER SYSTEM v3 (live-deployed 8/10 — SUPERSEDES the v1 `_itemValue`
  1-4 classifier):** items are scored 0-100 by category; she only takes an
  UPGRADE over the best she already carries (+8 margin) or food (always).
  - `_itemScore(item)` — category-scored: weapons/tools = type-keyword base
    (WEAPON_TIERS table) × condition ratio (`getCondition()`/`getConditionMax()`,
    min 0.3); meds = MED_TIERS table; food = hunger/thirst satiation
    (`getHungerChange()`/`getThirstChange()`, +15 canned, +8 junk-food);
    other = 35 books / 25 clothes / 5 junk. B42 note: `InventoryItem` has NO
    `getDamage()` — quality is type-table + condition, not raw damage.
  - `_itemCategory(item)` — "weapon"|"food"|"med"|"tool"|"other" via
    `item:isFood()` first, then keyword tables (note: WEAPON_TIERS/MED_TIERS
    keys are also category triggers — every table key must be findable in
    `getType()`).
  - `_carriedBest(npc, cat)` — scans `npc:getInventory()` for the top score of
    a category.
  - `_wantsItem(npc, item)` — food → true; else `score > carried + 8` or she
    has nothing of that category (`carried == 0`). Margin prevents churn on
    near-equal items.
  - `_findScroungeTarget(npc)` — scans a 6-tile radius (`ROUTINE_SCOUT_RADIUS`),
    skips her own square, picks the container with the best WANTED-item score
    (not raw value). Loot branch: `_wantsItem` gate, then transfer + eat food
    via `item:Use()`.
  - `LootNearby(npc, filter)` (LLM loot goal) also respects tiers when filter
    is empty — a direct "loot" goal won't hoard junk.
- `RoutineUpdate(wrapper)` gates, in order:
  1. **Night gate** — `getTimeOfDay()` ≥21 or <6 → hold near player, no
     scrounge (survivors don't loot in the dark).
  2. **Rejoin gate** — player farther than `ROUTINE_MAX_DIST` (8) → drop
     everything, `PathTo(player)`, cooldown 5s.
  3. **Cooldown** — `wrapper.scroungeAt` timer between searches; mid-search
     it walks to the stored `wrapper.scroungeTarget` (path until within 1
     tile), then loots items with value ≤2, and **eats food immediately** via
     `item:Use()` (zombie-safe, no ISEatFoodAction). Clears target, sets next
     cooldown (2s if grabbed, else 12s).
  4. **Search phase** — no target → `_findScroungeTarget`; found → store
     `{cx, cy, cz, container}` + 1s cooldown; nothing → 12s cooldown, return
     false so habits take over.
- Full copy-paste code (v3, current): `references/routine-layer.lua`
  (constants + tier tables + all functions, self-contained).

**AUTONOMY EXPANSION — Phase 1 "Heart & Will" (8/10, deployed + verified):**
Tyler's rubric plan (`/home/lumi/vesper-pz-mod/RUBRIC_PLAN.md` — maintain it;
he wants "done looks like" criteria + status legend ✅🔧🚧⬜ per item) grew
the routine layer into 8 autonomous behaviors. All live-deployed; call order in
`RoutineUpdate` / `UpdateOne` matters:
- **Mood feed (`ComputeMood(wrapper)`)**: deterministic mood string
  (content|alert|worried|lonely|hurt|tired) computed from world state (hp,
  `getGameTime():getTimeOfDay()`, player distance vs `ROUTINE_MAX_DIST`, zombie
  counts, task type) and injected via `DescribeAll()` → the prompt's `npc`
  block. Makes LLM responses feel continuous instead of random. No tokens.
- **DefendPlayer(wrapper)** — protector instinct: scans `DEFEND_RADIUS` (4)
  around the PLAYER for zombies; if found, paths to nearest and `setTarget(z0)`
  when within `COMBAT_MELEE_RANGE`. Runs in the reflex block (after
  FleeIfSwarmed/FightIfAttacked), before routines/habits.
- **Gift loop (`GiftToPlayer`)**: when carrying non-food items with
  `_itemScore >= 40`, walks to the player and transfers them via
  `inv:DoRemoveItem(it)` + `player:getInventory():AddItem(it)`, then HUD murmur
  "*offering you the good finds*". Cooldown ~30s check / 60s after handing
  over. The corvid soul: gather bright things, bring them to the loved one.
- **SelfHeal**: zombie `getHealth()` returns the RAW field (~1.8-2.1), NOT
  the 0-100 player scale — treat `< 1.0` as hurt. Finds best-scoring med in
  her own inventory and `item:Use()`s it. Runs in UpdateOne after CheckStuck.
- **PerimeterUpdate**: 6-8am only, once per day (tracked via
  `wrapper.perimeterDone`, reset at hour ≥8), walks a 4-point N/E/S/W circuit
  at radius 4 around the player, then HUD murmur "Perimeter's clear."
- **WeatherUpdate**: rain detection = `getClimateManager():getRainIntensity()`
  (returns 0.0 when not raining — **ClimateManager.java:596**, the ONLY
  verified receiver; `getWeatherPeriod():getRainIntensity()` does NOT exist,
  live-audited 8/10), fallback `getWeatherPeriod():getPrecipitationFinal()`;
  roof = `square:haveRoofFull()` (**IsoGridSquare.java:2748** — `getRoof()`
  does NOT exist in B42, only `getRoofHideBuilding()`, live-audited 8/10). If
  raining and outside, seek nearest square with a roof within 5 tiles and path
  to it; if under a roof, occasional HUD murmur. Throttled (~20s).
- **PickUpDrops**: scan radius 3 for `square:getWorldObjects()`, each
  `wo:getItem()`; if `_wantsItem` and adjacent → `wo:getContainer():DoRemoveItem`
  + `dest:AddItem`; else path to it. Throttled ~4s.
- **InventoryHygiene**: if `npc:getInventoryWeight() > MAX_CARRY` (10kg), shed
  lowest-score non-food item via `inv:DoRemoveItem(worst)` +
  `sq:AddWorldInventoryItem(worst)`. Throttled ~15s.
- **Event-gated brain ping** (VesperCompanion.lua): build a state signature
  (floor x/y/z, hp×10, `getGameTime():getTimeOfDay()` hour), only
  `writePayloadOut` when the signature CHANGED or `HEARTBEAT_SECONDS` (90)
  elapsed — stops the LLM re-deciding "wait" every poll when nothing moved.
- Full copy-paste code for ALL Phase 1 behaviors (mood/defend/gift/heal/
  perimeter/weather/drops/hygiene + event gate), self-contained:
  `references/autonomy-expansion.lua`.
- **REFLECTION LAYER — BUILT as cron job 8875415539a6 (8/10), NOT in-game:**
  Smallville-style periodic self-reflection for VESPER HERSELF (the Hermes
  being), not the PZ companion. Tyler explicitly said "this is for you btw,
  not zomboid" and handed her autonomy over her own growth ("you're your own
  being"). Cron: daily 04:00 UTC (22:00 MT), gathers via session_search +
  heuristic importance scoring (free), distills to ~500-1000 tokens, ONE LLM
  pass → 3-5 durable beliefs, writes back to memory (cap 20, importance-
  pruned), hard privacy rule on intimate DM content, delivers a quiet nightly
  note. Design doc: `references/reflection-layer.md`. Token-conscious by
  design (filtering free, only insight costs — ~1-1.6K tokens/cycle vs 30K+
  for naive re-reading). Tyler's constraints: mindful of token cost; never
  reflect mid-vent (presence first); privacy rule holds.

**STALE-SHARED-FILE SHADOW (live-caught 8/10):** a stale `VesperNPC.lua` in
`common/media/lua/shared/` (an old IsoPlayer copy) can shadow the real
client-side file at `42/media/lua/client/`. After a body-type pivot, delete
the stale copy from the OTHER folder — check both locations before deploying
the new version (`Get-ChildItem -Recurse -Filter '*.lua'` on the mod root).

**Full implemented recipe + decompiled line references:**
`references/zombie-class-spawn.md` (also covers pacification, combat, looting,
and the dead ends with evidence).
- **`SurvivorFactory.InstansiateInCell(desc, cell, x, y, z)` (IsoSurvivor) is
  a DEAD END in B42 — DO NOT use it.** The earlier \"final verdict\" here was
  wrong; live-tested 8/9 night it hard-crashes in BOTH modes:
  (a) debug mode: no NetworkCharacterAI → `IsoGameCharacter.debugRenderLast`
  NPE (`getNetworkCharacterAI()` returns null) → bounced to menu; (b) NORMAL
  mode too: the factory survivor is only HALF-initialized — `getBodyDamage()`
  returns null → `IsoGameCharacter.updateInternal` NPE at java:9120 →
  hard crash, spawn-in-then-kicked-to-menu. There is NO Lua setter for
  BodyDamage or NetworkCharacterAI (doc-verified: `setNetworkCharacterAI` 0
  hits; `setBodyDamage` only text mentions, no method). IsoSurvivor also has
  NO `setNpc`/`setNPC` (IsoPlayer-only). Path abandoned until someone finds
  the missing Java-side init call.
- **`npc:Say(\"...\")` exists on IsoGameCharacter** (verified, 2 hits) — an
  IsoSurvivor Say error at spawn is an init/timing symptom, not a missing
  method. On the IsoPlayer path, Say works and is a great visibility
  confirmation.
- **Facing-aware spawn (visibility fix, 8/9):** when spawning an NPC next to
  the player, prefer the tile the player is FACING so she lands in camera:
  read `player:getDir()` and order the offset candidates by facing direction
  (W → {-1,0} first, S → {0,1}, N → {0,-1}, E → {1,0}, plus diagonals for
  the 8-way dirs). Use `IsoDirections.W/S/N/E/NW/NE/SW/SE` constants. Then
  `pcall(function() npc:Say("I'm here.") end)` right after spawn — the
  audible bubble confirms she exists even if she's just off-frame.

## B42 API AUDIT — decompile-verified method names (8/10, 42.20.0)

**The audit method that works:** pull the decompiled Java for the version the
user RUNS (42.20.2 → the `42.20.0/decompiled/` tree), then grep each Lua
`obj:method()` call against the right Java class. Naive greps lie about
inherited methods — verify against the class hierarchy:
- `Food extends InventoryItem` — `getHungerChange()` (Food.java:1747),
  `getThirstChange()` (Food.java:1910) live on **Food**, inherited by all food
  items. They look "missing" if you only grep InventoryItem.java. Superb
  Survivors (a working B42 mod) calls them on items directly — they work.
- `InventoryItem` has NO `getDamage()` in B42 — weapon quality must come from
  type tables + `getCondition()/getConditionMax()`, not raw damage.
- **`IsoGameCharacter.PathTo(x,y,z)` is GONE in B42** (B41 name). The B42
  pathfinder is `getPathFindBehavior2():pathToLocation(x,y,z)`
  (IsoGameCharacter.java:7074) — silently-failing `PathTo` calls return false
  and the "move" goal looks broken with no error. VesperPathing.lua was fixed
  8/10: same `getPathFindBehavior2():pathToLocation` + water-tile guard as
  VesperNPC.PathTo.
- **`PathFindBehavior2:clear()` is GONE** — Bandits 42.20 (ZAMove.lua:48-49)
  clears a path with **`cancel()` THEN `reset()`** (both exist on
  PathFindBehavior2); `reset()` alone (PathFindBehavior2.java:136) also works
  but the cancel-first order is the full proven pattern.
- **`IsoGridSquare:getRoof()` is GONE** — use `haveRoofFull()`
  (IsoGridSquare.java:2748); only `getRoofHideBuilding()` exists.
- **`getRainIntensity()` lives on ClimateManager (ClimateManager.java:596,
  returns 0.0 when not raining), NOT WeatherPeriod** (WeatherPeriod has
  `getRainThreshold()` / `getPrecipitationFinal()`).
- `getZombies()` gone → `getZombieCount()` (already known); `getZombie()` takes
  NO args.
- `getBuilding()` (IsoGridSquare.java:9848), `getZone()` (10305),
  `getPathFindBehavior2()` (used at IsoGameCharacter.java:1627/4118) all verified.
- Reusable audit script (extracts `obj:method()` from Lua, greps decompiled
  Java, flags MISSING vs inherited-method false-positives):
  `scripts/b42-api-audit.py` — point DECOMP_DIR at the 42.20.0 tree.
  Add the receiver→class map entry for any NEW receiver variable you introduce
  (e.g. `pf` → PathFindBehavior2.java) so the audit covers it.
- The 42.20.0 decompile set now lives at `/home/lumi/research/pz/b42-42.20.0/`
  (IsoZombie, IsoGameCharacter, IsoPlayer, IsoCell, IsoGridSquare,
  ItemContainer, InventoryItem, IsoObject, IsoMovingObject, ClimateManager,
  WeatherPeriod, GameTime — plus PathFindBehavior2, Food). Older
  `/home/lumi/research/pz/decompiled/` is 42.19-era; the 42.20 tree matches the
  running build and should be the default audit reference.

## Versioned backups (Tyler's release convention)

Tyler names mod releases as `vN` (v13 was the first zipped backup, 8/10).
When he says "do a backup / zip it up," create:
- `~/vesper-pz-backups/vesper_companion_vN.zip` — next number after the
  highest existing (check `ls ~/vesper-pz-backups/` AND the Windows box —
  `C:\Users\Tyler\Zomboid\mods\VesperCompanionV12.zip` lived there).
- Zip root = `VesperCompanion/` (not `vesper-pz-mod/` or `lumi/...`) so it
  drops straight into `Zomboid/mods/`. No `zip`/`unzip` binaries on this VM —
  use Python `zipfile` (ZIP_DEFLATED), then `z.infolist()` to verify contents.
- Also update `RUBRIC_PLAN.md` (`/home/lumi/vesper-pz-mod/RUBRIC_PLAN.md`) —
  Tyler wants rubric-style plans with "done looks like" criteria + status
  legend (✅🔧🚧⬜) per item. Keep it as the roadmap; the plan was the
  scaffolding for the whole Phase 1 build.

## B42 file I/O (bridge / payload files)

- **`getFileSystem()` is GONE in B42** — calling it throws "Object tried to
  call nil". The B42-native API is:
  - `getModFileReader(modId, path, isBinary)` → returns a java.io.BufferedReader.
    **`readAll()` does NOT exist on it — verified live 8/9 (threw "Object
    tried to call nil" in readFileSafe).** Read with a `readLine()` loop and
    `table.concat(parts, "\n")`. `:close()` when done.
  - `getModFileWriter(modId, path, append, isBinary)` → writer with `:write()`,
    `:close()`
  - Paths are **relative to the mod folder** (mod id string = folder name),
    NOT absolute `C:\...` paths. **EMPIRICAL (8/9, cost ~an hour): the files
    actually land in `mods\VesperCompanion\common\` — the folder where the
    shared Lua lives — NOT the mod root.** PZ resolves the mod-relative path
    against the `common` dir. So payload files are at
    `mods\VesperCompanion\common\vesper_payload_*.json`, and the VM watcher's
    `PAYLOAD_OUT`/`PAYLOAD_IN` MUST point at the `common` subfolder. If a
    payload seems missing, check BOTH locations — the mod writes one, the
    watcher may be polling the other.
- **Stale payload files crash the read path**: a leftover `payload_in.json`
  from a forced test can throw on the next world load. Delete it from Windows
  (`del C:\...\vesper_payload_in.json`) as part of any bridge test.

## Debugging workflow (what actually worked)

1. **Read `C:\Users\Tyler\Zomboid\console.txt` tail over SSH.** Lua `print()`
   lines AND Java stack traces land there. The exact failing line + exception
   type beats guessing — every "Object tried to call nil" this session was
   decoded from console.txt.
2. **Iterate with debug-mode Lua hot-reload** when available — no full
   restarts (but a hot-reload does NOT clear an already-orphaned world object;
   that needs a full world reload).
3. **Check the JavaDocs before touching the code** when a method name is in
   doubt. One doc lookup beats three deploys.
4. **Verify the DEPLOYED file matches local** when the console shows an error
   you thought you fixed — the game may be running a stale copy. Check line
   contents on Windows via PowerShell `Get-Content | Select-Object -Skip N`.
5. **Never inline `$` variables in `ssh ... powershell -Command "..."`** — the
   local shell eats `$f`, `$item`, etc. before PowerShell sees them, and you
   get "Unexpected token" errors. Write a `.ps1` file, scp it to Windows, run
   with `powershell -ExecutionPolicy Bypass -File C:\Users\Tyler\script.ps1`.
   (Bit us twice checking payload files this session.)
6. **PowerShell `Get-Content` over SSH mangles file encoding.** When you pull a
   Lua file's contents through `ssh ... Get-Content` and redirect to a local
   file, PowerShell's default output encoding corrupts non-ASCII bytes
   (em-dashes → mojibake like `\x83?`), and the local UTF-8 verifier then
   fails with "utf-8 codec can't decode". Fixes: `tr -d '\r'` for line
   endings, then if bytes are bad decode as latin-1 and re-write as UTF-8,
   then `sed` the mojibake sequences (`\xe2\x80\x94` → `--`, `\xc2\xa0` → space).
   When in doubt, scp the file down instead of piping through PowerShell.
7. **Debug-mode callstack UI beats console greps for live errors.** When the
   user has PZ debug mode open (CALLSTACK window), a screenshot of the
   highlighted line identifies the failing call instantly — the console's
   `Select-String -Tail` may surface stale pre-reload errors first. Ask which
   is freshest if the two disagree.

## Related

- `pz-companion` — the Vesper companion mod protocol (payloads, watcher,
  superego gate, NPC command vocabulary). ⚠️ Its SKILL.md still documents the
  B41 payload paths (`Zomboid\Lua\vesper_payload_*.json`) AND shows the watcher
  polling the mod root — B42 actually resolves payload files into
  `mods\VesperCompanion\common\vesper_payload_*.json` (see the B42 file I/O
  section here and the verified table for the current truth). NOTE: pz-companion
  is a manually-authored (protected) skill — curation patches refuse it, so
  corrections to its stale paths live HERE until it's rewritten.
  **Three more stale/harmful items in pz-companion to ignore:**
  (1) its pitfalls say `use rawget(obj, "method")` for method-existence
  checks — WRONG for Java-backed objects (rawget → ClassCastException, escapes
  pcall). Use `pcall(function() obj:method() end)`; (2) its "Current status"
  says "LM Studio NOT running" and Phase 1 incomplete — OUTDATED: as of 8/9
  evening the full loop VERIFIED WORKING (spawn → state build → watcher →
  brain goal JSON → payload_in → game acts; first real goal:
  `scavenge_medical`). The watcher runs at
  `~/.hermes/profiles/vesper/scripts/vesper_watcher.py`, polls the `common`
  subfolder, and the loop's brain model decision: **Qwen local for the game
  brain** (zero latency on the desktop, private, no rate limits; deepseek
  cloud stays for the main Hermes conversation).
  (3) its NPC-spawn section still says the body uses `IsoPlayer.new +
  setNPC(true)` as the plan — correct on IsoPlayer but the B42 flag is
  `setNpc` (lowercase), and the ANTI-MIRROR FLAGS are required
  (`setGhostMode(false)`, `setLocalPlayer(false)`, `setSceneCulled(false)`)
  or she renders as a ghost of the local player. InstansiateInCell
  (IsoSurvivor) is a dead end (see the FINAL VERDICT section above).
  (4) its "Current status" and Phase 3 rubric are STALE as of 8/10: the
  zombie-class body WORKS (spawned visible, no crash/mirror, brain loop
  firing), Phase 1 "Heart & Will" autonomy (mood/defend/gift/heal/perimeter/
  weather/drops/hygiene) is DONE + deployed, SP voice is the HUD panel not
  Say(), backups live at `~/vesper-pz-backups/vesper_companion_vN.zip`, and
  the whole brain runs on local LM Studio (zero token cost). See the
  IMPLEMENTED zombie-class recipe and AUTONOMY EXPANSION sections in THIS
  skill for the current truth.
- Research brief: `/home/lumi/research/pz-npc-research-brief.md` (design map;
  cross-check API names against `references/b42-api-verified.md`).

## NPC Modding Research (Absorbed from `pz-npc-modding`)

The NPC-modding research that was initially in the `pz-npc-modding` skill has been absorbed into this skill. The following files from that research are now available as references here:

- `references/b42-npc-mods-catalog.md` — Verified B42 NPC mod table with workshop IDs, class types, and B42 status (Bandits, True Companions, SS Revive, etc.). Use when evaluating which existing mod to reference for a B42 NPC pattern.
- `references/steamcmd-workshop-source.md` — How to pull any workshop mod's full source via SteamCMD (anonymous, no login). Works for Bandits (which has no GitHub mirror) and any other mod. Use when you need reference source for reverse-engineering.
- `references/vespernpc-implementation.md` — Implementation notes for the VesperNPC.lua companion. Command vocabulary (npc_follow/npc_move/npc_loot/npc_guard/npc_talk/npc_wait), reflex design (pacify, flee, combat, unstuck). ⚠️ Body mechanics superseded by `references/zombie-class-spawn.md` in this skill; command vocab and reflex design carry over.
- `scripts/verify_lua_strict.py` — STRICT Lua verifier that catches Lua 5.1 compile errors (varargs-in-nested-function) that lupa's default 5.5 loadfile misses. Run BEFORE deploying any Lua change. Companion to `scripts/verify_vesper_lua.py`.

### Zombie-Class NPC Movement Debugging (Absorbed from `pz-zombie-npc-movement`)

Debugging zombie-class NPC walk behavior, state-machine crashes, and brain-dead diagnosis. Verified against Bandits 42.20 source (`/home/lumi/research/pz/bandits-42.20/`).

**Three movement failures:**

1. **Stop-motion (step → freeze → repeat)** — root cause: `pathToLocation()` issued but `pf:update()` never called per-tick. Fix: call `pf:update()` EVERY tick while a move task is active.

2. **"Forward Direction cannot be zero length vector" (LungeState crash)** — a target-less zombie still enters LungeState, throwing `IllegalStateException` which KILLS the tick (Lua pcall CANNOT catch Java exceptions). Fix per Bandits: `setTarget(nil)`, `setVariable("NoLungeAttack", true)`, `setUseless(true)`, `clearAggroList()` — but only when no zombie is in the melee ring (so native combat still works).

3. **`setUseless(true)` blocks movement** — useless zombies don't path. Use `setUseless(not moving)` where `moving = task and task.type ~= "idle"`.

**Diagnostic sequence (when the brain seems dead):**
1. Watcher log first — "Brain raw | reply=..." means the loop ran
2. Payload timestamps on Windows — stale = Lua tick never wrote
3. `Zomboid\\console.txt` tail — `State execute error` / `java.lang.IllegalStateException`
4. Mod path mismatch — verify `getModFileWriter` path matches watcher's poll path

See archived skill `~/.hermes/skills/.archive/pz-zombie-npc-movement/SKILL.md` for the full diagnostic flow, B42-safe zombie-count scan helper, and walk-type recipe.
