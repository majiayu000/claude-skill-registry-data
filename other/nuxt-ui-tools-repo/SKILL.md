---
name: nuxt-ui-tools-repo
description: Use this skill when implementing or refactoring code inside the nuxt-ui-tools repository itself. It routes the agent to the canonical AGENTS.md guide and the deeper maintainer skill so the agent can understand where code belongs, how domains relate, how to extend features, and what maintenance surfaces must be kept in sync.
---

# nuxt-ui-tools Repo

Use this skill for internal repository work.

## Canonical Guide

Read first:

- `AGENTS.md`

That file is the source of truth for:

- repository operation
- architecture
- coding rules
- task routing
- validation
- maintenance expectations

## Purpose Of This Skill

This is the lightweight internal router.

The deeper maintainer knowledge lives in:

- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`

Use `.agents/skills/` for:

- internal repository workflows
- implementation guidance
- maintainer-oriented procedures

Use `skills/consumer/` for:

- package-consumer guidance
- how to use the package
- user-facing feature documentation for AI agents

## Internal Skill Routing

For general internal architecture, placement, feature organization, or maintenance workflow, use:

- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`

For locale architecture, provider wiring, or translation-contract work, also use:

- `.agents/skills/nuxt-ui-tools-i18n/SKILL.md`

For table-specific internal work, also use:

- `.agents/skills/nuxt-ui-tools-table-runtime/SKILL.md`
