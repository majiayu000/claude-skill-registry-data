---
name: pr-review
description: Guide reviewers through systematic, constructive peer review of a pull request.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: analysis
  since: "2026-02-24"
---

## What I do

I help you review someone else's PR systematically across six key dimensions:

1. **Intent Understanding** — Read the PR description first; understand _why_ before looking at code
2. **Test Review** — Examine tests before implementation; they document intent
3. **Correctness** — Evaluate logic: Does the code do what it claims? What could go wrong?
4. **Edge Cases** — Identify boundary conditions: empty input, nulls, concurrency, large volumes
5. **Security** — Flag security-relevant changes: auth, inputs, secrets, privilege escalations
6. **Feedback Quality** — Ensure every comment is actionable and constructive

The result is a well-structured, thorough review that helps the author improve and maintains code quality.

Supporting files in this skill:

- `assets/review-checklist.template` — The six-dimension checklist as a markdown file

## When to use me

Use when you want to:

- Review a PR assigned to you with clear structure and guidance
- Avoid missing important review areas (logic, edge cases, security)
- Write actionable, constructive feedback instead of vague criticism
- Complete a thorough review efficiently
- Help the author improve the code, not just rubber-stamp it

## PR lifecycle focus

Stage: **Peer review by reviewer** (after PR is opened, before merge).

## Use Instead [if available]

- Use `pr-self-review` for author-side checks before requesting review.
- Use `pr-create` for drafting title/body and opening a PR.
- Use `github-pull-request-handling` for resolving existing review threads with follow-up commits and replies.

## Example usage

"Help me review this PR"
"Guide me through reviewing these changes"
"Walk me through a systematic peer review"
"Review PR #42"
"Review this PR: https://github.com/myorg/myrepo/pull/99"

---

## Workflow

Here's how I guide you through peer review:

### Step 0: Auto-Fetch PR Details (with `gh` CLI if available)

**If you provide a PR number or URL**, I'll automatically fetch metadata using `gh pr view`:
- PR title, description, and linked issues
- Files changed with change counts
- Lines added/removed
- CI/test status
- Current reviewers and approval status

**Fallback**: If `gh` is unavailable or unauthenticated, I'll ask you to paste the PR link or describe the changes manually.

---

### Step 1: Read the Intent First

**Start with the PR description and linked issues — NOT the code.**
(Note: If Step 0 auto-fetched the PR, I'll have already retrieved the description above)

- Read what the author says changed and why
- Read linked Jira issues for business context
- Ask yourself: "Do I understand the _problem_ being solved?"
- Confirm understanding before looking at implementation

### Step 2: Review Tests First

**Look at the test files before the implementation.**

- Tests document what the author intended to build
- Poor tests = poor specification of intent
- Flag missing tests or weak test coverage early
- Ask: "Do these tests actually verify the claimed behavior?"

### Step 3: Evaluate Correctness

**Review the implementation logic step-by-step.**
For each logical change:

- Does this code do what the PR description says it does?
- Is the logic sound?
- Are there off-by-one errors, null pointer risks, or type mismatches?
- Are assumptions about input clearly documented?

Example comment: "This [operation] assumes [X]. What happens if [X] is violated? Consider adding a guard."

### Step 4: Check Edge Cases

**Think like an adversary: What could break this code?**

- Empty input or null values?
- Concurrent access or race conditions?
- Large volumes (performance degradation)?
- Boundary values (min, max, zero)?
- Timeouts or network failures?
- Permission/authorization edge cases?

Example comment: "What happens when [condition]? Current code would [fail behavior]. Consider [suggested fix]."

### Step 5: Security Check

**Flag security-relevant changes.**

- New user inputs: Are they validated?
- Authentication/authorization changes: Correct implementation?
- Secrets or credentials: Any exposed in logs or code?
- Privilege escalations: Properly gated?
- External integrations: Using HTTPS, signing requests, validating responses?

Be specific: "This endpoint now accepts user input. Verify it's validated against [specific vulnerability class]."

### Step 6: Feedback Quality Pass

**Before submitting, review EVERY comment you wrote.**

Each comment must follow this pattern:

```
This [specific code element] [does what/could cause what].
Consider [specific, actionable suggestion] because [why it matters].
```

Examples:

- ✅ GOOD: "This loop assumes the list is sorted. Consider adding an assertion or a sort call because unsorted input would produce incorrect results."
- ❌ BAD: "This looks inefficient"
- ✅ GOOD: "This regex pattern doesn't account for escaped quotes. Use the standard library function instead because hand-rolled parsers miss edge cases."
- ❌ BAD: "Why reinvent the wheel?"

Distinguish **blocking** (must fix before merge) from **non-blocking** (nice to have):

- Use "MUST" for blocking issues
- Use "Consider" or "Suggest" for non-blocking improvements

### Step 7: Render Your Decision

**Submit your review with a clear decision:**

- **Approve**: Code is good, no changes needed
- **Approve with comments**: Code is good but has suggestions for future improvements
- **Request Changes**: Code has issues that must be fixed before merging
- **Comment**: Questions or discussion, decision deferred

Provide a brief summary:

```
Good PR overall. Main feedback:
- Tests look solid
- Logic is sound on auth changes
- One edge case to handle: [specific case]
```

---

## Tips for Success

- **Start with intent, not code** — 80% of review quality comes from understanding the problem first
- **Be constructive, not critical** — You're helping improve code, not finding fault
- **Ask questions, don't demand** — "What happens if...?" is more collaborative than "You didn't handle..."
- **Distinguish blocking from non-blocking** — Don't block merges over style preferences
- **Understand the context** — A 400-line PR solving a hard problem deserves more scrutiny than a typo fix
- **Approve good work** — Don't nitpick. If the code is correct and tests are solid, approve it
