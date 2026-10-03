---
name: claude-automation-recommender
description: >-
  Analyze a codebase and recommend AI automations (MCP servers, skills, hooks,
  subagents, slash commands). Use when the user asks for automation recommendations,
  wants to optimize Claude Code or Cursor setup, mentions improving agent workflows,
  asks how to set up a project for AI coding, or what hooks/skills/MCP to use.
---

# Claude / Cursor Automation Recommender

Analyze codebase patterns and recommend tailored automations. **Read-only** — analyze and report; do not create or modify files unless the user explicitly asks you to implement recommendations afterward.

**Source:** [claude-code-setup plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup)

## Cursor vs Claude Code paths

| Concept | Claude Code | Cursor IDE |
|---------|-------------|------------|
| Skills | `.claude/skills/<name>/SKILL.md` | `.cursor/skills/` or `~/.cursor/skills/` |
| Slash commands | Plugin / project commands | `.cursor/commands/*.md` → `/filename` |
| Rules | `CLAUDE.md`, `.claude/` | `.cursor/rules/*.mdc`, `AGENTS.md` |
| Hooks | `.claude/settings.json` | `.cursor/hooks.json` + `.cursor/hooks/*` |
| MCP | `.mcp.json`, `claude mcp add` | Cursor Settings → MCP, or project MCP config |
| Subagents | `.claude/agents/*.md` | Task tool (`explore`, `generalPurpose`, etc.) + skills |

When the user works in **Cursor** (this environment), prefer Cursor paths in recommendations. Mention Claude Code equivalents when relevant for teams using both.

## Output guidelines

- **Recommend 1–2 per category** — top picks only, unless the user asks for one category (then 3–5).
- **Go beyond reference lists** — use web search for tools/frameworks specific to the repo.
- **End with**: user can ask for more in any category; offer to help implement.

## Automation types

| Type | Best for |
|------|----------|
| **Hooks** | Automatic actions on tool/session events (format, lint, block edits) |
| **Subagents** | Specialized parallel reviewers (security, performance, a11y) |
| **Skills** | Packaged expertise and repeatable workflows |
| **Plugins** | Bundled skills (Claude marketplace / Cursor global skills) |
| **MCP Servers** | External tools (docs, DB, browser, GitHub, etc.) |
| **Slash commands** | Quick workflows (`/test`, `/pr-review`) |

## Workflow

### Phase 1: Codebase analysis

Gather project context (adapt commands for Windows PowerShell when needed):

```powershell
# Project markers
Get-ChildItem -Name package.json, pyproject.toml, Cargo.toml, go.mod, CMakeLists.txt, AGENTS.md, CLAUDE.md -ErrorAction SilentlyContinue

# Existing AI config
Test-Path .cursor, .claude, AGENTS.md, CLAUDE.md
Get-ChildItem .cursor -ErrorAction SilentlyContinue
Get-ChildItem .claude -ErrorAction SilentlyContinue
```

Also inspect: `engine/`, `src/`, `tests/`, CI configs, formatters/linters, `.env*`, lockfiles, MCP configs.

**Key indicators**

| Category | Signals | Informs |
|----------|---------|---------|
| Language / build | CMake, Cargo, package.json, etc. | Hooks, MCP |
| Frontend | React, Vue, Slint UI | Playwright MCP, UI skills |
| Backend / APIs | Express, FastAPI, custom servers | API doc skills |
| Database | Prisma, SQL, Supabase | DB MCP |
| External SDKs | Stripe, AWS, Vulkan | context7, domain MCP |
| Testing | pytest, CTest, Playwright | Test hooks, subagents |
| CI/CD | GitHub Actions | GitHub MCP |
| Docs | OpenAPI, AGENTS.md | Convention skills |

### Phase 2: Generate recommendations

Use reference files in this skill directory:

- [references/mcp-servers.md](references/mcp-servers.md)
- [references/skills-reference.md](references/skills-reference.md)
- [references/hooks-patterns.md](references/hooks-patterns.md)
- [references/subagent-templates.md](references/subagent-templates.md)
- [references/plugins-reference.md](references/plugins-reference.md)

**Cursor hooks:** map Claude `PostToolUse` / `PreToolUse` patterns to `.cursor/hooks.json` events such as `afterFileEdit`, `preToolUse`, `beforeShellExecution`, `beforeSubmitPrompt` (see create-hook skill if needed).

**Cursor subagents:** recommend Task tool usage + project skills (e.g. `code-reviewer`, `feature-dev` in `~/.cursor/skills/`).

### Phase 3: Recommendations report

Only **1–2 per category**; skip irrelevant categories.

```markdown
## Automation Recommendations

Analyzed your codebase. Top 1–2 picks per category:

### Codebase profile
- **Type**: …
- **Framework**: …
- **Key libraries**: …
- **AI tooling detected**: Cursor / Claude Code / both

---

### MCP servers
#### [name]
**Why**: …
**Install (Claude Code)**: `claude mcp add …`
**Install (Cursor)**: Settings → MCP, or project MCP config

---

### Skills
#### [name]
**Why**: …
**Cursor**: `.cursor/skills/<name>/SKILL.md` or `~/.cursor/skills/<name>/`
**Claude Code**: `.claude/skills/<name>/SKILL.md`

---

### Hooks
#### [name]
**Why**: …
**Cursor**: `.cursor/hooks.json` — event: `afterFileEdit` / `preToolUse` / …
**Claude Code**: `.claude/settings.json`

---

### Subagents / parallel agents
#### [name]
**Why**: …
**Cursor**: Task tool + skill, or dedicated explore/review prompt
**Claude Code**: `.claude/agents/<name>.md`

---

### Slash commands
#### /[name]
**Why**: …
**Cursor**: `.cursor/commands/<name>.md`

---

**Want more?** Ask for another category.
**Want implementation help?** Ask to set up any recommendation.
```

## Decision framework

### MCP servers
External services, live docs, browser testing, GitHub/Linear/Slack, cloud infra.

### Skills
Repeated workflows, project conventions, templates/scripts, user-only side effects (`disable-model-invocation: true`).

### Hooks
Post-edit format/lint, block sensitive files, validation after edits.

### Subagents
Security/performance review, parallel audits, large codebases.

### Plugins / command bundles
Multiple related skills; team standardization (e.g. official `feature-dev`, `claude-code-setup`).

## Configuration tips

- **Team MCP**: commit shared MCP config so the team matches.
- **Cursor project hooks**: prefer `.cursor/hooks.json` in repo for shared behavior.
- **Permissions (Claude Code)**: `.claude/settings.json` allow lists for hook tools.
- **Headless Claude (CI only)**: `claude -p "…"` when Claude Code CLI is installed.
