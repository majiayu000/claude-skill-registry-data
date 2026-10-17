---
name: learning-loop
description: 'Use for auto error capture, categorization and skill gen.'
category: system
---

# Learning Loop — Continuous Learning from Errors

Automatische Fehler-Capture, Kategorisierung, Memory-Speicherung, Skill-Generierung und Trend-Analyse.

## CLI Modi

| Modus | Beschreibung |
|-------|-------------|
| `--capture` | Scanne alle Logs nach Fehlern |
| `--analyze` | Kategorisiere und aktualisiere Memory |
| `--suggest` | Generiere Skills fuer wiederkehrende Fehler (count >= 4) |
| `--trend` | Zeige Verbesserungs-Trend (Fix-Rate, Fehler/h) |
| `--report [html|json]` | Generiere Report (default HTML) |
| `--auto` | Full Cycle: capture -> analyze -> suggest -> report |

Exit-Codes: 0=stabil, 1=neue Muster, 2=neue Skills

## Kategorien (13)

import_error, connection_failed, timeout, permission, syntax_error, file_not_found, api_error, provider_error, memory_error, cua_driver_error, tool_error, lsp_error, unknown

## Speicherstruktur

- `.learning-loop/memory.json` - Pattern-Memory
- `.learning-loop/metrics.json` - Zeitreihen-Metriken
- `.learning-loop/last_capture.json` - Letzter Capture-Zustand
- `.learning-loop/learning-loop-report.html` - HTML-Report
- `skills/learning-loop/` - Auto-generierte Skills

## Setup

```bash
python scripts/learning-loop.py --auto       # Erster voller Durchlauf
python scripts/learning-loop.py --trend      # Trend anzeigen
python scripts/learning-loop.py --report      # Report generieren
```

## Cron-Job (alle 60min)

```json
{
  "name": "Learning Loop Auto Cycle 60min",
  "script": "learning-loop.py --auto",
  "no_agent": true,
  "schedule": {"kind": "interval", "minutes": 60},
  "workdir": "C:\\Users\\damir\\AppData\\Local\\openamer-laptop"
}
```