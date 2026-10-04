---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Standard procedure for onboarding new software projects: Feature analysis, code quality review, onboarding checklist, and task creation."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="project-onboarding banner">

# Standardaufnahmeverfahren fuer neue Software-Projekte

**Version:** 1.0
**Stand:** 2026-03-12

---

## Uebersicht

Dieses Verfahren definiert, welche Schritte bei neu entdeckten Software-Ordnern durchzufuehren sind, bevor sie in ein Task-Management-System aufgenommen werden.

```
┌─────────────────────────────────────────────────────────┐
│           STANDARDAUFNAHMEVERFAHREN                     │
├─────────────────────────────────────────────────────────┤
│  1. Feature-Analyse erstellen                           │
│  2. Code-Qualitaetspruefung (Standard-Tests)            │
│  3. AUFGABEN.txt erstellen                              │
│  4. In Task-Management uebernehmen                      │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Feature-Analyse

**Zweck:** Verstaendnis des Tools, seiner Funktionen und des Entwicklungsstandes.

**Datei erstellen:** `Feature_Analyse_<ToolName>.md`

### Template

```markdown
# Feature-Analyse: <ToolName>

## Kurzbeschreibung
Ein kurzer Satz der beschreibt was das Tool macht.

---

## Highlights

| Feature | Beschreibung |
|---------|-------------|
| **Feature 1** | Beschreibung |
| **Feature 2** | Beschreibung |

---

## Bewertung der Ausbaustufe

### Aktueller Stand: **<Status> (<X>%)**

Moegliche Status:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Kategorie | Bewertung (1-5) | Details |
|-----------|:---------------:|---------|
| **Funktionsumfang** | 3 | |
| **UI/UX** | 3 | |
| **Stabilitaet** | 3 | |
| **Dokumentation** | 3 | |

---

## Empfohlene Erweiterungen

### Prioritaet: Hoch
1. ...

### Prioritaet: Mittel
2. ...

### Prioritaet: Niedrig
3. ...

---

## Technische Details

Framework:      <Framework>
Dateigroesse:   <X> Zeilen Python
Hauptdatei:     <main.py>

---
*Analyse erstellt: <Datum>*
```

---

## Phase 2: Code-Qualitaetspruefung

**Zweck:** Technische Qualitaet sicherstellen, bekannte Probleme identifizieren.

### Empfohlene Pruefungen

| Test | Werkzeug | Beschreibung |
|------|----------|--------------|
| **Encoding** | Encoding-Checker (z.B. `chardet`, `file`) | UTF-8 sicherstellen |
| **Methoden-Analyse** | Linter (z.B. `pylint`, `flake8`) | Grosse Methoden finden |
| **Einrueckung** | Formatter (z.B. `black`, `autopep8`) | Konsistenz pruefen |
| **Imports** | Import-Checker (z.B. `isort`, `pylint`) | Unused Imports finden |

### Pruefpunkte

- [ ] Alle .py Dateien UTF-8 kodiert?
- [ ] Keine ungewoehnlich grosse Methoden (>100 Zeilen)?
- [ ] Konsistente Einrueckung (Spaces vs Tabs)?
- [ ] Unused Imports entfernt?
- [ ] Docstrings vorhanden?

### Ergebnis dokumentieren

Probleme in AUFGABEN.txt unter "QUALITAETSPRUEFUNG" eintragen.

---

## Phase 3: AUFGABEN.txt erstellen

**Zweck:** Offene Aufgaben strukturiert erfassen.

**Datei erstellen:** `AUFGABEN.txt` im Projektordner

### Template

```
AUFGABEN - <ToolName> V<Version>
==============================
Status: <Status>
Stand: <Datum>

OFFENE AUFGABEN:
[ ] <Aufgabe 1> - Aufwand: <NIEDRIG|MITTEL|HOCH>
[ ] <Aufgabe 2> - Aufwand: <NIEDRIG|MITTEL|HOCH>

---
ERLEDIGT (Archiv):
- <Erledigte Aufgabe> (<Version>, <Datum>)
```

### Status-Werte

| Status | Bedeutung |
|--------|-----------|
| NEU ENTDECKT | Noch nicht analysiert |
| ANALYSE NOETIG | Feature-Analyse laeuft |
| QUALITAETSPRUEFUNG | Code-Tests laufen |
| VALIDIERT & BEREIT | Bereit fuer Features |
| MVP | Minimum Viable Product |
| NUR KOMPILIEREN | Nur noch Kompilierung noetig |
| GESPERRT | Wartet auf User-Test/Entscheidung |

---

## Phase 4: Task-Management-Integration

Nach Abschluss der Phasen 1-3:

1. **Aufgaben uebertragen:** AUFGABEN.txt-Eintraege als Tasks/Issues anlegen
2. **Pruefen:** Alle Aufgaben korrekt kategorisiert?
3. **Kategorisierung:** Projekt in passende Kategorie einordnen (Single-Tool, Suite, Library etc.)

### Automatische Onboarding-Tasks

Bei neuen Projekten folgende Standard-Tasks anlegen:

| Task | Aufgabe | Aufwand |
|------|---------|---------|
| onb_1 | Feature-Analyse erstellen | mittel |
| onb_2 | Code-Qualitaetspruefung | niedrig |
| onb_3 | AUFGABEN.txt erstellen | niedrig |

Tasks haben Abhaengigkeiten: onb_2 haengt von onb_1 ab, onb_3 haengt von onb_2 ab.

---

## Schnell-Checkliste

```
[ ] 1. Feature_Analyse_<Name>.md erstellt
[ ] 2. Code-Qualitaetspruefung durchgefuehrt (Linter, Encoding, Imports)
[ ] 3. AUFGABEN.txt erstellt mit Status
[ ] 4. Tasks in Task-Management uebernommen
```

---

## Beispiel: Neues Tool "MyTool"

```bash
# 1. Feature-Analyse
# -> Feature_Analyse_MyTool.md erstellen (siehe Template)

# 2. Code-Qualitaet
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Encoding pruefen

# 3. AUFGABEN.txt
# -> Im Tool-Ordner erstellen mit Status "QUALITAETSPRUEFUNG"

# 4. Tasks anlegen
# -> Eintraege aus AUFGABEN.txt als Issues/Tickets erfassen
```

---

*Erstellt: 2026-01-10 | Portiert: 2026-03-12*
