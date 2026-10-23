---
name: git-cleanup
disable-model-invocation: true
description: 'Audits stale Git resources and cleans them with approval. Use when pruning branches, removing abandoned worktrees, or closing stale PRs and issues.'
argument-hint: '[--dry-run|--apply] [--branches] [--worktrees] [--remotes] [--stashes] [--tags] [--prs] [--issues] [--stale-days=N] [--host=github|gitlab|auto] [--protect=<pattern>] [--report-only]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - AskUserQuestion
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(glab:*)
  - Bash(ls:*)
  - Bash(test:*)
  - Bash(find:*)
  - Bash(mkdir:*)
  - Bash(rm:*)
  - Bash(date:*)
  - Bash(awk:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh:*)'
---

# git-cleanup

Audit and clean up stale git resources — local branches, remote-tracking refs,
worktrees, stashes, tags, pull requests, and issues — across local checkouts,
GitHub, and GitLab. Before recommending any deletion, the skill cross-references
active code and project state to distinguish truly abandoned resources from
work-in-progress. **Dry-run is the default; destructive actions require `--apply`
plus explicit user confirmation.**

## Arguments

Parse `$ARGUMENTS`:

- **--dry-run** (default): Analyze and report only. Never deletes.
- **--apply**: Enable destructive actions. Still requires interactive confirmation.
- **--report-only**: Write the audit report and stop; skip the decision prompt.
- **--branches** / **--worktrees** / **--remotes** / **--stashes** / **--tags** /
  **--prs** / **--issues**: Limit scope to the listed domains. Default is all
  local domains (branches, worktrees, remotes, stashes, tags) plus remote
  domains (prs, issues) when a host CLI is available.
- **--stale-days=N**: Age threshold for "stale" (default: 90).
- **--host=github|gitlab|auto**: Remote host. `auto` (default) parses `origin`.
- **--protect=<pattern>** (repeatable): Extra branch patterns that must never be
  deleted. Always-protected: `main`, `master`, `develop`, the default branch,
  any branch that is the base of an open PR, and — when the repo has a
  `RELEASING.md` — the state's `trunk` and every `maintenance` branch.

**Questions:** class `confirm-destructive` (Phase 4 decision gate, per-item prompts); headless (no question tool or chat turn): produce the dry-run report even with `--apply`, delete nothing, and print the interactive rerun. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 0: Setup and Host Detection

1. **Verify working tree is a git repo**: `git rev-parse --git-dir`. Abort if not.
2. **Determine default branch**: `git symbolic-ref refs/remotes/origin/HEAD` →
   fall back to `main` / `master` if unset.
3. **Read the release state**: run
   `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh get` and parse
   its `key=value` output (format and rules:
   `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branching-model.md`).
   - `present=0` (no `RELEASING.md`): release-model rules are off. Every later
     phase behaves exactly as described without the "Release model" notes.
   - `present=1`: record `RELEASE_TRUNK` (`trunk`), `RELEASE_MAINTENANCE`
     (`maintenance`, comma-separated) and `RELEASE_FROZEN` (`frozen`,
     comma-separated). These drive the protected set, the retired
     maintenance branch category, and the sync-merge findings below.
   - Exit code 2 (malformed state block): **STOP**. Show the parse error from
     stderr and point the user at `/ycc:release-model --audit`. Never guess a
     trunk or a protected set from a broken block.
4. **Detect host CLIs and MCP tools**. Detection follows the bundle-wide
   contract in
   `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/forge-detection.md`
   (`forge_detect_provider origin` → `github` / `forgejo` / `gitea` / `gitlab` /
   `unknown`; `forge_cli` → `gh` / `tea` / `glab`); the git-cleanup-specific
   operation map lives in
   `${CLAUDE_PLUGIN_ROOT}/skills/git-cleanup/references/host-detection.md` (read when mapping a host operation to a CLI or MCP call).
   Summary:
   - Prefer `mcp__github__*` tools if available for GitHub operations.
   - Else `gh auth status` for GitHub, `tea login list` for the Forgejo/Gitea
     family, `glab auth status` for GitLab.
   - If `--host=auto`, parse `git remote get-url origin` via the shared lib.
     A Forgejo/Gitea remote (matched against `tea login list`) routes PR/issue
     cleanup through `tea` (`tea pull list/close`, `tea issues list/close`).
     Unknown hosts skip the remote-domain audits with a loud notice.
