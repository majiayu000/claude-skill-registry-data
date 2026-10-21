---
name: claude-automation-recommender
owner: baseline
description: Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). Use when user asks for automation recommendations, wants to optimize their Claude Code setup, mentions improving Claude Code workflows, asks how to first set up Claude Code for a project, or wants to know what Claude Code features they should use.
tools: Read, Glob, Grep, Bash
---

# Claude Automation Recommender

Analyze codebase patterns to recommend tailored Claude Code automations across all extensibility options.

**This skill is read-only.** It analyzes the codebase and outputs recommendations. It does NOT create or modify any files. Users implement the recommendations themselves or ask Claude separately to help build them.

## Working with the baseline

> **This skill is invoked from inside a project that ships the Claude Code Baseline (`docs/init/seed.md`).** Read that file before recommending — it lists what is already installed.

The baseline already provides the following. **Do not recommend any of these as additions** — they exist:

- **22 hooks**: 17 write/run-boundary guards — `setup_guard`, `destructive_cmd_guard`, `git_commit_guard`, `env_guard`, `direction_approval_guard`, `swarm_approval_guard`, `verify_pass_guard`, `track_guard`, `artifact_template_guard`, `plantuml_syntax_guard`, `spec_diagram_presence_guard`, `spec_design_calls_guard`, `swarm_boundary_guard`, `tdd_order_guard`, `process_lifecycle_guard`, `lint_runner`, `test_runner` — plus 4 lifecycle hooks: `memory_session_start`, `memory_stop`, `memory_pre_compact`, `harness_continuation` — plus 1 input-boundary hook: `consent_gate_grant`.
- **1 subagent**: `swarm-worker` — the only subagent in the baseline. It executes pre-decided recipes from main context inside isolated git worktrees during `/swarm-dispatch`. **No new subagents should be recommended.** All decision-making lives in skills running in main context, where conversational nuance and full file visibility are preserved.
- **36 skills**: artifact drafting (4), workflow phases (10), phase workers — `scenario`, `implement`, `verify`, `prose`, `design-ui` (5), spec helpers — `spec-lint`, `spec-render`, `spec-diagram-review`, `spec-traceability-review` (4), orchestration — `harness`, `swarm-plan`, `swarm-dispatch` (3), memory — `memory-sync` (1), audit — `audit-baseline` (1), alternate tracks — `chore` (1), plus seven shared globals: `claude-automation-recommender`, `code-structure`, `humanizer`, `documentation`, `technical-tutorials`, `copywriting`, `impeccable`. Several skills mandatorily invoke another skill: `scenario` and `implement` invoke `code-structure`; `design-ui` invokes `impeccable`; `prose` invokes `humanizer` (always) and `copywriting` (when persuasive). The `technical-tutorials` skill carries its audience-context reference doc inline at `.claude/skills/technical-tutorials/references/audience-context.md` (consolidated 2026-04-28 from the upstream `developer-audience-context` skill).
- **4 commands**: `/approve-direction`, `/approve-swarm`, `/grant-commit`, `/init-project`.
- **3 MCP servers**: the documentation provider named in `.claude/docs-provider.json` (library docs), `plantuml` (diagram rendering), `playwright` (Microsoft-official browser automation; used by `design-ui` for cross-engine visual verification, by `integrate` for optional cross-engine smoke).

Your job is to surface **gaps** the baseline doesn't cover for *this project*. Examples of valuable recommendations:

- **Project-management MCPs** (Linear, Jira, GitHub Issues) when the codebase shows references to those systems.
- **Monitoring / observability MCPs** (Sentry, Datadog) when the project has an error-tracking integration.
- **Stack-specific lint/test commands** populating `project.json → test.cmd` and `lint.cmd` based on detected framework (Vitest vs Jest vs pytest, Ruff vs Black vs Prettier+ESLint, etc.).
- **Stack-specific destructive-command patterns** to extend `project.json → destructive.{hard_block,ask}_patterns` (e.g., `terraform destroy`, `kubectl delete`, `rails db:drop`).
- **TDD glob conventions** matching the project's actual test file layout (`*_test.go`, `*.test.tsx`, `tests/test_*.py`).
- **New skills** for repeated project workflows the baseline phases don't cover (e.g., `release-notes` for a project with monthly cuts, or stack-specific skills like `react-patterns` that the `swarm-worker` template can preload via the `{{SKILLS}}` token).

