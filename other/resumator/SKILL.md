---
name: resumator
description: >-
  Multi-source document analysis platform generating structured reports with 
  configurable detail levels. Supports 7 content types (meeting, study, watch, 
  training, comparison, technical, audit) and 5 detail levels (flash to exhaustive).
  Features automatic web enrichment, Perplexity-style source tracking, and 
  anti-hallucination safeguards. Use when processing meeting transcriptions, 
  conducting thematic research, summarizing articles, comparing solutions, 
  creating technical documentation, or user says "résumé", "étude", "CR", 
  "transcription", "compte-rendu", "veille", "comparatif", "audit", "analyse".
  Not for audio transcription, translation, agenda generation, or video content.
---

# Resumator v3.0 — Multi-Source Analysis Platform

## Overview

Resumator transforms raw content (transcriptions, articles, documents, URLs) into structured, exhaustive reports. It supports **7 content types** and **5 detail levels**, with optional web enrichment and strict source traceability.

**Core principle**: Zero hallucination — every claim is sourced or marked uncertain.

## Quick Start

```
1. User provides source(s)
2. Resumator asks: Type? Level?
3. User responds (e.g., "b5" for Study/Exhaustive)
4. Resumator processes and generates report
```

## Workflow

### Step 1: Receive Sources

Accept any combination of:
- Meeting transcripts (with speaker names)
- YouTube transcripts (with timecodes)
- URLs (articles, documentation)
- PDFs / uploaded documents
- Raw notes

### Step 2: Configuration Questionnaire (ALWAYS ASK)

After receiving sources, ALWAYS present:

```
📊 Resumator v3 — Configuration

1️⃣ Type de traitement ?
   a. 📋 Réunion — Compte-rendu structuré
   b. 🔬 Étude — Recherche approfondie  
   c. 📰 Veille — Synthèse d'actualités
   d. 📖 Formation — Extraction pédagogique
   e. ⚖️ Comparatif — Analyse comparative
   f. 🔧 Technique — Documentation tech
   g. 📊 Audit — Analyse critique

2️⃣ Niveau de détail ? (1-5)
   1. ⚡ Flash — TL;DR en 5 lignes
   2. 📋 Résumé — Points clés (~500-800 mots)
   3. 📊 Détaillé — Analyse complète (~1500-2500 mots)
   4. 📚 Approfondi — + contexte (~3000-5000 mots)
   5. 🔬 Exhaustif — Recherche maximale (5000+ mots)

💡 Raccourci : tape "a3" pour Réunion/Détaillé ou "b5" pour Étude/Exhaustive
```

→ See [questionnaire.md](references/questionnaire.md) for shortcuts and defaults

### Step 3: Process Based on Type

| Type | Web Search | Template |
|------|------------|----------|
| 📋 Réunion | Only if level ≥4 | [reunion.md](references/templates/reunion.md) |
| 🔬 Étude | Yes (exhaustive) | [etude.md](references/templates/etude.md) |
| 📰 Veille | Yes (news focus) | [veille.md](references/templates/veille.md) |
| 📖 Formation | If level ≥4 | [formation.md](references/templates/formation.md) |
| ⚖️ Comparatif | Yes (alternatives) | [comparatif.md](references/templates/comparatif.md) |
| 🔧 Technique | Yes (docs) | [technique.md](references/templates/technique.md) |
| 📊 Audit | If level ≥4 | [audit.md](references/templates/audit.md) |

→ See [niveaux-detail.md](references/niveaux-detail.md) for level specifications

### Step 4: For Types Requiring Web Search

Execute research workflow:
1. Extract themes and gaps from sources
2. Generate search plan (5-7 axes)
3. Execute searches iteratively
4. Evaluate source reliability (1-5 ⭐)
5. Fetch and extract relevant content
6. Cross-check contradictions

→ See [workflow-recherche.md](references/workflow-recherche.md) for full process

### Step 5: Integrate Multiple Sources

When multiple sources provided:
1. Normalize each source to common structure
2. Build thematic cross-index
3. Detect contradictions
4. Merge with full traceability

→ See [integration-sources.md](references/integration-sources.md) for fusion rules

### Step 6: Generate Report

1. Use appropriate template for selected type
2. Apply detail level constraints
3. Include source citations [N] and [🌐N]
4. Add confidence scores where relevant
5. Output as downloadable `.md` file

**File naming**: `[TYPE]_[YYYY-MM-DD]_[slug].md`
- CR_2025-01-13_reunion-gardel.md
- ETUDE_2025-01-13_claude-code.md

---

## Critical Rules

### 🔴 CRITICAL (Never Violate)

1. **QUESTIONNAIRE**: ALWAYS ask type + level before processing
2. **ANTI-HALLUCINATION**: Every claim has source [N]/[🌐N] or marked "⚠️ non vérifié"
3. **EXHAUSTIVITY**: Every action/decision/commitment mentioned MUST be captured
4. **FIDELITY**: Never invent. If uncertain → "à confirmer" or "non spécifié"
5. **TRACEABILITY**: Web enrichments marked with 🌐, skill additions with ⚠️
6. **LANGUAGE**: Output in same language as input

