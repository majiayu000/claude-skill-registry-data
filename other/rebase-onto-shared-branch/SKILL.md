---
name: rebase-onto-shared-branch
description: "Use when rebasing onto a shared/team branch someone else pushed overlapping work to, or rebasing a branch you are not on without switching the checkout (e.g. handball1: full checkouts too slow). Also when git replay exits 1 with no output, a conflict must keep both sides, or a rebase must be proven to have dropped nothing before pushing."
---

# Rebase onto a shared branch that moved underneath you

Use when someone pushed to the branch you rebase onto (`<target>`, e.g.
`origin/<integration>`) and your commits touch nearby code, whether or not you are on the
branch being rebased (`<branch>`). The goal is not a clean rebase - it is a *correct* one,
proven per hunk and by running the merged code.

## 1. See what actually landed, before touching anything

```bash
git fetch --all --prune
git log --oneline <target> ^<branch> | head -30   # what they added
git log --oneline <branch> ^<target>              # what you owe
```

For any commit that sounds like it overlaps your work, read the **diffstat and the
diff**, not the subject line. A subject like "containerise X so a cluster can scale it"
can turn out to be 49 additive lines that touch none of your files - or a genuine parallel
implementation. Decide which from the diff.

## 2. Predict conflicts with set intersection

Only files changed on *both* sides can conflict:

```python
ours   = set(sh('git diff --name-only <target>...<branch>').split())
theirs = set(sh('git diff --name-only <branch>...<target>').split())
print(sorted(ours & theirs))   # the only files that can conflict
```

- Never predict with a log-count loop. Wrapped git (rtk, aliases, anything that decorates
  output) breaks `| wc -l` counting: every file appears to have >=1 commit, including
  files that only exist locally.
- The shell form, `comm -12 <(git diff --name-only <target>...<branch> | sort) <(git diff
  --name-only <branch>...<target> | sort)`, hits a trap on this Windows box: `sort` pins
  its temp dir to `G:/tmp` (nonexistent) regardless of `$TEMP`. Prefix
  `TMPDIR=<existing dir>`. `/tmp` does not resolve either - write scratch files into a
  repo-local dir you delete after.
- Sanity check: a file you created this session appearing in the overlap means the
  detection is wrong, not that they invented the same file.

## 3. Safety net, then rebase

```bash
git branch backup/<name>-preRebase <branch>
```

**On the branch:** `git rebase <target>`. Unstaged noise blocks the rebase. Before
discarding it, check what it is: a file showing as modified with an *empty* diff is
line-ending churn (`git stash push` on it reports `Empty stash`), not your edit.

**Not on it, and the caller's checkout must not move** (or a full checkout is too slow to
build): rebase in a temporary sparse worktree. The branch ref ends up replayed on top of
the target while the caller's working tree stays exactly where it was.

```bash
git worktree add --no-checkout /path/wt <branch>
cd /path/wt
git sparse-checkout set <dirs containing the overlap files>
git checkout
git rebase <target>
```

- Sparse is what makes this cheap. On handball1 (95k files, 1.4 GiB) the sparse checkout
  took ~1 second; a **full checkout took >30 minutes and timed out**.
- Rebase still replays commits touching files outside the sparse set - git updates those
  index entries without materialising them. Conflicted files are materialised
  automatically.
- Afterwards: `git worktree remove --force /path/wt` (seconds when sparse), then
  `git worktree prune`. The branch ref keeps the rebase; only the checkout is discarded.
