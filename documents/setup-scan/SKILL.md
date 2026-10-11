---
name: setup-scan
description: Setup-assistant scan — commands, discovery table, skill/MCP checks.
---

## Step 1 — Scan Commands

```bash
# Package files (infer stack)
ls package.json composer.json requirements.txt Gemfile go.mod Cargo.toml Dockerfile 2>/dev/null

# CI configs
ls .github/workflows/ Jenkinsfile .gitlab-ci.yml 2>/dev/null

# Git history and uncommitted state
git log --oneline -20
git status

# Installed version
source .dev-team-agents/scripts/lib/state.sh 2>/dev/null
state_get installed_version .dev-team-agents/user-data/state.json 2>/dev/null || echo "unknown"
```

Read: `README.md`, `CLAUDE.md`, `AGENTS.md`, `.claude/` directory structure.

Summarize findings (files + stack + commit history + installed version) before asking questions.

---

## Skill Availability Checks

Run when the project has UI or frontend work:

| Skill | Check | If missing |
|-------|-------|-----------|
| `frontend-design` | `test -d .claude/skills/frontend-design` | **Claude Code:** `/plugins` → search `frontend-design` → install → re-run installer. Other CLIs: install the skill through that CLI's own mechanism, then re-run the installer |
| `web-design-guidelines` | `test -d .claude/skills/web-design-guidelines` | `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines` → re-run installer |

Both `frontend-developer` and `ui-ux-designer` depend on these skills.

---

## Project Docs Discovery

Run before generating any `docs/` file:

```bash
# Root-level markdown (excluding already-read files)
find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CLAUDE.md" ! -name "AGENTS.md" | sort

# Documentation directories (up to 3 levels) — markdown and office formats
find . -maxdepth 3 \( -path "*/docs/*" -o -path "*/documentation/*" -o -path "*/doc/*" -o -path "*/wiki/*" \) \
  \( -name "*.md" -o -name "*.txt" -o -name "*.rst" -o -name "*.pdf" \
     -o -name "*.doc" -o -name "*.docx" -o -name "*.xls" -o -name "*.xlsx" \
     -o -name "*.csv" -o -name "*.yaml" -o -name "*.yml" \) 2>/dev/null | sort

# AI/agent config directories — may contain project instructions or conventions
find . -maxdepth 2 \( -path "./.cursor/*" -o -path "./.agents/*" -o -path "./.github/*" \) \
  -name "*.md" 2>/dev/null | sort
ls .cursor/rules/ .cursor/*.md .agents/*.md .github/CODEOWNERS .github/CONTRIBUTING.md \
  .github/pull_request_template.md 2>/dev/null || true

# OpenAPI / Swagger specs
find . -maxdepth 3 \( -name "openapi.yaml" -o -name "openapi.json" -o -name "swagger.yaml" -o -name "swagger.json" \) 2>/dev/null | sort

# Linting / convention configs
find . -maxdepth 2 \( -name ".eslintrc*" -o -name ".prettierrc*" -o -name "phpcs.xml" -o -name "pyproject.toml" -o -name ".rubocop.yml" -o -name "golangci.yml" -o -name ".stylelintrc*" \) 2>/dev/null | sort
```

| Found File Pattern | Feeds Into |
|-------------------|-----------|
| `ARCHITECTURE.md`, `docs/architecture*` | `architecture.md` → System Type, Layers, Module Map |
| `CONTRIBUTING.md`, `docs/contributing*`, `docs/development*` | `code-standards.md` → Naming Conventions, Patterns |
| `docs/api*`, `API.md`, `openapi.yaml`, `swagger.yaml` | `architecture.md` → API Contracts |
| `docs/stack*`, `docs/tech*`, `DEVELOPMENT.md`, `TECH*.md` | `tech-stack.md` → Tech Stack table, Dev Setup |
| `.eslintrc*`, `.prettierrc*`, `phpcs.xml`, `pyproject.toml`, etc. | `code-standards.md` → Detected Config |
| `CHANGELOG.md`, `docs/changelog*` | `project.md` → Active Areas |
| `docs/design*`, `DESIGN*.md` | `design/design-system.md` → UI conventions |
| `.cursor/rules/*`, `.cursor/*.md` | `code-standards.md` → Cursor AI conventions |
| `.agents/*.md` | `project.md` → Agent overrides in effect |
| `.github/CODEOWNERS`, `.github/CONTRIBUTING.md`, `.github/pull_request_template.md` | `code-standards.md` → Review process, PR standards |
| `docs/infra*`, `docs/devops*`, `docs/deploy*`, `*.tf`, `docker-compose*` | `docs/devops/` → Infrastructure and deployment docs |
| `docs/test*`, `docs/qa*`, `jest.config*`, `vitest.config*`, `playwright.config*` | `docs/tests/` → Test strategy and configuration |

Content is synthesized (not duplicated) into the target doc. Use `<!-- TODO: <agent> to fill -->` only for sections with no data yet.

---

## Issue Tracker MCP Configuration

| Tracker | MCP | What's needed |
|---------|-----|---------------|
| GitHub Projects | `github` | Personal access token (read:project scope) |
| GitLab Issues | `gitlab` | Personal access token (read_api scope) |
| Jira | `atlassian` | API token + workspace URL |
| Linear | `linear` | API key (read-only) |
| ClickUp | `clickup` | Personal API token |
| Others | none required | Agents read from user-provided markdown exports |

**Supported trackers:** GitHub Projects, GitLab Issues, Jira, Linear, ClickUp, Trello, Asana, Monday.com, Notion, Azure DevOps Boards, Shortcut.

Configure tokens in the active CLI's MCP settings — Claude Code: `~/.claude/settings.json` or `/mcp`; opencode: the `mcp` block of `opencode.json`; Codex CLI: its own MCP config. Never store credentials in project files. Agents read tasks but only write with explicit user consent.
