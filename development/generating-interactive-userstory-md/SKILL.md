---
name: generating-interactive-userstory-md
description: Build UserStory.md interactively via Q&A. Use when the user wants to create a user story document or start the assisted workflow.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: AskUserQuestion, Read, Write, WebFetch, WebSearch
  disable-model-invocation: true
  stability: stable
  content-hash: sha256:e36675831972045ce779f241dc6efedcbc399ee3c0238bd531291c5b2647f704
---

# User Story Builder

Interactively builds `docs/UserStory.md` through structured Q&A with the user.

## Purpose

Guides users through creating a user story document that can be transformed into PRD.md using the `generating-prd-md-from-userstory-md` skill.

## Workflow

1. **Check for existing UserStory.md**
   - If exists, ask user if they want to rebuild (backup as `docs/UserStory.md.bak`)

2. **Ask structured questions** using AskUserQuestion tool for each template section:
   - Project name
   - Problem statement
   - Target users
   - Value proposition
   - User stories (use "As a [role], I want to [action] so that [benefit]" format)
   - Success criteria
   - Constraints
   - Out of scope

3. **Generate UserStory.md**
   - Read template from `ralph/docs/templates/userstory.md.template`
   - Replace placeholders with user responses
   - Write to `docs/UserStory.md`

4. **Suggest next step**: `make ralph_prd_md` to generate PRD.md

## Template

See `ralph/docs/templates/userstory.md.template` for structure and placeholders.

## Usage

```bash
make ralph_userstory
```
