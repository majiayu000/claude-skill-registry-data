---
name: copilot-pr-reviewer
description: Reviews pull requests created by GitHub Copilot agents before merging. Triggers on "review this PR", "check PR #123", "validate agent work", or automatically when agents complete work. Ensures quality gates are met.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__github__*
---

# GitHub Copilot PR Reviewer

This skill reviews pull requests created by GitHub Copilot agents to ensure quality, correctness, and alignment with project standards before merging.

## When to Use This Skill

**Auto-trigger** when:

- User says: "Review PR #123"
- User says: "Check this pull request"
- User says: "Validate agent work"
- User says: "Is this PR ready to merge?"
- After a Copilot agent completes work and opens a PR
- Before merging any agent-created PR

**Manual trigger**:
- Final review before merging
- When PR has been updated after review comments
- Periodic review of open PRs

## Mission

Ensure all agent-created pull requests meet quality standards:

1. **Code correctness** - Does it do what it should?
2. **Test coverage** - Are changes tested?
3. **No regressions** - Did it break anything?
4. **Style compliance** - Follows project conventions?
5. **Security** - No vulnerabilities introduced?
6. **Performance** - No performance degradation?

## Review Checklist

See `checklists/` directory for domain-specific checklists:

- `frontend-review.md` - React, UI, components
- `backend-review.md` - API, database, server
- `testing-review.md` - Test quality and coverage
- `security-review.md` - Security considerations
- `performance-review.md` - Performance impact

## Review Process (Using GitHub MCP)

### 1. Fetch PR & Changes

**Use GitHub MCP to get PR details**:
```javascript
// Get PR metadata
const pr = await mcp__github__pull_request_read({
  method: "get",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber
})

// Get changed files
const files = await mcp__github__pull_request_read({
  method: "get_files",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber
})

// Get CI/CD status
const checks = await mcp__github__pull_request_read({
  method: "get_status",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber
})
```

Verify PR has:
- [ ] Clear title describing what was changed
- [ ] Description explaining why
- [ ] Links to related issue(s)
- [ ] Appropriate labels
- [ ] No merge conflicts (`pr.mergeable === true`)
- [ ] CI/CD checks passing (`checks.every(c => c.conclusion === "success")`)

### 2. Code Review with Inline Comments

**Create pending review**:
```javascript
await mcp__github__pull_request_review_write({
  method: "create",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber,
  body: "Reviewing changes..."
})
```

**Analyze each file** using domain-specific checklist:
- [ ] Changes match issue requirements
- [ ] Code is readable and maintainable
- [ ] No obvious bugs or issues
- [ ] Error handling is appropriate
- [ ] TypeScript types are correct
- [ ] No console.logs or debug code left in

**Add inline comments for issues**:
```javascript
await mcp__github__add_comment_to_pending_review({
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber,
  path: "client/src/components/Profile.tsx",
  body: "🚫 **Blocking**: Remove console.log before merging.",
  line: 42,
  side: "RIGHT",
  subjectType: "LINE"
})
```

### 3. Testing Review

Verify:
- [ ] Tests added for new functionality
- [ ] Tests updated for changed functionality
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Test coverage adequate (no major gaps)

### 4. Impact Analysis

Check:
- [ ] No breaking changes (or documented if intentional)
- [ ] Database migrations work correctly
- [ ] API contracts maintained
- [ ] Dependencies updated safely
- [ ] Performance impact acceptable

### 5. Security Review

For changes involving:
- [ ] Authentication/authorization logic
- [ ] User input handling
- [ ] Database queries
- [ ] External API calls
- [ ] File uploads
- [ ] Sensitive data

Verify no new vulnerabilities introduced.

### 6. Final Checks

Before approval:
- [ ] `npm run check` passes (TypeScript)
- [ ] No new ESLint warnings
- [ ] Documentation updated if needed
- [ ] CLAUDE.md updated if new patterns introduced

## Review Outcomes (Submit via GitHub MCP)

### ✅ Approve

**When**: PR meets all quality standards, inline comments added

**Submit approval**:
```javascript
await mcp__github__pull_request_review_write({
  method: "submit_pending",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber,
  body: `## Review: APPROVED ✅

This PR looks great! All quality checks passed.

**Verified**:
- ✅ Code correctness
- ✅ Test coverage
- ✅ No regressions
- ✅ Style compliance
- ✅ Security
- ✅ Performance

