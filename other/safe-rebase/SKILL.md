---
name: safe-rebase
description: "Safely rebase a branch onto a new/moved base commit or branch, catching conflicts on a disposable trial run before touching real history. Use for any rebase, rebase --onto, or 'move this branch onto an updated base' request — especially when the user is worried about conflicts, force-pushing a branch with an open PR, or losing work."
compatibility: "Requires: git, bash (Git Bash on Windows)"
disable-model-invocation: false
license: "MIT"
metadata:
  author: "Balagurunathan Marimuthu"
  version: "1.0.0"
  improvements: "Initial version: trial-rebase-first workflow, hunk-by-hunk conflict resolution guidance, git rebase --abort vs. undo (PRE_REBASE_TIP) distinction, force-with-lease push gated on explicit confirmation, Mermaid + plain-list workflow references."
---

# Safe Rebase

## Why this exists

`git rebase --onto` is one of the few git operations that's genuinely dangerous: it rewrites commit history, and if the branch is already pushed and has an open PR, a naive `git push --force` can clobber someone else's work or blow away the PR's review state. The core risk isn't "will there be conflicts" — it's finding that out *after* you've already rewritten the real branch, with no easy way back.

The fix is cheap: rehearse the rebase on a disposable branch first. If it's clean, you've paid almost nothing and now know the real rebase will be clean too. If it conflicts, you've learned that without touching anything real, and the user can decide how to handle it with a clear head instead of being dropped into a live conflict mid-operation.

## Inputs

You need three things, but usually only have to ask for one:

