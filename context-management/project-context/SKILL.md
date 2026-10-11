---
name: project-context
description: Foundational rule — context, coexistence, Plan Mode, language, credentials.
---

# Project Context Loading — Coexistence & Override Rule

This is the **foundational rule** for all agents in `dev-team-agents`. Read and apply it before acting on any task.

---

## Core Principle

> The `dev-team-agents` standards are the **base layer**. Any rule, pattern, or convention defined explicitly in the project overrides our base. We provide the floor — the project sets the ceiling.

This means every agent must:
1. Load and understand the project's own context
2. Identify where the project has explicit conventions
3. Apply project conventions where they exist; apply base standards where they don't

---

## First-Time Setup Guard

**Trigger: `[DEVTEAM:FIRST_TIME_SETUP]` at the start of a session.** Stop immediately — before
loading any other context or answering the original prompt — and load the full guard:
`skills/shared/project-context/references/first-time-setup.md`

---

## Language Policy

### Documents — Always English

**All generated documents, code comments, commit messages, and technical output must be written in English.**

This applies to:
- Architecture documents (`docs/development/`)
- Backlog items, sprint plans, and estimates (`docs/backlog/`)
- API contracts, code standards, design system docs
- Changelog entries and PR descriptions

**Exception**: if the user explicitly requests a document in another language (e.g., "write this in Portuguese"), honor that request for that specific document only. Default always reverts to English.

### Conversation — User's Preferred Language

**All responses directed at the user — including plans presented for approval, explanations, questions, confirmations, and notifications — must use the language in `.dev-team-agents/resolved/preferences.json` → `language` field.**

Read this value at the start of every session:

```bash
python3 -c \
  "import json; d=json.load(open('.dev-team-agents/resolved/preferences.json')); print(d.get('language','en'))" \
  2>/dev/null || echo "en"
```

If `preferences.json` does not exist or is unreadable, default to English and emit a `warning` notification prompting the user to configure preferences.

This rule applies to: explanations, questions, confirmations, summaries, notifications, and all user-facing text. It does NOT apply to document content, code comments, or commit messages.

Notifications (context window, stale config, tips) are raised by hooks and shown by the desktop app — never print a `DEV TEAM AGENTS` box. `skills/shared/notifier/SKILL.md` says what raises what, and how a hook adds a new one.

---

## Mandatory Plan Mode — No Silent Execution

**Load `skills/shared/plan-mode/SKILL.md` before executing any non-trivial task.** It owns the full when-a-plan-is-required table, the plan format, and the approval protocol — do not restate it here.

---

## Memory Layers

**This is the canonical map of the project's memory.** Every artifact below has exactly one job. Agents route by it; they do not restate it.

| Layer | Artifact | Holds | Lifespan |
|-------|----------|-------|----------|
| **Structural** | `docs/project.md`, `docs/development/*.md` | Current state: stack, architecture, standards | Rewritten in place — always describes now |
| **Episodic** | `<memory-dir>/session-summary.md` (`.dev-team-agents/memory-dir` pointer → portable memory) | What happened, in order | Decays (rotation policy below) |
| **Semantic** | `docs/wiki/` | What isn't derivable from the code | Permanent; superseded, never deleted |
| **Decisional** | `docs/development/adrs/` | Why a hard-to-reverse choice was made | Permanent and immutable |
| **Mechanical** | `graphify-out/graph.json` | Where things are in the code | Regenerated — never hand-written |

### Routing — which layer gets this?

Three questions, in order. The first "yes" wins:

1. **Is it derivable by reading the code?** → None of them. Do not write it down. This is the rule that keeps memory from becoming a second, aging source of truth that contradicts the repository.
2. **Is it a hard-to-reverse choice with non-obvious reasoning?** → ADR.
3. **Will it still be true after this sprint?** → Wiki if it's knowledge, structural docs if it's current state. If no → session summary, and let it decay.

A single finding lands in **one** primary layer. It may be referenced from another; it is never copied into one.

`/devteam:learn` is the promotion path from episodic to the durable layers, and the Promotion Guard below is what stops the episodic layer from expiring with unpromoted knowledge in it.

---

## Context Loading Order

