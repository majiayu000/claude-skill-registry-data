---
name: commit
description: "Create a git commit following project conventions. Enforces PREFIX-#.# prefix, imperative mood, no Co-Authored-By. TRIGGER when the user says \"commit this\", \"commit the changes\", \"let's commit\", \"make a commit\", \"save this progress\", \"check in the code\", \"snapshot this\", \"git commit\", or any request to create a git commit."
---

# Project Commit

Create a commit following project conventions.

## Current State

- Branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Untracked files: !`git status --short`

## Commit Rules

1. **Detect identifier** from current branch name using `.claude/skills/_shared/milestone-format.sh`:
   - Legacy M-format: `feature/M9.16-description` → `M9.16` (format: `M`)
   - New OpenSpec change-id: `feature/architecture-compliance-sweep` → `architecture-compliance-sweep` (format: `kebab`)
   - The shared utility normalizes both; commit prefix uses whichever format the branch uses.
2. **Stage specific files** — never use `git add .` or `git add -A` (risk of committing secrets or large binaries)
3. **Format commit message**:
   - First line: `<identifier>: Brief description` (imperative mood, e.g., "Add", "Fix", "Update")
   - Blank line
   - Bullet points of specific changes
4. **NO Co-Authored-By line** — this is a project convention
5. **Use HEREDOC** for multi-line messages

## Message Format

Legacy M-format branch:
```
M9.16: Brief imperative description

- Detail 1
- Detail 2
```

New OpenSpec change-id branch:
```
architecture-compliance-sweep: Brief imperative description

- Detail 1
- Detail 2
```

## Process

### Step 0: Doc Freshness Check

Before staging, verify core docs are current. For each issue found, fix it before proceeding:

1. **current-story.md**: Verify active milestone matches branch. If stale, update milestone status and progress.
2. **next-prompt.md**: Verify hub has pointer for current milestone. Scaffold if missing.
3. **next-prompt-PREFIX-#.md**: Verify file exists for branch's milestone. Scaffold if missing.
4. **development-journal.md**: Check today's date in first 20 lines. If stale, run `/dev-journal` via Agent (background).
5. **insights-log.md**: Verify file exists. Create if missing.
6. **requirements.md**: Verify current milestone has a section.

Prompt the user about insights: "Any technical insights worth logging from this session?" (optional, not blocking).

**Include doc updates in the same commit as code changes** — stage them alongside the code.

### Step 1: Review and Stage

1. Review all changes (staged + unstaged + untracked)
2. Identify which files should be committed (ask user if unclear)
3. Stage the appropriate files by name (including any doc updates from Step 0)
4. Draft the commit message and show it to the user
5. Commit using HEREDOC format
6. Do NOT push unless explicitly asked

## Commit Message Quality

Good:
- `M10.3: Add photo import OCR service`
- `M8.4: Fix confidence routing threshold`
- `M7.5: Refactor service ownership pattern`

Bad:
- `Fixed stuff` (no milestone prefix)
- `M10.3: Updated files` (vague)
- `WIP` (not descriptive)

## Post-Commit

After committing, automatically run these via Agents (background) for efficiency:
1. **Journal**: Read the top of `docs/development-journal.md` — if the latest entry doesn't reference today's date or the current milestone, invoke `/dev-journal` via an Agent to update it
2. **Insights**: Ask the user if there are any unlogged technical insights from this session. If yes, invoke `/log-insight` via an Agent
3. **Status line**: Check whether the branch-keyed status file still reflects the current focus. If this commit represents a transition (phase complete, sub-task done, moving from build to review), refresh it:

```bash
bash .claude/skills/_shared/status-line.sh write "[<identifier>] <new focus>"
```

Typical post-commit transitions: `phase 1 — scaffolding` → `phase 2 — wiring`, or `implementation` → `review / testing`, or after the final commit `ready for PR`.

