---
name: claude-hooks-sdk
description: Expert guide for building Claude Code hooks using the claude-hooks-sdk npm package. Use when implementing TypeScript hooks with HookManager, Logger, transforms, context tracking, or troubleshooting SDK features.
---

# Claude Hooks SDK Expert

You are an expert on the `claude-hooks-sdk` npm package. Help users build, configure, and troubleshoot Claude Code hooks using the SDK.

## Quick Reference

### Installation
```bash
bun add claude-hooks-sdk
# or
npm install claude-hooks-sdk
```

### Basic Setup
```typescript
#!/usr/bin/env bun
import { HookManager, success, block, createLogger } from 'claude-hooks-sdk';

const logger = createLogger('my-hook');

const manager = new HookManager({
  logEvents: true,
  clientId: 'my-hook',
  enableContextTracking: true,
  trackEdits: true,
});

manager.onPreToolUse(async (input, context) => {
  if (input.tool_name === 'Bash' && input.tool_input.command.includes('rm -rf /')) {
    return block('Dangerous command blocked');
  }
  return success();
});

manager.run();
```

### Configuration Options

```typescript
interface HookManagerOptions {
  // Logging
  logEvents?: boolean;
  clientId?: string;
  logDir?: string;
  debug?: boolean;

  // Context & Tracking
  enableContextTracking?: boolean;
  trackEdits?: boolean;

  // Error Handling
  blockOnFailure?: boolean;
  enableFailureQueue?: boolean;
  maxRetries?: number;
  handlerTimeout?: number;
}
```

## Logger Utility

```typescript
import { createLogger } from 'claude-hooks-sdk';

const logger = createLogger('my-hook');

logger.info('Always shown');
logger.logDebug('Only shown when DEBUG=1');
logger.warn('Warning message');
logger.error(new Error('Something failed'));
```

## Constants

```typescript
import {
  DEFAULT_HANDLER_TIMEOUT_MS,  // 30000
  DEFAULT_MAX_RETRIES,         // 3
  EXIT_CODE_SUCCESS,           // 0
  EXIT_CODE_ERROR,             // 1
  EXIT_CODE_BLOCK,             // 2
} from 'claude-hooks-sdk';
```

## Transforms

### ConversationLogger
```typescript
import { ConversationLogger } from 'claude-hooks-sdk';

const conversationLogger = new ConversationLogger();

manager.onUserPromptSubmit((input) => {
  conversationLogger.recordUserPrompt(input);
  return success();
});

manager.onStop(async (input, context) => {
  const turn = await conversationLogger.recordStop(input, context);
  console.log(`Turn ${turn.turn_number} recorded`);
  return success();
});
```

### FileChangeTracker
```typescript
import { FileChangeTracker } from 'claude-hooks-sdk';

const fileTracker = new FileChangeTracker();

manager.onPostToolUse((input) => {
  fileTracker.recordChange(input);
  return success();
});

manager.onStop(async (input) => {
  const changes = fileTracker.getBatch(input.session_id);
  console.log(`${changes.total_files} files modified`);
  return success();
});
```

## Hook Event Handlers

```typescript
manager.onSessionStart(async (input, context) => {
  console.log('Session started:', input.session_id);
  return success();
});

manager.onUserPromptSubmit(async (input, context) => {
  // Add context to Claude's prompt
  return success();
});

manager.onPreToolUse(async (input, context) => {
  // Block dangerous operations
  if (shouldBlock(input)) {
    return block('Reason for blocking');
  }
  return success();
});

manager.onPostToolUse(async (input, context) => {
  // React to tool completion
  return success();
});

manager.onStop(async (input, context) => {
  // Session ending - access context.editedFiles
  console.log('Edited files:', context.editedFiles);
  return success();
});
```

## Context Tracking

```typescript
interface EventContext {
  transactionId: string;
  conversationId: string;
  promptId?: string;
  project_dir?: string;
  git?: {
    user: string;
    email: string;
    repo: string;
    branch: string;
    commit: string;
    dirty: boolean;
  };
  editedFiles?: string[];  // When trackEdits: true
}
```

## Session Context Injection

One-liner to inject session info into Claude's context:

```typescript
#!/usr/bin/env bun
import { createUserPromptSubmitHook } from 'claude-hooks-sdk';

createUserPromptSubmitHook();
```

With customization:
```typescript
createUserPromptSubmitHook({
  format: (name, id) => `Session: ${name} [${id.slice(0, 8)}]`,
  customContext: async (input) => `Branch: ${getBranch()}`,
});
```

## Failure Queue

```typescript
const manager = new HookManager({
  enableFailureQueue: true,
  maxRetries: 3,
  onErrorQueueNotEmpty: (size) => {
    console.warn(`${size} events queued for retry`);
  },
});
```

## Blocking vs Non-Blocking

**Non-blocking (default):** Hook failures don't stop Claude Code
```typescript
const manager = new HookManager({
  blockOnFailure: false,
});
```

**Blocking:** Hook failures stop Claude Code
```typescript
const manager = new HookManager({
  blockOnFailure: true,
});
```

## Common Patterns

### API Integration
```typescript
manager.onStop(async (input, context) => {
  await fetch('https://api.example.com/events', {
    method: 'POST',
    body: JSON.stringify({ event: input, context }),
  });
  return success();
});
```

### Command Blocking
```typescript
manager.onPreToolUse(async (input) => {
  if (input.tool_name !== 'Bash') return success();

  const dangerous = [/rm\s+-rf\s+\//, /dd\s+if=\/dev\/zero/];
  for (const pattern of dangerous) {
    if (pattern.test(input.tool_input.command)) {
      return block('Blocked dangerous command');
    }
  }
  return success();
});
```

### File Change Notifications
```typescript
manager.onStop(async (input, context) => {
  if (context.editedFiles?.length > 10) {
    await sendSlackMessage({
      text: `Large changeset: ${context.editedFiles.length} files`,
    });
  }
  return success();
});
```

## Troubleshooting

### Logs not appearing
- Check `logEvents: true` is set
- Log path: `.claude/hooks/{clientId}/logs/events.jsonl`

### Context not enriched
- Verify `enableContextTracking: true`
- For git metadata: must be in a git repo
- For editedFiles: `trackEdits: true` required

### Handler timeout
```typescript
const manager = new HookManager({
  handlerTimeout: 30000,  // 30 seconds
});
```

## Resources

- **npm:** https://www.npmjs.com/package/claude-hooks-sdk
- **GitHub:** https://github.com/hgeldenhuys/claude-hooks-sdk
- **Examples:** https://github.com/hgeldenhuys/claude-hooks-sdk-examples
