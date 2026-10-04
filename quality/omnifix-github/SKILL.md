---
name: omnifix-github
description: Use when fixing review findings on a GitHub PR, resolving inline review threads, applying code review suggestions, or when asked to fix issues from an OmniForge report
version: 1.0.0
license: Apache-2.0
argument-hint: <pr-number>
allowed-tools: [Read, Glob, Grep, Bash, Agent, Write, Edit, mcp__omniforge__fetch_pr_data, mcp__omniforge__fetch_pr_discussions, mcp__omniforge__reply_to_pr_comment, mcp__omniforge__cleanup_omnifix_worktrees]
---

# OmniFix

> **Automated review finding fixer — triage with parallel subagents, sequential fixing, verification, comment replies.**

Fetch unresolved review threads from a GitHub PR, triage each finding with parallel subagents in isolated worktrees, present results for user approval, apply approved fixes sequentially, verify with a fresh-eyes agent, commit, post replies on threads, and clean up.

**Core principle:** Parallel triage + user approval gate + sequential fix + verification = safe, high-quality automated fixes.

**Announce at start:** "I'm using OmniFix to fix review findings on PR #{id}."

## Prerequisites

- `gh` CLI authenticated (`gh auth status` to verify)
- Git repository with remote pointing to GitHub
- Current working directory is in the git repo
- PR must have unresolved review comment threads

## Input Parsing

Accept any of: PR number (`136`), prefixed (`#136`), or full GitHub URL.
Extract PR ID. If URL provided, extract owner/repo and PR number.

## The Process

```
Input: PR number with unresolved review findings
    |
    v
Phase 1: GATHER — fetch unresolved comments + PR data
    |
    v
Phase 2: TRIAGE — N parallel subagents validate findings in read-only worktrees
    |
    v
Phase 3: APPROVE — present triage results, user explicitly approves
    |               (NO code changes until approval)
    v
Phase 4: FIX — single subagent applies approved fixes sequentially in writable worktree
    |
    v
Phase 5: VERIFY — fresh-eyes verification subagent reviews all changes
    |
    v
Phase 6: COMMIT + POST — commit, push (with permission), reply on threads
    |
    v
Phase 7: CLEANUP — remove all worktrees (ALWAYS runs)
```

---

## Phase 1: Gather

Fetch ALL data before dispatching triage agents.

**Step 1:** Fetch discussions/review comments.

```
mcp__omniforge__fetch_pr_discussions(pr_id="{id}", repo_root="{cwd}")
```

Returns structured review comment threads with: `comment_id`, `type` (inline/general), `file_path`, `line_number`, `body`, `author`, `replies`.

**Note:** GitHub does not have native thread resolution (resolve/unresolve) like GitLab. Instead of `resolvable`/`resolved` fields, use GitHub's review thread state. Threads are considered "open" if they have no resolving review. The `fetch_pr_discussions` tool handles this distinction.

**Step 2:** Filter discussions.
- Keep only: open/unresolved review threads (not already addressed)
- Skip: system notes, OmniForge summary comments (individual top-level comments)
- Skip: resolved/dismissed review threads

**Step 3:** Fetch PR metadata.

```
mcp__omniforge__fetch_pr_data(pr_id="{id}", repo_root="{cwd}")
```

Returns: title, author, source_branch, target_branch, diff, diff_line_map, commits, files_changed.

**Step 4:** Categorize each finding:
- **inline** — has `file_path` and `line_number` (from OmniForge inline threads or human comments on diff)
- **general** — no file position (from human general comments). Attempt to locate via grep in worktree; if found, treat as inline. If not, present as `NEEDS_HUMAN` in Phase 3.

**Step 5:** Parse each finding into standardized format:
```json
{
  "comment_id": "abc123",
  "file_path": ".github/workflows/ci.yml",
  "line_number": 1072,
  "body": "**Important** — Missing validation...",
  "author": "shahilkadia",
  "severity": "important",
  "type": "inline"
}
```

**Step 6:** Cap and present.
- If >25 findings, present options:
  1. Process top 25 by severity
  2. Process all (may be slow and expensive)
  3. Select specific findings to process
