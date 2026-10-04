---
name: "PR: Land"
description: "Land an approved PR: merge to main, delete the branch, tag the version, sync the roadmap, clean up"
when_to_use: "When a PR is approved with checks green and the user wants it merged and the aftermath handled."
model: opus
effort: medium
metadata:
  glyph: ᛟ
  family: pr
disable-model-invocation: true
allowed-tools: ["Read", "Edit", "Bash(git:*)", "Bash(gh:*)", "Bash(cd:*)", "Bash(grep:*)", "Bash(~/.claude/library/scripts/safe-version-next.sh:*)", "Bash(~/.claude/library/scripts/checkout-occupied.sh:*)", "Bash(python3:*)"]
arguments: ["pr"]
argument-hint: "[PR number | URL]"
---

# PR: Land

The post-approval sequence as one skill: verify the PR is genuinely ready, merge with a merge commit (granular commits are documentation; they belong on main), then handle everything a merge leaves behind: branch, worktree, version tag, roadmap.

## Hard rule: the version guard

**The 0.x → 1.x boundary is never crossed by this skill, under any circumstances.** Tagging v1.0.0 (or `{plugin}-v1.0.0`) declares that surface's API stable and only a human does that. The guard is programmatic: every tag this skill creates, root or plugin, always comes from `safe-version-next.sh` (bare for root, `--plugin {name} --dir {source}` for a plugin), which emits a 0.x minor bump when svu proposes 1.0.0 and passes every other bump through (2.x, 3.x major bumps are fine). Never call `svu next` directly here, and never hand-compute a tag or a `plugin.json` version.

## Step 1: Verify readiness

Resolve the PR from `$ARGUMENTS`, then `gh pr view --json state,reviewDecision,mergeable,mergeStateStatus,statusCheckRollup,headRefName,baseRefName,title`.

Proceed only when: state `OPEN`, every entry in `statusCheckRollup` has finished and passed, and `mergeable` isn't `CONFLICTING`. Both halves of the rollup are default-deny, so an enum value this text doesn't name still blocks. A check run whose `status` isn't `COMPLETED` (`QUEUED`, `IN_PROGRESS`, `PENDING`, `WAITING`, `REQUESTED`) counts as not passed, as does a status context whose `state` isn't `SUCCESS` (`PENDING` and `EXPECTED` are the non-terminal ones); a `conclusion` or `state` of `FAILURE`, `ERROR`, `CANCELLED`, `TIMED_OUT` or `ACTION_REQUIRED` fails outright. A completed check run passes on a `conclusion` of `SUCCESS`, `NEUTRAL` or `SKIPPED`; a status context passes only on `state` `SUCCESS`. `reviewDecision` must additionally be `APPROVED` unless the repo lives under `github.com/jasonwarrenuk/` (personal repos have no reviewer, so that value never appears; check the resolved owner, not the local remote string). Anything short of that: report exactly what's unmet and stop. This skill lands ready PRs; it doesn't chase approvals (`pr-handle_review`) or fix branches.

**Stack detection** (see `~/.claude/library/references/stacked-prs.md`): the PR is part of a stack when `baseRefName` isn't the default branch, or `gh pr list --base {headRefName} --state open` shows a child PR targeting it. A stacked merge is bottom-up and contiguous: merging this PR also merges **every unmerged PR below it**, so extend the readiness check to each of those layers too, and note any open children above (they survive the merge and retarget automatically). A layer whose `statusCheckRollup` is empty has had no CI and does not pass: a workflow that only runs on pull requests into `main` never reaches the upper layers.

## Step 1.5: Bump any touched plugin

Only when `.claude-plugin/marketplace.json` exists (most repos don't ship plugins; skip this step entirely when it's absent). For each plugin entry (`name`, `source`), check whether this PR's diff touches that subtree: `gh pr diff {number} --name-only | grep -q "^${source#./}/"`. A stacked merge checks every layer's diff, not just this PR's own.

