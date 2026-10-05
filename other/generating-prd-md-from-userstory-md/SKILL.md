---
name: generating-prd-md-from-userstory-md
description: Converts UserStory.md into a structured PRD.md document. Use after generating UserStory.md and before initializing the Ralph loop.
compatibility: Designed for Claude Code
metadata:
  disable-model-invocation: true
  allowed-tools: Read, Write
  stability: stable
  content-hash: sha256:ec9fcb1f7c496c6ea8dfd10499729bfbc4ff258fe367bf36a69ac287d7dc58a6
---

# Generate PRD.md from UserStory.md

Converts `docs/UserStory.md` into a structured `docs/PRD.md` using the PRD
template.

## Workflow

1. **Read `docs/UserStory.md`** — Validate it exists, parse all sections
   (Problem, Value, User Stories, Success Criteria, Constraints, Out of Scope)
2. **Read template** at `ralph/docs/templates/prd.md.template`
3. **Convert sections**:
   - Problem + Value Proposition → Project Overview
   - User Stories section → User Stories Reference
   - User stories → Functional requirements grouped by area
   - Success Criteria + Constraints → Non-Functional Requirements
   - Out of Scope → Out of Scope
4. **Backup** — If `docs/PRD.md` exists, copy to `docs/PRD.md.bak`
5. **Write** `docs/PRD.md`
6. **Suggest next step**: `make ralph_init_loop`

## Usage

```bash
make ralph_create_prd_md
```

## Template Location

`ralph/docs/templates/prd.md.template`
