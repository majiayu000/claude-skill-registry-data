---
name: ss-create-branch
description: Use when starting new development work to cut a properly named branch from the remote default branch, decide whether to develop it in an isolated git worktree, push it immediately, and set up upstream tracking. Takes a branch name, a requirement link, or a plain-language description as input.
---

# Create Development Branch

Create a named development branch from the latest remote default branch, decide whether to develop in an isolated git worktree (explicit request > repository default > ask the user), push the branch immediately, and set up upstream tracking.

## Inputs

- A branch name, a requirement link (issue/ticket/doc URL), or a plain-language description of the work. If none is given, ask.
- Optional: `--from <branch>` to branch off something other than the remote default.
- Optional: an explicit worktree preference (isolated worktree vs. develop in place) — if not given, follow Step 4's priority order below.
- Optional: `--verify-baseline` to run the full test suite once after the worktree is ready, to confirm the baseline. Skipped by default because the branch starts as a zero-diff cut of the remote base, so its baseline already equals whatever CI last confirmed.

## Step 1 — Determine the branch slug

Derive the slug (the name portion after the type prefix) from the input:

| Input | Example | Slug |
|-------|---------|------|
| Plain text | "add payment", "login fix 123" | Lowercase, spaces → hyphens |
| A requirement/ticket link | `https://tracker.example.com/issues/10442755` | If a numeric ID is visible in the URL, use it directly; otherwise fetch and summarize |
| A document link | any URL to a spec/PRD | Fetch its content with your document-reading tool and summarize to a 2–4 word English slug |
| Pasted markdown/text | `# Add User API\n...` | Extract the first heading/title and summarize to a 2–4 word English slug |

Slug rules: lowercase letters, digits, and hyphens only — no spaces, underscores, or other punctuation.

## Step 2 — Determine the branch type prefix

Supported prefixes: `feat/`, `fix/`, `hotfix/`, `refactor/`, `docs/`.

- If the user's input already includes a prefix (e.g., `fix/login-bug`), use it as given.
- If the input is a feature/requirement link, default to `feat/`; use `fix/` if the requirement is clearly a defect.
- If it's ambiguous, ask which prefix applies before proceeding.

## Step 3 — Determine the base branch

- Default: the remote's default branch, detected dynamically (`git remote show origin`, "HEAD branch" line) — never hardcode `main` or `master`.
- Override: if `--from <branch>` was given, use `origin/<branch>`.
- Always `git fetch origin` first; never branch off a possibly stale local ref.

## Step 4 — Decide: worktree or in place

Decide in this priority order:

1. **Explicit request** — the user said "in an isolated worktree" or "in place" → use that, skip the question.
2. **Repository default** — check `AGENTS.md` for a managed preference:
   ```bash
   grep -oE 'ss:worktree-default: *(worktree|in-place)' AGENTS.md 2>/dev/null
   ```
   If present, honor it without asking.
3. **Ask** — if neither of the above resolved it, ask the user once: "Develop this in an isolated worktree, or in place?" Mention that recording a preference in `AGENTS.md`'s `SS-WORKTREE` block avoids the question next time.

**Decision = in place** → the whole flow ends here:

```bash
git fetch origin
BASE=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}')
git checkout -b <prefix>/<slug> origin/$BASE
git push -u origin <prefix>/<slug>
```

**Decision = worktree** → continue to Step 5.

## Step 5 — Create the branch in an isolated worktree

