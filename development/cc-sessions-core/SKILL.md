---
name: cc-sessions-core
description: Provide comprehensive guidance for developing and maintaining the cc-sessions framework core functionality - primary skill for hooks, sessions, tasks, middleware, route handlers, and API endpoints
schema_version: 1.0
---

# cc-sessions-core

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** High

## Trigger Reference

This skill activates on:
- Keywords: "hook", "session", "task", "middleware", "route handler", "api endpoint", "cc-sessions"
- Intent patterns: "(create|modify|refactor).*?(hook|session|task)", "sessions.*?development", "api.*?(implementation|development)"
- File patterns: `sessions/**/*.js`, `sessions/hooks/**/*.js`, `sessions/api/**/*.js`

From: `skill-rules.json` - cc-sessions-core configuration

## Purpose

Provide comprehensive guidance for developing and maintaining the cc-sessions framework core functionality. This is the primary skill for all cc-sessions development work including hooks, sessions, tasks, middleware, route handlers, and API endpoints.

## Core Behavior

When activated in IMPLEMENT mode with an active cc-sessions task:

1. **Framework Core Development**
   - Guide implementation of new cc-sessions features
   - Ensure DAIC discipline enforcement
   - Maintain write-gating integrity
   - Implement state persistence mechanisms
   - Handle session lifecycle management

2. **Hook Development**
   - Create/modify hooks in `sessions/hooks/`
   - Ensure hooks respect DAIC modes
   - Implement proper error handling and logging
   - Validate hook execution order and dependencies
   - Test hook integration with enforcement layer

3. **API Endpoint Development**
   - Create/modify routes in `sessions/api/`
   - Follow RESTful conventions where applicable
   - Implement proper request validation
   - Ensure consistent error responses
   - Document API contracts

4. **Task Management Features**
   - Implement task creation, startup, and completion workflows
   - Handle task state transitions
   - Manage task manifests and context
   - Implement todo tracking and progression
   - Support task resumption and recovery

5. **Middleware & Route Handlers**
   - Create Express-compatible middleware
   - Implement route handlers with proper error handling
   - Ensure consistent request/response patterns
   - Apply security best practices (input validation, sanitization)

## Safety Guardrails

**CRITICAL WRITE-GATING RULES:**
- ✓ Only execute write operations when in IMPLEMENT mode
- ✓ Verify active cc-sessions task exists before writing
- ✓ Follow approved manifest/todos from task file
- ✓ Never weaken DAIC discipline or write-gating logic
- ✓ Never bypass framework safety mechanisms

**Framework Integrity Rules:**
- Never allow writes outside IMPLEMENT mode (core framework requirement)
- Never modify `CC_SESSION_MODE` or `CC_SESSION_TASK_ID` directly (only cc-sessions API may do this)
- Preserve SoT tier boundaries (Tier-1 canonical, Tier-2 task-scoped, Tier-3 ephemeral)
- Maintain backward compatibility when modifying core APIs
- Document breaking changes in `context/gotchas.md`

**Code Quality Standards:**
- Follow existing code style and patterns
- Add JSDoc comments for public APIs
- Include error handling for all async operations
- Validate inputs at API boundaries
- Write tests for new functionality (when test infrastructure exists)

## Examples

### When to Activate

✓ "Create a new hook for validating task manifests"
✓ "Modify the session state API to include timestamps"
✓ "Add a new command: sessions tasks archive"
✓ "Fix the write-gating enforcement in sessions_enforce.js"
✓ "Implement task resumption from state.json"

### When NOT to Activate

✗ In DISCUSS/ALIGN/CHECK mode (framework development requires IMPLEMENT)
✗ No active cc-sessions task (violates write-gating)
✗ User is working on application code (not framework code)
✗ Changes would weaken safety mechanisms

## Framework Architecture Awareness

### Key Files & Responsibilities

**Core:**
- `sessions/bin/sessions` - CLI entry point
- `sessions/api/router.js` - Main API router
- `sessions/sessions-state.json` - Session state persistence

**Hooks:**
- `sessions/hooks/sessions_enforce.js` - Write-gating and DAIC enforcement
- Hook execution: UserPromptSubmit, SessionStart, PreToolUse, PostToolUse

**API Modules:**
- `sessions/api/state_commands.js` - State management (show, mode, task, todos, flags, update)
- `sessions/api/task_commands.js` - Task operations (idx, start)
- `sessions/api/config_commands.js` - Configuration management
- `sessions/api/protocol_commands.js` - Protocol execution

### DAIC Flow
1. **DISCUSS** → Clarify, gather context, no writes
2. **ALIGN** → Design plan, create manifest, no writes
3. **IMPLEMENT** → Execute approved todos, writes allowed
4. **CHECK** → Verify, test, summarize, minimal writes

### State Management
- Session state tracked in `sessions/sessions-state.json`
- Task state tracked in `sessions/sessions-state.json` (lightweight checkpoint)
- Hooks enforce state consistency
- State transitions logged for debugging

## Decision Logging

When modifying core framework behavior, log in `context/decisions.md`:

```markdown
### Framework Change: [Date]
- **Component:** sessions/hooks/sessions_enforce.js
- **Change:** Added todo list change detection
- **Rationale:** Users were bypassing execution boundary by silently changing todos
- **Impact:** All todo modifications now require explicit approval
- **Breaking:** No (additive change only)
```

## Related Skills

- **cc-sessions-hooks** - Specialized hook development (defers to this when hooks are involved)
- **cc-sessions-api** - Specialized API development (defers to this when API commands are involved)
- **skill-developer** - For creating skills that integrate with cc-sessions
- **framework_health_check** - To validate framework health after changes
- **framework_repair_suggester** - If framework issues arise during development

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
