---
name: git-commit-push-pr
description: Commit current changes, push to remote, and create or update a pull request on GitHub. Use when making changes and preparing a complete pull request for review.
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git push:*)
  - Bash(gh pr create:*)
  - Bash(gh pr ready:*)
  - Bash(.agents/skills/git-commit-push-pr/scripts/get-pr-metadata.sh:*)
  - Bash(.agents/skills/git-commit-push-pr/scripts/get-base-branch.sh:*)
models:
  claude: sonnet      # medium-complexity; PR creation with template filling needs broader reasoning
  copilot: auto
  codex: gpt-5.4
---

# Git Commit, Push, and Create/Update Pull Request (GitHub)

Commit current changes with conventional commits format, push to remote, and create/update a pull request on GitHub using `gh` CLI.

## Draft vs Ready (default: DRAFT)

PRs are created as **draft by default**. The state is controlled by two switches:

| Switch | Effect |
|--------|--------|
| _(none)_ / `--draft` | Create the PR as a **draft** (default). On an existing draft PR, leave it as draft |
| `--ready` | Create the PR **ready for review** (omit `--draft`). On an existing draft PR, mark it ready via `gh pr ready` |

`--draft` and `--ready` are mutually exclusive; if both are passed, **STOP and ask the user** _(when `--mansplain` is also passed, default to `--draft` instead of asking)_. Resolve the requested state once at the start and apply it consistently in Step 6 (new PR) and the Update Existing PR section.

## Issue Auto-Close (default: ON)

By default, the PR description gets a `Closes #<issue>` line so GitHub **auto-closes the linked issue when the PR merges**. The behaviour is controlled by one switch and the issue-number resolution below:

| Switch | Effect |
|--------|--------|
| _(none)_ | Append `Closes #<issue>` to the Description section (default) |
| `--noclose` | Do **not** append any `Closes #` link |

**Issue-number resolution (when `--noclose` is NOT passed), in order:**

1. Explicit `--issue <number>` argument.
2. Otherwise, run `scripts/get-pr-metadata.sh` — it parses the branch name (`<type>/<issue>-short-description`) and returns JSON with `type`, `issue`, `slug`, and a ready-made `pr_title_prefix`.

If neither yields a number (e.g. a ticketless branch like `refactor/cleanup-dead-code`), **skip the close link gracefully** and tell the user no issue could be determined — do not block, and do not guess a number.

Resolve the close behaviour and issue number once at the start, then apply it in Step 5 (new PR) and the Update Existing PR section.

## Workflow Steps

### Step 1: Commit and Push (MANDATORY)

Invoke the **git-commit-push** skill as a sub-agent (medium-complexity task):
- Claude Code: `Task(subagent_type: "general-purpose", model: "sonnet", prompt: "invoke git-commit-push skill" + args)`
- Copilot: invoke `git-commit-push` skill with model `auto`
- Codex: invoke git-commit-push agent (model: `gpt-5.4`)
- If commit message provided, pass it to git-commit-push
- If `--issue <number>` was passed, forward it to git-commit-push so the branch is renamed before the push
- If `--mansplain` was passed, forward it to git-commit-push (and transitively to git-commit)
- This handles staging, committing with conventional format, branch renaming (when `--issue` is passed), and pushing to remote
- Respects logical units of work
- If there are no changes to commit or push, continue gracefully (not an error)

### Step 2: Check for Existing PR

Run `gh pr list --head $(git rev-parse --abbrev-ref HEAD) --json number,title`

- If the result contains a PR (non-empty output): go to **Update Existing PR** section below and STOP
- If no PR exists (empty output): **MUST CONTINUE** with Step 3

### Step 3: Build PR Title (Ticketed Conventional Format)

**MANDATORY FORMAT** (per `.agents/rules/git/git-policy.instructions.md` — the source of truth):

`<type>[{ticket}]: <description>` — e.g. `feat[1234]: add user authentication`, `chore[NO-TICKET]: update dependencies`

Run `scripts/get-pr-metadata.sh` to derive the prefix deterministically: its `pr_title_prefix` field is `<type>[<issue>]` (or `<type>[NO-TICKET]` for a ticketless conforming branch); append `: <description>` yourself. If the field is empty, the branch name is non-conforming — derive the type from the commits instead.

This title becomes the squash commit message on `main`, so it must be descriptive and follow the format precisely. **If a conforming ticket/title cannot be determined, STOP and ask the user — do not guess or proceed with a non-conforming title.** _(When `--mansplain` is passed: make your best determination and proceed without asking.)_

### Step 4: Read PR Template

**CRITICAL**: ALWAYS read `.github/pull_request_template.md` and use it EXACTLY as the PR description — NO CUSTOM FORMATS ALLOWED.

### Step 5: Fill Template Sections

