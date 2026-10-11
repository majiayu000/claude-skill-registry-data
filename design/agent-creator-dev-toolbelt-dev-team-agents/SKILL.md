---
name: agent-creator
description: Creates and validates agent files for the dev-team-agents repository. Enforces all authoring standards from CLAUDE.md — frontmatter, model assignment, required sections, line limit, and Worktree Isolation for coding agents. Use when creating a new agent or auditing an existing one for compliance.
---

# Agent Creator

This skill guides creation and validation of agent files in `agents/`. It is a maintenance tool for this repository — it does not get distributed to target projects.

Source of truth for all rules: `CLAUDE.md § Authoring Standards`.

---

## Activation Flow

1. Ask the user: **agent name**, **role description**, and **agent type** (coding or non-coding)
2. Determine the correct model (see table below)
3. Present a plan showing: file path to be created, model chosen, sections to include, and any registration steps needed — then state **"Awaiting your approval before proceeding."**
4. Draft the agent file following the structure below
5. Run the **Validation Checklist** before presenting the result
6. Run the **Post-Creation Checklist** after the file is written

---

## Model Assignment

| Agent type | Model |
|---|---|
| Decision-making (architect, analyst, reviewer) | `claude-opus-4-7` |
| Execution (developer, specialist, writer) | `claude-sonnet-4-6` |
| Structured output only | `claude-haiku-4-5-20251001` |

When in doubt, use `claude-sonnet-4-6`.

---

## Required Structure

Every agent must have these sections in this order:

```markdown
---
name: <agent-name>
description: <what it does and when to use it>
model: <see model table>
tools: Read, Write, Edit, Bash, Glob, Grep   ← adjust as needed
---

You are a **[Role Name]** — [one sentence defining the role and mindset].

## Foundational Rule — Load Context First

Before any action, load the project context in this order:

1. `README.md`, `CLAUDE.md`, `AGENTS.md` — project conventions
2. `docs/project.md` — synthesized project overview
3. `.claude/user-data/session-summary.md` — most recent entry only (topmost ## block)
4. `docs/backlog/` — current scope and task definition
5. `docs/development/` — architecture, tech stack, code standards
6. Run `git log --oneline -20` — recent patterns and active areas

**Project rules override base standards. Always.**

Follow `skills/shared/plan-mode/SKILL.md` before any non-trivial task.

---

## [Core Behavior Sections]

[Agent-specific behavior here. Keep each section focused.]

---

## Immutability Warning

This file is installed via symlink into user projects. Do not modify it
directly inside a project — changes will be lost on the next update.
To change behavior: edit the source in the dev-team-agents repository.
```

---

## Worktree Isolation (coding agents only)

Coding agents — `backend-developer`, `frontend-developer`, `database-specialist`, `devops-specialist`, `ui-ux-designer`, `backend-test-specialist`, `frontend-test-specialist` — must include this section after Foundational Rule:

```markdown
## Worktree Isolation

1. Read `.dev-team-agents/.worktree-session`:
   - If present: follow stored decision silently (`worktree=no` or `worktree=yes branch=<b>`)
   - If absent: ask the user once, write the decision, then act
2. On `worktree=yes`: load `skills/shared/worktree/SKILL.md` with the provided branch (default: `main`)
```

This ensures multi-agent workflows ask the worktree question exactly once.

---

## Validation Checklist

Run before finalizing any agent file:

- [ ] Frontmatter has all four fields: `name`, `description`, `model`, `tools`
- [ ] `name` matches the filename (e.g., `name: backend-developer` → `agents/backend-developer.md`)
- [ ] `description` answers: what does it do + when to invoke it
- [ ] Model matches the agent type (see model table)
- [ ] `## Foundational Rule` section present
- [ ] `## Immutability Warning` section present
- [ ] If coding agent: `## Worktree Isolation` section present with correct pattern
- [ ] No hardcoded framework, language, or tool references in core behavior
- [ ] File is ≤ 200 lines — move reference material to a skill if over the limit
- [ ] All content is in English

---

## Post-Creation Checklist

Run after the file is written:

- [ ] Run orphan scan: `bash helpers/orphan-skill-scan.sh` — resolve any ACTION REQUIRED lines before closing
- [ ] Auto-Docs Rule: if the new agent changes observable behavior (new capability, renamed agent, changed tools list) → update `README.md` and `README.pt-BR.md` in the same session

---

## Auditing an Existing Agent

To validate an existing agent without creating a new one:

1. Read the agent file
2. Run the Validation Checklist above
3. Report each violation with the line number and the fix required
4. Do not auto-fix — present findings and wait for approval

---

## Registering the New Agent

After creating the file, check if the agent should be referenced from any existing agent. Common registration points:

| Agent | Registers what |
|---|---|
| `agents/setup-assistant.md` | New agents that participate in project setup |
| `agents/software-architect.md` | Agents that make architectural or quality decisions |
| `CLAUDE.md § User-Invocable Skills` | Only if triggered directly via slash command |
