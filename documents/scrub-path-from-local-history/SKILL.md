---
name: scrub-path-from-local-history
description: "Use when a file or directory committed by mistake (a spike, an orphaned tool, a leaked file) must vanish from local commits that are unpushed or pushed only to your own branch, so history reads as if it never existed rather than deleting it going forward."
---

# Scrub a path from local history

Use when work committed locally (not pushed, or pushed only to a personal branch) added something that should never have existed - a spike, an orphaned tool, a leaked file - and the ask is "make it look like it never existed" rather than "delete it going forward".

Safe only for **unpushed or personally-owned** branches. A shared branch needs the team's agreement first, because everyone building on it must reset.

If the branch was pushed and the path held a secret, or GitHub must show no trace of the rewrite, see `git-history-scrub`.

## 1. Map the footprint before touching anything

```bash
git branch backup/with-<thing> HEAD          # always, first
git rev-parse origin/<branch>                # if it was pushed: the lease value for step 4
git log --reverse --format="%h %s" <base>..HEAD
```

For each commit, find three kinds of trace - files, message text, and prose in docs/comments:

```bash
for c in $(git rev-list --reverse <base>..HEAD); do
  files=$(git show --stat --format="" $c -- <PATH> | grep -c . )
  msg=$(git show --format="%s%n%b" --no-patch $c | grep -ci "<name>")
  docs=$(git show --format="" $c -- docs .docs | grep -ci "<name>")
  echo "$c files=$files msg=$msg docs=$docs"
done
```

Docs and commit messages are the traces people forget; a scrub that only removes files still reads as a cover-up in `git log`.

## 2. Rebuild by cherry-pick

Prefer this over `filter-branch`/`filter-repo` for a short branch: every commit is inspected, and message rewording comes free.

```bash
git reset --hard <base>
git cherry-pick <clean commits>              # ones with no trace, in original order
```

For each commit that touches the artifact:

```bash
git cherry-pick -n <sha>                     # stage without committing
git rm -r -q --cached <PATH>                 # drop the files from the index
rm -rf <PATH>                                # and from the working tree
# edit docs/comments that name it, then:
git commit -F - <<'MSG'
<original subject>

<original bullets minus the ones about the artifact>
MSG
```

Two cases worth expecting:

- **A commit that only modified the artifact** (e.g. a comment fix): its cherry-pick conflicts as `DU`. Resolve with `git rm --cached <file>` and keep the commit for its other changes, or skip it if nothing else remains.
- **The commit that deleted the artifact**: its deletions are now moot, but it usually carries unrelated edits worth keeping. Cherry-pick `-n`, drop the deletions, reword the subject to describe only what survives.

## 3. Verify - three zeros and a parity diff

```bash
git log -p <base>..HEAD | grep -ic "<name>"        # patches
git log --format="%s%n%b" <base>..HEAD | grep -ic "<name>"   # messages
git ls-tree -r --name-only HEAD | grep -ci "<name>"          # final tree
git diff --stat backup/with-<thing> HEAD                     # content parity
```

All three counts must be 0. The parity diff should show **only** the lines you intended to remove - anything else means a cherry-pick dropped a hunk.

Grep patterns lie: search for a distinctive substring, not a full sentence, because markdown emphasis (`**word**`) and reflowed lines break literal matches. A "0 matches" that surprises you is usually a bad pattern, not lost content - confirm before acting on it.

## 4. Build, then push

Rewriting can leave a tree that differs subtly from what was last tested. Build every affected project again. Never-pushed commits need only a plain `git push`. For a pushed branch, pin the lease to the SHA recorded in step 1 (not `backup/with-<thing>`, which may be ahead of the remote):

```bash
git push --force-with-lease=<branch>:<recorded-sha> origin <branch>
```

Never `--force` or a bare `--force-with-lease`: git 2.54's docs call the unpinned forms experimental, and a background fetch defeats them. The pinned form refuses if someone else pushed meanwhile.

## Keep the backups

Leave `backup/*` branches until the push is confirmed and the user is happy. They cost nothing and are the only way back.
