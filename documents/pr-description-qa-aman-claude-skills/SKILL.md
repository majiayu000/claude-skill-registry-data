---
name: pr-description
description: >
  Write a clear pull request description. Use when the user says "write a PR description",
  "PR template", "pull request description", "how do I describe this change",
  "commit message for this", "document this change", "open a PR for",
  or is about to merge code and needs to communicate what changed and why
  - even if they don't explicitly say "PR description".
---

## Overview

Based on **"The Pragmatic Programmer"** by Hunt & Thomas. Hunt & Thomas: "It's not just code you're writing - it's communication." A PR description is a letter to your reviewers (and to your future self). It should answer: what changed, why it changed, how to verify it, and what to watch out for. A reviewer who has to read all the code to understand the PR is doing your job for you.

## Workflow

### Step 1: Write the title
Format: `[type]: [short description in imperative mood]`

Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`

Rules:
- Imperative mood: "add pagination" not "added pagination" or "adds pagination"
- Under 72 characters
- Specific: "fix null pointer in payment processing" not "fix bug"

### Step 2: Write the Summary
2-4 sentences. Answer: what does this PR do?

Write for someone who hasn't seen the issue, ticket, or conversation. They should understand the change from this paragraph alone.

### Step 3: Write the Motivation (Why)
Why was this change needed? Link the ticket but don't rely on the link - links rot.

If it's a bug fix: what was broken and what impact did it have?
If it's a feature: what user need or business goal does it serve?
If it's a refactor: what was wrong with the old approach and what does the new approach enable?

### Step 4: Write the Approach (How)
For non-trivial changes: describe the key technical decisions.
- Why this approach over the alternative?
- What tradeoffs were made?
- What did you try that didn't work?

Don't explain what the code does (reviewers can read it). Explain what the code does that isn't obvious from reading it.

### Step 5: Write the Testing section
What did you do to verify this works?
- Unit tests added/updated?
- Manual testing steps?
- Environments tested on?

If there are no tests: say why (legacy code, trivial change, etc.).

### Step 6: Add screenshots or recordings (for UI changes)
Before/after screenshots are worth 1000 words. If the change is visual, include them. Always.

### Step 7: Note anything special for reviewers
- Areas of concern you want extra eyes on
- Known limitations of this approach
- Follow-up work deferred to a future PR

## Template

```markdown
## Summary
[2-4 sentences: what this PR does]

## Motivation
[Why this change was needed. Don't rely on the ticket link alone.]

## Approach
[Key technical decisions and why. What's non-obvious about the implementation.]

## Testing
- [ ] Unit tests: [added / updated / not applicable - reason]
- [ ] Manual testing: [steps taken]
- [ ] Environments: [local / staging / production]

## Screenshots (if UI change)
[Before] [After]

## Notes for reviewers
[Areas of concern, known limitations, follow-up work]
```

## Anti-Patterns

**1. Title that describes the ticket, not the change**
Bad: "JIRA-1234 user stuff"
Good: "feat: add email verification on user signup"

**2. Motivation that just links the ticket**
Bad: "See JIRA-1234"
Good: "Users could sign up with typo'd email addresses and never receive activation emails, causing support tickets. This adds verification before account creation."

**3. No testing section**
Bad: PR with no mention of how it was tested.
Good: Even "tested manually by logging in as a new user on staging" is better than nothing.

**4. 2000-line PRs**
Bad: One massive PR with 15 features and 4 bug fixes.
Good: PRs should be reviewable in 30 minutes. If it's larger, split it.

## Quality Checklist

- [ ] Title: type prefix + imperative mood + under 72 chars
- [ ] Summary explains the change to someone with zero context
- [ ] Motivation explains why (not just what ticket number)
- [ ] Approach explains non-obvious decisions
- [ ] Testing section describes what was tested and how
- [ ] Screenshots included for any UI changes
- [ ] PR size is reviewable (under 400 lines of meaningful changes)
