---
name: ship
version: 1.0.0
description: |
  ship it, push this, create PR, land this, send it, merge this, commit and push,
  open a pull request, ship this branch, clean gone branches, pr only, just make a pr,
  quick pr, docs only pr.
  Fully automated: merge main, test, review, split commits, push, create PR.
  PR-only mode for lightweight changes (docs, config, skills).
argument-hint: [clean | pr]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Skill
  - Agent
  - AskUserQuestion
---

# Ship: Fully Automated Ship Workflow

You are running the `/ship` workflow. This is a **non-interactive, fully automated** workflow. Do NOT ask for confirmation at any step unless specified. The user said `/ship` which means DO IT.

## Arguments

- `/ship` — full ship workflow (default)
- `/ship pr` — PR-only mode: commit, push, create PR. Skips tests, review, and simplification. For docs, config, skills, and other lightweight changes.
- `/ship clean` — clean up stale local branches marked as `[gone]` on remote, including worktrees

---

## PR-Only Mode

If `$ARGUMENTS` contains "pr":

Fast path — commit, push, and create a PR with a rich body. Skips tests, review, simplification, and CHANGELOG. Designed for docs-only, config, skill, and other low-risk changes.

### Step 1: Pre-flight

1. Check the current branch. If on `main`, **abort**: "You're on main. Ship from a feature branch."
2. Run `git status` (never use `-uall`).
3. Run `git diff origin/main...HEAD --stat` and `git log origin/main..HEAD --oneline` to understand what's being shipped.

### Step 2: Commit

Stage all changes and create a single commit:

```bash
git add -A && git commit -m "$(cat <<'EOF'
<type>: <summary>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

Use `docs:` for documentation, `chore:` for config/skills, `style:` for formatting. If there are already commits on the branch and no uncommitted changes, skip this step.

### Step 3: Push and create PR

```bash
git push -u origin $(git branch --show-current)
```

Create the PR following the standard PR body structure:

```bash
gh pr create --title "<type>(<scope>): <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points of what changed>

## Important Files
| File | Change |
|------|--------|
| `path/to/file` | description |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Skip "How It Works" / Mermaid diagrams, Test Results, Pre-Landing Review, and Doc Completeness sections — they don't apply to lightweight changes.

**Output the PR URL** — this should be the final output the user sees, then **STOP**.

---

## Clean Mode

If `$ARGUMENTS` contains "clean":

1. Run `git fetch --prune` to update remote tracking info.
2. List branches marked as gone: `git branch -vv | grep ': gone]'`
3. For each gone branch:
   - Check if it has an associated worktree: `git worktree list`
   - If worktree exists, remove it: `git worktree remove <path> --force`
   - Delete the branch: `git branch -D <branch>`
4. Report what was cleaned up, then **STOP**.

---

## Ship Mode (default)

**Only stop for:**
- On `main` branch (abort)
- Merge conflicts that can't be auto-resolved (stop, show conflicts)
- Test failures (stop, show failures)
- Pre-landing review finds CRITICAL issues and user chooses to fix
- Anything that would lose work

**Never stop for:**
- Uncommitted changes (always include them)
- CHANGELOG content (auto-generate from diff)
- Commit message approval (auto-commit)

---

## Step 1: Pre-flight

1. Check the current branch. If on `main`, **abort**: "You're on main. Ship from a feature branch."

2. Run `git status` (never use `-uall`). Uncommitted changes are always included.

3. Run `git diff origin/main...HEAD --stat` and `git log origin/main..HEAD --oneline` to understand what's being shipped.

---

## Step 2: Merge origin/main (BEFORE tests)

Fetch and merge `origin/main` into the feature branch so tests run against the merged state:

```bash
git fetch origin main && git merge origin/main --no-edit
```

**If merge conflicts:** Try to auto-resolve simple ones (CHANGELOG ordering, lock files). If complex, **STOP** and show them.

**If already up to date:** Continue silently.

---

## Step 3: Run tests (on merged code) — PARALLEL AGENTS

Check `git diff origin/main --name-only` to determine which areas changed. Read CLAUDE.md and package.json to discover the project's test commands.

Dispatch **parallel sub-agents** for each applicable test suite using the Agent tool. Launch all agents in a **single message** (multiple Agent tool calls). Each agent should run the appropriate test command for the changed area and report pass/fail count and any failures.