## Output format for `/init-project` consumption

When invoked from `/init-project`, structure your output as a JSON block (in addition to the human-readable narrative) that the orchestrator can parse and apply:

```json
{
  "stack": {
    "language": "typescript",
    "framework": "next.js",
    "test_runner": "vitest",
    "test_cmd": "vitest run --reporter=dot",
    "test_kind": "behavior",
    "linter": "biome",
    "lint_cmd": "biome check --apply"
  },
  "project_json": {
    "test": {
      "kind": "behavior"
    },
    "tdd": {
      "source_globs": ["src/**", "app/**"],
      "test_globs": ["**/*.test.{ts,tsx}"]
    },
    "destructive": {
      "ask_patterns_extend": ["\\bvercel\\s+remove\\b", "\\bsupabase\\s+db\\s+reset\\b"]
    }
  },
  "additions": {
    "mcp_servers": [
      {"name": "linear", "command": "npx -y @linear/mcp", "why": "issues referenced in 23 commits"}
    ],
    "skills": [],
    "hooks": [],
    "swarm_worker_skills": []
  },
  "gaps": [
    "No CI configuration detected; the baseline assumes the user runs tests locally"
  ]
}
```

Set `project_json.test.kind` (mirrored as the stack `test_kind` hint) to tell the chore track whether `test.cmd` can exercise a docs-only change: `behavior` — a code-only suite such as vitest — lets a pure-docs chore skip `verify`; `structural` (or an absent key) — a whole-repo check — always runs it. Recommend `behavior` whenever the `test_cmd` is a unit/integration runner. For vitest specifically, recommend `--reporter=dot` (the `basic` reporter was removed in vitest v4).

When invoked outside `/init-project` (ad-hoc), the human-readable narrative alone is fine — skip the JSON.

### `swarm-worker` template — stack skills the worker should preload

The baseline ships exactly one subagent: `swarm-worker`. It is template-rendered. `/init-project` reads `src/agents/swarm-worker.template.md` and substitutes four tokens. The base body always preloads `scenario` and `implement`; this section is about **adding stack-specific skills** that the worker should also have loaded so its `Skill(implement)` invocation lands in a context primed for the stack.

Recommend stack skills in `additions.swarm_worker_skills` — a flat list of skill names (no `from_template` indirection, no per-variant explosion). `/init-project` re-renders the worker with `SKILLS = ["scenario", "implement"] + swarm_worker_skills`.

Schema for the recommendation:

```json
"swarm_worker_skills": ["react-patterns", "react-testing-library", "accessibility"]
```

Rules:

- **Every skill listed must exist on disk** *or* appear earlier in `additions.skills[]` so it's installed before the worker re-render runs. `/init-project` enforces this; emit it correctly and the render lands cleanly.
- **Stack skills only.** Generic discipline (`code-structure`, `humanizer`) is already invoked by the worker's two mandatory skills (`scenario` → `code-structure`; `implement` → `code-structure` + the documentation provider). Don't duplicate.
- **Don't recommend new subagent types.** The worker's job is execution, not judgment; specialization happens via skills loaded into its context, not via parallel agent personas. New decision-making roles belong in skills, which run in main context where context richness matters.

## Output Guidelines

- **Recommend 1-2 of each type**: Don't overwhelm - surface the top 1-2 most valuable automations per category
- **If user asks for a specific type**: Focus only on that type and provide more options (3-5 recommendations)
- **Go beyond the reference lists**: The reference files contain common patterns, but use web search to find recommendations specific to the codebase's tools, frameworks, and libraries
- **Tell users they can ask for more**: End by noting they can request more recommendations for any specific category

## Automation Types Overview

| Type | Best For |
|------|----------|
| **Hooks** | Automatic actions on tool events (format on save, lint, block edits) |
| **Subagents** | Specialized reviewers/analyzers that run in parallel |
| **Skills** | Packaged expertise, workflows, and repeatable tasks (invoked by Claude or user via `/skill-name`) |
| **Plugins** | Collections of skills that can be installed |
| **MCP Servers** | External tool integrations (databases, APIs, browsers, docs) |

## Workflow

### Phase 1: Codebase Analysis

Gather project context:

