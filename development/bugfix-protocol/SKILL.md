---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Systematic 6-phase debugging protocol. Structured approach to bugs with quick checks, isolated testing, 20-minute rule, and bug report template.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="bugfix-protocol banner">

# Bugfix-Protokoll: Systematisches 6-Phasen Debugging

Strukturiertes Vorgehen bei Bugs — von der Symptom-Analyse bis zur Verifikation.
Verhindert planloses Herumprobieren und stellt sicher, dass Fixes nachhaltig sind.

---

## Uebersicht

| Phase | Name | Ziel | Max. Zeit |
|-------|------|------|-----------|
| 1 | Schnell-Checks | Offensichtliche Ursachen ausschliessen | 2 min |
| 2 | Diagnose | Ursache lokalisieren | 10 min |
| 3 | Isolierter Test | Bug reproduzierbar machen | 5 min |
| 4 | Fix | Minimale Korrektur | 10 min |
| 5 | Verifikation | Fix pruefen + Seiteneffekte | 5 min |
| 6 | Dokumentation | Wissen sichern | 2 min |

**20-Minuten-Regel:** Wenn nach 20 Minuten kein Fortschritt → Ansatz wechseln oder Hilfe holen.

---

## Phase 1: Schnell-Checks (2 min)

Bevor du tief einsteigst — pruefe die haeufigsten Ursachen:

### Checkliste

- [ ] **Syntax-Fehler?** Fehlermeldung genau lesen, Zeile pruefen
- [ ] **Import-Fehler?** Modul installiert? Richtiger Name? Circular Import?
- [ ] **Tippfehler?** Variablen-/Funktionsnamen korrekt?
- [ ] **Falscher Datentyp?** String statt Int? None wo Objekt erwartet?
- [ ] **Veralteter Cache?** `__pycache__` loeschen, Neustart
- [ ] **Falsche Umgebung?** Richtiges venv aktiv? Richtige Python-Version?
- [ ] **Encoding?** UTF-8 vs. cp1252 (Windows-Klassiker)

### Schnell-Aktionen

```bash
# Cache leeren
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Imports pruefen
python -c "import modulname"

# Syntax pruefen
python -m py_compile datei.py
```

---

## Phase 2: Diagnose (10 min)

### Strategie: Von aussen nach innen

1. **Fehlermeldung analysieren** — Traceback von unten nach oben lesen
2. **Letzte Aenderungen pruefen** — `git diff`, `git log --oneline -10`
3. **Diagnose-Tools einsetzen** — Eigene Diagnose-Tools je nach Projekt verwenden

### Diagnose-Tools (Beispiele)

Je nach Projekt koennen spezialisierte Diagnose-Skripte hilfreich sein:

| Tool | Zweck |
|------|-------|
| `import_diagnose.py` | Import-Probleme analysieren |
| `method_analyzer.py` | Methoden-Signaturen pruefen |
| `env_checker.py` | Umgebungsvariablen/Pfade validieren |

> **Hinweis:** Eigene Diagnose-Tools je nach Projekt erstellen oder vorhandene
> Projekt-Tools nutzen. Wichtig ist das systematische Vorgehen, nicht das
> spezifische Tool.

### Debugging-Techniken

```python
# 1. Print-Debugging (schnell aber effektiv)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Breakpoint (interaktiv)
breakpoint()  # Python 3.7+

# 3. Traceback erweitern
import traceback
traceback.print_exc()

# 4. Logging statt Print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## Phase 3: Isolierter Test (5 min)

### Minimal Reproducible Example (MRE)

Ziel: Bug mit minimal Code reproduzieren.

```python
# test_bug.py — Minimaler Reproduktions-Test
"""
Bug: [Kurze Beschreibung]
Erwartet: [Was sollte passieren]
Tatsaechlich: [Was passiert stattdessen]
"""

# Minimaler Setup
# ... nur das Noetigste

# Bug-Ausloeser
# ... exakter Code der den Bug triggert

# Erwartetes Ergebnis
# assert result == expected, f"Got {result}"
```

### Isolations-Strategien

1. **Neue Datei:** Bug in eigener Datei reproduzieren
2. **Abhaengigkeiten entfernen:** Eine nach der anderen, bis Bug verschwindet
3. **Halbieren:** Code-Block halbieren, pruefen welche Haelfte den Bug enthaelt
4. **Git Bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## Phase 4: Fix (10 min)

### Prinzipien

1. **Minimal:** Aendere so wenig wie moeglich
2. **Verstehen:** Nie blind fixen — verstehe WARUM es kaputt ist
3. **Eine Sache:** Ein Fix pro Commit, nicht mehrere Probleme gleichzeitig
4. **Rueckwaerts-kompatibel:** Bestehende Funktionalitaet nicht brechen

### Fix-Muster

```python
# SCHLECHT: Symptom behandeln
try:
    result = broken_function()
