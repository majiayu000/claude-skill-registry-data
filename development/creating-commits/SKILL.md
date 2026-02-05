---
name: creating-commits
description: Use before EVERY git commit - no exceptions. Enforces pre-commit quality checks, atomic commits, and conventional commit format to prevent hook failures and maintain clean history
---

# Creating Commits

Use before ANY commit - never skip for "simple" changes.

## MANDATORY FIRST STEP

**STOP: Create TodoWrite checklist BEFORE running any commands.**

**Correct pattern:**

1. Load this skill ✓
2. TodoWrite with 6 checklist items (see below) → FIRST response
3. Execute steps, updating todos (step 1 runs two operations in parallel)

**Wrong pattern (will fail):**

1. Load skill
2. Run git commands without TodoWrite
3. Forget a step
4. Hook blocks commit ❌

## Workflow Checklist

**Create these TodoWrite items as your FIRST action, ALL steps are required:**

1. ☐ Run `pnpm pre-commit` (if available) AND Read `docs/commit_specification.md` (PARALLEL)
2. ☐ Run `git diff` and analyze staging (see below)
3. ☐ `git add <files>` (stage atomic unit of related files)
4. ☐ `git diff --staged` (preview commit)
5. ☐ Write `.claude/.commit-state.json` (signals workflow completion)
6. ☐ `git commit -m "type(scope): description"`

**Parallel optimization:** Step 1 runs `pnpm pre-commit` (if the script exists) and reads `docs/commit_specification.md` simultaneously since they have no dependencies.

### Steps 2-3: Staging Analysis

Before running `git add`, check current staging state:

**Never stage files containing secrets** (`.env`, `credentials.json`, `*.pem`, `*_key`, etc.) - warn user if these appear in diff.

**Some files already staged?** User pre-selected - verify staged files form atomic unit.

**No files staged?** After reviewing `git diff`, evaluate what constitutes an atomic unit:

- If all changes form one logical unit → stage all files and proceed
- If multiple logical changes detected → use AskUserQuestion to ask which atomic unit to commit first, then suggest splitting rest into separate commits

**Multiple logical changes?** See Atomic Commits section below for how to identify and split.

### Step 5: Write Commit State File

Write this file after steps 1-4 and before step 6:

```bash
cat > .claude/.commit-state.json <<'EOF'
{
  "workflow_completed": true
}
EOF
```

This signals the pre-commit hook that you followed the workflow.
Expires in 5 minutes, auto-deletes after ANY `git commit` attempt (success or failure).

**If commit fails/is blocked:** Rewrite this file before retrying.

## Commit Message Format

`type(scope): description` - see [docs/commit_specification.md](../../docs/commit_specification.md)

**Focus on PURPOSE, not process:**

- ✅ "add creating-commits skill for git workflow"
- ❌ "create skill and refactor for efficiency"

Review FULL diff - message describes collective change, not just latest conversation.

## Atomic Commits

One logical change per commit.
If multiple concerns (mixed types, different scopes, unrelated files) → suggest splitting.

## Breaking Changes

If breaking backward compatibility → use `feat(api)!: description` and include `BREAKING CHANGE:` footer.

## Common Rationalizations (STOP)

**If you think any of these, STOP and follow checklist:**

- "Just a comment, skip checks" → Comments have syntax errors
- "User gave message, skip preview" → Can't see what's staged
- "Too simple for `pnpm pre-commit`" → Hooks fail on "simple" changes
- "One extra file won't hurt" → Breaks atomic commits

## When Checks Fail

**`pnpm pre-commit` fails on your changes?** Fix before committing.

**`pnpm pre-commit` fails on unrelated code?** Ask user:

1. Fix unrelated error first
2. Commit anyway (requires their decision)
3. Investigate error

Never assume "error is unrelated, skip check" - ask.

## Never Use `--no-verify`

Never use `git commit --no-verify` without **explicitly asking user permission first in bold text.**
