---
name: onboard
description: Generate onboarding documentation for a codebase — architecture overview, key files, local setup, and common gotchas. Use this skill whenever someone asks to onboard onto a codebase, create onboarding docs, generate a codebase overview, explain a project's architecture to newcomers, or asks "how does this codebase work". Also trigger when users say things like "document this repo for new devs", "write a getting started guide", or "help me understand this project".
---

# Codebase Onboarding Doc Generator

Generate a comprehensive `ONBOARDING.md` file that helps a new developer get productive in a codebase quickly. The doc should answer the questions a new team member would ask in their first week.

## Process

### 1. Discover the codebase

Run these investigations in parallel to build a mental model:

**Project identity:**
- Read `README.md`, `CLAUDE.md`, `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, or equivalent to understand the project's purpose, language, and framework
- Check for monorepo indicators (`workspaces`, `lerna.json`, `nx.json`, `turbo.json`, `pnpm-workspace.yaml`)

**Architecture:**
- Map the top-level directory structure (`ls -la` and one level deep)
- Identify the entry points (e.g., `main.ts`, `index.js`, `app.py`, `cmd/`, `src/main.rs`)
- Look for architectural patterns: routes/, controllers/, services/, models/, hooks/, components/, etc.
- Check for infrastructure config: `docker-compose.yml`, `Dockerfile`, `terraform/`, `k8s/`, `.github/workflows/`

**Setup and tooling:**
- Find setup scripts: `Makefile`, `justfile`, `scripts/`, `bin/setup`
- Check dependency files: `package-lock.json`, `yarn.lock`, `Pipfile.lock`, `poetry.lock`, `Gemfile.lock`
- Look for environment config: `.env.example`, `.env.template`, `.envrc`
- Check for database migrations: `migrations/`, `prisma/`, `alembic/`, `db/migrate/`

**Testing and CI:**
- Find test directories and config: `jest.config`, `pytest.ini`, `vitest.config`, `.github/workflows/`
- Check for linting/formatting config: `.eslintrc`, `.prettierrc`, `ruff.toml`, `rustfmt.toml`

**Gotcha indicators:**
- Read `.gitignore` for clues about generated files and local config
- Check for `CONTRIBUTING.md` or `docs/` directory
- Look for non-obvious dependencies: `.tool-versions`, `.nvmrc`, `.python-version`, `rust-toolchain.toml`
- Scan recent git history for patterns: `git log --oneline -30`

### 2. Identify key files

Select 10-20 files that a new developer should read first. Prioritize:
- Entry points and main application wiring
- Core domain models or types
- Key configuration files
- The most-changed files (they're often the most important): `git log --format= --name-only -100 | sort | uniq -c | sort -rn | head -20`
- README and contributing guides

### 3. Detect common gotchas

Look for things that trip up new developers:
- Required environment variables without defaults
- Non-obvious setup steps (database seeding, code generation, certificate setup)
- Unconventional project conventions (custom scripts, unusual directory structure)
- Version pinning requirements (Node version, Python version, etc.)
- Known issues in CI/CD that affect local development
- Files or directories that look important but are generated (and shouldn't be edited)

### 4. Write ONBOARDING.md

Save the file to the repository root. Use this structure:

```markdown
# Onboarding: [Project Name]

## What is this?
[2-3 sentence description of what the project does and who uses it]

## Architecture Overview
[High-level description of the system architecture. Include a text diagram if the system has multiple components or services.]

### Directory Structure
[Annotated tree of the important top-level directories — skip node_modules, vendor, etc.]

### Key Patterns
[Architectural patterns used: MVC, hexagonal, event-driven, etc. How data flows through the system.]

## Key Files to Read First
[Ordered list of 10-20 files with a one-line description of why each matters. Group by theme if helpful.]

## Local Setup

### Prerequisites
[Required tools and versions]

### Getting Started
[Step-by-step setup instructions — clone, install, configure, run]

### Running Tests
[How to run the test suite, including any setup needed]

### Common Commands
[Table or list of frequently used commands: build, test, lint, deploy, etc.]

## Common Gotchas
[Numbered list of things that trip up new developers, with solutions]

## Useful Links
[Links to relevant docs, dashboards, design docs, Slack channels, etc. — only if discoverable from the repo]
```

### Writing guidelines

- Write for someone who is a competent developer but knows nothing about this specific codebase
- Be concrete — use actual file paths, actual command names, actual environment variable names
- If you're uncertain about something (e.g., whether a setup step is still current), flag it with a "Verify:" note rather than guessing
- Keep the total doc under 300 lines — long onboarding docs don't get read
- Don't include information you can't verify from the codebase itself
