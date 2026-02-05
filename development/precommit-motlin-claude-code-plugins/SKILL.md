---
name: precommit
description: Running precommit checks and build validation. ALWAYS use after ANY code changes.
---

# Precommit and Build Validation

## 🔋 Battery Check

**CRITICAL**: Before running any build or test commands, check if the machine is on battery power:

```bash
scripts/check-battery || { echo "⚡ Skipping precommit on battery power"; exit 0; }
just precommit
```

- If on battery power, skip the build and report: "⚡ **Skipped precommit checks (on battery power)**"
- If on AC power, proceed with the build

## ⚙️ Running Precommit

Run `just precommit` to validate code:

- Use a timeout of at least 10 minutes
- Don't check if the justfile or recipe exists first
- This command typically runs autoformatting, builds, tests, and other quality checks

## 📋 Handle Missing Recipe

If the command fails because the justfile doesn't exist or the 'precommit' recipe is not defined, clearly explain this situation. Indicate whether the justfile file is missing or whether just the `precommit` recipe is missing.

## ❌ Handle Check Failures

When precommit fails (due to: type checking errors, test failures, linting issues, build errors):

- Analyze the error output to understand what failed
- Fix the specific failures
- Run the precommit command again
- Continue the fix-and-retry cycle until precommit completes successfully with exit code 0

## ✅ Reporting Results

Your final message MUST start with one of:

- "⚡ **Skipped precommit checks (on battery power)**" - if skipped due to battery
- "✅ **Precommit checks passed**" - if ran successfully
- "✅ **Precommit checks passed** (after fixing [brief description])" - if fixed issues

## Agents

| Task                    | Use                                  |
| ----------------------- | ------------------------------------ |
| Run precommit and fix   | `build:precommit-runner` agent       |
| Test all branch commits | `/build:test-branch` command         |
| Test and autosquash     | `build:build-fixer-autosquash` agent |
