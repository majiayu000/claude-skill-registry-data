---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Operating Rojo — the filesystem-to-Roblox-Studio sync tool for professional Roblox development in VS Code / Claude Code instead of the Studio editor. Use this skill whenever Rojo is involved: `rojo serve`/`rojo build`, writing or debugging `default.project.json`, rokit/rokit.toml and tool versions (Rojo, Lune, Wally), nested vs. flat path mapping (ReplicatedStorage.Project.shared), connect/port/sync problems, or when a Roblox project skeleton needs to be created. Also trigger on \"rojo connect not working\", \"scripts end up in the wrong place in Studio\", \"how do I map src/ to Studio\", \"port 34872 in use\", \"ModuleScript vs Script in Rojo\"."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: de
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---
<img src="banner.png" width="100%" alt="rojo banner">

# Rojo — Filesystem → Roblox Studio Sync

## Zweck

Rojo verbindet ein normales Dateisystem-Projekt (`.luau`-Dateien in `src/`, versioniert mit Git)
mit Roblox Studio. Du schreibst Code im Editor deiner Wahl (VS Code, Claude Code), Rojo
synchronisiert ihn live in eine laufende Studio-Instanz. So wird Roblox-Code versionierbar,
diffbar und mit echten Tools bearbeitbar — statt im eingebauten Studio-Skripteditor zu leben.

Nutze diesen Skill für alles rund um Rojo-Setup, das `default.project.json`-Mapping, die
Toolchain (rokit/Wally/Lune) und typische Sync-Probleme.

## Mentales Modell

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**Kernregel:** Das Dateisystem ist die Quelle der Wahrheit. Rojo überschreibt bei jedem
Connect die gemappten Studio-Bereiche mit dem Filesystem-Inhalt. Bearbeite Code daher **nie**
in Studio (geht beim nächsten Sync verloren), sondern nur im Editor. Der `Workspace`
(3D-Szene, Terrain) wird von Rojo **nicht** gemappt und bleibt erhalten — siehe Skill
`/rbx-studio` für den Szene-vs-Code-Workflow.

## Dateiendungen → Roblox-Typ (Rojo-Konvention)

Rojo leitet den Instanztyp aus der Endung ab. Das ist die häufigste Fehlerquelle:

| Datei              | Roblox-Typ    | `require()`-bar | Rolle                     |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **ja**          | Logik-Modul, Definitionen |
| `Foo.server.luau`  | Script        | nein            | Server-Entry-Point        |
| `Foo.client.luau`  | LocalScript   | nein            | Client-Entry-Point        |
| `init.luau`        | wird zum Ordner-Knoten selbst | ja | macht Ordner zum ModuleScript |

> Faustregel: **Nur Entry-Points** sind `.server.luau`/`.client.luau`. Alles, was per
> `require()` geladen wird, **muss** ein `.luau`-ModuleScript sein. `require()` auf ein
> Script/LocalScript wirft "Attempted to call require with invalid argument(s)".

## CLI-Befehle

```bash
rojo serve default.project.json     # Live-Sync-Server starten (Standard-Port 34872)
rojo serve                          # nutzt default.project.json automatisch
rojo build default.project.json -o game.rbxlx   # einmaliger Build → Place-Datei (XML)
rojo build default.project.json -o game.rbxl    # Build → Place-Datei (binär)
rojo plugin install                 # Rojo-Studio-Plugin installieren (einmalig)
rojo --version                      # installierte Version prüfen
```

Nach `rojo serve`: in Studio das Rojo-Plugin öffnen → **Connect** (localhost:34872).
`rojo build` braucht kein laufendes Studio — ideal für CI, Smoke-Tests und Releases.

## `default.project.json` — das Mapping

Diese Datei mappt Dateisystem-Pfade auf die Roblox-Datamodel-Hierarchie. Schlüssel:

- `name` — Projektname (Anzeige)
- `$className` — Roblox-Klasse des Knotens (`DataModel`, `ServerScriptService`, `Folder`, …)
- `$path` — Dateisystem-Pfad, der unter diesen Knoten gesynct wird (relativ zur Projektwurzel)

Ein einsatzfertiges Standard-Template liegt unter [`assets/default.project.json`](assets/default.project.json).

### Flach vs. verschachtelt — die wichtigste Entscheidung

Dein Code muss zum Mapping passen. Zwei Varianten:

**Flach** — Inhalt von `src/server` landet direkt in `ServerScriptService`:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ Code referenziert z. B. `ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`.

**Verschachtelt** — Inhalt landet in `ServerScriptService.ProjektName`:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ Code referenziert `ReplicatedStorage.ProjektName.shared.Config` usw.

Beide sind gültig. Entscheide dich projektweit für **eine** Variante und halte jeden
`require`/`WaitForChild`-Pfad konsistent dazu. Symptom bei Mismatch: `WaitForChild(...)`
hängt endlos (Infinite yield), weil der erwartete Knoten an anderer Stelle liegt.

