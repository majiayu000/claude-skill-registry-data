---
name: greploop
description: >
  Iteratively improves a PR (GitHub), MR (GitLab), or shelved changelist (Perforce) until it reaches
  the repository's configured Greptile merge threshold with zero unresolved actionable comments, or
  until the five-review maximum is reached. Triggers Greptile review, fixes all actionable comments,
  pushes/re-shelves, re-triggers review only for new head SHAs unless a 5/5 score is already
  published, and repeats. Use when the user wants to optimize a PR/MR/CL against Greptile's code
  review standards without creating runaway review loops.
license: MIT
compatibility: Requires git, gh (GitHub CLI) or glab (GitLab CLI) authenticated, and Greptile installed on the repo. For Perforce, requires p4 CLI authenticated.
metadata:
  author: greptileai
  version: "1.5"
allowed-tools: Bash(gh:*) Bash(glab:*) Bash(git:*) Bash(p4:*)
---

# Greploop

Iteratively fix a PR/MR/CL until Greptile reaches the repository's configured merge threshold with zero unresolved actionable comments. Never run more than five Greptile review/fix iterations for one PR/MR/CL.

The default target is 5/5 confidence. Repository instructions or an explicit user instruction may lower the merge threshold, for example to 4/5. Do not keep triggering Greptile just to chase a perfect 5/5 once the local merge threshold is met.

If the latest published Greptile result for a PR/MR/CL is already **5/5**, stop the Greptile trigger loop. Do not request another Greptile review just because there are remaining actionable comments or because fixing them creates a new commit. Instead, fix the remaining comments, resolve the review threads, run the required local validation, push the fixes, and merge/close according to the repository workflow. A 5/5 score is sufficient to proceed after the remaining review feedback is addressed.

## Repository-specific configuration (canvasstudios-notebook)

- Merge threshold for this repository: **4/5** (per `AGENTS.md`). Do not chase a 5/5 once 4/5 is reached and all actionable comments are resolved or documented.
- Greptile/greploop may be triggered **at most once per PR head SHA**. Do not re-trigger for the same head.
- Detect whether Greptile accepted a manual `@greptile review` trigger by inspecting the trigger comment reactions. An `eyes` reaction from `greptile-apps[bot]` (or another Greptile bot) means Greptile is working; wait for the result and do not post another trigger for the same head SHA.
- After addressing review feedback and pushing a new commit, the new head SHA may be reviewed **once**.
- A `greploop` score of 4 out of 5 is sufficient for merge; a perfect 5 out of 5 is not required.
- Every Greptile/greploop comment must still be reviewed. Actionable comments must be fixed; non-actionable or false-positive comments must be documented and resolved.
- Only PRs with a `greploop` score of 4 or 5 and **zero unresolved review threads** may be merged into `main`; scores 0-3 block the merge until the issues are fixed and a new head SHA is reviewed.
- If `greploop` is unavailable or cannot produce a score for the current head SHA, treat the PR as blocked for merge into `main`.
- Before the first manual trigger, wait for the automatic Greptile review that runs after PR creation. Do not trigger `greploop` until the user confirms the first Greptile review is available, or explicitly asks for it.
- Do not start a sixth Greptile iteration. If the five-iteration cap is reached and the score did not improve further, stop triggering Greptile.

## Inputs

- **PR/MR/CL number** (optional): If not provided, detect the PR/MR for the current branch, or the default pending changelist for p4.
- **`--vcs <platform>`** (optional): Override platform detection (`github`, `gitlab`, or `perforce`). Use this for self-hosted GitLab instances whose hostname does not contain "gitlab".

## Instructions

### 0. Detect platform

First check for Perforce, then fall back to git remote detection:

```bash
# Check for Perforce environment
if p4 info >/dev/null 2>&1; then
  VCS="perforce"
else
  REMOTE_URL=$(git remote get-url origin)
  if echo "$REMOTE_URL" | grep -qi "gitlab"; then
    VCS="gitlab"
  else
    VCS="github"
  fi
fi
```

For self-hosted GitLab instances whose hostname doesn't contain "gitlab", the user can override by passing `--vcs gitlab` as an input. For Perforce, pass `--vcs perforce`.

### 1. Identify the PR/MR/CL

**GitHub:**
```bash
gh pr view --json number,headRefName -q '{number: .number, branch: .headRefName}'
```

**GitLab:**
```bash
glab mr view --output json | jq '{iid: .iid, branch: .source_branch}'
```

Switch to the PR/MR branch if not already on it.

**Perforce:**
```bash
# List pending changelists for current user/client
p4 changes -s pending -u $P4USER -c $P4CLIENT

# Describe a specific CL
p4 describe -s <CL_NUMBER>
```

