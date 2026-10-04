---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Findet und löscht Windows-reservierte NUL-Dateien, die durch die Nutzung von /dev/null in Git Bash entstehen. Headless oder mit GUI.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
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
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---
<img src="banner.png" width="100%" alt="nulcleaner banner">

# nulcleaner - Windows NUL-Datei Bereinigung

## Das Problem

Wenn in Git Bash unter Windows `/dev/null` in Befehlen verwendet wird (z.B. `> /dev/null`),
entsteht anstatt einer Umleitung ins Nichts eine echte **Datei namens `nul`** im aktuellen
Verzeichnis. Windows reserviert "NUL" als Device-Name, weshalb diese Dateien nicht normal
geloescht werden koennen.

Dieses Tool findet und loescht solche NUL-Dateien ueber den erweiterten UNC-Pfad (`\\?\`).

---

## Modi

| Modus | Beschreibung |
|-------|-------------|
| `scan` | Verzeichnis rekursiv nach NUL-Dateien durchsuchen |
| `delete` | NUL-Dateien finden und loeschen |
| `gui` | Grafische Oberflaeche mit Dateiauswahl |

---

## CLI Usage

```bash
# Nur scannen (zeigt gefundene NUL-Dateien)
python nulcleaner.py scan /pfad/zum/verzeichnis

# Scannen und loeschen
python nulcleaner.py delete /pfad/zum/verzeichnis

# GUI-Modus starten
python nulcleaner.py gui
```

---

## Headless-API (fuer Integration)

Das Tool bietet auch eine Python-API fuer headless-Betrieb:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/pfad/zum/verzeichnis", verbose=True)
print(f"Gefunden: {result['found']}, Geloescht: {result['deleted']}")
```

**Rueckgabe:** `{'found': int, 'deleted': int, 'errors': list}`

---

## Technische Details

- Nutzt den erweiterten UNC-Pfad (`\\?\`) um Windows-reservierte Dateinamen zu loeschen
- Rekursiver Scan mit `os.walk()`
- GUI mit tkinter (keine externen Dependencies)
- Funktioniert nur unter Windows (dort entsteht das Problem)

---

## Praevention

Am besten `/dev/null` in Git Bash vermeiden. Stattdessen:
- Ausgabe einfach weglassen
- `2>&1` fuer Stderr-Umleitung verwenden
- In Shell-Skripten auf Windows-Kompatibilitaet achten
