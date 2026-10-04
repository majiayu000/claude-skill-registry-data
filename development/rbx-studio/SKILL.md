---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Operating Roblox Studio for game development — the visual editor in which the 3D scene is built, tested, and published. Use this skill for: Studio basics (Explorer, Workspace, play-test, saving the place as .rbxl), the interplay with Rojo (Connect, scene-vs-code mode), AI control of Studio via the Roblox-Studio-MCP (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, reading the Console), the complete asset-pipeline workflow (Creator Store → clean up → kit → scene → .rbxl → Rojo brings it to life), and above all the MANDATORY malware scan for marketplace assets. Also trigger on \"embed an asset from the Store\", \"Studio MCP not working\", \"studios: []\", \"generate material\", \"save scene\", \"is this Roblox asset safe\", \"scripts disappear after Play\"."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: de
status: active
visibility: public
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="rbx-studio banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **Note:** Not affiliated with Roblox Corporation; "Roblox" is a trademark of its owners. "rbx" is the common community shorthand.



# Roblox Studio — Editor, Test, Assets, MCP (Deutsch)

## Übersicht & Zweck

Roblox Studio is the official editor: build the 3D scene, test the game in play mode,
insert assets from the Creator Store, and publish the place. In a Rojo workflow,
Studio owns the **scene** (Workspace, Terrain, placed models) and the **testing** —
the **code** comes via Rojo from the filesystem (see skill `/rojo`).

This skill covers: Studio basics, the clean separation of scene and code work,
AI control via the Roblox-Studio-MCP, and the asset workflow including the
**mandatory malware scan** for every marketplace asset.

## Basics

- **Explorer** — tree of all instances (Workspace, ServerScriptService, ReplicatedStorage, …).
  With Rojo active, the mapped areas are populated live from the filesystem.
- **Play-Test** — the green Play button (or F5) starts a local server+client session.
  After every start, **check the Output console for errors** — the most important debug reflex.
- **Save place** — File → Save As → `.rbxl` (binary) or `.rbxlx` (XML, diffable).
  The saved place contains the **scene**. Code lives in the filesystem, not in the place.

## The critical workflow: scene mode vs. code mode

On Connect, Rojo overwrites all mapped script areas with the filesystem content.
The `Workspace` (3D scene) is **not** mapped and stays intact. From this follows the
most important rule of daily work — never mix the two modes:

**Mode A — edit the scene (Rojo OFF):**
1. Stop the Rojo server (`taskkill //F //IM rojo.exe` or Ctrl+C).
2. Open the place in Studio, place assets, build the world, arrange.
3. File → Save → the `.rbxl` now holds the new scene.

**Mode B — test the code (Rojo ON):**
1. Open the same place in Studio.
2. Start `rojo serve` → in Studio's Rojo plugin → Connect.
3. Press Play and test. Rojo syncs the scripts; the Workspace comes from the `.rbxl`.
4. While Rojo is running, **do not** save (otherwise the Rojo state freezes into the `.rbxl`).

This way, scene work (Studio) and code work (editor + Rojo) can run in parallel and
conflict-free — artists build scenes, developers write code.

## Roblox-Studio-MCP — AI controls Studio