```bash
# Detect project type and tools
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | head -50

# Check dependencies for MCP server recommendations
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'

# Check for existing Claude Code config
ls -la .claude/ CLAUDE.md 2>/dev/null

# Analyze project structure
ls -la src/ app/ lib/ tests/ components/ pages/ api/ 2>/dev/null
```

**Key Indicators to Capture:**

| Category | What to Look For | Informs Recommendations For |
|----------|------------------|----------------------------|
| Language/Framework | package.json, pyproject.toml, import patterns | Hooks, MCP servers |
| Frontend stack | React, Vue, Angular, Next.js | Playwright MCP, frontend skills |
| Backend stack | Express, FastAPI, Django | API documentation tools |
| Database | Prisma, Supabase, raw SQL | Database MCP servers |
| External APIs | Stripe, OpenAI, AWS SDKs | the declared documentation provider for docs |
| Testing | Jest, pytest, Playwright configs | Testing hooks, subagents |
| CI/CD | GitHub Actions, CircleCI | GitHub MCP server |
| Issue tracking | Linear, Jira references | Issue tracker MCP |
| Docs patterns | OpenAPI, JSDoc, docstrings | Documentation skills |

### Phase 2: Generate Recommendations

Based on analysis, generate recommendations across all categories:

#### A. MCP Server Recommendations

See [references/mcp-servers.md](references/mcp-servers.md) for detailed patterns.

| Codebase Signal | Recommended MCP Server |
|-----------------|------------------------|
| Uses popular libraries (React, Express, etc.) | **the documentation provider** - Live documentation lookup, already shipped |
| Frontend with UI testing needs | **Playwright** - Browser automation/testing |
| Uses Supabase | **Supabase MCP** - Direct database operations |
| PostgreSQL/MySQL database | **Database MCP** - Query and schema tools |
| GitHub repository | **GitHub MCP** - Issues, PRs, actions |
| Uses Linear for issues | **Linear MCP** - Issue management |
| AWS infrastructure | **AWS MCP** - Cloud resource management |
| Slack workspace | **Slack MCP** - Team notifications |
| Memory/context persistence | **Memory MCP** - Cross-session memory |
| Sentry error tracking | **Sentry MCP** - Error investigation |
| Docker containers | **Docker MCP** - Container management |

#### B. Skills Recommendations

See [references/skills-reference.md](references/skills-reference.md) for details.

Create skills in `.claude/skills/<name>/SKILL.md`. Some are also available via plugins:

| Codebase Signal | Skill | Plugin |
|-----------------|-------|--------|
| Building plugins | skill-development | plugin-dev |
| Git commits | commit | commit-commands |
| React/Vue/Angular | frontend-design | frontend-design |
| Automation rules | writing-rules | hookify |
| Feature planning | feature-dev | feature-dev |

**Custom skills to create** (with templates, scripts, examples):

| Codebase Signal | Skill to Create | Invocation |
|-----------------|-----------------|------------|
| API routes | **api-doc** (with OpenAPI template) | Both |
| Database project | **create-migration** (with validation script) | User-only |
| Test suite | **gen-test** (with example tests) | User-only |
| Component library | **new-component** (with templates) | User-only |
| PR workflow | **pr-check** (with checklist) | User-only |
| Releases | **release-notes** (with git context) | User-only |
| Code style | **project-conventions** | Claude-only |
| Onboarding | **setup-dev** (with prereq script) | User-only |

#### C. Hooks Recommendations

See [references/hooks-patterns.md](references/hooks-patterns.md) for configurations.

| Codebase Signal | Recommended Hook |
|-----------------|------------------|
| Prettier configured | PostToolUse: auto-format on edit |
| ESLint/Ruff configured | PostToolUse: auto-lint on edit |
| TypeScript project | PostToolUse: type-check on edit |
| Tests directory exists | PostToolUse: run related tests |
| `.env` files present | PreToolUse: block `.env` edits |
| Lock files present | PreToolUse: block lock file edits |
| Security-sensitive code | PreToolUse: require confirmation |

#### D. Subagent Recommendations

**Do not recommend new subagent types in this baseline.** The architecture commits to: decisions live in main context (where conversation history, screenshots, and offhand user feedback are preserved); subagents only execute pre-decided recipes (currently only `swarm-worker` for parallel code execution). Anything you'd previously have made a `code-reviewer` / `security-reviewer` / `api-documenter` subagent should be a **skill** invoked from main context — find or recommend a skill, not an agent.

