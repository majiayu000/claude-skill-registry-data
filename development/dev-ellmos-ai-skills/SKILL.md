---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "Developer assistant (ATI successor). Provides a quick project overview via headless scan and routes to the available coding tools: CodeCommander MCP (analysis/refactor/diagnose) and the ellmos-code-tools module. Pure tool routing + scan, no own store."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: de
status: active
visibility: public
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="dev banner">

# Dev — Entwickler-Assistent (ATI)

Verschafft Überblick, dann übergibt er an die richtigen Werkzeuge.

## Zweck

Nachfolger von BACHs ATI/entwickler-Agent. Zwei Aufgaben:
1. **Projekt-Scan** (headless, stdlib): schneller, tokensparender Überblick über
   Struktur, Sprachen und Build-Marker eines Projekts — bevor teure Analyse läuft.
2. **Werkzeug-Routing:** leitet auf die vorhandenen Coding-Tools weiter statt eigene
   zu duplizieren.

## Trigger

| Nutzereingabe | Aktion |
|---|---|
| „Verschaff dir Überblick über das Projekt X" | `dev_core.py scan <pfad>` |
| „Was ist das für ein Projekt / welcher Stack?" | `dev_core.py scan <pfad>` |
| „Analysiere diese Datei / refactor" | → CodeCommander-MCP |
| „Generiere/prüfe Python-Code" | → CodeCommander-MCP / ellmos-code-tools |

## Werkzeug-Landschaft (Routing-Ziele)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` u.a.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): CLI-Devtools (Structural-Edit,
  pycutter-Kontext, Method-Analyzer).
- **FileCommander-MCP**: Datei-/Verzeichnis-Operationen über große Bäume.

## CLI-Einstieg (dev_core.py)

```bash
python dev_core.py scan .              # aktuelles Projekt
python dev_core.py scan /pfad/projekt  # Struktur + Sprachen + Marker
```

Erkennt u.a.: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, Git-Repo.

## Store

Kein Store. Reiner Scan + Routing.

## Haltung

Wir empfehlen CodeCommander/ellmos-code-tools als Coding-Werkzeuge, sind aber offen
für andere (z.B. ruff/pylint/eslint), falls der Nutzer das vorzieht.

## Datenschutz

- `dev_core.py` liest nur Datei-/Verzeichnisnamen (Struktur), keine Inhalte, kein Upload.
- Übersprungen werden u.a. `.git`, `node_modules`, `.venv`, `__pycache__`.

## Verwandte Ressourcen

- `assist/AGENTS.md` — Umbrella-Router
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## Changelog

### 0.1.0 (2026-06-22)
- Initiale Version. ATI/entwickler-Nachfolger: headless Projekt-Scan (stdlib) +
  Routing auf CodeCommander-MCP / ellmos-code-tools. Userneutral, kein Store.