Example agent prompts (adapt to the project's actual test commands):
```
prompt: "Run the test suite: <test-command>. Report pass/fail count and any failures."
description: "<area> tests"
```

Wait for all test agents to complete. Collect results.

**If any test fails:** Show the failures and **STOP**. Do not proceed.

**If all pass:** Continue — just note the counts briefly.

---

## Step 4: Simplify Changed Code

After tests pass, dispatch a **code simplification agent**:

```text
prompt: "Review all files changed between origin/main and HEAD (run `git diff origin/main --name-only` to find them). For each changed file, check for: code that could be reused from existing utilities, unnecessarily complex logic that could be simplified, redundant code, inconsistent patterns vs the rest of the codebase. Read CLAUDE.md conventions section first. Output a list of specific simplification suggestions with file:line references. If a suggestion is safe and obvious, apply the fix directly using Edit. Only apply fixes that preserve exact functionality."
description: "Simplify changed code"
```

If the agent made edits, stage them. If it only suggested changes, apply the safe ones.

**Important:** Simplification runs BEFORE the review so the review stamp covers the final code state.

---

## Step 4.5: Pre-Landing Review

After simplification is complete, invoke `/review` using the Skill tool:

```text
skill: "review"
args: "greptile"  ← include if the project uses Greptile
```

This dispatches the full `/review` workflow: parallel @code-reviewer + checklist agents, Greptile triage, TODO cross-reference, and review stamp.

**If `/review` reports BLOCKED:** The skill will have already asked the user about each critical finding via AskUserQuestion. If the user chose "Fix it now" on any issue, apply the fixes, commit them (`git add <fixed-files> && git commit -m "fix: apply pre-landing review fixes"`), then **re-run from Step 3** to verify fixes don't break tests.

**If `/review` reports PASS:** Continue. Include any informational findings in the PR body.

---

## Step 5: CHANGELOG (auto-generate)

1. Read `CHANGELOG.md` header to know the format. If no CHANGELOG.md exists, skip this step.

2. Auto-generate entries from **ALL commits on the branch**:
   - Use `git log origin/main..HEAD --oneline` for every commit being shipped
   - Use `git diff origin/main...HEAD` for the full diff
   - Categorize into: `### Added`, `### Changed`, `### Fixed`
   - Write concise, descriptive bullet points
   - Insert under `## [Unreleased]` section
   - Follow Keep a Changelog format

**Do NOT ask the user to describe changes.** Infer from the diff and commit history.

---

## Step 6: Commit (bisectable chunks)

**Goal:** Create small, logical commits that work well with `git bisect`.

1. Analyze the diff and group changes into logical commits. Each commit = one coherent change.

2. **Commit ordering** (earlier first):
   - **Schema/migrations:** new DB tables, schema changes
   - **Backend:** new config, services, background jobs (with their tests)
   - **API routes:** new/modified routes (with their tests)
   - **Frontend:** components, pages (with their tests)
   - **CHANGELOG:** always in the final commit

3. **Rules for splitting:**
   - A component and its test file go in the same commit
   - An API route and its test go in the same commit
   - Migrations are their own commit (or grouped with the schema they support)
   - If the total diff is small (< 50 lines across < 4 files), a single commit is fine

4. **Each commit must be independently valid** — no broken imports.

5. Commit messages: `<type>: <summary>` (type = feat/fix/chore/refactor/docs)
   Only the **final commit** gets the co-author trailer:

```bash
git commit -m "$(cat <<'EOF'
chore: update changelog

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Step 7: Push

Push to the remote with upstream tracking:

```bash
git push -u origin $(git branch --show-current)
```

---

## Step 8: Create PR

Construct a rich PR body with these sections, then create the PR using `gh pr create`.

### PR Body Structure

**1. Summary** — bullet points from CHANGELOG entries (what shipped).

**2. How It Works** (include when the PR has non-trivial logic):

Generate a **Mermaid diagram** showing the key flow introduced or changed. Pick the diagram type that fits best:

- `sequenceDiagram` — for request/response flows, multi-step pipelines, hook execution chains
- `flowchart TD` — for decision trees, state machines, before/after architecture comparisons
- `erDiagram` — for schema changes showing new tables/relationships

Keep diagrams focused — show the **new/changed flow only**, not the entire system. 5-15 nodes max. If the PR is small (< 50 lines, config-only, docs-only), skip diagrams entirely.

**3. Important Files** — table of the key files changed with a one-line description of what changed in each:

```markdown
| File | Change |
|------|--------|
| `path/to/file.ts` | Added X handler with Y validation |
| `path/to/other.ts` | Updated Z to support new field |
```

Only include files with meaningful logic changes. Skip auto-generated files, lock files, and trivial formatting changes. Group by layer (schema → backend → API → frontend → infra → docs). Max 10-12 rows — if more files changed, summarize the remainder as "N additional files with minor changes".

**4. Test Results** — table from Step 3.

**5. Pre-Landing Review** — findings from Step 4.5, or "No issues found."

**6. Doc Completeness** — checklist.

### Create the PR

```bash
gh pr create --title "<type>(<scope>): <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points from CHANGELOG>

## How It Works
<mermaid diagram — or omit section for small/docs-only PRs>

## Important Files
| File | Change |
|------|--------|
| `path/to/file` | description |

## Test Results
| Suite | Result |
|-------|--------|
| <suite> | <pass/fail count> |

## Pre-Landing Review
<findings from Step 4.5, or "No issues found.">

## Doc Completeness
- [ ] README updated (if applicable)
- [ ] CHANGELOG updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Output the PR URL** — this should be the final output the user sees.

---

## Gotchas

- **Use `origin/main` not local `main`.** Local main may be stale. All diff/merge commands use `origin/main`.
- **Review gate may block fix commits.** If you commit review fixes and the review gate blocks, re-run from Step 3 for a fresh stamp.
- **Simplify runs BEFORE review** so the review stamp covers the final code state. Don't reorder Steps 4 and 4.5.
- **`git push` may fail if the branch was force-pushed elsewhere.** Never force push to recover — ask the user.
- **CHANGELOG auto-generation reads all commits on the branch** — if prior commits have bad messages, the CHANGELOG entries will be vague.
- **`/ship pr` skips ALL safety checks** (tests, review, simplification). Only use for genuinely low-risk changes. If in doubt, use `/ship`.

## Important Rules

- **Never skip tests.** If tests fail, stop.
- **Never skip the pre-landing review.** Run it every time.
- **Never force push.** Use regular `git push` only.
- **Never ask for confirmation** except for CRITICAL review findings.
- **Split commits for bisectability** — each commit = one logical change.
- **The goal is: user says `/ship`, next thing they see is the review + PR URL.**
