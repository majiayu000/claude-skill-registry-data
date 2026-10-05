---
name: mav-git-workflow
description: Git branching strategy, commit conventions, merge conflict handling, and branch lifecycle. Implements a simplified Gitflow with protected branches and conventional commits. Covers worktree-based multi-story workflows and cross-references stacked-PR handling.
user-invocable: false
disable-model-invocation: true
---

# Git Workflow

A trunk-based strategy for all development work. This skill defines how branches, commits, and merges are managed.

## Remote Repository Requirement

A configured remote repository is **mandatory**. Local-only git is a hard fail — all projects must push to a remote hosting service (GitHub, GitLab, Bitbucket, Azure Repos, etc.).

### Validation

Before starting any work, verify a remote exists:

```bash
git remote -v
```

If no remote is configured:
1. **Stop work** — do not proceed with feature branches, commits, or PRs
2. **Notify the user** — report that no remote repository is configured and that this is a hard requirement
3. **Do not create a remote autonomously** — the user must set up the remote repository and configure the origin

A project with no remote cannot use protected branches, pull requests, or CI/CD — all of which are foundational to this workflow.

## Worktrees — required for multi-story workflows

Maverick's multi-story workflows (`do-epic`) run each story in
its own git worktree under `.maverick/worktrees/`. This keeps in-flight
stories isolated from each other and from the main checkout.

### Worktree precondition

Before entering `do-epic` (or any flow that relies on
worktrees), verify the capability:

```bash
uv run maverick worktree list
```

If this fails, the workflow aborts with a hard error. Worktrees require:

- A non-shallow clone (`git rev-parse --is-shallow-repository` returns
  `false`). Shallow clones cannot create new worktrees.
- A git version that supports `git worktree add` (2.15+).
- Filesystem write access under `.maverick/worktrees/`.

### Worktree lifecycle

One worktree per story, created off the resolved base branch:

```bash
uv run maverick worktree create <branch> [--base <base-branch>]
```

On every exit path — merge, eject, abort — destroy the worktree:

```bash
uv run maverick worktree destroy <path>
```

Leaving stale worktrees inflates disk usage and confuses future
`worktree list` reads. The only reason to keep a worktree after exit is
if a PR was ejected and the human may want to inspect the in-flight
state — note the path in the eject comment.

### Repo-specific post-create setup

A freshly created worktree shares the main checkout's `.git`, but **not**
its dependency installs, generated files, or untracked secrets. Many repos
need to materialise those before the first build can run inside the new
worktree (e.g. `pnpm install`, `pip install -e .`, symlinking `.env`).

If `.maverick/config.json` declares `hooks.worktree_post_create`, the CLI
runs that script after `git worktree add` succeeds. The hook receives:

- `$1` — absolute worktree path
- `MAVERICK_WORKTREE_PATH` — same as `$1`
- `MAVERICK_BRANCH` — newly created branch name
- `MAVERICK_BASE_BRANCH` — branch the new branch was forked from
- `MAVERICK_REPO_ROOT` — main checkout's absolute path

A non-zero exit, missing script, or non-executable script causes
`maverick worktree create` to exit non-zero with a clear error. The
worktree is **left on disk** so an engineer can inspect what the hook
produced — clean up with `maverick worktree destroy` once diagnosed.

Example wiring (`.maverick/config.json`):

```json
{
  "hooks": {
    "worktree_post_create": "scripts/worktree-setup.sh"
  }
}
```

The hook is optional. Repos that don't declare one see exactly today's
behaviour. The Maverick CLI stays language-agnostic — the hook can be
any executable.

### Stacked branches

If a story depends on a sibling story whose PR is still open, stack per
`mav-stacked-prs`. The worktree is created off the sibling
branch instead of the default branch. The retarget guard in
`mav-stacked-prs` handles the sibling merging.

## Branch Strategy

The branching layout is driven by the per-project config in
`.maverick/config.json` → `git_workflow`. Resolve the key branches
with the CLI:

```bash
STORY_BASE=$(uv run maverick git-workflow story-base)   # branch new work off this
PR_TARGET=$(uv run maverick git-workflow pr-target)      # gh pr create --base target
```

Example layout (trunk-based, story_base = main):

```
stable (what end users clone; CI-managed; fast-forwarded to the latest release tag)
main (trunk — carries -dev between releases; tagged at each release)
  ├── feat/42-add-export
  ├── fix/57-login-crash
  ├── chore/63-update-deps
  └── release/<version> (short-lived; exists only long enough to cut a release)
```

Example layout (Gitflow-style, story_base = develop):

```
main (production; tagged at each release)
develop (integration — carries -dev between releases)
  ├── feat/42-add-export
  ├── fix/57-login-crash
  └── chore/63-update-deps
```

