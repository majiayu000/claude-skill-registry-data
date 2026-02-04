---
name: cc-sessions-hooks
description: Specialized guidance for creating, modifying, and debugging cc-sessions hooks that enforce DAIC discipline, write-gating, and framework integrity
schema_version: 1.0
---

# cc-sessions-hooks

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** High

## Trigger Reference

This skill activates on:
- Keywords: "hook", "sessions_enforce", "post_tool_use", "user_messages", "subagent_hooks", "shared_state"
- Intent patterns: "(create|modify|fix).*?hook", "hook.*?(enforcement|validation)"
- File patterns: `sessions/hooks/**/*.js`

From: `skill-rules.json` - cc-sessions-hooks configuration

## Purpose

Specialized guidance for creating, modifying, and debugging cc-sessions hooks. Hooks are the enforcement layer that ensures DAIC discipline, write-gating, and framework integrity.

## Core Behavior

When activated in IMPLEMENT mode with an active cc-sessions task:

1. **Hook Types & Purposes**

   **UserPromptSubmit Hook:**
   - Fires when user submits a prompt
   - Use for: Mode transition triggers, startup protocols, context warnings
   - Access: User message content, current session state

   **PreToolUse Hook:**
   - Fires BEFORE any tool executes
   - Use for: Write-gating enforcement, permission checks, guardrails
   - Access: Tool name, parameters, current mode, task state
   - Can: Block tool execution, modify parameters, inject warnings

   **PostToolUse Hook:**
   - Fires AFTER tool completes
   - Use for: State updates, logging, cleanup, validation
   - Access: Tool name, parameters, result, errors

   **SessionStart Hook:**
   - Fires when Claude Code session begins
   - Use for: Initialization, state loading, environment checks
   - Access: Session configuration, environment variables

2. **Hook Development Patterns**

   **Basic Hook Structure:**
   ```javascript
   // sessions/hooks/example_hook.js
   module.exports = {
     name: 'example_hook',
     description: 'Brief description of what this hook does',

     async execute(context) {
       // Hook logic here
       // Return { success: true } or { success: false, error: 'message' }
     }
   };
   ```

   **Enforcement Hook Pattern:**
   ```javascript
   async execute(context) {
     const { toolName, toolParams, sessionState } = context;

     // Check conditions
     if (shouldBlock(toolName, sessionState)) {
       return {
         success: false,
         error: 'Tool blocked: [reason]',
         additionalContext: '[guidance for user]'
       };
     }

     return { success: true };
   }
   ```

3. **Write-Gating Enforcement**

   The `sessions_enforce.js` hook is CRITICAL for framework integrity:

   **What it enforces:**
   - Write tools (Edit, Write, MultiEdit) only in IMPLEMENT mode
   - Only cc-sessions may modify CC_SESSION_MODE / CC_SESSION_TASK_ID
   - Todo list changes require user approval
   - No writes when no active task exists

   **How to extend:**
   - Add new tool checks to `WRITE_TOOLS` array
   - Add new state validations to `checkWriteGating()`
   - Log enforcement decisions for debugging
   - Never weaken existing checks

4. **Shared State Access**

   Hooks can read/modify shared state:

   ```javascript
   const state = require('../sessions-state.json');
   const fs = require('fs');

   // Read state
   const currentMode = state.mode;
   const activeTask = state.task;

   // Modify state (carefully!)
   state.flags.contextWarning85 = true;
   fs.writeFileSync(
     path.join(__dirname, '../sessions-state.json'),
     JSON.stringify(state, null, 2)
   );
   ```

5. **Hook Execution Order**

   Understand execution flow:
   1. UserPromptSubmit (user input processed)
   2. PreToolUse (before each tool call)
   3. Tool executes
   4. PostToolUse (after each tool call)

   Hooks execute synchronously within their phase.

## Safety Guardrails

**CRITICAL WRITE-GATING RULES:**
- ✓ Only execute write operations when in IMPLEMENT mode
- ✓ Verify active cc-sessions task exists before writing hooks
- ✓ Follow approved manifest/todos from task file
- ✓ NEVER weaken write-gating logic
- ✓ NEVER allow hooks to bypass DAIC discipline

**Hook-Specific Safety:**
- Test hooks thoroughly before deployment (they can break the entire framework)
- Always return `{ success: true/false }` from execute()
- Include clear error messages when blocking actions
- Log hook decisions for debugging
- Never create infinite loops (hook triggering hook)
- Handle async operations properly (await all promises)
- Validate all inputs (context might be malformed)

**State Mutation Safety:**
- Only modify state when necessary
- Always validate state structure before writing
- Use atomic writes (read-modify-write pattern)
- Log state changes for auditability
- Never corrupt state (keep backups during development)

## Examples

### When to Activate

✓ "Add a hook to validate task manifest format"
✓ "Fix the sessions_enforce.js write-gating for MultiEdit tool"
✓ "Create a PostToolUse hook to log all file modifications"
✓ "Modify UserPromptSubmit to detect '/squish' command"
✓ "Debug why the IMPLEMENT mode transition isn't triggering"

### When NOT to Activate

✗ In DISCUSS/ALIGN/CHECK mode (hook development requires IMPLEMENT)
✗ No active cc-sessions task (violates write-gating)
✗ User wants to create non-hook cc-sessions code (use cc-sessions-core)
✗ Changes would weaken enforcement mechanisms

## Hook Testing Checklist

Before deploying a new or modified hook:

- [ ] Hook returns proper `{ success, error? }` structure
- [ ] Error messages are clear and actionable
- [ ] Hook doesn't block legitimate operations
- [ ] Hook doesn't create infinite loops
- [ ] Async operations are properly awaited
- [ ] State modifications are atomic and validated
- [ ] Hook behavior logged for debugging
- [ ] Tested in all DAIC modes
- [ ] Doesn't introduce performance issues
- [ ] Documented in hook file comments

## Common Hook Patterns

### 1. Blocking Pattern
```javascript
if (invalidCondition) {
  return {
    success: false,
    error: '[CATEGORY: Clear Error Message]',
    additionalContext: 'What user should do instead'
  };
}
```

### 2. Warning Pattern
```javascript
if (warningCondition) {
  console.warn('[Hook Warning]', message);
  // Continue execution
}
return { success: true };
```

### 3. State Update Pattern
```javascript
const state = loadState();
state.flags.someFlag = true;
saveState(state);
return { success: true };
```

### 4. Conditional Execution
```javascript
if (context.toolName === 'Write' && context.sessionState.mode !== 'IMPLEMENT') {
  return { success: false, error: 'Write only in IMPLEMENT mode' };
}
```

## Decision Logging

When creating or modifying hooks, log in `context/decisions.md`:

```markdown
### Hook Change: [Date]
- **Hook:** sessions/hooks/sessions_enforce.js
- **Change:** Added MultiEdit to WRITE_TOOLS array
- **Rationale:** MultiEdit can write to multiple files, needs same gating as Write/Edit
- **Testing:** Verified blocks in DISCUSS, allows in IMPLEMENT
- **Risk:** Low (additive change, follows existing pattern)
```

## Related Skills

- **cc-sessions-core** - For broader framework development beyond hooks
- **framework_health_check** - To validate hook behavior after changes
- **framework_repair_suggester** - If hooks malfunction or cause framework issues
- **daic_mode_guidance** - For understanding mode transitions that hooks enforce

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
