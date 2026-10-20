---
name: setup-workspace
description: Interactive wizard to create a new agentic workspace — walks through project definition, services, agents, skills, MCPs, and generates all configuration files from the agentic-workflows framework.
---

# Setup New Agentic Workspace

This skill guides you through creating a brand new agentic workspace from the `agentic-workflows` framework. It asks questions about your project, then generates all the configuration files — agents, skills, fragments, schemas, and manifest.

## Interaction Model — READ THIS FIRST

> **1. Switch to plan mode first.** Before executing anything, switch to planning mode:
>   - **Claude Code:** Enter plan mode (`/plan` or Shift+Tab)
>   - **Cursor:** Use chat mode (not agent mode)
>   - **OpenCode:** Switch to Plan agent (Tab)
>
> **2. Steps 0–5 are interactive.** Present each step's questions, wait for answers. Do NOT assume or skip.
>
> **3. After Step 5 — switch to execution mode:**
>   - **Claude Code:** Exit plan mode (normal mode)
>   - **Cursor:** Switch to agent mode
>   - **OpenCode:** Switch to Build agent (Tab)
>
> **4. Create a todo checklist** based on user's answers. Only generate files relevant to what they selected.
>
> **5. After each generation step,** briefly summarize what was created before moving to the next.

## Asking the User (MANDATORY)

When you need user input, you MUST use your tool's dedicated ask/question tool:

- **Claude Code:** Use the `AskUserQuestion` tool with structured options
- **Cursor:** Use the built-in ask question tool
- **OpenCode:** Use the question tool with select/text modes

**NEVER** just print a question as plain text. **ALWAYS** use the ask tool so the agent blocks until the user responds.

## Before Starting

Read the existing agentic-workflows repo to understand the framework structure:

1. Read `manifest.json` to see all files and their install paths
2. Read `agents/fragments/` to understand fragment structure
3. Read `workflow/phases.json`, `workflow/gates.json`, `workflow/state-schema.json`
4. Read `skills/onboard/SKILL.md` as a reference for how skills are structured
5. Read `agents/fragments/workflow-rules.core.md` — the orchestrator + subagent delegation model

This gives you the full template to adapt from.

## Step 0: Project Identity — **STOP, ask**

Use the ask tool:

> "Let's set up your new agentic workspace. First, some basics:"

### 0.1 Project name

> "What's your project name? (lowercase, used for directory names and prefixes)"
> - Text input (e.g., `myapp`, `acme-platform`, `dataflow`)

### 0.2 Description

> "One-line description of what this project does:"
> - Text input

### 0.3 Workspace style

> "How is your project structured?"
> - **Multi-repo orchestrated** — Multiple service repos in one workspace directory (like frndOS: `api/`, `web/`, etc.)
> - **Mono-repo** — Single git repo with all services
> - **Single service** — Just one repo, one service

Record all answers. The workspace style affects nearly every subsequent step.

## Step 1: Services — **STOP, ask**

### 1.1 Define services

> "List your services. For each one, I need:"
>
> | Field | Example |
> |-------|---------|
> | Name | `api` |
> | Directory | `api/` |
> | Repository | `org/repo-name` |
> | Stack | `Express, Node.js, PostgreSQL` |
> | Default branch | `main` |
> | Dev server port | `3000` |
> | Start command | `npm run dev` |
> | Health check URL | `http://localhost:3000/health` |
> | Healthy condition | `200 OK` |
> | Env file path | `api/.env` |
> | Env file contact | `alice` |
>
> "How many services do you have? List them one by one, or paste a table."

**STOP AND WAIT.** Let the user define all services. Ask follow-up questions if anything is ambiguous.

### 1.2 Service owners

> "Who owns each service? (for PR reviews and .env contacts)"

Record the full service registry.

## Step 2: Workflow Phases — **STOP, ask**

Present the default 8-phase state machine:

> "The default workflow has 8 phases:"
> ```
> idle → brainstorming → prd_creation → prd_splitting →
> implementation → pr_submission → [pr_review?] → completion → idle
> ```
> `pr_review` is conditional — skipped when the PR merges cleanly with no reviewer feedback.
>
> "Which phases do you need?"
> - **All 8** — Full workflow with brainstorming, PRD, implementation, PR submission + optional review
> - **No PRD splitting** — Single service, no need to split PRDs
> - **Minimal** — Just: idle → implementation → pr_submission → completion
> - **Custom** — I'll tell you which to keep/add

If user picks **Custom**, ask them to list:
- Phases to **remove** from the default 8
- Phases to **add** (describe what they do and where they fit)

## Step 3: Agents — none by default — **STOP, ask**

**No agent roster.** The modern framework has a single orchestrator — the running agent itself —
which delegates implementation to parallel subagents (right model + effort per task, intercom when
the harness supports it, see `workflow-rules.core.md`).

> "Any custom agents needed beyond the orchestrator + subagent model? (Default: none)"

### 3.1 Models

> "Any model preferences for subagent delegation?"
> - **Opus 5** — planning, review, complex code work
> - **Sonnet 5** — lighter mechanical tasks, status tracking
>
> "Default: per-task choice in the delegation batch — heavy reasoning for planning/review, cheap
> models for mechanical edits. Want to pin anything?"

### 3.2 Editor support

> "Which editors/CLIs should the install target?" (skills are shared; no per-editor agent files
> exist anymore)
> - Claude Code
> - Cursor
> - OpenCode
> - Amp

## Step 4: Skills & MCPs — **STOP, ask**

### 4.1 Built-in skills

> "Which skills do you need?"
> - `/onboard` — Interactive workspace setup wizard
> - `/workflow` — Feature state machine management
> - `/brainstorm` — Multi-choice question generator for the brainstorming phase
> - `/prd` — PRD creation helper
> - `/prd-split` — PRD splitter (also creates the feature branch)
> - `/pr-feedback` — address + resolve PR review threads
> - `/visual-testing` — browser-use visual validation for UI work
> - Custom: describe any additional skills

### 4.2 Community skills

> "Any community skills from [skills.sh](https://skills.sh)?"
> Examples:
> - `anthropics/skills@frontend-design`
> - `vercel-labs/next-skills@next-best-practices`
> - `busirocket/agents-skills@busirocket-tailwindcss-v4`
>
> "List any you want, or skip."

### 4.3 MCP servers

> "Which MCP servers do you need?"
>
> | MCP | Package | What it does | Needs credentials? |
> |-----|---------|-------------|-------------------|
> | Context7 | `@upstash/context7-mcp` | Library docs lookup | No |
> | GitHub | `@modelcontextprotocol/server-github` | PR/issue management | Yes (PAT) |
> | Lark CLI | official Lark CLI | Read pasted Lark doc links (read-only) | Yes (account auth — CLI only, never an MCP) |
> | Figma | `@anthropics/figma-mcp` | Design specs from Figma | Yes (PAT) |
>
> "List the ones you need. You can also add custom MCPs."

## Step 5: Dev Environment — **STOP, ask**

### 5.1 Toolchain

Tools are installed directly on the developer machine (Homebrew on macOS) — there is no Nix layer.

> "List the languages, tools, and databases you need, with pinned versions. Examples:"
> - Languages: `python@3.12`, `node@22`, `php@8.5`, `go`
> - Databases: `postgresql@18`, `redis`, `mongodb-community`
> - Tools: `curl`, `gh`, `git`, `jq`, `jj`

These become the install/verify tables in the generated `onboard/SKILL.md` Step 2.

### 5.2 Branch conventions

> "What branch naming conventions do you use?"
> - Feature branches: (e.g., `feature/vc-<slug>`, `feat/<name>`)
> - PR target branch: (e.g., `develop`, `main`)
> - Commit format: (e.g., `<type>(<scope>): <description>`)

### 5.3 Any other conventions?

> "Anything else I should know? Review process, team size, special rules, etc."

---

