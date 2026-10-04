---
name: closeout
description: "Primary pipeline tail step after /pre-merge, when a reviewed PR is ready to land and you want the workspace back to a clean base. Use to merge, switch off the worktree before removing it, prune the merged branch, pull base, and verify a clean end state. Triggers on 'close out', 'merge and clean up', 'get back to a clean main/base', 'tear down the worktree'. Not for capturing lessons (that's /compound) or closing PRD/slice issues and research-artifact hygiene (that's the cleanup prose in SYSTEM-OVERVIEW Step 9)."
sources:
  primary:
    - "Thinking in Systems — Donella Meadows"
    - "The Design of Everyday Things — Don Norman"
  secondary:
    - "The Checklist Manifesto — Atul Gawande"
    - "Continuous Delivery — Jez Humble & David Farley"
---

# Closeout

Take a reviewed PR and return the workspace to a clean base — merge, switch the shell off the worktree before removing it, prune the merged branch, pull base, and verify the end state. This is the pipeline's tail: the most-repeated motion ("I'm done, merge it and get me back to a clean main") moved out of the user's head and into a skill.

## Why This Exists

`/execute` Step 0 *creates* a worktree for every slice; until this skill existed, nothing *removed* one. Worktrees are a stock with an inflow and no outflow, so the stock rises without bound (Meadows, *Thinking in Systems* — the structural escape for an inflow-without-outflow stock is to *add the missing feedback loop*, not to exhort harder). The merge → teardown → pull sequence lived only in the user's memory, and "prospective memory fails silently" (Norman, *The Design of Everyday Things* — move the knowledge from the head into the world). The ordering is genuinely error-prone: removing a worktree while the shell's cwd is still *inside* it strands the shell on a trashed directory, and a `node_modules`-dependent Stop hook firing from there emits a wall of false `MODULE_NOT_FOUND` "lint/type errors" that read like a real regression. The cd-to-base-before-remove ordering in Step 4 is the load-bearing fix for exactly that slip.

