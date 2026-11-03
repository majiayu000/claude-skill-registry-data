---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Batch-Dateioperationen (Löschen, Verschieben, Kopieren, Auflisten) mit Glob-Mustern. CLI-Werkzeug für effiziente Dateisystem-Operationen. Ohne Abhängigkeiten.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---
<img src="banner.png" width="100%" alt="batch-file-ops banner">

# batch_file_ops - Batch-Dateioperationen

CLI-Tool fuer effiziente Batch-Operationen auf Dateien mit Glob-Patterns.
Unterstuetzt: delete, move, copy, list. Zero Dependencies (nur Python stdlib).

---

## Aktionen

| Aktion | Beschreibung |
|--------|-------------|
| `delete` | Dateien nach Pattern loeschen |
| `move` | Dateien nach Pattern verschieben |
| `copy` | Dateien nach Pattern kopieren |
| `list` | Dateien nach Pattern auflisten |

## CLI Usage

```bash
python batch_file_ops.py <aktion> <quelle> [<ziel>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Argumente

| Argument | Beschreibung |
|----------|-------------|
| `aktion` | `delete`, `move`, `copy` oder `list` |
| `quelle` | Quellordner |
| `ziel` | Zielordner (nur fuer `move` und `copy`) |
| `--pattern`, `-p` | Glob-Pattern (z.B. `*.py`, `TOOLS_*.py`) - Standard: `*` |
| `--dry-run`, `-n` | Nur anzeigen, nichts aendern |
| `--recursive`, `-r` | Rekursiv in Unterordnern suchen |

---

## Beispiele

```bash
# Alle Python-Dateien in einem Ordner auflisten
python batch_file_ops.py list /pfad/zum/ordner --pattern "*.py"

# Alle .tmp Dateien loeschen (erst Dry-Run!)
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp"

# Dateien verschieben
python batch_file_ops.py move /quelle /ziel --pattern "*.txt"

# Dateien kopieren (rekursiv)
python batch_file_ops.py copy /quelle /ziel --pattern "*.md" --recursive

# Pattern-Beispiele
python batch_file_ops.py delete /pfad --pattern "TOOLS_*.py"
python batch_file_ops.py list /pfad --pattern "backup_202?-*"
```

---

## Hinweise

- **Dry-Run zuerst:** Bei `delete` und `move` immer erst `--dry-run` verwenden
- **Glob-Patterns:** Nutzt Python `pathlib.glob()` / `pathlib.rglob()`
- **Windows-kompatibel:** Automatisches UTF-8 Output-Encoding
- **Nur Dateien:** Ordner werden uebersprungen (nur Dateien werden bearbeitet)