## Toolchain via rokit

[rokit](https://github.com/rojo-rbx/rokit) ist der Toolchain-Manager. Eine `rokit.toml` im
Projekt (oder Elternordner) pinnt exakte Tool-Versionen → reproduzierbare Builds auf allen
Maschinen. Fehlt sie, kommt `Failed to find tool 'rojo' in any project manifest file`.

Standard-`rokit.toml` (siehe [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> Versions-Hinweis: 7.4.4 ist die in der Referenz-Pipeline durchgängig gepinnte Version.
> Neuere Projekte können auf 7.6.x gehen — vorher mit `rojo build` gegen das Projekt prüfen,
> da sich das Projektformat zwischen Major-Versionen ändern kann.

Nach Klonen/Setup: `rokit install` zieht alle gepinnten Tools.

- **Lune** — Luau-Runner außerhalb Studio (Unit-Tests, Build-Skripte, Asset-Verarbeitung).
- **Wally** — Paketmanager: `wally install` → `Packages/` → in Studio unter
  `ReplicatedStorage.Packages`. Dependencies stehen in `wally.toml` (siehe
  [`assets/wally.toml`](assets/wally.toml)), z. B. das Framework `sleitnick/knit@1.7.0`.

## Neues Projekt anlegen

Das Skript [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) legt ein
komplettes Rojo-Skelett an (project.json, rokit.toml, wally.toml, `src/{shared,server,client,gui}/`
mit Starter-Dateien, KONZEPT-Stub):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # flaches Mapping (Default)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # verschachteltes Mapping
```

Danach: `cd MeinSpiel && rokit install && rojo serve`.

## Troubleshooting

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | keine `rokit.toml` | `rokit.toml` mit Rojo-Pin im Projekt/Elternordner anlegen, `rokit install` |
| `require` wirft "invalid argument(s)" | `require()` auf ein Script/LocalScript | nur `.luau`-ModuleScripts sind require-bar; Endung prüfen |
| Port 34872 belegt (`os error 10048`) | alter Rojo-Prozess läuft | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`, dann neu `rojo serve` |
| Scripts landen falsch in Studio | flaches statt verschachteltes Mapping (oder umgekehrt) | `default.project.json` an die Code-Pfade anpassen (siehe oben) |
| `WaitForChild` hängt endlos | erwarteter Knoten existiert nicht / Server-Fehler vor Erstellung | **zuerst Server-Console auf Fehler prüfen**; Mapping + Erstellungsreihenfolge checken |
| Sync nach Datei-Umbenennung bleibt aus | Rojo erkennt Rename nicht sofort | Server stoppen (Ctrl+C) + neu starten, in Studio Disconnect→Reconnect |
| Änderung in Studio weg nach Reconnect | Studio-Edit statt Filesystem-Edit | Code **nur** im Editor ändern; Rojo überschreibt gemappte Bereiche |

### Bekannte Rojo-Grenzen

1. **Kein Terrain-/Workspace-Sync** — 3D-Szene & Terrain in Studio bauen oder per Code generieren.
2. **Kein `.rbxl`-Merge** — Place-Dateien sind binär, nicht git-mergebar. Nie als primäre Quelle.
3. **Kein Live-Sync im Play-Modus** — Änderungen während Play werden bei Stop verworfen.
4. **Git Bash Path-Translation** — `/c/...` kann zu `C:/...` übersetzt werden und Rojo-Pfade brechen; im Zweifel relative Pfade oder native Windows-Pfade nutzen.

## Linting (Selene)

Roblox-Luau-Projekte werden üblicherweise mit **Selene** gelintet (`selene.toml` im Root,
`std = "roblox"`). Globals wie `_G` per `global_usage = "allow"` freigeben, wenn das Projekt
sie für geteilten Client-State nutzt. Selene aus dem Verzeichnis mit der Roblox-API-Definition
(`roblox.yml`) ausführen.

## Weiterführend

- Schwesterskills: `/rbx-studio` (Studio-Bedienung, MCP, Assets), `/game-design`
  (Rollen, Workflows, GDD), Metaskill `/rbx-dev` (vereint alle drei + Architektur-Pattern).
- Aktuelle Engine-/Rojo-Doku: Context7 MCP (`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) oder
  <https://rojo.space/docs/>.
- Falls auf diesem System vorhanden, liegt eine projektreiche Referenz-Pipeline unter
  `<your Roblox project pipeline>` (u. a. `ROJO_FAQ.md`, `SKILL.md`).

## Changelog

### 1.0.0 (2026-06-17)
- Initiale Version. Destilliert aus der `.ROBLOX`-Pipeline (ROJO_FAQ, ROJO_START, _template),
  nutzerneutral gefasst.

## Verwandte Skills

- `roblox-team-lock` — Datei-, Studio- und MCP-Claims, sobald mehrere Agenten am selben Projekt arbeiten. Erst lesen, dann claimen, dann arbeiten, dann freigeben.
