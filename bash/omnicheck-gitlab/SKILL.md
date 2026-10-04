---
name: omnicheck-gitlab
description: Use when checking if MR review findings have been applied — verifies both OmniForge-generated and human reviewer comments against the current diff, posts nudge replies on unaddressed threads
argument-hint: <mr-number>
allowed-tools: [Read, Glob, Grep, Bash, Agent, Write, Edit]
---

# OmniCheck

> **Verify whether requested MR changes have been applied — diff analysis + targeted nudge comments.**

Check all discussion threads on a GitLab MR against the current diff. Resolved threads are marked APPLIED. Unresolved threads are analyzed by a subagent to determine if the fix was applied silently or not at all. Unaddressed threads receive nudge replies and a summary comment. When every finding is verified applied, offer to approve the MR (as the OmniCheck bot when `OMNICHECK_BOT_TOKEN` is set).

**Core principle:** Thread status check + diff analysis + user approval gate = accurate, non-spammy follow-up — and, when clean, a one-keystroke approval.

**Announce at start:** "I'm using OmniCheck to verify findings on MR !{id}."

## Prerequisites

- `glab` CLI authenticated (`glab auth status` to verify)
- Git repository with remote pointing to GitLab
- Current working directory is in the git repo
- MR must have discussion threads

## Input Parsing

Accept any of: MR number (`136`), prefixed (`!136`), or full GitLab URL.
Extract MR ID. If URL provided, extract project path and MR IID.

## The Process

```
Phase 1: GATHER   — fetch all threads + MR diff/data
Phase 2: ANALYZE  — single subagent checks each open thread against the diff
Phase 3: REPORT   — present status table, then branch:
                     Branch A (unaddressed findings): user approves nudge list
                     Branch B (all verified):         "Approve MR? [Y/n]"
Phase 4: ACT      — Branch A: reply on each NOT_APPLIED thread + summary comment
                     Branch B: approve_mr() + summary comment
Phase 5: DONE     — no cleanup needed (no worktrees)
```

> **Auto-approval (Branch B) is OFF by default.** It only appears when `NOT_APPLIED + NEEDS_HUMAN = 0`, and only fires if the user answers **Y**. When `OMNICHECK_BOT_TOKEN` is set, `approve_mr` approves as the bot so it can clear the gate even when "Prevent approval by creator/committer" blocks the human user. See the setup guide.

---

## Thread Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| `APPLIED` | Thread is resolved — trusted as-is | None |
| `SILENTLY_APPLIED` | Thread open, but diff shows the concern was addressed | Note in summary only |
| `NOT_APPLIED` | Thread open, diff shows no relevant change | Nudge: thread reply + summary row |
| `NEEDS_HUMAN` | Ambiguous — cannot determine from diff alone | Flag in report; no automatic nudge |

## Verification Model v2 (dispositions, severity, kind, gate)

**REQUIRED REFERENCE:** `./references/verdict-model.md` — the closed vocabulary
(single source of truth, shared with the push sweep). The deterministic model
lives in `./scripts/omni_verdict.py` (pure stdlib; also a thin CLI:
`python3 omni_verdict.py --in <threads.json>`).

Before dispatching the analysis agent, run the deterministic layer over the
fetched threads:

1. **Artifact/command filter** — review report posts (`## OmniForge`), fix
   briefs, disposition summaries, regenloop round summaries, trigger commands
   (`/omnireview`, `/omniforge`, `/omnicheck`), and bot status notes never
   classify as findings.
2. **Disposition** — `fixed / not_fixed / obsolete / deferred / declined /
   decision / artifact`. Resolved threads are `fixed` **unless** a reply
   records a deferral/decline/decision (valid consent). Open threads with a
   consent reply are DISPOSED (`deferred`/`declined`/`decision`) — reported as
   ATTENTION_REQUIRED, never nudged, never blocking.
3. **Severity** — `critical|important|minor` from `**Critical**`-style markers,
   `severity:` JSON, or the regenloop `**blocking**`/`**non-blocking**`/`**note**`
   convention; unmarked threads are `minor` (severity must be evidenced to gate).
4. **Kind** — `code|test|docs|process|decision` from the anchor path and body.

Only threads that still need diff verification (open, not disposed, not
artifacts) go to the analysis agent. After verdicts return, compute the gate
with `omni_verdict.gate(findings)`:

- `BLOCKED` — an unfixed Critical/Important **code** finding with no valid consent.
- `CLEAN` — nothing open at all.
- `READY_WITH_NOTES` — anything else (open minors, unfixed test/docs/process
  findings, ATTENTION_REQUIRED disposed threads).

Fail-closed applies to the blocking class ONLY — process/decision threads and
report artifacts can never gate (this retires the audit's over-rejection
class), while unanswered Important code findings still block (retaining
fail-closed where it matters).

---

## Phase 1: Gather

**Step 1:** Fetch all discussion threads.

```
mcp__omniforge__fetch_mr_discussions(mr_id="{id}", repo_root="{cwd}")
```

