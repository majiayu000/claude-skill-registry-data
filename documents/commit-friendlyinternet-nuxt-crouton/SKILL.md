---
name: commit
layer: method
description: Smart, granular git commits following monorepo conventions. Analyzes changes, filters to session-relevant files, groups by intent, and uses conventional commit format. Use when committing code changes.
allowed-tools: Bash, Read, Grep, Glob
---

# Commit Skill

Smart, auto-committing workflow following this project's conventions. **Does not ask for confirmation** — analyzes, groups, commits, and reports.

## Rules

1. **NEVER use `git add .` or `git add -A`** — always stage specific files
2. **NEVER add `Co-Authored-By` lines** — omit any AI attribution footer
3. **NEVER commit unrelated changes together** — split into multiple commits if needed
4. **ALWAYS analyze changes before committing** — understand what changed and why
5. **ONLY commit files that were changed during this conversation** — if the working tree has pre-existing dirty files that were NOT part of the current task, leave them alone. Compare `git status` against what you actually touched in this session. When in doubt, ask the user.
6. **DO NOT ask for confirmation** — commit directly after analysis. The user invoked `/commit` as an explicit action.

## Workflow

### Step 0: Sync documentation (MANDATORY)

**Before committing, run `/sync-docs` to check if any documentation needs updating.**

This step:
1. Analyzes the changed files for public API impact
2. Updates relevant CLAUDE.md files, docs pages, or skills
3. Reports what was updated (or confirms nothing needed)

Any doc files updated by sync-docs become part of this commit (grouped with the code they document, or as a separate `docs()` commit if the code commit is already large).

**Skip sync-docs only if:**
- The changes are purely internal (no public API impact)
- The changes are docs-only (they ARE the doc update)
- User explicitly says to skip

### Step 0.5: i18n check (when .vue files changed)

**If any changed files are `.vue` files in an app with i18n configured, run `/i18n-check --fix`.**

This catches hardcoded labels, missing locale keys, and untranslated strings before they're committed. Any fixes become part of this commit.

**Skip i18n-check if:**
- No `.vue` files were changed
- Changes are only in packages (not apps)
- User explicitly says to skip

### Step 1: Analyze the working tree

Run these in parallel:
- `git status` — see all changed/untracked files
- `git diff` — see unstaged changes
- `git diff --cached` — see already-staged changes
- `git log --oneline -5` — see recent commit style

### Step 2: Filter to conversation-relevant changes

From the full `git status` output, identify ONLY files that were created or modified as part of the current conversation. Ignore pre-existing changes that were already dirty before this session started.

**How to determine relevance:**
- Files you created or edited (via Edit/Write tools) in this conversation → include
- Files modified by commands you ran (e.g., generators, formatters) as part of the task → include
- Files that were already dirty before this session started → exclude
- Files changed by unrelated work or previous sessions → exclude
- If unsure → ask the user

Briefly note excluded files:
```
Skipping N pre-existing file(s)
```

### Step 3: Group changes by intent

Categorize the **relevant** files into logical groups. Each group = one commit.

**Grouping rules:**
- Files that serve the same purpose go together (e.g., a component + its composable + its types)
- Config changes are separate from feature changes
- Documentation updates from `/sync-docs` go WITH the code they document (same commit) when they're small (1-2 files). Separate `docs()` commit only for larger doc-only changes.
- Test files go with the code they test, not in a separate commit
- Migration files go with their schema changes

### Step 4: Execute commits sequentially

For each group:
1. `git add <specific-files>`
2. **Verify staged files** — run `git diff --cached --name-only` and review the list. If ANY file looks unrelated to the commit's intent (wrong scope, different feature, pre-existing change that snuck in), unstage it with `git reset HEAD <file>` before committing. This is the last line of defense against sweeping unrelated changes into a commit.
3. `git commit` with the message (use HEREDOC format, no Co-Authored-By)

**Do not wait for approval.** Commit immediately.

### Step 5: Confirm

Show `git log --oneline -N` (where N = number of commits made) to confirm what was committed.

## Commit Message Format

```
<type>(<scope>): <description>

[optional body — only if the change needs explanation]
```

