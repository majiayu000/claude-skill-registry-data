---
name: review-triage
description: >-
  Fetch and triage PR/MR review comments from GitHub or GitLab. Classify each
  as actionable, discussable, or noise. Build implementation plan for actionable
  items, resolve the rest. Use when: "triage comments", "review comments",
  "check pr feedback", "pr comments", "mr comments", "resolve comments",
  "handle review feedback", "address review", "what do reviewers want".
---

# Review Triage

Fetch unresolved review comments from a PR/MR, classify them, and either build an implementation plan or resolve them.

## 1. Detect Platform & Fetch Comments

Run both in parallel to detect which platform is active:

```bash
# GitHub
gh pr view --json number,title,url,reviewDecision 2>/dev/null

# GitLab
glab mr view --output json 2>/dev/null
```

- Only one succeeds → use that platform
- Both succeed → ask user which one
- Both fail → ask user to provide PR/MR number and platform

**Fetch unresolved comments** — see `references/cli-commands.md` for platform-specific commands.

## 2. Classify Each Comment

Read every unresolved comment/thread and classify:

| Category | Criteria | Action |
|----------|----------|--------|
| **Actionable** | Requests code change, bug fix, refactor, or security fix | Add to implementation plan |
| **Question** | Asks for clarification or context — no code change needed | Draft a reply |
| **Nitpick** | Style preference, optional suggestion, or bike-shedding | Acknowledge + resolve |
| **Outdated** | References code that no longer exists or was already changed | Resolve with note |
| **Praise** | Positive feedback, LGTM, approval | Resolve |

Present the classification as a table:

```
| # | File | Category | Summary | Proposed Action |
|---|------|----------|---------|-----------------|
| 1 | src/auth.ts:42 | Actionable | Add input validation | Implement |
| 2 | src/api.ts:10 | Question | Why not use middleware? | Reply |
| 3 | src/utils.ts:5 | Nitpick | Prefer const over let | Resolve |
```

Ask user to confirm or reclassify before proceeding.

## 3. Act

### Actionable Items → Implementation Plan

For each actionable comment, produce:

```
### Comment #N — [file:line]
**Reviewer said:** <quote>
**What to change:** <concrete description>
**Files affected:** <list>
**Complexity:** low | medium | high
```

Sort by file proximity (group changes in the same file), then by complexity (low first).

After presenting the plan, ask: **"Start implementing, or adjust the plan?"**

### Questions → Draft Replies

For each question, draft a concise reply explaining the rationale. Present drafts for user approval before posting.

- GitHub: `gh pr comment <number> --body "reply"`
- GitLab: `glab mr note <iid> -m "reply"`

### Resolvable Items → Batch Resolve

Present the list of comments to resolve. After user confirms:

- GitHub: use `gh api graphql` with `resolveReviewThread` mutation (see references)
- GitLab: `glab mr note <iid> --resolve <note-id>`

## Decision Shortcuts

- **`/review-triage`** — full triage flow (detect → classify → act)
- **`/review-triage actionable`** — skip to actionable items only
- **`/review-triage resolve`** — classify and batch-resolve non-actionable items
