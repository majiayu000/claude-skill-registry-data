---
name: esper:init
description: Initialize esper in a project. Interviews the user, writes a constitutional document, defines the first phase, and creates a backlog. Run with a vague prompt — esper will ask the rest.
---

You are initializing the esper agent-powered development toolkit for this project.

## Step 0: Detect existing setup

Run `esperkit config check`. If it exits 0 (project already set up), use `AskUserQuestion` to ask:
  - "Esper is already set up in this project. What would you like to do?"
  - Options: "Update the constitution", "Add a new phase", "Reset everything"
- If it exits non-zero (not set up), proceed to Step 1.

When already set up, the options are:
  - **Update the constitution**: Re-read the existing `.esper/CONSTITUTION.md`, then run Steps 1–2 only (re-interview and rewrite). Keep `esper.json`, phases, and plans untouched.
  - **Add a new phase**: Tell the user to run `/esper:phase` instead — it handles phase transitions properly (archives current plans, bumps phase number, interviews for new scope). Stop.
  - **Reset everything**: Use `AskUserQuestion` to confirm ("This will delete all esper files. Are you sure?"). If confirmed, delete `.esper/` entirely and proceed from Step 1.

## Step 1: Interview the user

Use `AskUserQuestion` to interview the user. Cover these areas in 2–3 rounds — do not ask everything at once.

**Round 1 — Project vision** (use AskUserQuestion with these as questions):
- What is this project and what problem does it solve?
- What is it explicitly NOT? (scope boundaries — what will never be built here)
- Who are the primary users?

**Round 2 — Technical decisions** (use AskUserQuestion):
- What is the tech stack? (language, framework, runtime)
- What commands run tests, lint, and typecheck? (can be empty strings if not set up yet)
- What command starts the dev server? (can be empty)

**Round 3 — Process** (use AskUserQuestion):
- Testing strategy: what gets tested, how, with what tooling?
- Backlog mode: local files (`.esper/plans/`) or GitHub Issues?
  - If GitHub Issues: confirm `gh` CLI is installed and repo has a remote origin

## Step 2: Write CONSTITUTION.md

Create `.esper/` directory if it doesn't exist. Write `.esper/CONSTITUTION.md`:

```markdown
# [Project Name] — Constitution

## What This Is
[1-3 sentences on the project's purpose and users]

## What This Is NOT
[Explicit scope boundaries — what we will never build here]

## Technical Decisions
- **Stack**: [language, framework, runtime]
- **Architecture**: [key patterns, conventions]
- **Key dependencies**: [important libs and why]

## Testing Strategy
- **What gets tested**: [unit / integration / e2e — and what doesn't]
- **Tooling**: [test runner, assertion library]
- **Commands**: [how to run tests]

## Principles
[3-5 development principles specific to this project]
```

## Step 3: Write esper.json

Write `.esper/esper.json`:

```json
{
  "backlog_mode": "local",
  "current_phase": "001-<kebab-slug-from-phase-title>",
  "commands": {
    "test": "<from interview, or empty string>",
    "lint": "<from interview, or empty string>",
    "typecheck": "<from interview, or empty string>",
    "dev": "<from interview, or empty string>"
  }
}
```

Set `backlog_mode` to `"github"` if the user chose GitHub Issues.

## Step 4: Define Phase 1

Use `AskUserQuestion` to ask the user about MVP scope:
- What is the minimum version that delivers real value?
- What are the acceptance criteria — how do we know this phase is done?
- What is explicitly deferred to later phases?

Create `.esper/phases/` if it doesn't exist. Derive a kebab-case slug from the phase title (e.g. "MVP" → `001-mvp.md`, "Polish and Publish" → `001-polish-and-publish.md`). Write `.esper/phases/001-<slug>.md`:

```markdown
---
phase: 001-<slug>
title: <title from interview>
status: active
---

# Phase 1: <title>

## Goal
[What this phase delivers and why it matters]

## In Scope
- [feature or deliverable]
- [feature or deliverable]

## Out of Scope (deferred)
- [explicitly deferred items]

## Acceptance Criteria
- [ ] [measurable criterion]
- [ ] [measurable criterion]
```

## Step 5: Decompose into backlog items

Break phase 1 into atomic tasks — each task is one PR worth of work.

Create `.esper/plans/pending/`, `.esper/plans/active/`, `.esper/plans/done/`, `.esper/plans/archived/` directories if they don't exist.