> **Switch to execution mode now.** The user has answered all questions.
> - **Claude Code:** Exit plan mode (normal mode)
> - **Cursor:** Switch to agent mode
> - **OpenCode:** Switch to Build agent (Tab)
>
> **Create a todo checklist now.** Based on all answers, list every file that needs to be created or modified.

---

## Step 6: Create a Branch

```bash
git checkout -b setup/<project-name>
```

## Step 7: Generate Fragments

Based on user's answers, create/update files in `agents/fragments/`:

1. **`service-registry.md`** — Replace with user's services table, start commands, health checks, env files
2. **`session-protocol.md`** — Adapt health checks and service detection to match user's services
3. **`workflow-rules.md`** — Update phase list, branch conventions, gate conditions. Remove sections for phases the user dropped. Add sections for custom phases.
4. **`git-conventions.md`** — Update branch naming, commit format, PR conventions, default branches per service
5. **`prd-conventions.md`** — Keep or adapt based on whether PRD phases are included
6. **`track-conventions.md`** — Keep or adapt based on whether track files are needed

## Step 8: Generate Workflow Schema

Update files in `workflow/`:

1. **`phases.json`** — Only include phases the user selected. Add custom phases.
2. **`gates.json`** — Define gate conditions for each phase transition. Remove gates for dropped phases. Add gates for custom phases.
3. **`state-schema.json`** — Adapt feature schema to match the phases and service structure. Remove unused fields. Always include `phase_status` (`inprogress` | `completed`).

## Step 9: (was Agent Definitions — no agent files anymore)

The orchestrator model needs **no agent files**: the running agent drives all phases, delegation
happens via the harness's subagent capability, and per-task models/effort are chosen at delegation
time (see `workflow-rules.core.md`). Record any custom pinned-model preferences in the
registration notes; skip to Step 10.

## Step 10: Generate Skills

For each skill the user selected, create/update files in `skills/`:

1. **`workflow/SKILL.md`** — Adapt commands to match user's phases and services
2. **`onboard/SKILL.md`** — Rewrite for user's services, stack, tools, MCPs. Include their specific install commands, env file contacts, and health checks.
3. **Other skills** — Adapt or create as needed

## Step 11: Generate Config Files

1. **`onboard/SKILL.md` Step 2** — Build the install/verify tables from the user's pinned package list. Include version checks and health checks for their services.
2. **`AGENTS.md.template`** — Update fragment includes to match what was generated. Remove includes for dropped fragments.

## Step 12: Generate Templates

Update files in `templates/`:

1. **`prd/main-prd.template.md`** — Adapt frontmatter fields to user's services
2. **`prd/service-prd.template.md`** — Same
3. **`tracks/feature.track.template.md`** — Adapt to user's services and phases
4. **`pr/feature-pr.template.md`** — Adapt to user's PR conventions

## Step 13: Update Manifest

1. Compute SHA256 hashes for ALL generated files
2. Update `manifest.json` with correct hashes and install paths
3. Bump version in `VERSION`

## Step 14: Generate Scripts

1. **`scripts/generate-agents.sh`** — Adapt to assemble AGENTS.md from the user's fragments
2. **`scripts/update-check.sh`** — Should work as-is (generic)

## Step 15: Run Generate & Verify

```bash
bash scripts/generate-agents.sh
```

Verify:
- All files in `manifest.json` exist and hashes match
- `phases.json` phases match `state-schema.json` enum
- `gates.json` has entries for all phase transitions
- Agent routing table covers all phases
- No references to `frndos` remain (replaced with user's project name)

## Step 16: Summary

Present the user with:

```
Workspace "<project-name>" generated on branch setup/<project-name>.

Files created/modified:
  agents/fragments/     — <count> fragments
  agents/tools/         — <count> agent definitions
  skills/               — <count> skills
  workflow/             — phases, gates, state schema
  templates/            — <count> templates
  manifest.json         — file registry with hashes

To use this workspace:
  1. Create a new directory for your project
  2. Run the bootstrap script to install files
  3. Open a Claude Code session and run /onboard

Branch: setup/<project-name>
```
