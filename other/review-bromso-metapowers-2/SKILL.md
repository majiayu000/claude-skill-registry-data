---
description: Review code pre-merge for bugs, security, quality, and test coverage
---

# Review

Review the code changes for "$ARGUMENTS" before merging. Check for bugs, security issues, code quality, and test coverage.

## Prerequisites

Read `.metapowers/development/$ARGUMENTS/02-build.md` if it exists, to understand what was built. If not available, review the current branch diff against main.

## Process

1. **Gather the changes:**
   - Read the git diff of all changed files (staged + unstaged, or branch diff vs. main)
   - Understand the scope and intent of the changes

2. **Check for bugs:**
   - Logic errors, off-by-one, null/undefined handling
   - Race conditions or state management issues
   - Missing error handling at system boundaries

3. **Check for security issues:**
   - Input validation at system boundaries (user input, external APIs)
   - No secrets, tokens, or credentials in code
   - No injection vulnerabilities (SQL, XSS, command injection)

4. **Check code quality:**
   - Naming clarity — do names describe what things do?
   - Unnecessary complexity — can anything be simplified?
   - Consistency with existing codebase patterns
   - No dead code, commented-out code, or TODO placeholders

5. **Check tests:**
   - Do tests exist for new functionality?
   - Do tests verify behavior, not implementation?
   - Are edge cases covered?

6. **Write the artifact** to `.metapowers/development/$ARGUMENTS/04-review.md` with sections:
   - **Summary** — what was reviewed and overall assessment
   - **Issues** — categorized by severity (critical, important, minor)
   - **Strengths** — what's well done
   - **Recommendations** — suggested improvements

## Output

The review report written to `.metapowers/development/$ARGUMENTS/04-review.md`. Present a summary to the user highlighting:
- Overall assessment (approve / request changes)
- Critical issues (if any)
- Key recommendations
