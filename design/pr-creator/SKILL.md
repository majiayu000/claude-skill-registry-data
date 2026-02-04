---
name: pr-creator
description: Guide for creating pull requests with draft status confirmation. Use when user requests PR creation with phrases like 'create a PR', 'make a pull request', 'gh pr create', or similar PR creation requests.
---

# PR Creator

## Overview

Guides PR creation by confirming whether to create as draft before executing the gh pr create command.

## Workflow

When the user requests PR creation:

1. **Confirm draft status**: Use AskUserQuestion to ask whether to create the PR as draft

   ```
   Question: "Should this PR be created as a draft?"
   Options:
   - "Yes, create as draft" → Execute with --draft flag
   - "No, create as ready for review" → Execute without --draft flag
   ```

2. **Execute gh pr create**: Based on the user's choice, run the appropriate command:
   - Draft: `gh pr create --draft --title "..." --body "..."`
   - Ready: `gh pr create --title "..." --body "..."`

## PR Description Guidelines

Write concise, minimal descriptions:

- **No fixed format sections** (avoid ## Summary, ## Test plan, etc.)
- **Include only essential information** needed to understand the change
- **Keep it brief** - typically 1-3 sentences or a short bulleted list
- **Adapt format to PR content** - simple changes need simple descriptions

Examples:
- "Fix authentication bug in login flow"
- "Add user profile API endpoint\n- GET /api/users/:id\n- Returns user data with privacy filters"
- "Refactor database queries for performance"
