---
name: brain-operating-system
description: Quick reference for operating within jonmagic's second-brain workspace. Use when working with files in the brain repository—provides directory structure, naming conventions, append-only norms, wikilink patterns, and file organization rules. Essential for understanding where to create files, how to name them, and how to maintain continuity with existing structures.
---

# Brain Operating System

Navigation guide for jonmagic's second-brain workspace covering directory intents, naming conventions, and operational norms.

## Directory Map

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `Daily Projects/YYYY-MM-DD/` | Day-level focus logs, scratch pads, context files | Start new execution work here. Append to existing date folders rather than creating duplicates. |
| `Weekly Notes/YYYY-MM-DD/` | Planning, goals, schedules, backlinks to meeting notes | Anchor for weekly rituals. New headings at top (newest first). |
| `Snippets/YYYY-MM-DD-to-YYYY-MM-DD.md` | Weekly accomplishment summaries (Ships, Collabs, Risks, etc.) | Primary feed for retros and exec updates. Maintain existing section headers. |
| `Executive Summaries/YYYY-MM-DD/` | Distilled updates for leadership | Keep concise (1–2 pages). Reference snippets and priorities. |
| `Meeting Notes/<team-or-person>.md` | Rolling notes with `## YYYY-MM-DD` sections | Link to transcripts/summaries via wikilinks. New dates append at top. |
| `Projects/<slug>/` | Multi-week initiatives | Use README-like overviews, milestone logs, resource links. |
| `Archive/YYYY-MM-DD/` | Cold-storage for inactive artifacts | Only move files once captured elsewhere. |

Other directories (`Feedback/`, `Transcripts/`, `Templates/`, etc.) follow similar patterns—check existing files before adding content.

## Naming Conventions

- **Filenames**: lowercase with hyphens (`my-file-name.md`)
- **Date folders**: `YYYY-MM-DD` format
- **Sequential files**: When creating multiple related files in same date folder, use numeric prefixes (`01-new-angle.md`, `02-follow-up.md`)
- **Prefer appending**: Always try to append to existing date folders rather than creating duplicates

## Operational Norms

### Append-Only Discipline

- **Daily Projects, Weekly Notes, Meeting Notes**: Always append new entries at top (reverse-chronological)
- **Context files** (e.g., `snippets-context-*.txt`, `retro-context-*.txt`): Always append to end, never edit middle sections
- **Snippets, Executive Summaries**: Create new files for new time periods

### Wikilink Patterns

Use `[[...]]` wikilinks liberally to connect documents:
- `[[Snippets/2025-11-24-to-2025-11-30]]`
- `[[Projects/spiral-funnel-architecture/README]]`
- `[[Meeting Notes/alice]]`

### Thread Awareness

Before editing any document:
1. Scan the last few entries to understand current state
2. Check for linked documents that provide context
3. Maintain chronological or thematic continuity

### Minimal Duplication

- If concept exists elsewhere, link to it rather than restating
- Use wikilinks to connect related content
- Consolidate learnings into appropriate long-term documents (Weekly Notes, Projects, etc.)

## Workflow Expectations

1. **Start in Daily Projects**: Kick off new work in `Daily Projects/YYYY-MM-DD/`
2. **Propagate learnings**: Copy distilled notes into relevant Weekly Note, Snippet, or Project file
3. **Follow breadcrumbs**: Use wikilinks to trace decision history
4. **Version-friendly**: Use Markdown headings, tables, bullet lists; avoid inline HTML

## File Creation Decision Tree

**Creating a new file?**
1. Is it daily execution work? → `Daily Projects/YYYY-MM-DD/`
2. Is it weekly planning? → `Weekly Notes/YYYY-MM-DD/`
3. Is it accomplishment tracking? → `Snippets/YYYY-MM-DD-to-YYYY-MM-DD.md`
4. Is it a meeting record? → `Meeting Notes/<person-or-team>.md` (append new `## YYYY-MM-DD` section)
5. Is it multi-week scope? → `Projects/<slug>/`
6. Is it feedback? → `Feedback/`
7. Is it a transcript? → `Transcripts/`

**When in doubt**: Start in `Daily Projects/YYYY-MM-DD/` and migrate later if it becomes evergreen.