- Present: "Found {N} unresolved findings ({X} inline, {Y} general). Proceeding to triage."

**Handles three sources:**
- OmniForge findings (structured: severity tag in body, "Confidence: X/100")
- Human reviewer comments (unstructured: "this looks wrong", "consider using X")
- Automated CI/bot comments (skip: system notes, pipeline status)

---

## Phase 2: Triage (Parallel Subagents)

**Goal:** Validate each finding independently — is it real? What's the fix?

**Template:** `./references/triage-agent-prompt.md`

### Subagent Dispatch Strategy

| Finding Count | Strategy | Max Agents |
|---------------|----------|------------|
| <5 | 1 subagent per finding | 4 |
| 5-15 | Group by file, 1 subagent per file | 15 |
| >15 | Group by file, cap total agents | 8 |

### Worktree Setup

Create N detached read-only worktrees for triage:

```bash
# Resolve main repo root (handles linked worktrees)
MAIN_ROOT=$(git rev-parse --git-common-dir 2>/dev/null)
if [ -n "$MAIN_ROOT" ]; then MAIN_ROOT=$(cd "$(dirname "$MAIN_ROOT")" && pwd); else MAIN_ROOT=$(pwd); fi
cd "$MAIN_ROOT"

git fetch origin {source_branch}
git worktree add .worktrees/omnifix-triage-{pr_id}-1 origin/{source_branch} --detach
git worktree add .worktrees/omnifix-triage-{pr_id}-2 origin/{source_branch} --detach
# ... up to N
```

Before creating, clean any stale worktrees from previous crashed runs:
```bash
git worktree remove .worktrees/omnifix-triage-{pr_id}-* --force 2>/dev/null
git worktree prune
```

### Agent Dispatch

Dispatch all triage agents simultaneously using the **Agent tool** (parallel Agent calls). Each agent gets:
- The finding(s) assigned to it
- Its worktree absolute path (read-only)
- The triage-agent-prompt template with placeholders filled

Fill template placeholders:
- `{MR_ID}` — PR number
- `{MR_TITLE}` — PR title
- `{WORKTREE_PATH}` — **Absolute** path to agent's worktree
- `{FINDINGS_FOR_THIS_AGENT}` — JSON array of findings assigned to this agent

### Expected Return

Each agent returns structured verdicts:
```json
{
  "comment_id": "abc123",
  "file_path": ".github/workflows/ci.yml",
  "line_number": 1072,
  "verdict": "VALID",
  "confidence": 92,
  "reasoning": "The finding is correct — variable is validated but not mapped.",
  "proposed_fix": {
    "description": "Add placeholder mapping",
    "file_path": ".github/workflows/ci.yml",
    "before_context": "sed -i \"s|PLACEHOLDER_STRIPE...",
    "after_code": "sed -i \"s|PLACEHOLDER_STRIPE_PRICE_ENTERPRISE|...\""
  }
}
```

**Verdict types:**
- `VALID` — finding is correct, proposed fix included
- `INVALID` — finding is a false positive + reasoning why
- `NEEDS_HUMAN` — ambiguous, needs human judgment + what's unclear

### Cleanup

After all triage agents complete, immediately remove triage worktrees:
```bash
# Resolve main repo root (handles linked worktrees)
MAIN_ROOT=$(git rev-parse --git-common-dir 2>/dev/null)
if [ -n "$MAIN_ROOT" ]; then MAIN_ROOT=$(cd "$(dirname "$MAIN_ROOT")" && pwd); else MAIN_ROOT=$(pwd); fi
cd "$MAIN_ROOT"

git worktree remove .worktrees/omnifix-triage-{pr_id}-1 --force
# ... all N
git worktree prune
```

---

## Phase 3: Approve (User Gate)

**Goal:** Present triage results. User explicitly approves before any code changes.

**CRITICAL: No code changes until user explicitly approves.**

**REQUIRED REFERENCE:** `./references/approval-guide.md` — you MUST read this before presenting triage results. Contains the exact presentation format (VALID/INVALID/NEEDS_HUMAN sections), auto-reply options, commit strategy options, and the full user action matrix. Do NOT present results without loading this reference — the format and option text must match exactly.

