---
name: omnicheck-github
description: Use when checking if PR review findings have been applied — verifies both OmniForge-generated and human reviewer comments against the current diff, posts nudge replies on unaddressed threads
version: 1.0.0
license: Apache-2.0
argument-hint: <pr-number>
allowed-tools: [Read, Glob, Grep, Bash, Agent, Write, Edit, mcp__omniforge__fetch_pr_data, mcp__omniforge__fetch_pr_discussions, mcp__omniforge__reply_to_pr_comment, mcp__omniforge__post_pr_review_summary]
---

# OmniCheck

> **Verify whether requested PR changes have been applied — diff analysis + targeted nudge comments.**

Check all review comment threads on a GitHub PR against the current diff. Resolved threads are marked APPLIED. Unresolved threads are analyzed by a subagent to determine if the fix was applied silently or not at all. Unaddressed threads receive nudge replies and a summary comment.

**Core principle:** Thread status check + diff analysis + user approval gate = accurate, non-spammy follow-up.

**Announce at start:** "I'm using OmniCheck to verify findings on PR #{id}."

## Prerequisites

- `gh` CLI authenticated (`gh auth status` to verify)
- Git repository with remote pointing to GitHub
- Current working directory is in the git repo
- PR must have review comment threads

## Input Parsing

Accept any of: PR number (`136`), prefixed (`#136`), or full GitHub URL.
Extract PR ID. If URL provided, extract owner/repo and PR number.

## The Process

```
Phase 1: GATHER   — fetch all threads + PR diff/data
Phase 2: ANALYZE  — single subagent checks each open thread against the diff
Phase 3: REPORT   — present status table, user approves nudge list
Phase 4: NUDGE    — reply on each NOT_APPLIED thread + post summary PR comment
Phase 5: DONE     — no cleanup needed (no worktrees)
```

---

## Thread Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| `APPLIED` | Thread is resolved/dismissed — trusted as-is | None |
| `SILENTLY_APPLIED` | Thread open, but diff shows the concern was addressed | Note in summary only |
| `NOT_APPLIED` | Thread open, diff shows no relevant change | Nudge: thread reply + summary row |
| `NEEDS_HUMAN` | Ambiguous — cannot determine from diff alone | Flag in report; no automatic nudge |

---

## Phase 1: Gather

**Step 1:** Fetch all review comment threads.

```
mcp__omniforge__fetch_pr_discussions(pr_id="{id}", repo_root="{cwd}")
```

Returns structured threads with: `comment_id`, `type`, `file_path`, `line_number`, `body`, `author`, `replies`. The tool already excludes discussions whose notes are all system-generated — every thread returned contains at least one human note.

**Note:** When building `{UNRESOLVED_THREADS_JSON}` for the analysis subagent, include each thread's `comment_id` field as `comment_id` so verdicts can be mapped back to GitHub comment IDs for posting replies.

**Step 2:** Partition threads.
- Resolved/dismissed threads → pre-labeled `APPLIED`, skip analysis
- Open threads (any type) → pass to Phase 2. This includes both inline review threads and general comments — both can receive nudge replies.

**Note:** GitHub does not have a simple `resolved` boolean like GitLab. Thread resolution is determined by the PR review state. A review thread is considered "addressed" if the review was dismissed or the PR review that contains it was marked as "changes requested" and subsequently satisfied. The `fetch_pr_discussions` tool normalizes this into an open/closed state.

**Step 3:** Fetch PR metadata and diff.

```
mcp__omniforge__fetch_pr_data(pr_id="{id}", repo_root="{cwd}")
```

Returns: title, author, source_branch, target_branch, diff, diff_line_count, commits, files_changed.

**Step 4:** Early exit checks.
- Zero threads returned: "PR #{id} has no review comment threads. Nothing to check." Stop.
- Zero open threads: "All {N} threads are resolved. Nothing to nudge." Stop.

**Step 5:** Present: "Found {N} total threads ({R} resolved, {U} unresolved). Analyzing {U} unresolved threads."

---

## Phase 2: Analyze (Single Subagent)

**Goal:** For each unresolved thread, determine if the diff addresses its concern.

**Template:** `./references/analysis-agent-prompt.md`

Fill template placeholders:
- `{MR_ID}` — PR number
- `{MR_TITLE}` — PR title
- `{UNRESOLVED_THREADS_JSON}` — JSON array of all unresolved threads
- `{GIT_DIFF}` — Full diff string from Phase 1

**Large PR handling:** If unresolved thread count > 15 AND diff_line_count > 5000, group threads by file and dispatch up to 3 subagents. Merge results before Phase 3.

### Expected Return

