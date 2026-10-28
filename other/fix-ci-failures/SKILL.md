---
name: fix-ci-failures
description: Read a branch's latest failed CI runs, triage each failure from its existing logs, and fix the real ones.
disable-model-invocation: true
argument-hint: "Branch name (defaults to main), then optional guidance (\"skip lint\", \"only the test job\")"
allowed-tools: "Bash(gh run list *) Bash(gh run view *)"
---

# Fix CI Failures

Take the branch named in the input, or `main` when none is given. Find its most recent
CI failures, triage each one from the logs that **already exist**, and fix what is
real. The logs are the whole evidence: CI is a record you read, never a thing you
trigger. Your own proof that a fix works is the failing command run green locally.
Text after the branch name is overriding guidance.

**Project context.** Follow the repo's `AGENTS.md` / `CLAUDE.md` rules for tests, lint,
cache clears, and a dirty tree.

## 1. Find the latest failures

Run `git fetch origin`. For each workflow, take only its newest **completed** run on the
branch that was not cancelled, looking back at most 10 runs. An older failure whose
workflow has passed since is already fixed, and a run still in progress or cancelled is
not evidence: skip them. A workflow whose last 10 completed runs were all cancelled
comes back as `all_cancelled`: report it with no verdict, since it has no log to triage.

```bash
gh run list --branch B --status completed --limit 100 \
  --json databaseId,workflowName,conclusion,headSha,createdAt,url \
  --jq 'group_by(.workflowName) | .[] | sort_by(.createdAt) | reverse | .[:10]
        | (map(select(.conclusion != "cancelled")) | first)
          // {workflowName: .[0].workflowName, conclusion: "all_cancelled", url: .[0].url}
        | select(IN(.conclusion; "failure", "timed_out", "startup_failure", "all_cancelled"))'
gh run view RUN --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {databaseId, name, url}'
gh run view --job JOB --log-failed
```

No workflow comes back: report that the branch's latest completed runs are green, and stop.

Completion criterion: every failed job is listed with its workflow, run URL, `headSha`,
and the first real error from its log (not the trailing `exit code 1`).

## 2. Classify every failure

Read `git log --oneline <headSha>..origin/B` first: commits since the failed run may
already fix it. Then write one line per failed job:

```
Failure N: [LEGIT | STALE | FLAKY | INFRA] — <one-line evidence>
```

- **LEGIT**: the error points at code on the branch, and it reproduces at `origin/B`
  when you run the same command locally.
- **STALE**: a later commit fixed it. Cite the sha, or show the command passing locally.
- **FLAKY**: it passes locally at the same sha, and the log shows timing, ordering, or
  a network call.
- **INFRA**: runner, cache, registry, secret, or quota errors, and anything that needs
  a CI setting or a human decision. Name what it needs.

When the command cannot run locally (a missing service or secret), classify from the
log and the code alone, and say that it is unreproduced.

Completion criterion: every failed job has a line.

## 3. Fix the legit ones

No LEGIT left: go to step 5.

Work on the branch without disturbing a dirty tree or another worktree's checkout. When
the tree is dirty or the branch is checked out elsewhere, use
`git worktree add .claude/worktrees/ci-<branch> origin/B` (at that path, never a sibling
directory), then make it runnable with `laravel-herd-worktrees`' **Bootstrap a bare worktree** section before running anything in it. Leave it in place until step 5. Per
LEGIT failure: make the minimal change, run the failing command locally until it is
green, then commit with explicit staging (Conventional Commits, naming the job).

Completion criterion: every LEGIT failure has a commit that turned its command green
locally.

## 4. Land the fixes

A commit on the worktree fixes nothing until it is on `B`. Show the commits, say where
they will go, and land them without asking:

- **Default:** push to `B` with `git push origin HEAD:B` (no `--force`). If it is
  refused because `origin/B` moved, `git fetch origin`, rebase onto `origin/B`, re-run
  each fixed command, and push again.
- **Direct pushes forbidden** (branch protection, or the repo's rules): push a
  `fix/ci-<branch>` branch and open a pull request into `B` with a body in the `pr`
  skill's template.
- A user instruction in the input or the conversation ("open a PR", "don't push")
  overrides both.

The push starts new CI runs. Leave them running and do not come back for their result.
When step 3 worked in the main checkout on a local `B`, it is now in step with
`origin/B`; when it worked in a worktree, leave the user's local `B` as it is and say
it is behind.

Completion criterion: every fix commit is on `origin/B`, in an open pull request, or
kept local by the user's instruction.

## 5. Clean up and report

If step 3 created a worktree and its commits are on `origin/B` (or in the open pull
request), remove it without asking: `herd unlink <name>` from inside it if the bootstrap
linked it, then `git worktree remove` (no `--force`). If git refuses,
or the commits are kept local, keep it and ask one yes/no question: "Can I delete the
worktree I created?" Remove it only on yes, never with `--force`; otherwise name it in
the report as kept.

One line per failed job: fixed in `<sha>`, stale (`<sha>`), flaky, infra (what it
needs), or unreproduced. Then say where the commits landed, and each worktree removed
or kept.
Start each job line with a mark: ✅ fixed or stale, ⚠️ flaky, infra, or unreproduced.

## Guardrails

CI evidence comes only from runs that already exist. Do not run `gh run rerun`,
`gh workflow run`, or `gh run watch`, do not push an empty or retry commit, and do not
wait on a run.