**Note:** GitHub does not have native thread resolution via API in the same way GitLab does. Instead of "resolve/unresolve", the equivalent action is posting a reply that the concern has been addressed and optionally dismissing the review. The approval guide covers GitHub-specific reply behavior.

---

## Phase 4: Fix (Single Implementer Subagent)

**Goal:** Apply approved fixes sequentially in a writable worktree.

**Template:** `./references/fix-agent-prompt.md`

### Worktree Setup

Create a writable worktree on the PR source branch:

```bash
# Resolve main repo root (handles linked worktrees)
MAIN_ROOT=$(git rev-parse --git-common-dir 2>/dev/null)
if [ -n "$MAIN_ROOT" ]; then MAIN_ROOT=$(cd "$(dirname "$MAIN_ROOT")" && pwd); else MAIN_ROOT=$(pwd); fi
cd "$MAIN_ROOT"

git fetch origin {source_branch}
git worktree add .worktrees/omnifix-{pr_id} -b omnifix-temp-{pr_id} origin/{source_branch}
```

### Agent Dispatch

Dispatch a single implementer subagent with the fix-agent-prompt template:
- `{MR_ID}` — PR number
- `{MR_TITLE}` — PR title
- `{WORKTREE_PATH}` — **Absolute** path to writable worktree
- `{APPROVED_FIXES_JSON}` — JSON array of approved fixes from triage
- `{TEST_COMMAND}` — Test command (see discovery order below)

**CRITICAL: Dispatch with write permissions.** The fix agent needs Write and Edit tools to modify files in the worktree. Use `mode: "acceptEdits"` when dispatching:

```
Agent(prompt="...", mode="acceptEdits", subagent_type="general-purpose")
```

Without `mode: "acceptEdits"`, the subagent may be blocked by the user's permission settings and unable to edit files. If the fix agent returns `BLOCKED` due to permissions, fall back to applying fixes directly in the main agent context (read the proposed fixes and apply them with Edit/Write tools in the worktree yourself).

### Test Command Discovery

1. User passes `test_command` explicitly in invocation
2. Check repo's `CLAUDE.md` for test commands
3. Auto-detect:
   - `package.json` with `test` script -> `npm test` / `bun test`
   - `pyproject.toml` or `pytest.ini` -> `pytest`
   - `Makefile` with `test` target -> `make test`
   - `Cargo.toml` -> `cargo test`
   - `go.mod` -> `go test ./...`
4. If none found -> skip tests, warn user: "No test command detected. Fixes applied without testing."

### Fix Agent Behavior

The agent applies fixes **sequentially in file order** (to avoid conflicts):
1. Open the file in the worktree
2. Apply the proposed change
3. Run relevant tests (if identifiable)
4. If tests fail: attempt to adjust the fix, or flag for user
5. After all fixes: run full test suite, self-review via `git diff`
6. Do NOT commit — the main agent handles that after verification

### Expected Return

```json
{
  "status": "DONE",
  "fixes_applied": 2,
  "fixes_failed": 0,
  "tests_passed": true,
  "files_changed": [".github/workflows/ci.yml", "src/auth.py"],
  "details": [
    {"comment_id": "abc123", "status": "applied", "description": "Added placeholder mapping"},
    {"comment_id": "def456", "status": "applied", "description": "Added null check guard"}
  ]
}
```

**Status codes:** `DONE` | `DONE_WITH_CONCERNS` | `BLOCKED` | `NEEDS_CONTEXT`

**Why sequential (not parallel):** Two findings on the same file would create merge conflicts. Fix A might change line numbers that Fix B depends on. The agent needs cumulative state after each fix.

---

## Phase 5: Verify (Verification Subagent)

**Goal:** Fresh-eyes review of all changes before committing.

**Template:** `./references/verify-agent-prompt.md`

### Agent Dispatch

