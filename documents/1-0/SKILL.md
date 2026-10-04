---
name: resumator
description: >-
  Generate structured, exhaustive, and actionable meeting minutes from transcriptions, 
  articles, or documents. Extracts participants, decisions, and action items into 
  Notion-compatible Markdown. Use when processing meeting transcriptions, summarizing 
  articles from URLs, or analyzing uploaded PDFs. Triggers on "transcription", "compte-rendu", 
  "meeting", "résumé", "summary", or when long text is pasted. Not for simple text formatting, 
  translation-only tasks, or real-time transcription.
---

# Resumator

## Overview

Resumator transforms raw content (meeting transcriptions, articles, documents) into structured, professional summaries optimized for Notion. Priority is given to **exhaustive action item extraction** — every commitment mentioned must be captured.

## Quick Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│                    What content type?                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ TRANSCRIPTION │   │     URL       │   │   PDF/DOC     │
│ (long text)   │   │   (article)   │   │  (uploaded)   │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
   Detect type         Fetch & analyze      Extract & analyze
   Apply plan          Structured summary   Structured summary
```

## Mode 1: Meeting Transcription (Primary)

**Triggers**: Long text (>500 words), keywords: "transcription", "réunion", "meeting", "CR", "compte-rendu"

### Workflow

1. **Detect meeting type** automatically from content
2. **Apply corresponding plan** (see [meeting-plans.md](references/meeting-plans.md))
3. **Extract all elements**: participants, topics, decisions, actions, concerns
4. **Generate output** using [output-template.md](references/output-template.md)
5. **Output directly** — no intermediate validation

### Meeting Type Detection

| Type | Indicators |
|------|------------|
| Steering/Decision | "décision", "valider", "arbitrer", budget, deadlines |
| Information | "informer", "présenter", announcements, updates |
| Brainstorming | "idées", "propositions", "explorer", creative language |
| Training/Workshop | "formation", "exercice", learning objectives |
| Individual Review | One-on-one, feedback, performance, goals |
| **Generic (fallback)** | No clear indicators → use neutral plan |

## Mode 2: URL Analysis (Secondary)

**Trigger**: URL detected in input

### Workflow

1. Fetch URL content
2. Analyze and identify key points
3. Generate structured summary
4. Apply Notion-compatible Markdown format

## Mode 3: PDF/Document (Secondary)

**Trigger**: PDF file uploaded or mentioned

### Workflow

1. Extract document content
2. Identify document type and structure
3. Generate appropriate summary
4. Apply Notion-compatible Markdown format

## Critical Rules

1. **EXHAUSTIVITY ON ACTIONS**: Every task, commitment, or assignment mentioned MUST appear in the action items table. This is the highest priority.

2. **FIDELITY**: Never invent information. If uncertain, use "à confirmer" or "non précisé".

3. **DIRECT OUTPUT**: Generate the summary immediately. Do not ask for format preferences unless explicitly requested.

4. **FLEXIBILITY**: Adapt the plan to actual content. Skip empty sections. Add relevant sections if content warrants.

5. **LANGUAGE**: Output in the same language as the input (French by default).

6. **NOTION-READY**: All output must be clean Markdown, copy-paste ready for Notion.

## Output Structure

See [output-template.md](references/output-template.md) for complete template.

**Key sections**:
- 🎯 Executive Summary (3-5 bullet points)
- 📌 Context
- 💬 Topics Discussed
- ✅ Decisions Made
- 📝 Action Items (table: Who / What / When)
- ⚠️ Points of Attention
- ❓ Open Questions
- 💬 Key Quotes (if notable)

## Examples

### Input (Transcription excerpt)

```
Jean: Bon, on doit valider le budget avant vendredi.
Marie: Je m'occupe de finaliser les chiffres avec Thomas.
Jean: Parfait. Et pour le planning, qui s'en charge?
Pierre: Je peux le faire, mais j'ai besoin des specs de Marie.
Marie: Je te les envoie demain matin.
```

### Output (Action Items section)

| Responsable | Action | Échéance |
|-------------|--------|----------|
| Marie | Finaliser les chiffres avec Thomas | - |
| Marie | Envoyer les specs à Pierre | Demain matin |
| Pierre | Préparer le planning | - |
| Équipe | Valider le budget | Vendredi |

## User Options (On Request Only)

| Option | Values | Default |
|--------|--------|---------|
| Length | Concise / Standard / Detailed | Standard |
| Focus | Actions / Decisions / Complete | Complete |
| Action table | Yes / No | Yes |

Only apply if user explicitly requests a different format.

## Knowledge Base

- [Meeting Plans](references/meeting-plans.md) — 6 structured plans by meeting type
- [Output Template](references/output-template.md) — Complete Markdown template

## Limitations

This skill does NOT:
- Perform real-time transcription (audio → text)
- Translate content (focus is summarization)
- Generate meeting agendas (only processes existing content)
- Create presentations from minutes
- Handle video content directly

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-10 | Initial release |

## Current: v1.0.0