### Types
- `feat` — New feature or capability
- `fix` — Bug fix
- `refactor` — Code restructuring (no behavior change)
- `docs` — Documentation only
- `test` — Adding or updating tests
- `chore` — Build, config, dependencies
- `perf` — Performance improvement
- `style` — Formatting, whitespace (no logic change)

### Scopes (monorepo package short names)
- `crouton` — Main module
- `crouton-core` — Core layer
- `crouton-cli` — CLI/generator
- `crouton-i18n` — i18n layer
- `crouton-editor` — Rich text layer
- `crouton-flow` — Flow layer
- `crouton-assets` — Assets layer
- `crouton-devtools` — Devtools
- `crouton-auth` — Auth layer
- `crouton-triage` — Triage layer
- `crouton-pages` — Pages layer
- `crouton-bookings` — Bookings layer
- `docs` — Documentation app
- `playground` — Playground app
- `rakim` — Rakim app
- `root` — Root config, workspace-level

For changes spanning multiple packages: `feat(crouton-cli,crouton-core): description`

### Message quality guidelines

**Good messages explain WHY, not WHAT:**
- `fix(crouton-auth): prevent duplicate session on rapid login` (why)
- ~~`fix(crouton-auth): change if condition in auth.ts`~~ (what — bad)

**Keep the subject line under 72 characters.**

**Use the body for context when the change isn't obvious.**

### Two audiences in the body (REQUIRED)

Keep the conventional subject line, then write the body for **both** readers (full convention lives in the `github-tasks` skill):
- **👤 For humans** — a short, plain-language summary of what changed and why it matters (one line is fine for small commits).
- **🤖 For agents** — the precise specifics: files/symbols touched, behaviour changes, follow-ups.

Diagrams belong in PR/issue bodies (which render Mermaid), **not** in commit messages — keep commit text lean.

## HEREDOC Format (MANDATORY)

Always use this format to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
feat(crouton-core): add useTeamMembers composable

👤 For humans
Team settings can now show a live member list that filters by role and
flags who still has a pending invite — no manual refresh needed.

🤖 For agents
- New app/composables/useTeamMembers.ts — reactive list, role filter
- Surfaces invite status from member.status; used by TeamSettings.vue
EOF
)"
```

## Restructuring Previous Commits

If the new changes logically belong with a recent commit (e.g., a follow-up fix to something just committed), it's better to amend or restructure than to create a noisy separate commit.

**When to amend/restructure:**
- A small fix for something committed moments ago in the same session
- The previous commit message should be improved to cover the combined changes
- Commits from this session that would read better squashed or reordered

**When NOT to amend:**
- The previous commit was from a different session or a different topic
- The previous commit has already been pushed to a shared branch
- You're unsure — ask the user

**To amend:**
```bash
git add <specific-files>
git commit --amend -m "$(cat <<'EOF'
fix(crouton-auth): handle expired tokens

Also covers edge case where refresh token is revoked
mid-session.
EOF
)"
```

## Merging a Stack (retarget before `--delete-branch`)

When merging a PR whose branch is the **base of other open PRs**, deleting that branch on merge
makes GitHub **auto-close** the dependents — it does not retarget them. Silently, mid-train.

Before merging a stacked PR's base:

```bash
# 1. Find anything based on the branch you're about to delete
gh pr list --base <branch-being-merged>

# 2. Retarget each dependent onto the surviving integration branch FIRST
gh pr edit <dependent-pr> --base <surviving-branch>

# 3. Only then merge the base
gh pr merge <pr> --merge --delete-branch
```

Or merge **deepest-first**, so each merge carries the stack forward and no base is ever deleted
out from under an open PR.

Incident: epic #1303 (2026-07-10) — merging #1330 with `--delete-branch` auto-closed #1344 and
#1353. Both survived only because stacked branches carry their ancestors' commits; without that
property the work would have been silently dropped. Rule of record: `AGENTS.md` § Commits →
Merge policy.

## Edge Cases

### Nothing to commit
If `git status` shows no changes, tell the user — don't create an empty commit.

### Already-staged files
If files are already staged (`git diff --cached`), include them in the analysis.

### Sensitive files
Never commit: `.env`, `credentials.json`, `*.key`, `*.pem`, `.secret*`, `node_modules/`. Warn the user if these appear in the changeset.
