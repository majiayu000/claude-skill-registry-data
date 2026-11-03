---
name: dossier-briefing
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: Generates a structured research briefing for a topic or person as a Markdown scaffold (stdout or file). No persistent store.

tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: de
visibility: public
---
<img src="banner.png" width="100%" alt="dossier-briefing banner">

# Dossier-Briefing

**Strukturiertes Recherche-Briefing zu einem Thema oder einer Person**

---

## Überblick

Erzeugt ein leeres, strukturiertes Markdown-Briefing zu einem beliebigen Thema
(Person, Unternehmen, Ereignis, Konzept). Das Gerüst dient als Ausgangsbasis für
eine anschließende Recherche mit `research-agent` oder `web-reading`.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Erstell ein Briefing zu Marie Curie" | Scaffold: Person, Typ=person |
| „Dossier über OpenAI" | Scaffold: Unternehmen, Typ=organization |
| „Briefing zum Thema Quantencomputing" | Scaffold: Thema, Typ=topic |
| „Bereite ein Recherche-Briefing zu COP30 vor" | Scaffold: Ereignis, Typ=event |

---

## Workflow

1. **Subjekt benennen:** Name/Titel des Briefings aus der Nutzereingabe extrahieren.
2. **Typ erkennen:** person, organization, topic, event (oder unspecified).
3. **Scaffold generieren:** Markdown mit allen relevanten Abschnitten erzeugen.
4. **Ausgabe:** stdout oder optional in eine Datei schreiben (`-o datei.md`).
5. **Recherche starten:** Gerüst an `research-agent` oder `web-reading` übergeben,
   um fehlende Abschnitte zu befüllen.

---

## CLI

```bash
# Briefing zu stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# In Datei schreiben
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Themen-Briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantencomputing" --typ topic

# Ereignis
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Ohne Typ-Angabe (generisch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Mein Thema"

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Briefing-Typen und Abschnitte

| Typ | Abschnitte |
|---|---|
| `person` | Basisdaten, Vita/Hintergrund, Werk & Beiträge, Quellen, Notizen |
| `organization` | Profil, Geschichte, Produkte/Dienste, Schlüsselpersonen, Quellen, Notizen |
| `topic` | Überblick, Hintergrund/Kontext, Aktuelle Entwicklung, Schlüsselquellen, Offene Fragen, Notizen |
| `event` | Eckdaten, Beteiligte, Verlauf/Hintergrund, Bedeutung, Quellen, Notizen |
| `unspecified` | Überblick, Hintergrund, Details, Quellen, Notizen |

---

## Store

Kein persistenter Store. Das Gerüst wird nur ausgegeben (stdout oder Datei),
nicht in einer Datenbank abgelegt.

---

## Haltung

- Immer betonen, dass das Gerüst leer ist und durch Recherche befüllt werden muss.
- Nie Inhalte erfinden oder halluzinieren — nur Struktur liefern.
- Bei unklarem Typ nachfragen oder `unspecified` verwenden.

---

## Datenschutz

Kein Netzwerkzugriff. Kein Store. Rein lokale Verarbeitung.

---

## Verwandte Ressourcen

- `research-agent` — befüllt das Briefing-Gerüst mit Recherche-Ergebnissen
- `web-reading` — liest Webseiten und extrahiert Inhalte für das Briefing

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 1.0.0 | 2026-06-22 | Erstellt aus BACH dossier_generator.py v1.0.0; Store entfernt, verallgemeinert |
