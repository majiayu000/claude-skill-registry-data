---
name: code-promptor
description: >-
  Transform audio transcriptions or raw text into structured development briefs with 
  intelligent multi-task detection. Supports session mode for batch processing independent 
  briefs, auto-generates implementation plans with subtasks, and exports directly to Notion. 
  Features 3 complexity levels (quick fix, standard, major) with adaptive detail. 
  Use when processing voice memos, dictated specifications, "promptor session", "batch promptor", 
  or structuring project notes into actionable tasks. 
  Not for email writing (use corrector), meeting minutes (use resumator), or executing code.
---

# Code-Promptor — Transcript to Development Brief

## Overview

Code-Promptor transforms raw audio transcriptions or unstructured text into clean, professional development briefs. Version 2.1 adds **session mode** for batch processing, **multi-task detection**, and **direct Notion integration**.

**Core Principle**: Faithful extraction, never invention. Generate actionable briefs with intelligent subtask suggestions.

**Language**: Output matches input language. Mixed input defaults to French structure with English technical terms preserved.

## Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    How is Promptor activated?                    │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   SINGLE MODE         │       │   SESSION MODE        │
│   "promptor" + input  │       │   "promptor session"  │
└───────────┬───────────┘       └───────────┬───────────┘
            │                               │
            ▼                               ▼
    Process one dictation           Init session + project
    Full workflow                   → Each input isolated
                                    → Multi-task detection
                                    → Direct Notion export
```

## Session Mode

### Activation Triggers

- `promptor session` / `session promptor`
- `mode série promptor` / `batch promptor`

### Session Workflow

```
1. INIT: User activates session
   → Ask for Notion project (optional)
   → Confirm session active

2. DICTATION RECEIVED:
   → Clean voice artifacts
   → Detect mono vs multi-task
   → If multi: show checkpoint for validation
   → Generate brief(s)
   → Export to Notion
   → Reset context for next dictation

3. END: "fin session" or topic change
   → Show summary with all created tasks
```

### Session Commands

| Command | Action |
|---------|--------|
| `projet [nom]` | Change project mid-session |
| `status` | Show session state |
| `fin session` | End and show summary |

→ See [Session Init Message](templates/checkpoint-format.md#session-init)

## Multi-Task Detection

### Mode: AGGRESSIVE

The skill tends toward detecting multiple tasks. User can merge if needed.

### Detection Algorithm

1. **Clean** dictation (keep rupture markers)
2. **Segment** on explicit/implicit markers
3. **Score** each segment for independence
4. **Decide**: ≥2 segments with score ≥40 → MULTI-TASK

### Rupture Markers

| Type | Markers | Points |
|------|---------|--------|
| Explicit | "aussi", "et puis", "autre chose", "ah et", "sinon" | +30 |
| Implicit | Domain change, subject change | +15-25 |

### Independence Score

```
SCORE = SUBJECT_DIFF×25 + ACTION_DIFF×20 + DOMAIN_DIFF×25 + MARKERS
```

→ See [Multi-Task Detection](references/multi-task-detection.md) for full algorithm

## Checkpoint Validation

When multi-task detected, show validation checkpoint:

```
📋 **N tâches détectées**

┌───┬─────────────────────────┬──────────┬────────────┬───────┐
│ # │ Titre suggéré           │ Type     │ Complexité │ Temps │
├───┼─────────────────────────┼──────────┼────────────┼───────┤
│ 1 │ [Title]                 │ [Type]   │ [Level]    │ [Est] │
└───┴─────────────────────────┴──────────┴────────────┴───────┘

📝 Segments extraits: [show source segments]

📖 Commandes:
   ok          Générer tous les briefs
   ok 1,2      Sélection partielle
   merge 1,2   Fusionner
   edit N "x"  Modifier titre
   drop N      Supprimer
   split N     Découper
   reanalyze   Relancer détection
```

→ See [Checkpoint Format](templates/checkpoint-format.md) for full template

## Complexity Levels

| Level | Criteria | Time | Plan |
|-------|----------|------|------|
| **Quick fix** | <50 words, corrective verb | 1h | ❌ |
| **Standard** | 50-200 words, clear scope | 4h | ✅ |
| **Major** | >200 words, multi-component | 8h | ✅ Detailed |

→ See [Output Format](references/output-format.md) for templates per level

## Brief Structure

### Common Elements (all levels)

```markdown
# [Action Verb] + [Object] — Notion-ready title

📦 **[Complexity]** | ⏱️ [Time] | 🎯 Confidence: [Level]

## Objectif
[2-4 sentences]

## Description  
[Context and functioning]

## Exigences fonctionnelles
- [FR list]
```

### Standard/Major additions

```markdown
## Plan d'implémentation

1. **[Phase 1]**
   - [ ] Subtask auto-generated
   - [ ] Subtask auto-generated

2. **[Phase 2]**
   - [ ] Subtask auto-generated
```

→ See [Subtask Templates](references/subtask-templates.md) for generation rules

## Notion Integration

### Properties Filled

| Property | Source |
|----------|--------|
| Nom | Brief title |
| Description | Brief content |
| Type | Auto-detected |
| Temps estimé | Based on complexity |
| Projet | Session init |

### Type Mapping

| Detection | Notion Type |
|-----------|-------------|
| Bug, fix, corriger | Bloquant |
| Feature, créer | Evolution |
| Refacto, generic | Tache |
| Backend specific | Backend |
| Frontend specific | Frontend |

→ See [Type Mapping](references/type-mapping.md) for full rules

### Error Handling

If Notion API fails:
1. Display complete brief in text
2. Show error message
3. Offer retry option

## Additional Commands

| Command | Usage |
|---------|-------|
| `ref [n]` | Reference task n (creates dependency) |
| `--no-plan` | Disable subtask generation |
| `--no-estimate` | Disable time estimation |

## Critical Rules

1. **Never ask questions** — Produce brief with available info
2. **Never invent requirements** — Mark absent if not mentioned
3. **Never reference source** — Brief is self-contained
4. **Each dictation = isolated context** — No pollution between inputs
5. **Later wins** — Last stated version overrides earlier

## Knowledge Base

### References
- [Output Format](references/output-format.md) — 3 brief templates
- [Multi-Task Detection](references/multi-task-detection.md) — Detection algorithm
- [Subtask Templates](references/subtask-templates.md) — Auto-generation rules
- [Type Mapping](references/type-mapping.md) — Notion type mapping
- [Processing Rules](references/processing-rules.md) — Extraction methodology
- [Voice Cleaning](references/voice-cleaning.md) — Dictation cleanup

### Config
- [Notion IDs](config/notion-ids.md) — Database configuration
- [Projects Cache](config/projects-cache.md) — Project name resolution

### Templates
- [Checkpoint Format](templates/checkpoint-format.md) — Validation display
- [Brief Quick Fix](templates/brief-quickfix.md)
- [Brief Standard](templates/brief-standard.md)
- [Brief Major](templates/brief-major.md)

## Limitations

This skill does NOT:
- Ask clarifying questions (produces with available info)
- Execute development tasks (pre-processor only)
- Modify existing Notion tasks
- Handle bulk imports from files
- Work on already-structured documents

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-12 | Initial Claude skill (from GPT migration) |
| 2.1.0 | 2025-12-31 | Session mode, multi-task detection, Notion integration, subtask generation |

## Current: v2.1.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
