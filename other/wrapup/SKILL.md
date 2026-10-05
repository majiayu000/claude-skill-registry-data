---
name: wrapup
description: Close out a feature worktree once its PR has merged — confirm the merge, verify the deploy where one applies, remove the worktree, and clean up branches; with --abandon, tear down a killed feature after showing exactly what is being discarded. Requires a merged PR or an explicit --abandon — a session ending while work is still in flight is your session-close workflow, and unfinished work someone must resume is the handoff skill. Triggers on "/wrapup", "the PR merged, tidy up", "clean up this worktree", "abandon this feature".
---

# Wrap up a feature worktree

Two modes. Default: after the PR merges. `--abandon`: the feature is dead
and its work is being discarded on purpose. Every guard below exists to
avoid deleting work *unintentionally*.

Constant: `$MAIN` — the primary checkout the worktree is attached to.
Resolve it from git, never assume a path:

```bash
MAIN=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
```

If the common dir is itself a bare repository (a `repo.git` hub with every
checkout as a worktree), use it directly as `$MAIN` and take step 4's fetch
path — there is no checkout to pull.

Forge commands here assume a GitHub remote and the `gh` CLI — translate
them for another forge. A cold session that doesn't know the PR number
recovers it with `gh pr list --head <branch>`.

## Not this skill

| Situation | Use instead |
| --- | --- |
| Session ending, feature still in flight | Your session-close workflow |
| Unfinished work another session must resume | The `handoff` skill |
| Mid-work branch or stack sync | Your git tooling — no teardown involved |

A bare "wrap up" does not distinguish teardown from ending a session.
Route on evidence, not the phrase: no merged PR in the conversation and
no `--abandon` means this is not wrapup. When it stays ambiguous, ask —
the wrong guess here spends a teardown on a live feature.

## Ownership guard (both modes, before anything else)

Not every worktree holds your own branch — picking up a colleague's
branch for a review or a stacked pass is normal. Resolve ownership from
the worktree and the forge, not from the conversation:

```bash
gh pr view <number> --json author,headRefName,baseRefName
gh api user --jq '.login'
```

A PR authored by someone else, a branch that does not follow your own
naming, or a marker your bootstrap workflow left recording that this
worktree tracks a colleague's branch means **the remote side is someone
else's**. Teardown is then limited to `git worktree remove` and the
local `branch -D`. Never `gh pr close`, never
`git push origin --delete` — those target a colleague's live PR and
their branch. Say in the report which parts were skipped and why.

`--abandon` is the dangerous combination there: work pushed to their
branch is already out of your control, so the only thing left to
discard is theirs. Confirm the mode before running it.

## Process (default — merged)