5. **Check working-tree state**: Capture `git status --porcelain` and
   `git stash list`. Record whether the current branch has unpushed commits.
6. **Initialize progress tracking** with the task tools (one entry per phase).
7. **Create audit directory**: `.git-cleanup/` at the repo root. Report and
   per-domain finding files land here.
8. **If `--dry-run` was passed alongside `--apply`**: Abort — they conflict.

## Phase 1: Collect Raw Git State

Run only commands needed for the requested scope. Prefer porcelain / `--format`
flags that emit machine-readable output.

- **Branches**: `git for-each-ref refs/heads/ --format='%(refname:short)|%(upstream)|%(upstream:track)|%(committerdate:iso8601)|%(objectname)'`
- **Remote-tracking prune candidates**: `git remote prune <remote> --dry-run`
  for each remote from `git remote`.

<!-- ycc:verbatim-block:begin -->

- **Worktrees**: `git worktree list --porcelain`. Flag entries whose `worktree`
  path no longer exists, whose branch is `[gone]`, or which sit under a legacy
  global ycc root (`~/.claude-worktrees/`) instead of a repo-local managed root.
  The managed roots under the repo root are `.claude/worktrees/`,
  `.opencode/worktrees/`, `.codex/worktrees/`, `.cursor/worktrees/`,
  `.omp/worktrees/` and `.agents/worktrees/`; every runtime checks all of them.
  Entries under `~/.omp/wt` are OMP-managed (`omp worktree clear`): report only,
  never delete.

<!-- ycc:verbatim-block:end -->

- **Stashes**: `git stash list --date=iso`. Parse the date from each entry.
- **Tags**: `git for-each-ref refs/tags/ --format='%(refname:short)|%(creatordate:iso8601)|%(objectname)'`
  then `git ls-remote --tags <remote>` to find local-only tags.
- **PRs** (when host available): List merged-but-branch-still-local and stale
  open PRs authored by the current user. Example GitHub via `gh`:
  `gh pr list --state=all --author=@me --json number,title,state,headRefName,baseRefName,updatedAt,isDraft,mergedAt,closedAt`.
- **Issues** (when host available): `gh issue list --state=open --author=@me --json number,title,updatedAt,labels`
  filtered by `updatedAt < now - stale-days`.
- **Release model** (only when `present=1`):
  - **Release branches**: every local `release/*` branch
    (`git for-each-ref refs/heads/release/ --format='%(refname:short)'`) and
    every remote one (`git for-each-ref refs/remotes/ --format='%(refname:short)'`,
    keeping names whose part after `<remote>/` starts with `release/`).
  - **Sync-merge candidates**: branch names (local or remote, excluding
    `RELEASE_TRUNK`) containing `sync`, and, for every other local branch and
    remote-tracking branch, merge commits newer than `stale-days` that are not
    on the trunk and whose subject reads like a trunk sync:

    ```bash
    git log --merges --since="<stale-days> days ago" --format='%h|%s' -E \
      --grep="^Merge (remote-tracking )?branch '?([A-Za-z0-9._-]+/)?(main|master|trunk|develop|<RELEASE_TRUNK>)'? into" \
      "origin/<RELEASE_TRUNK>..<branch>"
    ```

    Rules and rationale (read when classifying a branch, stash, or worktree as active or deletable):
    `${CLAUDE_PLUGIN_ROOT}/skills/git-cleanup/references/active-code-rules.md`
    (R9, R10).

## Phase 2: Active-Code Analysis

This is the gating phase. **Never** recommend deletion of a resource that
Phase 2 flags as active. Read
`${CLAUDE_PLUGIN_ROOT}/skills/git-cleanup/references/active-code-rules.md` before
classifying any candidate; it holds rule rationales, edge cases, and the full decision matrix.

For each candidate branch, worktree, PR, and issue, mark as **active** if any
of the following is true:

1. **Recent commits**: Tip commit is newer than `stale-days` days.
2. **Unpushed work**: The local branch has commits not in its upstream (or no
   upstream is configured and commits are ahead of the default branch).
