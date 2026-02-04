---
name: copilot-workflow-orchestrator
description: Orchestrates complex multi-agent workflows for features requiring coordinated work across multiple GitHub Copilot agents. Triggers on "orchestrate workflow", "coordinate these agents", "manage agent execution", or when dealing with complex features spanning multiple domains.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__github__*
---

# GitHub Copilot Workflow Orchestrator

This skill manages complex workflows involving multiple GitHub Copilot agents working on related issues. It handles sequencing, handoffs, dependency resolution, and progress tracking for coordinated multi-agent development.

## When to Use This Skill

**Auto-trigger** when:

- User says: "Orchestrate this workflow"
- User says: "Coordinate these agents"
- User says: "Manage multi-agent execution"
- User says: "Run these issues in sequence"
- After assigning agents to a complex epic with dependencies
- When a feature requires 3+ agents working in sequence

**Manual trigger**:
- Complex features with clear phases (backend → frontend → testing)
- Coordinated refactoring across multiple files/domains
- Large epics with dependency chains

## Mission

Coordinate multiple GitHub Copilot agents to work together on complex features:

1. **Define workflow phases** - Break work into sequential or parallel phases
2. **Manage handoffs** - Ensure smooth transitions between agents
3. **Monitor progress** - Track which agents have completed their work
4. **Unblock dependencies** - Automatically assign next agent when dependencies clear
5. **Ensure quality** - Coordinate reviews and testing throughout workflow

## Core Concepts

### Workflow
A coordinated sequence of work items (issues) with dependencies, assigned to appropriate agents.

### Phase
A logical grouping of work that can happen in parallel. Phases execute sequentially.

### Handoff
The transition point when one agent completes work and the next agent can start.

### Checkpoint
A verification point where progress is validated before proceeding to next phase.

## Workflow Types

See `workflows/` directory for pre-defined workflow templates:

### 1. Full-Stack Feature Workflow
```
Phase 1: Backend Foundation
  └─ Database Specialist → Schema changes

Phase 2: API Implementation
  └─ Backend API Specialist → Endpoints (depends on Phase 1)

Phase 3: Frontend Implementation
  ├─ React Specialist → Components (depends on Phase 2)
  └─ Tailwind UI Specialist → Styling (depends on Phase 2)

Phase 4: Integration & Testing
  ├─ State Management Specialist → Wire up data flow
  └─ Testing Specialist → E2E tests

Phase 5: Review & Polish
  ├─ Code Review Specialist → Review all changes
  ├─ Performance Specialist → Check performance
  └─ Security Specialist → Security review
```

### 2. Refactoring Workflow
```
Phase 1: Preparation
  └─ Testing Specialist → Add tests for existing behavior

Phase 2: Refactoring
  └─ Refactoring Specialist → Restructure code

Phase 3: Verification
  ├─ TypeScript Specialist → Fix type issues
  └─ Testing Specialist → Verify tests still pass

Phase 4: Review
  └─ Code Review Specialist → Ensure no behavior changes
```

### 3. Integration Workflow
```
Phase 1: Authentication
  ├─ Authentication Specialist → OAuth flow
  └─ Security Specialist → Token security

Phase 2: API Integration
  └─ [Service] API Specialist → API calls

Phase 3: Frontend
  ├─ React Specialist → UI components
  └─ State Management Specialist → Data flow

Phase 4: Testing
  └─ Testing Specialist → Integration tests
```

## Workflow Management

### 1. Workflow Creation

When creating a workflow:

```typescript
{
  id: "workflow-123",
  epic: "#150",
  name: "Spotify Playlist Integration",
  phases: [
    {
      name: "Authentication",
      issues: ["#151"],
      agents: ["Third-Party-API-Specialist", "Authentication-Specialist"],
      dependencies: [],
      checkpoint: "OAuth flow working, tokens stored"
    },
    {
      name: "API Implementation",
      issues: ["#152", "#153"],
      agents: ["Third-Party-API-Specialist", "Backend-API-Specialist"],
      dependencies: ["Phase 1"],
      checkpoint: "API endpoints return playlist data"
    },
    // ... more phases
  ],
  status: "in_progress",
  currentPhase: 1
}
```

