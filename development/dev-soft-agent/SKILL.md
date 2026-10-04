---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Automated software development pipeline. Scans projects, prioritizes tasks, analyzes code, and orchestrates development loops. Zero dependencies (Python stdlib only).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="dev-soft-agent banner">

# Dev Soft Agent

Automatisierte Software-Entwicklungspipeline. Extrahiert aus BACHs ATI-Agent,
laeuft vollstaendig standalone mit reiner Python-Standardbibliothek.

## Komponenten

```
scripts/
  config.py              Konfiguration (Scan-Ordner, Naming-Prefixes, Gewichte)
  project_manager.py     Projekt-Scan + Klassifizierung nach Naming-Konvention
  task_engine.py          AUFGABEN.txt Parser + Code-Scanner (TODO/FIXME)
  code_analyzer.py       Statische Analyse (LOC, Imports, Klassen, Funktionen)
  dev_loop.py            Orchestrator (DevLoop)
  policies/
    naming.py            snake_case / PascalCase / SCREAMING_SNAKE Pruefung
    encoding.py          UTF-8 Enforcement + BOM Detection
    paths.py             Hardcoded-Path-Erkennung
  prompt_templates/
    task_prompt.txt      LLM-Prompt fuer Task-Bearbeitung
    review_prompt.txt    LLM-Prompt fuer Code-Review
    analysis_prompt.txt  LLM-Prompt fuer Projekt-Analyse
```

## Nutzung als Python-Library

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Projekte scannen
projects = loop.scan_projects()

# Projekt auswaehlen (gewichtete Zufallsauswahl nach Naming-Konvention)
project = loop.select_project()

# Code analysieren
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Tasks laden und priorisieren
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Komplette Dev-Session
result = loop.run_session()
loop.save_session()
```

## Nutzung als CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /pfad/zum/projekt
python -m devSoftAgent tasks /pfad/zum/projekt
python -m devSoftAgent session --project mein-projekt
python -m devSoftAgent status
```

## Naming-Konvention (Projekt-Klassifizierung)

Projekte werden anhand ihres Ordnernamens klassifiziert:

| Prefix | Label | Gewicht | Bedeutung |
|--------|-------|---------|-----------|
| `RDY` | Ready | 1.0 | Hoechste Prioritaet |
| `RDY_FAST` | Fast Ready | 0.5 | Schnell erledigbar |
| `FAST` | Fast | 0.33 | Kleine Aufgabe |
| `DEV` | Development | 0.17 | In Entwicklung |
| `REL` | Released | 0.0 | Fertig, keine Arbeit |
| `ARC` | Archived | 0.0 | Archiviert |

Gewicht bestimmt die Wahrscheinlichkeit bei zufaelliger Auswahl.

## AUFGABEN.txt Format

```markdown
# AUFGABEN - Projektname
# Stand: 2026-03-12

## OFFEN
- [ ] [BUG] Beschreibung des Fehlers
- [ ] [FEATURE] Neues Feature

## IN ARBEIT
- [-] [REFACTOR] Code-Umbau

## ERLEDIGT
- [x] [BUG] Behobener Fehler -- DONE 2026-03-01
```

## Policies

Qualitaets-Policies die automatisch gegen Code geprueft werden koennen:

- **NamingPolicy:** snake_case fuer Module/Funktionen, PascalCase fuer Klassen
- **EncodingPolicy:** UTF-8 erzwingen, BOM erkennen, CRLF markieren
- **PathPolicy:** Hardcoded absolute Pfade erkennen und melden

## Changelog

### 0.1.0 (2026-03-12)
- Migration aus MODULAR_AGENTS/devSoftAgent in Skillbibliothek
- Projekt-Scanner, Task-Engine, Code-Analyzer, DevLoop
- 3 Policies (Naming, Encoding, Paths)
- 3 Prompt-Templates (Task, Review, Analysis)
