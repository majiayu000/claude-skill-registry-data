---
name: Git
slug: git
version: 1.0.12
description: Commits, branches, merges, and rebases Git repositories, resolves conflicts, and recovers lost history. Use when the work touches a repo, commit, branch, merge, rebase, stash, tag, or submodule; when Git refuses a command — index.lock exists, push rejected as non-fast-forward, detached HEAD, dubious ownership, unrelated histories, conflict markers left behind; when something looks lost after a hard reset, a bad rebase, a deleted branch, or a dropped stash; when splitting a mixed change, wording commit messages, cleaning history before review, or force-pushing without wrecking a teammate's work; when a credential or a huge file got committed; when setting up worktrees, hooks, LFS, sparse checkout, signing, or separate work and personal identities. Not for CI pipeline YAML (github-actions, gitlab) or for composing the pull request description itself (pull-request).
homepage: https://clawic.com/skills/git
changelog: Display name shown correctly
metadata:
  clawdbot:
    emoji: 📚
    requires:
      bins:
      - git
    os:
    - linux
    - darwin
    - win32
    displayName: Git
    configPaths:
    - ~/Clawic/data/git/
    - ~/git/
    - ~/clawic/git/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/git/
      - ~/git/
      - ~/clawic/git/
---

User preferences and memory live in `~/Clawic/data/git/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/git/` or `~/clawic/git/`), move it to `~/Clawic/data/git/`, and say in one line that you moved it and from where.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/git/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| integration_style | rebase \| merge \| squash \| repo-default | repo-default | How branches get combined and what `pull` does; `repo-default` reads the last 20 merges (`git log --merges --oneline -20`) and follows what the repo already does |
| commit_style | conventional \| plain \| repo-default | repo-default | Shape of every generated commit subject (Commit Discipline); `repo-default` copies the style found in `git log --oneline -20` |
| branch_naming | text (pattern) | type/topic | Template used when creating branches, lowercase and hierarchical by default |
| protected_branches | list | main, master | Branches never committed to, rewritten, or force-pushed (Core Rule 2, Push gate); a request that targets one becomes "branch first, then propose the merge" |
| force_push_policy | never \| own-branches \| any | own-branches | Governs the Push gate: `never` turns every rewrite into a `git revert`; `any` still requires `--force-with-lease` |
| subject_max | number (chars, 50-100) | 72 | Hard stop for every generated commit subject (Core Rule 6) and the length any `commit-msg` gate enforces |
| message_language | text (language) \| repo-default | repo-default | Language of generated commit subjects, bodies, and tag messages; `repo-default` copies the language already in `git log --oneline -20` |
| remote_host | github \| gitlab \| bitbucket \| gitea \| other | github | Selects PR-vs-MR wording, blob size limits, and squash-merge semantics quoted in review and release guidance |
| signing | off \| ssh \| gpg | off | Adds signing flags and `commit.gpgsign` setup to commit and tag flows |

Preference areas to record as the user reveals them:

- **tooling** — CLI vs GUI vs IDE Git, hosting CLI in use, pre-commit framework, mergetool of choice
- **conventions** — subject format, ticket-ID placement, tag scheme, trailers such as `Co-authored-by`, monorepo tag prefixes
- **thresholds** — body-length and file-count limits a commit may reach, the large-file guard's size (`--above=`), reflog retention (`gc.reflogExpireUnreachable`), clone depth and filter in CI
- **restrictions** — repos, paths, or file types the agent must leave alone; operations banned outright (no rebase, no `filter-repo`); compliance regimes demanding signed or reviewed commits
- **platform** — hosting provider, SSH vs HTTPS, monorepo vs polyrepo, Windows/macOS line-ending and case sensitivity constraints
- **safety posture** — whether the agent may commit or push unprompted, confirmation before `--hard`/`clean -f`/history rewrites
- **work order** — commit granularity, whether to sync before starting, review gates expected before a push
- **cadence** — how often to fetch/prune, when to run maintenance on large clones

## When To Use

