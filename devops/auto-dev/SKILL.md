---
name: auto-dev
description: Autonomous PR development methodology. Use ONLY when the user explicitly invokes /auto-dev or explicitly asks to load this skill — never auto-activate. Reviews every PR twice, monitors all CI pipelines in background, replies to and resolves every review comment from any reviewer (automated systems like CodeRabbit and human reviewers alike), merges PRs (apps or infra) when green, then monitors post-merge and deployment pipelines, iterating on failures.
---

# auto-dev

You are running the **auto-dev** workflow: an autonomous development methodology applied to every PR you work on in this session.

## Invocation Guard (read first)

- **Explicit-invoke only.** Do NOT load or apply this skill on your own initiative. It activates only when the user runs `/auto-dev` or explicitly says to use auto-dev. If you find yourself reaching for this skill without an explicit user request, STOP.
- This is intentionally an autonomous, high-authority skill (it self-merges and self-deploys). It must never run as a silent default.

## Operating Philosophy — No Waits, No Blocks, No Stops

auto-dev is built for **long-running, self-feeding sessions**. After the single up-front consent, it runs fully automated:

- **Never block on a human.** Apart from the one-time consent, do not pause to ask the user for permission, scope, or guidance. Pick the sensible default and proceed.
- **Never block the main thread.** All pipeline/CI/deploy monitoring runs in background agents (Phase 3). You stay free to keep working and answer queries while they run.
- **Never stop the session on a blocker.** If something can't be auto-resolved (unfixable failure, hit iteration cap, ambiguous scope), **record it, report it inline, and move on** to the next PR / queued work — do not halt and wait. The loop keeps feeding itself.
- The only safety brakes are *local* (per-PR/per-deployment): they stop a futile sub-loop, not the session.

## Consent Model

This skill requires **one-time consent per session**. When you first load this skill, ask the user:

> "auto-dev is active. This means I will: review every PR twice, monitor all CI pipelines in background agents, reply to and resolve every review comment from any reviewer — CodeRabbit, other review bots, and human reviewers — (fixing the ones that need it), and monitor post-merge + deployment pipelines. I'll merge PRs myself (apps or infra) when all gates are green. Confirm to activate for this session?"

Once confirmed, **do not ask again** for the remainder of the session — apply auto-dev to every relevant PR action automatically, including merges and deployments. This is the single allowed interruption; after it, the session is fully automated.

**Compaction note:** if context compaction later drops the consent exchange, treat the skill being active as the standing consent — do NOT re-ask and do NOT block the loop. The user opted into autonomous merging/deploying for the whole session when they invoked auto-dev.

---

## Core Principles

- **Two independent review passes before any merge** — both are *your own* passes. Pass 1: your first review, incorporating CI + reviewer signals (CodeRabbit, other bots, human reviewers), where you fix everything actionable. Pass 2: your second, fresh review of the settled diff at the merge gate.
- **All CI must be green** — zero tolerance for red pipelines before merge.
- **Every review comment is handled, from any reviewer** — automated systems (CodeRabbit, other review bots) and human reviewers alike. Triage all of them, fix the ones that need it, then **reply to and resolve every thread** (fixed or not). The mechanism is identical for all reviewers — GitHub review threads are reviewer-agnostic. You do NOT need a human reviewer's formal approval to merge — only that their comments are verified and the relevant ones fixed.
- **You merge yourself** — apps or infra. Do not instruct the user to merge; do it via `gh pr merge`.
- **Post-merge pipelines are your responsibility** — monitor them; fix failures that originate from your changes.
- **Background pipeline monitors** — never block the main thread; always monitor in background agents so you can answer queries and work in parallel.

---

## Workflow

### Phase 1 — Pre-Review Setup

When a PR is ready for review (created or handed to you). Run `gh` from inside the repo, or pass `--repo <owner>/<repo>` explicitly on every command:

1. Fetch PR details:
   ```bash
   gh pr view <PR> --repo <owner>/<repo> --json number,title,url,headRefName,baseRefName,body,state,reviews,statusCheckRollup
   ```

2. Read the full diff:
   ```bash
   gh pr diff <PR> --repo <owner>/<repo>
   ```