- **working branch** — the branch being moved (often the branch currently checked out; confirm with `git branch --show-current` rather than assuming).
- **new base** — the branch or commit the work should now sit on top of (e.g. the target branch's new tip after it moved forward).
- **old base** — the commit where `working branch` originally diverged; this is the cut point for `--onto`. **Don't ask the user for this hash.** It's almost always `git merge-base <working-branch> <new-base>` — the last commit the two branches had in common before they diverged. Only fall back to asking the user if merge-base gives a nonsensical result (e.g. the tip of one of the branches, which usually means they've already diverged from a completely different point than expected).

## Workflow at a glance

Every path either ends in a clean state matching what the user asked for, or back at exactly the commit they started from — never stuck somewhere in between without the user having chosen to be there. A rendered Mermaid version of this flow lives at `references/workflow-diagram.md` — reach for it when a picture is more useful than text (e.g. showing someone else); the list below is what actually matters for following the flow, since it stays readable regardless of terminal width or word wrap.

1. **Trial** the rebase on a disposable branch (real branch untouched).
   - **Clean** → go to 2.
   - **Conflict** → report the conflicting files, then let the user choose:
     - **Hold off** → stop here, nothing touched.
     - **Resolve for real** → go to 2.
2. **Confirm** the plan with the user, then **apply** on the real branch (this records `PRE_REBASE_TIP` before doing anything).
   - **Conflict mid-apply** → resolve hunk by hunk (per commit):
     - Commit resolved → `git add`, `git rebase --continue`, repeat until no commits remain → go to 3.
     - User wants to stop → `git rebase --abort` (a *complete* revert to `PRE_REBASE_TIP`; see **Backing out**, below).
   - **Clean, or all commits resolved** → go to 3.
3. Check whether the branch **tracks an upstream**.
   - **No** → done, local only.
   - **Yes** → confirm push with the user (mention PR/CI impact):
     - **Decline / not yet** → stop; branch stays as rebased, `undo` is still available.
     - **Confirmed** → `push --force-with-lease` → done, remote/PR updated (the `undo` safety net is gone from here on).

### Backing out

Two distinct "give me back where I started" mechanisms, for two distinct moments — don't confuse them:

- **Mid-rebase, any commit conflicts** → `git rebase --abort`. This is always a *complete* revert to the branch's state before this rebase began (`PRE_REBASE_TIP`), regardless of how many commits already replayed successfully in this pass. Git has no "keep the ones that worked" abort — it's all-or-nothing by design, since nothing in a rebase-in-progress is real history yet. If the user wants to preserve conflict-resolution work done on earlier commits in the same rebase, abort is not the tool for that — only continuing (or accepting the loss) is.
- **Rebase finished, not yet pushed** → no rebase is in progress anymore, so `--abort` no longer applies. Use `scripts/safe_rebase.sh undo <working-branch> <PRE_REBASE_TIP>` instead — it hard-resets the branch back to the exact commit `apply` recorded before touching it. This window closes the moment you push: after that, the safety net is gone by design (pushing *is* the real point of no return here, not the local rebase) — say so plainly before pushing.

`git rebase --skip` is a different tool, not a synonym for either of the above — it drops the current commit and keeps going, which changes what ends up in history. Only reach for it if the user explicitly decides that commit's change should be dropped, not as a shortcut past a conflict you're unsure how to resolve.

Use `scripts/safe_rebase.sh` for every scripted step below — it's already written and tested to handle the branch bookkeeping (creating/deleting the disposable branch, restoring your original checkout, aborting cleanly on conflict, capturing `PRE_REBASE_TIP`). Don't hand-roll the equivalent bash; the script exists so this doesn't have to be re-derived and re-tested every time. Conflict *resolution* itself (deciding what a hunk should become) has no script — that step needs judgment, covered below.

### 1. Trial the rebase on a disposable branch

```
bash scripts/safe_rebase.sh trial <working-branch> <new-base> [old-base]
```

This creates a throwaway branch, attempts the real rebase on it, reports the result, and cleans up completely (deletes the trial branch, checks you back out onto whatever branch you started on) regardless of outcome. Nothing about the real branch or working tree changes.

Report the output plainly:
- The commits that will be replayed (`COMMITS_TO_REPLAY`).
- `STATUS=clean` — no conflicts, safe to proceed to step 2.
- `STATUS=conflict` — list the `CONFLICTING_FILES`. Do **not** proceed to step 2 automatically. Tell the user which files conflict, and offer the real choice: resolve it for real now (step 2 handles this — the real rebase is where resolution actually happens, since the trial branch is already gone), adjust the target, or hold off entirely. A conflict found here is strictly better than the same conflict found on the real branch with no warning — say so if it's useful context, but don't minimize it.

### 2. Confirm, then apply on the real branch

Rewriting history is hard to reverse and, per your operating rules, warrants explicit confirmation regardless of how confident the trial was — this holds whether the trial was clean or conflicted (a conflicted trial means you're now asking "do you want to resolve this for real", which is a bigger ask, not a smaller one). State the plan plainly (which branch, old base → new base, how many commits) and wait for a clear go-ahead before running:

```
bash scripts/safe_rebase.sh apply <working-branch> <new-base> [old-base]
```

This prints `PRE_REBASE_TIP` before doing anything else — hold onto that value. It's the exact commit to fall back to if the user wants everything undone later (see **Backing out**, above), and it stays valid until the branch is pushed.

**If this real rebase conflicts** (whether or not the trial already warned you), resolve it commit by commit rather than reaching for a blanket strategy:

1. For the commit currently blocked, look at what *it* was trying to do — its message and diff — and what the conflicting change on the new base side was trying to do. `git diff` shows both sides' hunks inline with conflict markers; read them as two competing intents, not just two blocks of text.
2. Resolve hunk by hunk based on that intent. Don't run `git checkout --ours <file>` or `--theirs <file>` as a blanket resolution for the whole file — a single file can easily contain one hunk that's a real, meaningful fix next to other hunks that are purely cosmetic (renames, reformatting), and a blanket pick silently drops whichever side loses, fix included. If a hunk carries a comment explaining why a line changed, that's often the tell for which side is the deliberate fix.
3. If a hunk's correct resolution genuinely isn't inferable from the diffs and messages — both sides look like legitimate, conflicting intent — stop and ask the user rather than guessing. This is a judgment call precisely because it's context-dependent per conflict; don't force a mechanical rule onto it.
4. Once a commit's conflicts are resolved, `git add` the resolved files and `git rebase --continue`. Repeat from step 1 for the next conflicting commit, if any.
5. At every pause, the user can also choose to stop instead of resolving — `git rebase --abort` reverts the whole attempt back to `PRE_REBASE_TIP` (see **Backing out**), no partial state survives. Offer this plainly rather than assuming they want to push through.

### 3. Ask about pushing — don't assume

The rebase finished locally — the branch is in its new shape now, but nothing is final yet. It's still fair game to mention that `undo <working-branch> PRE_REBASE_TIP` can put it back exactly as it was, right up until the moment it's pushed; some users will want to eyeball the result (build, test, review the diff) before deciding whether to keep it.

After a successful local rebase, check whether the branch even has anything to push:

```
bash scripts/safe_rebase.sh tracks <working-branch>
```

- `TRACKS=no` — nothing is pushed anywhere; there's no PR to worry about. Skip the push step entirely, mention the rebase is done locally, and stop.
- `TRACKS=yes` — ask the user to confirm before pushing. If the branch has   an open PR (common — ask if unsure, or check if you have a way to), say so explicitly: force-pushing will update the PR's diff and likely re-trigger any review tooling (CodeRabbit, CI, etc.), which may be exactly the point or may be a surprise worth flagging. Only after explicit confirmation:

```
bash scripts/safe_rebase.sh push <working-branch> [remote]
```

This always uses `--force-with-lease`, never a bare `--force` — it fails safely if someone else pushed to the remote branch since you last fetched, rather than silently overwriting their work.

## Talking to the user about this

Keep the report concrete and skip jargon-as-ceremony: "trial rebase onto `origin/main`'s tip was clean — 9 commits replay with no conflicts" beats narrating the mechanics of `--onto`. If a conflict shows up in the trial, name the files and let the user steer rather than presenting a wall of `<<<<<<<` markers. If the user seems less git-fluent, "the branch this was built on has moved forward, so we need to move your commits on top of the new version" works better than "rebase the topology onto the updated ancestor."
