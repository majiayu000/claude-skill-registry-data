---
name: copilot-agent-coordinator
description: Automatically assigns GitHub issues to appropriate GitHub Copilot agents based on issue type, labels, and content. Triggers on "assign agent", "who should work on this", "route this issue", or after creating issues via github-mcp-orchestrator.
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__github__*
---

# GitHub Copilot Agent Coordinator

This skill intelligently assigns GitHub issues to the most appropriate GitHub Copilot agent(s) based on issue type, labels, technical domain, and dependencies.

## When to Use This Skill

**Auto-trigger** when:

- User says: "Assign agents to these issues"
- User says: "Who should work on #123?"
- User says: "Route this to the right agent"
- User says: "Match agents to issues"
- After creating issues via `github-mcp-orchestrator` skill
- When reviewing a backlog and planning work assignment

**Manual trigger**:
- When you need to determine which Copilot agent is best suited for specific work
- When coordinating work across multiple specialized agents

## Mission

Analyze GitHub issues and assign them to the most appropriate GitHub Copilot agent(s) from the available agent pool. Ensure:

1. **Right agent for the right task** - Match issue requirements to agent expertise
2. **Dependency-aware assignment** - Respect issue dependencies and execution order
3. **No conflicts** - Don't assign blocked issues; wait for dependencies
4. **Clear handoff** - Provide context and acceptance criteria to agents
5. **Actual Copilot assignment** - Use `mcp__github__assign_copilot_to_issue` to assign agents automatically

## Available Agents

The repository has 25+ specialized GitHub Copilot agents. See `reference/agent-catalog.md` for the complete list and capabilities.

### Key Agent Categories

- **Frontend specialists**: React, Tailwind UI, shadcn components, mobile responsive
- **Backend specialists**: Express API, Drizzle database, authentication
- **Quality specialists**: Testing, code review, refactoring, performance
- **Integration specialists**: Spotify API, security, realtime features
- **DevOps specialists**: CI/CD, dependency management, git workflow
- **Documentation specialists**: README, API docs, accessibility

## Assignment Strategy

### 1. Parse Issue

Extract from the issue:
- **Type**: feature, bug, chore, test, docs
- **Area**: frontend, backend, database, infra, integration
- **Labels**: All assigned labels
- **Dependencies**: Blocked by or depends on other issues
- **Complexity**: Estimate from issue description and acceptance criteria

### 2. Match to Agent

Use the matching logic in `reference/agent-matching-rules.md`:

- **Type + Area combination** → Primary agent
- **Cross-cutting concerns** → Secondary agent(s)
- **Review requirements** → Add Code Review Specialist

**Examples**:
```
Issue: "Add user notification preferences UI"
Labels: type:feature, area:frontend, estimate:m
→ Primary: React Specialist
→ Secondary: Form Handling Specialist, Tailwind UI Specialist
→ Review: Code Review Specialist

Issue: "Fix database N+1 query in dashboard"
Labels: type:bug, area:database, priority:p1
→ Primary: Database Specialist
→ Secondary: Performance Specialist
→ Review: Code Review Specialist

Issue: "Add Playwright tests for checkout flow"
Labels: type:test, area:frontend, estimate:l
→ Primary: Testing Specialist
→ Secondary: Mobile Responsive Specialist
→ Review: Code Review Specialist
```

### 3. Check Dependencies

Before assignment:

- **If blocked**: Mark as `status:blocked`, do NOT assign agent
- **If unblocked**: Assign agent with `status:ready`
- **If in dependency chain**: Note execution order in issue comment

### 4. Assign Copilot Agent

For unblocked issues:

**A. Assign via GitHub API**
Use `mcp__github__assign_copilot_to_issue` to actually assign GitHub Copilot to the issue. This triggers the agent to start work.

**B. Add Assignment Comment**
Add a comment to the issue with context:

```markdown
## 🤖 Agent Assignment

**Assigned**: GitHub Copilot
**Specialist Mode**: [Agent Name] (e.g., React Specialist, Backend API Specialist)
**Supporting Context**: @[agent-name], @[agent-name]

### Context
[Brief summary of what needs to be done]

### Key Files to Focus On
- `path/to/file.ts`
- `path/to/component.tsx`

### Acceptance Criteria
- [ ] [Criterion from issue]
- [ ] [Additional criteria]

### Dependencies
- Depends on #123 (must complete first)
- Related to #124 (can work in parallel)

### Testing Requirements
- Unit tests for new functions
- E2E tests for user flow
- Manual testing checklist in issue

**Status**: ✅ Copilot assigned and ready to start
```

