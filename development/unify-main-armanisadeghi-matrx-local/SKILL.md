---
name: unify-main
description: The standing order for local git state in every AI Matrx repo — zero worktrees, zero local branches, zero dirty files, zero open PRs, everything merged to origin/main, and no code ever lost. Use when you find a worktree, a local branch, a stale checkout, an unpushed commit, or a dirty tree in any repo under /Users/armanisadeghi/code, when asked to "clean up", "unify", "merge everything", or when you are tempted to create a worktree or branch. Works without any access to Arman.
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/unify-main/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# unify-main — one tree, one branch, nothing lost

Arman, 2026-09-20: *"There is no reason for ever having a worktree. Updates should always be made to the single source of truth that is pushed live every 30 minutes or less. Everyone sees the same thing. Branches are ok for remote but not for local. They're forbidden."* Two full days of programming were lost when one release was missed and worktrees piled up. This skill exists so that never happens again, and so an agent with no way to reach Arman still knows exactly what to do.

## The end state, every repo, always

| Thing | Must be |
|---|---|
| Worktrees (`git worktree list`) | exactly one — the checkout itself |
| Local branches (`git branch`) | exactly one — `main` |
| Dirty files (`git status --porcelain`) | none |
| Open PRs (`gh pr list`) | none |
| `HEAD` vs `origin/main` | equal |
| Code | **none lost, ever** |

Never create a worktree. Never `git checkout -b`. Never `git stash`. Never `reset --hard`, never force-push. To protect a live feature while you rebuild it, build the replacement **beside it in the same tree** and swap when ready.

## How to decide what to do with something that is not on main

For every worktree, local branch, or dirty file set holding work that `origin/main` does not have, run these three options **in order**. Stop at the first that applies.

**Option 1 — find the owner.** Dispatch a `quick` (Sonnet) subagent to find the conversation that made it: `grep -rl "<worktree or branch name>" ~/.claude/projects/*/*.jsonl`, `~/.codex/sessions/**`, `~/.cursor`, and `git log -1 --format='%an %ae %ci'`. If the session is alive (transcript modified in the last 2 hours) and you can message it, tell it once, plainly: "your work on X is not on main; merge it to main and delete the worktree/branch now." If you cannot message it, go to Option 2.

**Option 2 — judge the code, then ship it.** Read the actual diff (`git diff origin/main...<ref>`) and write down: the feature (one line), the time of the last update (`git log -1 --format=%ci`), and whether it is **destructive** (drops or truncates tables or columns, deletes user data, removes a live route/tool/migration, rewrites others' files wholesale) or **obviously bad** (half-written, failing its own tests, contradicts a law in CLAUDE.md). If it is **not destructive, not obviously bad, and will not break the whole app**: merge it to main, delete the worktree/branch, and have a `standard` subagent verify (run the touched tests, boot if it is server code). **Regardless of the verification result, it ships** — a finding is a fixer's job, never a reason to hold code outside main. Record what you shipped and the verdict in the repo's `FOUND_DEFECTS.md` only if the verifier found something.

**Option 3 — escalate with specifics.** Only if the code IS destructive, obviously bad, or would break the whole app. Write the feature, the last-update time, and exactly why (which statement, which table, which route) onto the Question Desk via the `ask-arman` skill and, if Arman is reachable, tell him in plain English. Do not delete it. Do not leave it as a worktree either: move it onto a **remote** branch (`git push origin <sha>:refs/heads/hold/<name>`), record that branch name in the question, then delete the local worktree/branch.

The default is Option 2. "I could not find the owner" is never a reason to keep a worktree.

## Mechanics — merging without touching the working folder

The shared checkout is dirty by nature (many agents write to it). Never let that stop a merge. Work in git's database:

```bash
git fetch origin main
BASE=$(git rev-parse origin/main)   # PIN IT. Other sessions fetch constantly and move
                                    # origin/main under you; every step below uses $BASE,
                                    # never the moving name, or the commit silently carries
                                    # an older tree forward (13 files reverted, 2026-09-20).
T=$(git merge-tree --write-tree "$BASE" <ref>)             # exit 1 = real conflict
C=$(git commit-tree "$T" -p "$BASE" -p <ref> -m "Merge <name> into main")
git push origin "${C}:refs/heads/main"                     # rejected = main moved: fetch, re-pin, redo (up to 5×)
```

**Brace every variable that is followed by a colon** — `"${C}:refs/heads/main"`, `"${BASE}:path/to/file"`. The shells here are zsh, where `$C:refs` is a modifier (`:r` strips a suffix, `:s` aborts the whole command with `bad substitution`): two pushes silently went to a mangled ref on 2026-09-20.

A real conflict (`merge-tree` exits 1) is resolved by hand: `git merge-tree --write-tree` prints the conflicted paths; resolve each blob (`git show <side>:<path>`), write the resolution with `git hash-object -w`, put it in a temporary index (`GIT_INDEX_FILE=$(mktemp)`; `git read-tree $T`; `git update-index --cacheinfo`), `git write-tree`, `commit-tree`, push. Keep both sides' intent; when two agents changed the same line, the newer commit wins unless it is obviously wrong.

A single commit onto main (e.g. a dirty file set): pin `BASE` the same way → `git hash-object -w <file>` → temp index from `$BASE` (`GIT_INDEX_FILE=$(mktemp -u) git read-tree "$BASE"`) → `update-index --add --cacheinfo` → `write-tree` → `commit-tree -p "$BASE"` → push. After every push, `git diff --stat "$BASE" "$C" --diff-filter=D` must list only deletions you intended: an unexpected deletion means you carried a stale tree.

## Dirty files in the shared checkout

A dirty tracked file is somebody's edit, and it goes live as it is. It is never discarded and never stashed. Procedure: run `./ship.sh` in that repo — it commits every uncommitted file, merges GitHub and pushes (Arman's design: `policies/shared-checkout.md`, never a risk to report or an owner to chase). Where a repo has no `ship.sh`, commit the set to main by pathspec with a message naming the files as "recovered uncommitted work", verify, push. Untracked files that are not ignored: same. Generated junk (`.venv`, `node_modules`, `__pycache__`, build output) is ignored, not committed. After the commits land, `git merge --ff-only origin/main` in the checkout; if it refuses because another dirty file overlaps, that file is the next one to handle — loop until clean.

A merge in progress (`.git/MERGE_HEAD` exists) belongs to someone else: do not touch that repo's working folder until it is gone.

## Order of work in a repo

1. `git fetch origin main`; list worktrees, branches, dirty files, PRs.
2. Worktrees and branches with **zero** unpushed commits and **zero** real edits: delete now (`git worktree remove --force`, `git branch -D`, `git worktree prune`).
3. Every remaining ref with unpushed commits: Options 1→2→3. Duplicate branches carrying the same commits: merge one, delete all.
4. Dirty files: the procedure above.
5. Open PRs: merge if green and not destructive (Option 2), otherwise close with a comment saying where the work went.
6. Catch the checkout up: `git merge --ff-only origin/main`. If it cannot fast-forward because of local commits, merge them to main first (mechanics above), then fast-forward.
7. Prove it: the table at the top, all zeros, and `git rev-parse HEAD` == `git rev-parse origin/main`. Report that table, one row per repo.

## Report shape

One table: repo · what was on the ref · feature · last update · option taken · verification verdict · commit on main. No prose beyond one line per row.