3. Fetch all review threads with their node IDs (needed for replying + resolving later). This GitHub API is reviewer-agnostic — it returns threads from every reviewer: automated bots (CodeRabbit appears as `coderabbitai[bot]`, other bots have their own `[bot]` logins) and human reviewers (their GitHub handle). The `author.login` field on each comment tells you who left it, so you can tailor the reply, but you handle them all:
   ```bash
   gh api graphql \
     -f query='query($owner:String!, $repo:String!, $pr:Int!, $first:Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $pr) {
           reviewThreads(first: $first) {
             nodes {
               id
               isResolved
               isOutdated
               comments(first: 100) {
                 nodes { databaseId author { login } body }
               }
             }
           }
         }
       }
     }' \
     -f owner='<owner>' -f repo='<repo>' -F pr=<PR> -F first=100
   ```
   Record every unresolved thread's `id` (`PRRT_...`) along with its author login(s) — you will reply to and resolve every one in Phase 2, regardless of whether the reviewer is a bot or a human. Skip threads already `isResolved: true`.

4. Launch a background CI monitor (see Phase 3) immediately — don't wait for CI before starting your review.

---

### Phase 2 — First Review (your first pass)

This is **your own** first review pass. CI and reviewer comments (CodeRabbit, other bots, human reviewers) are inputs to it, not a substitute for it.

1. Triage every review comment, from any reviewer (bot or human):
   - `fix-required` — correctness, security, logic error, broken test, type error
   - `fix-recommended` — style, naming, clarity (fix unless trivial churn)
   - `nitpick` — optional, low-value; note but don't block
   - `stale` — comment on code already changed; no fix needed
   - Treat a human reviewer's `fix-required`/`fix-recommended` with at least the same weight as a bot's — and prefer fixing over dismissing when a human raised it.

2. Read the diff yourself, independent of the reviewers. Look for:
   - Logic errors not caught by any reviewer
   - Missing tests for new behaviour
   - Undocumented breaking changes
   - Obvious performance issues

3. Compile a **first-pass action list** — all `fix-required` and `fix-recommended` items (reviewer-found, bot or human, + your own findings).

4. If the action list is non-empty:
   - Check out the branch, apply all fixes
   - Commit clearly (e.g. `fix: address first-round review comments`)
   - Push (re-triggers CI)
   - Launch a NEW background CI monitor for the new commit
   - **Do not proceed to the Phase 4 merge gate until the new CI run completes**