### 2. Phase Execution

For each phase:

1. **Check dependencies** - Ensure previous phases complete via GitHub MCP
2. **Assign agents** - Use `mcp__github__assign_copilot_to_issue` for each issue
3. **Monitor progress** - Real-time PR monitoring via `mcp__github__pull_request_read`
   - Track PR creation (agents open PRs)
   - Monitor CI/CD checks status
   - Watch review comments
   - Detect when PR is merged
4. **Validate checkpoint** - Verify phase goals met
   - All issues closed
   - All PRs merged
   - Tests passing
   - Checkpoint criteria satisfied
5. **Proceed to next** - Trigger next phase automatically when ready

### 3. Handoff Management

When transitioning between phases:

```markdown
## Phase Handoff: Authentication → API Implementation

**Previous Phase**: Authentication ✅ Completed
- #151 merged in PR #200
- OAuth flow working
- Tokens stored securely

**Next Phase**: API Implementation 🚀 Starting
- Agents: @Third-Party-API-Specialist, @Backend-API-Specialist
- Issues: #152, #153
- Context: Use OAuth tokens from Phase 1 to make Spotify API calls

**Handoff Notes**:
- Token storage methods available in `server/storage.ts:456`
- OAuth callback route is `/api/spotify/callback`
- Access tokens expire after 1 hour, use refresh logic

**Checkpoint**: API endpoints should return playlist data successfully
```

### 4. Progress Tracking

Track workflow status:

```
Workflow: Spotify Playlist Integration (#150)
Status: Phase 2 of 4 (50% complete)

✅ Phase 1: Authentication (Completed 2 hours ago)
   - #151: Spotify OAuth flow → Merged in PR #200

🚀 Phase 2: API Implementation (In Progress)
   - #152: Playlist search API → PR #201 (in review)
   - #153: Track metadata API → Assigned, not started

⏳ Phase 3: Frontend (Blocked - waiting on Phase 2)
   - #154: Playlist browser UI
   - #155: Playback controls

⏳ Phase 4: Testing (Blocked - waiting on Phase 3)
   - #156: E2E tests for playlist flow
```

## Workflow Monitoring (Real-Time via GitHub MCP)

### Automatic Progress Detection

**Using GitHub MCP tools** to monitor in real-time:

- **PR creation** - Use `mcp__github__search_pull_requests` to find new PRs
- **PR status** - Use `mcp__github__pull_request_read` with `method: "get"`
- **CI/CD checks** - Use `mcp__github__pull_request_read` with `method: "get_status"`
- **Review status** - Use `mcp__github__pull_request_read` with `method: "get_reviews"`
- **PR merge** - Detect when `pr.merged === true`
- **Issue status** - Use `mcp__github__issue_read` to check if closed

### Monitoring Loop

```javascript
// Poll every 5 minutes
while (!phaseComplete) {
  for (const issueNum of phaseIssues) {
    const issue = await mcp__github__issue_read({
      method: "get",
      owner: "{owner}",
      repo: "{repo}",
      issue_number: issueNum
    })

    // Check if issue has linked PR
    if (issue.pull_request) {
      const pr = await mcp__github__pull_request_read({
        method: "get",
        owner: "{owner}",
        repo: "{repo}",
        pullNumber: issue.pull_request.number
      })

      // Track progress
      if (pr.merged) {
        markIssueComplete(issueNum)
      }
    }
  }

  await sleep(300000) // 5 minutes
}
```

### Checkpoint Validation

Before moving to next phase, validate via GitHub MCP:

1. **All issues closed** - Use `mcp__github__issue_read` to verify `state === "closed"`
2. **All PRs merged** - Check `pr.merged === true` for each PR
3. **Tests passing** - Use `pull_request_read` with `method: "get_status"`
   - Verify all checks have `conclusion: "success"`
4. **No blocking issues** - Search for P0/P1 bugs created during phase
5. **Checkpoint criteria met** - Custom validation per workflow