**Ready to merge**: Yes
**Suggested next steps**: Merge and close #${issueNumber}`,
  event: "APPROVE"
})
```

### 🔄 Request Changes

**When**: PR has blocking issues (already added as inline comments)

**Submit change request**:
```javascript
await mcp__github__pull_request_review_write({
  method: "submit_pending",
  owner: "{owner}",
  repo: "{repo}",
  pullNumber: prNumber,
  body: `## Review: CHANGES REQUESTED 🔄

Found ${blockingIssues.length} blocking issue(s) that need attention.

All issues have been marked inline with specific line comments.

### Summary
- 🚫 Blocking: ${blockingIssues.length}
- 💡 Suggestions: ${suggestions.length}

Please address the blocking issues and update the PR.`,
  event: "REQUEST_CHANGES"
})
```

Note: Individual issues are already added as inline comments via `add_comment_to_pending_review`

### ⚠️ Needs Discussion

PR has architectural or approach concerns:

```markdown
## Review: DISCUSSION NEEDED ⚠️

The implementation works, but I have concerns about the approach.

### Concerns

1. **[Concern 1]**
   - What: [What's concerning]
   - Why: [Why it's a problem]
   - Alternatives: [Alternative approaches]

2. **[Concern 2]**
   - What: [What's concerning]
   - Why: [Why it's a problem]
   - Alternatives: [Alternative approaches]

**Recommendation**: Let's discuss the approach before proceeding.

@[User] please weigh in on preferred approach.
```

## Agent Feedback

Provide constructive feedback to improve agent work:

### Positive Feedback
```markdown
**Nice work on**:
- Clean separation of concerns in the API layer
- Comprehensive test coverage
- Good error handling patterns
```

### Improvement Areas
```markdown
**For future PRs**:
- Consider extracting this 50-line function into smaller units
- Add JSDoc comments for complex logic
- Use `const` instead of `let` where possible
```

## Integration with Workflow

### In Multi-Agent Workflows

Review happens at transition points:

```
Phase 1: Backend
  ↓
  PR #200 created
  ↓
  🔍 PR Review (this skill)
  ↓
  ✅ Approved & Merged
  ↓
Phase 2: Frontend (unblocked)
```

### Review Triggers

- **After agent completes work** - Review before next phase
- **Before workflow continues** - Validate checkpoint
- **On PR update** - Re-review after changes
- **Manual request** - User asks for review

## Quality Gates

### Must Pass to Merge

1. **All tests passing** - CI/CD green
2. **No TypeScript errors** - `npm run check` clean
3. **No blocking issues** - All critical items resolved
4. **Security reviewed** - If touching auth/data/APIs
5. **Performance acceptable** - No major degradation

### Should Pass to Merge

1. **Code coverage maintained** - No significant drops
2. **Documentation updated** - If needed
3. **Mobile responsive** - For UI changes
4. **Accessibility maintained** - For UI changes

## Special Review Cases

### Database Migrations

Extra checks:
- [ ] Migration is reversible
- [ ] No data loss
- [ ] Tested on copy of prod data
- [ ] Indexes added where needed
- [ ] Migration runs quickly (<1 min)

### API Changes

Extra checks:
- [ ] Backward compatible or version bumped
- [ ] Documentation updated
- [ ] Error responses documented
- [ ] Rate limiting considered

### Security-Related Changes

Extra checks:
- [ ] Security Specialist reviewed
- [ ] No hardcoded secrets
- [ ] Input validated
- [ ] Authorization checked
- [ ] Sensitive data encrypted

### Performance-Critical Changes

Extra checks:
- [ ] Performance Specialist reviewed
- [ ] Benchmarks run
- [ ] No N+1 queries introduced
- [ ] Caching strategy sound

## Reference Documentation

- **Checklists**: See `checklists/` directory
- **Review templates**: See `reference/review-templates.md`
- **Common issues**: See `reference/common-issues.md`

## What This Skill Does

- Reviews PRs for quality and correctness
- Checks tests and coverage
- Validates security and performance
- Provides constructive feedback
- Approves or requests changes
- Gates workflow progression

## What This Skill Doesn't Do

- Doesn't write code (agents do that)
- Doesn't fix issues (requests agent to fix)
- Doesn't make architectural decisions (discusses with user)
- Doesn't merge PRs (recommends merge, user decides)

## Output Format

### Review Summary

```
# PR Review Summary: #[PR-NUM]

**PR Title**: [Title]
**Issue**: #[issue-num]
**Agent**: @[Agent-Name]-Specialist
**Changes**: [Brief description]

## Review Status: [APPROVED ✅ | CHANGES REQUESTED 🔄 | DISCUSSION NEEDED ⚠️]

### Code Quality: [✅ | ⚠️ | ❌]
[Comments]

### Test Coverage: [✅ | ⚠️ | ❌]
[Comments]

### Security: [✅ | ⚠️ | ❌]
[Comments]

### Performance: [✅ | ⚠️ | ❌]
[Comments]

## Blocking Issues
[List or "None"]

## Suggestions
[List or "None"]

## Next Steps
[What should happen next]

**Reviewed by**: copilot-pr-reviewer skill
**Reviewed at**: [Timestamp]
```
