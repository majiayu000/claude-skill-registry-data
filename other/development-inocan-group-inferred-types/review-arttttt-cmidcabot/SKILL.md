---
name: review
description: "Code review. Use when the user invokes /review or asks for a review of changes tied to an issue."
---

# Review Command

## Behavior Profile

Use the `reviewer` skill as the behavior profile for this command.
Treat its rules as mandatory.

Follow `CLAUDE.md`, `conventions.md`, and `ARCHITECTURE.md`.

## Task

Conduct code review and record findings.

## Interaction Contract

1. Read issue details and change scope.
2. Perform review and prepare verdict.
3. Show verdict and ask about unrelated issues.
4. Save review comment via `beads`.

## Algorithm

### Step 1: Get issue

- If ID missing → ask "Which issue to review?"
- Normalize ID: add `DCATgBot-` prefix if missing
- Use `beads` to get issue details
- Determine scope: changed files from branch

### Step 2: Review

- Read `ARCHITECTURE.md` and `conventions.md` first
- Review checklist: correctness, architecture, security, code quality
- Categorize: related vs unrelated findings
- Produce verdict

### Step 3: Confirm

```
## Review Complete
Status: <verdict>

### Related Findings
<related>

### Unrelated Issues
<unrelated>
---
Create issues for unrelated? (yes/no/select)
```

### Step 4: Record

- Save review as comment via `beads`
- If approved: create issues for unrelated with `discovered-from` dependency

### Step 5: Report

**Needs work:**
```
Review complete. Status: Needs work.
Critical: [C1], [C2]...
Next: /fix <id>
```

**Approved:**
```
Review complete. Status: Approved.
Ready for merge.
```

## Findings Format (for comment)

```markdown
## Review

**Status:** Needs work | Approved
**Date:** <YYYY-MM-DD>

### Critical
- [C1] Description — `file:line`

### Should Fix
- [S1] Description — `file:line`

### Consider
- [N1] Description — `file:line`

### Verdict
<Summary>
```

## Important

- Never skip verdict confirmation
- Never implement fixes during review
- Use `beads` for comments and issue creation
