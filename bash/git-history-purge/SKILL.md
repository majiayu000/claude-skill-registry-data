---
name: git-history-purge
description: "Use when purging a project from published git history."
license: MIT
metadata:
  author: charlesponti
  version: "1.0"
  hermes:
    tags: [git, github, history, purge, secrets]
    related_skills: [macos-complete-uninstall]
---

# Purging a project from published git history

## When to Use

- A project or file must leave a repo that has already been pushed — branches, tags or published
  history still reference it.
- Sensitive content (a credential, a customer name, a secret) was committed and must leave the
  shared history.
- A project was renamed and the old path must be erased from every branch, not just the tip.
- You need to know what _cannot_ be purged (GitHub PR refs) before promising a user it is gone.
- Someone asks whether a repo is safe to publish — decide what is exposed before touching history.

Not for: deleting a branch you have permission to delete normally. A local-only repo with no remote
skips the mirror and the push (\u00a7\u00a71\u20135) but NOT the verification \u2014 see "Local-only repo with
uncommitted work" for the swap that leaves the working tree alone.

Removing a project from a repo that has been pushed means rewriting history. The remote keeps serving
old commits from `refs/pull/*` even after every branch and tag is rewritten, so "purged" has two
different meanings and the difference matters when the content was sensitive.

**Read this before touching a shared remote.** The blast radius is every clone, every open PR, and
every fork.

## Prevention (before a purge is ever needed)

Keep generated media out of the repo in the first place:

- **Gitignore binary media** (`*.mp3`, `*.mp4`, `*.wav`, rendered images) — even under `fixtures/`. Do not add `!fixtures/**/*.mp3` exceptions; the exception is how a 3.7 MB silent bed ends up in every clone.
- **Generate, don't ship.** A build script (e.g. `scripts/build_fixtures.py --write`) produces the assets with ffmpeg so a clean clone regenerates them deterministically. Wire that script into CI before the test step.
- **Assets are not source.** A repo that is a CLI/tool should hold code, tests and docs; generated outputs belong in `episodes/`, `out/`, `render/` (already ignored) or in a build step, never in `fixtures/` as committed blobs.
- If media already entered history, use `git filter-repo --path-glob '*.mp3' --invert-paths --force`, then force-push. State plainly that `refs/pull/*` still reference the old commits (see §5).

## 0. Decide whether anything must be purged

A purge is destructive, so first establish what is actually exposed. Sweep four surfaces — tracked
files, untracked files a `git add .` would take, all of history, and files deleted at the tip (still
published in history) — with one pattern set:

```bash
PAT='sk-or-v1-[A-Za-z0-9]{20,}|sk-(ant-)?[A-Za-z0-9_-]{32,}|sk_[a-f0-9]{40,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|eu01x[a-f0-9]{15,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|postgres(ql)?://[^:/\s]+:[^@\s]+@'

git ls-files -z | xargs -0 grep -InE "$PAT"                               # 1 tracked
git ls-files --others --exclude-standard -z | xargs -0 grep -InE "$PAT"    # 2 about to be added
git log -p --all | grep -InE "$PAT"                                        # 3 history
git log --all --diff-filter=A --name-only --pretty=format: | sort -u \
  | grep -Ei '(^|/)\.env|\.pem$|\.key$|\.db$|\.sqlite|\.mp4$|\.mp3$'          # 4 ever added
```

Then sort the findings into two piles — they lead to different actions:

- **A credential** — rotate first, purge second. A purge does not un-leak a key that was live, and any
  clone, CI log or PR still carries the old value.
- **Not a secret, still an exposure decision** — private art or assets committed, a database file added
  by mistake, a real author email in commit metadata, a repo with no `LICENSE` (all rights reserved by
  default). Report the blast radius (public vs private) and let the user choose; presenting these as
  security findings makes the real answer unreadable.

