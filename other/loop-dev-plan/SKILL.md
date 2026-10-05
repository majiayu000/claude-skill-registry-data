---
name: loop-dev-plan
description: Iterate development from plans in .cursor/plans. Implements plan tasks, validates self-testing, marks complete, moves to docs/plans/done/, and commits. Use when user wants to work through pending plans with validate-review-commit loop.
---

# Loop Dev Plan

Iteratively develop plans from `.cursor/plans`, validate, move to `docs/plans/done`, and commit.

## Workflow

### Step 1: Check Pending Plans

List files in `.cursor/plans/`:

```bash
ls -la .cursor/plans/
```

**If no files exist**: Exit with message "No pending plans found. Development loop complete."

**If files exist**: Select the first (oldest by modification time) plan file.

### Step 2: Check Plan Status

Read the plan file and check whether it is already marked as completed.

A plan is considered **completed** when its YAML front matter contains `status: completed` (typically the `todos` list also has every entry with `status: completed`).

- **If the plan is already completed**:
    - Skip Steps 3–6 (no implementation, testing, review, or commit).
    - Jump directly to **Step 7: Mark Complete & Move** to relocate it to `docs/plans/done/`.
    - Log a single line: `[Step 2] Plan already completed — skipping implementation`.
    - Continue to **Step 8** to process the next plan.
- **If the plan is not completed**: Continue with Step 3 as normal.

### Step 3: Read Plan (When Not Completed)

Read the plan file to understand:

- What tasks need to be implemented
- What self-testing or validation is required
- Any specific completion criteria

### Step 4: Implement Plan

Execute tasks defined in the plan:

- Make code changes as specified
- Follow project coding standards

### Step 5: Self-Testing

Run validation/tests as specified in the plan:

- Follow any test instructions in the plan
- Fix any failures
- Repeat until tests pass

### Step 6: Code Review

Review modified files against project standards:

**API code** (Python in `apps/api/`):

- Follow: `.cursor/rules/python-standards.mdc`
- Key areas: logging, retry, JSON formatting, Pydantic models, DRY utilities

**Web code** (TypeScript/TSX in `apps/web/`):

- Follow: `.cursor/rules/ts-tsx-react-language-standards.mdc`
- Key areas: string/number comparison, type placement, constants, React components

For each standard violation found, fix it.

### Step 7: Commit

**Only commit when actual code changes were made.** If the plan was already completed in Step 2 and you only moved the file, skip this step (no commit needed).

After all validations pass and code review is complete:

```bash
git status
git diff --stat
git log --oneline -5  # for commit message style reference
```

Create a commit with message following project conventions (conventional commits format). **Do not push to remote — only commit locally.**

### Step 8: Mark Complete & Move

Move the plan file from `.cursor/plans/` to `docs/plans/done/`:

```bash
mv .cursor/plans/<plan-file> docs/plans/done/<plan-file>
```

Optionally rename with completion timestamp:

```bash
mv .cursor/plans/plan.md docs/plans/done/plan-2024-01-15.md
```

### Step 9: Loop or Exit

- If more pending plans exist: Continue from Step 1 with the next plan
- If no more plans: Exit with "All plans processed. Development loop complete."

## Progress Tracking

Track progress in output:

```
[Loop Dev Plan] Processing: <plan-name>
  [Step 1: Pending plans found
  [Step 2: Plan already completed — skipping implementation
  [Step 8: Moved to done/
```

```
[Loop Dev Plan] Processing: <plan-name>
  [Step 1: Pending plans found
  [Step 3: Implementation complete
  [Step 5: Self-testing passed
  [Step 6: Code review complete
  [Step 7: Committed (local only — no push)
  [Step 8: Moved to done/
```

## Guardrails

- Always detect plan completion status before implementing (Step 2)
- Always skip implementation/testing/review/commit when plan is already completed
- Always code review before commit
- Always move to done before checking next plan
- Always commit locally only — **never push** to remote
- Always exit cleanly when no plans remain
- Mark tasks complete in plan as they are done
