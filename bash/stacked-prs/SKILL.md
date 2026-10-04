---
name: stacked-prs
description: >-
  Manage GitHub stacked pull requests end to end with the native `gh stack` extension — split one large change into a chain of reviewable layers, submit the stack, navigate it, keep it synced when trunk moves, review it layer by layer, land it, and repair it when a restack or a mid-stack merge breaks the chain. Use this skill whenever the user mentions a stack, stacked PRs, `gh stack`, a PR chain, dependent PRs, a PR "on top of" another, restacking, "this PR is too big to review", splitting a branch into several PRs, or a PR whose base is another feature branch instead of main — even if they never say the word "stack". Also use it when a PR's base branch was deleted or squash-merged and its children now show the wrong diff, when a stacked PR will not merge, or when a merge queue ejected a child PR. Pass `--auto` for non-interactive, skill-to-skill invocation. For a single non-stacked branch rebase, use the `rebase` skill instead.
allowed-tools: Bash(git *) Bash(gh *) Bash(jq *) Bash(~/.claude/skills/stacked-prs/scripts/*) Read AskUserQuestion
---

# Stacked PRs

A stack is a chain of branches where each PR's base is the branch below it, not the trunk. Stacks make a large change reviewable. They also add one failure mode normal branches do not have: **a change to any layer invalidates every layer above it.** Everything here follows from that.

`gh stack` is GitHub's own extension for the native stacked-PR feature, in public preview since 2026-03-10. It is not a third-party tool, and the feature is still changing. Trust `gh stack <cmd> --help` over any command shape you remember, including the ones written here.

## The one discipline that matters

`gh stack` v0.1.0 **exits 0 even when it fails.** Verified locally: with a stack branch checked out in a second worktree, both `gh stack rebase` and `gh stack sync` printed `✗ checking out sp-probe-l1: failed to run git` and still returned `rc=0`.

So never treat a zero exit as success, and never chain stack commands with `&&`. Run this loop instead:

1. **Probe** the state with the bundled script.
2. **Act** on one verdict.
3. **Re-probe** and compare. A changed state is your only proof the command worked.

Read stdout as well. The `✗` lines carry the real error.

## Step 0 — always probe first

```bash
~/.claude/skills/stacked-prs/scripts/stack-state.sh          # human table
~/.claude/skills/stacked-prs/scripts/stack-state.sh --json   # normalized JSON
```

The script is the only thing that should read `gh stack view --json`. Two schema traps make hand-rolled `jq` wrong, both verified against real output:

- The branch key is `name`, not `branch`.
- `base` is the **trunk SHA** the stack was cut from, not the parent branch. The parent chain exists only as array order, so the script derives `parent` from the index. A column showing `base` as a branch name is lying to you.

The script also reports `squash-only` and `merge-queue` for the repo, because that pair changes how you land (see Landing).

### Exit codes

| Code | Meaning | What to do |
|------|---------|------------|
| 0 | Tracked stack found | Act on `verdict` |
| 2 | Branch is in no stack | Offer `gh stack init`, or `gh stack checkout` to adopt one |
| 3 | `gh`, `jq`, or the extension is missing | Install it, then re-probe |
| 4 | PR has a non-trunk base but no tracked stack | Adopt it — see Adopting |
| 5 | `gh` or the API failed | **Stop.** Unknown is not "no stack". Never force-push here |

Exit 5 is the dangerous one. A `gh` auth or network failure reads as "not stacked", and acting on that reading force-pushes a stacked branch onto trunk.

## Verdicts and their playbooks

The script reports every true condition, not just one, because a stack is routinely both behind trunk and unsubmitted. Work the primary verdict, then re-probe.

| Verdict | Meaning | Command |
|---------|---------|---------|
| `CLEAN` | Every layer submitted and current | `gh stack merge` |
| `UNSUBMITTED` | Local layers have no PR yet | `gh stack submit` |
| `TRUNK_MOVED` | Trunk advanced under the stack | `gh stack sync` |
| `STALE` | A layer's parent moved (`needsRebase`) | `gh stack rebase`, then `gh stack push` |
| `MERGED_MIDSTACK` | A layer landed, descendants are broken | `gh stack sync --prune` |
| `CONFLICT` | A restack stopped mid-flight | Resolve, then `gh stack rebase --continue` |
| `ALL_LANDED` | Whole stack merged | `gh stack sync --prune` |
| `SQUASH_QUEUE_RISK` | Squash-only repo with a merge queue | Land one PR at a time — see Landing |

`MERGED_MIDSTACK` outranks the others for a reason. Under squash merge the squash commit exists in no child's history, so every descendant carries the parent's changes as its own diff until it restacks. The PR looks wrong to reviewers before it looks wrong to git.

After any repair that rewrites a layer — `sync`, `rebase`, or a `--prune` — tell the reviewers of the layers above it. **A restack sends no notification and posts no comment.** Their approvals now sit against a diff that no longer exists, and nothing in the GitHub UI tells them so. Saying "I restacked, your diff moved" is part of the repair, not a courtesy.

## Prefer sync over push

`gh stack push` is **not atomic.** Its own help says a branch may update even when another is rejected, which leaves the stack half-pushed. `gh stack sync` pushes with `--force-with-lease --atomic`, so the whole stack moves or none of it does.

Reach for `push` only to retry the one branch a previous `sync` left behind.

Set `push.useForceIfIncludes=true` once per machine if it is unset. `--force-with-lease` alone trusts your remote-tracking ref, which a background fetch can advance without you ever reading the new commits, so a teammate's commit gets clobbered anyway. `--force-if-includes` checks the reflog and closes that gap.

## Autonomy contract

Interactive is the default. Reads and local restacks run freely.

Before the first remote write in a session — `submit`, `sync`, `push`, `merge`, `unstack` — name the branches that will move and ask once with `AskUserQuestion`. One confirmation covers the rest of that operation. Do not ask per branch.

### `--auto` mode

When invoked as `/stacked-prs --auto`, skip every `AskUserQuestion`. This is the non-interactive contract for another skill or an orchestrator. In auto mode:

- **Dirty tree** — refuse. Print `--auto requires a clean tree` and exit non-zero. Never commit or stash on the user's behalf.
- **Probe exit 5** — refuse. Stacked state is unknown, so any push is a guess.
- **`CONFLICT`** — refuse. Print the conflicting branch and stop. A conflict needs a human decision about intent.
- **`gh stack merge`** — never. Landing is irreversible, and how far up the stack to go is the user's call.
- Everything else — `sync`, `rebase`, `push`, `submit` — runs without prompting.

## Working in worktrees

**Stack metadata is per worktree.** Verified: it lives at `$GIT_DIR/gh-stack`, which for a worktree is `.git/worktrees/<name>/gh-stack`, not the shared common dir. A stack created in one worktree is invisible from another worktree of the same repo, where the probe returns exit 2.

Two consequences:

- Run every `gh stack` command from the worktree that created the stack. Re-adopt elsewhere with `gh stack checkout <pr-number>`.
- A stack branch checked out in a second worktree makes `sync` and `rebase` fail, with exit 0. When a restack prints `✗ ... already used by worktree`, free the branch there, then re-probe.

Plain `git rebase --update-refs` has the same boundary by design: it never moves a branch checked out in another worktree. That is a documented safety rule, not a bug.

## Splitting one change into a stack

This is the judgment the tooling cannot make. A good layer is **independently reviewable and leaves the build green.**

Order layers so each needs only what is already below it:

1. Schema and migrations.
2. Models and validations.
3. Services and business logic.
4. Controllers, routes, serializers.
5. Frontend.
6. The flag flip or entry point that makes the feature reachable.

Two boundary tests:

- If a layer's tests cannot pass without a later layer, the boundary is wrong. Move the code down, not the tests up.
- If a reviewer must read layer 4 to judge layer 2, they are one layer.

Keep the stack shallow. Every trunk move cascades through all of it, so depth costs restacking work continuously while review quality plateaus. Three to five layers is common practice rather than a documented rule, so treat it as a default to argue with, not a limit.

Build it with `gh stack init <bottom> <middle> <top>`, or grow it a layer at a time with `gh stack add -Am "<message>" <branch>`.

### Restructuring

`gh stack modify` opens a TUI to drop, fold, reorder, insert, or rename layers. It stages everything and applies on Ctrl+S. Run `gh stack submit` afterwards, because modify changes local branches without updating the PRs.

## Reviewing a stack

Review bottom up, one layer at a time. A layer's diff is only meaningful against its own parent, so read `parent` from the probe and check the PR's base matches it before judging the diff. A mismatch means the stack needs a restack, and the diff you are reading is noise.

When review lands changes on a lower layer, everything above goes stale. Fix the lower layer, run `gh stack sync`, re-probe, then tell the reviewers of the upper layers that their diffs moved. Restacking notifies nobody.

## Landing

Land bottom up. Every source agrees on this, and GitHub enforces it: a stacked PR merges only once it and every PR below it meet all requirements and the stack has linear history. A push to a lower layer breaks linearity and blocks the merge until you restack.

`gh stack merge` is GitHub's atomic stack merge. Every PR up to your selection lands as one all-or-nothing operation, so a partial merge cannot strand descendants.

- `gh stack merge` — interactive picker for how far up to go.
- `gh stack merge <pr-number>` — land everything up to and including that PR.
- `gh stack merge --yes --squash` — non-interactive, explicit method.

### Squash plus a merge queue

When the probe reports both `squash-only=true` and `merge-queue=true`, do **not** enqueue the whole stack. This combination reproducibly ejects the child PR with `invalid_merge_commit`, because the queue validates the child's speculative merge commit against a base that does not yet contain the parent's squashed result.

Land those stacks serially instead. Enqueue the bottom PR alone, let it merge and let GitHub retarget the child, restack, then enqueue the child alone. The batched "enqueue stack" path is the broken one.

Merge-commit and rebase-merge strategies are not shown failing this way.

### Other landing notes

- The queue keeps a stack together and will exceed its configured group size by up to 50 percent to do so. A stack too large for one group can still split across consecutive groups, which is how the base-deleted closure bug in `references/failure-modes.md` starts.
- Merge requirements cannot be bypassed for a stack. GitHub evaluates branch protection when the merge runs and reports failures back.
- Do not hand-merge layers bottom up in a squash-only repo. Each squash orphans the next layer's history and forces a restack you did not need.
- After landing, `gh stack sync --prune` deletes local branches for merged PRs and keeps the metadata the remaining layers rely on.

## Adopting an existing chain (probe exit 4)

A hand-built chain — PRs whose bases point at each other via `gh pr edit --base` — is not a tracked stack. Two ways in:

- `gh stack checkout <pr-number>` when the PRs already form a stack on GitHub.
- `gh stack link <bottom> <middle> <top>` otherwise. It takes branch names, PR numbers, or PR URLs in bottom-to-top order, pushes branches, creates missing PRs with the right base chain, and needs no local tracking. This is also the way in for anyone driving `jj`, Sapling, or `git-town`.

Pass a stack number as the first argument to append to an existing stack.

## Limits worth knowing before you start

- **Cross-fork stacks are unsupported.** Every branch must live in one repo.
- **The web "Rebase stack" button produces unsigned commits.** A repo requiring signed commits has to restack from the CLI.
- **A closed mid-stack PR blocks every PR above it.** The stack relationship survives the close, so you unstack and rebuild rather than just reopening.
- **`gh stack unstack` leaves merged and queued PRs stacked.** GitHub decides what can dissolve. When some PRs stay, the stack stays and local tracking is untouched.

## Delegating

- **Single branch, not stacked** — use the `rebase` skill. It owns detection, the conflict loop, and its own `--auto` contract.
- **Whole stack** — stay here. `rebase --auto` deliberately never runs whole-stack operations.

Never pass `--update-refs` to a `gh stack` command. It is the bare-git equivalent for untracked local stacks, and it moves local refs only.

## Reference files

- `references/failure-modes.md` — symptom-first repair table. Read it on `CONFLICT`, `MERGED_MIDSTACK`, a `✗` line, a closed or unmergeable stacked PR, or a queue ejection.
- `references/other-tools.md` — bare `git rebase --update-refs`, Graphite, Aviator, Sapling, `spr`, `ghstack`. Read it when the repo does not use `gh stack`.

## Traps

- Treating exit 0 as success. Re-probe instead.
- Treating a `gh` failure as "not stacked", then force-pushing onto trunk.
- Hand-rolling `jq` over `gh stack view --json` and reading `base` as a branch name.
- Running `gh stack` from a worktree that does not own the stack.
- Enqueueing a whole stack in a squash-only repo with a merge queue.
- Hand-merging layers bottom up under squash merge.
- Using `gh stack push` where `sync` is what keeps the stack atomic.
- Restacking after review, then not telling reviewers their diffs moved.
- Confusing the docs site `github.github.com/gh-stack` with the source repo `github.com/github/gh-stack`. The first is documentation, the second is where the bug reports live.