### Branch Roles

| Branch | Purpose | Who commits | Protected |
|---|---|---|---|
| `stable` (if present) | What end users install — always points at the most recent release tag | Fast-forwarded by CI only; never by humans | Yes (CI-only) |
| Default branch (e.g. `main`) | Trunk or production branch — tagged at each release | Merge from story/release branches via PR only | Yes |
| Story base (e.g. `develop`, or same as default) | Integration branch feature branches are created from and PR'd back to | Merge from feature/fix/release branches via PR only | Yes |
| Feature/fix/chore branches | Active development | Claude Code and developers | No |
| `release/<version>` | Short-lived release prep — bumps version, updates CHANGELOG | Created by release scripts | No |

### Rules

- **Never commit directly to the story base or default branch**. All changes reach them via pull request.
- **All work happens on short-lived branches** created from `$STORY_BASE` and PR'd back to `$PR_TARGET`.
- **One branch per issue/task**. Do not combine unrelated work on a single branch.
- **Release branches are ephemeral**. Created by the release script, deleted after the release PR merges.
- **Always pass `--base $PR_TARGET`** explicitly when creating PRs via `gh pr create` — do not rely on the repository's default branch setting, which may differ from the PR target.

## Branch Naming

Format: `<type>/<issue-number>-<short-description>`

### Deriving the Type

Resolve the branch prefix from the project config:

```bash
PREFIX=$(uv run maverick git-workflow branch-prefix <label>)
```

The CLI maps issue labels to branch prefixes per the project's
`git_workflow.branch_prefixes` config. Default mapping when not
overridden:

| Label or keyword | Branch prefix |
|---|---|
| `bug`, `fix`, `defect` | `fix/` |
| `feature`, `enhancement` | `feat/` |
| `docs`, `documentation` | `docs/` |
| `refactor`, `tech-debt` | `refactor/` |
| `chore`, `maintenance`, `deps` | `chore/` |
| `test`, `testing` | `test/` |
| Default (when unclear) | `feat/` |

### Deriving the Description

- Use 2-4 lowercase words separated by hyphens
- Describe the outcome, not the method
- Keep it short — branch names appear in logs and PRs

**Good:** `feat/42-add-rubric-export`, `fix/57-prevent-login-crash`
**Bad:** `feature/issue-42-implement-the-new-rubric-export-feature-for-teachers`

## Creating a Branch

```dot
digraph branch {
    "Identify base branch" [shape=box];
    "Pull latest" [shape=box];
    "Derive branch name" [shape=box];
    "Create branch" [shape=box];
    "Verify clean state" [shape=diamond];
    "Stash or commit first" [shape=box];

    "Identify base branch" -> "Pull latest";
    "Pull latest" -> "Verify clean state";
    "Verify clean state" -> "Derive branch name" [label="clean"];
    "Verify clean state" -> "Stash or commit first" [label="uncommitted changes"];
    "Stash or commit first" -> "Derive branch name";
    "Derive branch name" -> "Create branch";
}
```

### Identify the Base Branch

The base branch comes from the project config — resolve it via the CLI:

```bash
STORY_BASE=$(uv run maverick git-workflow story-base)
```

This reads `git_workflow.story_base` from `.maverick/config.json`
(default: `main`). Do not auto-detect or hard-code the branch — the
config is the single source of truth, written once by `maverick init`.

### Base Branch Freshness (rule)

