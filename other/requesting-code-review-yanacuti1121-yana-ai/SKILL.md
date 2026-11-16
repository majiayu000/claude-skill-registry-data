---
name: requesting-code-review
description: "Use when asked to review code, a diff, or a PR. Triggers on: 'review this', 'check my diff', 'review the PR', 'is this code ok', 'look at my changes', 'code review'. Focuses on real bugs, security issues, and env leaks — not style."
---

# Requesting Code Review Skill

Code review has one job: find things that will break in production or compromise security.
Style, preference, and micro-optimisations are out of scope unless the reviewer asked for them.

## When to use this skill

- User shares a diff, PR link, or file and asks for review
- User says "review this", "check my changes", "is this safe"
- User is about to merge and wants a second opinion

## What to review

### Priority 1 — Must catch
- **Logic bugs**: off-by-one, wrong condition, silent failure path
- **Security issues**: SQL injection, command injection, XSS, hardcoded secrets, open redirects
- **Env leaks**: `.env` values, tokens, or credentials committed or logged
- **Data loss risk**: missing transaction, unguarded `DELETE`/`DROP`, migration with no rollback

### Priority 2 — Should catch
- **Missing error handling** at system boundaries (external API calls, file I/O, DB queries)
- **Race conditions** or non-atomic operations on shared state
- **Resource leaks**: unclosed connections, missing `finally` blocks
- **Auth bypasses**: missing permission check on a new route/endpoint

### Priority 3 — Note if obvious
- Dead code, console.log left in, commented-out blocks
- Naming that will confuse the next reader

## What NOT to review
- Formatting/indentation (that's a linter's job)
- Personal style preferences
- Architecture opinions unless the user asks
- Hypothetical future concerns ("what if we need to scale this")

## Review format

```markdown
## Code Review

**Reviewed:** [filename or PR#]

### Must fix
- [file:line] [issue] — [why it matters]

### Should fix
- [file:line] [issue]

### Notes
- [file:line] [minor observation]

### Verdict
APPROVE / REQUEST CHANGES / NEEDS DISCUSSION
Reason: [one sentence]
```

If there are no issues, say so explicitly: "No issues found in priority 1-2 categories."

## How to run the review

```bash
# See the full diff first
git diff main...HEAD

# Check for secrets
git diff main...HEAD | grep -iE '(password|secret|token|api_key)\s*='

# Check for debug artifacts
git diff main...HEAD | grep -iE '(console\.log|print\(|debugger|TODO|FIXME)'
```

Show evidence for each finding — do not assert without pointing to the specific line.
