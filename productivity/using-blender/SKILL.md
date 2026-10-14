---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: General Blender workflow skill for AI agents working with .blend, .fbx, .obj, .glb, glTF, materials, scene inspection, bpy automation, headless Blender batch runs, export/reimport validation, previews, and optional Blender MCP control. Use when a task asks to open, inspect, create, automate, convert, optimize, render, or verify Blender or 3D asset files in a user-agnostic way.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: de
status: active
visibility: public
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="using-blender banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `using-blender`.


# Using Blender (Deutsch)

## Kernregel

Arbeite mit Blender in drei Modi, passend zur Aufgabe:

1. **GUI-Modus:** Blender sichtbar öffnen, wenn der Nutzer ein Asset anschauen, beurteilen oder manuell weiterbearbeiten will.
2. **Headless-Modus:** `blender --background --python <script.py>` nutzen, wenn Export, Reimport, Batch-Verarbeitung oder deterministische Prüfung gefragt ist.
3. **MCP-Modus:** Nur verwenden, wenn ein laufendes Blender-Addon bewusst verbunden ist und Live-Szenensteuerung nötig ist. Vorher Sicherheits- und Lizenzlage prüfen.

## Standardablauf

1. Ziel klären: ansehen, erzeugen, konvertieren, optimieren, rendern oder verifizieren.
2. Bestehende Dateien lesen: Manifest, README, Exportformate und vorhandene Prüfergebnisse zuerst.
3. Blender-Pfad ermitteln: `blender` auf PATH, projektspezifische Konfiguration oder Nutzerpfad. Keine lokalen Privatpfade in publizierbare Doku schreiben.
4. Für Automatisierung ein kleines `bpy`-Script verwenden, das Eingaben, Ausgaben und Fehler explizit macht.
5. Nach jedem Export mindestens einen Reimport- oder Ladecheck ausführen, bevor das Ergebnis als nutzbar gilt.
6. Artefakte knapp dokumentieren: Quelle, Exportformate, Toolversion, Prüfstatus und bekannte Grenzen.

## Export- und Prüfregeln

- Für allgemeine Web-/Preview-Nutzung bevorzugt `.glb`.
- Für Game-Engines und DCC-Austausch zusätzlich `.fbx` oder `.obj/.mtl` anbieten, wenn der Zielworkflow das braucht.
- Für Roundtrips immer prüfen: Datei existiert, nicht leer, kann reimportiert werden, erwartete Objekt-/Materialnamen sind vorhanden.
- Für große Assets Metriken erfassen: Mesh-Anzahl, Materialien, Bounding Box, Dateigröße und optional Triangle Count.
- Für Renderprüfungen kleine Preview-Auflösung verwenden, bevor teure Cycles- oder Full-HD-Renders gestartet werden.

## Sicherheitsregeln

- `bpy`-Code ist lokaler Python-Code mit Dateisystemzugriff. Nur selbst geschriebene oder auditierte Scripts ausführen.
- Keine fremden Blender-Addons, Asset-Downloader oder Telemetrie-Server aktivieren, ohne Lizenz- und Datenschutzcheck.
- Bei MCP-Servern mit beliebigem `execute_python`-Tool vorher Scope, Netzwerk, Arbeitsverzeichnis und Timeout begrenzen.
- Bei Marketplace- oder externen Assets die Lizenz separat prüfen. Die technische Ladefähigkeit ersetzt keine Nutzungsrechte.

## MCP-Optionen

Für Live-Steuerung lies [references/blender-mcp-review.md](references/blender-mcp-review.md), wenn ein Blender-MCP-Server ausgewählt, installiert oder bewertet werden soll.

## Änderungsprotokoll

### 1.0.0 (2026-06-20)
- Initialer nutzeragnostischer Blender-Skill mit GUI-, Headless- und MCP-Routing.

## Ergebnis prüfen, ohne die GUI zu öffnen

Für Assets gibt es ein fertiges Background-Gate, das **vier Renders und messbare Metriken**
in einem Lauf liefert (Rotation, Pivot, schwebende Teile):

```powershell
blender.exe --background --factory-startup `
  --python "<OneDrive>\.TOPICS\.ROBLOX\_tools\verify_asset_visual.py" -- `
  --fbx "<asset.fbx>" --out "<ordner>" --json
```

Kein GUI, kein Fokus nötig. Details und Grenzen (u. a.: der MCP-Server `ellmos-blender-use`
kann **nicht** rendern): `.ROBLOX\BLENDER_ASSET_CHANNELS.md`.
Ausführlicher Workflow: Skill `build-assets-with-blender`.
