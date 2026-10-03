---
name: create-agents-md
description: Generate, update, or review repository AGENTS.md files for AI coding agents. Use when a user asks to create an AGENTS.md, automate agent onboarding instructions, document build/test/style/security guidance for coding agents, add nested AGENTS.md files for subprojects, or align an existing AGENTS.md with https://agents.md/ conventions.
---

# Create AGENTS.md

## Overview

Create a concise, accurate `AGENTS.md` that helps coding agents work in a repository without bloating human-facing docs. Prefer repository facts over guesses, and leave explicit TODOs where a command or policy cannot be inferred.

## Workflow

1. Inspect the repository before writing:
   - Read `README*`, package manifests, build files, test configs, lint/format configs, CI workflows, and existing `AGENTS.md` files.
   - Search for monorepo package roots and nested toolchains.
   - Check whether Playwright is configured when UI testing or browser automation is relevant.
2. Draft or refresh `AGENTS.md`:
   - Run `scripts/generate_agents_md.py --repo <repo>` for a repo-informed first draft.
   - Use `--output <path>` to target a nested package.
   - Use `--force` only after confirming overwrite behavior or after reading the existing file.
3. Refine the draft manually:
   - Remove incorrect inferred commands.
   - Add missing project-specific gotchas from docs, CI, deployment files, or user-provided instructions.
   - Keep instructions imperative and scoped to agents.
4. Validate the result:
   - Ensure commands match actual package scripts or project docs.
   - Preserve existing user instructions unless the user asks to replace them.
   - For nested files, make scope clear because closer `AGENTS.md` files override parent instructions.

## Recommended Sections

Use this default shape unless the repository needs something else:

- `Project Overview`: purpose, stack, key entry points, and important directories.
- `Build And Test Commands`: install, dev, build, lint, typecheck, unit, integration, and e2e commands.
- `Code Style Guidelines`: formatter, lint rules, language conventions, naming, and architecture boundaries.
- `Testing Instructions`: focused test commands, fixture expectations, UI/browser validation, and when to use Playwright MCP automation.
- `Security Considerations`: secret handling, auth flows, unsafe operations, dependency changes, data privacy, and production safeguards.
- `Additional Instructions`: PR/commit expectations, large datasets, deployment steps, generated files, and anything a new teammate should know.

## Playwright MCP Guidance

When Playwright is configured or the user mentions UI validation, include practical instructions such as:

- Use Playwright MCP or available browser automation to exercise changed user flows.
- Capture screenshots for visual regressions and layout-sensitive changes.
- Prefer existing e2e specs before creating new browser scripts.
- Keep local dev server commands and ports explicit.

## Resources

- `scripts/generate_agents_md.py`: Generate a repo-informed AGENTS.md draft from common manifests and config files.
- `references/agents-md-checklist.md`: Read when manually reviewing a generated file or adapting a nonstandard repository.
