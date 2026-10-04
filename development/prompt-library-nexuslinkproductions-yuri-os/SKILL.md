---
name: prompt-library
description: Query the local Claude Code prompt library (52 official prompts, tagged by SDLC phase, category, and role) when composing task prompts for any lane — orchestrator packets, worker dispatch, or OMP micro-tasks. Filter by phase (discover/design/build/ship/operate), category, or role via prompts.json.
---

# Prompt Library

> Curated Claude Code prompt library — 52 prompts extracted from the official Claude Code Prompt Library page, organized by SDLC phase and category.

## Structure

`prompts.json` — clean JSON array, all 52 entries preserved with all original fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique prompt identifier (kebab-case) |
| `sdlc` | string | SDLC phase: `discover`, `design`, `build`, `ship`, `operate` |
| `cat` | string | Category within phase (e.g. `Understand`, `Plan`, `Implement`, `Test`, `Debug`) |
| `roles` | string[] | Intended audience roles (empty = general) |
| `prompt` | string | The prompt template with `{slot}` placeholders |
| `slots` | object | Example slot values (optional) |
| `startN` | number | Suggested workflow step order (optional) |
| `nextHref` | string | Link to next doc page (optional) |
| `needs` | string | Required tool/integration (optional) |
| `paste` | string | Expected paste type (optional) |
| `src` | string | Source section: `workflows`, `best-practices`, `teams`, `ebook`, `legal`, `cybersecurity` |

## Count by SDLC phase

| Phase | Count |
|-------|-------|
| discover | 7 |
| design | 6 |
| build | 22 |
| ship | 5 |
| operate | 12 |
| **Total** | **52** |

## How to query

Any lane can read the full list or filter by SDLC phase:

```bash
# All prompts
cat skills/prompt-library/prompts.json

# Filter by phase (e.g. build)
node -e "const p=require('./skills/prompt-library/prompts.json');console.log(JSON.stringify(p.filter(x=>x.sdlc==='build'),null,2))"

# Filter by category
node -e "const p=require('./skills/prompt-library/prompts.json');console.log(JSON.stringify(p.filter(x=>x.cat==='Debug'),null,2))"

# Filter by role
node -e "const p=require('./skills/prompt-library/prompts.json');console.log(JSON.stringify(p.filter(x=>x.roles.includes('pm')),null,2))"
```

## Source

Extracted 2026-07-24 from the official Claude Code Prompt Library (https://code.claude.com/docs/en/prompt-library). All 52 entries preserved with all original fields. No modifications. Re-extract from the live page to refresh.
