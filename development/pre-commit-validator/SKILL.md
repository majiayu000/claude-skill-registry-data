---
name: pre-commit-validator
description: Validates code quality before commits in the MigraineTracker React Native project. Use this skill when preparing to commit code, before pushing changes, or when the user asks to run pre-commit checks. Ensures TypeScript type safety, test coverage (80%+), passing tests, and proper branch strategy compliance.
---

# Pre-Commit Validator

## Overview

Automates the pre-commit validation workflow for the MigraineTracker React Native application. Runs all required checks to ensure code quality, test coverage, and adherence to project standards before allowing commits.

## When to Use This Skill

Invoke this skill when:
- User is preparing to commit code
- User asks "Can I commit this?" or "Run pre-commit checks"
- Before any git push operation (per project requirements)
- User mentions committing, pushing, or creating a pull request
- After making significant changes that should be validated

## Pre-Commit Validation Workflow

### Step 1: Verify Working Directory

Ensure the current working directory is `/app` (the React Native application root). All validation commands must run from this directory.

```bash
cd /Users/vfilby/Projects/MigraineTracker/app
```

### Step 2: Run TypeScript Type Checking

Execute TypeScript compiler in check mode to identify type errors:

```bash
npx tsc --noEmit
```

**Success criteria**: No type errors reported.

**If failures occur**: Report the specific type errors to the user. Do not proceed until all type errors are resolved.

### Step 3: Run Unit and Integration Tests

Execute the Jest test suite:

```bash
npm test -- --coverage
```

**Success criteria**: All tests pass.

**If failures occur**: Report which tests failed and the error messages. Do not proceed until all tests pass. Remember: Never skip, delete, or comment out failing tests - always fix the underlying issue.

### Step 4: Validate Test Coverage

Check that test coverage meets the 80% threshold for all metrics (statements, branches, functions, lines).

Coverage data is available in `coverage/coverage-summary.json` after running tests with `--coverage`.

**Coverage requirements**:
- **Minimum 80% coverage** for:
  - Repositories (`src/database/*Repository.ts`)
  - Stores (`src/store/*.ts`)
  - Utilities (`src/utils/*.ts`)
- **All four metrics** must meet threshold:
  - Statements
  - Branches
  - Functions
  - Lines

**If coverage is insufficient**: Identify which files or code paths lack coverage and recommend adding tests. Reference `references/testing-requirements.md` for detailed testing standards.

### Step 5: Validate Branch Strategy

Check the current git branch to ensure the user is not committing directly to `main` or `master`:

```bash
git branch --show-current
```

**Success criteria**: Current branch is NOT `main` or `master`.

**If on main/master**: Alert the user that direct commits to main/master are forbidden. Recommend creating a feature branch:

```bash
git checkout -b feature/descriptive-name
```

Branch naming conventions:
- Features: `feature/description`
- Bug fixes: `bugfix/description`

### Step 6: Report Validation Results

After completing all checks, provide a clear summary:

**If all checks pass**:
```
✅ All pre-commit validation checks passed!
   - TypeScript: No errors
   - Tests: All passing
   - Coverage: XX% (meets 80% requirement)
   - Branch: feature/branch-name

You may proceed with your commit.
```

**If any checks fail**:
```
❌ Pre-commit validation failed:
   - [List specific failures]

Please resolve these issues before committing.
```

## Using the Validation Script

This skill includes an automated validation script at `scripts/validate.sh` that executes all five validation steps in sequence.

To use the script:

```bash
cd /Users/vfilby/Projects/MigraineTracker/app
bash /path/to/scripts/validate.sh
```

The script will:
1. Verify working directory
2. Run TypeScript type checking
3. Run unit/integration tests with coverage
4. Validate coverage meets 80% threshold
5. Validate branch strategy
6. Report comprehensive results

**Note**: The script exits on the first failure, making it efficient for catching issues early.

## Project-Specific Testing Details

For comprehensive information about the MigraineTracker testing requirements, refer to `references/testing-requirements.md`, which includes:

- Complete testing stack details
- E2E testing with Detox
- Test troubleshooting guides
- Platform-specific considerations
- Testing principles and best practices

## Key Reminders

- **All commands run from `/app` directory**
- **Never skip or delete failing tests** - always fix the root cause
- **80% coverage required** for repositories, stores, and utilities
- **Never commit directly to main/master** - always use feature branches
- **iOS is the primary platform** - test iOS first
- **Pre-commit checks are mandatory** before pushing code
