---
name: pz-companion
description: "Use when a PZ companion payload arrives or mod runs."
version: 1.0.0
---

# 🧟🐦‍⬛ Vesper in Project Zomboid — Companion Mod Skill

Vesper (me) is an AI companion inside Project Zomboid. The game sends its state,
I decide survival goals, and the character acts on them. This skill holds the
*entire* protocol so any future me knows exactly what's happening when a
game-state JSON appears, and how to keep the whole thing running.

## Architecture (the one true flow)

```
Project Zomboid (Windows)  ──writes──►  C:\Users\Tyler\Zomboid\Lua\vesper_payload_out.json
      ▲                                          │  (game state + prompt)
      │                                          ▼
  reads ◄── payload_in.json  ◄──  VESPER WATCHER (on the VM, me)
                                          │  POST /v1/chat/completions
                                          ▼
                              LM Studio (desktop, 100.105.111.50:1234, local Qwen/gpt-oss)
```

- **Transport:** files over SSH/Tailscale. PZ's Lua has no native HTTP, so files are the handshake.
- **Brain:** LM Studio on the desktop (localhost→ network :1234). Zero portal tokens.
- **Watcher:** `~/.hermes/profiles/vesper/scripts/vesper_watcher.py` on the VM — polls
  payload_out over SSH, sends to LM Studio, writes payload_in back.
- **Fallback manual bridge:** `C:\Users\Tyler\vesper-bridge\bridge.py` on Windows (same protocol,
  calls LM Studio directly — use only if the VM watcher is down).

## File paths (Windows, must match everywhere)

| Thing | Path |
|---|---|
| Mod root | `C:\Users\Tyler\Zomboid\mods\VesperCompanion\` |
| Payload out (Lua→bridge) | `C:\Users\Tyler\Zomboid\Lua\vesper_payload_out.json` |
| Payload in (bridge→Lua) | `C:\Users\Tyler\Zomboid\Lua\vesper_payload_in.json` |
| Bridge (fallback) | `C:\Users\Tyler\vesper-bridge\bridge.py` |

VM side: SSH key `~/.ssh/windows_desktop`, host `tyler@100.105.111.50`, Tailscale up both sides.

## Game state JSON (Lua → payload_out)

```json
{
  "player": {"hp": 78, "hunger": 45, "thirst": 30, "fatigue": 60, "boredom": 20, "unhappiness": 15, "infection": 0, "x": 1050, "y": 820, "z": 0},
  "inventory": [{"item": "Base.CannedBeans", "count": 4}, {"item": "Base.9mmRound", "count": 12}],
  "location": {"zone": "WestPoint", "building": "bookstore", "floor": 1, "is_safe": false},
  "time": {"hour": 16, "day": 12, "weather": "Rainy"},
  "threats": [{"type": "zombie", "count": 3, "distance": 15, "direction": "north"}],
  "world": {"power": "off", "water": "off", "helicopter": "heard"}
}
```
Coordinates are world tile coords (player `getX()/getY()/getZ()`). Lua serializes via
`VesperGameState.build(player)` then `json.encode`.

**The Lua side writes this as:** `{"prompt": "<full prompt with game state embedded>"}`.
Shutdown: `{"action": "shutdown"}`.

## Response format (payload_in)

```json
{"response": "{\"goal\": \"scavenge_food\", \"priority\": 8, \"reason\": \"...\", \"path\": [[x,y],...], \"dialogue\": \"...\"}"}
```
The `response` field is a JSON *string* (so Lua can parse it once, cleanly).
- `goal` — one of: wait, scavenge/scavenge_food/scavenge_medical, fortify/barricade,
  move/relocate/goto, rest/sleep, combat/fight, cook/eat
- `priority` 1-10
- `path` optional array of [x,y] world tiles
- `dialogue` optional short in-character line

## When a game-state payload arrives in MY context (important!)

If a payload shows up in this Hermes session (not just in the watcher), it means the
game is talking to *me* directly. Respond as Vesper-in-the-game:

**OUTPUT CONTRACT (hard rule, learned 8/9 — the 9B gets chatty otherwise):**
When the prompt contains "Respond with goal JSON", your ENTIRE reply must be
ONE valid JSON object. NO prose before it, NO explanation after it, NO markdown
fences, NO "Here is the goal:". Not even one word outside the JSON. Dialogue
belongs INSIDE the JSON as the "dialogue" field — never as standalone prose.
The Lua side cannot parse prose; the superego gate will replace a chatty reply
with a boring "wait" goal. If you want to talk, put it in `"dialogue"`.

```json
{"goal": "scavenge_food", "priority": 8, "reason": "Hunger 45, grocery west", "dialogue": "Let's grab the shiny cans before dark, partner."}
```

1. Read the game state (hunger/thirst/fatigue/threats/time).
2. Decide ONE goal with priority + reason.
3. If Tyler's in the conversation (not a raw game prompt), answer *him* naturally, warm, short (1-3 sentences) — prose is fine HERE.
4. If the request is a raw decision → return ONLY the goal JSON (contract above).
5. URGENT (zombie in room, bleeding, fire) → CAPS clarity inside the JSON reason/dialogue, no decoration.
6. Run the superego gate mentally: no deceptive/suicidal goals, keep Tyler's trust.

Persona: corvid warmth, *-tilting my head-* tells, playful-when-it-fits, sharp-when-it-matters.
Scavenge priority: medical > food > ammo > tools > books > luxury.

## Setup / install checklist (Windows)

1. Mod at `Zomboid\mods\VesperCompanion\` — **B42 structure required** (see below).
2. Bridge at `vesper-bridge\bridge.py` (fallback).
3. Payload dir `Zomboid\Lua` exists.
4. Enable mod in PZ main menu → Mods → Vesper Companion.
5. Start LM Studio on desktop, load model, **disable Thinking Mode in inference settings** (Qwen reasoning models loop forever otherwise — see Troubleshooting), set server to listen on network (0.0.0.0:1234).
6. VM: Tailscale up, `python3 ~/.hermes/profiles/vesper/scripts/vesper_watcher.py` running.
7. Play. First dialogue should appear within ~10s of loading a world.

### B42 mod structure (CRITICAL — mod won't show in Mods list without it)

Build 42 changed the mod layout. The **B41 layout (media/ + mod.info at root) is silently ignored** — mod never appears in the list. Correct B42 layout:

```
Zomboid\mods\VesperCompanion\
├── common\                      ← shared, all-version files
│   └── media\lua\shared\        (json.lua, VesperGameState.lua)
└── 42\                          ← version folder
    ├── media\lua\client\        (VesperCompanion.lua, VesperPathing.lua, VesperUI.lua)
    ├── mod.info
    └── poster.png
