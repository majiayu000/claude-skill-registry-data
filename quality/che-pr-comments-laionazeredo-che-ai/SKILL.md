---
name: "che-pr-comments"
description: "Scans all comments on a GitHub PR, classifies them (human vs bot / valid vs invalid / actionable vs nitpick), produces a structured triage report, and prepares: (a) a numbered implementation plan for valid actionable comments, (b) pre-written English responses for comments we should reject/ignore. Invoke when user passes a PR URL and asks to process review comments, or when /che-pr-comments is called."
---

# Che — PR Comments Triage & Response Drafts

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - GitHub CLI gh auth + pull/post comments commands: `_shared_checklists/GITHUB_CLI_COMMON.md`
> - Security/PII triage for review comments about compliance: `_shared_checklists/SECURITY_PII_COMMON.md`

Given a GitHub PR URL, this skill:
1. Pulls ALL comments (issue-level + review-level + individual file review comments) via `gh`.
2. Classifies and groups.
3. Produces a triage report: what to IMPLEMENT, what to RESPOND and reject, what to mark as resolved without action.

**NEVER actually posts comments to GitHub UNLESS user explicitly says "upload these responses". First deliver the triage + plan + draft responses to the user chat for approval.**

---

## 0. Preconditions

1. **PR URL** from user. If missing → ASK.
2. **`gh auth status` OK.** If not → guide user and stop.
3. Worktree path optional: if provided, we can actually implement the valid ones later. If not, triage and drafts only.

---

## 1. Gather ALL PR comments

Use `gh` CLI (not browser):

```bash
# Issue-level comments (PR body replies, general comments)
gh pr view <PR_URL> --json comments,number > /tmp/issue-comments.json

# Review-level: every review (APPROVED / CHANGES_REQUESTED / COMMENTED) + per-file comments inline
gh pr view <PR_URL> --json reviews > /tmp/reviews.json
# Reviews include .comments[] on each review (in-file line comments)
```

Flatten and de-duplicate into one list: `ALL_COMMENTS[]`.

For each comment record:
```
id:
author_username:
author_association: OWNER / MEMBER / COLLABORATOR / CONTRIBUTOR / FIRST_TIME_CONTRIBUTOR / NONE
body_text: raw markdown / text
is_bot: true/false (check username ends with [bot], or known bot list: dependabot[bot], renovate[bot], codecov[bot], github-actions[bot], lintr[bot], snyk-bot, vercel[bot], deploy-preview, sonarcloud...)
in_reply_to_comment_id: null or parent id
file_path: null (issue-level) OR path (inline review)
line_number: null or line number
created_at: ISO
resolved? (optional: look at review comments API for resolved flag)
```

---

## 2. Classify EACH comment into categories

### 2.1 Author kind → HUMAN vs BOT vs SYSTEM

- **BOT / CI**: if username matches known bot list or `author_association=NONE + username contains bot`.
  Examples: codecov comment, dependabot merge conflict note, lint warning line note, vercel preview URL.
- **SYSTEM / meta**: "This PR was edited by ...", merge conflict banner, auto-generated release notes.
- **HUMAN**: everything else.

### 2.2 Content classification

For BOT comments → auto-classify:
| Pattern | Classification |
|---|---|
| Codecov report: "Coverage decreased by 0.3%" | BOT_COVERAGE (INFO, usually non-actionable unless >3% drop) |
| Lint bot inline line note | BOT_LINT_WARNING — cross-check with latest CI run; if CI clean, outdated, mark resolved |
| Dependabot alerts / vuln notice | BOT_VULN — HIGH priority, must act |
| Renovate version bump description | BOT_DEPS — meta |
| Vercel preview URL deployment | BOT_PREVIEW — link only, no action needed unless link broken |
| SonarCloud quality gate fail | BOT_SONAR — cross-check findings |
| Any bot with "This branch has conflicts that must be resolved" | BOT_MERGE_CONFLICT — HIGH, PR block, must fix. |

For HUMAN comments → classify content:

| Sub-type | Signals | Actionable? |
|---|---|---|
| **CORRECTNESS_REQUEST**: actual bug / logic issue | Phrases: "This crashes when X", "this should return Y when Z"; includes example input/output; refers to runtime behavior | ✅ YES, HIGH priority |
| **SECURITY_REQUEST**: PII / injection / auth issue | Keywords: security, PII, log this email, SQL string concat, no auth check | ✅ YES, CRITICAL priority |
| **ARCHITECTURE_REQUEST**: cross-module concern | "We should move this to X layer instead", "this couples A+B which is bad" | ✅ YES, MEDIUM priority — only if reviewer gives rationale; vague "this is bad architecture" = DISCUSSION |
| **SCOPE_CREEP_WARNING**: "this should NOT be in this PR" | Reviewer points out extra code unrelated to ticket | ✅ YES, per user spec: scope deviation must be flagged |
| **QUESTION**: reviewer doesn't understand, asks why | "Why did you use X instead of Y?", ends with `?` | ✅ RESPONSE needed, NO code change required |
| **NIT / STYLE_PREFERENCE**: Biome / format / naming preference | "Rename to snake_case pls", "extra blank line" | ⚠️ LOW priority. Usually response "Done" if easy; otherwise repo convention decides. |
| **PRAISE / LGTM / APPROVAL_META**: "Looks good", "nice work", "LGTM!" | | ❌ No action |
| **DISCUSSION / OPINION**: debatable, no clear right/wrong | "IMO we should use zod here not manual" (when repo already uses manual guards) | ❌ Discussion only. Respond once explaining rationale; don't change unless maintainer overrules OR you agree it's a good idea anyway |
| **OUTDATED**: comment on line that was already changed / no longer applies | | ❌ Mark resolved with "Fixed in <commit sha>" or without response |
| **DUPLICATE**: same exact point already raised by another comment | | ❌ Ignore after confirming duplicate |

---

## 3. Triage Report Structure

### 2.9 🔴 STORAGE PREFLIGHT + MANDATORY PATHS (BEFORE FIRST WRITE)

Run EXACTLY this block; then use ONLY `che output_path`. NEVER construct paths manually.
NEVER create `<worktree>/.trae/` or `<worktree>/reports/` or `<worktree>/pr_comments/`. MORATORIUM §20.

```bash
# Resolve the `che` CLI (owns the Che-home cascade + canonical path construction)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Aborting write."; exit 98; }

SESSION_ID="${CHE_CURRENT_SESSION_ID:-${CHE_SESSION_ID:-fallback-pr-comments-session}}"
if [ -n "${WORKTREE_ROOT:-}" ] && [ -d "$WORKTREE_ROOT" ]; then
  eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
  che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"
  che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "WORKSPACE_SHARED"
fi

# Construct UNIQUE path via CLI:
# - type = pr_comments (maps to subfolder pr_comments/)
# - slug = triage-report
# - related_id = pr-<ID> (groups everything related to this PR)
# - scope = workspace (durable: shared between sessions in this worktree, can be reopened tomorrow)
# - ext = md
PR_COMMENTS_REPORT_PATH="$(che output_path "pr_comments" "triage-report" "pr-${PR_ID}" "workspace" "md")"
```

Example result: `$CHE_WORKSPACE_SHARED/pr_comments/pr-382/20260902-111500-triage-report.md`
→ Timestamp prefix automatically sorts if there are multiple triage rounds on the same PR.
→ related_id = `pr-382` groups everything together. Trivial future search: `ls -1 pr_comments/pr-382/*.md`.

**Final file written using atomic write:**
```bash
# pipe the full markdown content to the atomic helper (tmp → mv):
cat <<'MARKDOWN_EOF' | che write_file_atomic "$PR_COMMENTS_REPORT_PATH"
# ... triage report body here ...
MARKDOWN_EOF
```

### Summary table

| Bucket | Count |
|---|---|
| BOT comments (total) | `N` |
|   BOT_MERGE_CONFLICT (action required) | `N` |
|   BOT_VULN (action required) | `N` |
|   BOT_COVERAGE / LINT_WARNING / PREVIEW / DEPS / META (no action) | `N` |
| HUMAN comments (total) | `N` |
|   ✅ TO IMPLEMENT — Code change required | `N` |
|   ✏️ TO RESPOND — No code change, draft reply needed | `N` |
|   ❌ OUTDATED / DUPLICATE — Resolve silently | `N` |
|   💬 PRAISE / LGTM / APPROVAL_META — Ignore | `N` |
|   ⚠️ NIT — Optional, decide per user | `N` |
|   🗣️ DISCUSSION / OPINION — User decides | `N` |

---

### Section 1: ✅ TO IMPLEMENT (sorted by priority: CRITICAL → HIGH → MEDIUM → LOW)

Each entry:
```
## I-1 <severity> — <short description>

Reviewer: @username (role: COLLABORATOR)
File:line: path/to/file.ts:42
Original comment body:
> <quoted markdown>

Rationale for implementation:
<1 sentence: this is a real bug / security issue / scope mismatch → must act>

Proposed code change plan:
- File 1: change lines XX-YY → replace `<old>` with `<new>`
- File 2: ...
- Tests: add / modify spec at `<path>` to cover this fix

Estimated blast radius: N files (≤ 10 or flag for user re-evaluation)
Estimated effort: XS / S / M / L
```

### Section 2: ✏️ TO RESPOND — Human comments, no code change

