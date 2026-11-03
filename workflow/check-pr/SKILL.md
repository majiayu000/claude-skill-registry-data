---
description: "Address PR review findings from inline threads and general review summaries, verify their disposition, and respond where each was raised."
---

# /check-pr

Address PR review findings from inline threads and general review summaries, verify their disposition, and respond where each was raised.

## Arguments

- `$ARGUMENTS` - PR number (optional, defaults to current branch's PR)

## Instructions

### 0. Wait for Automated Reviews

Copilot review typically takes **3-5 minutes** after PR creation to even begin. If you run `/check-pr` immediately after creating the PR, the review won't exist yet.

Check the repository's Copilot requirement and current review state. Process every posted review. If a required review is pending, wait through the host's supported mechanism; it remains a merge gate. If an optional review is unavailable, record that fact and continue the independent review and existing feedback rather than waiting indefinitely. The bounded polling example below applies only where the host permits it; use native review/status controls otherwise.

```bash
PR_NUM=${1:-$(gh pr view --json number -q .number)}
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Check how old the PR is
PR_AGE_SECONDS=$(gh pr view ${PR_NUM} --json createdAt \
  --jq "((now - (.createdAt | fromdateiso8601)))")

# Check Copilot review status
COPILOT_STATUS=$(gh api repos/${REPO}/pulls/${PR_NUM}/reviews \
  --jq '[.[] | select(.user.login == "copilot-pull-request-reviewer[bot]")] | if length == 0 then "NOT_FOUND" elif (any(.[]; .state == "PENDING")) then "IN_PROGRESS" else "COMPLETED" end')

# If no review exists yet AND PR is less than 5 min old, wait for it to appear
if [ "$COPILOT_STATUS" = "NOT_FOUND" ] && [ "${PR_AGE_SECONDS%.*}" -lt 300 ]; then
  echo "PR is ${PR_AGE_SECONDS%.*}s old. Copilot review not yet started. Waiting (polls every 30s, max 5 min)..."
  for i in $(seq 1 10); do
    sleep 30
    COPILOT_STATUS=$(gh api repos/${REPO}/pulls/${PR_NUM}/reviews \
      --jq '[.[] | select(.user.login == "copilot-pull-request-reviewer[bot]")] | if length == 0 then "NOT_FOUND" elif (any(.[]; .state == "PENDING")) then "IN_PROGRESS" else "COMPLETED" end')
    [ "$COPILOT_STATUS" != "NOT_FOUND" ] && echo "Copilot review detected (status: $COPILOT_STATUS)" && break
  done
fi

# If review is in progress, wait for it to complete
if [ "$COPILOT_STATUS" = "IN_PROGRESS" ]; then
  echo "Copilot review in progress. Polling every 30s (max 5 min)..."
  for i in $(seq 1 10); do
    sleep 30
    COPILOT_STATUS=$(gh api repos/${REPO}/pulls/${PR_NUM}/reviews \
      --jq '[.[] | select(.user.login == "copilot-pull-request-reviewer[bot]")] | if length == 0 then "NOT_FOUND" elif (any(.[]; .state == "PENDING")) then "IN_PROGRESS" else "COMPLETED" end')
    [ "$COPILOT_STATUS" != "IN_PROGRESS" ] && break
  done
fi
```

### 1. Fetch PR Info

```bash
# Fetch all review comments (inline) — paginate to avoid truncation
gh api repos/${REPO}/pulls/${PR_NUM}/comments --paginate

# Fetch all reviews
gh api repos/${REPO}/pulls/${PR_NUM}/reviews --paginate

# Fetch issue-level comments (to check if previous check-pr already ran)
gh api repos/${REPO}/issues/${PR_NUM}/comments --paginate
```

Read the bodies of general reviews and issue comments, including agent-review summaries and linked findings. A review with no inline thread can still contain a blocking defect. Deduplicate the same finding across sources and retain its permalink and disposition evidence.

### 2. Skip Already-Replied Comments (Idempotency)

Before processing, filter out comments that already have replies from this workflow.
This makes `/check-pr` safe to re-run without duplicating work.

```bash
# Fetch all review comments with reply threading info
ALL_COMMENTS=$(gh api repos/${REPO}/pulls/${PR_NUM}/comments --paginate)

# Determine the current workflow user (used to detect this workflow's replies)
WORKFLOW_USER=$(gh api user --jq .login)

# Build list of comment IDs that already have replies FROM THIS WORKFLOW (filter by author)
REPLIED_IDS=$(echo "$ALL_COMMENTS" | jq --arg user "$WORKFLOW_USER" \
  '[.[] | select(.in_reply_to_id != null and .user.login == $user) | .in_reply_to_id] | unique')

# Filter to only unprocessed top-level comments (no existing reply from this workflow)
PENDING_COMMENTS=$(echo "$ALL_COMMENTS" \
  | jq --argjson replied "$REPLIED_IDS" \
    '[.[] | select(.in_reply_to_id == null) | select([.id] | inside($replied) | not)]')
```

Use `PENDING_COMMENTS` to avoid duplicate inline replies. Also process unaddressed findings in general reviews and issue comments. An existing reply, resolved thread, or linked issue is not proof a finding is fixed: re-check its disposition against the current head before carrying forward a clean verdict. Exit as already addressed only when both inline and general findings have supported dispositions.

### 3. Process EVERY Pending Finding — ONE AT A TIME

Honor any caller-supplied correction-round and budget allowance from the shared run record. Use the current round recorded by `/full-review`; do not count it twice or reset it here. Before beginning a new correction round, establish and record its remaining allowance before editing. At an exhausted or unknown applicable limit, report unresolved blocking findings as `**BLOCKED**`, retain `request_changes`, and return control without starting another repair. Eligible nonblocking findings can still be documented as follow-ups. Read-only disposition checks may continue within remaining budget.

For each pending review comment (Copilot or human), you MUST do ALL of these steps **before moving to the next comment**:

1. Read the comment carefully
2. Establish one of the three completed dispositions below, or leave a verified unresolved blocker pending
3. Take the required action AND post a reply

Reply inline to each inline finding (`gh api ... /comments/${COMMENT_ID}/replies`). For a finding in a general review or issue comment, post its disposition on the PR with the source permalink. A combined summary does not replace those replies.

**Triage by impact before choosing a disposition.** Verify uncertain claims and distinguish blocking correctness, security, data-integrity or promised-acceptance defects from low-impact nonblocking findings and optional improvements. Record whether the finding is new, worsened or pre-existing; provenance informs the analysis but does not alone decide severity.

**Blocking findings must be fixed, removed or verified contained before merge.** An authorized fallback must preserve safety, correctness, required runtime/cost constraints and essential capability; record its evidence and track the underlying problem. If no acceptable remedy is possible within scope and limits, keep the PR blocked and advance independent authorized work. A time estimate, file boundary or issue URL is not an exemption.

**Documented low-impact nonblocking findings may be deferred**, including minor findings introduced by this PR, when evidence shows the agreed feature remains acceptable and no blocking correctness, security or data-integrity risk is left open. Create or link a scoped issue and explain the impact and deferral rationale. Do not require another CI cycle solely for an eligible follow-up. Small size alone does not make a finding nonblocking.

**There are THREE valid completed dispositions. Use one only when its evidence supports closing the finding:**

1. **FIX** — Make the code change, commit, reply with commit hash + before/after code
2. **FALSE POSITIVE** — Reply explaining why the suggestion is incorrect, with evidence
3. **FOLLOW-UP ISSUE** — Track a verified low-impact nonblocking finding, optional improvement, or underlying problem already contained by the verified fallback above; reply with the issue URL, impact and evidence that the current PR remains acceptable

**There is NO "acknowledge and move on" option.** A valid deferred finding needs a scoped issue and supported rationale; a blocking finding needs a fix, removal or verified containment. Never use "out of scope" or an issue link to clear a blocking finding.

**REPLY FORMAT:** A completed disposition starts with `**FIX**`, `**FALSE POSITIVE**`, or `**FOLLOW-UP ISSUE**` on its own line. If a blocking finding remains unresolved, reply `**BLOCKED**` with the failing behavior, attempted remedies and remaining dependency; keep the thread open and the verdict `request_changes`. BLOCKED is pending work, not a fourth completed disposition.

### Reply Format Examples

Study these examples. Your replies must match this structure exactly.

#### Example: FIX reply

> **FIX**
>
> Fixed in `7bab8be4`
>
> **Change:** Added `marginBottom: 4` to `promptHeaderRow` so spacing is owned by the row container.
>
> ```diff
> - promptHeaderRow: {
> -   flexDirection: 'row',
> -   justifyContent: 'space-between',
> -   alignItems: 'center',
> - },
> + promptHeaderRow: {
> +   flexDirection: 'row',
> +   justifyContent: 'space-between',
> +   alignItems: 'center',
> +   marginBottom: 4,
> + },
> ```

#### Example: FALSE POSITIVE reply

> **FALSE POSITIVE**
>
> **Reason:** The `remaining <= 0` in the dependency array is intentional — it acts as a boolean gate that prevents the effect from re-creating an interval once the countdown reaches zero.
>
> **Evidence:**
> - Without it, the effect would restart on every `expiresAt` change even after expiry
> - Same pattern used in React docs for "run once then stop" effects
> - The expression evaluates to a stable `true`/`false`, not a changing number

#### Example: FOLLOW-UP ISSUE reply

> **FOLLOW-UP ISSUE**
>
> Created https://github.com/owner/repo/issues/123 to track this.
>
> **Reason for deferral:** This optional protocol simplification predates the PR. The current countdown handles reconnects and expiry correctly in the linked tests; the PR introduces no dependency on the proposed change.

---

#### Outcome 1: FIX

When the verified finding blocks delivery, fix it within the shared repair allowance. Eligible nonblocking findings may use Outcome 3.

**Required in reply:** commit hash AND before/after code diff. Both are mandatory.

1. Make the code fix
2. Commit with descriptive message (NO attribution — no Co-Authored-By, no "Generated with", no AI mentions)
3. Reply inline with the EXACT format below:

```bash
gh api repos/${REPO}/pulls/${PR_NUM}/comments/${COMMENT_ID}/replies \
  --method POST \
  -f body="**FIX**

Fixed in \`${COMMIT_SHA}\`

**Change:** Brief description of fix

\`\`\`diff
- old_code_line
+ new_code_line
\`\`\`"
```

**NEVER post a fix reply without the commit SHA and a code diff.** If you fixed it, prove it.

---

#### Outcome 2: FALSE POSITIVE (evidence REQUIRED)

Only use this if the suggestion is factually incorrect. You MUST provide evidence.

**Required in reply:** specific evidence why the comment is wrong (doc reference, code reference, or logical proof).

```bash
gh api repos/${REPO}/pulls/${PR_NUM}/comments/${COMMENT_ID}/replies \
  --method POST \
  -f body="**FALSE POSITIVE**

**Reason:** Clear explanation of why this is correct

**Evidence:**
- Reference to docs/pattern used (e.g., 'per CLAUDE.md: no semicolons')
- Link to similar code in codebase"
```

---

#### Outcome 3: FOLLOW-UP ISSUE (GitHub issue creation MANDATORY)

Use only for the eligible cases defined in step 3. Create or link a matching GitHub issue, explain the finding's impact, provenance and reason for deferral, and cite containment/acceptance evidence. A blocking defect remains blocked until fixed, removed or verified contained.

**Required in reply:** issue URL, impact and evidence that deferral leaves no blocking defect or promised acceptance gap. For a general-review finding use its actual source permalink instead of the inline `COMMENT_URL` construction below.

```bash
# 1. Create the scoped issue unless a matching issue already tracks this finding
# Use existing `enhancement` and `from-review` labels.
# COMMENT_ID — the id of the comment THIS iteration of step 3's loop is
# processing (from step 1's fetched `.../pulls/${PR_NUM}/comments`, same
# per-comment variable the reply examples above use). COMMENT_URL is its
# permalink, for the Filed from: line:
COMMENT_URL="https://github.com/${REPO}/pull/${PR_NUM}#discussion_r${COMMENT_ID}"
ISSUE_URL=$(gh issue create \
  --title "Short descriptive title" \
  --label "enhancement" \
  --label "from-review" \
  --body "$(cat <<EOF
## Context

Filed from: #${PR_NUM} (${COMMENT_URL})

Identified during review of PR #${PR_NUM}.

## Description

What needs to be done and why.

## Original Comment

> Quote the review comment here verbatim

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
EOF
)")

# 2. Reply inline referencing the issue — MUST include the FULL issue URL
# NEVER write "Created a follow-up issue" without the URL. The URL is the whole point.
gh api repos/${REPO}/pulls/${PR_NUM}/comments/${COMMENT_ID}/replies \
  --method POST \
  -f body="**FOLLOW-UP ISSUE**

Created ${ISSUE_URL} to track this.

**Reason for deferral:** Verified low-impact nonblocking finding; state impact, evidence that current acceptance holds, and any verified containment and its limits"
```

---

**INVALID outcomes (never use these):**

- "Good idea, we should do this later" without an issue URL
- "Follow-up." or "Deferred." without a `**FOLLOW-UP ISSUE**` label and issue URL
- "Intentional design decision" without evidence — use FALSE POSITIVE with evidence instead
- "Noted" / "Acknowledged" without a FIX or ISSUE URL
- Any reply without a completed-disposition label or an explicit `**BLOCKED**` pending state
- Empty Reference cells in the summary table

### 4. Push All Fixes

```bash
git push
```

### 5. Cross-Reference Fixes Against Open Issues

After pushing fixes, check if any open `from-review` issues were resolved by the work in this PR. This commonly happens when Copilot feedback addresses the same problem an agent-review issue was tracking.

```bash
# List open from-review issues
gh issue list --label "from-review" --state open --limit 100 --json number,title,body,url

# For each fix, check if an open issue describes the same problem.
# If so, close it with a comment linking the PR:
gh issue comment ${ISSUE_NUM} --body "Addressed in PR #${PR_NUM} — ${DESCRIPTION}."
gh issue close ${ISSUE_NUM}
```

**RULE: Every closed issue MUST reference a PR.** The comment is the paper trail. No silent closes.

### 6. Verify All Inline Replies Were Posted

**This step is MANDATORY. Do NOT skip it.**

```bash
# Count root comments (not replies) from reviewers
ROOT_COUNT=$(gh api repos/${REPO}/pulls/${PR_NUM}/comments --paginate \
  --jq '[.[] | select(.in_reply_to_id == null)] | length')

# Count unique root comments that have at least one reply
REPLIED_COUNT=$(gh api repos/${REPO}/pulls/${PR_NUM}/comments --paginate \
  --jq '[.[] | select(.in_reply_to_id != null) | .in_reply_to_id] | unique | length')

echo "Root comments: ${ROOT_COUNT}, Replied: ${REPLIED_COUNT}"
```

If `REPLIED_COUNT < ROOT_COUNT`, you have UNREPLIED comments. Go back to step 3 and post the missing inline replies BEFORE proceeding. **Do NOT post the summary comment until every thread has a reply.**

### 6b. Resolve Conversation Threads

**This step is MANDATORY whenever branch protection requires conversation resolution before merge.** Posting an inline reply does NOT auto-resolve the thread on GitHub — the REST `/replies` endpoint only adds a comment, leaving the thread state as `isResolved: false`. If you skip this step, the PR sits blocked at merge time even when every comment has a reply, every check is green, and the summary comment claims success. The user has to click "Resolve conversation" once per unresolved thread to unblock the merge. Don't make them.

Resolve only threads whose step-3 disposition is supported at the current head. Export `ELIGIBLE_THREAD_IDS` as the newline-separated GraphQL IDs of those threads from the triage record; do not copy the unresolved list wholesale. Unresolved blocking findings stay open and keep the verdict blocked. Findings in general summaries must satisfy the same gate even though they have no thread to resolve.

GraphQL is required here — REST doesn't expose thread state. Threads are GraphQL-only objects (`PRRT_*` IDs); the `resolveReviewThread` mutation needs the GraphQL node ID, not the REST `databaseId`.

```bash
# Fetch all unresolved review thread IDs (GraphQL — REST doesn't expose thread
# state). --paginate auto-loops on pageInfo.hasNextPage so PRs with >100 threads
# are fully covered; without it, threads on later pages stayed unresolved AND
# unreported, so the resolve step silently appeared to succeed while the merge
# gate stayed red. --jq runs per-page and outputs are concatenated, so we emit
# one ID per line rather than building one mega-array across pages.
THREAD_IDS=$(gh api graphql --paginate -f query="
  query(\$endCursor: String) {
    repository(owner: \"${REPO%/*}\", name: \"${REPO#*/}\") {
      pullRequest(number: ${PR_NUM}) {
        reviewThreads(first: 100, after: \$endCursor) {
          nodes { id isResolved }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
  }" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | .id')

# Resolve only eligible unresolved threads via Python — pass the Base64-ish thread ID
# (PRRT_*) as a GraphQL *variable* (-f id=...) so it never gets interpolated
# into the query string or the shell (merge.md Critical Rule 4). The
# --paginate THREAD_IDS fetch above stays in bash (it only emits IDs). gh
# exits 0 even when the GraphQL response body carries an `errors` array, so
# validate the parsed response's isResolved rather than the exit code;
# surface each failure per-thread.
echo "$THREAD_IDS" | python3 -c "
import sys, subprocess, json, os
eligible = set(os.environ.get('ELIGIBLE_THREAD_IDS', '').split())
q = 'mutation(\$id: ID!) { resolveReviewThread(input: {threadId: \$id}) { thread { isResolved } } }'
for tid in sys.stdin.read().split():
    if tid not in eligible:
        print('  LEFT OPEN: no verified disposition for ' + tid)
        continue
    r = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + q, '-f', 'id=' + tid], capture_output=True, text=True)
    ok = False
    if r.returncode == 0:
        try:
            d = json.loads(r.stdout)
            ok = 'errors' not in d and d['data']['resolveReviewThread']['thread']['isResolved'] is True
        except (ValueError, KeyError, TypeError):
            ok = False
    print('  resolved: ' + tid if ok else '  FAILED to resolve: ' + tid)
"

# Verify zero unresolved threads remain. --paginate emits one length per page,
# which we sum with awk so the count is correct on PRs with >100 threads. If
# this stays nonzero, either the resolve loop failed on specific threads or new
# threads landed mid-flight or a finding remains blocking. Re-triage; never
# resolve a blocking finding merely to make this count zero.
UNRESOLVED=$(gh api graphql --paginate -f query="
  query(\$endCursor: String) {
    repository(owner: \"${REPO%/*}\", name: \"${REPO#*/}\") {
      pullRequest(number: ${PR_NUM}) {
        reviewThreads(first: 100, after: \$endCursor) {
          nodes { isResolved }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
  }" --jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length' \
  | awk '{s+=$1} END {print s+0}')

echo "Unresolved threads: ${UNRESOLVED}"
[ "$UNRESOLVED" -eq 0 ] || { echo "FAIL: ${UNRESOLVED} threads still unresolved"; exit 1; }
```

**Pagination cap:** `gh api graphql --paginate` follows `pageInfo.hasNextPage` until exhausted — no implicit cap. On the rare PR with thousands of threads, GitHub's GraphQL rate limit (5000 points/hr) is the practical ceiling. If you see HTTP 403 with "API rate limit exceeded" from gh on step 6b, the resolve loop will short-circuit on the failing call and the verify will report nonzero — re-run after the rate limit window resets.

**When to skip this step:** only if the repo's branch protection does NOT require conversation resolution AND you have explicit evidence (e.g., a memory/customization note) that unresolved threads are acceptable here. Default behavior is **always resolve**.

**Edge cases:**
- A thread you marked FALSE POSITIVE: still resolve it. The reply records the rationale; if a reviewer disagrees, they can re-open the thread.
- A FOLLOW-UP ISSUE thread: resolve only after confirming step 3's eligibility and evidence. The issue link alone does not establish that the delivered change is acceptable.
- A FIX thread: resolve it after the fix commit lands and the reply with the commit SHA is posted.

### 7. Post Summary Comment

After triaging ALL inline and general findings, post a summary on the PR. Every row needs disposition evidence: fix commit, false-positive evidence, eligible follow-up URL with rationale, or an explicit unresolved blocker. Do not mark a blocker addressed merely to complete the table.

```bash
gh pr comment ${PR_NUM} --body "$(cat <<'EOF'
## Review Comments Addressed

| # | Comment | Outcome | Reference |
|---|---------|---------|-----------|
| 1 | Comment 1 summary | FIX | `abc1234` |
| 2 | Comment 2 summary | FALSE POSITIVE | Evidence: [brief] |
| 3 | Comment 3 summary | FOLLOW-UP | [#456](https://github.com/OWNER/REPO/issues/456) |

**Total:** X comments addressed
- Fixed: Y (commit hashes above)
- False positives: Z (with evidence)
- Follow-up issues created: V (linked above)
- Existing issues closed: W
EOF
)"
```

**Summary table rules:**
- The **Reference** column must NEVER be empty
- FIX rows: commit hash (e.g., `abc1234`)
- FALSE POSITIVE rows: brief evidence summary
- FOLLOW-UP rows: issue URL or auto-linked issue number (e.g., `#456`)

### 8. Report to User

Output a **summary table** followed by details. The table is the PRIMARY output — it must be scannable at a glance.

```markdown
| PR | Comments | Changes | Issues |
|----|----------|---------|--------|
| #XX | N → Y fixed, Z false pos | brief change 1, brief change 2 | Created: #A, #B. Closed: #C |
```

**Column guide:**
- **Comments:** `N → Y fixed` (and `, Z false pos` / `, W deferred` if any)
- **Changes:** Comma-separated brief descriptions of what changed (2-5 words each). Works for fixes, features, refactors — keep it generic.
- **Issues:** `Created: #X, #Y` for new follow-up issues. `Closed: #Z` for resolved from-review issues. `—` if none.

**Capture the results when this run is the review of record** — i.e. check-pr ran standalone
rather than after `/agent-review` (which already records its own `review-result` per its step
7). Map the summary table above onto the schema (`request_changes` while a blocking defect or acceptance gap remains; `approve` only when every inline and general finding has a verified acceptable disposition; otherwise `comment`; one finding per distinct finding)
and record it the same way: `python3 ~/.claude/scripts/review-result.py record --agent <id>
--skill check-pr --pr ${PR_NUM}`.

Then below the table, list:
- Full commit hashes for each fix
- Reasons for any false positives
- URLs for created/closed issues
- PR ready for re-review: Yes/No

## Critical Rules

1. **EVERY pending finding gets a reply** — No silent dismissals. Reply inline for inline findings and with a source permalink for general-review findings. Read both before deciding the PR is clean.
2. **Reply IMMEDIATELY after each comment** — Process one comment at a time: read → fix/defer → post inline reply → next. Do NOT batch all fixes and try to reply later.
3. **Three completed dispositions** — FIX, FALSE POSITIVE, or FOLLOW-UP ISSUE. Unresolved blocking findings stay BLOCKED with open threads and a `request_changes` verdict.
4. **FIX requires commit hash + code diff** — Both mandatory in reply
5. **FALSE POSITIVE requires evidence** — No bare dismissals
6. **FOLLOW-UP requires issue URL and eligibility** — Classify by impact and record evidence for nonblocking deferral; blocking correctness/security/data-integrity defects and missing promised acceptance require a fix, removal or verified fallback before merge. Estimates and issue links do not discharge that gate.
7. **Summary table has no empty cells** — Every row has a reference
8. **Verify before summarizing** — Run the verification step (step 6) and confirm all threads have replies BEFORE posting the summary comment. If any are missing, go back and post them.
9. **Resolve eligible threads (step 6b)** — Posting a reply does NOT resolve a thread. Resolve supported dispositions explicitly; leave unresolved blocking findings open. All threads must satisfy the repository's merge gate before merge.
10. **Idempotent** — Avoid duplicate replies (author-filtered), but re-validate carried-forward dispositions at the current head. Resolution status alone never proves a fix.
11. **No attribution** — Follow Zero Attribution Policy (no Co-Authored-By, no "Generated with Claude", no AI mentions anywhere)

## Example Workflow

```
1. Run /check-pr 42
2. Poll Copilot review... ready (state: COMPLETED)
3. Fetch 5 comments, 2 already replied → 3 pending
4. Comment A: "Missing null check on line 45"
   → Outcome: FIX
   → Commit fix, reply with **FIX** + hash + before/after diff
5. Comment B: "This variable seems unused"
   → Outcome: FALSE POSITIVE
   → Reply with **FALSE POSITIVE** + evidence: "Used on line 78 in _process()"
6. Comment C: "Optional diagnostics for an unchanged background task"
   → Outcome: FOLLOW-UP ISSUE
   → Verify its low impact and that it is not an acceptance dependency; create #99 and reply with evidence + URL
7. Push fixes
8. Verify all threads have replies (step 6)
9. Resolve verified eligible threads via GraphQL (step 6b); remaining blocking findings keep the PR blocked
10. Post summary table (all Reference cells filled)
11. Report to user
```