Dispatch a verification subagent with:
- `{MR_ID}` — PR number
- `{MR_TITLE}` — PR title
- `{WORKTREE_PATH}` — Absolute path to fix worktree
- `{FINDINGS}` — Original findings that were being fixed
- `{GIT_DIFF}` — Complete diff output (`git diff` in the worktree)
- `{TEST_COMMAND}` — Same test command from Phase 4

### Verifier Checks

1. Does each change actually address its finding?
2. Are there any regressions? (new bugs introduced by fixes)
3. Do all tests pass?
4. Is the code style consistent with the codebase?
5. Are there any unintended side effects?

### Expected Return

- `APPROVED` — all good, proceed to commit
- `NEEDS_REWORK` — issues found + what to fix

### NEEDS_REWORK Loop

When verification returns `NEEDS_REWORK`:
1. Present verifier's issues to user
2. Options:
   a. Send back to fix agent with feedback (max 2 rework iterations)
   b. Proceed anyway
   c. Abort
3. After 2 rework iterations without `APPROVED`, escalate to user unconditionally

---

## Phase 6: Commit + Post

**Goal:** Commit fixes and update all review comment threads.

**REQUIRED REFERENCE:** `./references/commit-and-post-guide.md` — you MUST read this before committing or posting. Contains the race condition check procedure, commit template (with `PRE_COMMIT_ALLOW_NO_CONFIG=1`), push command, thread reply MCP tool calls (`reply_to_pr_comment`), and summary comment template. Do NOT commit or post without loading this reference — the commit format and thread reply pattern must be followed exactly.

**GitHub-specific notes:**
- GitHub uses `comment_id` instead of `discussion_id` for replies. The `reply_to_pr_comment` MCP tool takes a `comment_id` parameter.
- GitHub does not have native thread resolution (resolve/unresolve) via the REST API in the same way GitLab does. Instead of resolving threads, post a reply indicating the concern has been addressed. If the thread is part of a PR review, the review can be dismissed, but this is not automatic.

Key rules:
- **Race condition check** before push — fetch and compare source branch HEAD
- **Never force-push** — abort if rebase has conflicts
- **Ask user before pushing** — never auto-push
- **No AI attribution** in commits or posted content

### Replying to Review Comments

Use the MCP tool for each thread reply:

```
mcp__omniforge__reply_to_pr_comment(
  pr_id="{id}",
  comment_id="{comment_id}",
  body="{reply_text_with_commit_sha}",
  repo_root="{cwd}"
)
```

**Fallback (without MCP tool):**

```bash
gh pr comment {id} --body "{reply_text}" --json id
```

Note: GitHub's `gh pr comment` creates a new top-level comment. To reply to a specific review thread, use the GitHub API:
```bash
gh api repos/{owner}/{repo}/pulls/{id}/comments/{comment_id}/replies \
  --method POST \
  --field body="{reply_text}"
```

---

## Phase 7: Cleanup

**ALWAYS runs, regardless of success or failure.**

```
mcp__omniforge__cleanup_omnifix_worktrees(mr_id="{id}", repo_root="{cwd}")
```

Removes:
- `.worktrees/omnifix-{pr_id}` (fix worktree)
- `.worktrees/omnifix-triage-{pr_id}-*` (triage worktrees)
- Temp branch `omnifix-temp-{pr_id}`
- `git worktree prune`

**Fallback (if MCP tool unavailable):**

```bash
# Resolve main repo root (handles linked worktrees)
MAIN_ROOT=$(git rev-parse --git-common-dir 2>/dev/null)
if [ -n "$MAIN_ROOT" ]; then MAIN_ROOT=$(cd "$(dirname "$MAIN_ROOT")" && pwd); else MAIN_ROOT=$(pwd); fi
cd "$MAIN_ROOT"

git worktree remove .worktrees/omnifix-{pr_id} --force 2>/dev/null
for wt in .worktrees/omnifix-triage-{pr_id}-*; do
    git worktree remove "$wt" --force 2>/dev/null
done
rm -rf .worktrees/omnifix-{pr_id} .worktrees/omnifix-triage-{pr_id}-* 2>/dev/null
git worktree prune
git branch -D omnifix-temp-{pr_id} 2>/dev/null
```