- Any task touching a Git repository: staging, commits, branches, merges, rebases, tags, stashes, submodules.
- Something looks lost — deleted branch, bad rebase, hard reset, vanished stash: recovery is a first-class use (→ Recovery Playbook, `recovery.md`).
- Git refuses to run and the message is opaque (`index.lock`, non-fast-forward, dubious ownership, detached HEAD) → `errors.md`.
- Before any history rewrite or force push: run the Output Gates below first.
- Investigating when a behavior broke, who changed a line, or where code came from → `forensics.md`.
- Not for CI pipeline configuration — GitHub workflows are `github-actions`, GitLab pipelines are `gitlab`; writing the PR description itself is `pull-request`.

## Quick Reference

| Situation | File |
|-----------|------|
| Staging surgery, splitting a mixed change, wording a message, stashing | `commits.md` |
| Creating or switching branches, merge vs rebase, stacked branches | `branching.md` |
| A merge or rebase stopped on conflicts | `conflicts.md` |
| Undoing: reset, revert, amend, rewriting a branch before review | `history.md` |
| Work looks lost: bad reset, dropped stash, deleted branch, detached commits | `recovery.md` |
| Git printed an error and refuses to proceed | `errors.md` |
| "When did this break", "who wrote this line", "where did this code go" | `forensics.md` |
| Push/pull friction, review flow, force-pushing on a shared branch | `collaboration.md` |
| Forks, upstreams, mirrors, moving or splitting a repository | `remotes.md` |
| Two checkouts at once: hotfix mid-refactor, parallel agent tasks | `worktrees.md` |
| Nested repositories: submodules, subtrees, vendored code | `submodules.md` |
| Slow clone or status, monorepo scale, huge files, LFS | `large-repos.md` |
| Pre-commit/pre-push automation, lint gates, a hook that never runs | `hooks.md` |
| A credential or a giant blob reached the history | `secrets.md` |
| Wrong author identity, auth failures, ignore rules, CRLF churn | `config.md` |
| Tags, version bumps, backports, release branches, changelogs | `releases.md` |
| A flag or one-time config that removes a whole trap class | `commands.md` |
| Git driven from a script, a CI job, or a non-interactive agent | `scripting.md` |
| User states a workflow preference | `setup.md` + `memory-template.md` |
| Anything else | Stay here — Core Rules, Revision Syntax, and the Recovery Playbook cover the default path |

## Core Rules

1. **Rewrite only unpushed history.** Check: `git log @{u}..` lists exactly the commits safe to amend/rebase/squash. A commit missing from that output is published — fix forward with `git revert` instead.
2. **Force push = `--force-with-lease`, own branch only, never a branch in `protected_branches`.** The lease is void if anything fetched after the remote moved — IDE auto-fetch does this without warning — so add `--force-if-includes` (git >=2.30) to close that hole.
3. **Destructive command → name the casualties first.** `git status` before `reset --hard`, `git clean -n` before `git clean -f`, `git diff @{u}` before force push. If you cannot list what dies, you are not ready to run it. Cheap insurance when you are unsure: `git branch backup/$(date +%F-%H%M)` costs one ref and zero bytes.
4. **`git reflog` before panic.** Committed work survives 90 days (reachable) / 30 days (unreachable) — those are reflog-entry lifetimes, and a commit some reflog entry still names does not count as unreachable, so `gc`'s shorter two-week prune window never applies to it (→ `recovery.md`). The only truly unrecoverable losses: never-staged edits killed by `reset --hard`/`restore`, and untracked files killed by `clean -f`.
5. **Conflicts repeat per commit in rebase, once in merge.** Same region conflicting across 3+ replayed commits → abort and merge instead (one resolution), or enable `rerere` so each resolution is recorded once.
6. **Commit = one reviewable change.** Mixed changes → `git add -p` to split. Subject: aim ≤50 chars (convention), hard stop `subject_max`, default 72 because `git log` indents bodies by four spaces inside an 80-column terminal — hosts truncate around the same width in list views. Body explains why, not what; subject and body both follow `message_language`.
7. **A pushed secret is a leaked secret.** Rotate the credential first; history rewrite (filter-repo) is cleanup, not containment — forks, clones, and CI caches keep the old objects.
8. **Escalate undo by blast radius; stop at the first tool that reaches the goal.** `git restore` (one file, nothing else moves) → `git revert` (one commit, safe on shared branches) → `git reset` (moves your branch pointer only) → `git rebase` (new SHAs, everyone tracking the branch pays) → `git filter-repo` (every clone in existence is now wrong). Reaching for the right-hand tools when a left-hand one suffices is the single most common self-inflicted Git incident.