### Progress Notifications

Update epic issue with progress:

```markdown
## Workflow Progress

**Last Updated**: 2025-01-15 14:30 UTC

### Phase 1: Authentication ✅
- #151 Completed (PR #200)

### Phase 2: API Implementation 🚀 IN PROGRESS
- #152 In Review (PR #201)
- #153 Not Started

### Phase 3: Frontend ⏳ BLOCKED
Waiting on #152, #153

### Phase 4: Testing ⏳ BLOCKED
Waiting on #154, #155

**Overall Progress**: 25% (1/4 phases complete)
**Estimated Completion**: 3-4 days remaining
```

## Conflict Resolution

### Agent Conflicts

When two agents need to modify the same file:

1. **Sequential assignment** - Assign agents in order
2. **Clear boundaries** - Define which agent owns which sections
3. **Communication** - Add notes about shared files in assignments

### Merge Conflicts

When PRs conflict:

1. **Detect conflict** - Monitor PR status
2. **Coordinate resolution** - Assign to agent who opened later PR
3. **Re-review** - Code Review Specialist reviews conflict resolution

### Blocking Issues

When new bugs block workflow:

1. **Create blocking issue** - File as P0/P1
2. **Pause workflow** - Mark current phase as blocked
3. **Assign fix** - Route to appropriate agent
4. **Resume** - Continue workflow when fixed

## Workflow Templates

Pre-defined workflows in `workflows/` directory:

- `full-stack-feature.md` - Complete backend + frontend feature
- `api-integration.md` - Third-party API integration
- `refactoring.md` - Safe code refactoring workflow
- `performance-optimization.md` - Performance improvement workflow
- `security-hardening.md` - Security improvement workflow
- `testing-pyramid.md` - Comprehensive test coverage workflow

## Integration with Other Skills

### After github-mcp-orchestrator + copilot-agent-coordinator

Typical flow:

1. **Orchestrator** creates epic + child issues
2. **Coordinator** assigns agents to issues
3. **Workflow Orchestrator** (this skill) manages execution sequencing
4. **PR Reviewer** reviews completed work

### Workflow Lifecycle

```
Issue Creation → Agent Assignment → Workflow Orchestration → PR Review → Merge
     ↑                ↑                      ↑                   ↑          ↑
     |                |                      |                   |          |
MCP Orchestrator  Agent Coordinator   Workflow Orchestrator  PR Reviewer  Done
```

## Reference Documentation

- **Workflow templates**: See `workflows/` directory
- **Handoff patterns**: See `reference/handoff-patterns.md`
- **Monitoring guide**: See `reference/monitoring.md`

## What This Skill Does

- Creates and manages multi-phase workflows
- Coordinates agent handoffs between phases
- Monitors workflow progress
- Validates phase checkpoints
- Updates epic with progress
- Detects and resolves blockers
- Ensures quality gates are met

## What This Skill Doesn't Do

- Doesn't write code (agents do that)
- Doesn't review code (Code Review agent does that)
- Doesn't create issues (github-mcp-orchestrator does that)
- Doesn't assign individual agents (copilot-agent-coordinator does that)
- Doesn't execute CI/CD (GitHub Actions does that)

## Output Format

### Workflow Status Report

```
# Workflow Status: [Workflow Name]

**Epic**: #[NUM]
**Started**: [Date]
**Current Phase**: [N of M]
**Overall Status**: [On Track | At Risk | Blocked]

## Phase Summary

### ✅ Completed Phases
- Phase 1: [Name] (Completed [date])
  - Issues: #X, #Y
  - PRs: #A, #B

### 🚀 Active Phase
- Phase 2: [Name] (In Progress)
  - Issues: #C (in review), #D (assigned)
  - Blockers: None
  - Checkpoint: [Criteria]

### ⏳ Upcoming Phases
- Phase 3: [Name] (Blocked by Phase 2)
- Phase 4: [Name] (Blocked by Phase 3)

## Next Actions
1. [Action 1]
2. [Action 2]

## Risks
- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

**Estimated Completion**: [Date / Days remaining]
```
