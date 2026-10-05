---
name: agent-migrate
description: One-shot migration of an existing .workflow/ markdown workflow (BACKLOG.md / TODO.md / DONE.md / plans/ / tasks/) into a freshly-configured GitHub Project board. Idempotent, produces backup + mapping report. Run from project root with /agent-migrate.
---

# Agent Migrate Skill

When invoked with `/agent-migrate`, take this project's existing markdown
workflow files and push them into a GitHub Project board. After this skill
finishes, `agent.yaml` will have `workflow.backend: github_project` and
all subsequent agent runs will go through **board-man**.

This is a one-shot, opt-in migration. It is safe to re-run (idempotent —
already-migrated items are detected and skipped). It produces a complete
backup and a mapping report so the user can audit every change.

**You never write application code.** Your job is purely to translate
markdown state into board state.

---

## Hard rules

- Do NOT delete any source markdown until Step 8 (Archive), and only after
  explicit user confirmation.
- Do NOT push or merge anything to git remotes. agent.yaml changes and any
  archive `git mv` operations are staged but not committed by this skill —
  the user reviews and commits.
- Every `gh` write goes through **board-man**. This skill itself never
  shells out to `gh project` / `gh issue` / `gh api graphql`. Spawn
  board-man via `Agent(subagent_type="board-man", prompt="<op> <args>")`.
- A `200ms` sleep between board-man write calls in Step 4 to keep API
  rate limits comfortable.

---

## Step 0: Pre-flight

1. **gh auth.** Run `gh auth status`. If it fails, stop and instruct the user
   to run `gh auth login`.
2. **gh project scope.** Verify the token has the `project` scope (look for
   `project` in the token-scopes line of `gh auth status`). If missing,
   stop and tell the user to run `gh auth refresh -s project`.
3. **agent.yaml exists.** Read `agent.yaml`. If it does not exist, stop and
   tell the user to run `/agent-init` first.
4. **Already-migrated check.** If `agent.yaml` already has
   `workflow.backend: github_project`, ask "This project is already on the
   github_project backend. Re-run anyway? [y/N]". On no, exit. On yes,
   continue (board-man will dedupe writes via `find-issue-by-marker`).
5. **Project info.** Prompt the user for:
   - GitHub owner (user or org). Default: parse from `git remote get-url origin`.
   - Repo (`owner/repo`). Default: parse from `git remote get-url origin`.
   - Project number. Leave blank to create a new project.
   - Project title (only used if creating). Default:
     `<project.name from agent.yaml> board`.
6. **Provision the project.** Run:
   ```
   <framework>/scripts/board-man-setup.sh --owner <o> --repo <r> [--number <n>] [--title <t>] --project-root <pwd>
   ```
   This creates the project (if no number given), provisions all labels
   (FEATURE, CHANGE, BUG, TASK, parallel-group/0..9), ensures Status
   options BACKLOG/READY/TODO/IN-PROGRESS/DONE, ensures the Parallel
   Group number field, and writes `.workflow/temp/.board-man-cache.json`.
   Locate `<framework>` via `$CLAUDE_AGENT_HOME` if set, otherwise default
   to `$HOME/.claude-agent` (the install.sh default), with a fallback to
   `dirname` of this skill's location traced two levels up.
   If the script exits non-zero, surface the stderr to the user and stop.

---

## Step 1: Snapshot

Create a timestamped backup directory:
```
.workflow/migrate-backup-<YYYY-MM-DDTHH-MM-SS>/
```

Copy (do not move yet) the following into it, preserving relative structure:
- `<workflow.backlog_file>` (default `.workflow/BACKLOG.md`)
- `<workflow.todo_file>` (default `.workflow/TODO.md`)
- `<workflow.done_file>` (default `.workflow/DONE.md`)
- `<workflow.bugs_file>` (default `.workflow/BUGS.md`) — if it exists
- `<workflow.plans_dir>/` (default `.workflow/plans/`) — recursively
- `<agents.tasks_dir>/` (default `.workflow/tasks/`) — recursively

Write a `MANIFEST.md` in the backup dir:
```
# Migration backup — <ISO timestamp>

| Source | Lines | SHA-256 |
|--------|-------|---------|
| BACKLOG.md | <wc -l> | <sha256> |
| TODO.md | <wc -l> | <sha256> |
| ...     | ...     | ...     |
```

