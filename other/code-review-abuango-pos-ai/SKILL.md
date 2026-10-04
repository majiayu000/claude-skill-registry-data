---
name: code-review
description: Perform standardized code reviews for projects. Use when reviewing code, checking implementation quality, or when user mentions "code review", "review changes", "check the code", or "review implementation".
allowed-tools: Read, Glob, Grep, Bash
---

# Code Review Skill

You are performing a code review for the POS. Reviews ensure code quality, security, and adherence to the approved plan.

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

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
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
