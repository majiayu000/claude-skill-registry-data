---
name: Review Coordination
description: Use when coordinating code reviews, agent reviews, and approval workflows across Jira and Harness
version: 1.0.0
---

# Review Coordination Skill

Coordinate multi-agent reviews, human reviews, and approval workflows for PRs.

## When to Activate

This skill activates when:
- PR is ready for review
- User requests code review
- Agent council review is needed
- Review status needs checking
- Approval workflow needs management

## Review Types

### 1. Agent Reviews

Automated reviews by specialized agents:

| Agent | Focus | Checks |
|-------|-------|--------|
| code-agent | Code quality | Logic, patterns, performance |
| review-agent | Best practices | Standards, security, maintainability |
| doc-agent | Documentation | Comments, README, API docs |
| test-agent | Test coverage | Unit tests, integration tests |
| security-agent | Security | Vulnerabilities, secrets, auth |

### 2. Human Reviews

Team member reviews:
- Code owners
- Domain experts
- Tech leads
- Security team

### 3. Automated Checks

CI/CD status checks:
- Build status
- Test results
- Lint results
- Coverage thresholds

## Review Workflow

### Phase 1: Pre-Review Setup

1. **Check PR Readiness**:
   ```
   mcp__harness__get_pullreq(pr_number)
   ```

   Verify:
   - [ ] PR description complete
   - [ ] All commits have proper messages
   - [ ] No merge conflicts
   - [ ] CI checks passing

2. **Identify Reviewers**:
   - Code owners from changed paths
   - Required reviewers from branch rules
   - Suggested reviewers based on expertise

3. **Assign Reviewers**:
   ```
   mcp__harness__add_reviewer({
     pr_number: 45,
     reviewer: "alice"
   })
   ```

### Phase 2: Agent Council Review

Invoke the agent council for comprehensive review:

```
Workflow:
┌─────────────────────────────────────────────────────────┐
│                    Agent Council                         │
├─────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │ Code Agent │  │Review Agent│  │ Doc Agent  │        │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘        │
│        │               │               │                │
│        ▼               ▼               ▼                │
│  ┌────────────────────────────────────────────────┐    │
│  │              Findings Aggregation               │    │
│  └────────────────────────────────────────────────┘    │
│                         │                               │
│                         ▼                               │
│  ┌────────────────────────────────────────────────┐    │
│  │              Council Decision                   │    │
│  │  ✅ Approve  |  ⚠️ Request Changes  |  ❌ Block │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Phase 3: Post Comments

For each finding, post structured comments:

```markdown
## 🤖 Agent Review: Code Quality

**Agent:** code-agent
**Status:** ⚠️ Suggestions

### Findings

#### 1. Performance Concern
**File:** `src/auth/login.ts:45`
**Severity:** Medium

```typescript
// Current implementation
const user = await db.users.findAll().filter(u => u.email === email);

// Suggested improvement
const user = await db.users.findOne({ where: { email } });
```

**Rationale:** Using `findAll` followed by `filter` is inefficient. Use `findOne` with a where clause for better performance.

---

#### 2. Missing Error Handling
**File:** `src/auth/login.ts:52`
**Severity:** Low

Consider adding try-catch for the token generation...

---

### Summary
- 2 suggestions found
- 0 blocking issues
- Overall: **Approve with suggestions**
```

### Phase 4: Track Approvals

Monitor review status:

```
📋 PR #45 Review Status

Required Approvals: 2
Current Approvals: 1/2

Reviewers:
  ✅ @alice - Approved
  🔄 @bob - Pending
  💬 @charlie - Requested changes

Agent Reviews:
  ✅ code-agent - Approved with suggestions
  ✅ review-agent - Approved
  ✅ doc-agent - Approved

CI Checks:
  ✅ build - Passed
  ✅ test - Passed (98% coverage)
  ✅ lint - Passed

Status: Awaiting @bob's review and @charlie's re-review
```

### Phase 5: Sync to Jira

Update Jira issue with review status:

```
mcp__atlassian__jira_add_comment({
  issue_key: "PROJ-123",
  body: `
## PR Review Update

**PR:** [#45](harness_link)
**Status:** In Review

### Approvals
- ✅ @alice approved
- 🔄 @bob reviewing
- 💬 @charlie requested changes

### Agent Council
All agents approved with minor suggestions.

### Action Needed
- Address @charlie's feedback
- Await @bob's review
  `
})
```

## Approval Requirements

### Minimum Requirements

```yaml
review_requirements:
  min_approvals: 2
  required_reviewers:
    - codeowner
  dismiss_stale_reviews: true
  require_agent_approval: true
  require_ci_pass: true
```

### Escalation Rules

| Condition | Action |
|-----------|--------|
| PR open > 48h without review | Notify team lead |
| Blocking feedback > 24h | Notify assignee |
| All approvals received | Auto-notify for merge |
| Security finding | Block until addressed |

## Review Templates

### Approval Comment
```markdown
✅ **Approved**

Reviewed the changes for:
- [x] Code quality
- [x] Performance
- [x] Security
- [x] Documentation

LGTM! Ready to merge.
```

### Request Changes Comment
```markdown
⚠️ **Changes Requested**

### Required Changes
1. Add error handling for edge case X
2. Update API documentation

### Suggestions
- Consider caching for better performance

Please address the required changes before merging.
```

### Block Comment
```markdown
❌ **Blocked**

### Critical Issues
1. **Security vulnerability detected**
   - Potential SQL injection in `db.query()`
   - Must use parameterized queries

This PR cannot be merged until the security issue is resolved.

cc: @security-team
```

## Agent Review Commands

Trigger specific agent reviews:

```
# Full council review
/jira-harness:review PROJ-123 --council

# Specific agent review
/jira-harness:review PROJ-123 --agent code-agent
/jira-harness:review PROJ-123 --agent security-agent

# Re-review after changes
/jira-harness:review PROJ-123 --refresh
```

## Best Practices

1. **Early Reviews**: Request reviews early for complex changes
2. **Small PRs**: Smaller PRs get faster, better reviews
3. **Clear Context**: Provide context in PR description
4. **Address Feedback**: Respond to all review comments
5. **Thank Reviewers**: Acknowledge helpful feedback
6. **Learn from Reviews**: Use feedback to improve