1. **Confirm the merge.** `gh pr view <number> --json state,mergedAt`.
   Not `MERGED` → report and stop; nothing below is safe. (Feature
   dropped rather than merged → that's `--abandon`, not a bypass.)

2. **Deploy check (when the merge ships a deployable service).** Confirm
   the deployed build actually contains the merge before declaring it
   done — compare whatever build identifier the service exposes (a
   version endpoint, release tag, or deploy dashboard) against the merge
   commit, and treat "the PR merged" as evidence of nothing by itself.
   Skip only when nothing deploys from this change.

3. **Guard the worktree.** Before removing, from the worktree: working
   tree clean (`git status --porcelain` empty) and no local commits
   ahead (`git log --oneline origin/<branch>..HEAD` empty). Gate the
   second check on `git rev-parse --verify --quiet origin/<branch>` —
   no origin ref (never pushed, or pruned after the merge) means that
   range is meaningless; compare against the merge-base with the
   default branch instead:
   `git log --oneline "$(git merge-base origin/<default-branch> HEAD)"..HEAD`.
   Either non-empty → surface what's there and stop; never `--force`
   the removal.

   Both checks can pass on a worktree that still refuses to delete.
   `git worktree remove` deregisters first and deletes second, so a
   failure ("Directory not empty") strands a directory git no longer
   tracks. Two causes, neither visible to `status`:

   - **Live processes rooted in the worktree**:
     `ps -eo pid,comm,args | grep -F "<worktree-path>" | grep -v grep`.
     Dev servers, file watchers, and language servers race the
     recursive delete. Discount matches that merely *mention* the path
     in their arguments — a global daemon that once took the path as an
     argument is a standing false positive; confirm a real holder with
     `lsof -a -d cwd -p <pid>`.
   - **Gitignored build artefacts** (dependency dirs, caches):
     `git status --porcelain` never reports them;
     `git status --porcelain --ignored` does.

   A manual wrapup invocation pre-authorises stopping this worktree's
   own per-worktree dev services — the user invokes it on finished,
   merged work. Stop them directly and name them in the report. That
   authority is scoped to services rooted in the worktree being torn
   down, on a manual invocation. Reached any other way (chained from
   another skill, an autonomous loop), or for any process that is not
   part of this worktree's services: report the holder, hand the user
   the paste-ready line, and wait.

   Holders this session spawned itself (helper binaries, children of a
   finished sub-task) are yours to kill once their work is done.
   Recover a half-failed removal with `rm -rf "$WT"` then
   `git -C "$MAIN" worktree prune`.

4. **Sync trunk.** If `$MAIN` has the default branch checked out:
   `git -C "$MAIN" pull --ff-only origin <default-branch>`. Anything
   else checked out → update the ref without touching the checkout:
   `git -C "$MAIN" fetch origin <default-branch>:<default-branch>`.
   Always name the refspec — on a large remote a bare fetch pulls
   every ref and can hang for minutes. Failure is a warning, not a
   stop; teardown does not depend on it.

5. **Remove — or arm the reaper if this session lives inside the
   worktree.** Resolve the path from git, not from convention —
   worktrees live wherever they were created:

   ```bash
   WT=$(git -C "$MAIN" worktree list --porcelain \
     | awk -v b="branch refs/heads/<branch>" \
       '/^worktree /{p=substr($0,10)} $0==b{print p}')
   # substr, not $2: a worktree path containing spaces must survive intact —
   # everything below hands $WT to remove/rm commands.
   [ -n "$WT" ] || { echo "no worktree found for <branch>"; exit 1; }
   ```

   An empty `$WT` means no worktree holds the branch — stop and report;
   never feed an empty path to the removal commands below.

   Session outside the worktree → remove directly:

   ```bash
   git -C "$MAIN" worktree remove "$WT"
   git -C "$MAIN" branch -D <branch>   # -D: squash merges break ancestry
   ```

   Delete the branch with plain git. If you use stacked-branch tooling,
   keep its sync commands out of teardown — they typically restack
   every tracked branch in the repo, far beyond this cleanup's scope.

   Session inside the worktree (cwd under it) → removing your own cwd
   breaks every later command, so write a marker and hand the deletion
   to a detached reaper: it waits for this session's process to exit,
   then removes worktree and branch on its own.

   ```bash
   SESSION_PID=$PPID               # the harness process — the tool's own shell is ephemeral
   ps -p "$SESSION_PID" -o comm=   # must name your agent-harness binary, not a shell
   BRANCH=<branch>
   MARKER_DIR="$(git -C "$MAIN" rev-parse --path-format=absolute --git-common-dir)/pending-cleanup"
   mkdir -p "$MARKER_DIR"
   MARKER="$MARKER_DIR/${BRANCH//\//-}-$(printf %s "$BRANCH" | shasum -a 256 | cut -c1-8)"
   # hash suffix: slash-to-dash mangling alone lets a/b-c and a-b/c collide
   MODE_LINE="guards=passed"
   printf 'branch=%s\npid=%s\n%s\n' "$BRANCH" "$SESSION_PID" "$MODE_LINE" > "$MARKER"
   (nohup bash -c '
     PID=$1 MAIN=$2 WT=$3 BRANCH=$4 MARKER=$5
     cd "$MAIN" || exit 1   # cwd is the worktree being deleted — leave it first
     LOG="$MARKER.log"
     kill -0 "$PID" 2>/dev/null || { echo "dead pid at spawn; never reap" >>"$LOG"; exit 1; }
     while kill -0 "$PID" 2>/dev/null; do sleep 15; done
     sleep 5
     FORCE=""; grep -q "^mode=abandon$" "$MARKER" 2>/dev/null && FORCE="--force"
     for attempt in 1 2 3; do
       if git -C "$MAIN" worktree remove $FORCE "$WT" >>"$LOG" 2>&1; then
         if git -C "$MAIN" branch -D "$BRANCH" >>"$LOG" 2>&1; then
           rm -f "$MARKER" "$LOG"
         else
           echo "worktree removed but branch $BRANCH survived" >>"$LOG"
         fi
         exit 0
       fi
       sleep 5
     done
     echo "gave up after 3 attempts; worktree left in place" >>"$LOG"
   ' _ "$SESSION_PID" "$MAIN" "$WT" "$BRANCH" "$MARKER" \
     >/dev/null 2>&1 &)   # subshell double-fork — macOS has no setsid
   ```

   The `ps` check is a precondition, not decoration: if it names
   anything other than your harness binary the pid is wrong, and the
   reaper would delete the worktree seconds from now instead of after
   the session ends. Don't arm it — report manual cleanup instead. The
   marker doubles as the breadcrumb if the reaper dies (reboot, crash):
   sweep `pending-cleanup/` at your next bootstrap, or clean up by hand.

6. **Close the ledger.** If you keep a workstream log or running memory
   for this feature, write its final state — outcome, merged PR,
   lessons worth keeping — and stop treating it as live.

7. **Report** the teardown as it actually happened: PR merged (+ deploy
   status if checked), and "worktree removed, branch `<name>` deleted"
   only if those commands ran and succeeded — otherwise "reaper armed —
   cleanup runs itself when this session closes", or what still holds
   the worktree and the line the user needs to run. Never report a
   branch cleaned on the strength of having run a sync command.

## Process (--abandon — feature killed)

Discards work by design, so the guards invert: instead of refusing on
dirty/ahead state, show it and make the user own the loss.

1. **Show what's being discarded**, all three, even when empty:
   `git status --porcelain` (uncommitted),
   `git log --oneline origin/<branch>..HEAD` (unpushed),
   `git diff origin/<default-branch>...HEAD --stat` (the branch's whole
   delta vs trunk).

   Gate the unpushed check on
   `git rev-parse --verify --quiet origin/<branch>`. No origin ref here
   means the entire branch is unpushed and will be lost — say so, and
   list it with
   `git log --oneline "$(git merge-base origin/<default-branch> HEAD)"..HEAD`.

2. **Explicit confirmation (hard stop).** Present the summary and wait
   for an unambiguous yes to "permanently discard this". Never proceed
   on the original "--abandon" alone — the user asked before seeing the
   inventory.

3. **Close the PR** if one is open **and it is yours** (§ Ownership
   guard): `gh pr close <number> --comment "Abandoned."` — an open PR
   for a deleted branch confuses reverts and incident response. Someone
   else's PR is never closed here; report it as left open.

4. **Tear down.** Resolve `$WT` per default step 5.

   Session outside the worktree:

   ```bash
   git -C "$MAIN" worktree remove --force "$WT"
   git -C "$MAIN" branch -D <branch>
   git push origin --delete <branch>   # only if the branch was pushed
   ```

   The remote delete is the line the ownership guard forbids on a
   colleague's branch. Drop it there; the first two still run.

   Session inside it → set `MODE_LINE="mode=abandon"` and run default
   step 5's block otherwise unchanged. The reaper gates `--force` on
   that literal line, and an abandoned worktree is dirty by definition,
   so with `guards=passed` every removal attempt fails and the worktree
   strands while the report claims cleanup is under way. The two lines
   are mutually exclusive — this mode never writes `guards=passed`.

5. **Report**: what was discarded (commit count + diffstat), PR closed
   (if any), worktree and branches removed. If you keep a workstream
   log, record why the feature died and whether that was knowable
   earlier — the one lesson this mode reliably produces.