- Do not reach for `git replay --onto <target> <target>..<branch>`. It looks perfect (no
  worktree, prints `update-ref` lines), but on any conflict it exits **1 with no output
  at all** - silent, in under a second, indistinguishable from "nothing to do" (git
  2.54's docs: no stderr output on conflicts, exit status 1). Try it once at most; on
  exit 1 go straight to the worktree. Never pipe it through `tee`/`tail` and read `ok` as
  success - that `ok` is rtk's own output.

## 4. Resolve by intent, keeping both sides where they are additive

During a rebase, `HEAD`/"ours" is **upstream** and "theirs" is **your commit** - the
reverse of what people expect. Read both sides' comments to learn what each protects. A
guard upstream added (`InTransaction ? null : ...`) plus a change you made (log level,
message) are usually *both* wanted; taking either side wholesale silently reverts the
other's fix. After resolving, re-read the merged region to confirm both intents survived.

To amend a mid-rebase commit non-interactively:

```bash
GIT_SEQUENCE_EDITOR="sed -i 's/^pick <sha>/edit <sha>/'" GIT_EDITOR=true git rebase -i <target>
# edit files
git add -A && GIT_EDITOR=true git commit --amend --no-edit
GIT_EDITOR=true git rebase --continue
```

Only worth it for real defects - replaying 30 commits to restore a blank line is not one.

## 5. Prove the replay, per hunk

1. `git range-diff <oldbase>..<backup> <newbase>..<branch>` - expect `=` on every commit
   except the ones you resolved. A missing or `!`-marked commit you did not touch is a
   dropped/altered commit.
2. `git merge-base <target> <branch>` == `git rev-parse <target>`, and
   `git rev-list --count <branch>..<target>` == 0.
3. Removals audit - for each overlap file, list only `-` lines of
   `git diff <target> <branch> -- <file>`. Every removed upstream line must trace to a
   *deliberate* branch edit: prove it with `git log -S<symbol> <target> ^<mergebase>`
   (empty ⇒ upstream never touched it since the base, so the branch owns the removal)
   and `git merge-base --is-ancestor <adding-commit> <mergebase>`.
4. Upstream-hunk survival - for each target commit landed after the base that touched an
   overlap file: `git diff C^ C -- <files> | git apply --reverse --check`.
   **A failure here is usually a false positive**: the branch edited nearby lines, so
   context drifted. Confirm by grepping the rebased file for the commit's added lines
   before claiming anything was lost.
5. Stranded references - if the branch deleted a subsystem, grep the *rebased tree* for
   its symbols (`git grep -n <symbol> <branch> -- src`) to prove no upstream caller now
   dangles, and that any upstream consumer still has its producer.
6. `git grep -c -e '^<<<<<<< ' --or -e '^>>>>>>> ' <branch> -- src` ⇒ no markers.
7. Generated project files (`.vcxproj`): parse the XML and assert no duplicate
   `Include=` values - auto-merge duplicates entries silently.

## 6. Prove it runs, don't just build it

A clean rebase proves textual merge only. Build every project that touches the conflicted
files, then exercise the merged path for real:

- Rebuild the running service (Aspire `rebuild` resource command, or restart the host).
- Drive traffic that hits the specific merged branch - for a DAL conflict-handling path, a
  load run that produces conflicts; assert zero failures rather than "it started".
- If the teammate's work has its own build path (a Dockerfile, another RID), verify
  **your** change still satisfies it: e.g. `dotnet publish -r linux-x64` when they
  containerised a project you added a Windows-only package to.

A compile is the only proof of a C++ merge, but if the cold checkout alone exceeds the
timeout (the handball1 case), the build path is disproven, not merely slow. Report
"textually verified, not compile-verified" with the step 5 evidence rather than fixing
someone else's build environment for a rebase request.

## 7. Report before pushing

State: base commit, new tip vs backup tip and the backup branch name, commits replayed,
each conflict and why its resolution keeps both intents, the per-hunk survival results,
every build result and the runtime evidence, what was *not* verified, and the remote
divergence. A rebased branch needs a lease pinned to its old remote SHA
(`--force-with-lease=<branch>:<old-remote-sha>`; git 2.54's docs call the bare form
experimental, and a background fetch defeats it) - never push unasked.

Flag documentation drift where two docs now describe the same capability differently -
that is how one of them gets deleted later by someone who only read the other.