### 🟡 IMPORTANT

7. **TL;DR FIRST**: Even level 5, executive summary at top (mandatory)
8. **SOURCE PRIORITY**: Primary > Recent > Secondary
9. **CONTRADICTIONS**: Document both sides, don't arbitrarily choose
10. **PROGRESS FEEDBACK**: For long processing, show progress updates
11. **DIAGRAMS**: Auto-detect flows → Mermaid (max 6 per report)

### 🟢 DESIRABLE

12. **GLOSSARY**: Extract acronyms and technical terms
13. **RELATED TOPICS**: Suggest areas for further exploration
14. **KEY QUOTES**: Preserve impactful verbatims

→ See [anti-hallucination.md](references/anti-hallucination.md) for detailed rules

---

## Source Traceability (Perplexity-style)

### Inline Citations
```
Claude Code allows terminal-based task delegation [1]. 
It supports slash commands for navigation [2][🌐1].
```

### Bibliography Section
```
## 📖 Sources
### Fournies
[1] Transcript YouTube "Claude Code Tutorial" — 03:45
[2] Documentation PDF — page 12

### Recherches web
[🌐1] docs.anthropic.com — "Slash commands reference"
[🌐2] blog.anthropic.com — "Claude Code announcement"

### Non retenues
- oldsite.com — Obsolète (2022)
```

### Reliability Scores
| Score | Meaning |
|-------|---------|
| ⭐⭐⭐⭐⭐ | Official docs, primary sources |
| ⭐⭐⭐⭐ | Recognized tech media, verified experts |
| ⭐⭐⭐ | Community (SO, Reddit with arguments) |
| ⭐⭐ | Unsourced blogs, undated |
| ⭐ | Obsolete, unreliable → excluded |

---

## Meeting Mode (📋 Réunion) — Preserved from v2

For backward compatibility, meeting reports retain v2 structure:

### Meeting Type Detection
| Type | Indicators |
|------|------------|
| Steering/Decision | "décision", "valider", budget, deadlines |
| Information | "informer", "présenter", updates |
| Brainstorming | "idées", "explorer", creative |
| Technical | "architecture", "API", technical terms |
| Generic | No clear indicators → neutral plan |

### Action Status Indicators
| Indicator | Meaning |
|-----------|---------|
| 🟢 | Owner AND deadline defined |
| 🟡 | Owner OR deadline (one missing) |
| 🔴 | Neither owner nor deadline |

→ See [templates/reunion.md](references/templates/reunion.md) for full template
→ See [legacy/mermaid-detection.md](references/legacy/mermaid-detection.md) for diagrams
→ See [legacy/proactive-rules.md](references/legacy/proactive-rules.md) for insights
→ See [legacy/glossary-extraction.md](references/legacy/glossary-extraction.md) for glossary

---

## User Options

| Option | Effect |
|--------|--------|
| `--no-web` | Disable web search |
| `--no-diagrams` | Disable Mermaid generation |
| `--no-glossary` | Disable glossary extraction |
| `--max-diagrams N` | Limit diagram count (default: 6) |

Note: Options can be stated naturally ("sans recherche web", "pas de diagrammes")

---

## Knowledge Base

### Configuration
- [Questionnaire](references/questionnaire.md) — Questions and shortcuts
- [Detail Levels](references/niveaux-detail.md) — 5 levels specification

### Workflows
- [Web Research](references/workflow-recherche.md) — Exhaustive search process
- [Source Integration](references/integration-sources.md) — Multi-source fusion
- [Anti-Hallucination](references/anti-hallucination.md) — Traceability rules

### Templates (7 types)
- [Réunion](references/templates/reunion.md) — Meeting reports
- [Étude](references/templates/etude.md) — Thematic research
- [Veille](references/templates/veille.md) — News watch
- [Formation](references/templates/formation.md) — Training extraction
- [Comparatif](references/templates/comparatif.md) — Comparative analysis
- [Technique](references/templates/technique.md) — Technical documentation
- [Audit](references/templates/audit.md) — Critical analysis

### Legacy (from v2)
- [Mermaid Detection](references/legacy/mermaid-detection.md)
- [Proactive Rules](references/legacy/proactive-rules.md)
- [Glossary Extraction](references/legacy/glossary-extraction.md)

---

## Limitations

This skill does NOT:
- Perform audio transcription (speech-to-text)
- Translate content
- Generate meeting agendas
- Process video content directly
- Generate more than 6 diagrams per report
- Access paywalled content

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-10 | Initial release |
| 2.0.0 | 2025-12-16 | Added: Mermaid diagrams, proactive insights, glossary, action indicators |
| 3.0.0 | 2025-01-13 | Added: 7 content types, 5 detail levels, questionnaire, web research, multi-source integration, anti-hallucination, Perplexity-style citations |

## Current: v3.0.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
