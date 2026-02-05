---
name: sentry-fix-issues
description: Find and fix issues from Sentry using MCP. Use when asked to fix Sentry errors, debug production issues, investigate exceptions, or resolve bugs reported in Sentry. Methodically analyzes stack traces, breadcrumbs, traces, and context to identify root causes.
---

# Fix Sentry Issues

Discover, analyze, and fix production issues using Sentry's full debugging capabilities.

## Invoke This Skill When

- User asks to "fix Sentry issues" or "resolve Sentry errors"
- User wants to "debug production bugs" or "investigate exceptions"
- User mentions issue IDs, error messages, or asks about recent failures
- User wants to triage or work through their Sentry backlog

## Prerequisites

- Sentry MCP server configured and connected
- Access to the Sentry project/organization

## Phase 1: Issue Discovery

Use Sentry MCP to find issues to work on:

```
# Get recent unresolved issues
mcp: sentry_search_issues
  query: "is:unresolved"
  sort: "date"

# Or search for specific errors
mcp: sentry_search_issues
  query: "is:unresolved error.type:TypeError"

# Or get a specific issue by ID
mcp: sentry_get_issue
  issue_id: "PROJECT-123"
```

**Before proceeding, confirm with user which issue(s) to fix.**

## Phase 2: Deep Issue Analysis

For each issue, gather ALL available context:

### 2.1 Core Error Data
```
mcp: sentry_get_issue
  issue_id: "[ISSUE_ID]"
```

Extract and document:
- [ ] Exception type and message
- [ ] Full stack trace (every frame)
- [ ] File paths and line numbers
- [ ] Function/method names in call chain

### 2.2 Event Details
```
mcp: sentry_get_event
  issue_id: "[ISSUE_ID]"
  event_id: "[LATEST_EVENT_ID]"
```

Extract:
- [ ] Breadcrumbs (user actions, console logs, HTTP requests leading to error)
- [ ] Tags (browser, OS, environment, release, user segment)
- [ ] Custom context (user data, feature flags, app state)
- [ ] Request data (URL, headers, body if available)

### 2.3 Trace Context (if available)
```
mcp: sentry_get_trace
  trace_id: "[TRACE_ID_FROM_EVENT]"
```

Map the full transaction:
- [ ] Parent transaction and spans
- [ ] Database queries before failure
- [ ] External API calls and their durations
- [ ] Where in the trace did the error occur?

### 2.4 Replay Data (if available)
```
mcp: sentry_get_replay
  replay_id: "[REPLAY_ID_FROM_EVENT]"
```

Note:
- [ ] User actions before the error
- [ ] UI state at time of failure
- [ ] Network requests visible in replay

## Phase 3: Root Cause Hypothesis

Before touching code, you MUST document:

1. **Error Summary**: One sentence describing what went wrong
2. **Immediate Cause**: The direct code path that threw
3. **Root Cause Hypothesis**: Why the code reached this state
4. **Supporting Evidence**: Breadcrumbs, traces, or context that support this
5. **Alternative Hypotheses**: What else could explain this? Why is your hypothesis more likely?

**Challenge yourself**: Could this be a symptom of a deeper issue? Check:
- Is this error type occurring elsewhere?
- Are there related issues with similar stack traces?
- Does the trace show upstream failures that caused this?

## Phase 4: Code Investigation

### 4.1 Locate the Failing Code
Read every file in the stack trace, starting from the top (where error was thrown):

```
Read [file_from_stack_trace] at line [N] with surrounding context
```

### 4.2 Trace Data Flow
For each variable involved in the error:
- [ ] Where does this value originate?
- [ ] What transformations does it undergo?
- [ ] What assumptions does the code make about it?
- [ ] Are those assumptions validated?

### 4.3 Check Error Boundaries
- [ ] Is there try/catch around this code?
- [ ] If yes, why didn't it handle this case?
- [ ] If no, should there be?