If the project has a strong stack signal that warrants additional skills the `swarm-worker` should preload, recommend them via `additions.swarm_worker_skills` (described under "`swarm-worker` template — stack skills the worker should preload").

#### E. Plugin Recommendations

See [references/plugins-reference.md](references/plugins-reference.md) for available plugins.

| Codebase Signal | Recommended Plugin |
|-----------------|-------------------|
| General productivity | **anthropic-agent-skills** - Core skills bundle |
| Document workflows | Install docx, xlsx, pdf skills |
| Frontend development | **frontend-design** plugin |
| Building AI tools | **mcp-builder** for MCP development |

### Phase 3: Output Recommendations Report

Format recommendations clearly. **Only include 1-2 recommendations per category** - the most valuable ones for this specific codebase. Skip categories that aren't relevant.

```markdown
## Claude Code Automation Recommendations

I've analyzed your codebase and identified the top automations for each category. Here are my top 1-2 recommendations per type:

### Codebase Profile
- **Type**: [detected language/runtime]
- **Framework**: [detected framework]
- **Key Libraries**: [relevant libraries detected]

---

### 🔌 MCP Servers

#### [server name]
**Why**: [specific reason based on detected libraries]
**Install**: `claude mcp add [server name]`

---

### 🎯 Skills

#### [skill name]
**Why**: [specific reason]
**Create**: `.claude/skills/[name]/SKILL.md`
**Invocation**: User-only / Both / Claude-only
**Also available in**: [plugin-name] plugin (if applicable)
```yaml
---
name: [skill-name]
description: [what it does]
disable-model-invocation: true  # for user-only
---
```

---

### ⚡ Hooks

#### [hook name]
**Why**: [specific reason based on detected config]
**Where**: `.claude/settings.json`

---

### 🤖 Swarm-worker stack skills

#### [skill name to preload]
**Why**: [specific reason — usually a strong stack signal that justifies preloading the skill into the swarm-worker's context]
**Where**: `additions.swarm_worker_skills` in the JSON output

---

**Want more?** Ask for additional recommendations for any specific category (e.g., "show me more MCP server options" or "what other hooks would help?").

**Want help implementing any of these?** Just ask and I can help you set up any of the recommendations above.
```

## Decision Framework

### When to Recommend MCP Servers
- External service integration needed (databases, APIs)
- Documentation lookup for libraries/SDKs
- Browser automation or testing
- Team tool integration (GitHub, Linear, Slack)
- Cloud infrastructure management

### When to Recommend Skills

- Document generation (docx, xlsx, pptx, pdf — also in plugins)
- Frequently repeated prompts or workflows
- Project-specific tasks with arguments
- Applying templates or scripts to tasks (skills can bundle supporting files)
- Quick actions invoked with `/skill-name`
- Workflows that should run in isolation (`context: fork`)

**Invocation control:**
- `disable-model-invocation: true` — User-only (for side effects: deploy, commit, send)
- `user-invocable: false` — Claude-only (for background knowledge)
- Default (omit both) — Both can invoke

### When to Recommend Hooks
- Repetitive post-edit actions (formatting, linting)
- Protection rules (block sensitive file edits)
- Validation checks (tests, type checks)

### When to Recommend Subagents
**Don't.** The baseline ships exactly one subagent (`swarm-worker`) for parallel code execution; "specialized expertise" is a skill-shaped problem in this architecture, not an agent-shaped one. Recommend the skill instead.

### When to Recommend Plugins
- Need multiple related skills
- Want pre-packaged automation bundles
- Team-wide standardization

---

## Configuration Tips

### MCP Server Setup

**Team sharing**: Check `.mcp.json` into repo so entire team gets same MCP servers

**Debugging**: Use `--mcp-debug` flag to identify configuration issues

**Prerequisites to recommend:**
- GitHub CLI (`gh`) - enables native GitHub operations
- Puppeteer/Playwright CLI - for browser MCP servers

### Headless Mode (for CI/Automation)

Recommend headless Claude for automated pipelines:

```bash
# Pre-commit hook example
claude -p "fix lint errors in src/" --allowedTools Edit,Write

# CI pipeline with structured output
claude -p "<prompt>" --output-format stream-json | your_command
```

### Permissions for Hooks

Configure allowed tools in `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Edit", "Write", "Bash(npm test:*)", "Bash(git commit:*)"]
  }
}
```