Returns structured threads with: `id`, `resolvable`, `resolved`, `type`, `file_path`, `line_number`, `body`, `author`, `replies`. The tool already excludes discussions whose notes are all system-generated — every thread returned contains at least one human note.

**Note:** When building `{UNRESOLVED_THREADS_JSON}` for the analysis subagent, include each thread's `id` field as `discussion_id` so verdicts can be mapped back to GitLab thread IDs for posting replies.

**Step 2:** Partition threads.
- `resolved: true` → pre-labeled `APPLIED`, skip analysis
- `resolved: false` (any `resolvable` value) → pass to Phase 2. This includes both resolvable inline threads and general (`resolvable: false`) human comments — both can receive nudge replies.

**Step 3:** Fetch MR metadata and diff.

```
mcp__omniforge__fetch_mr_data(mr_id="{id}", repo_root="{cwd}")
```

Returns: title, author, source_branch, target_branch, diff, diff_line_count, commits, files_changed, head_sha, `truncated_files`.

**Truncation guard:** when `diff_truncated` is true, threads anchored in `truncated_files` cannot be verified from the diff — mark them NEEDS_HUMAN with the stated truncation reason (run `omni_verdict.apply_truncation_guard`, or set the reason manually). Never report "no relevant change" for a region the diff never showed.

**Step 4:** Early exit checks.
- Zero threads returned: "MR !{id} has no discussion threads. Nothing to check." Stop.
- Zero unresolved threads (`resolved: false`): "All {N} threads are resolved. Nothing to nudge." Stop.

**Step 5:** Present: "Found {N} total threads ({R} resolved, {U} unresolved). Analyzing {U} unresolved threads."

---

## Phase 2: Analyze (Single Subagent)

**Goal:** For each unresolved thread, determine if the diff addresses its concern.

**Template:** `./references/analysis-agent-prompt.md`

Fill template placeholders:
- `{MR_ID}` — MR number
- `{MR_TITLE}` — MR title
- `{UNRESOLVED_THREADS_JSON}` — JSON array of all unresolved threads
- `{GIT_DIFF}` — Full diff string from Phase 1

**Large MR handling:** If unresolved thread count > 15 AND diff_line_count > 5000, group threads by file and dispatch up to 3 subagents. Merge results before Phase 3.

### Expected Return

```json
[
  {
    "discussion_id": "abc123",
    "file_path": "src/auth.py",
    "line_number": 47,
    "body_summary": "Missing null check on user input",
    "verdict": "NOT_APPLIED",
    "confidence": 91,
    "reasoning": "The diff shows no changes to src/auth.py around line 47. The null check is still absent."
  },
  {
    "discussion_id": "def456",
    "file_path": ".gitlab-ci.yml",
    "line_number": 1072,
    "body_summary": "Missing placeholder mapping for STRIPE_PRICE_ENTERPRISE",
    "verdict": "SILENTLY_APPLIED",
    "confidence": 87,
    "reasoning": "Line 1072 in .gitlab-ci.yml was changed in the diff to include the placeholder mapping. The thread was not resolved but the concern is addressed."
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
OmniCheck — MR !{id}: {title}

  ✓ Applied (resolved):     {N} threads
  ✓ Silently Applied:       {N} threads
  ✗ Not Applied:            {N} threads
  ? Needs Human Review:     {N} threads
```

Then branch on the gate outcome and outstanding findings.

### Branch A — there are unaddressed findings (`not_fixed` findings remain, or the gate is BLOCKED)

This is the standard nudge path. Show the breakdown and ask before posting:

```
NOT_APPLIED threads (will receive nudge):
  1. {file}:{line} — {body_summary} [confidence: {score}%]
  2. {file}:{line} — {body_summary} [confidence: {score}%]

NEEDS_HUMAN threads (no automatic nudge):
  3. general — {body_summary}

Post nudge replies on NOT_APPLIED threads? [Y/n]
(Enter numbers to exclude specific threads, e.g. "exclude 2")
```

On approval, proceed to Phase 4 Branch A.

### Branch B — all findings verified or disposed (no `not_fixed` findings remain)

There is nothing to nudge. DISPOSED threads (deferred / declined / decision)
are listed as ATTENTION_REQUIRED — they do not block, but say so before
approving. Offer to **approve** the MR instead:

```
✅ All {N} findings verified applied (0 unresolved).
Approve MR !{id}? [Y/n]
```

- On **Y**: proceed to Phase 4 Branch B (`approve_mr()` + a summary comment).
- On **n**: stop — nothing left to do. Report "No findings to nudge; approval skipped."
- If `OMNICHECK_BOT_TOKEN` is **not** set, warn the user that `approve_mr` will run as the *current* `glab` user, which is blocked when that user is the MR author or a committer (the likely reason for running this). Still proceed if they confirm.

**CRITICAL: No comments are posted and no approval is issued until the user explicitly approves at the gate.**

---

## Phase 4: Act

Take the branch selected in Phase 3.

### Branch A — Nudge (unaddressed findings)

**REQUIRED REFERENCE:** `./references/nudge-guide.md` — contains the exact thread reply template and summary comment template. Do NOT post without loading this reference.

