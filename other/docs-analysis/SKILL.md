---
name: docs-analysis
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Document requirements analysis: Analyzes concept and requirements documents in the docs/ folder, checks requirements against current code, and creates a consolidated difference report."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="docs-analysis banner">

# Dokumenten-Anforderungsanalyse

> Analysiert alle Konzept- und Anforderungsdokumente, prueft deren Anforderungen gegen den aktuellen Code und erstellt einen konsolidierten Differenz-Bericht.

---

## Zweck

Analysiert alle Konzept- und Anforderungsdokumente im ../docs/ Ordner, prueft deren Anforderungen gegen den aktuellen Code und erstellt einen konsolidierten Differenz-Bericht.

---

## Namenskonvention

### Praefix und Suffix
Alle analysierten Dokumente erhalten:
- **Praefix:** `conN_` wobei N = Analyse-Version (1, 2, 3, ...)
- **Suffix:** `_XX` wobei XX = Erfuellungsgrad in Prozent (gerundet auf 10er)

### Archivierungs-Schwelle
- **>= 75% erfuellt:** Dokument wird nach `../docs/_archive/` verschoben
- **< 75% erfuellt:** Dokument bleibt in `../docs/` mit Praefix/Suffix
- **Schwelle konfigurierbar** (Default: 75)

---

## Ablauf

### Phase 1: Dokumente sammeln
- Liste alle *.md und *.txt Dateien in ../docs/ (root)
- Filtere README.txt aus

### Phase 2: Anforderungen extrahieren
Fuer jedes Dokument:
- Lese Inhalt
- Identifiziere Anforderungen (Checklisten, Tabellen, FEHLT/TODO Marker)
- Kategorisiere: Struktur, Code, API, DB-Schema, CLI, Feature

### Phase 3: Code-Pruefung
Fuer jede Anforderung:
- Bestimme Pruefmethode (Glob, Grep, Read)
- Fuehre Pruefung durch
- Markiere als: ERFUELLT, TEILWEISE, FEHLT

### Phase 4: Bewertung
- Zaehle erfuellte vs. offene Anforderungen
- Berechne Erfuellungsgrad (%)
- Entscheide: archivieren (>= 75%) oder belassen (< 75%)

### Phase 5: Ausgabe generieren
- Erstelle ANFORDERUNGSANALYSE.md (Zusammenfassung)
- Erstelle consense_diff.md (nur offene Anforderungen, nach Prioritaet)

### Phase 6: Versionierung
- Scanne nach hoechstem conN_ Praefix
- Neue Version = hoechste + 1

### Phase 7: Umbenennen und verschieben
- Dokumente mit neuem Praefix/Suffix versehen
- Archivieren oder belassen

---

## Ausgabe

| Datei | Beschreibung |
|-------|--------------|
| `conN_ANFORDERUNGSANALYSE.md` | Vollstaendige Analyse (Version N) |
| `consense_diff_N.md` | Konsolidierte offene Anforderungen |
| `_archive/conN_*_XX.*` | Archivierte (>=75%) Dokumente |

---

## Prioritaets-Klassifizierung

| Prioritaet | Kriterien |
|:----------:|-----------|
| P1 | Kernfunktionalitaet fehlt, System nicht nutzbar |
| P2 | Wichtige Feature fehlt, Workaround moeglich |
| P3 | Nice-to-have, verbessert UX |
| P4 | Kosmetisch, Dokumentation, Code-Qualitaet |

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
