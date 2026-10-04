---
name: readme
description: Assess the codebase and update the README with any new or outdated information
---

# Update README

Assess the current state of the project and update (or create) the README to accurately reflect it.

**DO NOT fabricate. Read actual files, configs, and code before writing anything.**

## Step 1: Assess the Project (Parallel)

Launch **all four agents in a single message** to build a complete picture of the codebase simultaneously. Do NOT run them sequentially.

**Agent 1 — Project identity and current README:**
- Read `README.md` (if it exists) to understand the current documented state
- Read package manifests (`package.json`, `composer.json`, `Cargo.toml`, `build.gradle`, `pyproject.toml`, `go.mod`, `Gemfile`, `*.csproj`, etc.)
- Read `.claude-plugin/plugin.json`, `plugin.json`, or similar plugin/extension manifests
- Determine: project name, description, version, language, framework, license, author
- Output the full content of the existing README (or note that none exists)

**Agent 2 — Structure and features:**
- List top-level directories and key files
- Identify major modules, packages, or components
- Read entry points (`main.*`, `index.*`, `app.*`, `server.*`, `src/`, `cmd/`, etc.)
- Identify APIs, CLI commands, routes, or other public interfaces
- Check for Docker/container files, CI/CD configs, deployment scripts

**Agent 3 — Setup and usage:**
- Check for Makefiles, Dockerfiles, docker-compose, scripts/, bin/
- Identify build commands, test commands, lint commands from package manifests and scripts
- Check for environment variables (`.env.example`, `.env.sample`, config files)
- Check for database migrations, seed files, or other required setup steps
- Read CONTRIBUTING.md, DEVELOPMENT.md, or similar if they exist

**Agent 4 — Dependencies and configuration:**
- Read dependency files (lock files, requirement files)
- Identify key dependencies and their purpose
- Check for config files that need documenting
- Look for pre-requisites (runtime versions, system dependencies, external services)

**Wait for all four agents to complete before proceeding.**

## Step 2: Diff and Update

Synthesize all four agent outputs. Compare the codebase state against the existing README (from Agent 1) and identify:

- **Missing**: features, commands, modules, config, or setup steps that exist but aren't documented
- **Stale**: entries that reference files, commands, APIs, or patterns that no longer exist
- **Inaccurate**: descriptions that don't match the current code behavior
- **Outdated**: version numbers, dependency lists, or instructions that have drifted

Then edit (or create) the README following these principles:

Edit (or write) the README following these principles:

- **Match the existing style.** If the README uses tables, keep tables. If it uses bullet lists, keep bullet lists. Don't impose a new format on an established README.
- **Preserve intentional content.** Don't remove sections the author wrote manually (architecture decisions, contribution guidelines, acknowledgements) unless they're factually wrong.
- **Add what's missing.** New modules, commands, features, config options, setup steps.
- **Remove what's gone.** Entries for deleted files, deprecated features, old instructions.
- **Fix what's wrong.** Stale version numbers, incorrect commands, outdated descriptions.
- **Keep it concise.** The README should help someone get started and understand the project, not document every implementation detail.

For a new README, include at minimum:
1. Project name and one-line description
2. Prerequisites and installation
3. Usage / getting started
4. License (if determinable from manifests)

Only add additional sections if the project has content worth documenting (API reference, configuration, architecture, contributing guidelines, etc.).

## Step 3: Verify (Parallel)

Launch **two agents in a single message** to verify the updated README:

**Agent 1 — Completeness check:**
- Every documented file, command, or feature actually exists in the codebase
- Every significant public interface or module has a mention
- No entries reference files or commands that don't exist on disk

**Agent 2 — Accuracy check:**
- Install/build/test instructions are runnable (check the actual commands exist in manifests and scripts)
- Version numbers match package manifests
- No placeholder text, TODO markers, or guessed descriptions remain

If either agent finds issues, fix them before reporting done.

## Hard Rules

1. **Read before writing** — every description must come from reading actual code or config, not inferring from names
2. **Preserve voice** — match the existing README's tone and style, don't impose your own
3. **No bloat** — don't add sections the project doesn't need. A 20-line README for a small project is fine.
4. **No lies** — if you can't determine what something does after reading it, say so or omit it. Never guess.
5. **Minimal diff** — change only what's wrong or missing. Don't rewrite sections that are already accurate.