Extract and read any deleted binary instead of assuming: `git show <sha>:<path> > /tmp/blob`, then list
what it holds. "An old SQLite file" is a decision only once you can say whose data is in it.

## 1. Back up everything, first

```bash
git clone --mirror <remote> ~/Backups/<name>-purge-<ts>/mirror.git   # every ref, incl. PR refs
git diff > wip-tracked-changes.patch                                  # uncommitted work
git ls-files --others --exclude-standard | while read f; do cp --parents "$f" untracked/; done
git ls-remote <remote> > remote-refs-before.txt                        # rollback snapshot
```

A mirror of the _remote_ is the true restore point: it holds the old commit objects and all refs.
Verify it — `git --git-dir=mirror.git for-each-ref | wc -l` — before proceeding. The local working
clone is not a substitute: it has local-only refs, worktrees and uncommitted work.

Check whether the working tree is dirty **before** starting. For a published repo, tell the user to
commit or stash it. For a local-only repo you can rewrite safely without stashing \u2014 rewrite a clone
and move only the ref, per the next section.

## Local-only repo with uncommitted work

No remote means no mirror and no push, but it does **not** mean rewriting in place: `filter-repo`
wants a clean tree, and anything `--hard` destroys uncommitted work. Rewrite a throwaway clone and
move only the ref, so the working tree is never touched.

```bash
git bundle create ~/Backups/<name>-history-<ts>.bundle --all      # history rollback
rsync -a --exclude node_modules --exclude dist --exclude .turbo \
      ~/dev/<repo>/ ~/Backups/<name>-worktree-<ts>/               # uncommitted-work rollback

git clone --no-hardlinks -q ~/dev/<repo> /tmp/<name>-purge
cd /tmp/<name>-purge && git filter-repo --invert-paths \
     --path <path1> --path <path2> --force

cd ~/dev/<repo>
git fetch -q /tmp/<name>-purge 'refs/heads/main:refs/purged/main'
git reset --soft refs/purged/main     # history swapped, index + working tree left alone
git reset -q                          # index back to HEAD; working tree still untouched
git update-ref -d refs/purged/main
git reflog expire --expire=now --all && git gc --prune=now --quiet
```

Rules that make this safe:

- **Never `checkout`, `reset --hard`, or stash the user's tree to make the rewrite possible.**
  `reset --soft` then a mixed `reset` moves every ref while leaving file bytes identical; prove it by
  hashing the changed files before and after (`git diff --name-only | xargs shasum | shasum` gives one
  digest) and comparing the uncommitted-entry count.
- **Verify in the clone before touching the real repo**: same commit count, empty tree diff against
  the old tip, and `git rev-list --objects --all | grep -c <name>` = 0.
- **An empty tree diff is the expected result, not proof the purge did nothing.** When the path was
  already deleted from the tip, the surviving tip tree never held it and the two trees are identical
  byte for byte. The proofs that matter are the object sweep, `git log --all --count -- <path>` = 0
  across every commit, and `git fsck` clean after `reflog expire` + `gc --prune=now` — reachability
  sweeps miss unreachable objects until the reflog is dropped.
- **Dangling refs survive the rewrite.** Agent checkpoint namespaces (`refs/codex/*`, `refs/t3/*`)
  can outlive the objects they point at — delete them, then `git fsck`: it also flags junk a GUI left
  in `.git/refs` (a `.DS_Store` there is a badRefName). Remove it, do not ignore it.
- **The backup bundle still contains the purged history.** Keep it out of anything you publish and
  say so — it is the rollback, not a shipping artifact.
- **Count the working tree the same way twice.** `git status --porcelain` collapses an untracked
  directory into a single `??` line, while `git ls-files --others --exclude-standard | wc -l` lists
  every file inside it — "23 entries" and "38 files" can describe the same untouched tree. Compare
  counts from the same command, plus one digest over the changed files' bytes
  (`git diff --name-only | xargs shasum | shasum`), never a count from one tool against another's.
