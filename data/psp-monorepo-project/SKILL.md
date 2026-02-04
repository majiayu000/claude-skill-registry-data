---
name: psp-monorepo-project
description: Setup personal web app with pnpm workspace monorepo structure deployable to Cloudflare. Use when starting a new personal project.
---

# Personal Project Setup

Setup a personal web application with pnpm workspace monorepo structure deployable to Cloudflare.

## Steps

1. Ask the user for project name and description
2. Run the setup script: `${CLAUDE_PLUGIN_ROOT}/skills/psp-monorepo-project/setup.ts <project-name>`
3. Replace `<PROJECT_NAME>` and `<PROJECT_DESCRIPTION>` in AGENTS.md
4. Create config files in apps/web/ (see @${CLAUDE_PLUGIN_ROOT}/skills/psp-monorepo-project/config-templates.md)
5. Create Cloudflare resources and update wrangler.jsonc

## Tech Stack

@${CLAUDE_PLUGIN_ROOT}/skills/psp-monorepo-project/tech-stack.md

## Directory Structure

```
<project-name>/
├── apps/
│   └── web/                 # TanStack Start application
├── packages/
│   └── shared/              # Shared utilities (optional)
├── pnpm-workspace.yaml
├── package.json
├── biome.json
├── AGENTS.md
└── .claude/
    └── rules/
```
