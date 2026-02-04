---
name: local-review
description: Review current changes against project guidelines before PR
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: reviewer
---

# Local Review

Perform a comprehensive self-review of changes before creating a pull request.

## Instructions

1. **Gather Context**
   - Get current branch name
   - Find associated workflow folder
   - Read the original issue/concept and plan

2. **Get Changes**
   - Run `git diff main...HEAD` to see all changes
   - Run `git log main...HEAD --oneline` to see commits
   - List all modified files

3. **Review Against Guidelines**

   Review the code against **[REVIEW_GUIDELINES.md](../../../REVIEW_GUIDELINES.md)**, which covers:
   - Architecture checklist
   - Code style checklist
   - Configuration precedence checklist
   - Anti-over-engineering checklist
   - Testing checklist
   - Commit message checklist
   - Documentation checklist

4. **Code Quality Checks**
   ```bash
   # Build check
   go build ./...

   # Test check
   go test ./...

   # Format check
   go fmt ./...

   # Vet check
   go vet ./...
   ```

5. **Generate Review Report**

   Create a summary with:

   ```markdown
   # Local Review: <branch-name>

   ## Summary
   - Files changed: <count>
   - Lines added: <count>
   - Lines removed: <count>
   - Commits: <count>

   ## Checklist Results

   ### Passed
   - <item 1>
   - <item 2>

   ### Issues Found
   - [ ] <issue 1> - <file:line> - <description>
   - [ ] <issue 2> - <file:line> - <description>

   ### Warnings
   - <warning 1>

   ## Quality Checks
   - Build: PASS/FAIL
   - Tests: PASS/FAIL (<count> passed)
   - Format: PASS/FAIL
   - Vet: PASS/FAIL

   ## Recommendations
   1. <recommendation>
   2. <recommendation>

   ## Ready for PR?
   <YES/NO - explain if NO>
   ```

6. **Report Findings**
   - If issues found, list them with specific file:line references
   - Suggest fixes for each issue
   - Indicate if changes are PR-ready

## Issue Categories

### Blocking (must fix)
- Test failures
- Build errors
- Missing error handling
- Security concerns
- Guideline violations

### Warnings (should fix)
- Missing documentation
- Inconsistent naming
- Suboptimal patterns

### Suggestions (nice to have)
- Code clarity improvements
- Additional test cases
- Performance optimizations
