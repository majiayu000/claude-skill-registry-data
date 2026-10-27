---
description: Structured session handoff to another person or AI
argument-hint: "[who you're handing off to]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git log:*, git status:*, git diff:*, date:*)
---

Generate a structured handoff briefing when passing work to another person or AI. Captures context, decisions, risks, and next steps so nothing gets lost in transition.

## Steps

### Step 1: Gather session context

Read:
- `.claude/memory.md` — current state
- Recent daily note — today's work log
- `Task Board.md` — active tasks and priorities
- `git status` and `git log --oneline -10` — recent changes

### Step 2: Identify what was done

From the session context and git history, list:
- **Completed:** Tasks finished in this session
- **In progress:** Work started but not finished (with current state)
- **Decisions made:** Choices and their rationale
- **Files touched:** Every file modified with a one-line summary of the change

### Step 3: Identify what's pending

- **Immediate next steps:** What should happen next (ordered)
- **Blocked items:** Tasks that can't proceed and why
- **Open questions:** Decisions that need input
- **Risks:** Anything that could go wrong if not handled

### Step 4: Context the recipient needs

- **Project context:** What is this project and what matters right now?
- **Key files:** Where to look for the most important things
- **Gotchas:** Non-obvious things that will trip someone up
- **Dependencies:** External people, services, or events this work depends on

### Step 5: Write the handoff

Save to `handoffs/handoff-[date]-[time].md`:

```markdown
# Session Handoff

**From:** [current session / your name]
**To:** [recipient if specified, otherwise "Next session"]
**Date:** [date and time]

---

## Status Summary
[2-3 sentences: where things stand right now]

## What Was Done
- [completed task with file references]
- [completed task]

## What's In Progress
- **[task]** — Current state: [where it's at]. Next action: [what to do next]

## Decisions Made
| Decision | Rationale | Reversible? |
|----------|-----------|-------------|
| [decision] | [why] | Yes/No |

## Files Changed
| File | Change |
|------|--------|
| [path] | [one-line summary] |

## Next Steps (Priority Order)
1. [Most important next action]
2. [Second priority]
3. [Third priority]

## Blocked Items
- **[item]** — Blocked by: [reason]. Unblock by: [action needed]

## Open Questions
- [Question that needs answering before proceeding]

## Risks
- [Risk and what to do about it]

## Key Files to Read
- [file] — [why it matters]
- [file] — [why it matters]

## Gotchas
- [Non-obvious thing that will trip you up]

---
Handoff complete. Read this before starting work.
```

Output the summary section so the user can verify it's accurate.