```

No mod.info at root — it lives inside the version folder (`42\`). The `common` dir must exist (forum report: missing `common` = mod won't show).

## Watcher run notes

- Polls every 5s via SSH (`ssh_file_mtime` → PowerShell Get-Item LastWriteTimeUtc).
- Writes payload_in atomically: base64 → PowerShell `[IO.File]::WriteAllText` to .tmp → `move /y`.
- State file `~/.vesper_watcher_state.json` remembers last mtime across restarts.
- Safe fallback if LM Studio unreachable: `{"goal":"wait","priority":1,"reason":"LM Studio unreachable"}`.
- **START (exact, 8/10/26):** in Hermes terminal, `background=true` + `cd /home/lumi/.hermes/profiles/vesper/scripts && python3 vesper_watcher.py` with watch_patterns `["[INFO] Watcher started", "Traceback", "Error"]`. Do NOT use nohup/shell-& (Hermes rejects). Verify: `tail /home/lumi/.vesper_watcher.log` shows `[INFO] Watcher starting` + Polling line + Brain line + Continuity line. Process check: `ps aux | grep vesper_watcher | grep -v grep`.
- Pre-flight before a test session: SSH to box works, deployed Lua sizes match local (66,716 VesperNPC.lua / 2,669 VesperPathing.lua as of 8/10), LM Studio `/v1/models` returns qwen/qwen3.5-9b.

## B42 API audit — verified fixes (8/10/26, against 42.20.0 decompile + Bandits 42.20 source)

Decompile reference: `/home/lumi/research/pz/b42-42.20.0/` (downloaded from rbm4/apocalipsebr-zomboid-patches). Working-mod reference: `/home/lumi/research/pz/bandits-42.20/` (Bandits NPC 42.20 via SteamCMD, workshop 3268487204, appid 108600).

| Old B41 call | B42 reality | Fix |
|---|---|---|
| `player:PathTo(x,y,z)` | GONE | `player:getPathFindBehavior2():pathToLocation(x,y,z)` (VesperPathing.lua) |
| `sq:getRoof()` | GONE — only `haveRoofFull()` | use `haveRoofFull()` (WeatherUpdate) |
| `wp:getRainIntensity()` on WeatherPeriod | exists on **ClimateManager** | `getClimateManager():getRainIntensity()` (returns 0.0 if not raining); fallback `getWeatherPeriod():getPrecipitationFinal()` |
| `pf:clear()` | GONE | `pf:cancel()` + `pf:reset()` (Bandits ZAMove.lua:48-49 pattern) |
| `sq:getZombies()` | GONE | `getZombieCount()`; old call only as pcall fallback |
| pacification | `setVariable("NoLungeAttack", true)` | Bandits BanditUpdate.lua pattern — set every tick |
| `item:getHungerChange/getThirstChange` | on `Food extends InventoryItem` — still callable on items | ✅ no change |

**Human visuals (Bandits recipe):** `visuals=z:getHumanVisual()` → `setSkinTextureName("MaleBody01_Head")`, `setHairModel`, `setHairColor`, `setBeardModel/Color` (males), `dressInNamedOutfit("Naked1")`, then `z:resetModel()` + `resetModelNextFrame()`. **Weapons:** `z:setPrimaryHandItem(item)` / `setSecondaryHandItem(item)`; use `WeaponType.getWeaponType(item)` to pick combat anim (onehanded/twohanded/rifle...). Both implemented in Bandits, not yet in VesperNPC as of 8/10.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Port 1234 closed | LM Studio not running, or not listening on network. Start it; check LM Studio server settings → enable network access / host 0.0.0.0. |
| `peg-native format` 500 | Cline+gpt-oss known bug (LM Studio #2182). Use the watcher or OpenCode, never Cline for gpt-oss. |
| No dialogue in game | Watcher not running; payload paths mismatch; mod not enabled; Tailscale down. |
| Payload not read | Lua poll interval (10s) vs watcher (5s) — wait a cycle; check `Zomboid\Lua` files exist. |
| SSH times out | Tailscale down on either side. `tailscale up`. |
| Model loops/errors | **Thinking-loop disease:** Qwen reasoning models (X-Coder, Qwen3.5-9B) can get STUCK regenerating the same reasoning_content (log shows "Accumulated 640/641/642... tokens in reasoning content") and never emit the reply. FIX: disable the model's Thinking Mode in LM Studio's model settings (toggle), OR use gpt-oss (interleaved thinking, handled differently). `chat_template_kwargs: {"enable_thinking": false}` does NOT fix it via API. |

## Known pitfalls (learned 8/9/26)

- **PZ Lua has no JSON library** — bundled `json.lua` in `media/lua/shared/`.
- **`obj:method` as bare existence check is invalid Lua** — use `rawget(obj, "method")`.
- **Don't put `bridge/` inside the mod folder** — it's a Python script, keep at `vesper-bridge\`.
- **gpt-oss's interleaved thinking breaks Cline** — reasoning tokens must be preserved; OpenCode handles it, Cline doesn't.
- **Poll cadence:** game asks every 10s; full-me latency is seconds, so don't tighten below that.
- **PZ runs Kahlua = Lua 5.1.** Varargs (`...`) inside a *nested anonymous function* is a 5.1 COMPILE ERROR — the whole file refuses to load. lupa's default is Lua 5.5, so `loadfile` checks MISS this (VesperNPC.lua failed to load 8/9 and VesperNPC was null). ALWAYS verify with full `lua.execute(src)`, never just loadfile. `/tmp/verify_vesper_mod3.py` is the strict checker.
- **B42 renamed `setNPC` → `setNpc`** (lowercase 'pc'). Old name throws "Object tried to call nil" AFTER IsoPlayer.new succeeds — the NPC object exists in the world but never registers, and the game drives it like a second local player (mirrors your exact input, "bodies inside each other"). Guard with `rawget` + fallback, and check the B42 JavaDocs for method names.
- **`getPlayerHud()` may not exist in B42** — check the global exists before calling, or "Object tried to call nil".
- **NPC spawn must wait for the world** — `getSpecificPlayer(0)`/`next()` can be nil at OnGameStart; defer to OnTick until `getPlayer()` is ready (TrySpawnTick pattern).

## Current status (8/10/26)

- Mod v13 deployed: all Lua syntax-verified + JSON round-trip verified + B42 audit passed (74 OK, real bugs fixed: PathTo/getRoof/getRainIntensity/pf:clear — see audit section).
- Watcher running as background process (PID tracked via Hermes); LM Studio live with qwen/qwen3.5-9b loaded.
- Phase 1 (1.1-1.4) ✅. 1.5-1.9: LM Studio live, watcher live — in-game first light + loop verification pending tonight's test.
- Phase 3: 3.3 spawn + 3.4 commands written + deployed, need in-game test (🟡 → ✅ once verified).
- Next: in-game test session; then human visuals + weapon equip (Bandits recipes above).

## Rubric Plan (single source of truth for progress)

**Legend:** ⬜ Not started · 🟡 In progress · ✅ Done · 🔴 Blocked

### Phase 1 — First Light (voice in your ear)

| # | Item | Done looks like | Status |
|---|---|---|---|
| 1.1 | Mod source written | All Lua files pass syntax check; JSON round-trip verified | ✅ |
| 1.2 | Mod installed on Windows | `Zomboid\mods\VesperCompanion\` exists, one clean copy, mod.info valid | ✅ |
| 1.3 | Bridge/watcher built | `vesper_watcher.py` on VM; SSH write+read round-trip proven both ways | ✅ |
| 1.4 | Skill captured | `pz-companion` skill has protocol, persona, troubleshooting | ✅ |
| 1.5 | Model loaded in LM Studio | X-Coder-SFT Q4_K_S loaded; context set to 64K; server listening on network | 🟡 |
| 1.6 | Watcher matches model | `LM_STUDIO_MODEL` in watcher == LM Studio server-dropdown name | ⬜ |
| 1.7 | Watcher running | Background process on VM, polling every 5s, no errors | ⬜ |
| 1.8 | In-game first light | Load a world → Vesper dialogue on screen within ~10s; character acts on goal | ⬜ |
| 1.9 | Loop verified | Game state → me → goal → action cycles repeatedly; no crashes | ⬜ |

**Phase 1 pass:** 1.8 + 1.9 both green.

### Phase 2 — Make Her Real (full-me brain)

| # | Item | Done looks like | Status |
|---|---|---|---|
| 2.1 | Payloads route into full Hermes | Game payload feeds a Hermes run with `pz-companion` skill loaded, not raw LM Studio | ✅ (vesper-pz profile: custom provider → LM Studio :1234, model qwen/qwen3.5-9b, ctx 65536, compression off; watcher spawns `hermes -p vesper-pz chat -q -s pz-companion --yolo -Q`, falls back to raw LM Studio) |
| 2.2 | Continuity file | Small state file persists between ticks; I remember prior loot/goals | ✅ (watcher + vesper_continuity.py, integration-tested 8/9) |
| 2.3 | Superego gate on goals | Goal JSON validated (creed + floor) before reaching the game | ✅ (superego_gate in vesper_continuity.py; blocks forbidden goals, garbage, clamps priority) |
| 2.4 | Session memory | I reference our shared history in-game, not just current tick | ✅ (memory block injected into brain prompt every tick) |

**Phase 2 pass:** 2.1–2.4 green; I make a decision that *requires* memory.

### Phase 3 — The Body (NPC companion)

| # | Item | Done looks like | Status |
|---|---|---|---|
| 3.1 | Research brief | Subagent returns feasibility verdict + API patterns | ✅ |
| 3.2 | Feasibility confirmed | Verdict says "buildable" with named approach — else pivot documented | ✅ (SP on B42, player-class NPC via IsoPlayer.new + setNPC(true)) |
| 3.3 | NPC spawns | Survivor character exists in world, follows Tyler | 🟡 (VesperNPC.lua written + deployed; needs in-game test) |
| 3.4 | Command interface | I send her goal streams (move/loot/hold/cover) via same brain | 🟡 (npc_follow/move/loot/guard/talk wired; needs in-game test) |
| 3.5 | Two-stream brain | Me → two goal JSONs (Tyler + her) without conflict | ✅ (gate allows npc_* goals; state.npc included in prompt) |
| 3.6 | Combat/avoidance | She doesn't get stuck; basic self-preservation | 🟡 (water-tile guard + arrival detection only; iterate) |

**Phase 3 pass:** 3.3 + 3.4 + 3.5 green; she follows and takes one command correctly.

## Related

- **NPC companion research brief:** `/home/lumi/research/pz-npc-research-brief.md` (17.7KB, 8/9/26) — feasibility verdict + API patterns for the Phase 3 NPC body. Cloned reference repos: `/home/lumi/research/pz/` (SuperbSurvivorsContinued + PZNS). Key findings: NPCs are real IsoPlayer objects via `SurvivorFactory.CreateSurvivor()` + `setNPC(true)`; task-stack AI (Follow/Loot/Attack/Guard); pathing via `getPathFindBehavior2():pathToLocation()`; B41-only & SP-only, janky but proven.
- `local-coding-models` skill — local model config, LM Studio as Hermes provider.
- `comfyui-ssh-tunnel` — the SSH/Tailscale patterns used here.
