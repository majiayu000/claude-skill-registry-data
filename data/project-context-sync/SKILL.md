---
name: project-context-sync
description: |
  Maintains synchronized project context for long-running work across sessions.
  Use when: starting a session (read context), completing significant work (update context),
  making architectural decisions (document rationale), or before stopping work (ensure clean handoff).
  Triggers on: "continue working", "what's next", "resume", "pick up where", "context", "progress",
  "document", "handoff", "session", "PROGRESS.md", "plan feature", "feature list"
---

# Project Context Synchronization

This skill ensures Claude maintains accurate project state across sessions, following patterns from Anthropic's long-running agent research.

## Core Philosophy

Each session should:
1. **Start informed**: Read existing context before diving in
2. **Work incrementally**: One feature at a time, commit often
3. **End verified**: Run verification commands before marking work complete
4. **End clean**: Leave documentation that your future self (next session) can understand

## Context Files

### .claude/PROGRESS.md

This is the **semantic bridge** between sessions. It answers: "What was I doing? What's next?"

Required sections:
- **Current State**: What's working, what's broken
- **Recent Work**: Last 3-5 significant changes with rationale
- **Next Steps**: Prioritized list of what to work on
- **Blockers** (optional): Known issues or decisions needed
- **Architecture Decisions** (optional): Why significant choices were made

### .claude/feature_list.json (For Multi-Session Features)

When working on features that span multiple sessions, use this structured format:

```json
{
  "feature": "User Authentication",
  "description": "Add JWT-based authentication with login/logout",
  "created": "2025-01-15T10:00:00Z",
  "status": "in-progress",
  "estimatedSessions": 4,
  "completedSessions": 1,
  "items": [
    {
      "id": "item-001",
      "description": "Create JWT token generation utility",
      "status": "complete",
      "acceptanceCriteria": [
        "Generates valid JWT tokens",
        "Tokens include user ID and expiration"
      ],
      "verification": [
        {
          "command": "npm test -- --grep 'JWT'",
          "description": "JWT tests pass"
        }
      ],
      "completedAt": "2025-01-15T14:30:00Z",
      "sessionId": "abc123"
    },
    {
      "id": "item-002",
      "description": "Create login API endpoint",
      "status": "in-progress",
      "acceptanceCriteria": [
        "POST /api/login accepts email/password",
        "Returns JWT token on success",
        "Returns 401 on failure"
      ],
      "verification": [
        {
          "command": "npm test -- auth.test.ts",
          "description": "Auth tests pass"
        },
        {
          "command": "curl -X POST http://localhost:3000/api/login -d '{}'",
          "description": "Login endpoint responds",
          "expectedOutput": "401"
        }
      ],
      "dependencies": ["item-001"]
    }
  ],
  "metadata": {
    "complexity": "medium",
    "riskFactors": ["Breaking API changes"],
    "relatedFiles": ["src/auth/", "src/middleware/"]
  }
}
```

**Key Benefits:**
- Session-sized work items with clear boundaries
- Verification commands run automatically before session end
- Smoke tests on session start verify previous work still passes
- Progress tracking across sessions

### .claude/context-sync.json (Optional)

Plugin configuration:

```json
{
  "enabled": true,
  "requireProgressFile": false,
  "gitHistoryLines": 10,
  "showFullProgress": true,
  "quietStart": false,
  "runSmokeTests": true,
  "smokeTestTimeout": 30,
  "verificationTimeout": 60,
  "autoUpdateFeatureList": true,
  "requireVerificationPass": true
}
```

## Session Workflow

### On Session Start

The plugin automatically:
1. Injects PROGRESS.md content
2. Shows active feature progress (if feature_list.json exists)
3. Runs smoke tests on last completed work item
4. Displays next work item with acceptance criteria

You should:
1. **Review context**: Check for regression warnings
2. **Confirm next task**: Usually the suggested work item
3. **Mark item in-progress**: Update feature_list.json if needed

### During Work

- **Commit incrementally**: After each logical unit of work
- **Use descriptive messages**: Future sessions read these
- **Test continuously**: Don't wait until the end
- **Update PROGRESS.md**: After completing significant milestones

### Before Stopping

The Stop hook will:
1. Run verification commands for current work item
2. If verification passes, mark item complete
3. Validate PROGRESS.md structure
4. Check for uncommitted changes

If verification fails, you'll be prompted to fix issues.

## Commands

- `/sync-context` - Force synchronize context (read + update)
- `/whats-next` - Show prioritized next actions
- `/plan-feature <description>` - Create feature_list.json with work items

## Planning Multi-Session Features

Use `/plan-feature` for complex work:

```
/plan-feature Add user authentication with JWT tokens
```

This triggers the planning workflow:
1. **Discovery**: Explore codebase for relevant code
2. **Architecture**: Design the approach, identify risks
3. **Work Items**: Break into session-sized pieces
4. **Verification**: Define commands to prove completion

The result is a `feature_list.json` that guides subsequent sessions.

### Good Work Item Sizing

**Too Large:**
- "Implement authentication" (vague, multiple sessions)
- "Refactor the entire auth module" (unclear scope)

**Good:**
- "Create JWT token generation utility"
- "Add password hashing to user model"
- "Create login API endpoint with validation"
- "Add auth middleware to protected routes"

### Good Verification Commands

```json
{
  "verification": [
    {
      "command": "npm test -- auth.test.ts",
      "description": "Auth tests pass"
    },
    {
      "command": "npm run typecheck",
      "description": "No TypeScript errors"
    },
    {
      "command": "npm run lint",
      "description": "No lint errors"
    }
  ]
}
```

## Best Practices

### Commit Messages
Write for your future self:
- Bad: "fix bug"
- Good: "Fix auth token refresh failing after 24h - was comparing timestamps in wrong timezone"

### Progress Updates
Be specific:
- Bad: "Worked on auth"
- Good: "Implemented password reset flow. Email sending works, but reset link expiration not yet tested."

### Incremental Work
From Anthropic's research: "Ask the model to work on only one feature at a time."

If a task is too large for one session:
1. Use `/plan-feature` to create work items
2. Each session completes one work item
3. Verification ensures clean handoffs

## Integration with Git

This skill complements git, not replaces it:
- **Git**: What changed (code)
- **PROGRESS.md**: Why it changed, what's next (intent)
- **feature_list.json**: Structured progress tracking (state machine)

Together they form a complete picture for the next session.

## Workflow Example

**Session 1: Planning**
```
> /plan-feature Add user notifications
```
Creates feature_list.json with 5 work items.

**Session 2: Item 1**
- Start: See "item-001: Create notification model"
- Work: Implement model, write tests
- End: Verification runs → Tests pass → Item marked complete

**Session 3: Item 2**
- Start: Smoke test on item-001 passes ✅
- See "item-002: Create notification service"
- Work: Implement service
- End: Verification runs → All tests pass

**Session N: Complete**
- All items complete
- Feature status → "complete"
- PROGRESS.md updated with summary
