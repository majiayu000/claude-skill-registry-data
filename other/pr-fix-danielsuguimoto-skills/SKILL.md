---
name: pr-fix
description: "Activate when a pull request has review feedback that requires code fixes and direct thread responses."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before fixing PR review feedback (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/git-hosts.md`

Address PR feedback by making fixes and replying directly to review threads — NEVER standalone PR comments. Tools: git host tool (see `<project-root>/docs/git-hosts.md`).

Modes: `review` (default; approval required before commit/push/reply) or `auto` (commits/pushes without approval). `<pr-ref>` is the only authoritative source for the target PR — never assume current branch determines it.

> CRITICAL: in `review` mode, get explicit approval (Step 9) before committing, pushing, or replying. Never infer approval.

### 1. Interpret Arguments
`auto` → `<execution-mode>` = `auto`; PR number/URL → `<pr-ref>`; extra guidance → `<additional-context>`; otherwise → `review`.

### 2. Load PR Context
Resolve project root via `git rev-parse --show-toplevel` → `<repo-path>` (use as `cwd` for MCP calls). Primary thread source: git host list unresolved review comments (filters `isResolved=false` server-side). CLI fallback: GraphQL `reviewThreads` with `isResolved` filter. Use REST `pulls/{n}/comments` only as `databaseId` cross-reference — never as primary (returns resolved comments too).

PR metadata: git host view PR + list reviews. CLI fallback:
```bash
gh pr view <pr-number> --json number,title,body,url,headRefName,baseRefName,author,state,commits
gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews
```
Extract `<pr-branch>`, `<base-branch>`, `<pr-number>`, `<pr-url>`. Run `git branch --show-current` → `<current-branch>`. Review attachments when relevant. No feedback → output "No changes".

### 3. Align Local Branch
If `<pr-branch>` unavailable → STOP. Check out via git host checkout PR or `gh pr checkout <pr-number>`. Store as `<active-branch>`. Checkout fails → STOP. Don't modify code until `<active-branch>` == `<pr-branch>`. Never skip checkout — `<pr-ref>` is authoritative.

### 4. Load Changes
Git host PR diff. CLI fallback: `gh pr diff <pr-number>` or `git diff <base-branch>...<active-branch>`. Store as `<changes>`.

### 5. Analyze Feedback
1. Review unresolved threads; check review states (`CHANGES_REQUESTED`, `APPROVED`, etc.)
2. Use `<changes>` to understand the diff. Prioritize critical issues (bugs, security, broken contracts).
3. Effectively resolved threads (skip): GitHub-unresolved but have "Fixed..."/"Done..." reply + later commit implementing the fix. Verify via commit diff. If in doubt, ask.
4. For each actionable thread, record `<comment-id>`, `<file>`, `<lines>`, `<category>`, `<suggestion>`, `<reviewer-body>`, `<current-heading>`. Don't blindly follow suggestions. `noise`/`question` threads → `not-fixing` list with reasons (record `<reviewer-body>` only there, for Step 12).

### 6. Plan Implementation
Fast path: every thread is a straightforward code suggestion with no conflicts → `<implementation-plan>` = `trivial`, skip to Step 7. Skip fast path when any thread is ambiguous, has cross-thread dependencies, or needs judgment. Otherwise: build ordered fix list (`critical` → `important` → `style`, then file, then line). Move effectively resolved/`noise`/`current-heading: yes` to `not-fixing`. Mark `invalid` threads (misreading, would break behavior, contradicts PR intent) → `not-fixing` with reason (reply why in Step 12). Map dependencies → `<dependencies>`.

### 7. Implement Fixes
Fix critical first, follow existing patterns, use `<active-branch>`, focused minimal changes. Store `<changes-count>`.

### 8. Validate Changes
Run lint + tests on changed files. Confirm fixes address feedback. Store `<validation-results>`, `<validation-passing>` (`yes`/`no`).

### 9. Approval Gate (mandatory in `review` mode)
Never skip. Only `decision: approved` counts — don't infer from silence. If `<validation-passing>` = `no` → STOP. If `auto` mode → skip to Step 11.

Present gate: fix summary, changed file count, validation results. Ask (header `Approval`): "Ready to commit, push, and respond?" Options: `Go Ahead` (→ `approved`) or `Needs Review` (requires feedback → `concerns`).

- `approved` → Step 11. `concerns` → store `<review-feedback>` → Step 10 → re-implement (7) → re-validate (8) → re-present gate. Repeat until `approved`.
- When `<changes-count>` = 0, surface no-change state so user picks `Go Ahead` (no-op) or `Needs Review` with feedback.

### 10. Apply Review Feedback
Use `<review-feedback>` to refine without widening scope. Return to Step 7. No commit/push/reply during this step.

### 11. Commit and Push (after `approved` or in `auto` mode)
`git add -A`, `git commit -m "<message>"`, `git push origin <active-branch>`. Never use generic messages like "address review feedback". Store `<pushed>` (`yes`/`no`).

### 12. Respond to Threads
Reply only after commit + push succeed. ALWAYS reply via thread reply API — NEVER standalone PR comments (`gh pr review -c`, `gh pr comment`). Sole exception: flat PR comments (no line anchor) → single flat PR comment quote-replying (blockquote original + author handle, then response).

Use git host reply to review thread (`pr_number`, `comment_id`, `body`). CLI fallback:
```bash
gh api repos/{owner}/{repo}/pulls/<pr-number>/comments/<comment-id>/replies \
  --method POST --input - <<'EOF'
{"body":"<reply-text>"}
EOF
```
Use `--input -` (not `-f body=`) for special characters. Keep replies short and factual.

### 13. Resolve Addressed Threads
After replying, resolve fully addressed threads via GraphQL `resolveReviewThread` (GraphQL-only; no REST endpoint). Use git host list review threads to map comment IDs to thread node IDs (`PRRT_...`), then git host resolve review thread. CLI fallback:
```bash
gh api graphql -f query='{ repository(owner: "<owner>", name: "<repo>") { pullRequest(number: <pr-number>) { reviewThreads(first: 100) { nodes { id isResolved comments(first: 1) { nodes { databaseId body author { login } } } } } } } }'
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<thread-node-id>"}) { thread { isResolved } } }'
```
Match by first comment's `databaseId`. Only resolve fully addressed threads. Don't resolve intentionally skipped or reviewer-reopened threads. Store `<threads-resolved>`.

## Output
Summary of changes and validation results. At the approval gate: one line per fix, not full diffs. Example: "Fixed N threads across M files" + validation status.