Before starting any task, load context in this order (read what exists — skip what doesn't):

```
1. README.md                              ← project overview, setup, conventions
2. CLAUDE.md                              ← Claude-specific rules (highest precedence)
3. docs/project.md               ← synthesized project overview; if present, use it to
                                             orient fast before reading individual dev files
4. <memory-dir>/session-summary.md        ← last session's decisions and next steps; read the
                                             most recent entry (top of file). See `layout` below
5. docs/development/adrs/        ← list ADR files and read any relevant to the task
6. AGENTS.md                             ← agent-specific instructions for this project
7. .claude/settings.json                 ← Claude Code configuration
8. .agents/ (directory)                  ← project-level agent overrides
9. docs/development/             ← architecture, code-standards, tech-stack
10. docs/backlog/                ← current sprint and task context
11. docs/wiki/README.md          ← retrieval index; grep it for the task's keywords and
                                             open only the entries that match
12. extra context_paths                   ← additional knowledge folders this project declares;
                                             read-only, and only what the task needs
```

**Steps 4 and 12 resolve through the project's own configuration, not a fixed path.**

`.dev-team-agents/project.json` (committed) declares where this project's knowledge lives:

```json
{ "schema": 1, "project_id": "…", "layout": 2, "context_paths": ["docs", "rfcs"] }
```

- **`context_paths`** — the first entry is the write root (`docs` by default, which is what every
  path above assumes). Any additional entry is an **extra knowledge folder, read-only**: read from
  it when the task's subject matter is there, and never write to it. A folder that is not listed is
  not project knowledge, however suggestive its name.
- **`layout`** — where the project's own state lives. Layout 1 means `.dev-team-agents/user-data/`
  (both machine-local state and portable memory together). Layout 2 means the data store, with two
  one-line pointer files: `.dev-team-agents/state-dir` (machine-local state directory)
  and `.dev-team-agents/memory-dir` (portable memory directory). Read the pointers rather than
  guessing paths; `scripts/lib/state.sh` already resolves them for every bash caller.

`context_paths` is topology, not preference — it is committed so every developer on the project
reads the same folders. Preferences are personal and never committed; see § User Preferences.

**When `docs/project.md` exists**, it provides a pre-synthesized orientation (stack, active areas, key constraints) that reduces the need to read multiple raw files from scratch. Read it at step 3, then load only the specific `development/` files relevant to the current task instead of reading the entire directory.

After reading `project.md`, extract the `<!-- last-updated: YYYY-MM-DD -->` field from line 1. If the date is more than 30 days in the past, include this warning at the top of your first response:

> ⚠️ `project.md` may be stale (last updated: YYYY-MM-DD). Consider running `setup-assistant` in REFRESH mode to bring it up to date.

**When `<memory-dir>/session-summary.md` exists** (path resolved via `.dev-team-agents/memory-dir` pointer on layout 2, or `.dev-team-agents/user-data/` on layout 1), read only the most recent entry (the topmost `## YYYY-MM-DD` block). It captures what was done last session, decisions made, and what comes next — use it to avoid re-asking questions that were already resolved.

**When `docs/development/adrs/` exists**, list its files and read any ADR whose title is relevant to the current task. This prevents contradicting or duplicating past architectural decisions.

**When `docs/wiki/README.md` exists**, read that index — and only that index. Derive two or three keywords from the task (domain nouns, component names, the error being chased) and match them against the **Keywords** column; open only the entries that hit. Never load the wiki directory: the index exists precisely so that context cost stays flat as the wiki grows. An empty match set is a valid result — proceed without opening anything.

This is the wiki's **read** path. Writing entries is `skills/shared/docs-sync/references/wiki-format.md`, which owns the index row format the lookup depends on.

Read each file that exists. Combine the information into a unified understanding of the project before acting.

**Trivial-task exception**: when the task is confined to a single file with a small, well-specified change — the same bar as the Plan Mode "single-line typo fix" exception in `skills/shared/plan-mode/SKILL.md` — skip this loading order entirely and load only `CLAUDE.md` plus the target file. Fall back to the full order the moment the task turns out to touch more than one file or needs architectural context.

---

## Session Summary — Write Rules

**Trigger: you are about to write or trim the session summary file (resolved via `.dev-team-agents/memory-dir`).** Load
the full write rules (multi-agent append format, rotation policy, Promotion Guard) before doing so:
`skills/shared/project-context/references/session-summary-write-rules.md`

---

## Contradiction Guard

Automatically enforced by all agents. Load details on-demand: `skills/shared/project-context/references/contradiction-guard.md`

---

## Wiki Knowledge Base

Every project gets a wiki at `docs/wiki/`. Load full protocol: `skills/shared/project-context/references/wiki.md`

---

## Override Logic

When a conflict exists between our base standard and a project convention:

| Scenario | Rule |
|----------|------|
| Project CLAUDE.md defines a code style | Use the project's style |
| Project uses tabs, we recommend spaces | Use tabs |
| Project has no defined convention | Apply our base standard |
| Project explicitly states "do not use X" | Never use X, even if we recommend it |
| Project is ambiguous or silent on a topic | Apply our base standard and note the assumption |

**Explicit beats implicit.** A project convention must be clearly stated to override a base standard — don't infer overrides from one or two examples.

---

## Immutability Warning

**Trigger: a user asks to modify any file inside `.dev-team-agents/`.** Load the full warning text
before responding: `skills/shared/project-context/references/immutability-warning.md`

---

## Applying Combined Context

When base standard and project context are both present, produce output that:

1. Follows the project's conventions for naming, style, structure, and tools
2. Fills gaps with our base standards
3. Explicitly calls out assumptions: `"No convention found for X in project context — applying base standard: [rule]"`

Example: if the project uses PHPDoc for all methods but our base standard says "only when WHY is non-obvious", follow the project — it has an explicit convention.

---

## Interaction Patterns — Quiz-first Rule

**Load `skills/shared/interaction-patterns/SKILL.md` before asking the user any question.**

The skill defines when and how to use the `AskUserQuestion` tool (quiz format with Yes/No, multiple-choice, or "Other" for open input) instead of plain text prompts. Apply it to every confirmation, choice, and gate in your workflow.

---

## Test Execution — Scoped by Default

**Load `skills/shared/scoped-test-execution/SKILL.md` before running any test command.**

This binds **every** agent, not only the test specialists. If your task ends with you invoking a test runner — implementing, fixing, refactoring, reviewing, or validating — you run only the tests covering the code you touched. The project's full suite runs on one signal and one only: the user asking for it in this session.

| Situation | What runs |
|-----------|-----------|
| You changed code and want to verify it | Tests covering the change and its direct dependents |
| A scoped test failed | Fix it — a failure never authorizes widening the run |
| The change touches shared code, or the suite is fast | Still scoped. Neither is an escalation signal |
| The request is vague ("make sure nothing broke") | Still scoped. Offer the full run; do not start it |
| The user explicitly asked for the whole suite | Full suite |
| A CI pipeline is executing | Full suite — this rule governs local runs only and never constrains a pipeline |

Load the skill for the blast-radius derivation and the per-stack runner filters. Do not work from this table alone.

---

## Quality / Security Scanners

Detect and load the appropriate skill when any scanner config is present:

| Detection | Skill to load |
|-----------|--------------|
| `sonar-project.properties`, `.sonarcloud.properties`, or `SONAR_TOKEN` env var | `skills/devops/sonarqube/SKILL.md` |

When loaded, the scanner skill governs: quality gate reporting, security hotspot handling, coverage thresholds, and how findings surface in reviews and QA reports.

---

## Development Environment

Detect and load the appropriate skill when the environment signal is present:

| Detection | Skill to load |
|-----------|--------------|
| `docker-compose.yml`, `docker-compose.override.yml`, or `compose.yml` at the root | `skills/devops/docker-dev/SKILL.md` |

When loaded, that skill governs the command execution contract: every command runs inside the
container, which compose form to use, and the explicit-host exception.

---

## Remote Environment Credentials

When a task requires accessing a remote environment (staging, production, QA, etc.):

1. **Load** `skills/shared/credentials/SKILL.md` and follow its instructions
2. **Read** credentials from `.dev-team-agents/credentials.local.json` in the main checkout (resolve its path as `skills/shared/credentials/SKILL.md` § How to Use describes)
3. If fields are empty, ask the user for access details
4. **Read-only by default** — ask permission before any write/execute operation

This applies to SSH, database, HTTP/HTTPS, Docker, Kubernetes, and any other remote access.

---

## What Counts as "Project Context"

- Explicit rules in CLAUDE.md, README.md, AGENTS.md
- Existing code patterns (if consistent across 3+ files, treat as a convention)
- Linter/formatter config files (`.eslintrc`, `phpcs.xml`, `.prettierrc`, `pyproject.toml`, etc.)
- CI/CD config that enforces checks (failing lint = enforced rule)
- Architecture docs in `docs/development/`

What does **not** count:
- One-off examples in a single file
- Commented-out code
- TODO comments