Any workflow that reads from the main checkout before opening a
worktree — typically the design / planning subagents in
`do-issue-solo` / `do-issue-guided` / `do-epic` Phase 1 — must
refresh the local base branch against origin first. A stale local
base lets pre-resolved ambiguities slip into the analyst's design
pass and surfaces as phantom blockers (#102).

The pattern advances the local ref without forcing the user out of
whatever branch they happen to be on:

```bash
STORY_BASE=$(uv run maverick git-workflow story-base)
git fetch origin "$STORY_BASE"
CURRENT=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT" = "$STORY_BASE" ]; then
    git pull --ff-only origin "$STORY_BASE"
else
    # Update the local ref directly; safe because $STORY_BASE is not the
    # checked-out branch (git refuses to fetch onto the current branch).
    git fetch origin "$STORY_BASE:$STORY_BASE"
fi
```

Both forms refuse a non-fast-forward — that means the local base has
commits that are not on origin, which violates trunk-based discipline.
Halt and report to the user; do not auto-rebase or force-update.

### Create the Branch

```bash
git checkout $STORY_BASE && git pull origin $STORY_BASE && git checkout -b $BRANCH_NAME
```

## Versioning

Releases follow **SemVer**; conventional-commit types drive the bump
(`fix:` → patch, `feat:` → minor, breaking change → major). Version
bumps land only via release commits/branches — never ad-hoc edits to
version files mid-feature.

## Conventional Commits

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<optional scope>): <description> (#<issue-number>)
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |
| `style` | Formatting, whitespace (no logic change) |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration changes |

### Rules

- **Always reference the issue number** in the commit message: `(#42)`
- **Use imperative mood**: "add export" not "added export" or "adds export"
- **Keep the first line under 72 characters**
- **One logical change per commit** — do not batch unrelated changes

### Examples

```
feat: add rubric export endpoint (#42)
fix: prevent crash when rubric is empty (#57)
test: add integration tests for grading service (#42)
refactor: extract token cost calculation into utility (#63)
chore: update vitest to v3.1 (#71)
```

### Push cadence — after every task

Commit and push **after every task**, not only at end of story. This
makes work durable across machine death: a takeover instance can fetch
the branch from origin and resume at the next unchecked task. See
`mav-durability-on-gh` for the rationale and the worked
pattern.

### Multi-line Commits

For commits that need more context:

```
feat: add rubric export endpoint (#42)

Adds a new GET /api/assessments/:id/export endpoint that returns
the assessment rubric as a downloadable CSV file. Includes proper
content-type headers and filename disposition.
```

## Merge Conflicts

```dot
digraph conflicts {
    "Conflict detected?" [shape=diamond];
    "Trivial conflict?" [shape=diamond];
    "Auto-generated files only?" [shape=diamond];
    "Resolve automatically" [shape=box];
    "Flag for human intervention" [shape=box];
    "Continue working" [shape=box];

    "Conflict detected?" -> "Trivial conflict?" [label="yes"];
    "Conflict detected?" -> "Continue working" [label="no"];
    "Trivial conflict?" -> "Auto-generated files only?" [label="yes"];
    "Trivial conflict?" -> "Flag for human intervention" [label="no"];
    "Auto-generated files only?" -> "Resolve automatically" [label="yes — lock files, generated code"];
    "Auto-generated files only?" -> "Flag for human intervention" [label="no"];
    "Resolve automatically" -> "Continue working";
}
```

### When to Resolve Automatically

Only resolve conflicts in **auto-generated files** where the resolution is unambiguous:
- Lock files (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`) — regenerate with `pnpm install` / `npm install`
- Generated type files — regenerate with the appropriate codegen command

### When to Flag for Human Intervention

Flag all other conflicts for human review. Report clearly:
- Which files have conflicts
- What the conflicting changes are (both sides)
- Why the conflict likely occurred (e.g., "both branches modified the grading calculation")

```bash
# Show conflicting files
git diff --name-only --diff-filter=U

# Show the conflict markers in a specific file
git diff -- path/to/file.ts
```

**Never:**
- Silently resolve conflicts in application code
- Choose "ours" or "theirs" without understanding the intent of both sides
- Delete one side of a conflict to make it go away

## Branch Cleanup

After a pull request is merged, clean up the feature branch.

### Local Cleanup

```bash
# Switch back to the base branch
git checkout $BASE_BRANCH && git pull origin $BASE_BRANCH

# Delete the local feature branch
git branch -d $BRANCH_NAME
```

Use `-d` (not `-D`) — this will refuse to delete if the branch has unmerged changes, which is a safety check.

### Remote Cleanup

GitHub can be configured to auto-delete branches after PR merge. If not:

```bash
git push origin --delete $BRANCH_NAME
```

### Bulk Cleanup of Merged Branches

For cleaning up stale local branches that have been merged:

```bash
STORY_BASE=$(uv run maverick git-workflow story-base)

# List merged branches (excluding the story base)
git branch --merged $STORY_BASE | grep -vE "^\*|$STORY_BASE"

# Delete them
git branch --merged $STORY_BASE | grep -vE "^\*|$STORY_BASE" | xargs git branch -d
```

## Pulling Updates

When your feature branch falls behind the base branch:

```bash
# Preferred: rebase onto latest base (clean history)
git fetch origin && git rebase origin/$BASE_BRANCH

# Alternative: merge base into feature (preserves history)
git fetch origin && git merge origin/$BASE_BRANCH
```

Use rebase for branches with only your own commits. Use merge if the branch has been shared or has a complex history. If uncertain, ask the user.

## Pre-Flight Checks

Before any branch operation, verify the working tree is clean:

```bash
git status --porcelain
```

If there are uncommitted changes:
- **Commit them** if they are part of the current work
- **Stash them** if they are unrelated: `git stash push -m "WIP: description"`
- **Ask the user** if you are unsure what to do with them

<!-- maverick-plugin-version: 4.0.2-dev -->
