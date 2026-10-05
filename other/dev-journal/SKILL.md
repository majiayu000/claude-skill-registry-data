---
name: dev-journal
description: Write or update the narrative session entry in docs/development-journal.md. Captures decisions, learning, and AI tooling observations. MANDATORY before every commit. TRIGGER when the user says "update the journal", "write a journal entry", "log the session", or when preparing to commit (should auto-check if journal is current).
---

# Development Journal Entry

Write or update the session narrative in `docs/development-journal.md`.

## Current Context

- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Changes this session: !`git diff --stat`

## Journal Entry Format

Entries are reverse chronological (newest at top). Each session gets one entry.

### Template

```markdown
### Session [N] — [Date] — [Milestone]

**What happened**: [1-3 sentences summarizing the session's work]

**Key decisions**:
- [Decision 1 and rationale]
- [Decision 2 and rationale]

**Learning**:
- [Non-obvious thing discovered]
- [Pattern or approach that worked well/poorly]

**AI tooling observations**: [How Claude Code helped or hindered — what worked, what didn't]

**What's next**: [What the next session should pick up]

**Retro** (include when completing a milestone):
- Estimate vs actual: [Xh estimated, Yh actual]
- What surprised you: [unexpected complexity, discovery, or outcome]
- Process improvement: [what would help next time]
```

## Rules

1. **Read the existing journal first** — check the latest session number and continue the sequence
2. **Be narrative, not mechanical** — explain WHY decisions were made, not just what was done
3. **Capture learning** — the journal's value is in recording insights that prevent future mistakes
4. **Include AI observations** — how was Claude Code used? What prompts worked well? What was frustrating?
5. **Write DURING the session** — do not defer to end. Sessions can be interrupted or run out of context.
6. **Every commit should have a current journal** — treat this as a hard requirement

## Verification

- [ ] Session number is sequential (check previous entry)
- [ ] Date is correct
- [ ] Milestone reference uses PREFIX-#.# format
- [ ] Entry captures at least one decision with rationale
- [ ] Entry captures at least one learning item
