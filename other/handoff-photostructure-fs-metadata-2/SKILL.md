---
name: handoff
description: Update TPP for engineer handoff when context is running low. Use when ending a session, running out of context, or switching to a different task.
disable-model-invocation: false
allowed-tools: Read, Edit, Write, Glob, Grep
---

# TPP Handoff

We're out of time or context and need to hand off the remaining work
so the next session can pick up exactly where we left off.

## Required Reading First

Before any work, you MUST read:

- **CLAUDE.md** — project conventions, critical knowledge, anti-patterns, and CI/CD constraints
- **doc/TPP-GUIDE.md** — how TPPs work in this project
- **doc/C++\_REVIEW_TODO.md** — C++ review checklist (when native code was touched)

## Your Task

1. Find the active TPP in `_todo/` (use Glob for `_todo/*.md`)
2. Re-read the TPP thoroughly
3. Update it with everything the next session needs to know:

### Progress Update

- Mark completed tasks with `[x]`
- Update the "Current phase" checklist
- Note partial progress on in-flight tasks

### Discoveries & Lore

- Add non-obvious findings to the Lore section
- Document any gotchas encountered
- Record platform-specific behaviors discovered

### Failed Approaches

- Document what was tried and didn't work, and WHY
- This prevents the next session from repeating mistakes

### Remaining Work

- Clarify what remains and the recommended next step
- Note any blockers or open questions
- If the approach changed from the original plan, explain why

### Context for Next Session

- Add a "Next steps" section at the top of the Tasks list
- Include file paths and line numbers for work in progress
- Reference any relevant test output or error messages

## Quality Check

Before finishing, verify the TPP answers these questions:

- Could a new session pick this up cold and make progress immediately?
- Are all dead ends documented so they won't be re-explored?
- Is the current state of the code accurately reflected?
