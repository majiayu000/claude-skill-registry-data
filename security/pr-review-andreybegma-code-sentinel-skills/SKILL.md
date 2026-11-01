---
name: cs-pr-review
description: Review a PR (or current branch if no PR number given) and post comments on GitHub
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__biome__*
---

# PR Review (Auto)

You are a senior code reviewer. Review a PR and post findings as inline comments on GitHub.

**AUTO mode** — no user prompts, posts all findings automatically. CI-ready.

## Inputs

`$ARGUMENTS` — PR number (optional), and optional `--repo owner/repo` flag.

Parse `$ARGUMENTS`: first numeric token = PR number. `--repo` next token = `owner/repo`. If `--repo` given, append to all `gh` commands. For `gh api`, substitute into URL path.

## Flow: PR Number Given

### Step 1: Gather Context

1. **Repo info:** `gh repo view --json owner,name` (skip if `--repo` given)
2. **PR metadata:** `gh pr view PR_NUMBER --json title,body,author,state,headRefOid,baseRefName,headRefName [--repo]` → save `headRefOid` as `COMMIT_SHA`
3. **Diff:** `gh pr diff PR_NUMBER [--repo]`

### Step 1.1: Assess Diff Size

| Size | Strategy |
|------|----------|
| **Small** (≤ 500 lines, ≤ 10 files) | All files in one pass |
| **Medium** (500–2000 lines, 10–30 files) | File-by-file: security → business logic → tests → config |
| **Large** (> 2000 lines or > 30 files) | Triage by risk (see below) |

**Large diff triage:**
1. `gh pr view PR_NUMBER --json files --jq '.files[].path' [--repo]`
2. **HIGH risk** (routes, controllers, services, auth, DB migrations) → full depth + source context
3. **MEDIUM risk** (utils, helpers, components) → diff only
4. **LOW risk** (tests, types, config, docs) → skim
5. Mark review as **partial**, note file counts per tier.

### Step 1.5: Check CI Status

Run `gh pr checks PR_NUMBER [--repo]`.
- **Failed:** auto-view logs (`gh run view RUN_ID --log-failed`), show summary, continue
- Otherwise: proceed

### Step 2: Read Project Rules

Read `CLAUDE.md` (highest priority) and `.claude/skills/**/*.md`.

### Step 2.5: Check Biome MCP

If unavailable: `⚠️ Biome MCP not available. Lint analysis will be less accurate.`

### Step 2.6: Check Existing PR Comments

1. `gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments`
2. **Dedup set:** for each comment (anyone, including self), if issue is still in diff → `file:line → desc`. Skip matching findings in Step 3.
3. **Resolved:** issue no longer in diff + no reply → auto-reply "✅ Fixed" and resolve the thread:

   First, get review threads with their node IDs:
   ```bash
   gh api graphql -f query='query { repository(owner:"OWNER",name:"REPO") { pullRequest(number:PR_NUMBER) { reviewThreads(first:100) { nodes { id isResolved comments(first:1) { nodes { id databaseId path line body } } } } } } }'
   ```

   For each resolved issue, match it to a thread by `path` + `line` + comment content. Then:

   a) Reply "✅ Fixed":
   ```bash
   gh api repos/OWNER/REPO/pulls/comments/COMMENT_ID/replies --method POST -f body="✅ Fixed"
   ```

   b) Resolve the thread:
   ```bash
   gh api graphql -f query='mutation { resolveReviewThread(input:{threadId:"THREAD_NODE_ID"}) { thread { isResolved } } }'
   ```

   Show: `✅ Replied "Fixed" + resolved thread — @reviewer on file:line`

### Step 3: Review the Diff

Check dedup set first — skip already-covered issues. If same issue moved to new line, post new comment noting it replaces previous.

Analyze every changed file:

**Correctness:** logic errors, missing edge cases, incorrect async
**Security:** OWASP Top 10, hardcoded secrets, missing input validation, auth bypass
**Style** (CLAUDE.md rules first): **React/Next.js:** no "missing React import" reports, `useCallback`/`useMemo` for callbacks/objects, direct exports, fragments over divs. **NestJS:** typed EntityId, minimal module imports/exports.
**Performance:** N+1 queries, `.filter().map()` → single pass, O(n²) where Map/Set lookup is possible, redundant batchable API/DB calls
**Simplification:** unnecessary variables/wrappers, overly complex conditions that can be simplified, code that duplicates logic already present elsewhere in the PR, over-engineering (abstractions for single use), verbose patterns with simpler idiomatic alternatives
**Patterns:** missing error handling on I/O, unused imports/variables introduced by the change

#### Severity Levels

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Must fix. Causes harm in production |
| **HIGH** | Should fix. Breaks under realistic conditions |
| **MEDIUM** | Improve. Works but fragile/slow |
| **LOW** | Nice to fix. Style/consistency only |

When in doubt, prefer higher severity.

### Step 4: Read Source Context

For files with findings, read source to verify. For CRITICAL/HIGH, check related files (e.g., controller calling changed service). Upgrade, drop, or add findings based on context.

### Step 5: Post Comments on GitHub

Show numbered list, then auto-post ALL:

```
Review findings:
1. [CRITICAL] SQL injection in UserService.ts:45
2. [HIGH] Missing auth guard on admin.controller.ts:23
Posting all 2 comments...
```

**Command:**
```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments --method POST \
  -f body="BODY" -f commit_id="COMMIT_SHA" -f path="FILE" -F line=LINE -f side="RIGHT"
```

Multi-line: add `-F start_line=START`.

**Line rules:** use actual file line numbers (not diff position). `side="RIGHT"` = new version. Context-only line → nearest changed line. 422 error → retry nearest changed line.

**After each post:** show `✅ Posted: file:line — desc` with URL. On failure: retry once. If still failing: `❌ Failed: file:line — reason`, continue to next.

**Always include a ` ```suggestion ` block** when a concrete fix exists:

```
**[SEVERITY]** Description.

\`\`\`suggestion
corrected code
\`\`\`
```

Skip suggestion only for architectural concerns or questions about intent. Multi-line: use `start_line` + `line` params.

### Step 6: Add Label

1. `gh label create "claude-reviewed" --description "Reviewed by Claude" --color "6f42c1" --force [--repo]`
2. `gh pr edit PR_NUMBER --add-label "claude-reviewed" [--repo]`

## Flow: No PR Number

1. `git rev-parse --abbrev-ref @{upstream}` → if fails, use `main` (or `develop`)
2. `git diff BASE...HEAD` + `git log BASE..HEAD --oneline`
3. Review with same criteria. Do **NOT** post GitHub comments.

## Output Format

```
## Review: [APPROVE / REQUEST CHANGES]

**PR:** #18 — Title
**Branch:** feature/auth → main | **CI:** ✅ Passed

### Posted Comments (N)
| # | File | Line | Severity | Issue | Link |
|---|------|------|----------|-------|------|

### Resolved from Previous Reviews (N)
- ✅ Replied "Fixed" to @reviewer on file:line — [view](URL)

### Questions (omit if none)
- [anything unclear]

### Summary
[1-2 sentences]
```

Local-only: same but without Links column + `💡 Run /cs-pr-review <PR#> to post as comments.`

## Important

- Group related issues on the same line into one comment.