## Revision Syntax

Most "Git did something I did not ask for" reports are a misread revision expression. Decoder:

| Expression | Means | Trap |
|---|---|---|
| `HEAD~2` | Two commits back along first parents | Follows the mainline through merges, skipping the merged branch |
| `HEAD^2` | The SECOND PARENT of a merge commit | Not "two back": `^` selects a parent, `~` walks generations |
| `HEAD@{2}` | Where HEAD pointed two reflog moves ago | Time, not ancestry — and local to this clone only |
| `@{u}` / `@{push}` | The tracked upstream / where a push would land | They differ in triangular setups (fork: pull from upstream, push to origin) |
| `A..B` | Commits reachable from B but not A | In `git diff`, the same expression means the plain A-to-B diff |
| `A...B` | `log`: commits on either side but not both. `diff`: B against the MERGE-BASE | The one expression whose meaning changes between `log` and `diff` — the source of "my diff shows unrelated files" |
| `:/fix login` | Most recent commit whose message contains that text | Searches all reachable history, not just this branch |
| `:1:file` `:2:file` `:3:file` | During a conflict: base, ours, theirs | Numbering is fixed; "ours/theirs" inverts under rebase (→ Conflict Basics) |
| `main@{yesterday}` | Branch tip as of yesterday | Reflog-based: empty in a fresh clone, and gone after reflog expiry |
| `v1.2^{}` | The commit an annotated tag points at | Without peeling, a tag is its own object — `git diff v1.2` compares against the tag object's target, scripts that assume a commit break |

Ambiguity between a branch and a path is resolved with `--`: `git checkout -- config` is always the file.

## Recovery Playbook

| Symptom | Play |
|---------|------|
| Just finished a bad rebase/merge/reset | `git reset --hard ORIG_HEAD` — Git saved your pre-operation position |
| Commits vanished after a rewrite | `git reflog` → `git reset --hard HEAD@{n}` (the entry just before the damage) |
| Deleted a branch | `git reflog` → `git branch restored <sha>` |
| Committed on the wrong branch (unpushed) | `git switch right-branch && git cherry-pick <sha>`, then `git switch - && git reset --hard HEAD~1` |
| Committed on detached HEAD, then switched away | Commit stays in `git reflog` for 30 days → `git branch rescue <sha>` |
| Need one file as it was N commits ago | `git restore --source HEAD~N -- path` — nothing else moves |
| `reset --hard` ate staged-but-uncommitted work | `git fsck --lost-found` — staged content survives as dangling blobs; never-staged edits are gone |
| Dropped a stash | `git fsck --unreachable \| grep commit` → `git stash apply <sha>` |
| Bad commit already on a shared branch | `git revert <sha>` — never rewrite shared history |
| Unsure what happened / anything else | `git reflog` first; before experimenting, `git branch backup` — a branch is free insurance |

Deeper chains (deleted file archaeology, corrupted index, post-`filter-repo` rescue, what expiry actually deletes): `recovery.md`.

## Commit Discipline

- One reviewable change per commit; `git add -p` splits mixed work. `git commit --fixup <sha>` + `git rebase -i --autosquash` batches corrections without "fix typo" noise.
- Match the repo's existing message style before imposing one — check `git log --oneline -20`, or follow `commit_style` and `message_language` when the user set them. Conventional commits (`type(scope): description`) only where the log or release tooling already uses them.
- `git pull --rebase --autostash` before push: no surprise merge commits, works with a dirty tree.
- First push: `git push -u origin HEAD`, or set `push.autoSetupRemote` (git >=2.37) once and never type `-u` again.

## Conflict Basics

- Set `merge.conflictStyle zdiff3` (git >=2.35) once: markers include the base version, so you see what each side changed instead of guessing intent.
- Ours/theirs invert during rebase: "ours" = the branch you are rebasing onto, "theirs" = your own commit being replayed — rebase checks out upstream and applies your commits as patches on top.
- After resolving: `git grep -nE '^(<{7}|={7}|>{7})'` must return nothing, then build/tests, then `--continue`.
- Everything else → `conflicts.md`.

