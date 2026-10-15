---
name: commit-session-work
description: >-
  Finish Git work at session end: commit, land on main by PR, clean up. Default: this session. local: no push. all/tout/clean: whole tree. Triggers: "committe ce qu'on vient de faire", "fais juste un commit local", "ne pousse pas", "mets ça dans main", "commit everything", "rends la branche clean".
---

# Commit Session Work

Finish Git work safely, using the mode selected by the invocation. Preserve user data, repository policy, and remote history in every mode. Never force-push, rewrite history, discard changes, expose secrets, or bypass a required red gate.

Invoking this skill authorizes only the actions selected by its mode. Scoped and Full-tree modes authorize ordinary commits on a session work branch, a normal push of it, opening its pull request to the resolved target branch and merging it (which deletes that remote branch), and cleanup of session-created worktrees or local temporary branches after proof that their useful content is retained. Local-commit mode authorizes only an in-place commit on the current branch. No mode authorizes force-push, deleting any other remote branch, destructive cleanup of ambiguous content, or bypassing a protection rule enforced by the repository or runtime.

<!-- runtime-slot:session-def -->
"This session" means the current Claude Code conversation, including any subagents/threads it delegated to. Attribution is read from the conversation, not from timestamps, file names, or `git status` alone.
<!-- /runtime-slot:session-def -->

## 1. Select the mode

The mode comes from the first word of the skill argument, normalized to lowercase. An absent or unrecognized argument is **Scoped**.

| Argument | Mode | Scope | Branch |
|---|---|---|---|
| *(none)* | Scoped | Only work attributable to this session and its delegated threads/subagents | PR to the primary branch when the source is the primary checkout or session-created; otherwise the current branch |
| `local`, `commit`, `commit-only` | Local commit | Session-attributable work only | Current branch only; no integration or push |
| `all`, `tout`, `clean` | Full tree | Every tracked and untracked non-ignored change (`clean` adds clean source/target/disposable-session postconditions) | Same as Scoped |

`clean` is not a dry run: it commits the full tree and lands it by PR. Local-commit mode is strict: do not fetch, resolve or switch to the primary branch, integrate, push, set/change an upstream, create or remove a branch/worktree, or clean the source checkout.

In Full-tree mode, do not ask which files to include. Decide `.gitignore` autonomously, commit everything else from the source checkout, and land it on the resolved target.

Before any Git mutation, capture the source checkout path, `INITIAL_BRANCH=$(git branch --show-current)`, `INITIAL_HEAD=$(git rev-parse HEAD)`, `git rev-parse --git-common-dir`, and `git worktree list --porcelain`. A detached `HEAD` is supported in push-enabled modes, but is a hard blocker in Local-commit mode because there is no current branch to receive the commit.

Outside Local-commit mode, resolve `PRIMARY_BRANCH` without assuming `main`: an explicit repository-policy target; else the branch named by `refs/remotes/origin/HEAD`; else an existing local `main`, then `master`; if still ambiguous, stop before mutation.

## 2. Read repository policy and Git state

From the repository root:

<!-- runtime-slot:policy-files -->
- Read `CLAUDE.md`, `AGENTS.md`, and any governing instructions. Honor project rules (e.g. `.claude/rules/`), required gates, and commit conventions.
<!-- /runtime-slot:policy-files -->
- Run `git status --short --branch`, `git diff --name-status`, and `git ls-files --others --exclude-standard`. Inspect all untracked paths before staging.
- Inspect `git worktree list --porcelain` and the current branch. Inspect target branches, merge-base, source-only commits, and both checkout states only when integration may be required.
- Inspect `git config user.name` / `git config user.email` without changing identity unless policy requires it. Inspect `git remote -v` and upstream configuration only in push-enabled modes.
<!-- runtime-slot:account-alias -->
- **Account / SSH alias (this machine).** Three GitHub accounts are disambiguated by SSH remote aliases: `git@github-perso:…` (default, `franckdjiongo`, `djiongoelly@yahoo.fr`), `git@github-automintech:…` (`automintech@gmail.com`), `git@github-cobacam:…` (`ca.cobacam@gmail.com`). The commit identity follows the alias via `~/.gitconfig`. In push-enabled modes, confirm the remote is an SSH alias URL (never `https://github.com/…`, never a `gh` account switch) and that `git config user.email` matches the intended account before pushing. A mismatch with repository policy is a hard blocker.
<!-- /runtime-slot:account-alias -->
- Check that no credential, private key, deployment token, secret value, or generated secret file would be staged. Never print secret values.

## 3. Build the scope ledger

**Scoped and Local-commit modes.** Read the conversation and record exact paths in four groups: **Owned** (created or changed by this session, including completed delegated threads and subagents), **Mixed** (changed by the session but already dirty, generated from unrelated inputs, or also changed by the user), **Unrelated** (dirty before the session or produced by another task), **Ignore candidates** (disposable local artifacts that should never be versioned). Never infer ownership from timestamps, names, or `git status` alone. Leave an ambiguous material path unstaged and report it.

**Full-tree mode (`all`, `tout`, `clean`).** Inventory the same groups for awareness, but do not use ownership to exclude changes. Include every tracked modification, tracked deletion, and untracked path unless it is safely ignored or blocked by security/policy. An unknown non-secret path that is not clearly disposable must be committed rather than left dirty.

## 4. Resolve landing and transfer session work