### 5.0 — Check for existing isolation (never nest worktrees)

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Submodule guard: a submodule always has GIT_DIR == GIT_COMMON, so it can never be
# mistaken for a linked worktree. This positive check confirms a submodule context —
# if it prints a path, report it and work from the superproject root instead.
git rev-parse --show-superproject-working-tree 2>/dev/null
```

Evaluate, in this order, wherever the session currently is:

1. **The target branch already has a worktree** (visible in `git worktree list --porcelain` as `branch refs/heads/<prefix>/<slug>`) → reuse it: switch into that directory, go to 5.2.
2. **Already inside a linked worktree** (`GIT_DIR != GIT_COMMON`, and not a submodule) → don't create another one:
   - Already on the target branch → reuse it, go to 5.2.
   - Otherwise, switch this worktree to the target branch (`git checkout -b <prefix>/<slug> origin/$BASE`, or plain `git checkout <prefix>/<slug>` if it exists locally without its own worktree — rule 1 already ruled out it living elsewhere) → go to 5.2.
3. **Neither** → create a new worktree, Step 5.1.

### 5.1 — Create the worktree

**If a native worktree tool is available** (e.g., your coding assistant's built-in worktree command), use it to create and enter the worktree, then make sure the branch inside it is correct:

```bash
git checkout -b <prefix>/<slug> origin/$BASE   # or rename a tool-created temp branch
```

**Otherwise**, fall back to a project-local `.worktrees/` convention. The directory name is the branch name with `/` flattened to `-` (e.g., branch `feat/10442755` → `.worktrees/feat-10442755`):

```bash
git fetch origin
# .worktrees MUST be git-ignored before anything is created inside it
git check-ignore -q .worktrees || echo '.worktrees/' >> .gitignore
git worktree add .worktrees/<prefix>-<slug> -b <prefix>/<slug> origin/$BASE
cd .worktrees/<prefix>-<slug>
```

Notes and edge cases:

- **Never auto-commit the `.gitignore` edit.** The main checkout may be on whatever branch the user happened to be on; a silent commit there pollutes its history. Leave the edit uncommitted and mention it in the Step 6 report — it takes effect immediately (`git check-ignore` reads the working tree) even before it's committed.
- Branch exists already (local or remote) but has no worktree → `git worktree add .worktrees/<prefix>-<slug> <prefix>/<slug>` (no `-b`).
- Branch is checked out in another worktree already → git refuses; report that worktree's path and suggest switching into it instead.
- The target directory exists but isn't a registered worktree (leftover from an interrupted run) → report it, ask the user to confirm clearing it, then retry.
- `.gitignore` can't be modified (read-only) → report it and ask whether to develop in place instead, or let the user fix it and retry.
- Worktree creation is denied by a sandbox/permission layer → tell the user it was denied and fall back to the in-place flow from Step 4.

### 5.2 — Environment readiness

```bash
# If this project uses git submodules for shared spec/config content, they start
# empty in a fresh worktree:
git submodule update --init --recursive
```

Then auto-detect and install the stack's dependencies (these are long operations — run them in the background if your tooling supports it):

- `package.json` → `npm install`
- `go.mod` → `go mod download`
- `pom.xml` / `build.gradle` → usually no action needed; build tools fetch on demand

If submodule init fails, warn that spec-injection steps in other skills may be missing content, and ask whether to continue anyway.

If `--verify-baseline` was requested, run the full test suite once now; report any failures and ask whether to proceed.

### 5.3 — Push and set upstream

```bash
git push -u origin <prefix>/<slug>
```

## Step 6 — Report

- The full branch name created (e.g., `feat/10442755`) and confirmation of remote tracking (`origin/<prefix>/<slug>`).
- The worktree path, or "developed in place" — and where that decision came from (explicit request / repository default / user's answer / sandbox fallback).
- If `.gitignore` was auto-amended in 5.1: note that the edit is uncommitted and should land with the next commit.
- A reminder that all subsequent commands run inside the worktree directory, and that finishing development should be followed by the `ss-cleanup` skill to remove the worktree and delete the branch.

## Examples

```
Create a branch: feat/add-payment-gateway
Create a branch for https://tracker.example.com/issues/10442755
Create a branch from a pasted requirement doc, prefix fix/
Create a branch off dev: refactor/cleanup-auth
Create a branch for add-payment, force an isolated worktree
Create a branch for login-bug fix, develop in place
```
