---
name: new-branch
description: "Use when starting new work that needs a branch — creates and switches to a categorized branch from a description, ticket/issue link, or current uncommitted/ahead-of-base work. Works before or after implementation begins. Invoke when the user says 'new branch', 'start a branch', or begins a new task."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before creating or switching to the branch (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/git-hosts.md`
- `<project-root>/docs/issue-trackers.md` (only when a ticket/issue link argument is provided)

# Branch From Argument or Work

Create and switch to a categorized branch. The branch name is derived from an argument (description or ticket/issue link) when provided, otherwise from current uncommitted or ahead-of-base work. Git changes are always validated regardless of argument type.

## Operations

| Operation | Tool (see `<project-root>/docs/git-hosts.md`) | CLI fallback per `<project-root>/docs/git-hosts.md` |
|-----------|--------------|--------------|
| Load change state | git host change scan (see `<project-root>/docs/git-hosts.md` in the project root) | `git branch --show-current` + `git status --short` + `git diff --cached --stat` + `git diff --stat` + `git log origin/<branch>..<branch> --oneline` |
| Pull, create, publish | git host branch create (see `<project-root>/docs/git-hosts.md` in the project root, with `branch_name`) | `git pull origin <branch>` + `git checkout -b <cat>/<slug>` + `git push -u origin <new-branch>` |

Follow `<project-root>/docs/git-hosts.md` in the project root for all git/gh operations.

### 1. Interpret Arguments

Classify the invocation argument (if any) into one of three modes. Store `<arg-mode>` (`description` | `ticket` | `none`) and `<branch-context>`.

- **Description** — free-form text that is not a URL/issue link. Use the text directly as `<branch-context>`. Set `<arg-mode>` = `description`.
- **Ticket/issue link** — a URL or identifier referencing a ticket/issue (e.g. GitHub issue, Linear, Jira). Set `<arg-mode>` = `ticket`. Extract ticket content via the issue tools documented in `<project-root>/docs/issue-trackers.md` in the project root (title, summary, labels/type). Store the distilled content as `<branch-context>`. If extraction fails, fall back to any slug-relevant fragment in the link (issue number, path slug) and note the gap.
- **None** — no argument provided. Set `<arg-mode>` = `none`. `<branch-context>` is empty; the branch name will be derived from git changes (Step 2).

### 2. Load Changes

Always run, regardless of `<arg-mode>`. Git changes are validated every invocation.

If a pre-scan was forwarded, use `<current-branch>`, `<uncommitted>`, `<ahead-commits>`, `<change-summary>`, and `<branch-category>` directly. Skip to Step 3.

Otherwise:

Step 1: Load change state via the operations table above. Store `<current-branch>` and `<uncommitted>`.

Step 2: If `<uncommitted>` is empty, check commits ahead using `origin/<current-branch>..<current-branch>`. Store `<ahead-commits>`.

Step 3: Analyze scope (used for validation and as a fallback branch-name source when `<arg-mode>` = `none`):
- Primary scope: `<uncommitted>`; fallback: `<ahead-commits>`.
- Group into logical themes. Summarize what and why, not how.
- Store as `<change-summary>`.

### 3. Check Blockers

- No argument and nothing to branch from: `<arg-mode>` = `none` AND `<uncommitted>` AND `<ahead-commits>` all empty → STOP: "Nothing to branch from."
- Already on work branch: `<current-branch>` starts with `feature/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`, `feat/`, `bugfix/`, `hotfix/`, `perf/`, `build/`, or `ci/` → STOP: "Branching skipped because the current branch already looks like a work branch."

Note: When `<arg-mode>` is `description` or `ticket`, missing git changes do NOT block — the branch is created from the argument and the empty change state is recorded as validation output.

### 4. Determine Category and Slug

- If `<branch-category>` was forwarded from pre-scan, reuse it; only generate the slug.
- Otherwise choose a category:
  - When `<arg-mode>` = `ticket`, infer from ticket type/labels first; fall back to `<change-summary>` and `<branch-context>`.
  - When `<arg-mode>` = `description`, infer from `<branch-context>`; fall back to `<change-summary>`.
  - When `<arg-mode>` = `none`, infer from `<change-summary>` and `<branch-context>`.
  - Categories:
    - `feature` — new functionality
    - `fix` — bug fixes
    - `refactor` — restructuring without behavior change
    - `docs` — documentation
    - `test` — test-only
    - `chore` — tooling, dependencies, maintenance
    - `perf` — performance
    - `build` — build system
    - `ci` — CI/CD
- Store `<branch-category>`.
- Generate a concise kebab-case slug (2-4 words, descriptive). Source priority:
  - `<arg-mode>` = `description` or `ticket` → derive from `<branch-context>`; consult `<change-summary>` only to disambiguate.
  - `<arg-mode>` = `none` → derive from `<change-summary>` and `<branch-context>`.
- Store as `<branch-slug>`.

### 5. Pull Latest from Remote

Pull `origin/<current-branch>` via git host tool or CLI. If the pull fails (diverged history, no remote tracking), continue with the current state and note it in the output.

### 6. Create and Checkout Branch

Create `<branch-category>/<branch-slug>` via git host branch create (see `<project-root>/docs/git-hosts.md` in the project root) or `git checkout -b` per `<project-root>/docs/git-hosts.md`. If the branch exists, retry once with a numeric suffix (`-2`). Store as `<new-branch>`.

### 7. Publish Branch to Remote

Push with upstream via git host branch create (see `<project-root>/docs/git-hosts.md` in the project root) or `git push -u origin <new-branch>` per `<project-root>/docs/git-hosts.md`. `git push` only pushes committed changes; uncommitted changes stay local. Store `<published>` as `true` or `false`. Output the new branch name when created.