Each entry uses four fields plus the post command. Nothing else — the user copies THIS, not the triage above.

```
## R-1 — <short title of what comment was>

Reviewer: @<username>
Comment ID: <numeric id of the review comment being answered>
Context: <issue-level | in-file:path:line>
Original comment:
> <quoted, trimmed to 2 lines max>

### Action: DECLINE — reply only, no code change.

Rationale (1 line):
<why we are NOT making the code change. E.g.: "Repo convention uses manual guards everywhere already; moving to zod here is inconsistent + out of scope for this ticket. We can open a follow-up for the migration.">

### Reply (ENGLISH, MAX 2 sentences, simple, ready to paste):
Thanks for raising this, @<username> — the current approach matches the convention used in <file1> and <file2>, so I would rather keep it consistent here. I have noted the migration as a follow-up for a separate refactor PR so we do not lose it.

### Post command (inline review comment):
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body='Thanks for raising this, @<username> — the current approach matches the convention used in <file1> and <file2>, so I would rather keep it consistent here. I have noted the migration as a follow-up for a separate refactor PR so we do not lose it.'
```

HARD RULES for the reply command:

1. **Two endpoints, pick by where the comment lives.** Inline review comment → `POST /repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies`. PR-level (issue) comment → `POST /repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments` (no `<COMMENT_ID>`).
2. **`COMMENT_ID` is the numeric id of the comment being answered**, not the review id and not the thread id. Read it with `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --jq '.[] | {id, path, line, user: .user.login}'`.
3. **MAX 2 sentences.** If the objection does not fit in two, we have not understood it yet — go back to classification, do not pad the reply.
4. **Prefer phrasing without apostrophes** inside `-f body='...'` — English contractions ("doesn't", "won't", "I'd") break the shell string. Write "does not" / "I would" instead, or post from stdin with `-F body=@-` when the wording genuinely needs a contraction.
5. **Replying works even when the comment is OUTDATED** — the endpoint targets the comment, not the line, so an outdated thread can still be answered in place.
6. **Never auto-post.** Same rule as §5: only after the user explicitly says to post the responses, and only for the entries the user names.

### Section 3: 💬 DISCUSSION — User decides (we draft BOTH sides)

Same four fields as Section 2, but `Action: PENDING USER` and two reply drafts instead of one.

```
## D-1

Reviewer: @<username>
Comment ID: <numeric id>
Context: <issue-level | in-file:path:line>
Original comment:
> "IMO use zod instead."

### Action: PENDING USER — this reviewer is <owner|member|contributor>; do not decide alone.

### Reply if we ACCEPT:
<2-sentence English reply confirming the change, plus which commit will carry it>

### Reply if we DECLINE:
<2-sentence English reply, same shape as Section 2>

### Post command (run only the draft the user picks):
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies -f body='<the chosen 2-sentence reply>'
```

### Section 4: NITs — quick / optional

```
## N-1 — "rename var to snake_case"

Action: DONE via trivial edit (≤ 5 min effort). We'll include in same commit batch.
OR
Action: DECLINED + response (see Section 2 style).
```

### Section 5: OUTDATED / DUPLICATE / RESOLVED SILENTLY

Numbered list with IDs and 1-line: "Resolved without posting a reply."

---

## 4. Proposed aggregated implementation plan (if user says "proceed with implement")

Aggregate all Section 1 items into logical batches (atomic commits):

```
Aggregated plan:

Batch 1 — Commit: fix(security): patch email log PII leak in order flow
  • I-1 (CRITICAL) — path/to/log
  • Tests: update log assertion specs

Batch 2 — Commit: fix(correctness): early return when profile is null
  • I-2 (HIGH) — renderPhone function
  • Tests: add null profile test case

Batch 3 — Commit: chore(scope): remove password reset feature added by mistake
  • I-3 (MEDIUM scope creep) — delete PasswordReset.vue + references

Estimated total new commits: 3
Estimated total files touched: 6 (≤ 10 ✅)
```

---

## 5. Hard stops / rules

- **Never write a response that sounds aggressive / dismissive.** Always: thank → explain rationale → offer follow-up / alternative path.
- **Never auto-decide ARCHITECTURE_REQUEST or DISCUSSION when reviewer is a repo OWNER/MEMBER.** Flag to user: "This reviewer is an owner/maintainer. I suggest implementing unless you strongly disagree."
- **Never auto-post replies to GitHub.** Only do so when user explicitly types: "upload these responses" or similar, and AFTER user approves the full triage report + plan + response drafts.
- If any comment says "Merge conflicts" / "This branch is out-of-date with base" — classify as BOT_MERGE_CONFLICT → HIGH priority, must resolve as part of Section 1 before anything else.