The Roblox-Studio-MCP lets Claude/Gemini/Codex directly control a **running** Studio
instance: execute code, inspect, Play/Stop, read the Console, insert assets. It does **not**
replace Rojo — it complements it: Rojo for persistent code changes, MCP for inspection,
tests, asset insertion, and material generation.

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```

### Available MCP tools (typical)

| Tool | Purpose |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | list open instances / select the active one |
| `search_game_tree` / `inspect_instance` | search the hierarchy / read properties |
| `execute_luau` | execute Luau code directly in Studio |
| `script_read` / `script_grep` / `script_search` | analyze scripts |
| `multi_edit` | change multiple instances/scripts in a batch |
| `start_stop_play` | control Play/Stop |
| `get_console_output` | read the Output log |
| `screen_capture` | screenshot of the scene |
| `insert_from_creator_store` | insert an asset from the Creator Store |
| `generate_material` | generate an AI material/texture (MaterialVariant) |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | simulate input |

### Setup (user-neutral)

The MCP runs as a server shipped with Studio, often connected via a thin JSON-filter wrapper
(it filters out non-JSON banners that some clients otherwise cannot parse):

- MCP batch (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- optional wrapper: `<your roblox-mcp wrapper>`
  (if present on this system; shared by Claude/Codex/Gemini)
- Client configs: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

Example entry (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

### Common MCP problems

| Symptom | Meaning / fix |
| --- | --- |
| `studios: []` or `Not connected to WS host` | not immediately "broken": send `initialize` → wait 2–3 s → `list_roblox_studios`; otherwise restart Studio |
| `Error: connection closed: initialized request` | Studio is not open at all — start Studio, load the place, try again |
| scripts written via MCP gone after Play/Stop | MCP edits to code are not persistent — for lasting code changes use **Rojo** |
| value via `require()` in the plugin VM is wrong | the plugin VM has its own require cache — to verify, read `.Source` directly or check the server log after Play |

## Asset pipeline (Creator Store → game)

Greybox first (gameplay), assets later (before release). The proven sequence:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```

**Variant technique ("modular kit"):** Take a good base asset and derive a whole
set from it (house → tower, barn, smithy, ruin). They all share materials, colors, and
proportions → a consistent look with minimal effort, the way pro studios do it.

**Asset sources (priority):** Creator Store (free, huge, **malware check mandatory**) →
AI materials (`generate_material`) → your own meshes (Blender → .fbx) → purchased asset packs.

## MANDATORY: malware scan for marketplace assets

Creator Store assets can contain obfuscated malicious scripts (backdoors, remote code,
bot-network hooks). Scan **every** imported asset before use and remove all scripts —
keep only geometry/meshes.

- Pattern reference: [`references/malware-patterns.md`](references/malware-patterns.md) — the 8
  known obfuscation patterns (reversed attribute payload, fake system script, remote
  `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, hidden Values, delayed execution).
- Scanner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — run it in Studio via
  `execute_luau` (or the Command Bar); it checks an instance against all patterns and reports finds.

**Red flags immediately:** a large script in a pure decoration model · reversed strings in
attributes · `require(<number>)` · `loadstring` · `HttpService` in an asset that needs no
networking. When in doubt: delete the script. Document finds (e.g. `_malware_reports/YYYY-MM-DD_*.md`
in the reference pipeline).

## Important Luau/Studio pitfalls (excerpt)

The most common ones that bite in Studio — the full list is kept by the skill `/rbx-dev`:

- `Model.Position` does not exist → `model:GetPivot().Position`.
- `tick()` is deprecated → `os.clock()` / `workspace:GetServerTimeNow()`.
- `SetPrimaryPartCFrame()` deprecated → `model:PivotTo(cf)`.
- DataStore calls **always** in `pcall`.
- Baseplate + procedural floor at the same height → Z-fighting (flicker): remove the baseplate
  or raise the floor by +0.1 studs.
- Keep an eye on the part budget (~50–80 parts per procedurally generated room).

## Further reading

- Sister skills: `/rojo` (sync, project setup), `/game-design` (roles, workflows, GDD),
  meta skill `/rbx-dev` (architecture patterns + all Luau lessons).
- Engine/Creator docs: Context7 MCP (`/websites/create_roblox_reference_engine`,
  `/roblox/creator-docs`) or <https://create.roblox.com/docs>.
- Reference pipeline (if present): `<your Roblox project pipeline>`
  (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`).

## Änderungsprotokoll

### 1.0.0 (2026-06-17)
- Initial version. Distilled from the `.ROBLOX` pipeline (ROBLOX_MCP_FAQ, ASSET_PIPELINE,
  PATTERNS, LESSONS_LEARNED), written user-neutral.