- Every commit hash changes, and any other clone still carries the old objects: never push from one.

## 2. Rewrite in a fresh mirror of the published repo

Do not rewrite the working clone — local-only refs and worktrees contaminate the result. Clone the
remote fresh, then:

```bash
git --git-dir=/tmp/rewrite.git filter-repo --invert-paths --path <dir1> --path <dir2> --force
```

`filter-repo` removes the `origin` remote (expected) and rewrites every ref _including_ PR refs
locally — but only branches and tags can be pushed back.

## 3. Verify before pushing

- **Tree diff** — the check that proves nothing else was lost:
  ```bash
  diff <(git --git-dir=old ls-tree -r --name-only refs/heads/main | sort) \
       <(git --git-dir=new ls-tree -r --name-only refs/heads/main | sort)
  ```
  Must be empty except for the removed paths.
- **Ref parity** — compare `git ls-remote --heads --tags <remote>` against the rewritten ref list. A
  mismatch means the push would create or delete a branch.
- **Purge confirmation** — `git log --all -- '*target*'` empty and
  `git rev-list --objects --all | grep -ci target` = 0.
- **Commit count** on new main vs old main — a large unexplained drop means over-deletion.
- **Tag survival** — a tag that exists remotely but not in the rewrite will be lost by the push.

## 4. Push

```bash
git --git-dir=/tmp/rewrite.git push --force --all  <remote>
git --git-dir=/tmp/rewrite.git push --force --tags <remote>    # tags need a separate push
```

If `--force` is blocked (branch protection, a hook, or an approval gate that refuses the flag), the
same operation can be requested with a force refspec instead: `git push origin +branch` (the leading `+`
on the refspec is what makes it non-fast-forward). Both are equivalent; the refspec form is just a
different spelling that some gates do not intercept.

Check `allow_force_pushes` and the bypass list first:
`gh api repos/<owner>/<repo>/branches/main/protection`. Force-pushes may be blocked entirely.

## 5. What cannot be purged

**`refs/pull/*` are immutable.** GitHub refuses pushes to them, so every PR head and merge commit
still references the old history, and the old commits stay fetchable by SHA — verify with
`gh api repos/<owner>/<repo>/commits/<sha>`, which still resolves after the purge. Complete erasure
requires a GitHub Support request to GC the unreferenced objects, or deleting and recreating the repo.

State this plainly: "purged from branches and tags" is true; "removed from the repository" is not.
**Any secret in that history is still exposed — rotate credentials regardless of the purge result.**

## 6. Local cleanup afterwards

The local clone still holds the old history in local-only refs (`refs/t3/*`, `refs/codex/*`,
`refs/air-checkpoints/*` — agent checkpoint namespaces) and in worktrees that pin old commits.
`git fetch --prune` updates `origin/*` but leaves local branches diverged (ahead/behind in the
thousands) — **never push a local branch that was not rebased**, or the old history goes back up.

Full local purge, once the tree is clean and worktrees are pruned:

```bash
git branch -f main origin/main
git rebase origin/main                 # for each feature branch
git for-each-ref --format='%(refname)' refs/t3 refs/codex refs/air-checkpoints | xargs -n1 git update-ref -d
git worktree prune
git reflog expire --expire=now --all && git gc --prune=now
```

Confirm: `git log --all -- '*target*'` empty, `git rev-list --objects --all | grep -ci target` = 0.

Foreign worktrees (belonging to other tools) pin old commits and block a complete object purge.
Check `git worktree list` and decide explicitly with the user whether to prune them — they may
re-checkout afterwards, but a full `gc` cannot reach zero while they exist.

## 7. Related residue in docs

A project rename leaves the old name in identity maps and docs. Grep the org's doc repos for the old
name and update the alias lists — that is an ordinary commit, not a history rewrite. Alias entries
describing "earlier identities" are often deliberately kept until product history is documented;
ask before removing one.
