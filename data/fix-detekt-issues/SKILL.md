---
name: fix-detekt-issues
description: Automatically fixes detekt code quality issues by running detekt --auto-correct iteratively until all auto-correctable findings are resolved
---

# Fix Detekt Issues

Automatically resolves detekt code quality findings using detekt's auto-correct feature. Runs iteratively until all findings are fixed or no further progress can be made.

## Usage

```bash
./.claude/skills/fix-detekt-issues/auto-fix.main.kts
```

The script will:
1. Run `./gradlew detekt --auto-correct`
2. Parse the number of findings from the output
3. Repeat until findings reach 0 or stop decreasing
4. Report success or indicate manual fixes are needed

## Output Behavior

**Success (exit 0):**
```
Starting detekt auto-fix iterations...

=== Iteration 1 ===
Running: ./gradlew detekt --auto-correct
Progress: 42 findings remaining

=== Iteration 2 ===
Running: ./gradlew detekt --auto-correct
Progress: 15 findings remaining (reduced from 42)

=== Iteration 3 ===
Running: ./gradlew detekt --auto-correct
Progress: 0 findings remaining (reduced from 15)

✓ Success! All detekt findings have been resolved.
```

**No Progress (exit 1):**
```
Starting detekt auto-fix iterations...

=== Iteration 1 ===
Running: ./gradlew detekt --auto-correct
Progress: 23 findings remaining

=== Iteration 2 ===
Running: ./gradlew detekt --auto-correct

⚠ No progress: Findings count unchanged at 23.
Some findings cannot be auto-corrected and require manual fixes.
```

## How It Works

Detekt's `--auto-correct` flag automatically fixes many common code style and quality issues, but:
- A single run may not fix all issues (some fixes reveal new issues)
- Some findings cannot be auto-corrected and require manual intervention

This script handles both scenarios by:
- Running multiple iterations to handle cascading fixes
- Detecting when no progress is made (manual fixes needed)
- Providing clear feedback on progress and final state

## Safety Features

- **Maximum iterations**: Stops after 10 iterations to prevent infinite loops
- **Progress detection**: Exits if findings don't decrease
- **Anomaly detection**: Warns if findings unexpectedly increase

## When to Use

- Before committing code to ensure code quality standards
- After bulk code changes or refactoring
- When preparing code for review
- As part of CI/CD pre-commit checks

## Manual Fixes

If the script exits with remaining findings that cannot be auto-corrected:

1. Run `./gradlew detekt` to see detailed findings
2. Review the HTML report at `build/reports/detekt/detekt.html`
3. Fix issues manually or suppress with `@Suppress("RuleName")` if justified
4. Rerun the script to verify all issues are resolved

## Integration with Claude Code

This skill is automatically available to Claude Code. When Claude detects code quality issues or after making significant changes to Kotlin code, it can proactively use this skill to ensure code quality standards are met.