- **Description**: Replace placeholder with bullet points of actual changes made. **Unless `--noclose` was passed**, append `Closes #<issue>` as the last bullet point in the Description section, where `<issue>` is resolved per the **Issue Auto-Close** section above (explicit `--issue <number>`, else parsed from the branch name). If no issue number can be determined, omit the close link and note this to the user.
- **Type of Change**: Check the appropriate checkbox(es)
- **Testing**: Check applicable test levels and describe test details
- **Checklist**: Complete all items appropriately
- **AI Review Notes**: Fill Focus Areas, Context, and Known Issues

### Step 6: Create the PR

**Default (draft)** — run:

`gh pr create --draft --title "<title>" --body "<filled template content>" --base main`

**When `--ready` was passed** — omit `--draft`:

`gh pr create --title "<title>" --body "<filled template content>" --base main`

- **Base branch**: use `scripts/get-base-branch.sh` if unsure (returns `main`/`master`/remote default)
- **Draft is the default** — only create a non-draft (ready) PR when `--ready` is explicitly passed
- **ABSOLUTE REQUIREMENT**: Use the `<type>[{ticket}]: <description>` title format (Step 3), STRICT template for body

### Step 7: Verify (MANDATORY)

Run `gh pr view <pr-number> --json body` and confirm the PR description contains ALL template sections.

If any section is missing or uses a non-template format, update immediately with `gh pr edit <pr-number> --body "<updated template content>"`.

Report the PR URL **and its draft/ready state** to the user.

---

## Update Existing PR

If a PR already exists for the current branch (detected in Step 2):

1. **Get PR number and target branch** from the Step 2 output
2. **Read existing PR description**: `gh pr view <pr-number> --json body` and capture current AI Review Notes
3. **Read PR template**: Load `.github/pull_request_template.md`
4. **Analyze COMPLETE changeset** (`git diff main...HEAD`) — not just latest commit
5. **Preserve PR title**: Keep existing title unchanged unless scope fundamentally changed
6. **FULL UPDATE (not incremental)**: Completely replace the PR description based on the template. **Unless `--noclose` was passed**, ensure the Description section ends with `Closes #<issue>` (issue number resolved per the **Issue Auto-Close** section). If the existing description already has a correct `Closes #` line, preserve it; if `--noclose` was passed, remove any existing `Closes #` line
7. **Execute update**: Run `gh pr edit <pr-number> --body "<updated template content>"`
8. **Apply draft/ready switch**: If `--ready` was passed and the PR is currently a draft, run `gh pr ready <pr-number>` to mark it ready. If neither switch (or `--draft`) was passed, leave the existing draft/ready state unchanged
9. **Verify** (mandatory): `gh pr view <pr-number> --json body` and confirm all template sections are present

**CRITICAL**:
- This is a FULL replacement of the entire PR description, not an incremental update
- Analyze the COMPLETE diff with main and ALL commits
- ALWAYS preserve the AI Review Notes section from the existing PR description

## Arguments

- Optional: pre-defined commit message (if not provided, will analyze changes and generate appropriate conventional commit message)
- `--draft` — create the PR as a draft (this is the **default** behavior)
- `--ready` — create the PR ready for review (or mark an existing draft PR ready). Mutually exclusive with `--draft`
- `--noclose` — do **not** append a `Closes #<issue>` link to the PR description. By default (without this switch) the link is added so GitHub auto-closes the linked issue on merge
- `--issue <number>` — two effects:
  1. Renames the local branch to `<type>/<number>-short-description` before pushing (delegated to **git-commit-push**)
  2. Sets the issue number used for the `Closes #<number>` link explicitly. **Note:** the close link is added **by default** even without `--issue` — when `--issue` is omitted the number is parsed from the branch name. Use `--issue` only to override that, or `--noclose` to suppress the link entirely
- `--mansplain` — suppress all interactive questions throughout the entire chain (commit → push → PR). The agent uses its best judgment on commit grouping, messages, and PR title without stopping to ask. If `--draft` and `--ready` are both passed alongside `--mansplain`, defaults to `--draft`.

## Usage Examples

```
/git-commit-push-pr                                  # commit, push, open a DRAFT PR (default); closes the branch's issue on merge
/git-commit-push-pr --ready                          # commit, push, open a READY PR; closes the branch's issue on merge
/git-commit-push-pr feat: add user authentication    # draft PR with a pre-defined commit message
/git-commit-push-pr --ready feat: add auth system    # ready PR with a pre-defined commit message
/git-commit-push-pr --noclose                        # draft PR WITHOUT a Closes #<issue> link
/git-commit-push-pr --issue 42                       # draft PR, renames branch to feat/42-*, closes #42 on merge
/git-commit-push-pr --ready --issue 42               # ready PR, renames branch to feat/42-*, closes #42 on merge
/git-commit-push-pr --mansplain                      # draft PR; no questions asked — agent decides everything
/git-commit-push-pr --mansplain --issue 42           # draft PR, renames branch, no questions asked
/git-commit-push-pr --mansplain --ready              # ready PR; no questions asked
```

All `gh` commands (shown inline in the steps above) require GitHub CLI authenticated via `gh auth login`.