This skill *orchestrates existing tools* (`gh pr merge`, `wt remove` / `git worktree remove`, `commit-commands:clean_gone`). It introduces no filesystem state. It verifies the **outcome** — clean tree, on a fresh base, PR merged — not merely that cleanup *ran* (Meadows' "seeking the wrong goal": a closeout measured by "did it run" optimizes the proxy and produces brittle ceremony).

## Invocation Position

This is a primary pipeline skill that owns the `merge → cleanup` tail of the default delivery path:

```
… → /pre-merge → /compound (in-PR, when a lesson exists) → /pre-merge (re-run over the compound commit; re-stamps) → [merge + worktree teardown — THIS SKILL] → [issue-closing — Step 9 prose]
```

Use `/closeout` when:

- `/pre-merge` has created a PR and the review is done (or the change is trivial enough not to need one)
- the PR is approved and mergeable, and you want it merged and the workspace returned to a clean base
- the user asks to "close out," "merge and clean up," "tear down the worktree," or "get back to a clean main/base"

Do not use `/closeout` when:

- the PR is not yet created or still under review — run `/pre-merge` first
- you want to capture a durable lesson — that is `/compound`, which by default has already ridden the PR before `/closeout` merges (post-merge `/compound` is the fallback); `/closeout` does not capture lessons
- you want to close the PRD and slice issues or reconcile the research artifact's frontmatter — that is the cleanup prose in `SYSTEM-OVERVIEW.md` Step 9; `/closeout` performs the *git-hygiene* half and defers the *issue-closing and research-artifact-supersession* half to Step 9 rather than duplicating it
- the change is not on a feature branch at all (you are on the base branch with nothing to merge) — there is nothing to close out

It is HITL-confirmed and non-blocking: it operationalizes an already-optional tail. It never auto-merges — merge is outward-facing and hard to reverse, so it always confirms first.

## Process

Run this as a do-confirm checklist (Gawande): perform each step, then verify its outcome before the next. The destructive steps (4–6) are self-guarded — confirm the safety preconditions in Step 2 hold before running them.

### 0. Host-provisioned isolation? Cede teardown first

Before the merge/teardown sequence, determine whether this repo's isolation is **host-owned** (Conductor, Codespaces, devcontainers). When it is, `/closeout` still performs the GitHub-native merge but **does not** tear down the worktree or prune the local branch — the host owns that half of the lifecycle, and fighting it is Meadows' policy-resistance (two actors pushing the same stock). Cede the worktree stock to the host.

Outflow detection is **stricter than `/execute`'s inflow check** and must *not* use the generic "toplevel ≠ primary working tree" heuristic alone: a *pipeline-made* worktree also satisfies that test, so the generic signal cannot distinguish "host owns teardown" from "the pipeline made this and must tear it down." Resolve from `.claude/settings.json` `worktree.provisioning` (default `"auto"` when absent), and honor an explicit override at this end exactly as `/execute` does at the inflow:

- **`host`** — cede teardown unconditionally.
- **`pipeline`** — the pipeline owns teardown. Run the full Steps 4–6 below *even if a host env var is present* — an explicit `pipeline` setting means `/execute` provisioned the worktree itself, so `/closeout` must tear it down (the pre-host behavior). A host env var does not override an explicit `pipeline` choice.
- **`auto`** (default) — cede teardown only if a host environment variable describes *this* tree: the block below prints `host_owned=yes`. Never cede on the generic "toplevel ≠ primary" signal alone, and never on the bare presence of `CONDUCTOR_WORKSPACE_PATH` — a shell started under Conductor inherits it and can carry one naming a different repository's workspace, and ceding on that leaves a pipeline-made worktree with no one to tear it down.

```bash
# host-signal: does a host env var describe THIS tree, not just this shell?
host_owned=no
top=$(cd "$(git rev-parse --show-toplevel)" && pwd -P)
if [ -n "${CONDUCTOR_WORKSPACE_PATH:-}" ]; then
  ws=$(cd "$CONDUCTOR_WORKSPACE_PATH" 2>/dev/null && pwd -P) || ws=
  if [ -n "$ws" ]; then
    case "$top/" in "$ws"/*) host_owned=yes ;; esac
  fi
fi
if [ -n "${CODESPACES:-}" ] || [ -n "${REMOTE_CONTAINERS:-}" ]; then host_owned=yes; fi
echo "host_owned=$host_owned"
```

If teardown is not ceded (including `worktree.provisioning: "auto"` with `host_owned=no`), the pipeline owns it — run the full Steps 4–6 below as written.

When isolation is host-owned, `/closeout` runs a reduced sequence:

- **Step 3 (merge) still runs in full** — `gh pr merge --delete-branch`. Conductor and similar hosts create the PR but leave the *merge* to a human action; the pipeline performing the GitHub-native merge is the value it adds, and the host reflects the result. The deferral is scoped to filesystem teardown, **never** the merge.
- **Skip Step 4's re-anchor, Step 5's `wt remove` / `git worktree remove` / `ExitWorktree { remove }`, and Step 6's local-branch prune** — the host owns the worktree and branch lifecycle (Conductor reclaims them when the workspace is archived). Never `--force` against a host-managed tree.
- **Step 8's checklist:** "Worktree gone" and "Branch pruned" become **"N/A — host-managed."** The merge, clean-tree, PR-merged, and **remote-branch** checks still apply. The last one is easy to file under the same N/A and is not: what the host owns is the *filesystem* worktree and the *local* branch, while the remote branch is deleted by the `gh pr merge --delete-branch` this skill still runs in full one bullet above. Ceding the half the host owns does not cede the half it does not.

### 1. Confirm intent and gather state

Never auto-merge. State what you are about to do and get an explicit go-ahead.

Gather the facts first (these are read-only):

```bash
git branch --show-current                                   # the feature branch
git rev-parse --show-toplevel                               # the current working tree (may be a worktree)
git worktree list --porcelain | awk '/^worktree /{print $2; exit}'   # the BASE checkout (main working tree)
gh pr view --json number,title,url,state,mergeable,mergeStateStatus,reviewDecision 2>/dev/null
```

Determine the base branch the PR targets — the repo's declared default, not an assumption:

```bash
git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's@^origin/@@'   # e.g. origin/main → main; origin/prod → prod
```

This site wants the base branch **name**, not a ref — it feeds `git switch <base-branch>` at Step 4, and `git switch` rejects a remote-tracking ref outright (`fatal: a branch is expected, got remote branch 'origin/prod'`) — it wants the local base branch you are about to pull. It deliberately does *not* grow the `$BASE_REF` guard that `/pre-merge`, `/help`, `/walk-commits`, `/visual-recap`, and `/compound` carry; that guard exists only because those five use the base as a **range endpoint**, which this skill never does. Do not "fix" this to match them.

Tell the user, in one short block: which PR will merge, which worktree (if any) and branch will be torn down, and which base branch you will return to and pull. Wait for confirmation. If there is no PR on this branch, stop and route to `/pre-merge`.

### 2. Verify safety preconditions before any destructive step

The teardown is destructive; verify it is safe first (self-guard). All of these must hold:

- [ ] The feature branch is fully pushed — `git status` shows no unpushed commits, and `git log @{u}..` is empty.
- [ ] A PR exists for this branch and is mergeable (`mergeable` is `MERGEABLE`; `mergeStateStatus` is not `BLOCKED`/`DIRTY`).
- [ ] Required checks are green and review is approved (`reviewDecision` is `APPROVED`, or the repo does not require review and the user has explicitly accepted).

If any precondition fails, stop and report which one — do not merge or remove anything. A failed precondition is a signal to return to review, not to force through.

**Review currency — does the approval still cover *this* diff? (non-blocking)**

The three checkboxes above ask whether a review happened. None of them asks whether it covered the diff about to merge. In the intended linear flow those are the same question, which is exactly why the gap is invisible; in a real HITL session scope accretes on a branch *after* its review pass, and nothing connects the diff `/pre-merge` read to the diff `/closeout` merges. That is an inflow with no feedback loop (Meadows — the structural fix is to add the loop, not to exhort), and it quietly degrades "the PR was reviewed" into "an early version of the PR was reviewed" at the one moment the degradation matters most. Continuous Delivery states the rule plainly: the artifact you reviewed must be the artifact you ship.

Read the stamp `/pre-merge` Phase 4 left in the PR body and compare it to the current head:

```bash
git fetch --quiet
REVIEWED_SHA=$(gh pr view <number> --json body -q .body \
  | sed -n 's/.*<!-- reviewed-at: \([0-9a-f]\{40\}\) -->.*/\1/p' | tail -1)
HEAD_SHA=$(gh pr view <number> --json headRefOid -q .headRefOid)
```

**Exactly 40 hex characters, compared by string equality.** Both halves of that sentence are load-bearing, because this marker is a contract that spans two skills. `/pre-merge` Phase 4 emits the full 40-character OID, and `headRefOid` is always 40 characters, so `\{40\}` is the only width that can ever compare equal — accepting a shorter one would let a malformed marker (a hand-edited body, a template placeholder substituted into the wrong half) parse successfully and then differ from `$HEAD_SHA` forever. `[[ "$REVIEWED_SHA" == "$HEAD_SHA" ]]` is the comparison: exact string equality on two full OIDs, never a prefix test. A marker the regex rejects yields an empty `$REVIEWED_SHA` and takes the "no stamp found" branch below, which degrades gracefully — far better than the "SHAs differ" branch crying wolf on a PR whose head never moved. In the Skill Kit repo, `scripts/test-review-currency-marker.sh` pins this round trip against both skills so the writer's format and this parser cannot drift apart silently.

Three outcomes, and only one of them interrupts:

- **The SHAs match** — string-equal full OIDs, so the reviewed diff *is* the merge candidate. Pass silently. Do not narrate it: this is the common case, and announcing a non-event every run is what turns a gate into wallpaper.
- **No stamp found** (`$REVIEWED_SHA` empty) — a hand-authored PR, an external contribution, a PR that predates the stamp, or a marker whose shape the regex above rejected. Note it in one line ("no `/pre-merge` stamp on this PR — review currency unknown") and continue. Absence of a stamp is not evidence of an unreviewed diff, and stopping on every un-stamped PR is precisely the alarm fatigue that gets a gate reflexively defeated (Meadows, *policy resistance*).
- **The SHAs differ** — two well-formed 40-character OIDs that are not string-equal, meaning commits landed after the review. Do not stop, and do not merge yet. Show the *magnitude* of what was added, so the decision is proportional to the size of the delta rather than to the bare fact of one:

  ```bash
  git diff --stat "$REVIEWED_SHA".."$HEAD_SHA"
  git log --oneline "$REVIEWED_SHA".."$HEAD_SHA"
  ```

  If `$REVIEWED_SHA` is not present locally — the branch was force-pushed and the reviewed commit was rewritten away — say so. The reviewed diff is unrecoverable, which is a *stronger* divergence signal than a measurable delta, not a weaker one.

  **Name a `docs: compound` commit for what it contains, not for its subject line.** One post-stamp commit has a standing explanation available — the `docs/solutions/` entry `/compound`'s in-PR path commits onto the branch — and that explanation is the one most likely to get the menu below clicked through. It is only ever *half* available: `/compound` Phase 5 stages Phase 4's mechanism in the same commit, so a `docs: compound` subject covers both a docs-only entry and a commit that ships code. In the measurement behind #336, four of ten past-stamp merges on one repo were compound commits and two of the four shipped code — a contract test rewritten to derive its coverage from the schema, and a new test file. Read the paths rather than the subject:

  ```bash
  git log --format='%H %s' "$REVIEWED_SHA".."$HEAD_SHA" \
    | sed -n 's/^\([0-9a-f]*\) \(docs: compound.*\)$/\1/p' \
    | while read -r sha; do
        outside=$(git show --name-only --format= "$sha" | grep -v '^docs/solutions/' || true)
        if [ -z "$outside" ]; then
          echo "$sha  docs-only /compound entry"
        else
          echo "$sha  'docs: compound' subject, but also touches:"
          printf '%s\n' "$outside" | sed 's/^/    /'
        fi
      done
  ```

  A commit the loop prints as a **docs-only `/compound` entry** is the expected post-stamp delta on the in-PR path, and saying so is worth one line — a divergence the operator cannot account for and one they can are different situations, and describing them identically is how the gate becomes wallpaper. It is still *unreviewed* unless the `/compound` handoff's `/pre-merge` re-run ran; naming it explains the delta, it does not discharge it. A commit that prints **paths outside `docs/solutions/`** is a code delta like any other and gets no discount at all: say that the subject line is misleading and show the paths, so the menu below is answered on the diff rather than on the prefix.

  Then ask once, with a single `AskUserQuestion`, recommended option first:

  - **→ Re-review the delta with `/pre-merge` (recommended)** — put the added commits through the review dimensions, then re-stamp and return here. `/pre-merge` reads this same stamp itself and takes the post-stamp delta as its subject (its Phase 1 step 4), so there is no range to pass it; it falls back to the whole branch on the force-push case above and when a merge commit landed after the stamp.
  - **Merge anyway — I've seen these commits** — an explicit acknowledgement. Repeat it in the Step 3 merge confirmation so the choice is on the record rather than implicit.
  - **Stop — I want to look at this first** — leaves the PR unmerged and the workspace untouched.

  The platform's free-text "Other" option is the escape hatch — don't add one.

This precondition **never hard-blocks**. `/closeout` is HITL and non-blocking by design, and the fix here is making the divergence *visible* — not seizing the merge decision from the user.

The git guardrail hook does hard-block, on the merge command rather than here, so that a merge which never passes through `/closeout` cannot skip this read (`/git-guardrails-claude-code` → "What Gets Blocked Conditionally"). Where it is installed, the **Merge anyway** branch above needs the opt-out named in Step 3.

### 3. Merge the PR

Merge with the repo's convention (squash is the common default; confirm if unsure). Let the merge delete the remote branch where the platform supports it, and **give the squash commit the PR body as its message**. Without `--body-file`, `gh` builds the squash message from the per-unit commit messages, so a reader who runs `git blame` months later lands on every fix-round message concatenated (bodies of 200–400 lines were measured across four repos on 2026-09-10) and never on the walkthrough `/pre-merge` Phase 2 wrote. That is also why authors put history in code comments: it was the only per-line record that survived the merge. `/execute` and `/compound` route incident history to the PR body on the promise that it lasts; this flag is what keeps the promise.

```bash
BODY_FILE=$(mktemp)
gh pr view <number> --json body -q .body > "$BODY_FILE"
gh pr merge <number> --squash --delete-branch --body-file "$BODY_FILE"   # or --merge / --rebase per repo convention
rm -f "$BODY_FILE"
```

If the guardrail hook is installed and Step 2 found a stale stamp that the user chose to accept, this command is refused — the hook reads the same stamp and does not know a human just decided. Carry the decision across explicitly:

```bash
ALLOW_STALE_STAMP_MERGE=1 gh pr merge <number> --squash --delete-branch --body-file "$BODY_FILE"
```

Only after the user picked **Merge anyway** in Step 2. Reaching for the variable because a merge was refused, without going back through Step 2, is defeating the gate rather than passing it.

Confirm the PR now reports `MERGED` before touching the worktree:

```bash
gh pr view <number> --json state -q .state       # expect: MERGED
```

**Then release the post-review edit lock.** `/pre-merge` Phase 4 wrote
`.claude/.review-stamped` beside the review-currency stamp; the classification
hook reads it and refuses implementation writes while it exists and
`.claude/.fix-findings-active` does not. Once the PR is merged that review is
spent, and a flag left behind would lock the *next* branch on the strength of
this one's review. Remove it here, while the shell is still in the checkout that
holds it — after Step 5 removes the worktree there may be nothing left to reach,
and on a plain `git checkout -b` branch, or a host-owned worktree Step 5 skips,
the flag would otherwise survive indefinitely:

```bash
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
rm -f "$PROJECT_DIR/.claude/.review-stamped"
```

`.claude/.fix-findings-active` is not removed here — `/fix-findings` removes its
own flag on every exit path, and a copy still present at merge means that run
aborted without cleaning up. Say so rather than deleting it silently; it is the
one signal that the lock has been standing open.

### 4. Re-anchor the shell to the base checkout — BEFORE removing the worktree

**This is the load-bearing step.** If the current working tree is a linked worktree, move the shell to the base checkout *now*, while the worktree still exists, so nothing is removed out from under the running shell. Pick the re-anchor mechanism that matches how the session got into the worktree:

**If this same session entered the worktree via `EnterWorktree`** — the inflow `/execute` now uses (`pwd` reports a path under `.claude/worktrees/` and `EnterWorktree` was called earlier in *this* session) — re-anchor with the matching harness tool, not a bare `cd`:

`ExitWorktree { action: "keep" }` restores the shell to the base checkout (the directory the session was in before `EnterWorktree`) and, per the tool's contract, will *not* remove a worktree entered via `path`. Use `keep`, never `remove`: the worktree's branch is what just merged, and Step 5/6 own its teardown and pruning. Removal stays in Step 5.

**Otherwise** — a fresh `/closeout` session that did not itself call `EnterWorktree`, or a plain `git checkout -b` checkout with no worktree — re-anchor with a bare `cd` (`ExitWorktree` only operates on worktrees its own session entered, so it is a no-op here):

```bash
cd "$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')"
git rev-parse --show-toplevel    # confirm cwd is now the base checkout, not the worktree
```

If Step 1 showed the current tree *is* the base checkout (you were on a plain `git checkout -b` branch, not a worktree), there is no worktree to remove — skip to switching branches:

```bash
git switch <base-branch>
```

Either way, confirm the shell is no longer inside the feature worktree before proceeding.

### 5. Remove the worktree (only if one was created — skip when isolation is host-owned, Step 0)

Now that the shell is anchored to the base checkout, removing the worktree is safe:

```bash
wt remove <worktree-or-branch>          # if worktrunk is available
# or
git worktree remove <worktree-path>     # plain git
```

If the worktree has uncommitted or untracked changes you have not accounted for, `git worktree remove` will refuse — investigate rather than forcing `--force`. (Everything reviewed in the PR is already merged; anything left behind is unexpected.)

### 6. Prune the merged branch (skip when isolation is host-owned, Step 0)

The local feature branch (and its now-`[gone]` remote-tracking ref) is dead weight after merge. Prune it:

```bash
git fetch --prune                       # drop the [gone] remote-tracking ref
git branch -d <feature-branch>           # safe delete; fails if not merged — investigate if it does
```

`commit-commands:clean_gone` removes all `[gone]` branches and their worktrees in one pass — prefer it when several stale worktrees have accumulated (the recurring symptom this skill exists to stop). Do not reimplement what it already does.

### 7. Pull the base branch

Bring the local base up to date so it reflects the merge you just made:

```bash
git pull --ff-only       # fast-forward; resolves the merge into local base
```

### 8. Verify the clean end state (outcome, not activity)

Confirm the *outcome*, not that the steps ran. All must be true:

- [ ] On the base branch — `git branch --show-current` reports the base.
- [ ] Working tree clean — `git status --short` is empty.
- [ ] PR merged — `gh pr view <number> --json state -q .state` reports `MERGED`.
- [ ] Worktree gone — the feature worktree no longer appears in `git worktree list`. (N/A — host-managed — when isolation is host-owned, Step 0.)
- [ ] Branch pruned — the feature branch no longer appears in `git branch`. (N/A — host-managed — when isolation is host-owned, Step 0.)
- [ ] Remote branch gone — the branch Step 3's `--delete-branch` was supposed to delete is not on the remote (the command below exits **2**). This one is not N/A under host-owned isolation: the host owns the filesystem worktree, `gh` owns the remote branch.

```bash
git ls-remote --exit-code --heads origin <feature-branch>   # exit 2 = confirmed gone (pass); exit 0 = still on the remote (fail); anything else = could not check
```

**Why the remote gets its own check.** Every other item above passes while the remote branch survives — Step 3 confirms the PR reports `MERGED`, Step 6 prunes the local branch and its remote-*tracking* ref, and this list's "Branch pruned" reads `git branch`, which is local. None of them asks the remote. In the field `gh pr merge --delete-branch` aborted at its local step in a multi-worktree checkout (`'main' is already used by worktree`) *after* the remote merge had succeeded: the merge reported success, the branch deletion silently did not happen, and a fully green closeout ran over the top of it. `--exit-code` is what makes found and not-found distinguishable at all here; without it the command exits 0 in both states and the check reads as permanently clean.

**Read the number, not just its sign.** `--exit-code`'s documented contract (`git-ls-remote(1)`) only names status `2`, for "no matching refs" — that is the sole status this check should read as pass. Status `0` means the branch is still there. Every other status — an unreachable remote from an expired credential, a renamed `origin`, a transient network blip — is also non-zero and would misread as "gone" under a bare non-zero check, which silently reproduces the exact failure this item exists to close, one level down. If the exit status is neither `0` nor `2`, the check did not run; treat the item as open, fix the access problem, and re-run it rather than passing it.

Report the end state in one short block. If any check fails, say which and stop — a half-clean state is exactly the failure mode this skill exists to prevent.

### 9. Hand off

- If a durable lesson emerged from this work and was **not** already captured on the PR (per the PR-attachable `/compound` model), invoke `/compound` now. If the lesson already rode the PR, say so and skip it. `/closeout` never captures lessons itself.
- Closing the PRD and any remaining slice issues, and confirming the research artifact's frontmatter still reflects what shipped (superseding with a new dated artifact if a version bumped), is the cleanup prose in `SYSTEM-OVERVIEW.md` Step 9 — name it as the remaining tail work; do not perform research-artifact supersession from here.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The PR looks fine, I'll just merge it without asking." | Merge is outward-facing and hard to reverse. `/closeout` always confirms intent first (Step 1). Auto-merge is an explicit non-goal. |
| "I'll `wt remove` first, then `cd` out of the trashed directory." | That is the exact slip this skill exists to prevent — it strands the shell inside a removed worktree and makes a `node_modules`-dependent Stop hook emit false `MODULE_NOT_FOUND` errors. Re-anchor to base *before* removing (Step 4). |
| "Verifying the steps ran is the same as verifying it worked." | Meadows' "seeking the wrong goal" — measuring activity, not outcome. Step 8 checks the actual end state: on base, clean tree, PR merged, worktree gone, branch pruned. |
| "There's a review on this PR, so the diff has been reviewed." | Only if nothing landed after it. `/pre-merge` stamps the SHA it reviewed; Step 2 compares that to the current head and shows `git diff --stat` of anything added since. A review of an earlier state is not a review of the release candidate (Continuous Delivery). |
| "I'll force the worktree removal — there's just some leftover state." | Everything reviewed is already merged; leftover state is unexpected. Investigate it rather than `--force`-ing it away. |
| "I'll close the PRD issue and refresh the research artifact while I'm here." | That is Step 9's job, not closeout's. Performing research-artifact supersession from here duplicates and risks contradicting the canonical cleanup prose. Name it as remaining work and hand off. |
| "I'll capture the lesson in `docs/solutions/` as part of closing out." | That is `/compound`. Under the PR-attachable model the lesson may already be on the PR; if it isn't, hand to `/compound` — don't fold knowledge capture into closeout. |

## Red Flags

- About to run `wt remove` / `git worktree remove` while the shell's cwd is still inside that worktree.
- Merging before confirming the PR is pushed, mergeable, and approved (skipping Step 2).
- Merging a PR whose head has moved past its `<!-- reviewed-at: … -->` stamp without ever showing the user the post-review delta.
- A Stop hook or feedback loop suddenly reporting `MODULE_NOT_FOUND` / "cannot find module" for `biome`, `tsc`, or `vitest` right after a teardown — almost always a stranded cwd, not a real failure.
- Reporting "cleanup done" without the Step 8 outcome checks actually passing.
- `git worktree list` showing several stale feature worktrees — evidence the outflow loop is being skipped; this is the symptom closeout removes.
- Closeout performing issue-closing or research-artifact supersession itself instead of deferring to Step 9.

## Verification

A run of `/closeout` is not complete until:

- the user explicitly confirmed the merge before it ran
- review currency was checked — the stamped SHA matched the merge candidate, the PR carried no stamp (noted and continued), or the post-review delta was shown and the user chose to re-review, acknowledge, or stop
- the PR reports `MERGED`
- the shell was re-anchored to the base checkout *before* the worktree was removed
- the feature worktree (if one existed) is gone from `git worktree list` and the merged branch is pruned — or, when isolation is host-owned (Step 0), teardown and pruning were correctly ceded to the host while the merge still ran
- the base branch was pulled and the working tree is clean on the base branch
- the end state was reported, and remaining tail work (`/compound` if a lesson is uncaptured, Step 9 issue-closing) was named in the handoff

## Handoff

- **Expected input:** a reviewed, mergeable PR created by `/pre-merge`, on a feature branch (in a worktree or a plain checkout)
- **Produces:** the PR merged, the worktree torn down, the merged branch pruned, the base branch pulled, and a verified clean end state — no filesystem state introduced
- **May invoke:** `/compound` when a durable lesson emerged and was not already captured on the PR
- **Comes next by default:** `/compound` (only when an uncaptured lesson is worth recording) and the `SYSTEM-OVERVIEW.md` Step 9 cleanup prose (close the PRD and slice issues, confirm research-artifact frontmatter). After that, the loop is closed — `/help` when you return to the repo.

**Next-step menu.** With the merge done and a clean base reached, offer the tail as a menu rather than leaving it to recall (see `references/next-step-menu.md`). Present a single `AskUserQuestion` with the recommended step first, each option naming its outcome rather than just its skill: **→ `/compound` (capture a lesson from this change)** when an uncaptured lesson is worth recording, **Step 9 issue-closing still to do** when a PRD or slice issues remain, **Stopping here — clean base, nothing left open**, **`/help` (pick up the next piece of work)**. The last three are distinct destinations, not one state described three ways: Step 9's cleanup prose, ending the session, and asking what to start next. Each label leads with the act that distinguishes it, not with a shared word the reader has to scan past. Name Step 9 as remaining work; do not perform it from here. The platform's free-text "Other" option is the escape hatch — don't add one.