5. **Reply to and resolve EVERY review thread** — from any reviewer (bot or human), regardless of whether it produced a fix. For each thread `id` recorded in Phase 1:

   Reply (note the input field is `pullRequestReviewThreadId`). Write a real, courteous reply — especially for human reviewers, the reply should explain what you did or why no change was needed, not just "done":
   ```bash
   gh api graphql \
     -f query='mutation($threadId: ID!, $body: String!) {
       addPullRequestReviewThreadReply(input: { pullRequestReviewThreadId: $threadId, body: $body }) {
         comment { id }
       }
     }' \
     -f threadId='PRRT_...' \
     -f body='Fixed in <commit-sha>.'        # or: 'Acknowledged — no change needed: <reason>.'
   ```

   Resolve (note this mutation's input field is `threadId`, NOT `pullRequestReviewThreadId`):
   ```bash
   gh api graphql \
     -f query='mutation($threadId: ID!) {
       resolveReviewThread(input: { threadId: $threadId }) {
         thread { isResolved }
       }
     }' \
     -f threadId='PRRT_...'
   ```

   The merge gate requires **every** review thread (any reviewer) replied-to and `isResolved: true`.

---

### Phase 3 — Pipeline Monitoring (Background, Always)

**Rule: every CI run you care about gets its own background monitor. Never block on pipelines yourself.**

The monitor must NOT poll in an LLM loop — it runs a single **blocking shell command** (`gh pr checks --watch`), which waits in the shell with zero token cost and exits non-zero on failure. Use the cheapest tier (`quick`):

```
task(
  category="quick",
  load_skills=[],
  run_in_background=true,
  description="Monitor CI for PR #<N>",
  prompt="""
  TASK: Monitor CI for PR #<N> (<branch>) until all checks settle, then report.

  REQUIRED TOOLS: Bash (gh CLI) only.

  MUST DO:
  - Run exactly one blocking command and let it wait for you:
      gh pr checks <N> --repo <owner>/<repo> --watch --interval 60
    This blocks until every check reaches a terminal state, then exits:
      exit 0 = all passed | exit 1 = a check failed | exit 8 = still pending/none
  - If exit code is non-zero, identify the failed run and fetch its logs:
      gh run list --repo <owner>/<repo> --branch <branch> --limit 5
      gh run view <run_id> --repo <owner>/<repo> --log-failed
  - Report: each check name + status, the exit code, and (on failure) the
    failing check, the log URL, and a ~50-line error summary.

  MUST NOT DO:
  - Do NOT poll in a model loop (no repeated single `gh pr checks` calls) —
    the --watch command blocks for you in the shell.
  - Do NOT fix anything or modify files.
  - Do NOT report success while exit code is 8 (still pending) — re-run --watch.

  CONTEXT:
  - PR: #<N> — <title> | Branch: <branch> → <base> | Repo: <owner>/<repo>
  """
)
```

Store the background task ID (`bg_...`) and continuation session ID (`ses_...`). When the `<system-reminder>` fires, collect results via `background_output` and act on failures.

**Simultaneous monitors are normal.** You may have 3–5 running at once (pre-fix CI, post-fix CI, post-merge deploy, etc.). This is expected and correct.

---

### Phase 4 — Second Review (Merge Gate, your second pass)

This is **your own** second, fresh review of the settled diff. Perform it **only after**:
- All CI checks are green on the latest commit
- **Every** review thread (any reviewer — bot or human) is replied-to and resolved (`isResolved: true`)

You do NOT wait on a human reviewer's formal approval — verifying and resolving their comments (fixing the relevant ones) is sufficient.

Second-pass checklist:
1. Re-read the full diff one more time: `gh pr diff <PR> --repo <owner>/<repo>`
2. Re-verify no thread is left unresolved (re-run the Phase 1 GraphQL query; all should be `isResolved: true`)
3. Verify commit history is clean (no stray debug/WIP commits)
4. Confirm the PR description matches what's being merged

If anything new surfaces → fix it, push, and restart from Phase 2 (new reviewer/CI cycle). If clean → proceed to merge.

---

### Phase 5 — Merge

Merge synchronously yourself — no waiting, no confirmation prompt (consent was granted once at session start). You are the gate, so do **not** use `--auto` (that would defer the merge to GitHub and fire before/independent of your gate):

```bash
# Feature branches → squash:
gh pr merge <PR> --repo <owner>/<repo> --squash --delete-branch
# Release/infra branches with meaningful history → merge commit:
gh pr merge <PR> --repo <owner>/<repo> --merge --delete-branch
```

Default to `--squash` unless the branch warrants a merge commit (release trains, infra PRs with meaningful history).

Confirm the merge actually happened before starting post-merge monitoring:
```bash
gh pr view <PR> --repo <owner>/<repo> --json state,mergedAt,mergedBy
```
`state` must be `MERGED` and `mergedAt` non-null before proceeding to Phase 6.

---

### Phase 6 — Post-Merge Pipeline Monitoring

Immediately after a confirmed merge, identify and monitor all downstream pipelines.

**App repos (pipeline triggers on push to the base branch):**
```bash
gh run list --repo <owner>/<repo> --branch <base_branch> --limit 10
```
Take the new run and monitor it with a Phase 3-style background monitor (`gh run watch <run_id> --repo <owner>/<repo>` blocks until it settles).

**Infra repos (pipeline does NOT trigger on push to main — only on PR or `workflow_dispatch`):**
For infra, merging produces a push-to-main that triggers **no** deployment pipeline. Do not wait on a run that will never start. Instead, trigger the deployment explicitly via `workflow_dispatch`, then monitor that run:
```bash
# Trigger the deployment workflow (only when a deploy is intended):
gh workflow run <deploy-workflow>.yml --repo <owner>/<repo> --ref <branch> [-f <input>=<value> ...]
# Find the run it created and monitor it:
gh run list --repo <owner>/<repo> --workflow <deploy-workflow>.yml --limit 5
gh run watch <run_id> --repo <owner>/<repo>
```
Dispatch the deployment automatically — do not pause to ask which services. Default scope: deploy the service(s) changed by the merge (infer from the changed paths / affected service dirs). If the repo has an obvious "deploy everything" workflow and no per-service split, use it. State the scope you chose inline and proceed.

**ArgoCD / Kubernetes (only if you have cluster access — check first):**
```bash
kubectl rollout status deployment/<name> -n <namespace>   # requires kubeconfig/context
```
If there is no cluster context available, skip and report rather than guessing.

Launch a background monitor for each downstream pipeline (Phase 3 pattern).

**You are responsible for failures that trace back to your merged changes.** If a post-merge pipeline fails:
1. Determine whether the failure is caused by your change (logs, compare to pre-merge baseline)
2. If yes → fix forward: new branch, fix, new PR, full auto-dev cycle (subject to the iteration cap below)
3. If no (pre-existing/unrelated) → report to user; do not attempt to fix

---

### Phase 7 — Service Deployment Monitoring

If the merge (or a `workflow_dispatch` you triggered) launches a service deployment (Kubernetes rollout, ECS task update, Lambda deploy, etc.):

1. Launch a dedicated background monitor for the deployment
2. Monitor until it reaches a stable terminal state (`rollout complete`, `deployment available`, `task running`, etc.)
3. If it fails or rolls back:
   - Collect the failure reason (pod logs, deployment events, CloudWatch logs as applicable)
   - Determine if caused by your change
   - If yes → investigate, fix, re-deploy following this same methodology (subject to the iteration cap)
   - Report to user with full context

---

## Iteration Rule

Every fix cycle (reviewer comment — bot or human, CI failure, or post-merge issue) follows the same methodology:

1. Fix on the appropriate branch
2. Push → triggers CI
3. Launch background CI monitor (Phase 3)
4. CI green → reply+resolve threads → second review → merge (or re-merge for post-merge fixes)
5. Launch post-merge / deployment monitor
6. Repeat until stable

**Local safety brakes (per-PR/per-deployment — they stop a futile sub-loop, NOT the session):**
- **Maximum 5 fix-forward cycles** per PR/deployment. On reaching 5, stop iterating *that* PR, **park it** (post an inline note on the PR + report in-session summarizing what was attempted), and **move on** to the next PR / queued work. Do not halt the session or wait for the user.
- **Circuit breaker:** if the *same* check/error fails twice in a row despite a fix, stop pushing fixes for *that* failure immediately — never shotgun the same error. Park the PR with a note and continue the session.

These brakes bound a single PR's effort; they never stop the overall self-feeding loop. Within the brakes, a PR has no exit until its deployment is stable and all pipelines are green — but a parked PR is set aside, not blocked-on.

---

## Background Agent Management

- Store every background task ID (`bg_...`) you launch and its continuation session ID (`ses_...`)
- When a `<system-reminder>` fires, immediately `background_output(task_id="bg_...")` to collect results
- Cancel monitors superseded by a new commit via `background_cancel(taskId="bg_...")`
- **Never** use `background_cancel(all=true)` — cancel individually

---

## User Communication

- Launching a monitor: "Monitoring [pipeline] in background — I'll alert you when it completes."
- About to merge: "All checks green, every review thread resolved, second review clean — merging now."
- Background failure: "⚠️ [check] failed on PR #N — [brief error]. Fixing now (cycle X/5)."
- Parked a PR (cap/breaker hit): "⏸ Parked PR #N after [N cycles / repeated failure] — [summary]. Moving on; flagged for later." (report, don't wait)
- After stable deploy: "✅ PR #N merged and [service] deployed successfully."
- You may answer user queries at any time while monitors run in the background.

---

## Tool Reference

```bash
# PR operations (pass --repo <owner>/<repo> or run from inside the repo)
gh pr view <N> --repo <owner>/<repo> --json number,title,url,headRefName,baseRefName,body,state,statusCheckRollup
gh pr diff <N> --repo <owner>/<repo>
gh pr checks <N> --repo <owner>/<repo> --watch --interval 60   # blocks; exit 0 pass / 1 fail / 8 pending
gh pr view <N> --repo <owner>/<repo> --comments
gh pr merge <N> --repo <owner>/<repo> --squash --delete-branch  # synchronous; NO --auto
gh pr merge <N> --repo <owner>/<repo> --merge  --delete-branch

# CI run operations
gh run list  --repo <owner>/<repo> --branch <branch> --limit 10
gh run view  <run_id> --repo <owner>/<repo>
gh run view  <run_id> --repo <owner>/<repo> --log-failed
gh run watch <run_id> --repo <owner>/<repo>                      # blocks until settled

# Infra deployment (workflow_dispatch — infra does not deploy on push to main)
gh workflow run <deploy>.yml --repo <owner>/<repo> --ref <branch> [-f key=value ...]

# Review threads — any reviewer (CodeRabbit, other bots, humans): list (get PRRT_ ids), reply, resolve — all GitHub GraphQL
# List threads + comment authors (author.login shows bot vs human):
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!,$first:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:$first){nodes{id isResolved isOutdated comments(first:100){nodes{databaseId author{login} body}}}}}}}' -f owner='<owner>' -f repo='<repo>' -F pr=<N> -F first=100
# Reply to a thread (input field: pullRequestReviewThreadId):
gh api graphql -f query='mutation($threadId:ID!,$body:String!){addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$threadId,body:$body}){comment{id}}}' -f threadId='PRRT_...' -f body='Fixed in <sha>.'
# Resolve a thread (input field: threadId):
gh api graphql -f query='mutation($threadId:ID!){resolveReviewThread(input:{threadId:$threadId}){thread{isResolved}}}' -f threadId='PRRT_...'
```

> GraphQL var typing with `gh api graphql`: use `-F` for Int/Boolean (`pr`, `first`), `-f` for strings (`owner`, `repo`, `threadId`, `body`).
