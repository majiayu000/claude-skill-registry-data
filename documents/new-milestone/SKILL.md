---
name: new-milestone
description: "Set up a new milestone for development. Creates feature branch, updates current-story.md, and creates branch-specific next-prompt file with implementation guidance. TRIGGER when the user says \"new milestone\", \"start a new milestone\", \"create milestone\", \"begin feature\", \"next milestone\", \"set up milestone\", or any request to start a new development milestone."
argument-hint: <PREFIX-#.# brief description>
---

# New Milestone Setup

**Milestone**: $ARGUMENTS

## Step 0: Detect Identifier Format

Forager accepts two identifier formats (per `docs/openspec-workflow-reference.md`):
- **Legacy M-format**: `M7.7`, `M9.16`, `M18.1.3` — historical work only (forward-only policy)
- **New OpenSpec change-id**: `architecture-compliance-sweep`, `migrate-to-structured-logging` — all new work

Normalize and validate the input via the shared utility:
```bash
bash .claude/skills/_shared/milestone-format.sh "$ARGUMENTS"
# Output: format=M|kebab  id=<identifier>  original=<identifier>
# Exit 2 if the input matches neither format
```

The skill's subsequent steps substitute `<identifier>` for the normalized ID regardless of format — branch names, PRD file names, next-prompt file names, and commit prefixes all use the identifier as-is.

## Step 1: Verify Prerequisites

- Current branch: !`git branch --show-current`
- Main is up to date: !`git log origin/main..main --oneline`

If not on `main`, switch to main and pull:
```bash
git checkout main && git pull origin main
```

## Step 2: Create Feature Branch

Branch naming:
- Legacy M-format: `feature/M9.16-brief-kebab-case` (3-5 words max)
- New OpenSpec change-id: `feature/<change-id>` (the change-id is already kebab-case; no extra suffix needed)

```bash
# Legacy example
git checkout -b feature/M9.16-grocery-list-item-service
git push -u origin feature/M9.16-grocery-list-item-service

# New OpenSpec example
git checkout -b feature/architecture-compliance-sweep
git push -u origin feature/architecture-compliance-sweep
```

## Step 3: Update `docs/current-story.md`

- Add new milestone section with status ACTIVE
- Include: scope, estimated hours, sub-phases if known
- Update the priority queue

## Step 4: Create Branch-Specific Next-Prompt File

The file name matches the milestone ID you pass (e.g., `next-prompt-AUTH-1.md` for AUTH-1, or `next-prompt-AUTH-1.3.md` for AUTH-1.3). Sub-tasks can share a parent file or have their own.

Create `docs/next-prompt-[milestone].md`:

```markdown
# [milestone] — ACTIVE: [Title]

**PRD**: [path to PRD if exists]
**Branch**: feature/[milestone]-description
**Problem**: [What needs to be solved]

---

## What's Done
- [Completed items]

## What's Left
- [Remaining items]

## Key Design Decisions
1. [Decision and rationale]

## Key Files
- [file paths relevant to this work]
```

Then add a pointer line in `docs/next-prompt.md` under **Active Milestones**:

```markdown
- [PREFIX-#: Title](next-prompt-PREFIX-#.md) — Branch: `feature/PREFIX-#-description` | Status: ACTIVE
```

## Step 5: Check for PRD

- Search `docs/prds/active/` for an existing PRD for this milestone
- If PRD exists and is >2 weeks old, audit it against current codebase
- If no PRD exists and milestone is >6 hours, consider creating one

## Step 6: Write Status Line

Write the initial status label for the new branch. The status-line helper derives the branch-slug from the current branch, so no manual slugging needed:

```bash
bash .claude/skills/_shared/status-line.sh write "[<identifier>] setup"
```

Update with a more specific focus (e.g., `"[<identifier>] phase 1 — scaffolding"`) as soon as work on the first phase begins.

## Step 7: Initial Commit

```bash
git add docs/current-story.md docs/next-prompt.md docs/next-prompt-[milestone].md
git commit -m "PREFIX-#.#: Set up milestone - [description]"
git push
```

## Verification

- [ ] On feature branch (not main)
- [ ] Branch name follows `feature/PREFIX-#.#-description` format
- [ ] current-story.md updated with ACTIVE status
- [ ] `docs/next-prompt-[milestone].md` created with implementation guidance
- [ ] `docs/next-prompt.md` has pointer to branch-specific file under Active Milestones
- [ ] Branch-keyed status file written via `status-line.sh write`
- [ ] Initial commit pushed to remote
