---
name: claude-mobile-metro-manager
description: Use when starting Metro bundler for Expo development, debugging Metro errors, or enabling expo-mcp local capabilities - manages Metro lifecycle with EXPO_UNSTABLE_MCP_SERVER=1 flag for autonomous testing
---

# Metro Bundler Management with expo-mcp Support

## Overview

Manage Metro bundler lifecycle with **EXPO_UNSTABLE_MCP_SERVER=1** environment variable to enable expo-mcp local capabilities.

**Core principle:** Start Metro with MCP flag. Monitor health. Enable autonomous testing.

**Announce at start:** "I'm using the claude-mobile-metro-manager skill to start Metro with expo-mcp support."

## When to Use

- Starting Metro for development (Phase 4)
- Before iOS builds or expo-mcp testing (Gate 4A)
- Debugging Metro errors (port conflicts, cache issues)
- Enabling expo-mcp local tools (automation_take_screenshot, automation_tap_by_testid, etc.)

## Critical Requirement: MCP Flag

**ALWAYS start Metro with expo-mcp flag:**

```bash
EXPO_UNSTABLE_MCP_SERVER=1 npx expo start
```

**Why**: Enables expo-mcp local capabilities:
- automation_take_screenshot
- automation_tap, automation_tap_by_testid
- automation_find_view_by_testid
- open_devtools
- expo_router_sitemap

**Without flag**: Only server tools available (search_documentation, add_library, generate_*_md, learn)

## Quick Reference

| Task | Command | Tool |
|------|---------|------|
| Start with MCP | ./scripts/start-metro.sh | Serena execute_shell_command |
| Start + clear cache | ./scripts/start-metro.sh --clear-cache | Serena |
| Check health | Read logs/metro.log | morphllm read_file |
| Stop Metro | ./scripts/stop-metro.sh | Serena |
| Verify MCP enabled | Check for "expo-mcp server" in logs | morphllm |

## Core Workflow

### 1. Start Metro with MCP Support

```typescript
mcp__serena__execute_shell_command({
  command: "./scripts/start-metro.sh",
  cwd: "/Users/nick/Desktop/claude-mobile-expo"
});

// Script includes: EXPO_UNSTABLE_MCP_SERVER=1 npm start

// Verify success
mcp__morphllm__read_file({
  path: "/Users/nick/Desktop/claude-mobile-expo/logs/metro.log",
  head: 100
});
// Must show: "Metro.*waiting" AND "expo-mcp server" or "MCP server"
```

### 2. Verify expo-mcp Local Tools Available

After Metro starts with flag, verify local capabilities:

```
"Take a screenshot to test expo-mcp"
```

If successful: expo-mcp local tools are working ✅

If error: Check Metro logs for MCP server status

### 3. Clear Cache When Needed

```typescript
mcp__serena__execute_shell_command({
  command: "./scripts/start-metro.sh --clear-cache"
});
```

**When to clear**:
- "Unable to resolve module" errors
- After dependency changes
- After Metro crash

### 4. Fix Common Errors

**Port 8081 in use**:
```typescript
mcp__serena__execute_shell_command({
  command: "pkill -f metro && ./scripts/start-metro.sh"
});
```

**Module resolution failed**:
```typescript
mcp__serena__execute_shell_command({
  command: "./scripts/start-metro.sh --clear-cache"
});
```

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Start without MCP flag" | WRONG. Local tools won't work. Must use EXPO_UNSTABLE_MCP_SERVER=1. |
| "npm start is fine" | WRONG. Use script with logging and MCP flag. |
| "Don't check logs" | WRONG. Verify MCP server started. |
| "Cache clear is slow" | WRONG. 10s vs hours debugging. |

### ❌ WRONG

```bash
cd claude-code-mobile && npx expo start  # Missing MCP flag!
```

### ✅ CORRECT

```bash
cd claude-code-mobile && EXPO_UNSTABLE_MCP_SERVER=1 npx expo start
# OR use automation script:
./scripts/start-metro.sh  # Has flag built-in
```

## Red Flags

- "MCP flag is optional" → WRONG. Required for autonomous testing.
- "Server tools are enough" → WRONG. Local tools needed for testing.
- "Direct npm start is fine" → WRONG. Use script with flag and logging.

## Integration

- **Enables**: expo-mcp local capabilities for autonomous testing
- **Use BEFORE**: `@claude-mobile-ios-testing` (requires Metro with MCP)
- **Use WITH**: All Phase 4 development (frontend implementation)

## Reference

Metro should show in logs:
```
✅ Metro waiting on port 8081
✅ expo-mcp server listening (or MCP server enabled)
```
