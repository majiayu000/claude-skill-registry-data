---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Meta-skill for complete Roblox game development with Rojo — the entry point that knows and unifies the three specialist skills `/rojo` (filesystem→Studio sync, project setup), `/rbx-studio` (editor, MCP, assets, malware scan) and `/game-design` (roles, workflows, GDD). Use this skill for ANY Roblox game-dev undertaking: planning/building/setting up a Roblox game, scaffolding a new project, defining code architecture (Main + manager modules, _G.ClientState + HUD, remotes in GameEnums), avoiding Luau/Roblox pitfalls, or when it is unclear which of the Roblox specialist skills fits — routing happens from here. Also trigger on \"develop Roblox game\", \"build Roblox game\", \"new Roblox project\", \"Luau project structure\", \"how do I organize Roblox code\", \"Roblox dev setup\"."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: de
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---
<img src="banner.png" width="100%" alt="rbx-dev banner">

> **Hinweis:** Nicht mit der Roblox Corporation affiliiert; „Roblox" ist eine Marke ihrer Inhaber. „rbx" ist das gängige Community-Kürzel.



# Roblox-Dev — Meta-Skill für Roblox-Spieleentwicklung

## Zweck

Der zentrale Einstieg für Roblox-Game-Dev mit einem Rojo-basierten, versionierbaren Workflow.
Dieser Skill bündelt das übergreifende Wissen — Projektstruktur, Architektur-Pattern und die
wichtigsten Luau-Fallstricke — und leitet für Spezialfragen an die drei Unterskills weiter:

| Unterskill | Wofür |
| --- | --- |
| **`/rojo`** | Filesystem→Studio-Sync, `default.project.json`, rokit/Wally/Lune, Projekt-Skelett, Sync-Probleme |
| **`/rbx-studio`** | Studio-Bedienung, Szene-vs-Code-Modus, Studio-MCP, Asset-Pipeline, **Malware-Scan** |
| **`/game-design`** | Rollen & Teilaufgaben, Entwicklungs-Chains, Game Design Document (KONZEPT.md), Multi-Agent |

> Routing-Regel: Geht es um **Sync/Build/Setup** → `/rojo`. Um **Editor/Assets/Testen in Studio**
> → `/rbx-studio`. Um **Konzept/Rollen/Prozess** → `/game-design`. Um **Code-Architektur,
> Luau-Stolperfallen oder den Gesamtablauf** → hier bleiben.

## Stack auf einen Blick

- **Sprache:** Luau (`.luau`, nicht `.lua`). Code englisch, Kommentare/Doku deutsch, UI-Texte deutsch.
- **Sync:** Rojo via rokit (gepinnte Tool-Versionen). Dateisystem = Quelle der Wahrheit.
- **Tools:** Rojo (Sync/Build), Lune (Tests/Skripte außerhalb Studio), Wally (Packages),
  optional Knit (Service-/Controller-Framework, neue Projekte), Selene (Linter).
- **Steuerung:** Roblox-Studio-MCP für KI-gesteuerte Inspektion/Tests/Asset-Insertion.

## Projektstruktur (Standard)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

Ein Skelett legt `/rojo` per `scaffold_roblox_project.sh` an.

## Architektur-Pattern

**Server — Main + Manager-Module.** Pro Projekt nur **ein** Script: `Main.server.luau`. Es
erstellt zentral den Remotes-Ordner und lädt alle Feature-Module per `require()`:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
Alle anderen Server-Dateien sind `.luau` (ModuleScripts).

**Client — geteilter State + HUD.** Der GameClient schreibt einen geteilten State, das HUD liest
ihn im Heartbeat:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — zentral in GameEnums.** Remote-Namen einmal in `GameEnums.Remotes` definieren;
Server erstellt die Events darüber, Client sucht sie über dieselben Namen. So gibt es keine
String-Mismatches zwischen Server und Client.

## Gesamtablauf eines Spiels

1. **Konzept** (`/game-design`): KONZEPT.md — Genre, USP, 3–4 Kern-Mechaniken, Monetarisierung.
2. **Setup** (`/rojo`): Skelett scaffolden, `default.project.json`-Mapping festlegen.
3. **Backend**: Config → GameEnums → *Defs → Main.server → *Manager.
4. **Frontend**: GameClient → HUD.
5. **Greybox-Playtest** (`/rbx-studio`): Gameplay zuerst, Parts + ggf. KI-Materials.
6. **Asset-Upgrade** (`/rbx-studio`): Creator-Store-Assets, **Malware-Scan**, Szene als .rbxl.
7. **Test** (`/game-design`): QA + Spielkritiker + Persona-Blindtests, iterieren.
8. **Release** (`/game-design` Business-Rolle): Store-Seite, Monetarisierung, Live-Ops.

## Luau-/Roblox-Fallstricke (Kurzliste)

Die häufigsten Stolperfallen — vollständige, kommentierte Liste:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md).

- Semicolon nach `task.wait(x)`, wenn weiterer Code in derselben Zeile folgt.
- `Model.Position` existiert nicht → `model:GetPivot().Position`.
- `#table` auf Dictionaries = 0 → manuell zählen.
- `mouse.Hit` kann nil sein → vor Gebrauch prüfen.
- DataStore-Calls **immer** in `pcall`.
- `tick()` deprecated → `os.clock()`; `SetPrimaryPartCFrame` → `PivotTo`.
- Event-Namen zentral in `GameEnums.Remotes`; alle Remotes in `Main.server.luau` erstellen.
- Keine zirkulären `require`s (sonst Deadlock).
- `require()` nur auf `.luau`-ModuleScripts, nie auf Scripts/LocalScripts.

## Vor jedem Commit (Checkliste)

- [ ] Semicolons nach `task.wait(...)` in Mehrfach-Statements
- [ ] kein `Model.Position`, kein `tick()`, kein `SetPrimaryPartCFrame`
- [ ] DataStore in `pcall`, `mouse.Hit` auf nil geprüft
- [ ] Event-Namen matchen Server↔Client (über GameEnums)
- [ ] alle RemoteEvents in `Main.server.luau` erstellt
- [ ] keine zirkulären Requires
- [ ] Marketplace-Assets gescannt (`/rbx-studio` → Malware-Scan), Reports abgelegt

## Wissensquellen

- **Aktuelle Engine-/Creator-Doku:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine` (Engine-API) und `/roblox/creator-docs`
  (Tutorials/Guides); Fallback <https://create.roblox.com/docs>.
- **Referenz-Pipeline** (falls auf diesem System vorhanden): `<your Roblox project pipeline>` —
  u. a. `SKILL.md`, `GUIDE.md`, `LESSONS_LEARNED.md`, `ROJO_FAQ.md`, `ROBLOX_MCP_FAQ.md`,
  `AGENT_ROLES.md`, `_malware_reports/PATTERNS.md`, `_knowledge/` (lokaler API-Cache).

## Changelog

### 1.0.0 (2026-06-17)
- Initiale Version. Meta-Skill über `/rojo`, `/rbx-studio`, `/game-design`; Projektstruktur,
  Architektur-Pattern und Luau-Lessons destilliert aus der `.ROBLOX`-Pipeline, nutzerneutral.
