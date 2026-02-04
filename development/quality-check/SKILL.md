---
name: quality-check
description: Run all quality checks including linting, formatting, and type checking. Use when user asks to check code quality, run checks, or verify code before committing.
allowed-tools: [Bash, TodoWrite]
---

# Quality Check Skill

Run comprehensive quality checks for the project including ESLint, Prettier formatting, and TypeScript type checking.

## Instructions

When this skill is invoked:

1. Execute the quality check script:

   ```bash
   bash .claude/skills/quality-check/scripts/run-checks.sh
   ```

2. The script will:
   - Run ESLint, Prettier formatting check, and TypeScript type checking
   - Display color-coded results for each check
   - Provide a summary showing passed/failed counts
   - List suggested fixes for any failures

3. If the script exits with code 1 (failures detected):
   - Show the complete output from the script
   - Ask the user if they want to run suggested auto-fix commands:
     - `npm run lint:fix` for linting issues
     - `npm run format` for formatting issues
   - Explain that type errors require manual fixes

4. If the script exits with code 0 (all passed):
   - Confirm success and show the script output
   - Let the user know the code is ready

## Script Details

The [run-checks.sh](scripts/run-checks.sh) script:

- Runs all three quality checks in sequence
- Uses colored output for better readability
- Tracks which checks failed and provides specific suggestions
- Returns appropriate exit codes for CI/CD integration

## When to Use

- User asks to "check code quality" or "run checks"
- Before creating a commit
- After making code changes
- When user asks "is the code ready?"

## Success Criteria

All three checks must pass (exit code 0) for overall success.