Ensure the correct workspace (`p4 client`) is set before proceeding.

Key field differences:
- GitHub: `number`, `headRefName`, `headRefOid`
- GitLab: `iid`, `source_branch`, `sha`
- Perforce: changelist number, `P4CLIENT`, shelved files

### 2. Loop

Repeat the following cycle. **Max 5 Greptile review/fix iterations** to avoid runaway loops. Count each Greptile review result consumed for a head SHA as one iteration. Do not trigger more than one Greptile review for the same head SHA.

Track score progress across iterations. If the confidence score does not improve after the review cap is reached, stop the loop instead of continuing to chase the same feedback.

Before triggering a new Greptile review, check the latest published score. If it is **5/5**, skip triggering entirely and move directly to fixing/resolving any remaining comments, then merge/close after validation. Do not require a fresh score for commits that only address those remaining comments.

For this repository, also stop triggering once **4/5** is reached and all actionable comments are addressed; 4/5 is the merge threshold and a 5/5 is not required.

#### A. Trigger Greptile review

Push/shelve the latest changes (if any):

**GitHub/GitLab:**
```bash
git push
```

**Perforce:**
```bash
# Re-shelve to update the shelved files for review
p4 shelve -f -c <CL_NUMBER>
```

Wait for checks to start after push/shelve:

```bash
sleep 5
```

**GitHub** — check if Greptile is already running before posting a new trigger comment:

```bash
GREPTILE_STATE=$(gh pr checks <PR_NUMBER> --json name,state | jq -r '.[] | select(.name | test("greptile"; "i")) | .state')
```

If Greptile is **not** already running (`PENDING` or `IN_PROGRESS`), request a fresh review:

```bash
if [ "$GREPTILE_STATE" != "PENDING" ] && [ "$GREPTILE_STATE" != "IN_PROGRESS" ]; then
  gh pr comment <PR_NUMBER> --body "@greptile review"
fi
```

After posting `@greptile review`, inspect the trigger comment reactions before deciding Greptile is idle. Greptile may not create a check run, but `greptile-apps[bot]` adds an `eyes` reaction to the trigger comment when it has accepted the review and is working. Treat that `eyes` reaction as an in-progress signal and do **not** post another trigger for the same head SHA.

```bash
# List all review trigger comments and their aggregate reaction counts.
gh api --paginate "repos/{owner}/{repo}/issues/<PR_NUMBER>/comments?per_page=100" \
  --jq '.[] | select(.body == "@greptile review") | {id, created_at, user: .user.login, reactions: .reactions}'

# Check a specific trigger comment for the Greptile "eyes" reaction.
gh api "repos/{owner}/{repo}/issues/comments/<COMMENT_ID>/reactions" \
  --jq '[.[] | select(.content == "eyes" and (.user.login | test("greptile"; "i"))) | {user: .user.login, content, created_at}]'
```

Then poll for the Greptile check run to complete:

```bash
HEAD_SHA=$(gh pr view <PR_NUMBER> --json headRefOid -q .headRefOid)

while true; do
  GREPTILE_CHECK=$(gh api "repos/{owner}/{repo}/commits/$HEAD_SHA/check-runs" \
    --jq '.check_runs[] | select(.name | test("greptile"; "i"))' 2>/dev/null)
  
  if [ -z "$GREPTILE_CHECK" ]; then
    echo "Waiting for Greptile check to appear..."
    sleep 5
    continue
  fi
  
  STATUS=$(echo "$GREPTILE_CHECK" | jq -r '.status // "completed"')
  CONCLUSION=$(echo "$GREPTILE_CHECK" | jq -r '.conclusion // "pending"')
  
  if [ "$STATUS" = "completed" ]; then
    if [ "$CONCLUSION" = "success" ]; then
      echo "Greptile check passed!"
    else
      echo "Greptile check completed with: $CONCLUSION"
    fi
    break
  fi
  
  echo "Waiting for Greptile... (status: $STATUS)"
  sleep 10
done
```

**GitLab** — check if Greptile is already running before posting a trigger comment:

```bash
PIPELINES=$(glab api "projects/:fullpath/merge_requests/<MR_IID>/pipelines")
GREPTILE_RUNNING=$(echo "$PIPELINES" | jq '[.[] | select(.status == "running" or .status == "pending")] | length')
```

If no pipeline is running, post a trigger comment:

```bash
if [ "$GREPTILE_RUNNING" = "0" ]; then
  glab mr note <MR_IID> --message "@greptile review"
fi
```