### 4.4 Review Related Code
- [ ] Are there similar patterns elsewhere that might have the same bug?
- [ ] Check tests - is this scenario covered?
- [ ] Check recent changes - was this introduced by a recent commit?

```bash
git log --oneline -20 -- [file_path]
git blame [file_path] | grep -A2 -B2 "[line_number]"
```

## Phase 5: Implement Fix

### 5.1 Fix Requirements Checklist
Before writing code, confirm your fix will:
- [ ] Handle the specific case that caused the error
- [ ] Not break existing functionality
- [ ] Handle edge cases (null, undefined, empty, malformed)
- [ ] Provide meaningful error messages if it still fails
- [ ] Be consistent with codebase patterns

### 5.2 Apply the Fix
Implement the minimum change that resolves the issue. Prefer:
1. Input validation over try/catch when possible
2. Graceful degradation over hard failures
3. Specific error handling over generic catches
4. Fixing root cause over patching symptoms

### 5.3 Add Tests (if applicable)
Write a test that:
- Reproduces the exact conditions from the Sentry event
- Verifies the fix handles this case
- Tests related edge cases

## Phase 6: Verification Audit

**You MUST complete this audit before declaring the issue fixed:**

### 6.1 Evidence Review
- [ ] Does your fix address the exact error message from Sentry?
- [ ] Does your fix handle the data state shown in the event context?
- [ ] Would your fix have prevented ALL events for this issue, not just some?

### 6.2 Regression Check
- [ ] Could your fix break any existing functionality?
- [ ] Are there other code paths that call this function?
- [ ] Have you maintained backward compatibility?

### 6.3 Completeness Check
- [ ] Did you check for similar patterns elsewhere in the codebase?
- [ ] Are there related Sentry issues that might have the same root cause?
- [ ] Should you add monitoring/logging to catch similar issues earlier?

### 6.4 Self-Challenge
Answer honestly:
- "Am I certain this fix addresses the root cause, not just a symptom?"
- "Have I considered all the data in the Sentry event, not just the stack trace?"
- "If this error occurs again, will my fix handle it?"

## Phase 7: Report Results

```markdown
## Fixed: [ISSUE_ID] - [Error Type]

### Issue Summary
- **Error**: [Exception message]
- **Frequency**: [X events, Y users affected]
- **First/Last Seen**: [dates]

### Root Cause
[One paragraph explaining why this happened]

### Evidence Used
- Stack trace: [key frames]
- Breadcrumbs: [relevant user actions]
- Context: [key data that informed the fix]
- Trace: [relevant span data if applicable]

### Fix Applied
- **File(s)**: [paths]
- **Change**: [description of what was changed and why]

### Verification
- [ ] Fix addresses exact error condition
- [ ] Edge cases handled
- [ ] No regressions identified
- [ ] Tests added: [yes/no, describe if yes]

### Follow-up Recommendations
- [Any additional issues to investigate]
- [Monitoring/alerting suggestions]
- [Related code that should be reviewed]
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `sentry_search_issues` | Find issues by query (status, error type, tags) |
| `sentry_get_issue` | Get issue details, stats, and latest events |
| `sentry_get_event` | Get full event data (breadcrumbs, context, tags) |
| `sentry_get_trace` | Get distributed trace for an event |
| `sentry_get_replay` | Get session replay data |
| `sentry_list_projects` | List available projects |
| `sentry_get_project` | Get project configuration |

## Common Issue Patterns

| Pattern | Investigation Focus |
|---------|---------------------|
| TypeError: Cannot read property 'x' of undefined | Check data flow, API responses, race conditions |
| Unhandled Promise Rejection | Trace async flow, check error boundaries |
| Network Error | Check breadcrumbs for request details, CORS, timeouts |
| ChunkLoadError | Check deployment, caching, code splitting |
| Rate Limit / 429 | Check trace for request patterns, add throttling |
| Memory / Performance | Check trace spans, look for N+1 queries |