## Output Gates

Before declaring Git work done:

- [ ] Rewrite gate: every amended/rebased commit appeared in `git log @{u}..` before I touched it
- [ ] Deletion gate: I listed the casualties (`git status`, `git clean -n`) before any `--hard` / `-f`
- [ ] Push gate: target is not in `protected_branches` and not a shared branch; if forcing at all, `--force-with-lease` minimum, and within `force_push_policy`
- [ ] Conflict gate: marker grep is clean AND the project builds after resolution
- [ ] Identity gate: `git config user.email` is the right identity for this repo (work vs personal)
- [ ] Content gate: `git diff --cached --stat` reviewed — no credential, no build artifact, no blob the host will reject

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| `git stash` before a risky operation, expecting untracked files saved | Plain stash skips untracked files | `git stash -u` |
| Assuming `stash pop` dropped the stash after a conflict | Pop only drops on clean apply; on conflict the entry stays | Resolve, then `git stash drop` |
| `git clean -fdx` to "clean build artifacts" | `-x` also deletes ignored files: `.env`, IDE config, local secrets | `git clean -fd`, always preview with `-n` |
| Renaming `Foo.js` → `foo.js` works locally, breaks CI | macOS/Windows filesystems are case-insensitive, Linux is not | `git mv Foo.js tmp && git mv tmp foo.js` |
| `git branch -d` refuses to delete after squash-merge | Squashed commits are unreachable from main, so Git thinks the branch is unmerged | Verify the PR merged, then `-D` |
| Committing a large binary "just this once" | GitHub warns >50 MB, blocks >100 MB — and history keeps the blob forever | Git LFS before first commit; after the fact, `git filter-repo` (`secrets.md`) |
| "Sharing" hooks via `.git/hooks` | `.git/hooks` is never versioned | Commit a hooks dir + `git config core.hooksPath` (`hooks.md`) |
| Cloned repo has empty submodule directories | Submodules need explicit initialization | `git clone --recurse-submodules`, or `git submodule update --init` |
| Adding a path to `.gitignore` to stop tracking it | Ignore rules never apply to already-tracked files — the file keeps showing up in every diff | `git rm --cached <path>`, commit the removal, then ignore it |
| `git reset --hard` when the intent was "unstage this" | `--hard` also throws away the working tree; unstaging needs no destructive flag | `git restore --staged <path>` (index only) |
| Marking a config file `--assume-unchanged` so local edits stop appearing | Git now lies in `status`, and any incoming change to that file breaks pull with a confusing error | Commit a `.example` template, gitignore the real file (`config.md`) |

## Where Experts Disagree

- **Squash-merge vs preserve commits.** Squash school treats PR commits as WIP noise (small PRs, GitHub-centric teams); preserve school needs atomic commits for bisect and surgical reverts (long-lived repos, kernel-style review). Follow the repo's existing merge style — mixing styles hurts more than either choice.
- **Trunk-based vs long-lived branches.** DORA research associates branches merged within about a day with higher delivery performance; git-flow-style release branches pay off only when you maintain multiple released versions in parallel.
- **Conventional commits.** Pay off when tooling consumes them (changelog generation, semver automation); pure ceremony otherwise. Detect: release automation in the repo → use them.
- **Mandatory commit signing.** Provenance school signs everything (supply-chain audits, OSS releases, regulated code). Skeptics note that a signature proves a key was present, not that the author was — a compromised laptop signs happily. Boundary: sign what outsiders consume; internal application repos gain little beyond noise.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/git (install if the user confirms):
- `pull-request` — when the branch is ready and the PR itself has to be written and validated
- `review-code` — when the job is judging someone else's diff, not producing it
- `github-actions` — when the failure is in workflow YAML rather than in the repository
- `gitlab` — GitLab CI/CD pipelines and merge-request settings
- `code` — planning, implementing, and verifying the change the commits will carry

## Feedback

- If useful, star it: https://clawic.com/skills/git
- Latest version: https://clawic.com/skills/git

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/git.