except:  # Alles schlucken
    result = default_value

# GUT: Ursache beheben
def broken_function():
    if input_data is None:  # Eigentliche Ursache: None-Check fehlte
        return default_value
    return process(input_data)
```

### Haeufige Fix-Kategorien

| Kategorie | Typischer Fix |
|-----------|--------------|
| None/Null | Guard-Clause: `if x is None: return default` |
| Index-Fehler | Bounds-Check: `if i < len(lst)` |
| Type-Fehler | Explizite Konvertierung: `str(x)`, `int(x)` |
| Import-Fehler | Pfad korrigieren, Paket installieren |
| Encoding | UTF-8 explizit angeben: `encoding='utf-8'` |
| Race Condition | Lock/Mutex, oder Reihenfolge aendern |
| State-Bug | Initialisierung pruefen, Reset einfuegen |

---

## Phase 5: Verifikation (5 min)

### Checkliste

- [ ] **Bug ist gefixt:** Originales Problem tritt nicht mehr auf
- [ ] **MRE besteht:** Isolierter Test laeuft durch
- [ ] **Keine Regression:** Bestehende Tests laufen noch
- [ ] **Edge Cases:** Leere Eingabe, None, grosse Daten getestet
- [ ] **Projekt-Tools:** Im Projekt-Tools-Verzeichnis nachschauen ob es relevante Test-/Validierungstools gibt

### Test-Befehle

```bash
# Unit-Tests
python -m pytest tests/ -v

# Nur betroffene Tests
python -m pytest tests/test_modul.py -v -k "test_name"

# Type-Check
python -m mypy datei.py

# Lint
python -m flake8 datei.py
```

---

## Phase 6: Dokumentation (2 min)

### Bug-Report Template

```markdown
## Bug-Report: [Kurztitel]

**Datum:** YYYY-MM-DD
**Schwere:** kritisch / hoch / mittel / niedrig
**Komponente:** [Modul/Datei]

### Symptom
[Was der User sieht / Fehlermeldung]

### Ursache
[Technische Root-Cause]

### Fix
[Was geaendert wurde + warum]

### Betroffene Dateien
- `datei1.py` — [Aenderung]
- `datei2.py` — [Aenderung]

### Praevention
[Wie kann dieser Bug-Typ in Zukunft vermieden werden?]
```

### Commit-Message Format

```
fix: [Kurze Beschreibung des Fixes]

Ursache: [Root-Cause in einem Satz]
Fix: [Was geaendert wurde]
Test: [Wie verifiziert]
```

---

## PyQt6 / GUI Debugging — Haeufige Fallen

> Diese Sektion ist relevant fuer Desktop-GUI-Projekte mit PyQt6/PySide6.

### Top 5 PyQt6 Traps

| Trap | Problem | Loesung |
|------|---------|---------|
| **Signal-Slot Disconnect** | Signal connected aber Handler laeuft nicht | `print` in Handler, Signature pruefen |
| **Thread-Safety** | GUI-Update aus Worker-Thread | `QMetaObject.invokeMethod` oder Signal nutzen |
| **Layout-Cascade** | Widget unsichtbar/falsch platziert | `widget.show()`, Layout-Hierarchie pruefen |
| **Event-Loop Block** | GUI friert ein | Langzeit-Ops in QThread auslagern |
| **Garbage Collection** | Widget verschwindet ploetzlich | Referenz als `self.widget` halten |

### PyQt6 Debug-Helfer

```python
# Widget-Hierarchie ausgeben
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Signal-Debugging
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## Quick Reference

```
BUG GEFUNDEN?
     │
     ▼
[Phase 1: Schnell-Checks]  ──── Offensichtlich? → FIX
     │
     ▼
[Phase 2: Diagnose]  ────────── Ursache klar? → Phase 4
     │
     ▼
[Phase 3: Isolierter Test]  ── Reproduzierbar? → Phase 4
     │                              │
     │                         Nicht reproduzierbar?
     │                              │
     │                         Logging einbauen,
     │                         auf erneutes Auftreten warten
     ▼
[Phase 4: Fix]  ─────────────── Minimal + verstanden
     │
     ▼
[Phase 5: Verifikation]  ────── Tests gruen? → Phase 6
     │                              │
     │                         Tests rot? → Zurueck zu Phase 4
     ▼
[Phase 6: Dokumentation]  ───── Bug-Report + Commit
```

### 20-Minuten-Regel

Wenn du nach 20 Minuten festhaengst:

1. **Ansatz wechseln** — Andere Debugging-Technik probieren
2. **Rubber Duck** — Problem laut erklaeren (oder aufschreiben)
3. **Pause** — 5 Minuten weggehen, dann mit frischem Blick
4. **Hilfe holen** — Kollege fragen, Stack Overflow, Dokumentation
5. **Zuruecksetzen** — `git stash`, komplett neu anfangen