```json
[
  {
    "comment_id": "abc123",
    "file_path": "src/auth.py",
    "line_number": 47,
    "body_summary": "Missing null check on user input",
    "verdict": "NOT_APPLIED",
    "confidence": 91,
    "reasoning": "The diff shows no changes to src/auth.py around line 47. The null check is still absent."
  },
  {
    "comment_id": "def456",
    "file_path": ".github/workflows/ci.yml",
    "line_number": 1072,
    "body_summary": "Missing placeholder mapping for STRIPE_PRICE_ENTERPRISE",
    "verdict": "SILENTLY_APPLIED",
    "confidence": 87,
    "reasoning": "Line 1072 in .github/workflows/ci.yml was changed in the diff to include the placeholder mapping. The thread was not resolved but the concern is addressed."
  }
]
```

**Verdict definitions:**
- `SILENTLY_APPLIED` — thread open but diff shows the concern was addressed
- `NOT_APPLIED` — thread open and diff shows no relevant change
- `NEEDS_HUMAN` — diff changes are present but genuinely unclear if they address the concern

---

## Phase 3: Report (User Approval Gate)

**REQUIRED REFERENCE:** `./references/nudge-guide.md` — read before presenting results. Contains the exact presentation format and user action matrix. Do NOT present without loading this reference.

Present status combining Phase 1 resolved threads + Phase 2 verdicts:

```
OmniCheck — PR #{id}: {title}

  ✓ Applied (resolved):     {N} threads
  ✓ Silently Applied:       {N} threads
  ✗ Not Applied:            {N} threads
  ? Needs Human Review:     {N} threads

NOT_APPLIED threads (will receive nudge):
  1. {file}:{line} — {body_summary} [confidence: {score}%]
  2. {file}:{line} — {body_summary} [confidence: {score}%]

NEEDS_HUMAN threads (no automatic nudge):
  3. general — {body_summary}

Post nudge replies on NOT_APPLIED threads? [Y/n]
(Enter numbers to exclude specific threads, e.g. "exclude 2")
```

**CRITICAL: No comments are posted until the user explicitly approves.**

---

## Phase 4: Nudge

**REQUIRED REFERENCE:** `./references/nudge-guide.md` — contains the exact thread reply template and summary comment template. Do NOT post without loading this reference.

For each approved NOT_APPLIED thread:

**Step 1:** Post thread reply.

```
mcp__omniforge__reply_to_pr_comment(
  pr_id="{id}",
  comment_id="{comment_id}",
  body="{nudge_reply_text}",
  repo_root="{cwd}"
)
```

**Fallback (without MCP tool):**

```bash
gh api repos/{owner}/{repo}/pulls/{id}/comments/{comment_id}/replies \
  --method POST \
  --field body="{nudge_reply_text}"
```

**Step 2:** After all thread replies succeed or fail, post one summary comment.

```
mcp__omniforge__post_pr_review_summary(
  pr_id="{id}",
  summary="{summary_comment_text}",
  repo_root="{cwd}"
)
```

**Fallback (without MCP tool):**

```bash
gh pr comment {id} --body "{summary_comment_text}"
```

**Ordering guarantee:** All thread replies before the summary comment.

**On reply failure:** Collect the failure, continue with remaining threads, and note the failure in the summary comment.

---

## Phase 5: Done

No worktrees → no cleanup needed.

Report:
```
OmniCheck complete — PR #{id}

  ✓ Nudged: {N} threads
  ✗ Failed to post: {N} threads (list them)
```

---

## Error Handling

| Error | Response |
|-------|----------|
| gh not authenticated | "Run `gh auth login` first." Stop. |
| PR not found | "PR #{id} not found. Verify the number and repository." Stop. |
| No comment threads | "PR #{id} has no review comment threads. Nothing to check." Stop. |
| All threads resolved | "All {N} threads are resolved. Nothing to nudge." Stop. |
| Analysis agent fails | Present error to user; offer to retry or abort |
| Thread reply fails | Continue with remaining threads; note failure in summary |
| Summary comment fails | Report failure; thread replies already posted |

---

## Integration

**MCP Tools:**
- `mcp__omniforge__fetch_pr_discussions` — Fetch all review comment threads
- `mcp__omniforge__fetch_pr_data` — Fetch PR metadata and diff
- `mcp__omniforge__reply_to_pr_comment` — Post nudge reply on a thread
- `mcp__omniforge__post_pr_review_summary` — Post summary comment on PR

**Subagent Template:**
- `./references/analysis-agent-prompt.md` — Analysis Agent (single, diff-only check)

---

## Never

- Post comments without explicit user approval (Phase 3 gate)
- Add AI attribution to any posted comment
- Use `glab` (GitHub — use `gh` exclusively)
- Dismiss any PR reviews (OmniCheck only nudges, never dismisses)
- Create worktrees (diff-only analysis)
- Skip any of the 5 phases

## Always

- Fetch threads and diff in Phase 1 before dispatching analysis
- Present status table and wait for user approval before posting
- Post thread replies before the summary comment
- Report final outcome including any failed posts
- Use `gh` for all GitHub operations
