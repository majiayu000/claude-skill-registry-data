---
name: research-agent
version: 0.2.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-08-22
description: Project-first Research pipeline with live gates, source/PDF evidence, claim boundaries, compute and publication controls; includes an optional PubMed/arXiv standard-library helper.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="research-agent banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


# Research Agent (Deutsch)

Diese Fassung ist der zentrale Paketursprung. Innerhalb von
`<OneDrive>/.TOPICS/.RESEARCH` gilt die aktuelle Projekt- und
Research-Pipeline als Autorität; der mitgelieferte PubMed/arXiv-Code ist nur
ein optionales Recherchewerkzeug.

## Verbindliche Autoritätskette

1. Aktueller Nutzerauftrag und globale `AGENTS.md`-/`GPT.md`-/`CLAUDE.md`-
   Regeln.
2. Projektlokale aktuelle Dateien, Livezustand, Locks, Entscheidungen und
   Register. Nummerierte Fortsetzungen und explizite Current-Pointer gehen
   ihren Vorläufern vor; Archive und Konfliktkopien werden nicht stillschweigend
   zur Ersatzautorität.
3. Live-Pipeline im Research-Root: insbesondere `CLAUDE.md`, `START*`,
   `MASTER*`, `POLICY*`, `PUBLIKATIONSVERFAHREN.md`, `QUALITY_RULES*`, aktuelle
   Status-/TODO-Pointer sowie `CHECKS-LOG.txt` und `CHECKS-REG.md`.
4. Dieser Skill und seine generischen Suchskripte.

Zu Beginn sind `~/.codex/GPT.md`, die beiden globalen
`CLAUDE.md`-Dateien, die Research-Regeln und die aktuellen projektlokalen
`KONZEPT*`, Plan-, `TODO*`, `BEWEISNOTIZ*`, Entscheidungs-, Publikations- und
Bibliografiedateien zu lesen. Bei Widersprüchen gilt fail-closed.

## Live-Gates und Mutationen

- Ein aktuelles unlesbares `CHECKS-LOG.txt` ist ein hartes Read-only-Gate.
- Vor Auswahl oder Änderung: `CHECKS-REG.md`, Projektregister,
  Entscheidungen, gegebenenfalls Fable-Plan, Locks, Konfliktkopien und
  Livezustand prüfen.
- BACH/BYUM-Holds und Ablauf ausschließlich mit `fc_get_time` belegen.
- In OneDrive FileCommander für Navigation, Reads, Metadaten, Checksums,
  Cloud-Locks und Ausführung verwenden. Vor Writes eng locken, fremde Locks
  und Änderungen bewahren, am Ende nur den eigenen Lock entfernen.
- Produkt-/Fachentscheidungen, Cooldowns, fehlende kanonische Klone,
  Reproduktionsgates und verbrauchte Einmalfreigaben nicht autonom umgehen.

## Evidenz-, Claim-, Compute- und Publikationsregeln

- Lokale `.WISSEN`-Funde früh nutzen, wissenschaftliche Aussagen danach an
  Primärquellen verifizieren. Satz/Abschnitt/Seite, Voraussetzungen,
  Normalisierung und Objekttyp exakt binden; volatile Abfragen datieren.
- PDFs nur nach `%PDF-`, lesbarer Seitenzahl/Text-Extraktion und SHA-256 als
  Quellen führen. HTML-, CAPTCHA-, 404- und Platzhalterdateien zählen nicht.
- Messung, Langzeitevidenz, Unsicherheit und Forschungsoption trennen; keinen
  Proxy, Preflight, Review oder Teillauf zum wissenschaftlichen Claim
  hochstufen.
- Deutsche End-User-Artefakte verwenden echte Umlaute. EN/DE und nur dann ein
  Kombi-Artefakt prüfen, wenn die aktuelle Pipeline es zulässt: Struktur,
  Bibliografie, Build, Extraktion und Encoding.
- Compute ausschließlich nach live `.COMPUTE`-/Projektvertrag und
  Placement-Regeln. Keine langen Laptopläufe, Retries, Fortsetzungen,
  Queueänderungen oder verbrauchten Einmalläufe ohne ausdrückliche Autorität.
  Timeout/Infrafehler sind kein mathematisches Negativergebnis.
- Upload, Public-Switch, Submit, Registry-Buchung und Release sind getrennte
  User-Gates. Vorbereitung und Dry-Run sind keine Publikation.
- Abschluss erst nach erforderlichen Tests/Builds, Artefakt-Readback,
  Projekt- und Root-Registern, gegebenenfalls Automationsgedächtnis/Handoff
  und Entfernung eigener temporärer Locks. Restgates ausdrücklich nennen.

## Optionaler Literaturhelfer

Die folgenden Python-Module nutzen ausschließlich die Standardbibliothek
(`urllib`, `xml`, `json`). Sie unterstützen Suche und Review, ersetzen aber
keine der obigen Autoritäts- oder Evidenzprüfungen.

## Architecture

```
ResearchAgent (Orchestrator)
  sources/          Data sources (PubMed, arXiv)
    base.py         Article/SearchResult dataclasses, Source ABC
    pubmed.py       NCBI E-utilities (esearch + efetch)
    arxiv.py        arXiv Atom API
  workflows/        Research workflows
    quick_search.py Quick search across multiple sources
    literature_review.py  4-phase literature review
```

## Usage as Python Library

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Quick search (Deutsch)
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Structured literature review (Deutsch)
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "articles found")

# Save result (Deutsch)
agent.save_result(result, "research_ml.md", fmt="markdown")
```

## Usage as CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Data Sources

| Source | API | Rate Limit | Access |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/s (without key), 10/s (with key) | Free |
| arXiv | Atom REST API | None documented | Free |

Extensible: New sources implement the `Source` ABC from `sources/base.py`.

## Extension

```python
from scripts.sources.base import Source, SearchResult

class MySource(Source):
    @property
    def name(self) -> str:
        return "my-source"

    def search(self, query, max_results=10, **kwargs):
        # Implement API query
        ...

    def get_article(self, article_id):
        ...

    def is_available(self) -> bool:
        return True
```

## BACH Notes

> Only relevant when used within BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## Änderungsprotokoll

### 0.2.0 (2026-08-22)
- Projekt- und Pipeline-Autorität vor generischen Suchskripten verankert
- Live-Gates, OneDrive-/Lock-Regeln und Current-Pointer aufgenommen
- Primärquellen-/PDF-Nachweise, Claim-Grenzen und bilinguale Prüfungen ergänzt
- Compute-, Upload-, Register- und Closeout-Gates fail-closed festgeschrieben

### 0.1.0 (2026-03-12)
- Migration from MODULAR_AGENTS/ResearchAgent to skill library
- PubMed + arXiv sources
- QuickSearch + LiteratureReview workflows
