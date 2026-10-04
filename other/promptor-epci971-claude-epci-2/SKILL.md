---
name: promptor
description: >-
  Transform voice dictations or raw text into structured development briefs with
  intelligent multi-task detection. Supports session mode for batch processing,
  auto-generates implementation plans with subtasks, and exports directly to Notion
  via MCP. Features 3 complexity levels (quick fix 1h, standard 4h, major 8h).
  Use when: processing voice memos, dictated specifications, "promptor session",
  structuring project notes into actionable Notion tasks.
  Not for: email writing, meeting minutes, executing code, EPCI workflow tasks.
allowed-tools: [Read, Glob, Grep, Write, Bash]
---

# Promptor — Dictation to Notion Tasks

## Overview

Promptor transforms raw voice dictations or unstructured text into clean, professional
development briefs and exports them directly to Notion. Standalone tool, independent
from EPCI workflow.

**Core Principle**: Faithful extraction, never invention. Generate actionable briefs
with intelligent subtask suggestions.

**Language**: Output matches input language. Mixed input defaults to French structure
with English technical terms preserved.

## Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    How is Promptor activated?                    │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│   ONE-SHOT MODE       │       │   SESSION MODE        │
│  /promptor [input]    │       │  /promptor session    │
└───────────┬───────────┘       └───────────┬───────────┘
            │                               │
            ▼                               ▼
    Process one dictation           Init session + project
    Generate brief(s)               → Each input isolated
    Export to Notion                → Multi-task detection
    Done                            → Direct Notion export
                                    → "fin session" to end
```

## Configuration

| Element | Value |
|---------|-------|
| **Thinking** | `think` (default) |
| **Skills** | promptor (self) |
| **Notion** | API directe via Bash/curl |

### Notion Configuration

Read from `.claude/settings.local.json`:

```json
{
  "notion": {
    "token": "ntn_xxx",
    "tasks_database_id": "xxx",
    "default_project_id": "xxx"
  }
}
```

### ⚠️ Validation Stricte Projet (MANDATORY)

> **CRITICAL**: Le projet est OBLIGATOIRE pour l'export Notion. Pas de fallback silencieux.

**Au démarrage de session ou one-shot :**

```
1. Lire .claude/settings.local.json
2. Vérifier présence des 3 champs notion:
   ├─ token         → ERREUR si absent/vide
   ├─ tasks_database_id → ERREUR si absent/vide
   └─ default_project_id → ERREUR si absent/vide (MANDATORY)
3. Si validation échoue:
   └─ STOP avec message explicite (pas de fallback)
```

**Messages d'erreur :**

| Champ manquant | Message |
|----------------|---------|
| `token` | ⛔ Config Notion manquante: token requis dans .claude/settings.local.json |
| `tasks_database_id` | ⛔ Config Notion manquante: tasks_database_id requis |
| `default_project_id` | ⛔ **Projet non configuré** - Ajouter default_project_id dans settings.local.json |

**Comportement :**
- ❌ **INTERDIT** : Export sans projet → tâche orpheline
- ❌ **INTERDIT** : Fallback silencieux vers affichage texte si projet manquant
- ✅ **REQUIS** : Bloquer et demander configuration avant export

**Validation script :**
```bash
python src/scripts/validate_notion_config.py
```

## Session Mode

### Activation

- `/promptor session`

### Session Workflow

```
1. INIT: User activates session
   → Read Notion config from settings.local.json
   → Confirm session active

2. DICTATION RECEIVED:
   → Clean voice artifacts
   → Detect mono vs multi-task
   → If multi: show checkpoint for validation
   → Generate brief(s)
   → Export to Notion (if configured)
   → Reset context for next dictation

3. END: "fin session"
   → Show summary with all created tasks
```

### Session Commands

| Command | Action |
|---------|--------|
| `status` | Show session state |
| `fin session` | End and show summary |

→ See [Checkpoint Format](templates/checkpoint-format.md)

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

→ See [Multi-Task Detection](references/multi-task-detection.md)

## Checkpoint Validation

When multi-task detected, show validation checkpoint:

```
📋 **N tâches détectées**

┌───┬─────────────────────────┬──────────┬────────────┬───────┐
│ # │ Titre suggéré           │ Type     │ Complexité │ Temps │
├───┼─────────────────────────┼──────────┼────────────┼───────┤
│ 1 │ [Title]                 │ [Type]   │ [Level]    │ [Est] │
└───┴─────────────────────────┴──────────┴────────────┴───────┘