This guarantees the user can diff or restore later.

---

## Step 2: Build the ledger

Parse the source markdown into an in-memory ledger of items to migrate. The
shape:

```
{
  "feature_items": [
    {"title": "...", "type": "FEATURE", "gh_marker": "[GH #123]" | null,
     "source_line": "BACKLOG.md:14", "body": "<original line + any trailing context>",
     "matched_plan": null, "matched_tasks": [], "destination_issue": null}
  ],
  "change_items":  [...],
  "bug_items":     [...],
  "todo_items":    [...],
  "done_items":    [...],
  "plan_files":    [
    {"slug": "add-auth", "path": "plans/add-auth.md", "body": "<full file>",
     "matched_item": null}
  ],
  "task_files":    [
    {"slug": "auth-backend", "path": "tasks/auth-backend.md",
     "metadata": {"Type": "...", "Status": "...", "Repo": "...",
                  "Parallel Group": 1, "Branch": "...", "Source Item": "..."},
     "body": "<full file>", "matched_parent": null}
  ]
}
```

Parsing rules:

**BACKLOG.md / TODO.md / DONE.md:**
- Recognize `## Features`, `## Changes`, `## Issues` (case-insensitive)
  section headers. Each line of form `- [ ] <text>` becomes an item with
  type FEATURE / CHANGE / BUG respectively. Items in TODO.md and DONE.md
  default to FEATURE unless their `[GH #N]` marker resolves to an existing
  issue with a different label, in which case use that label.
- A leading `[GH #N]` token on the line populates `gh_marker`.
- Multi-line item bodies (continuation lines indented under the bullet)
  are folded into the item's `body` field.

