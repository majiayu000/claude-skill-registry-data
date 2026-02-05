---
name: cc-sessions-api
description: Specialized guidance for developing cc-sessions API commands and subsystems for state management, task operations, configuration, and protocol execution
schema_version: 1.0
---

# cc-sessions-api

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** High

## Trigger Reference

This skill activates on:
- Keywords: "session command", "task command", "state command", "protocol command", "config command"
- Intent patterns: "(create|modify|fix).*?(command|api)", "sessions.*?api"
- File patterns: `sessions/api/**/*.js`

From: `skill-rules.json` - cc-sessions-api configuration

## Purpose

Specialized guidance for developing cc-sessions API commands and subsystems. The API provides CLI commands for state management, task operations, configuration, and protocol execution.

## Core Behavior

When activated in IMPLEMENT mode with an active cc-sessions task:

1. **API Architecture**

   **Entry Point:** `sessions/bin/sessions` (CLI binary)
   **Router:** `sessions/api/router.js` (command dispatch)
   **Subsystems:**
   - `state_commands.js` - State management
   - `task_commands.js` - Task operations
   - `config_commands.js` - Configuration
   - `protocol_commands.js` - Protocol execution

2. **Command Subsystems**

   **State Commands** (`state_commands.js`)
   ```bash
   sessions state show          # Display current session state
   sessions state mode [value]  # Get/set DAIC mode
   sessions state task [value]  # Get/set active task
   sessions state todos         # Manage todo list
   sessions state flags         # View/modify session flags
   sessions state update        # Update state values
   ```

   **Task Commands** (`task_commands.js`)
   ```bash
   sessions tasks idx list              # List task indexes
   sessions tasks idx <index-name>      # View tasks in index
   sessions tasks start <task-file>     # Start a task
   ```

   **Config Commands** (`config_commands.js`)
   ```bash
   sessions config show         # Display all configuration
   sessions config phrases      # View startup phrases
   sessions config git          # Git integration settings
   sessions config env          # Environment variables
   sessions config features     # Feature flags
   sessions config read <key>   # Read specific config value
   sessions config write        # Write config values
   sessions config tools        # Tool configurations
   ```

   **Protocol Commands** (`protocol_commands.js`)
   ```bash
   sessions protocol startup-load       # Startup initialization
   ```

3. **Command Development Pattern**

   **Basic Command Structure:**
   ```javascript
   // sessions/api/example_commands.js
   module.exports = {
     name: 'example',
     description: 'Example command subsystem',

     async execute(args) {
       const [subcommand, ...rest] = args;

       switch (subcommand) {
         case 'action1':
           return this.handleAction1(rest);
         case 'action2':
           return this.handleAction2(rest);
         default:
           return this.showHelp();
       }
     },

     async handleAction1(args) {
       // Implementation
       return { success: true, message: 'Action completed' };
     },

     showHelp() {
       return {
         success: true,
         message: `
Usage: sessions example <action>

Actions:
  action1  - Description of action1
  action2  - Description of action2
         `.trim()
       };
     }
   };
   ```

4. **State Management Patterns**

   **Reading State:**
   ```javascript
   const fs = require('fs');
   const path = require('path');

   const statePath = path.join(__dirname, '../sessions-state.json');
   const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));

   console.log('Current mode:', state.mode);
   console.log('Active task:', state.task.name);
   ```

   **Writing State:**
   ```javascript
   // Read-modify-write pattern
   const state = loadState();
   state.mode = 'IMPLEMENT';
   state.task.status = 'in_progress';
   saveState(state);
   ```

   **Validation:**
   ```javascript
   function validateMode(mode) {
     const validModes = ['DISCUSS', 'ALIGN', 'IMPLEMENT', 'CHECK'];
     if (!validModes.includes(mode)) {
       throw new Error(`Invalid mode: ${mode}. Must be one of: ${validModes.join(', ')}`);
     }
   }
   ```

5. **Error Handling**

   **Consistent Error Format:**
   ```javascript
   if (errorCondition) {
     return {
       success: false,
       error: 'Clear, actionable error message',
       hint: 'Optional suggestion for user'
     };
   }
   ```

   **Input Validation:**
   ```javascript
   async execute(args) {
     if (args.length === 0) {
       return {
         success: false,
         error: 'Missing required argument: <action>',
         hint: 'Use "sessions example help" for usage'
       };
     }
     // ...
   }
   ```