**C. Update Issue Labels**
Add `status:assigned` label to track assignment.

If blocked:
```markdown
## ⏳ Agent Assignment Pending

**Status**: 🚫 Blocked

This issue depends on:
- #123 Database schema changes
- #124 API endpoint implementation

**Planned Agent**: React Specialist (will assign when unblocked)
```

## Workflow

### 1. Intake

- Receive issue number(s) or list of issues to assign
- Fetch issue details via GitHub MCP
- Parse labels, description, acceptance criteria

### 2. Agent Discovery

- Read agent catalog from `reference/agent-catalog.md`
- Apply matching rules from `reference/agent-matching-rules.md`
- Consider multi-agent scenarios

### 3. Dependency Check

- Read dependency graph from issues
- Verify dependencies are complete
- Determine if issue is ready for assignment

### 4. Assignment

For each unblocked issue:

**A. Assign Copilot via API**
```javascript
mcp__github__assign_copilot_to_issue({
  owner: "{owner}",
  repo: "{repo}",
  issueNumber: 123
})
```

**B. Add Context Comment**
```javascript
mcp__github__add_issue_comment({
  owner: "{owner}",
  repo: "{repo}",
  issue_number: 123,
  body: "## 🤖 Agent Assignment\n\n**Assigned**: GitHub Copilot\n..."
})
```

**C. Update Labels**
Use `issue_write` method to add `status:assigned` label

**D. Track assignment** in output summary

### 5. Output Summary

Generate assignment report:

```
## Agent Assignment Summary

### Assigned (Ready to Start)
- #124 → Database Specialist (no blockers)
- #126 → React Specialist + Form Handling Specialist (no blockers)

### Blocked (Waiting on Dependencies)
- #125 → Backend API Specialist (blocked by #124)
- #127 → Testing Specialist (blocked by #125, #126)

### Execution Order
1. Start #124, #126 in parallel
2. After #124 completes → start #125
3. After #125 and #126 complete → start #127

### Next Steps
1. Agents can begin work on #124 and #126 immediately
2. Monitor #124 progress; assign #125 when complete
3. Monitor #125 and #126; assign #127 when both complete
```

## Assignment Rules

### Rule 1: One Primary Agent
- Every issue gets ONE primary agent responsible for implementation
- Primary agent "owns" the issue from start to finish

### Rule 2: Optional Supporting Agents
- Complex issues may need 1-2 supporting agents for specific expertise
- Supporting agents provide guidance, not full implementation

### Rule 3: Always Include Code Review
- Every code-producing issue must be reviewed by Code Review Specialist
- Review happens after implementation, before PR merge

### Rule 4: No Assignment When Blocked
- Never assign agents to blocked issues
- Track planned assignment for when dependencies clear

### Rule 5: Consider Cross-Cutting Concerns

Issues involving:
- **Security**: Always include Security Specialist
- **Performance**: Consider Performance Specialist for data-heavy features
- **Accessibility**: Include Accessibility Specialist for UI work
- **Mobile**: Include Mobile Responsive Specialist for responsive features

## Integration with Other Skills

### After github-mcp-orchestrator

When issues are created via the orchestrator skill:

1. Orchestrator creates epic + children
2. This skill (coordinator) automatically assigns agents
3. Output includes both issue map AND agent assignments

### Before copilot-workflow-orchestrator

When complex multi-agent workflows are needed:

1. This skill assigns agents to individual issues
2. Workflow orchestrator manages sequencing and handoffs
3. Progress tracker monitors execution

## Reference Documentation

- **Agent catalog**: See `reference/agent-catalog.md`
- **Matching rules**: See `reference/agent-matching-rules.md`
- **Assignment templates**: See `templates/assignment-comment.md`

## What This Skill Does

- Analyzes issues for technical domain and complexity
- Matches issues to best-fit Copilot agents
- Checks dependencies before assignment
- Creates agent assignment comments on issues
- Tracks assignment status across multiple issues
- Provides execution order recommendations

## What This Skill Doesn't Do

- Doesn't write code (agents do that)
- Doesn't manage agent execution (that's orchestrator)
- Doesn't review code (Code Review agent does that)
- Doesn't create issues (github-mcp-orchestrator does that)
