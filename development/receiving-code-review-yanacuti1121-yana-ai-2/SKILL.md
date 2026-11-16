---
name: receiving-code-review
description: "Use when you receive review feedback on your own code or changes. Triggers on: 'reviewer said', 'PR feedback', 'review comments', 'address the feedback', 'fix the review'. Classifies feedback into must-fix / optional / reject-with-reason."
---

# Receiving Code Review Skill

Review feedback is not a to-do list to blindly execute.
Classify each item, act on what matters, and justify what you decline.

## When to use this skill

- You receive review comments on a PR or diff you wrote
- Someone flags issues in code you produced
- User asks you to "address the feedback" or "fix the review comments"

## Step 1 — Read all feedback before acting

Do not start editing on the first comment. Read everything first.
Build a complete picture of what the reviewer is asking.

## Step 2 — Classify each comment

| Category | Definition | Action |
|----------|-----------|--------|
| **Must fix** | Correctness bug, security issue, data loss risk | Fix immediately |
| **Should fix** | Real concern, reasonable improvement | Fix unless there's a strong reason not to |
| **Optional** | Style, preference, minor nitpick | Fix if fast (<5 min), otherwise note and move on |
| **Reject** | Disagrees with an intentional design choice | Respond with reasoning, do not change code |

## Step 3 — Act

For each **must-fix** and **should-fix**:
1. Make the change
2. Confirm the fix with evidence (diff or test output)
3. Reply to the reviewer with what you changed

For each **optional**:
- If fast: do it
- If not: "Noted, deferring — [why]"

For each **reject**:
- Write a clear explanation: "This is intentional because [X]. I'm keeping it as is."
- Do not change the code under social pressure alone

## Step 4 — Do not over-accept

Signs you are over-accepting:
- Applying every comment without reading context
- Changing code you are confident was correct
- Letting the reviewer's style override your project's conventions

If a comment would break something or contradict a documented decision: push back.

## Response format (for PR reply)

```markdown
Thanks for the review. Here's what I did:

**Fixed:**
- [comment ref] [what I changed] — [file:line]

**Deferred:**
- [comment ref] [why — e.g. out of scope, separate ticket]

**Not changing:**
- [comment ref] [reason — e.g. this is intentional because X]
```

## After applying changes

Run tests and use `verify-before-done` before marking the PR ready again.