**Run every command in this step from a checkout of the PR's own head branch**, not main: `safe-version-next.sh --dir` (svu's `--log.directory` underneath) scans commits from `HEAD`, so running it from main (the common case, since Step 1 doesn't require checking the branch out) scans the wrong history and either misses the bump or, once a plugin tag exists, silently scans zero relevant commits. `gh pr checkout {number}` first (or `cd` into the worktree that already holds it), exactly as Step 4's cleanup later expects a checkout to exist.

For each touched plugin, run `~/.claude/library/scripts/safe-version-next.sh --plugin {name} --dir {source}`:

- **Exit 0** (a real bump): note the tag it printed (`{name}-v{X.Y.Z}`, not created yet, just computed) and the bare version (`{X.Y.Z}`) for the manifest. Find this plugin's own build script (`library/scripts/build-{name}-plugin.py` is this repo's naming for it; a repo with a differently-named or non-Python build step needs its own equivalent, found by reading the plugin's own docs or asking rather than assumed). That script names its version source file as a constant near its other per-plugin paths (`VERSION_SOURCE` in `build-roadmap-plugin.py`, for instance). Read the current value first: if it already equals `{X.Y.Z}` (someone bumped it by hand, or this step already ran once on this branch), skip straight to the rebuild check below rather than trying to commit a no-op. Otherwise write the bare version there, run the build script to regenerate the shipped plugin, then commit both onto the PR branch: `git commit -m "chore({name}): bump plugin version to {X.Y.Z}"` and push. This becomes part of what gets merged; it is not exempt from the "never amend or rebase reviewed commits" rule elsewhere in this config, because it is a brand new commit, not a rewrite of one the reviewer already saw. Rebuild check: even when the version file was already correct, `git status --short` the plugin's output directory after running the build script, since the version alone changing isn't the only reason the build could differ; commit if it produced any diff.
- **Exit 3** (nothing to release): the touching commits were all `docs`/`chore`/`refactor`-type, nothing version-worthy. Leave the plugin's version untouched; note this in the Step 2 summary so it's not mistaken for an oversight.
- **Exit 2** (environment error): stop and report; don't guess a version by hand.

A plugin's own bump commit is scoped to that plugin's subtree only (the rebuild output plus the version source file); never bundle unrelated changes into it. Multiple touched plugins in one PR each get their own bump commit, pushed in the same batch before Step 2's confirmation.

**Pushing restarts checks.** A push here can dismiss an existing approval or re-queue CI on a repo that has either; re-run Step 1's readiness check against the pushed commit before proceeding to Step 2, rather than trusting the state Step 1 read before this step existed.

## Step 1.6: Stamp end dates

Only when the repo has a rich roadmap (`python3 "$HOME"/.claude/library/scripts/roadmap.py detect` exits 0); otherwise skip silently. It runs on the PR's head branch, in the same checkout as Step 1.5, because the roadmap it edits is the branch's own and the date has to merge with the work. Never commit it to main afterwards: Step 3's rule stands.

1. Preview: `python3 "$HOME"/.claude/library/scripts/roadmap.py stamp-ended --base origin/{default branch} --pr {number} --dry-run --json`. The set is every done task that was not done at the branch's merge-base with the default branch, plus any done task whose `pr` is this PR's number, minus tasks that already have `ended`. Using the default branch as the base, even for a stacked PR, makes the set span every layer this merge lands.
2. Non-zero exit: the CLI prints a plain `✗` line, not JSON; relay it word for word. If it says `roadmaps.json` is not in canonical form, say that a write would reformat the whole file and rerun the preview with `--reformat` solely when the user agrees, keeping the flag on the write. On a refusal or any other failure (no merge-base with `origin/{default branch}`, a phase the merge-base cannot read, a bad `--date`, an unreadable roadmap on exit 2), skip this step, say in the Step 2 summary that no end dates were stamped and carry on; `roadmap-maintain` in Step 4 backfills them.
3. Empty `tasks`: nothing to do, move on. Otherwise rerun without `--dry-run`, then `git commit -m "chore(roadmap): end {IDs}"` (the roadmap file only) and push.
4. The date is today, which is the landing day. If the PR sits waiting past midnight, pass `--date` with the day the approval to merge is given.

A task the PR finished but that is not marked `done` on the branch is not stamped; say so in the Step 2 summary so it is not mistaken for an oversight (`roadmap-maintain` fixes the status and backfills the date later). Like Step 1.5, this push restarts checks: re-run Step 1's readiness check against the pushed commit before Step 2.

## Step 2: Confirm and merge

Show a one-line summary (title, head → base, review state, checks) and **await approval**; merging is irreversible in practice. For a stacked PR the summary must list every layer the merge will land (this PR plus all unmerged PRs below it): the approval covers the lot. If Step 1.5 bumped any plugin, list each one's new version and the commit that carries it, so the approval covers that too. If Step 1.6 stamped end dates, list the task IDs and the date. Then, for an ordinary PR:

```bash
gh pr merge {number} --merge --delete-branch
```

For a stacked PR:

```bash
gh stack merge {number} --merge
```

Do not run plain `gh pr merge` on a stack (the docs say the legacy merge endpoint can't merge stacks). **Always name the PR: `gh stack merge {number} --merge`, never a bare `gh stack merge`, a stack number or `--yes` alone.** In Claude's shell, which has no terminal, `gh stack merge` merges everything it names without prompting, so a bare invocation lands every layer including those above the PR just approved. Stack numbers and PR numbers never overlap (`gh stack link --help`), so there is no collision to work around; before running, confirm the layers `gh stack merge {number}` would land match the approved summary. It lands that PR and every unmerged layer below it, all or nothing, bottom-up (whether each layer gets its own merge commit is unverified: check `git log --first-parent` after the first real stacked landing); open PRs above retarget `main` via GitHub's server-side rebase, which produces unsigned commits. `gh stack merge` has no `--delete-branch`, so afterwards delete each merged layer's remote branch (`git push origin --delete {branch}`), but **only after confirming no open PR still targets it** (`gh pr list --base {branch}`; retargeting is normally immediate).

Merge commit, never squash or rebase: the branch's atomic commits are the history. `--delete-branch` removes the remote branch and, where the local branch isn't checked out elsewhere, the local one too.

If child PRs remain open above the merge point, run `gh stack sync --prune` from a checkout of the stack so the surviving local branches rebase onto the new `main` and stale refs go.

## Step 3: Tag the version

**The main checkout is never switched, pulled or committed to here.** Another session may be working in it, and a branch change under that session sends its next commits to the wrong branch. Everything after the merge runs in a detached landing worktree on `origin/main`, created from wherever the shell is:

```bash
git fetch origin main --tags \
  && git worktree add --detach "${TMPDIR:-/tmp}/pr-land-{repo}-{number}" origin/main \
  && cd "${TMPDIR:-/tmp}/pr-land-{repo}-{number}"
```

The path is built from the repo name and PR number because shell variables don't survive between commands; later steps rebuild the same string.

**Then find out whether CI tags this repo.** Look on the default branch for a workflow that creates tags on push:

```bash
git grep -lE 'git tag|svu|semantic-release|release-please|tag-action' origin/main -- .github/workflows
```

Read each hit (`git show origin/main:{path}`) to confirm it runs on a push to the default branch and pushes a tag for this series.

**A tagging workflow exists: defer to it and create no tag.** Find its run for the merge commit and wait for it:

```bash
gh run list --workflow {file} --commit {mergeSha} --json databaseId,status,conclusion
gh run watch {databaseId} --exit-status
git fetch origin --tags && git tag --points-at {mergeSha}
```

Report the tag CI created, or that CI found nothing to release. A failed or missing run gets reported as it stands and tagging stops there: a hand-made tag on a repo whose CI tags is how tag and changelog drift apart. If the CI tag crossed 0.x → 1.x, say so plainly in the report.

**No tagging workflow: tag from the landing worktree.**

```bash
TAG="$("$HOME"/.claude/library/scripts/safe-version-next.sh)" \
  && { git ls-remote --exit-code --tags origin "refs/tags/$TAG" >/dev/null 2>&1 \
       && echo "$TAG already on origin, leaving it alone." \
       || { git tag "$TAG" && git push origin "$TAG"; }; }
```

The `ls-remote` check is a backstop for a tag source the grep missed; it costs one no-op round-trip everywhere else. A multi-layer stack merge is one landing event: tag once for the lot, never once per layer. Push the single tag, never `git push --tags` (that publishes every local tag, strays included). Script exit **3** means nothing to release: no version-bumping commits since the current tag (a docs-only or chore-only PR); say so and skip to Step 4. If the script printed its 0.x guard note to stderr, relay it: the user should know a major bump was requested and deliberately held at 0.x.

**Any plugin Step 1.5 bumped gets tagged here too** (unless the CI workflow covers that plugin's tag series as well), same landing event, same `ls-remote`-before-push pattern, with `--plugin {name} --dir {source}` on `safe-version-next.sh` and `{name}-v{X.Y.Z}` as the tag. Since the version was already computed and committed pre-merge, this recomputes the same value from the now-merged commit (the tag anchors to the merge commit, not the pre-merge bump commit) rather than reusing the Step 1.5 string outright: if something else landed on main between Step 1.5 and the merge, this is the check that catches drift. A mismatch here (the script proposes something other than what Step 1.5 bumped to) means main moved under you; stop and report rather than tagging something that no longer matches `plugin.json`.

## Step 4: Clean up the checkout

Steps 1 and 2 run from the landing worktree: it sits outside the branch's own worktree, and its `HEAD` holds the merge, which is what `git branch -d` checks against.

1. If a worktree held this branch (`git worktree list`), remove it, from **outside** it, never while the shell is inside. A stack merge may have landed several branches; clean up each merged layer's worktree, but leave the worktrees of still-open child PRs alone (post-sync they're live work, not leftovers).
2. If the local branch survived (it was checked out somewhere), `git branch -d {branch}`: only `-d`; a refusal means unmerged commits and stops the line, not `-D`.
3. Remove the landing worktree last, standing in the main checkout without touching its branch: `cd "$(git rev-parse --path-format=absolute --git-common-dir)/.." && git worktree remove "${TMPDIR:-/tmp}/pr-land-{repo}-{number}" && git worktree prune`.
4. Bring the main checkout up to date only when that is safe. Run `~/.claude/library/scripts/checkout-occupied.sh` there: fast-forward with `git pull --ff-only` when it exits 0 **and** its JSON shows `branch` as `main` and `dirty_files` as 0. Anything else (another live session, a different branch, uncommitted files), leave the checkout exactly as it is and name the reason in the Step 6 report.

## Step 5: Roadmap sync

If the repo has a rich roadmap (`python3 "$HOME"/.claude/library/scripts/roadmap.py detect` exits 0), offer to run the `roadmap-maintain` skill so the merged work's task lands as `done` and the projections refresh; it also backfills any done task whose `ended` Step 1.6 missed. Offer, don't assume; the PR may not map to a roadmap task.

## Step 6: Report

PR merged (URL), tag(s) created (root and any bumped plugin), branch/worktree state after cleanup, roadmap synced or skipped, and the task IDs given an end date by Step 1.6. If the changelog matters for this project, offer `/doc-changelog root md {tag}` for the root tag and, for each bumped plugin, `/doc-changelog plugin:{name} md {name}-v{X.Y.Z}`; `doc-changelog`'s scope and version arguments together scope each run to exactly one release. Also offer `/hud-whats_new {previousTag}` so the user sees what they can now do that they couldn't before this landing.

## Red flags

**Never:** cross 0.x → 1.x on any tag series, root or plugin (the guard script is the only tag source); squash or rebase-merge; merge with failing or pending checks "because they'll pass"; run `git checkout`, `git switch` or a bare `git pull` in the main checkout; create a tag on a repo whose CI tags; remove a worktree from inside it; use `git branch -D`; tag before the merge has actually landed on main; run plain `gh pr merge` on a stacked PR, or run `gh stack merge` with no PR number, with a stack number, or with `--yes` alone (use `gh stack merge {number} --merge`); delete a branch that is still the base of an open PR; hand-edit a plugin's `version` field or its build output instead of running `safe-version-next.sh` and the plugin's own build script.

<raw-arguments value="$ARGUMENTS" />
