---
name: code-review-workflow
description: Use this skill when performing code review on branch changes. Runs parallel CodeRabbit and architecture reviews, consolidates findings, and executes improvements. Invoke when reviewing code changes before finalizing a PR.
---

# Code Review Workflow

This skill provides a structured code review process that combines automated tooling with architectural analysis.

## When to Use

- After implementing features or fixes, before finalizing a PR
- When `/fly` or `/refuel` reaches the code review phase
- When explicitly asked to review code changes

## Phase 1: Parallel Reviews

**Send notification:** Run `${CLAUDE_PLUGIN_ROOT}/scripts/notify.sh review "Starting code review"`

Launch two review processes simultaneously:

### Review A: CodeRabbit Review

```
Run `coderabbit review --prompt-only` and return the complete output.
Do not summarize - return everything.
```

### Review B: Architecture & Code Quality Review

```
Review all changes in this branch against clean code principles and clean architecture.

First, run `${CLAUDE_PLUGIN_ROOT}/scripts/get-changed-files.sh` to identify changed files.

Review criteria:

1. **Clean Code**
   - Single responsibility principle
   - DRY (Don't Repeat Yourself)
   - Meaningful naming
   - Function size and complexity
   - Comments (only where logic isn't self-evident)
   - Error handling

2. **Clean Architecture**
   - Dependency direction (inward only)
   - Layer separation
   - Abstraction boundaries
   - Coupling and cohesion
   - Testability

3. **Specification Compliance** (if spec exists)
   - Read all files in the spec directory
   - Verify implementation matches requirements

Return structured report with:
- File-by-file findings
- Severity (critical/major/minor/suggestion)
- Line numbers where applicable
- Concrete recommendations
```

## Phase 2: Consolidate Findings

Synthesize both reviews:

1. **Deduplicate** overlapping findings

2. **Categorize** each unique issue:
   - `[CRITICAL]` - Bugs, security issues, spec violations, incomplete fixes
   - `[MAJOR]` - Architecture/design problems
   - `[MINOR]` - Code quality improvements
   - `[STYLE]` - Formatting, naming

3. **Create prioritized TODO list**

4. **Analyze parallelization:**
   - Issues in different files → can parallelize
   - Same file or dependencies → must serialize
   - Max 3-4 parallel subagents

## Phase 3: Execute Improvements

For each batch of parallelizable issues, spawn subagents:

```
Task: Fix ISSUE-XXX

Issue: [description]
File(s): [files to modify]

Requirements:
- Minimal change for this specific issue
- Do NOT refactor unrelated code
- Run build/check commands before completing
- Note (don't fix) any new issues discovered
```

After each batch:
- Review changes for correctness
- Resolve any conflicts
- Update TODO list
- Proceed to next batch

## Phase 4: Commit Review Fixes

If any changes were made during the review process:

```bash
git add -A
git commit -m "refactor: address code review feedback

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

## Output

After completing the review workflow, report:
- Total issues found (by source: CodeRabbit vs Architecture review)
- Issues by severity
- Issues addressed
- Any remaining issues (with justification if deferred)