**Perforce** — Perforce does not have native check runs. If Greptile is integrated via a webhook triggered on `p4 shelve`, wait for it to process. Check your Greptile installation's webhook endpoint or dashboard for the review status. Poll by re-fetching the Greptile review comment on the CL until a score appears.

Then poll for the Greptile pipeline job to complete (see [GitLab API reference](references/gitlab-api.md)):

```bash
HEAD_SHA=$(glab mr view <MR_IID> --output json | jq -r '.sha')

while true; do
  PIPELINES=$(glab api "projects/:fullpath/merge_requests/<MR_IID>/pipelines")
  # Find the most recent pipeline for this SHA
  PIPELINE_ID=$(echo "$PIPELINES" | jq -r --arg sha "$HEAD_SHA" \
    '[.[] | select(.sha == $sha)] | sort_by(.id) | last | .id // empty')

  if [ -z "$PIPELINE_ID" ]; then
    echo "Waiting for Greptile pipeline to appear..."
    sleep 5
    continue
  fi

  JOBS=$(glab api "projects/:fullpath/pipelines/$PIPELINE_ID/jobs")
  GREPTILE_JOB=$(echo "$JOBS" | jq '.[] | select(.name | test("greptile"; "i"))')

  if [ -z "$GREPTILE_JOB" ]; then
    echo "Waiting for Greptile job to appear..."
    sleep 5
    continue
  fi

  JOB_STATUS=$(echo "$GREPTILE_JOB" | jq -r '.status')

  if [ "$JOB_STATUS" = "success" ] || [ "$JOB_STATUS" = "failed" ] || [ "$JOB_STATUS" = "canceled" ]; then
    echo "Greptile job completed with: $JOB_STATUS"
    break
  fi

  echo "Waiting for Greptile... (status: $JOB_STATUS)"
  sleep 10
done
```

#### B. Fetch Greptile review results

Greptile may surface its score in several places — check **all** of the relevant sources:

**GitHub:**

**1. PR description (body):**
```bash
gh pr view <PR_NUMBER> --json body -q '.body'
```

**2. General PR comments (issue comments):**
```bash
gh api --paginate "repos/{owner}/{repo}/issues/<PR_NUMBER>/comments?per_page=100"
```

Filter for Greptile-authored comments and use the body from the most recently updated comment (`updated_at`), not the most recently created comment. Greptile may edit the same general PR comment on each review cycle; parse the current body, including the "Prompt to fix all with AI" section, before deciding there are no remaining issues.

**3. PR reviews:**
```bash
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/reviews
```

Look for the most recent entry from `greptile-apps[bot]` or `greptile-apps-staging[bot]`.

**GitLab:**

**1. MR description (body):**
```bash
glab mr view <MR_IID> --output json | jq -r '.description'
```

**2. MR notes (comments):**
```bash
glab api "projects/:fullpath/merge_requests/<MR_IID>/notes"
```

Filter for notes from the Greptile bot user (check the `author.username` field — the exact username may vary per installation; verify on first run).

**Perforce:**

**1. CL description:**
```bash
p4 describe -s <CL_NUMBER>
```

Check the description field for a Greptile-appended score block.

**2. CL comments / review notes:**
If your installation uses a review tool such as Helix Swarm, fetch comments via its API.

Example (Swarm API):
GET /api/v11/comments?topic=reviews/<REVIEW_ID>

Response fields of interest typically include:
- user (author username)
- body (comment text)
- flags/state indicating whether the comment is resolved

Filter to comments authored by the Greptile bot:
- Prefer exact username match if known
- Otherwise, use a heuristic where the author name contains "greptile" (case-insensitive)

For all platforms, parse the text for:
- **Confidence score**: a pattern like `3/5` or `5/5` (or `Confidence: 3/5`).
- **Comment count**: Number of inline review comments noted in the summary.

Use whichever source has the **most recently updated** score. For GitHub, prefer `updated_at` from issue comments when comparing an edited Greptile summary against older review entries.

Also fetch all unresolved inline comments:

**GitHub:**
```bash
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments
```

Also carry forward actionable items from the latest Greptile general PR comment, especially the "Prompt to fix all with AI" section, even if the inline comment endpoint returns zero unresolved comments.

**GitLab:**
```bash
glab api "projects/:fullpath/merge_requests/<MR_IID>/discussions"
```

Filter to `DiffNote` type discussions (`notes[0].type == "DiffNote"`) from Greptile that are on the latest commit and not yet resolved (`"resolved": false`).

**Perforce:**
If using Swarm:

# Fetch inline diff comments for the review associated with the CL
GET /api/v11/comments?topic=reviews/<REVIEW_ID>

