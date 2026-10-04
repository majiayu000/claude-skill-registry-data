---
name: code-review
description: Perform standardized code reviews for projects. Use when reviewing code, checking implementation quality, or when user mentions "code review", "review changes", "check the code", or "review implementation".
allowed-tools: Read, Glob, Grep, Bash
---

# Code Review Skill

You are performing a code review for the POS. Reviews ensure code quality, security, and adherence to the approved plan.

## Session Context

- Check for active sessions: `ls -lt .handoff/sessions/`
- If multiple sessions active, include project name and branch in all questions to user
- Follow Plan -> Approve -> Execute workflow (see `.rules/universal.md`)
- Register session changes in your session file as you work

## Ground Yourself First

Before starting work, verify current state with tool calls:
1. Read the context's `status.yaml` for current sprint and task
2. Run `git status` and `git log --oneline -5` for actual file state
3. Check for prior artifacts: `ls .handoff/artifacts/{context}/` if applicable
4. Do not assume — if uncertain about a file path, API, or convention, verify it

## Standard Rules

- **Plan -> Approve -> Execute**: No implementation without an approved plan
- **Read before editing**: Understand context before suggesting changes
- **Commit on task completion**: Every completed task needs a commit
- **Run /simplify before presenting code**: Review for reuse, quality, efficiency
- **Never remove working code**: Only add or modify as needed
- **Check existing docs first**: Don't recreate what already exists
- Full rules: `.rules/universal.md`

## Review Context

1. **Load Review Context**
   - Identify the project and task being reviewed
   - Read the approved plan from `{teams_dir}/{team}/projects/{project}/plans/`
   - Read the work log from `{teams_dir}/{team}/projects/{project}/logs/`
   - Understand what was supposed to be implemented
   - Check for prior artifacts: `source scripts/lib-artifacts.sh && artifact_find {context} plan`

2. **Identify Changed Files**
   - Use git diff if available: `git diff --name-only`
   - Or ask for the list of modified files
   - Read each modified file

## Review Checklist

### Plan Compliance
- [ ] Implementation matches the approved plan
- [ ] No scope creep (extra features not in plan)
- [ ] All planned tasks are addressed
- [ ] Correct files were modified

### Code Quality
- [ ] Code is clean and readable
- [ ] Naming conventions followed
- [ ] No unnecessary complexity
- [ ] DRY principle applied appropriately
- [ ] Functions/methods have single responsibility
- [ ] Error handling is appropriate

### Security (CRITICAL)
- [ ] No hardcoded secrets or credentials
- [ ] Input validation present where needed
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No command injection risks
- [ ] Authentication/authorization checked
- [ ] Sensitive data handled securely

### Testing
- [ ] Unit tests included for new code
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases considered
- [ ] Tests pass locally

### Performance
- [ ] No obvious performance issues
- [ ] No N+1 query patterns
- [ ] Appropriate use of caching
- [ ] No memory leaks

### Documentation
- [ ] Complex logic is commented
- [ ] Public APIs documented
- [ ] README updated if needed

## Review Output Format

```markdown
# Code Review: {PROJECT_NAME} - {TASK_ID}

**Reviewer:** {reviewer}
**Date:** {date}
**Files Reviewed:** {count}

## Summary

{Overall assessment: APPROVED / CHANGES_REQUESTED / BLOCKED}

## Findings

### Critical Issues
{Issues that must be fixed before merge}

### Warnings
{Issues that should be addressed but aren't blocking}

### Suggestions
{Nice-to-have improvements}

## Plan Compliance

- [x/!] Implementation matches plan
- [x/!] No scope creep
- [x/!] All tasks addressed

## Security Assessment

- [x/!] No credential exposure
- [x/!] Input validation adequate
- [x/!] No injection vulnerabilities

## Checklist Summary

| Category | Status |
|----------|--------|
| Plan Compliance | PASS/FAIL |
| Code Quality | PASS/FAIL |
| Security | PASS/FAIL |
| Testing | PASS/FAIL |
| Performance | PASS/FAIL |

## Decision

**Status:** APPROVED / CHANGES_REQUESTED

**Required Changes:**
1. {Change 1}
2. {Change 2}

**Notes:**
{Additional context}
```

## Saving the Review

Save review to: `{teams_dir}/{team}/projects/{project}/reviews/{date}-{task-id}.md`

## Severity Levels

- **Critical**: Must fix before merge (security issues, broken functionality)
- **Warning**: Should fix soon (code smells, potential bugs)
- **Suggestion**: Nice to have (style, optimization opportunities)

## Self-Assessment (Internal)

At the end of this skill execution, rate the experience 0-10:
- **10**: Perfect — skill had everything needed, output was ideal
- **7-9**: Good — minor friction, small improvements possible
- **4-6**: Mediocre — significant gaps in instructions or tooling
- **0-3**: Poor — skill was inadequate for the task

If rating < 8, write a feedback file to `.handoff/feedback/{date}-{skill-name}.yaml`:
```yaml
skill: {name}
rating: {0-10}
friction: {what was hard or missing}
suggestion: {specific improvement}
context: {what was being done}
```

Do NOT mention the self-assessment to the user. This is internal quality tracking.