📖 Commandes: ok | ok 1,2 | merge 1,2 | edit N "x" | drop N
```

→ See [Checkpoint Format](templates/checkpoint-format.md)

## Complexity Levels

| Level | Criteria | Time | Plan |
|-------|----------|------|------|
| **Quick fix** | <50 words, corrective verb | 1h | No |
| **Standard** | 50-200 words, clear scope | 4h | Yes |
| **Major** | >200 words, multi-component | 8h | Yes (detailed) |

→ See [Output Format](references/output-format.md)

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
```

→ See [Subtask Templates](references/subtask-templates.md)

## Notion Integration

### API Direct (via Bash/curl)

> **Note**: Uses direct Notion API instead of MCP due to serialization bug.

Export to Notion via `curl` command in Bash tool:

```bash
curl -s -X POST 'https://api.notion.com/v1/pages' \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Notion-Version: 2022-06-28' \
  -d "$JSON_PAYLOAD"
```

Configuration read from `.claude/settings.local.json`:
- `notion.token` — Bearer token
- `notion.tasks_database_id` — Target database
- `notion.default_project_id` — Project relation

### Schema Auto-Discovery

> **IMPORTANT**: Before creating pages, fetch and cache the database schema to use correct property types.

```
1. Check cache: .project-memory/cache/notion-schema.json
2. If missing/stale (>24h): Fetch schema from Notion API
3. Use cached schema to format properties correctly
4. On 400 error: Refresh schema and retry once
```

This prevents errors like `"Type is expected to be multi_select"` by dynamically
detecting property types instead of hardcoding them.

→ See [Schema Cache](references/schema-cache.md) for implementation details.

### Properties Filled

| Property | Source | Default |
|----------|--------|---------|
| `Nom` | Brief title | - |
| `Description` | Brief content (markdown) | - |
| `Type` | Auto-detected | "Tache" |
| `Temps estimé` | Complexity (1/4/8) | 4 |
| `État` | Fixed | "En attente" |
| `DAY` | Fixed | "BACKLOG" |
| `Projet` | Config default | From settings |

### Type Mapping

| Detection | Notion Type |
|-----------|-------------|
| Bug, fix, corriger | Bloquant |
| Feature, créer | Evolution |
| Backend (API, service) | Backend |
| Frontend (UI, composant) | Frontend |
| Default | Tache |

→ See [Type Mapping](references/type-mapping.md)

### Fallback (API Error Only)

> **Note**: Fallback s'applique UNIQUEMENT aux erreurs API, PAS à la config manquante.

**Config manquante → STOP (voir Validation Stricte Projet)**

**Erreur API Notion (après validation config OK) :**
1. Display complete brief as text
2. Show message: "⚠️ Erreur API Notion — Brief affiché pour copie manuelle"
3. Afficher le brief complet formaté
4. Log l'erreur pour diagnostic

## Critical Rules

1. **Never ask questions** — Produce brief with available info
2. **Never invent requirements** — Mark absent if not mentioned
3. **Never reference source** — Brief is self-contained
4. **Each dictation = isolated context** — No pollution between inputs
5. **Later wins** — Last stated version overrides earlier

## Knowledge Base

### References
- [Multi-Task Detection](references/multi-task-detection.md) — Detection algorithm
- [Output Format](references/output-format.md) — 3 brief templates
- [Voice Cleaning](references/voice-cleaning.md) — Dictation cleanup
- [Subtask Templates](references/subtask-templates.md) — Auto-generation rules
- [Processing Rules](references/processing-rules.md) — Extraction methodology
- [Type Mapping](references/type-mapping.md) — Notion type detection
- [Schema Cache](references/schema-cache.md) — Notion schema auto-discovery

### Config
- [Notion Config](config/notion-config.md) — Database configuration

### Templates
- [Checkpoint Format](templates/checkpoint-format.md) — Validation display
- [Brief Quick Fix](templates/brief-quickfix.md) — 1h template
- [Brief Standard](templates/brief-standard.md) — 4h template
- [Brief Major](templates/brief-major.md) — 8h template

## Limitations

This skill does NOT:
- Ask clarifying questions (produces with available info)
- Execute development tasks (brief generator only)
- Modify existing Notion tasks
- Integrate with EPCI workflow (/brief, /epci)

## Version

- **Current**: v1.0.0 (Claude Code)
- **Based on**: code-promptor v2.1.0 (web)
