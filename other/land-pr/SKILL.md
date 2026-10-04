---
name: land-pr
description: Take a reviewed branch from ready to landed — merge-strategy verdict with rationale, history cleanup with per-commit verification, then merge and branch deletion. Also answers "rebase or merge?" as an advisory-only run.
disable-model-invocation: true
---

# Land PR

Takes a reviewed branch from "ready" to "landed", with two gates and one early exit:

1. **Verdict** — analyze the commit series, recommend a strategy with rationale, propose the final commit list. Stop and wait. If Atila only asked "rebase or merge?", this is the whole job.
2. **Rewrite** — on go-ahead, clean the history so every retained commit is a valid state, then update the remote branch.
3. **Land** — on a second confirmation, merge and delete the feature branch.

Runs only when Atila invokes it by name — the rewrite never starts from another skill's flow. Siblings cover the adjacent jobs: `commit-me` lands a single commit, `aa-commit-clarity` decides boundaries for an uncommitted diff, `draft-pr` describes the branch without reshaping it, `deploy-check` turns a flagged diff into a deployment verdict and runbook. This skill is the reshaping-and-landing step that runs after the PR has been reviewed.

## Judgment: the three jobs of history

Small commits are valuable when each is a valid, coherent state. A superseded mistake preserved in history is not memory — it is a **false trail**: a commit whose message or test codifies behavior a later commit corrects. Bisect can land on it green, and a future agent can read it as intent and try to restore it.

History serves three jobs, and the verdict must argue from all three:

1. **Review** — small commits let a reviewer follow the building blocks. Usually already served by the time this skill runs.
2. **Bisect/revert** — every commit must build, pass, and mean what it says. A green commit codifying wrong behavior looks authoritative.
3. **Memory** — the causal structure of the final system: which invariant each commit introduces, why the code exists. The discovery journey ("implemented X, learned it was wrong, replaced it") served review; it is not architecture.

Verdicts, first fit wins:

- **preserve-as-is** — the series is already meaningful, valid building blocks. Common when `commit-me` and `aa-commit-clarity` did their jobs during development. Skip Step 3 entirely.
- **fold-and-clean** — building blocks worth keeping, plus fixups and review corrections that belong inside the commits they repair. The typical shape after a post-PR review round.
- **squash** — the change is genuinely indivisible, or the history is too tangled to clean economically.
- **merge-commit** — the branch topology itself matters (coordinated multi-branch work). Rare on a linear single-author branch.

## Workflow

### Step 1: Preconditions

Identify the base branch: `git symbolic-ref --quiet refs/remotes/origin/HEAD` (strip the prefix), falling back to `origin/main`, then `origin/master`, then ask.

Then check, after `git fetch origin`:

- **Dirty working tree** → stop and ask. The changes might belong in the PR — that is `commit-me` / `aa-commit-clarity` territory, not a stash.
- **Local commits not on the remote PR head** → normal in Atila's flow (review-round fixes). Fold them into the plan and note them in the verdict ("includes unpushed `abc1234`").
- **Remote commits not local** (`git rev-list --count HEAD..origin/<branch>` > 0) → stop and ask. Someone else touched the branch.
- **Allowed merge methods** — query before verdicting, so the verdict is executable:
  - GitHub: `gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`
  - GitLab: `glab api "projects/:id" --jq .merge_method`

  When the ideal method is disabled, say so in the verdict and reason within what the repo allows. Squash-only repos change the calculus: folding is only worth it when the multi-commit series helps the PR reader — otherwise recommend squash and skip the rewrite.

**Done when** base branch, branch sync state, and allowed methods are all known.

### Step 2: Verdict — gate 1, and the advisory exit

Read the series in full — `git log <base>..HEAD --format=fuller` and `git diff <base>...HEAD --stat` (three dots) — and classify every commit: valid building block, fixup/correction, or false trail. While reading, also scan for deployment-impact signals — migrations, new env-var reads, cron/worker/queue/cache/API-contract changes. **Done when** each commit has a classification, grounded in messages and diff shape, not subject lines alone, and the impact scan has a result.

If the scan flagged anything, run `deploy-check` on `<base>...HEAD` before presenting the verdict. A **red** deploy-check verdict changes the landing strategy itself (usually an expand/contract split into two PRs) — fold that into the verdict rather than landing as planned.

Then present the verdict in this shape — the three-jobs rationale is required, not decoration; it is how Atila learns why this method fits this PR:

> **Verdict: fold-and-clean → rebase-and-merge (3 commits)**
>
> - *Review*: served — the PR was reviewed commit-by-commit.
> - *Bisect*: commits 4 and 7 codify behavior commit 8 corrects — a false trail.
> - *Memory*: the final series should read as invariants, not the discovery journey.
>
> Proposed final series:
> 1. `fix(tracking): gate enquiry conversions to successful enquiries` — hook, integration, behavioral tests (folds in 8's correction)
> 2. `fix(thank-you): preserve loader response headers` — response composition, server-boundary tests
> 3. `docs(tracking): record enquiry conversion signal decisions`
>
> Repo allows all three merge methods.
> Deploy impact: yellow — additive migration + new env var; runbook at gate 2. *(or: "none — merge is the whole deploy story")*

Stop here and wait. If the invocation was advisory ("rebase or merge?"), this is the deliverable — offer to continue, then leave it. A **preserve-as-is** verdict skips Step 3 on go-ahead and moves straight to Step 4.

### Step 3: Rewrite

On go-ahead only:

1. **Backup ref** — `git branch backup/<branch>-before-history-cleanup-<YYYYMMDD>` at the current head. It stays after the merge; the summary reports it.
2. **Rebase onto fresh base first** when the branch is behind — the fold and the update are one rebase. Verifying boundaries against the *new* base is the point: a server-side rebase at merge time re-creates commits without re-running anything. If conflicts arise, that is `resolving-merge-conflicts` territory — pause and surface, don't improvise.
3. **Build each retained commit** and verify at every boundary: the project's test suite, typecheck, and formatter all pass. This is the load-bearing promise — a bisect must never land on a broken or lying intermediate commit.
4. **Commit messages** follow `commit-me`'s conventions. Two rules restated because they fail silently: no attribution footers, and `Refs #N` never `Closes`/`Fixes`.
5. **Prove equivalence** — `git rev-parse HEAD^{tree}` matches the backup ref's tree. The reviewed code and the rewritten code are byte-identical; only the history changed.
6. **Push** with `--force-with-lease`.

**Done when** every boundary passed verification, the trees match, and the forge reports the PR clean and mergeable.

### Step 4: Land — gate 2

Present the final state (commit list, verification results) — plus `deploy-check`'s runbook when Step 2's scan flagged anything — and ask once. On confirmation, merge with the verdict's method and delete the feature branch:

```sh
# GitHub
gh pr merge <number> --rebase --delete-branch   # or --squash / --merge

# GitLab
glab mr merge <number> --remove-source-branch   # method per project settings; add --squash when squashing
```

Then summarize: the commits that landed (full messages), verification results, and the backup ref's name so Atila can delete it whenever.
