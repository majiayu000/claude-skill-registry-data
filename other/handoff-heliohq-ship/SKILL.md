---
name: handoff
version: 0.5.0
description: >
  Ship completed work: verify locally, commit related changes, push, create or
  update the PR, watch CI/reviews, and fix until merge-ready or escalated. Use
  for "ship it", "create PR", "handoff", or finished code needing delivery.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - Monitor
  - TaskStop
  - mcp__codex__codex
  - mcp__codex__codex-reply
---

# Ship: Handoff

Do not stop when the PR is created.
Do not stop while any GitHub check is pending.
If any GitHub check fails, fix the problem, push again, and wait again.
If the PR is not merge-ready, sync with base or resolve conflicts inside
the same fix loop.

This is a goal-directed loop, not a counted one. Keep looping while each
round makes progress toward the completion conditions; escalate on
evidence, never on a round counter — the specific evidence classes are
in [Loop Governance](#loop-governance). Done means every condition in
[Completion](#completion) is satisfied.

## Process Flow

Phase index — the phases below own the detail:

1. Pre-flight (resolve branch, base, and scope)
2. Verify locally
3. Update changelog / directly affected docs
4. Push and create/update the PR
5. Wait for GitHub checks
6. Fix loop — governed by the round ledger, not a counter

## Red Flag

**Never:**
- **Stop when the PR is created** — #1 failure mode
- Push code changes without re-running relevant local verification
- Force push without `--force-with-lease`
- Rewrite an already-pushed PR branch when there are human review,
  approval, or shared-branch signals
- Treat `pending` checks as "good enough"
- Treat green checks as sufficient when `mergeStateStatus` is still blocked
- Create the PR before local verification runs
- Use `git add -A` when unrelated local changes are present
- Forget to stage and commit changelog or doc edits before the first push
- Mark a thread or comment as resolved before the fix is actually pushed
- Resolve comments that still need product, security, or architecture judgment
- Silently ignore a comment — a decline is a visible reply with a reason
- Apply "further fixes add no value" to CI or merge-readiness — that
  judgment exists only for the comment decline classes
- Fix failures without reading the actual check logs or review comments
- Sync with base preemptively — only when drift, conflicts, or repo policy require it
- Re-attempt a fix for a failure signature that already survived a fix
  aimed at it — the second identical outcome is evidence the approach is
  wrong; escalate with the ledger instead of iterating on hope
- Count rounds as a stopping condition — progress, judgment, and external
  blockers are the only reasons to stop looping
- Leave doc debt implicit — carry it into the PR

---

## Loop Governance

Modern harnesses run goal-directed loops natively — a fixed retry cap
abandons hard-but-progressing PRs while adding no safety that progress
detection doesn't provide better. The loop is governed by three things:

**1. Progress detection (the round ledger).** Every fix round appends one
block to `<task_dir>/handoff.md` (or tracks inline when no task dir):

```
Round <i>: trigger=<check name + error class, or "conflict"/"review">
  action=<what was changed, one line>
  result=<next terminal state: new signature | same signature | green>
```

Before starting a round, compare the current failure to the ledger:

- **New failure signature** (different check, or same check failing
  differently) → progress; loop.
- **Same signature after a fix aimed at it** → the approach is wrong.
  Escalate with the ledger as evidence — do not iterate on hope.
- The ledger survives context compaction; after a compaction, trust it
  over recollection.

**2. Judgment boundaries.** Product/security/architecture review
comments, conflicts you cannot resolve confidently, and rebase-policy
dead ends escalate immediately regardless of progress. A fix that would
change the shipped behavior (not just repair its delivery) is scope
drift — escalate; the fix loop repairs delivery, it does not redesign.

**3. The harness's own goal net.** Under `/ship:auto`, the stop gate
already blocks session exit until the PR is merge-ready. In a standalone
run on a harness with a native goal condition (e.g. Claude Code's
`/goal`), suggest the user arm one at the start — `PR checks green and
merge-ready, or stop after 25 turns` — as the outer bound; the harness's
turn bound replaces any hand-rolled cap.

## Progress Tracking

Track your progress with the harness's task/todo list. Create the items
at the start based on what the repo actually needs.
Not every repo has a CHANGELOG, CI, or docs to update — only include
items for work that will actually happen.

**Principle**: one item per phase the user would wait on. Fix rounds
are dynamic — add them only when a check fails.

---

## Phase 1: Pre-flight

Resolve only the context needed to ship the PR:

1. Determine the current branch.
   - If HEAD is detached, create a feature branch before continuing.
2. Determine the base branch:
   - use the existing PR base if a PR already exists
   - otherwise use the repo default branch
3. If the current branch is the base branch, create a feature branch before continuing.
4. Inspect the current scope with `git status --short`, `git diff <base>...HEAD --stat`, `git diff --cached --stat`, and `git diff --stat`.
5. Decide which local changes belong to this handoff.
6. Do not use `git add -A` unless every dirty file belongs to this handoff.
7. If unrelated local changes cannot be separated safely, stop and escalate instead of guessing.
8. If the caller already provides `task_dir`, use it. Otherwise do not guess one here; resolve it only if a later phase needs to write artifacts.

Output a short start summary with the branch, base branch, and scope being shipped.

## Phase 2: Verify Before PR

Before the first push in handoff, run the most relevant local verification
available for this repo.

- Prefer the same commands the repo or CI already uses.
- Run only the checks that are relevant to the changed area: tests, lint,
  typecheck, build, or targeted smoke checks as applicable.
- If code changes during handoff, run the relevant verification again before
  the next push.
- If a task directory already exists, do not invent extra artifacts just for handoff.
- If verification fails, fix the issue before pushing.

Output a short summary of what was run and whether it passed.

## Phase 3: Update CHANGELOG and Docs

### Step A: CHANGELOG (auto-generate)

`[ -f CHANGELOG.md ] || echo 'NO_CHANGELOG'`
- No CHANGELOG.md → skip silently.

If CHANGELOG.md exists:
1. Read header to learn the format
2. Generate entry from: `git log <base>..HEAD --oneline`
3. Categorize: Added / Changed / Fixed / Removed
4. Insert after header, dated today
5. Commit: `git add CHANGELOG.md && git commit -m "docs: update CHANGELOG"`

After changelog handling, check whether the shipped changes also changed any
user-facing or repo-facing documentation truths before the first push.

Use `references/documentation.md` for the documentation decision tree and
ownership rules.

- Only inspect docs that directly describe the changed commands, config,
  file paths, workflow, or behavior.
- Do not scan every markdown file in the repo.
- Route each changed truth to the narrowest correct document instead of
  defaulting to top-level docs.
- If a doc is mechanically stale, fix it in the same handoff loop.
- If the doc issue is semantic and you are not confident about the right
  wording, carry that note into the PR instead of inventing an explanation.
- Before moving on, explicitly record one of:
  - docs updated
  - docs checked, no update needed
  - doc debt to note in the PR

## Phase 4: Push and Create PR

When opening or updating the PR, keep the title and body concise.

Include only:
- what changed
- what local verification ran
- any known follow-up, risk, or skipped check

Do not invent a long template if the change is simple.

Push and create:
1. Review the final diff, then stage all related changes that should ship now, including any changelog or doc edits made in this handoff.
2. Commit the staged changes if anything new was staged in this phase.
3. `git push -u origin HEAD`
4. Create the PR if it does not exist.
5. If the PR already exists, update the body or add a short comment with the latest verification summary.
6. If `task_dir` exists, write or update `<task_dir>/handoff.md` with:
   PR URL, branch, base, verification commands/results, docs outcome,
   current check summary, current `mergeStateStatus`, and the round
   ledger (Loop Governance format — one block per fix round). This file
   is the handoff evidence consumed by the stop gate, and the ledger is
   what makes progress detection survive context compaction.

Output: `[Handoff] PR created: <url>`

## Phase 5: Wait for GitHub Checks

Inspect `.github/workflows`, branch protection signals, and the current PR
checks once so you understand what this repo expects to run. A repo can
have required checks from GitHub Apps even when it has no local workflow
files, so never skip this phase based on `.github/workflows` alone.

**Let the harness wait — never agent-side sleep polling.**
`gh pr checks --watch` blocks locally and polls GitHub itself every ~10s;
your job is to park on it with whatever waiting primitive your harness
has, so idle waiting costs nothing. The watch command in every case
below is `timeout 3600 gh pr checks --watch`:

- **Monitor available** (Claude Code): arm one watch per wait cycle. A
  Monitor is single-use — it wakes you when output arrives and is
  re-armed fresh after each fix push. Use an explicit timeout, NOT
  `persistent: true` (persistent overrides `timeout_ms` entirely and
  needs a manual TaskStop; it is meant for dev servers, not bounded
  waits):

      Monitor(
        command: 'timeout 3600 gh pr checks --watch; echo "TERMINAL exit=$?"',
        description: "PR <number> checks settling",
        timeout_ms: 3600000
      )

  Before arming, check whether a Monitor for this PR is already running —
  on resume the prior watch may still be alive. If so, wait for its
  event; do not arm a duplicate.
- **Background command support, no Monitor**: run the watch command as a
  background command — the completion notification wakes you with the
  exit code.
- **Neither** (e.g. Codex today): run the watch command as a plain
  blocking command; the harness waits on the process. If the harness
  offers a scheduled-wakeup loop instead, poll `gh pr checks` on a
  few-minute interval.

When the watch terminates (`TERMINAL exit=<code>` event, background
completion, or command return), pull the authoritative state once:

```bash
# Full snapshot for interpretation
gh pr view --json state,statusCheckRollup,reviews,reviewDecision,mergeable,mergeStateStatus,comments

# Machine-readable check summary
gh pr checks --json name,state,bucket,link,workflow

# Read failing check logs if any. Prefer the failed run URL/check URL from
# the snapshot; use gh run view only after identifying the run id.
gh run view <run-id> --log-failed
```

Also inspect unresolved review threads when review comments may be
actionable. `gh pr view --json comments,reviews` is not enough because it
does not reliably expose thread resolution state.

```bash
OWNER=$(gh repo view --json owner --jq '.owner.login')
REPO=$(gh repo view --json name --jq '.name')
PR_NUMBER=$(gh pr view --json number --jq '.number')
gh api graphql -f owner="$OWNER" -f repo="$REPO" -F number="$PR_NUMBER" -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 20) {
            nodes {
              id
              author { login }
              body
              path
              line
              outdated
              url
            }
          }
        }
      }
    }
  }
}'
```

Interpret the snapshot:

- All relevant checks `SUCCESS`, `NEUTRAL`, or intentionally ignored
  optional `SKIPPED`/`CANCELLED` → check gate green
- Any relevant `FAILURE`, `ERROR`, `ACTION_REQUIRED`, or failed check
  bucket → Phase 6 fix loop
- Any relevant pending, queued, in-progress, expected, or waiting check
  → keep waiting
- `mergeStateStatus` is `DIRTY`, `BEHIND`, `BLOCKED`, `DRAFT`, or
  `UNKNOWN` after one re-query → Phase 6 fix loop or escalation
- `mergeable` is `CONFLICTING` → Phase 6 fix loop
- Any actionable unresolved review thread, review comment, or bot/workflow
  comment → Phase 6 fix loop
- `CANCELLED` checks → informational only when they are optional and do
  not block normal CI/CD
- Exit code non-zero but no concrete failure found in snapshot → re-query
  once, then escalate as ambiguous CI state

**Wait timeout.** If the watch hits its 1h bound with checks still
pending, re-query once: checks that moved → re-arm the watch and keep
waiting (slow CI is progress, not failure); checks frozen with no
movement since the previous query → escalate as an external GitHub wait,
not a code-fix failure. Record which checks were still pending so the
user can investigate.

**Re-entering the fix loop.** When Phase 6 finishes pushing a fix, arm a
fresh watch (the previous one terminated on its event) and loop back to
the event-wait above.

## Phase 6: Fix Loop

If CI failures, review comments, or merge conflicts exist, fix them.
The loop is governed by progress, not a counter — see [Loop Governance](#loop-governance);
step 0 below carries the in-loop ledger check.

### Comment Triage

Review comments are not all action-required. Triage each one before
spending a fix round on it — "addressed" means fixed OR declined with a
visible reason, never silently ignored:

| Comment class | Action |
|---|---|
| Correctness, security, or spec violation (any author) | Fix it — this is what fix rounds are for |
| Human reviewer explicitly requests changes | Fix it, or escalate to the user — never self-judge a human's request away |
| Style, polish, or subjective preference (especially bot/AI reviews) | Fix only if trivial and local; otherwise reply with a one-line reasoned decline and move on |
| Out-of-scope suggestion (new feature, broader refactor) | Decline with a reply; note it as a follow-up in the PR body |

**Diminishing returns is a stop signal for comments — never for CI or
merge-readiness.** When every remaining comment falls in the decline
classes, the comment gate is satisfied: reply, minimize what's obsolete,
and stop polishing. Checks green and merge-ready stay objective gates —
"I think further fixes add no value" is never grounds to stop while a
check is red or the PR is not merge-ready.

In each fix round:

0. Compare the current failure signature against the round ledger in
   `<task_dir>/handoff.md`. Same signature as the previous round's
   target → stop and escalate with the ledger. New signature → append
   the new round entry and continue.
1. Re-read the current PR status on GitHub, including checks,
   `mergeStateStatus`, and unresolved review threads.
2. If checks failed, inspect the failing check logs and fix the smallest
   real cause.
3. Triage review comments per Comment Triage above: fix the
   correctness/security/spec class, decline the polish and out-of-scope
   classes with a reasoned reply.
4. If a comment requires product, security, or architecture judgment,
   escalate instead of guessing.
5. If `mergeStateStatus` reports conflicts, base drift, branch protection
   blockage, or a repo policy requires an update from base, sync with base
   and resolve it carefully.
   Use this strategy:
   - Always start with `git fetch origin <base-branch>`.
   - Prefer `git rebase origin/<base-branch>` when it can preserve a
     clean linear history without disrupting collaborators. This is
     always appropriate before the branch is pushed.
   - For an already-pushed PR branch, choose rebase only when all of
     these safety gates pass: the branch is agent-owned, there are no
     human approvals or unresolved human review threads, no other author
     has pushed commits to the branch, and the repo appears to expect
     linear history. Push the result with `git push --force-with-lease`,
     never plain `--force`.
   - If any safety gate fails, prefer `git merge --no-ff
     origin/<base-branch>` (or the repo's equivalent update-branch
     operation) so the fix can be pushed without rewriting review
     history.
   - If repo policy requires linear history but the rebase safety gates
     do not pass, escalate for user approval.

   For an already-pushed PR branch, prove the safety gates before
   rebasing. Default to **not safe** if any command fails, returns
   ambiguous output, or shows collaboration:

   ```bash
   BRANCH=$(git branch --show-current)
   BASE=$(gh pr view "$BRANCH" --json baseRefName --jq '.baseRefName')
   PR_AUTHOR=$(gh pr view "$BRANCH" --json author --jq '.author.login')
   ME=$(gh api user --jq '.login')
   export PR_AUTHOR ME

   # 1. Agent-owned branch naming convention.
   case "$BRANCH" in
     ship/*|codex/*) echo "agent-owned-name" ;;
     *) echo "NOT_SAFE: branch name is not agent-owned"; exit 1 ;;
   esac

   # 2. No human approvals, change requests, comments, or review threads.
   # gh --jq exits 0 even when the expression prints "false" — capture the
   # boolean and test the string, or the gate can never fire.
   NO_HUMAN_SIGNALS=$(gh pr view "$BRANCH" --json reviews,comments --jq '
     [
       .reviews[]?.author.login,
       .comments[]?.author.login
     ]
     | map(select(. != "github-actions[bot]" and . != "dependabot[bot]"))
     | map(select(. != env.PR_AUTHOR and . != env.ME))
     | length == 0
   ')
   [ "$NO_HUMAN_SIGNALS" = "true" ] || { echo "NOT_SAFE: human review/comment signal"; exit 1; }

   # 3. No unresolved review threads from humans.
   OWNER=$(gh repo view --json owner --jq '.owner.login')
   REPO=$(gh repo view --json name --jq '.name')
   PR_NUMBER=$(gh pr view "$BRANCH" --json number --jq '.number')
   NO_HUMAN_THREADS=$(gh api graphql -f owner="$OWNER" -f repo="$REPO" -F number="$PR_NUMBER" -f query='
   query($owner: String!, $repo: String!, $number: Int!) {
     repository(owner: $owner, name: $repo) {
       pullRequest(number: $number) {
         reviewThreads(first: 100) {
           nodes {
             isResolved
             comments(first: 20) {
               nodes { author { login } }
             }
           }
         }
       }
     }
   }' --jq '
     [
       .data.repository.pullRequest.reviewThreads.nodes[]?
       | select(.isResolved == false)
       | .comments.nodes[]?.author.login
     ]
     | map(select(. != "github-actions[bot]" and . != "dependabot[bot]"))
     | map(select(. != env.PR_AUTHOR and . != env.ME))
     | length == 0
   ')
   [ "$NO_HUMAN_THREADS" = "true" ] || { echo "NOT_SAFE: unresolved human review thread"; exit 1; }

   # 4. No other commit authors on this PR branch.
   git fetch origin "$BASE"
   MY_EMAIL=$(git config user.email)
   UNEXPECTED_AUTHORS=$(git log --format='%ae' "origin/$BASE..HEAD" | \
     sort -u | grep -vxF "$MY_EMAIL" || true)
   [ -z "$UNEXPECTED_AUTHORS" ] || {
     echo "NOT_SAFE: unexpected commit authors: $UNEXPECTED_AUTHORS"
     exit 1
   }

   # 5. Repo appears to prefer/require linear history.
   OWNER=$(gh repo view --json owner --jq '.owner.login')
   REPO=$(gh repo view --json name --jq '.name')
   LINEAR_HISTORY=$(gh api "repos/$OWNER/$REPO" --jq '
     (.allow_rebase_merge == true or .allow_squash_merge == true)
     and (.allow_merge_commit == false)
   ')
   [ "$LINEAR_HISTORY" = "true" ] || { echo "NOT_SAFE: repo does not clearly require linear history"; exit 1; }
   ```

   Only when all gates are proven safe may the agent run:

   ```bash
   git rebase "origin/$BASE"
   <relevant local verification command>
   git push --force-with-lease
   ```
6. Do not resolve conflicts mechanically with `--ours` or `--theirs` unless
   one side is clearly disposable.
7. Read both sides of the conflict and preserve the behavior this PR is
   trying to ship. If both sides contain valid changes, merge them.
8. If you cannot resolve the conflict confidently, escalate instead of guessing.
9. After any code change, run the relevant local verification again.
10. Commit the fix and push it.
11. Update `<task_dir>/handoff.md` if `task_dir` exists.
12. If the push fully addresses GitHub feedback, mark the addressed feedback as resolved:
    - for review threads, resolve the thread
    - for obsolete bot or workflow comments, hide/minimize the comment with
      classifier `RESOLVED`
13. Never resolve, hide, or minimize feedback that is only partially addressed
    or still needs user judgment.
14. Go back to Phase 5.

Use GitHub GraphQL when needed:

```bash
# Resolve a PR review thread
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { id isResolved }
    }
  }' -F threadId="<thread-id>"

# Hide/minimize an obsolete bot or workflow comment as resolved
gh api graphql -f query='
  mutation($subjectId: ID!) {
    minimizeComment(input: {subjectId: $subjectId, classifier: RESOLVED}) {
      minimizedComment { isMinimized }
    }
  }' -F subjectId="<comment-node-id>"
```

Output: `[Handoff] Fix round <i> — target: <failure signature> — <what was fixed>. Tests pass. Re-checking CI...`

---

## Execution Handoff

Output the report card — read the format from `../shared/report-card.md`
(resolved against this skill's base directory, not the working directory):

```
## [Handoff] Report Card

| Field | Value |
|-------|-------|
| Status | <DONE / BLOCKED> |
| Summary | PR #<N> — checks <green / pending / failed>, merge <ready / blocked> |

### Metrics
| Metric | Value |
|--------|-------|
| PR URL | <url> |
| Check status | <green / N passing, M failed> |
| Merge state | <mergeStateStatus> |
| Fix rounds | <N> (each targeting a new failure signature) |
| Docs outcome | <updated / checked-no-update / debt-noted> |

### Artifacts
| File | Purpose |
|------|---------|
| PR on GitHub | Shipped code |
| .ship/tasks/<task_id>/handoff.md | PR URL, checks, merge state, verification, docs outcome |
| CHANGELOG.md | Updated changelog (if repo has one) |
```


---

## Example Workflow

Condensed to show the loop shape. The full log would include the same
verify/commit/push pattern after every fix round.

```
[Handoff] Start — branch feat/auth, base main, 4 files + 2 doc edits
[Handoff] Verify → npm test, npm run lint: PASS
[Handoff] CHANGELOG entry added, README updated
[Handoff] Push, PR created: https://github.com/org/repo/pull/123

[Handoff] Wait → ci/test FAILURE
[Handoff] Fix round 1 — target: ci/test nil deref — added nil guard, re-verify PASS, push
[Handoff] Wait → AI review: requested error-path coverage
[Handoff] Fix round 2 — target: review error-path coverage — added test, re-verify PASS, push
                 resolved review thread, minimized obsolete bot comment
                 (each round hit a NEW signature — progress; ledger updated)

[Handoff] Wait → all checks green
[Handoff] Merge state → CLEAN
[Handoff] DONE — PR #123 green and merge-ready
```

## Completion

Done when:

- the PR exists
- relevant GitHub checks are green
- no relevant GitHub checks are pending
- `mergeStateStatus` is merge-ready (`CLEAN`, `HAS_HOOKS`, or `UNSTABLE`
  only when all failing checks are irrelevant/non-blocking)
- `mergeable` is not `CONFLICTING`, and there are no unresolved merge
  conflicts in the local worktree
- the branch is not behind base in a way GitHub/repo policy requires
  updating before merge
- every review thread and bot/workflow comment is addressed: fixed, or
  declined with a reasoned reply per Comment Triage (a human "changes
  requested" review is never satisfied by an agent-side decline)

Escalate when:

- a failure signature survives a fix aimed at it (no-progress evidence —
  bring the round ledger)
- a remaining issue requires user judgment (product, security,
  architecture, or a fix that would change shipped behavior rather than
  repair its delivery)
- GitHub checks stay frozen past the wait timeout with no movement
  between re-queries (external blocker)
- GitHub state remains ambiguous after one re-query
- merge conflicts or required branch updates cannot be resolved confidently