For each task, write `.esper/plans/pending/NNN-slug.md` (NNN = zero-padded integer starting at 001).

Each plan has a `type:` field — ask (or infer from context) whether each item is a fix or a feature:
- `type: "fix"` → standalone patch, its own PR on ship → `branch: fix/[kebab-slug]`
- `type: "feature"` → part of the phase, batched into a phase PR → `branch: feature/[current_phase]` (e.g. `feature/001-mvp`)

```markdown
---
id: 001
title: [task title]
status: pending
type: feature
priority: 1
phase: 001-<slug>
branch: feature/001-<slug>
created: [today's date in YYYY-MM-DD format]
---

# [Task title]

## Context
[What exists in the codebase relevant to this task — explore before writing]

## Approach
[Step-by-step implementation plan]

## Files to change
- [file path] ([create/modify] — [why])

## Verification
- Run: [test command]
- Expected: [what passing looks like]
- Edge cases: [anything non-obvious to verify]
```

Assign priorities: 1 = must ship first (blocking), higher number = can wait.

If `backlog_mode` is `"github"`, create ONE GitHub issue for the entire phase (not per plan — features are batched into one phase PR):
```bash
gh issue create --title "Phase 1: [phase title]" --body "[phase goal and scope summary]"
```
Store the returned issue number as `gh_issue: <number>` in the phase file frontmatter (`.esper/phases/001-<slug>.md`).

## Step 6: Install hooks

Check if `.claude/settings.json` exists.

- If it does not exist, create it with the hooks below.
- If it exists, read it first, then merge the hooks into the existing JSON — do not overwrite any existing keys.

Add these hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "bash .esper/hooks/verify-quick.sh" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "bash .esper/hooks/session-reminder.sh" }]
      }
    ]
  }
}
```

Create `.esper/hooks/` directory if it doesn't exist.

Create `.esper/hooks/verify-quick.sh`. Write the actual commands from the interview as literal strings — do NOT use variable interpolation or eval. Omit any block for commands the user left empty:

```bash
#!/usr/bin/env bash
# Generated by esper:init. Commands are project-specific and static.
FAILED=0

echo "--- esper: lint ---"
npm run lint
[ $? -ne 0 ] && FAILED=1

echo "--- esper: typecheck ---"
npm run typecheck
[ $? -ne 0 ] && FAILED=1

if [ $FAILED -ne 0 ]; then
  echo ""
  echo "esper: verification failed — fix the errors above before continuing."
fi

exit 0
```

(The example above shows `npm run lint` and `npm run typecheck` — replace with the actual commands from the interview, or omit the block entirely if the user left that command empty.)

Create `.esper/hooks/session-reminder.sh`:

```bash
#!/usr/bin/env bash
REMINDERS=()

UNCOMMITTED=$(git status --porcelain 2>/dev/null)
if [ -n "$UNCOMMITTED" ]; then
  CHANGED=$(echo "$UNCOMMITTED" | wc -l | tr -d ' ')
  REMINDERS+=("  ! $CHANGED uncommitted file(s) — run /esper:finish when ready")
fi

ACTIVE_PLANS=$(ls .esper/plans/active/*.md 2>/dev/null)
if [ -n "$ACTIVE_PLANS" ]; then
  PLAN=$(head -5 .esper/plans/active/*.md | grep '^title:' | head -1 | sed 's/title: //')
  REMINDERS+=("  > active plan: $PLAN")
fi

PENDING=$(ls .esper/plans/pending/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$PENDING" -gt 0 ]; then
  REMINDERS+=("  · $PENDING pending item(s) in backlog — run /esper:backlog to review")
fi

if [ ${#REMINDERS[@]} -gt 0 ]; then
  echo ""
  echo "esper:"
  for r in "${REMINDERS[@]}"; do echo "$r"; done
fi

exit 0
```

Make both scripts executable:
```bash
chmod +x .esper/hooks/verify-quick.sh .esper/hooks/session-reminder.sh
```

## Step 7: Summary

Print a summary covering:
- Constitution written to `.esper/CONSTITUTION.md`
- Phase 1 defined in `.esper/phases/001-<slug>.md`
- N backlog items created in `.esper/plans/pending/`
- Hooks installed in `.esper/hooks/` and `.claude/settings.json`
- Next step: "Run `/esper:backlog` to see your backlog, then `/esper:apply` to start building."
- Note: "For future phases, use `/esper:phase` when Phase 1 is complete."
