---
name: github-pr-review
description: Handles PR review comments and feedback resolution. Use when user wants to resolve PR comments, handle review feedback, fix review comments, address PR review, check review status, respond to reviewer, verify PR readiness, review PR comments, analyze review feedback, evaluate PR comments, assess review suggestions, or triage PR comments. Fetches comments via GitHub CLI, classifies by severity, applies fixes with user confirmation, commits with proper format, replies to threads.
---

# GitHub PR review

Resolves Pull Request review comments with severity-based prioritization, fix application, and thread replies.

## Current PR

!`gh pr view --json number,title,state -q '"PR #\(.number): \(.title) (\(.state))"' 2>/dev/null`

## Core workflow

### 1. Fetch and classify comments

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
PR=$(gh pr view --json number -q '.number')
gh api repos/$REPO/pulls/$PR/comments
```

Filter out replies (`in_reply_to_id != null`). Classify originals by severity and process in order: CRITICAL > HIGH > MEDIUM > LOW.

| Severity | Indicators | Action |
|----------|------------|--------|
| CRITICAL | `critical.svg`, "security", "vulnerability" | Must fix |
| HIGH | `high-priority.svg`, "High Severity" | Should fix |
| MEDIUM | `medium-priority.svg`, "Medium Severity" | Recommended |
| LOW | `low-priority.svg`, "style", "nit" | Optional |

See `references/severity_guide.md` for full detection patterns (Gemini badges, Cursor comments, keyword fallback, related comments heuristics).

### 2. Process each comment

For each comment, in severity order:

1. **Show context**: comment ID, severity, file:line, quote
2. **Read affected code** and propose fix
3. **Confirm with user** before applying
4. **Apply fix** if approved
5. **Verify ALL issues** in the comment are addressed (multi-issue comments are common)

### 3. Commit changes

Use git-commit skill format. Functional fixes get separate commits, cosmetic fixes are batched:

| Change type | Strategy |
|-------------|----------|
| Functional (CRITICAL/HIGH) | Separate commit per fix |
| Cosmetic (MEDIUM/LOW) | Single batch `style:` commit |

Reference the comment ID in the commit body.

### 4. Reply to threads

**Important**: use `--input -` with JSON. The `-f in_reply_to=...` syntax does NOT work.

```bash
COMMIT=$(git rev-parse --short HEAD)
gh api repos/$REPO/pulls/$PR/comments \
  --input - <<< '{"body": "Fixed in '"$COMMIT"'. Brief explanation.", "in_reply_to": 123456789}'
```

**Reply templates** (no emojis, minimal and professional):

| Situation | Template |
|-----------|----------|
| Fixed | `Fixed in [hash]. [brief description of fix]` |
| Won't fix | `Won't fix: [reason]` |
| By design | `By design: [explanation]` |
| Deferred | `Deferred to [issue/task]. Will address in future iteration.` |
| Acknowledged | `Acknowledged. [brief note]` |

### 5. Run tests and push

Run the project test suite. All tests must pass before pushing. Push all fixes together to minimize review loops.

### 6. Submit review (optional)

After addressing all comments, formally submit a review:

- `gh pr review $PR --approve --body "..."` - all comments addressed, PR is ready
- `gh pr review $PR --request-changes --body "..."` - critical issues remain
- `gh pr review $PR --comment --body "..."` - progress update, no decision yet

## Avoiding review loops

When bots (Gemini, Codex, etc.) review every push:

1. **Batch fixes**: accumulate all fixes, push once
2. **Draft PR**: convert to draft during fixes
3. **Commit keywords**: some bots respect `[skip ci]` or `[skip review]`

## Important rules

- **ALWAYS** confirm before modifying files
- **ALWAYS** verify ALL issues in multi-issue comments are fixed
- **ALWAYS** run tests before pushing
- **ALWAYS** reply to resolved threads using standard templates
- **ALWAYS** submit formal review (`gh pr review`) after addressing all comments
- **NEVER** use emojis in commit messages or thread replies
- **NEVER** skip HIGH/CRITICAL comments without explicit user approval
- **Functional fixes** -> separate commits (one per fix)
- **Cosmetic fixes** -> batch into single `style:` commit

## References

- `references/severity_guide.md` - Severity detection patterns (Gemini badges, Cursor comments, keyword fallback, related comments heuristics)
