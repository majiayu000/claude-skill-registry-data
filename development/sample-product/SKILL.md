---
name: commit-review
description: >-
  Review git commits for quality, clarity, and best practices before pushing.
  Checks commit message format, diff size, test coverage signals, and common
  mistakes. Use when reviewing commits, before pushing, when asked to "check
  my commits", "review changes", or "is this ready to push".
---

# Commit Review

> Systematic review of git commits for message quality, diff hygiene, and common mistakes before pushing.

**Version:** 1.0.0
**Category:** Skills
**Author:** @sample-creator

---

## When to Use

- You want to review your commits before pushing to a shared branch
- You need to check if commit messages follow conventional format
- You want to catch common mistakes (large files, secrets, debug code)
- A PR has commits that need cleanup before merge

## When NOT to Use

- For full code review (use a dedicated code review tool instead)
- For CI/CD pipeline checks (this is a pre-push local review)
- For rebasing or rewriting history (this reviews, not rewrites)

---

## Activation Protocol

Before responding to any invocation:

1. **Load review criteria:** Read `${CLAUDE_SKILL_DIR}/references/review-criteria.md`
   — Contains: commit message format rules, diff size thresholds, anti-patterns
2. **Load examples:** Read `${CLAUDE_SKILL_DIR}/examples/good-vs-bad.md`
   — Contains: 5 examples of good commits vs. problematic commits
3. **Identify scope:** How many commits to review? Last N, a range, or all unpushed?
4. **Run question system:** Check for required inputs (see below)

---

## Question System

| Input | Required | If Missing |
|-------|----------|-----------|
| Commits to review | Yes | Ask: "How many recent commits should I review? Or give me a range (e.g., HEAD~3..HEAD)" |
| Branch context | No | Default: current branch. State assumption. |
| Strictness level | No | Default: `standard`. Options: `relaxed` (personal project), `standard`, `strict` (team/OSS) |

---

## Core Instructions

### Review Pipeline

For each commit in the review scope:

**Step 1 — Message Quality**
- Does the message follow conventional format? (`type: subject` or `type(scope): subject`)
- Is the subject line under 72 characters?
- Does it explain WHY, not just WHAT?
- Is it written in imperative mood? ("add feature" not "added feature")

**Step 2 — Diff Analysis**
- How many files changed? Flag if >10 files (might need splitting)
- How many lines added/removed? Flag if >500 lines net
- Are there unrelated changes mixed in? (scope creep)

**Step 3 — Anti-Pattern Scan**
- Debug code left in? (`console.log`, `debugger`, `print("HERE")`)
- Secrets or credentials? (API keys, tokens, passwords)
- Large binary files? (images, compiled assets >1MB)
- TODO/FIXME comments added without ticket reference?

**Step 4 — Quality Signal**
- Were tests modified alongside code changes? (good signal)
- Were docs updated if behavior changed? (good signal)
- Is the commit atomic? (one logical change per commit)

### Modes

| Mode | When to Use | What Changes |
|------|------------|-------------|
| `relaxed` | Personal project, rapid iteration | Skip message format, allow larger diffs |
| `standard` | Team project (default) | Full review, balanced feedback |
| `strict` | Open source, shared codebase | Enforce conventional commits, flag all anti-patterns |

---

## Output Structure

```
COMMIT REVIEW — {branch} ({N} commits)

Commit 1: {short hash} — {subject}
  Message:  PASS | WARN | FAIL — {note}
  Diff:     {files} files, +{added}/-{removed} lines — {assessment}
  Patterns: {anti-patterns found or "clean"}
  Signal:   {quality signals detected}

...

SUMMARY
  Reviewed: {N} commits
  Ready to push: {yes/no}
  Issues: {count} ({critical}, {warnings})
  Recommendation: {specific action}
```

---

## Quality Gate

Before delivering the review:
- [ ] Every commit in scope was reviewed (none skipped)
- [ ] Each finding includes a specific recommendation (not just "fix this")
- [ ] Anti-pattern scan checked for secrets (security-critical)
- [ ] Summary gives a clear push/no-push recommendation
- [ ] Output follows the structure template above

If any check fails: complete the review before delivering.

---

## Anti-Patterns

- **Rubber-stamping**: Saying "looks good" without actually reviewing the diff
- **Nitpicking format over substance**: Obsessing over commit message style when the diff has real issues
- **Missing the forest**: Reviewing individual commits without noticing they should be squashed
- **False security**: Scanning for `console.log` but ignoring hardcoded API keys

---

## Composability

- **As input to:** `/publish` (review commits before publishing a myClaude product)
- **As output from:** Any development workflow that produces commits
- **In workflows:** Can be embedded as a pre-push step in a development workflow