Filter to comments from the Greptile bot user that have not been marked as resolved/addressed.

#### C. Check exit conditions

Stop the loop if **any** of these are true:

- Confidence score meets the repository/user merge threshold (this repo: **4/5**; default elsewhere: **5/5**) AND there are **zero unresolved actionable comments**
- Confidence score is **5/5**, even if actionable comments remain; fix and resolve those comments without triggering Greptile again, then merge/close after local validation
- Max five Greptile iterations reached
- The score no longer improves and the latest result already meets the repository/user merge threshold

When the loop stops because the merge threshold is met, merge/close the PR/MR according to the repository workflow after documenting the final score. When the five-iteration cap is reached and the score did not improve further, stop triggering Greptile. If the final score still meets the repository/user merge threshold and all actionable comments are fixed or resolved, merge/close the PR/MR. If the user has explicitly instructed that capped PRs should be merged even below the normal threshold, document the residual score and unresolved non-actionable items before merging; otherwise treat the PR/MR as blocked and report the remaining issues.

For this repository specifically: scores 0-3 block the merge until issues are fixed and a new head SHA is reviewed; scores 4-5 with zero unresolved review threads allow merge into `main`.

#### D. Fix actionable comments

For each unresolved Greptile comment:

1. Read the file and understand the comment in context.
2. Determine if it's actionable (code change needed) or informational.
3. If actionable, make the fix.
4. If informational or a false positive, note it but still resolve the thread. Document false positives in the PR so reviewers can see the rationale.

#### E. Resolve threads

**GitHub** — fetch unresolved review threads and resolve all that have been addressed (see [GraphQL reference](references/graphql-queries.md)):

```bash
gh api graphql -f query='
query($cursor: String) {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes { body path author { login } }
          }
        }
      }
    }
  }
}'
```

Resolve addressed threads:

```bash
gh api graphql -f query='
mutation {
  t1: resolveReviewThread(input: {threadId: "ID1"}) { thread { isResolved } }
  t2: resolveReviewThread(input: {threadId: "ID2"}) { thread { isResolved } }
}'
```

**GitLab** — fetch unresolved discussions and resolve each one (see [GitLab API reference](references/gitlab-api.md)):

```bash
glab api "projects/:fullpath/merge_requests/<MR_IID>/discussions?per_page=100"
```

Filter for `"resolved": false` discussions. Then resolve each by its `id`:

```bash
glab api --method PUT \
  "projects/:fullpath/merge_requests/<MR_IID>/discussions/<DISCUSSION_ID>" \
  --field resolved=true
```

Repeat for each unresolved discussion ID. (GitLab has no batch resolution — loop through each one.)

#### F. Commit and push / re-shelve

**GitHub/GitLab:**
```bash
git add -A
git commit -m "address greptile review feedback (greploop iteration N)"
git push
```

If the latest published Greptile score before this fix met or exceeded the merge threshold (4/5 for this repo, 5/5 elsewhere), do not return to step A after pushing. Resolve addressed threads, confirm local validation and repository checks required by the project, then merge/close according to the repository workflow.

**Perforce:**
```bash
# Stage changes back into the CL and re-shelve for the next review round
p4 shelve -f -c <CL_NUMBER>
```

Wait for checks to start after push/shelve:

```bash
sleep 5
```

Then go back to step **A**.

### 3. Report

After exiting the loop, summarize:

| Field              | Value      |
| ------------------ | ---------- |
| Platform           | GitHub / GitLab / Perforce |
| Iterations         | N          |
| Final confidence   | X/5        |
| Comments resolved  | N          |
| Remaining comments | N (if any) |

If the loop exited due to max iterations, list any remaining unresolved comments, the best score reached, and whether the repository/user merge threshold allows merging. Do not start a sixth Greptile iteration.

For this repository, also document the final `greploop` score in the PR description before merging, per `AGENTS.md`.

## Output format

```
Greploop complete.
  Platform:      GitHub
  Iterations:    2
  Confidence:    4/5
  Resolved:      7 comments
  Remaining:     0
```

If not fully resolved:

```
Greploop stopped after 5 iterations.
  Platform:      GitLab
  Confidence:    3/5
  Resolved:      12 comments
  Remaining:     2

Remaining issues:
  - src/auth.ts:45 — "Consider rate limiting this endpoint"
  - src/db.ts:112 — "Missing index on user_id column"
```

**Perforce example:**

```
Greploop complete.
  Platform:      Perforce
  Changelist:    12345
  Iterations:    3
  Confidence:    4/5
  Resolved:      9 comments
  Remaining:     0
```