3. **Uncommitted / stashed changes**: For worktrees — dirty working tree
   (`git -C <worktree> status --porcelain` non-empty) or a stash attached to
   the branch.
4. **Referenced in open PR**: The branch is the `headRef` of any open PR, OR
   the `baseRef` of an open PR (never touch a base branch).
5. **Referenced in active code**: Grep the tracked working tree for the branch
   name — `git grep -l -w <branch-name>` — in docs, issue templates, CI config,
   release notes, and comments. A textual reference in tracked files means the
   branch is load-bearing.
6. **Linked to active issues**: PR/issue body references an open issue updated
   within `stale-days`, or has the `status:in-progress` / `status:needs-info`
   label family defined by this repo's taxonomy.
7. **Protected name**: Matches `main|master|develop`, the default branch, or
   any `--protect=<pattern>`. When `present=1`, also `RELEASE_TRUNK` and every
   branch in `RELEASE_MAINTENANCE` (local or remote).
8. **Recent reflog activity**: `git reflog show <branch>` shows motion within
   `stale-days`.

Candidates that fail every check become **stale** — eligible for cleanup.
Record the reason per candidate so the user can audit the decision.

**Release model** (only when `present=1`; see R9 and R10 in the rules file):

- **Retired maintenance branch**: a local or remote `release/*` branch that is
  not in `RELEASE_MAINTENANCE` and not protected (rule 7, or rule 4 as an
  open-PR base) is classified as retired, never as Stale — even when rules 1–8
  would call it stale or active (`RELEASING.md` mentioning a frozen branch does
  not make it active).
  Branches listed in `RELEASE_FROZEN` are retired too and are flagged
  "frozen by RELEASING.md".
- **Sync-merge anti-pattern**: branches named like `*sync*` and merge commits
  collected in Phase 1 are informational findings. They never change a
  candidate's classification and never produce a cleanup command.

## Phase 3: Produce the Audit Report

Write `.git-cleanup/report.md` with sections keyed by domain:

- **Protected** — always-kept resources and why (default branch, open-PR bases,
  user-protected patterns).
- **Active (skip)** — candidates gated out by Phase 2, each with the specific
  rule that matched.
- **Stale (eligible)** — candidates safe to clean, grouped by domain, with the
  exact `git` / `gh` / `glab` command that would remove each one.
