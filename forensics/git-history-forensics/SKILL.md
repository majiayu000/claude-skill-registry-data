---
name: git-history-forensics
description: >
  Investigate and recover from Git history problems with hypothesis-driven, read-only-first
  methods: find when/where a bug or change was introduced (bisect, pickaxe, line-history blame),
  recover lost commits, branches, stashes and dropped work (reflog, fsck), and reason about what
  gc and expiry will delete. Use when someone asks "who/when/why did this change", "I lost my
  commits after reset/rebase/force-push", "find the commit that broke X", "recover a deleted
  branch or dropped stash", or "did this secret ever enter history". Not for everyday branching
  or merging (use git-workflow, git-merge-conflicts), and history rewriting or secret purges are
  out of scope until the user explicitly authorizes them.
compatibility: >
  Agent Skills-compatible coding agents with a shell and Git 2.30 or newer (checked against
  current git-scm.com documentation). Works on any local clone; no network needed.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "git, forensics, reflog, fsck, bisect, blame, recovery, history"
  topics: "software-development, debugging"
---

# Git History Forensics

Git almost never destroys data immediately. Commits that look "lost" are usually unreachable, not deleted, and they stay recoverable until reflog expiry and garbage collection remove them. Forensics is therefore a race against expiry plus a discipline: **observe first, preserve, then change anything**.

Boundaries: everyday branching is `git-workflow` / `git-branching-worktrees`; conflict resolution is `git-merge-conflicts`; generic bug hunting outside history is `debugging-workflow`; leaked-credential handling after discovery is `secrets-management`. This skill covers *investigating and recovering*.

## Non-negotiable rules

1. **Read-only first.** `log`, `show`, `reflog`, `cat-file`, `blame`, `rev-list`, `fsck` (without `--lost-found`) change nothing. Use them until you know what happened.
2. **Preserve before you act on a damaged repo.** If something may be lost, make a byte-level copy of the repository directory (`cp -a` of the `.git` directory or the whole worktree) before any command that can prune: `gc`, `prune`, `reflog expire`, `repack -d`. Setting `git config gc.auto 0` in the copy or original prevents an automatic gc from running mid-investigation.
3. **Never rewrite or destroy history without explicit user authorization**: `reset --hard`, `clean -fdx`, `push --force`, `filter-repo`, `filter-branch`, `reflog expire --expire=now`, `gc --prune=now`, deleting branches or tags. Describe the effect and the undo path, then wait for a clear yes.
4. **Recover by creating a ref, not by moving one.** `git branch recovered/<what> <sha>` is non-destructive; `git reset --hard <sha>` on a dirty tree is not.
5. **Treat history contents as sensitive.** Do not print or paste suspected secrets into chat or tickets; report the commit, path and line, then follow `secrets-management`. Rotation comes before any purge.
6. **Distinguish what you saw from what you infer.** Author/committer names and dates are user-controlled and forgeable; only the object hashes and signature verification (`git log --show-signature`) carry integrity weight.

## Workflow

### 1. State the question as a testable hypothesis

Bad: "figure out what happened". Good: "Commit X was removed from `main` by a force-push on or after Tuesday; it should still be in my reflog or a teammate's clone." Decide what evidence would refute it.

### 2. Survey without touching anything

```bash
git status --short --branch
git log --oneline --graph --decorate --all -n 30
git reflog show --date=iso -n 40          # HEAD movements, newest first
git reflog show <branch>                  # one ref's history
git for-each-ref --sort=-committerdate    # all refs incl. remotes, tags, stash
```

The reflog is **local and per-ref (the HEAD reflog is per-worktree; branch reflogs are shared)**; it records where refs *pointed*, including before a reset or rebase (`HEAD@{n}`, `<branch>@{2.hours.ago}`). It does not exist in a fresh clone, on a server bare repo (usually), or for another person's machine. Entries expire (see step 5).

### 3. Pick the technique that matches the question

| Question | Technique | Notes |
|---|---|---|
| Which commit introduced a regression? | `git bisect` with a deterministic test | Automate with `git bisect run <script>`; exit 0 = good, 125 = skip (cannot test), 1-127 otherwise = bad, 128+ aborts the bisect |
| Did a secret ever enter history? | `git log --all -S'<non-secret prefix or pattern>' --oneline --name-only` | Search by a distinctive prefix, never paste the full value; report sha and path only |
| When did this string/function appear or vanish? | `git log -S'text'` (count changes) or `-G'regex'` (diff lines match) | Add `--all`, `-p`, and a path limiter; `-S` finds add/remove, `-G` also finds edits |
| History of one function or line range | `git log -L :funcname:path` or `-L10,20:path` | Follows moves inside the file |
| Who last touched these lines, ignoring noise? | `git blame -w -C -C -C <path>` and `--ignore-revs-file` | `-w` ignores whitespace; `-C` detects moved/copied lines; blame shows the *last* change, not the *cause* |
| History across renames | `git log --follow -- <path>` | Single path only |
| Was a file ever deleted? | `git log --diff-filter=D --name-only -- <path>` then `git show <sha>^:<path>` | |
| Which merge brought it into `main`? | `git log --ancestry-path --merges <sha>..main` | Or `git log --first-parent` to read mainline only |
| Is a commit in a release? | `git branch -a --contains <sha>`, `git tag --contains <sha>` | |
| What did a lost commit contain? | `git show <sha>`, `git cat-file -p <sha>` | Works on unreachable objects if they still exist |