6. **Output Formatting**

   **Success Messages:**
   ```javascript
   return {
     success: true,
     message: '✓ Task started successfully',
     data: { taskName, branch }
   };
   ```

   **Informational Output:**
   ```javascript
   console.log('=== Session State ===');
   console.log(`Mode: ${state.mode}`);
   console.log(`Task: ${state.task.name}`);
   ```

## Safety Guardrails

**CRITICAL WRITE-GATING RULES:**
- ✓ Only execute write operations when in IMPLEMENT mode
- ✓ Verify active cc-sessions task exists before writing
- ✓ Follow approved manifest/todos from task file
- ✓ Never allow commands to bypass DAIC discipline
- ✓ Never allow direct modification of protected state (CC_SESSION_MODE, CC_SESSION_TASK_ID)

**API-Specific Safety:**
- Validate all user inputs before processing
- Never expose internal state structure directly
- Sanitize file paths to prevent directory traversal
- Use atomic read-modify-write for state changes
- Return consistent error formats
- Log command execution for debugging
- Never execute arbitrary code from user input

**State Integrity:**
- Always validate state structure before writing
- Preserve state schema compatibility
- Handle missing or corrupted state gracefully
- Provide clear error messages for invalid state
- Log state changes for auditability

## Examples

### When to Activate

✓ "Add a new command: sessions tasks archive"
✓ "Modify state show to include task branch"
✓ "Fix the task idx command to handle missing indexes"
✓ "Create a new subsystem for managing LCMP files"
✓ "Add validation to the state mode command"

### When NOT to Activate

✗ In DISCUSS/ALIGN/CHECK mode (API development requires IMPLEMENT)
✗ No active cc-sessions task (violates write-gating)
✗ User wants to work on hooks (use cc-sessions-hooks)
✗ User wants general framework features (use cc-sessions-core)

## Command Development Checklist

Before deploying a new or modified command:

- [ ] Command follows naming conventions (subsystem + action)
- [ ] Help text is clear and includes examples
- [ ] All inputs are validated
- [ ] Error messages are actionable
- [ ] State changes are atomic
- [ ] Command works with missing/invalid state
- [ ] Output format is consistent with other commands
- [ ] Edge cases are handled gracefully
- [ ] Command is documented in router.js
- [ ] Manual testing completed

## Common Command Patterns

### 1. Get/Set Pattern
```javascript
async execute(args) {
  if (args.length === 0) {
    // GET: Show current value
    return { success: true, data: state.value };
  } else {
    // SET: Update value
    state.value = args[0];
    saveState(state);
    return { success: true, message: 'Value updated' };
  }
}
```

### 2. List Pattern
```javascript
async handleList() {
  const items = loadItems();
  if (items.length === 0) {
    return { success: true, message: 'No items found' };
  }

  console.log('Available items:');
  items.forEach(item => console.log(`  • ${item.name}`));
  return { success: true };
}
```

### 3. Subcommand Pattern
```javascript
async execute(args) {
  const [subcommand, ...rest] = args;

  const handlers = {
    'list': this.handleList,
    'add': this.handleAdd,
    'remove': this.handleRemove
  };

  const handler = handlers[subcommand];
  if (!handler) {
    return { success: false, error: `Unknown subcommand: ${subcommand}` };
  }

  return handler.call(this, rest);
}
```

## Decision Logging

When creating or modifying commands, log in `context/decisions.md`:

```markdown
### API Change: [Date]
- **Command:** sessions tasks archive
- **Change:** New command to move completed tasks to done/ directory
- **Rationale:** Users need way to clean up task list without deleting history
- **API:** sessions tasks archive <task-name>
- **State Impact:** Updates task index, moves file, logs action
- **Testing:** Verified with 3 test tasks, handles missing files gracefully
```

## Related Skills

- **cc-sessions-core** - For broader framework development beyond API
- **cc-sessions-hooks** - If commands need hook integration
- **framework_health_check** - To validate API behavior after changes
- **framework_repair_suggester** - If API commands malfunction
- **daic_mode_guidance** - For understanding mode transitions that commands trigger

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