**Return to repo root after cleanup:**

```bash
cd {repo_root}
```

If any bash commands during Phases 4-6 changed the working directory into the worktree, this ensures the main agent returns to the repo root. Failure to do this leaves the agent's working directory pointing at a deleted path.

---

## Error Handling

| Error | Response |
|-------|----------|
| gh not authenticated | "Run `gh auth login` first." Stop. |
| PR not found | "PR #{id} not found. Verify the number and repository." Stop. |
| No unresolved comments | "PR #{id} has no unresolved review threads. Nothing to fix." Stop. |
| Network failure | Retry gh command once. If still fails, report error and stop. |
| Worktree creation fails | Try with timestamp suffix. If still fails, clean up and stop. |
| Triage agent fails | Continue with remaining agents. Note gap in results. |
| Fix agent returns BLOCKED | Present blocker to user. Offer to skip that fix or abort. |
| Verification returns NEEDS_REWORK | Rework loop (max 2 iterations), then escalate to user. |
| Push fails (race condition) | Offer rebase, abort, or separate PR. Never force-push. |
| Comment reply fails | Collect error, continue with remaining threads, report summary. |
| Cleanup fails | Force remove directories. Report if still stuck. |

**Cleanup guarantee:** The entire flow is wrapped in a try/finally pattern. Phase 7 runs no matter what.

---

## Red Flags — STOP and Follow the Process

| Thought | Reality |
|---------|---------|
| "I can just apply the fix without triage" | Triage catches false positives. Always triage first. |
| "The fix is obvious, skip verification" | Obvious fixes introduce subtle regressions. Always verify. |
| "I'll push the fix without asking" | Never auto-push. Always ask user before pushing. |
| "I'll auto-reply 'fixed' on all threads" | Default is NO auto-reply. The original reviewer should verify. |
| "I'll commit before verification finishes" | Verification exists to catch regressions. Wait for it. |
| "This finding is clearly valid, no need to check the code" | Be adversarial. Verify against the actual code in the worktree. |
| "I'll skip tests, the change is minor" | Minor changes break things. Run tests when available. |
| "I'll edit files in the main workspace" | All edits happen in the worktree. Never touch the main workspace. |
| "Cleanup can wait" | Stale worktrees accumulate. Clean up immediately. |

**All of these mean: Follow the 7-phase OmniFix process. No shortcuts.**

---

## Never

- Use `glab` (this is GitHub — use `gh` exclusively)
- Push to origin without explicit user permission
- Apply code changes before user approval (Phase 3 gate)
- Auto-reply on threads without user opt-in
- Skip worktree cleanup (even on failure)
- Force-push under any circumstance
- Add AI attribution in commit messages or posted comments
- Edit files in the main workspace (use worktrees)
- Skip any of the 7 phases for any reason

## Always

- Fetch discussions and PR data in Phase 1 before dispatching agents
- Create isolated worktrees for triage and fixing
- Present triage results and wait for explicit user approval
- Apply fixes sequentially in file order (never parallel)
- Run verification before committing
- Ask user before pushing
- Post thread replies with commit SHA references
- Clean up all worktrees regardless of outcome
- Use `gh` for all GitHub operations

---

## Integration

**MCP Tools:**
- `mcp__omniforge__fetch_pr_discussions` — Fetch structured review comment threads
- `mcp__omniforge__fetch_pr_data` — Fetch PR metadata, diff, and diff_line_map
- `mcp__omniforge__reply_to_pr_comment` — Post reply on a review comment thread
- `mcp__omniforge__cleanup_omnifix_worktrees` — Remove all OmniFix worktrees and temp branches

**Subagent Templates:**
- `./references/triage-agent-prompt.md` — Triage Agent (parallel, read-only)
- `./references/fix-agent-prompt.md` — Fix Agent (single, writable)
- `./references/verify-agent-prompt.md` — Verification Agent (fresh-eyes review)

**Uses:**
- `superpowers:using-git-worktrees` — Worktree setup/teardown pattern
- `superpowers:dispatching-parallel-agents` — Parallel dispatch pattern