- **Ambiguous (ask)** — edge cases (e.g., branch has unpushed commits **and**
  hasn't been touched in 6 months; worktree with clean tree but branch `[gone]`).
- **Retired maintenance branch** (only when `present=1`) — `release/*` branches
  outside `RELEASE_MAINTENANCE`, each marked local or remote, with
  "frozen by RELEASING.md" on those listed in `RELEASE_FROZEN`. For each, show
  the archive command to run first and the deletion command, for example:
  `git tag archive/release/0.3 release/0.3` then `git branch -d release/0.3`;
  for a remote branch, `git tag archive/release/0.3 origin/release/0.3`,
  `git push origin archive/release/0.3`, then
  `git push origin --delete release/0.3`.
- **Anti-patterns (informational)** (only when `present=1`) — sync-named
  branches and sync-merge commits (hash, subject, branch), with a pointer to
  the branching-model rule "Never merge one long-lived branch into another"
  and the fix: rebase the topic branch onto `origin/<RELEASE_TRUNK>` instead,
  and move fixes to maintenance branches with `/ycc:backport`.
- **Host-API notes** — PRs/issues surfaced from GitHub/GitLab with current
  state and decision rationale.

Also emit a one-screen summary to stdout: counts per category and the path to
the full report. If `--report-only`, **STOP** here.

## Phase 4: User Decision Gate

Present the summary via AskUserQuestion. Offer structured choices:

- **View full report** — print `.git-cleanup/report.md` in chunks.
- **Apply all stale (skip ambiguous)**.
- **Apply all stale + resolve ambiguous interactively**.
- **Choose per domain** — branches only, worktrees only, etc.
- **Cancel** — exit without changes.

For ambiguous items, re-prompt per item with the evidence summary and the
exact command that would run.

Retired maintenance branches are never part of "Apply all stale". Each one
needs its own explicit confirmation, and the prompt offers to create the
`archive/<branch>` tag first (default: yes). Anti-pattern findings have no
action to confirm.

If `--dry-run` is active (default), **STOP** here — do not invoke Phase 5 even
if the user clicks "Apply". Tell them to rerun with `--apply`.

## Phase 5: Execute (only with `--apply`)

For each approved item, in this order (safest first):

1. **Remote-tracking prune**: `git remote prune <remote>`.
2. **Worktrees**: `git worktree remove <path>`. If missing on disk, use
   `git worktree prune`.
3. **Local branches**: `git branch -d <name>` (never `-D` unless the branch
   has been merged to the default branch or its upstream is `[gone]` AND the
   user explicitly confirmed in Phase 4). For a confirmed retired maintenance
   branch, create and (for a remote branch) push the `archive/<branch>` tag
   first when the user accepted it; delete a remote one with
   `git push <remote> --delete <branch>` only after that tag exists.
4. **Local-only tags**: `git tag -d <name>`.
5. **Stashes**: `git stash drop stash@{N}`. Drop highest-indexed first to keep
   indices stable during the sweep.
6. **PRs**: close via host CLI / MCP (`gh pr close` or GitLab equivalent). Add
   a closing comment referencing staleness if repo conventions require one.
7. **Issues**: close with a stale-label comment or add a `wontfix` / stale
   label from the repo's taxonomy — never invent ad-hoc labels.

Record each action (success / failure / skipped) in `.git-cleanup/actions.log`.
On any individual failure: log and continue. On systemic failure (e.g., auth
error): abort and report.

## Phase 6: Verification and Summary

1. **Re-run Phase 1 collection** for the targeted domains and diff against the
   pre-execution snapshot. Confirm each approved item is gone.
2. **Print final summary**: counts removed per domain, any skipped items with
   reason, and the paths to `.git-cleanup/report.md` and `actions.log`.
3. **Do NOT commit** anything automatically — cleanup output lives under
   `.git-cleanup/` which should be added to `.gitignore` by the user.

## Host-Specific Notes

- **GitHub**: Prefer `mcp__github__*` tools when present. Fall back to `gh`.
  Use `gh pr list --search` for richer stale-age filters when supported.
- **GitLab**: Use `glab` with equivalent subcommands (`glab mr list`,
  `glab issue list`). Self-hosted GitLab URLs resolve via `glab` config.
- **Neither CLI available**: Skip `--prs` and `--issues` domains with a loud
  notice; local cleanup still proceeds.

## Subagent Delegation

For large repos where Phase 2's active-code scan is expensive, delegate to
`ycc:git-cleanup` agent via the Agent tool. The agent performs the read-only
audit (Phases 1-3) and returns the structured report inline without writing
files; this skill writes it to `.git-cleanup/report.md` (Phase 3) and
orchestrates Phases 4-6. Pass the Phase 1 collection commands inline in the dispatch
prompt, along with the invocation options and Phase 0 `release-state.sh get` output,
so the agent can collect each in-scope domain and apply the same protected set and
release-model rules (a malformed state has already stopped the run in Phase 0).

## Important Notes

- **Dry-run by default**. Destruction requires `--apply` **and** interactive
  approval.
- **Never touch the default branch, protected branches, or open-PR bases.**
  With a `RELEASING.md`, that includes the state's trunk and maintenance
  branches.
- **Retired maintenance branches are never auto-deleted.** Suggest the
  `archive/<branch>` tag first and require per-item confirmation.
- **A malformed `RELEASING.md` state block stops the audit** with the parse
  error and a pointer to `/ycc:release-model --audit`.
- **Never `git branch -D`** without explicit per-item confirmation.

<!-- ycc:verbatim-block:begin -->

- **Worktrees under any repo-local managed root** (`.claude/`, `.opencode/`,
  `.codex/`, `.cursor/`, `.omp/` or `.agents/` followed by `worktrees/`) are fair
  game per this repo's convention. Legacy worktrees under `~/.claude-worktrees/`
  should be reported and, if the user confirms, relocated or removed. Never delete
  worktrees under `~/.omp/wt`; OMP manages them (`omp worktree clear`).

<!-- ycc:verbatim-block:end -->

- **Respect the repo's label taxonomy**. Do not invent stale/wontfix labels.
- **No secrets**. Do not log tokens or API responses containing credentials.
- **Ambiguous items are always surfaced**, never auto-deleted.