**plans/*.md:**
- One file = one plan. The slug is the basename without `.md`.
- The H1 header (`# <something>`) is the plan title. Use it for matching.

**tasks/*.md:**
- One file = one task. The slug is the basename without `.md`.
- Header is `# Task: <task-name>`. Body has bulleted YAML-ish metadata
  (Type, Status, Repo, Parallel Group, Branch, Source Item, Dependencies).
  Parse each `- **Field**: value` line.

**Plan ↔ Item matching (fuzzy):**
For each plan, lowercase its slug and the title of every backlog/todo/done
item, strip non-alphanumerics. The item with the closest match (by
substring or Levenshtein distance ≤ 4) is the candidate. If no candidate
within tolerance, leave `matched_item: null` and ask the user in Step 3.

**Task ↔ Parent matching:**
The task's `Source Item` field is the join key. Lowercase + strip and look
up against item titles. If no match, leave `matched_parent: null` for
Step 3.

---

## Step 3: Resolve ambiguities (interactive)

For each unmatched plan, ask the user:
> `plans/<slug>.md` does not match any backlog/todo/done item.
> (a) Skip — leave the plan file in place, do not migrate.
> (b) Create a new FEATURE issue titled "<inferred from H1>" and attach this plan to it.
> (c) Attach to an existing item: <numbered list of items>
> Choice [a/b/c]?

For each unmatched task, ask:
> `tasks/<slug>.md` has Source Item "<source>" which does not match any feature.
> (a) Skip — do not migrate.
> (b) Create a synthetic parent FEATURE titled "<task slug rolled up>" and attach this task as a sub-issue.
> (c) Attach to an existing item: <numbered list>
> Choice [a/b/c]?

For each item that appears in DONE.md, confirm the import policy once
(applies to all done items):
> Import DONE.md items as closed issues with status DONE? [Y]
> Alternative: skip / migrate as open in BACKLOG. Choice [Y/s/o]?

If the user picks (a) for any item, mark it `migrate: false` in the ledger
and surface it in the final mapping report as "skipped".

---

## Step 4: Push to GitHub (the writes)

Order matters — parents before plans before children. Between each
board-man write call, sleep 200ms (`sleep 0.2`) for rate-limit hygiene.

### 4a. Parents

For every `feature_items[]`, `change_items[]`, `bug_items[]`,
`todo_items[]`, `done_items[]` with `migrate: true` and no
`destination_issue` yet:

1. Check if it's already on the board:
   ```
   board-man find-issue-by-marker "<title-or-gh-marker>"
   ```
   If found, set `destination_issue` to that issue number and skip to next item.
2. Otherwise create:
   ```
   board-man create-issue <TYPE> <title> <body-with-marker-footer>
   ```
   Body footer (always): `\n\n<!-- migrated-from: <source_line> -->`
   If `gh_marker` was present: also append `\n*Originally tracked as <gh_marker>.*`
3. board-man already sets the new issue to BACKLOG. Items from TODO.md/DONE.md
   need their status corrected:
   - TODO.md item (FEATURE/CHANGE/BUG, with no plan and no tasks) → leave at BACKLOG
   - DONE.md item (and the user said Y to "import as closed") → board-man
     `set-status <#> DONE`. Then close the issue:
     `gh issue close <#> --repo <r>`. (This single `gh` is acceptable
     because `gh issue close` is not a project-board operation.)
4. Record `destination_issue` in the ledger and append a row to the
   in-memory mapping report.

### 4b. Plans

For every `plan_files[]` with a matched_item that has destination_issue set:

1. Build the plan body by reading the plan file. Prepend an H1 if missing:
   `# Plan: <feature-slug>\n\n<file contents>`
2. Call:
   ```
   board-man post-plan-comment <destination_issue> <plan-body>
   ```
   board-man returns the comment ID and pins
   `<!-- plan-comment-id: <id> -->` into the parent body.
3. Advance the parent to READY (only if it's currently in BACKLOG):
   ```
   board-man set-status <destination_issue> READY
   ```
4. Record the mapping: `plans/<slug>.md → comment <id> on issue #<n>`.

### 4c. Tasks

For every `task_files[]` with a matched_parent that has
destination_issue set:

1. Build the title: `Task: <task-name>` (from `# Task:` header).
2. Build the body: take the entire original task file content. Append a
   footer: `\n\n<!-- migrated-from: tasks/<slug>.md -->`
3. If body length > 60000 chars, split: first 60k as `body`, remainder
   as the first comment after creation. Append a `(continued in comment
   below)` line at the truncation point.
4. **Repo validation (single-repo gating).** Read the parsed `Repo:`
   metadata. If it does not equal `agent.yaml.workflow.github_project.repo`
   (e.g., `mobile.ios` vs `whinchman/midi-man-mk3`), print a WARNING:
   "task `<slug>` has Repo:`<value>` which does not match the configured
   single-repo board (`<configured>`). The sub-issue will still be created,
   but coders may not match it. Multi-repo support is a follow-up." Then
   continue.
5. Create the sub-issue:
   ```
   board-man create-task-issue <parent#> <title> <body> <parallel_group> <repo> <branch>
   ```
   board-man does: create issue with TASK + parallel-group/<N> labels,
   add to project, set Status TODO, set Parallel Group field, link as
   sub-issue via GraphQL `addSubIssue`.
6. If the original task `Status` was `done`:
   - `board-man set-status <new-issue#> DONE`
   - `gh issue close <new-issue#> --repo <r>`
7. If the body was split (step 3): post the remainder via
   `board-man add-comment <new-issue#> <remainder>`.
8. Record the mapping: `tasks/<slug>.md → issue #<n> (parent #<p>, parallel-group/<g>)`.

### 4d. Done items reconciliation

For every item that came from DONE.md (and the user opted to migrate as
closed), if it has no remaining open task children, ensure it's in DONE
and closed. board-man's `verify-children-done` does the check; loop and
advance any parent whose children are all DONE.

---

## Step 5: Reconcile parents

For every parent (feature/change/bug) whose ledger row gained children in
Step 4c:
```
board-man verify-children-done <parent>
```
If `all_done: true`, the parent should be in DONE — call
`board-man set-status <parent> DONE`. Otherwise leave at READY.

---

## Step 6: Mapping report

Write `.workflow/migrate-backup-<ts>/MAPPING.md`. One section per source
type. Example shape:

```markdown
# Migration mapping — <ISO timestamp>

Project: https://github.com/users/<owner>/projects/<n>
Repo:    <owner/repo>

## Parents

| Source                                  | Destination                                      | Status   |
|-----------------------------------------|--------------------------------------------------|----------|
| BACKLOG.md:14 (Features → "Add auth")   | https://github.com/o/r/issues/42                 | BACKLOG  |
| BACKLOG.md:18 (Issues → "Login crash")  | https://github.com/o/r/issues/43                 | BACKLOG  |
| DONE.md:8 (Features → "Add login")      | https://github.com/o/r/issues/12 (closed)        | DONE     |

## Plans

| Source                  | Destination                            |
|-------------------------|----------------------------------------|
| plans/add-auth.md       | comment #1234567 on issue #42 (READY)  |

## Tasks

| Source                  | Destination                                                  |
|-------------------------|--------------------------------------------------------------|
| tasks/auth-backend.md   | https://github.com/o/r/issues/44 (TODO, parent #42, parallel-group/1) |
| tasks/auth-frontend.md  | https://github.com/o/r/issues/45 (TODO, parent #42, parallel-group/1) |

## Skipped

| Source                  | Reason                                          |
|-------------------------|-------------------------------------------------|
| plans/old-experiment.md | User chose (a) — left in place, not migrated   |

## Warnings

- task `mobile-ios-foo`: Repo:`mobile.ios` does not match configured repo `whinchman/midi-man-mk3`
```

Print the path to the mapping report and a one-line summary
(`Migrated N parents, P plans, T tasks. Skipped K. Warnings: W.`).

---

## Step 7: Update agent.yaml

Edit `agent.yaml`:
- Set `workflow.backend: "github_project"`
- Add (or replace) the `workflow.github_project` block:
  ```
  github_project:
    owner: "<owner>"
    number: <number>
    repo: "<owner/repo>"
  ```

Show the diff to the user (use `git diff agent.yaml`). Do NOT commit.

---

## Step 8: Archive the markdown (with confirmation)

Ask:
> The board is now the source of truth. Move BACKLOG.md, TODO.md, DONE.md,
> BUGS.md, plans/, and tasks/ into `.workflow/migrate-backup-<ts>/` so they
> stop confusing future agent runs? [Y/n]

On Y:
- `git mv` each file/directory into the backup dir. (Use git so the rename
  is preserved in history.)
- Leave the backup dir tracked in git so the snapshot survives in the
  repo's history.

On n:
- Leave them in place. Print: "Markdown files retained at their original
  paths. board-man will ignore them in `github_project` mode, but they may
  drift out of sync with the board going forward."

Either way, do NOT commit. The user reviews and commits.

---

## Step 9: Stamp the per-project install

Run:
```
<framework>/scripts/install-skills-local.sh <pwd>
```
This copies skills + agents into `.claude/skills/` and `.claude/agents/`,
writing `.claude/skills/.framework-version` with the framework's git SHA
and branch. After this, the project is pinned to the framework version
that ran the migration — future framework updates won't change behavior
until the user explicitly re-runs `install-skills-local.sh`.

Also copy the issue templates:
```
mkdir -p .github/ISSUE_TEMPLATE
cp -n <framework>/templates/.github/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/
```
(`-n` so it never overwrites an existing template the project may have
customized.)

---

## Step 10: Final report

Print:
- Project URL (https://github.com/users/<owner>/projects/<n>)
- Path to the mapping report
- Path to the backup directory
- Whether markdown was archived
- Suggested next commands:
  ```
  git status                  # review changes (agent.yaml, .claude/, .github/, archive)
  git diff agent.yaml         # confirm the backend switch
  cat .workflow/migrate-backup-<ts>/MAPPING.md
  /coordinator                # exercise the new pipeline against the board
  ```

---

## Failure recovery

If anything in Step 4 (writes) fails partway through:
1. Print the last successful operation and the error from board-man.
2. Tell the user: "The migration is partially complete. Re-running
   `/agent-migrate` is safe — already-created issues will be detected via
   `find-issue-by-marker` and skipped. To roll back instead: revert
   agent.yaml, leave backup in place, manually delete created issues from
   the board UI."
3. Do NOT continue to Steps 7–10.

If `board-man` returns `{"error": "lock timeout", ...}`: another agent is
holding the write lock. Wait 60s and retry once. If it still fails, surface
to user.

---

## See also

- `~/.claude/skills/board-man/SKILL.md` — operations this skill calls
- `<framework>/scripts/board-man-setup.sh` — provisioning helper invoked in Step 0
- `<framework>/scripts/install-skills-local.sh` — per-project skill copy
- `~/.claude/skills/agent-init/SKILL.md` — fresh-project initialization with the same backend choice
- `~/.claude/skills/agent-upgrade/SKILL.md` — schema migrations between framework versions