Rules for bisect: pin the test so it fails for the *bug*, not for build breakage (return 125 for "cannot test"); record `git bisect log` as evidence; always finish with `git bisect reset`. Bisect lands on the first bad commit *for your test*; confirm with `git show` and by reverting that commit in a scratch worktree before blaming it.

### 4. Recover lost work (ordered by cost and risk)

1. **Reflog hit?** `git reflog` / `git log -g --oneline`. Pick the sha before the damaging operation (e.g. `HEAD@{3}`), then `git branch recovered/x <sha>`.
2. **Dropped stash or deleted branch whose reflog is gone?** Look for dangling commits:
   ```bash
   git fsck --no-reflogs --unreachable --no-progress | grep commit
   git fsck --lost-found        # writes pointers under .git/lost-found; mutates .git slightly
   ```
   Inspect each candidate with `git show --stat <sha>`. A dropped stash is a commit whose message starts with `WIP on` or `On <branch>:`. Restore with `git stash apply <sha>` (not `pop`) or branch it.
3. **Someone force-pushed?** Your remote-tracking ref may still hold the old tip (`git reflog show origin/main`), as may teammates' clones and CI caches. Host-side reflogs/events (for example the hosting platform's activity log) are a user-side action; ask the user.
4. **Uncommitted work lost to `reset --hard`/`checkout .`?** Tracked changes that were never added are not in Git. If they were ever `git add`ed, their blobs exist: `git fsck --lost-found` lists dangling blobs. Editor local-history is the other source.
5. **Corrupt repo** (`error: object file ... is empty`, `bad object`): `git fsck --full`, then fetch missing objects from a remote into a *copy*. Do not delete "empty" object files until a copy exists.

### 5. Know the expiry clock

From current `git gc` documentation: `gc.reflogExpire` defaults to 90 days; `gc.reflogExpireUnreachable` to 30 days (entries not reachable from the tip, typical after `--amend`/rebase); `gc.pruneExpire` to 2 weeks (unreachable loose objects older than this are deleted); `gc.auto` triggers at about 6700 loose objects. Consequently: a commit orphaned by a rebase can lose its reflog entry in ~30 days, and its object disappears two weeks after that or earlier if `gc --prune=now` was run. Check actual values with `git config --get-regexp 'gc\.'` before promising recoverability. `gc.pruneExpire=now` is risky with concurrent writers.

### 6. Hand over evidence

Report: the question, commands run (read-only vs mutating), the shas involved, what was recovered and as which ref, what remains unknown. Offer destructive follow-ups (history rewrite, force-push, branch deletion) as options, not actions.

## Worked example: "I lost three commits after a rebase"

1. Hypothesis: the pre-rebase tip is in the reflog.
2. `git reflog show feature/payments --date=iso` shows `feature/payments@{4}: commit: add retry` before a `rebase (start)` entry.
3. `git show --stat feature/payments@{4}` confirms the three commits and files.
4. `git branch recovered/payments feature/payments@{4}` creates a safe ref. Nothing else changed.
5. `git range-diff feature/payments...recovered/payments` shows what the rebase altered or dropped; the user decides whether to cherry-pick the missing change.

If step 2 had shown nothing, escalate to `fsck --no-reflogs --unreachable` on a copy before any gc.

## Anti-patterns

- Running `git gc` or `git prune` "to clean up" before recovering.
- `git reset --hard` as an investigation step on a dirty working tree.
- Trusting `git blame` as the root cause (it shows the last formatting change when `-w`/`-C` are omitted).
- Bisecting with a flaky test, or with a test that fails to build on old commits (use exit 125).
- Treating author dates as evidence of when something happened; commit dates can be rewritten.
- Purging a leaked secret from history and skipping rotation: the secret is already compromised.
- Concluding "it was never there" from a shallow clone (`git rev-parse --is-shallow-repository`) or a single-branch clone.

## Verification checklist

- [ ] A byte-level backup or `gc.auto 0` precedes any pruning-capable command.
- [ ] Every mutating command was named to the user and authorized.
- [ ] Recovered commits live on a new named ref and were inspected with `git show`.
- [ ] Bisect result was confirmed independently and `git bisect reset` was run.
- [ ] Reported facts are labeled as observed or inferred; no secrets quoted.

## References

- [references/recovery-playbook.md](references/recovery-playbook.md): per-incident decision tables.
- [references/scenarios.md](references/scenarios.md): activation and evaluation scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