For each approved NOT_APPLIED thread:

**Step 1:** Post thread reply.

```
mcp__omniforge__reply_to_discussion(
  mr_id="{id}",
  discussion_id="{discussion_id}",
  body="{nudge_reply_text}",
  repo_root="{cwd}"
)
```

**Step 2:** After all thread replies succeed or fail, post one summary comment.

```
mcp__omniforge__post_review_summary(
  mr_id="{id}",
  summary="{summary_comment_text}",
  repo_root="{cwd}"
)
```

**Ordering guarantee:** All thread replies before the summary comment.

**On reply failure:** Collect the failure, continue with remaining threads, and note the failure in the summary comment.

### Branch B — Approve (all findings verified)

**Step 1:** Approve the MR. The tool approves as the OmniCheck bot when `OMNICHECK_BOT_TOKEN` is set, else as the current `glab` user. It pins to the MR HEAD sha automatically — pass `checked_sha` = the `head_sha` the Phase-1 fetch recorded, so a head move since the check refuses the approval.

```
mcp__omniforge__approve_mr(
  mr_id="{id}",
  repo_root="{cwd}",
  checked_sha="{head_sha from Phase 1}"
)
```

Check the returned `approver` (`bot` | `current_user`) and `success`. If `success` is false (commonly `403` / "not allowed to approve"), report the cause to the user and stop — do **not** post a misleading success comment. The tool also REFUSES (fail-closed) on: `unresolved_threads` (a resolvable thread is still open), `missing_reviewed_label` (the MR lacks `omniforge::reviewed` — run the OmniForge review first; this approval must never certify an unreviewed MR), and `head_moved` (re-run the check at the new head). Other typical causes: bot is not a Maintainer, bot is not an Eligible approver, the token is unset so the current (blocked) user was used, or the bot is the MR author/committer.

**Step 2:** Only after a successful approval, post one summary comment.

```
mcp__omniforge__post_review_summary(
  mr_id="{id}",
  summary="{approval_summary_comment_text}",
  repo_root="{cwd}"
)
```

The summary comment states how many findings were verified and that the MR was approved (by the bot or current user). No AI attribution.

**Ordering guarantee:** Approve first, summary comment second — never claim approval in the comment if `approve_mr` failed.

---

## Phase 5: Done

No worktrees → no cleanup needed.

Report:
```
OmniCheck complete — MR !{id}

  ✓ Nudged: {N} threads            (Branch A)
  ✗ Failed to post: {N} threads (list them)

  — or —

  ✓ Approved: as {approver}        (Branch B)
  ✗ Approval failed: {reason}
```

---

## Error Handling

| Error | Response |
|-------|----------|
| glab not authenticated | "Run `glab auth login` first." Stop. |
| MR not found | "MR !{id} not found. Verify the number and repository." Stop. |
| No discussion threads | "MR !{id} has no discussion threads. Nothing to check." Stop. |
| All threads resolved | "All {N} threads are resolved. Nothing to nudge." Stop. |
| Analysis agent fails | Present error to user; offer to retry or abort |
| Thread reply fails | Continue with remaining threads; note failure in summary |
| Summary comment fails | Report failure; thread replies already posted |
| `approve_mr` fails (403) | Report cause (not Maintainer / not eligible approver / token unset / bot is author); do not post a success comment |

---

## Integration

**MCP Tools:**
- `mcp__omniforge__fetch_mr_discussions` — Fetch all discussion threads
- `mcp__omniforge__fetch_mr_data` — Fetch MR metadata and diff
- `mcp__omniforge__reply_to_discussion` — Post nudge reply on a thread
- `mcp__omniforge__post_review_summary` — Post summary comment on MR
- `mcp__omniforge__approve_mr` — Approve MR (as bot when `OMNICHECK_BOT_TOKEN` set, else current user)

**Subagent Template:**
- `./references/analysis-agent-prompt.md` — Analysis Agent (single, diff-only check)

**Deterministic model + replay:**
- `./scripts/omni_verdict.py` — disposition/severity/kind extractors, artifact filter, gate (import, or CLI: `--in threads.json`)
- `./references/verdict-model.md` — the vocabulary decision (single source of truth; the push sweep reuses it verbatim)
- `./scripts/replay_audit.py` + `./references/replay-table-2026-09-11.md` — audit-corpus replay harness and the release-gate table it produced

---

## Never

- Post comments or approve the MR without explicit user approval (Phase 3 gate)
- Offer approval (Branch B) when `NOT_APPLIED + NEEDS_HUMAN > 0`
- Post a success/approval summary comment when `approve_mr` failed — report the failure instead
- Add AI attribution to any posted comment
- Use `gh` (GitLab — use `glab` exclusively)
- Auto-resolve any threads (OmniCheck only nudges and approves, never resolves)
- Create worktrees (diff-only analysis)
- Skip any of the 5 phases

## Always

- Fetch threads and diff in Phase 1 before dispatching analysis
- Present status table and wait for user approval before posting
- Post thread replies before the summary comment
- Report final outcome including any failed posts
- Use `glab` for all GitLab operations