**Local-commit mode.** Keep the current checkout and branch exactly as they are. Do not resolve a landing branch, transfer commits, fetch, push, create or remove worktrees or branches, change upstream configuration, or clean unrelated files. Build the Scoped ledger, validate, stage only attributable work, commit in place, prove the new commit belongs to `INITIAL_BRANCH`, and leave unrelated changes untouched. Skip the transfer workflow below.

**Push-enabled modes.** Session work reaches `PRIMARY_BRANCH` only through a pull request, never by a local merge, cherry-pick or commit pushed onto it. Whatever the source (primary checkout, session-created worktree, detached session checkout, or secondary branch attributable to the current task), follow the ten steps of `references/landing.md`. Read it before committing.

<!-- runtime-slot:pr-merge -->
The merge step invokes `ship-pr` naming that PR, after `references/landing.md` step 8's preflight. Its sync fast-forwards or realigns with `reset --keep`, never merges, stashes or pushes; skip its redeploy; if it stops, report the landing pending.
<!-- /runtime-slot:pr-merge -->

<!-- runtime-slot:session-branch -->
Temporary session branches are named `claude/session-<id>`.
<!-- /runtime-slot:session-branch -->

For an ambiguous or user-owned secondary branch, do not delete or reinterpret it. Land it on the primary branch (by PR) only when the user explicitly asked to land that branch or the session ledger proves the exact attributable commits; otherwise commit/push according to the branch's existing intent and report that primary integration remains pending.

Never use `git reset --hard`, `git checkout --`, an implicit stash, or another destructive shortcut to get a clean tree.

## 5. Decide `.gitignore` autonomously

Add a narrow ignore rule only for an untracked, local, disposable, reproducible artifact that project conventions do not expect versioned and whose ignoring hides no source, documentation, fixtures, migrations, lockfiles, required generated outputs, or user-authored data. Never ignore an unknown directory wholesale, and never ignore a tracked file instead of reviewing it. Full-tree mode adds safe rules without asking and commits the `.gitignore` change; a tracked file containing a secret is a hard blocker (`.gitignore` cannot protect tracked content). Criteria and Full-tree handling: `references/gitignore.md`.

## 6. Validate before staging

Run repository-required gates and the smallest relevant validations for changed artifacts, then `git diff --check`. In Scoped mode, regenerate canonical outputs only from inputs that belong in the commit; if a generated file mixes in unrelated inputs, stage a commit-specific version (known baseline plus Owned inputs) without overwriting the working-tree file. In Full-tree mode, regenerate from the full tree when policy requires it. Do not commit when a required gate is red. Report the failure without asking a question.

## 7. Stage and review

- Scoped and Local-commit modes: stage whole Owned paths with `git add -- <exact-path>...`; for Mixed files, stage only attributable hunks or a verified commit-specific index entry. Never use `git add -A`, `git add .`, or a broad wildcard.
- Full-tree mode: after the ignore and secret audits, use `git add -A`. This broad staging is authorized only in Full-tree mode.
- Every mode: review `git diff --cached --name-status`, `--stat`, `--check`, and the text diff. In Scoped and Local-commit modes compare the staged list to the ownership ledger. In Full-tree mode compare it to `git status` and confirm every non-ignored change is staged. Never discard working-tree content while correcting staging.

## 8. Commit and optionally push

Derive a concise commit message from the staged outcome and follow repository conventions. **Never add AI attribution or `Co-Authored-By` metadata** (a standing rule on this machine). Before committing, confirm identity, selected branch, staged scope, and required gates (in push-enabled modes also the remote and upstream). Create one cohesive commit unless policy clearly requires separation. If no changes remain, do not create an empty commit.

In Local-commit mode, stop after creating and verifying the local commit: `HEAD` is the new commit on `INITIAL_BRANCH` and the selected staged changes are retained. Do not run `git fetch`, `git pull`, `git push`, any remote mutation, or any upstream-setting command.

In push-enabled modes, fetch first, then push normally: session work goes to its work branch and lands through the PR of `references/landing.md`, never by pushing `PRIMARY_BRANCH` yourself; work kept on a user-owned/current branch goes to that branch's own upstream (none and `origin` valid: `git push -u origin "${INITIAL_BRANCH}"`). Never reuse another branch's upstream or push a detached `HEAD`. If the remote branch is ahead with no divergent local commit, fast-forward first. Do not rebase or rewrite history. Never force-push. On conflict or divergence, stop, preserve the state, and report the blocker without asking a question. Verify that each pushed branch equals its remote-tracking branch.

## 9. Postcondition and final report

Check the mode's postcondition and write the final report as in `references/postconditions.md`. Scoped and Local-commit modes may leave unrelated changes: list them, and claim a clean repository only when `git status --porcelain` proves it. Full-tree mode requires a merged PR when work was landed, a clean status, an upstream, `HEAD` equal to it, and no leftover session worktree or temporary branch.

## Hard blockers

Stop without weakening safety when:

- a required validation fails;
- Local-commit mode is selected while `HEAD` is detached;
- the attributable path scope is ambiguous;
- a tracked secret or protected artifact would be committed;
- Git reports corruption or an unresolved conflict;
- in a push-enabled mode: the remote identity conflicts with repository policy (wrong account/SSH alias), the primary branch or its checkout cannot be resolved safely, the exact commit set for landing/cleanup is ambiguous, source and target contain overlapping uncommitted changes, a non-fast-forward update cannot be integrated safely, or the PR cannot be opened or merged (no review PASS, red or pending checks, conflict, red gate after merge).

Do not ask a question in Full-tree mode. Explain the blocker and the safest next action. Preserve all user data.
