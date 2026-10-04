---
name: workflow
description: Activates a structured development session with PLAN.md-driven subagent delegation and HISTORY.md tracking. Invoke when the user wants a disciplined, context-efficient workflow using plan agents, execute agents in worktrees, and append-only history. Argument is the docs directory (defaults to cwd).
argument-hint: <docs-dir>
---

# Workflow Skill

A session protocol that fights context bloat by using files as primary memory and subagents as context shields. The main agent orchestrates; plan and execute agents do the work in isolation.

## Core Recipe

### Step 1 — Session Start

Determine `DOCS_DIR` from the argument, or default to the current working directory.

Check for `PLAN.md` in `DOCS_DIR`:
- **Found**: Read it. Summarize the current goals and feature backlog to the user. Ask which feature to work on next.
- **Not found**: Tell the user no `PLAN.md` exists. Draft one from context (ask clarifying questions if needed). Present the draft and ask the user to approve or edit it before saving.

Also read `FEATURES.md` and `HISTORY.md` if they exist — use them to understand what has already been built and what decisions were made.

### Step 2 — Feature Loop

For each feature the user selects:

**2a. Plan Agent**

Spawn a foreground `general-purpose` agent with this prompt (fill in `[DOCS_DIR]` and `[FEATURE]`):

```
You are a Plan Agent. Your job is RESEARCH AND PLANNING ONLY — do not write or edit any code.

Read the following files if they exist:
- [DOCS_DIR]/PLAN.md
- [DOCS_DIR]/FEATURES.md
- [DOCS_DIR]/HISTORY.md

Then produce an implementation plan for: [FEATURE]

Your plan must include:
1. Files to create or modify (with paths)
2. Approach and key design decisions
3. Anything in PLAN.md that constrains this feature
4. Any risks or open questions

Return ONLY the plan. Do not implement anything.
```

Present the plan to the user. Ask for approval or changes. Iterate until approved.

**2b. Execute Agent**

Spawn an `isolation: worktree` `general-purpose` agent with this prompt:

```
You are an Execute Agent. Implement the following approved plan.

Docs directory: [DOCS_DIR]
Read PLAN.md, FEATURES.md, and HISTORY.md before starting.

Approved plan:
[PLAN FROM PLAN AGENT]

When done:
1. Append an entry to [DOCS_DIR]/FEATURES.md in this format:

## [FEATURE NAME]
- Agent ID: [your agent session identifier or a short UUID]
- Branch: [worktree branch name]
- Built: [1-2 sentence summary of what was built]
- Files changed: [comma-separated list]
- Key decision: [the most important design choice made]

2. Return a 3-4 line summary and the branch name.
```

### Step 3 — Review & Merge

After the execute agent reports back:

1. Run `git diff main...[branch]` to review changes.
2. Ask the user to approve the diff.
3. If approved, merge the branch (or let the user merge manually).
4. **Append to `HISTORY.md`**:

```markdown
## [DATE] — [FEATURE NAME]

- Branch merged: [branch]
- Built: [what was implemented]
- Key decisions: [reasoning behind main choices]
- Pivots: [any reversals or scope changes, with why]
```

5. Ask the user if they want to continue with another feature (return to Step 2) or end the session.

---

## File Contracts

### `PLAN.md`
- Forward-looking: goals, architecture, constraints, non-negotiables, feature backlog
- Features are marked done when complete — never deleted
- Save important decisions made during the session here
- **Agents read this file; they never write it.** Only the user (with your help) updates it.

### `FEATURES.md`
- One entry per completed feature
- Each entry: agent ID, branch, what was built, files changed, key decision
- Append-only — do not edit past entries

### `HISTORY.md`
- Append-only session log
- Each entry: date, feature + branch merged, key decisions and reasoning, pivots with why
- Purpose: fast context recovery after compaction or in a new session

---

## When Applying This Skill

1. Confirm `DOCS_DIR` — is the user passing an explicit path or using cwd?
2. Always read all three files before spawning any agent, even if they don't all exist yet.
3. Never let a plan agent write code. If it does, discard the result and re-spawn.
4. Worktree isolation for execute agents is mandatory — it keeps main clean and makes diffs clean.
5. After every merge, update `HISTORY.md` before asking about the next feature.
6. If `PLAN.md` becomes stale during the session, update it with the user before continuing.
