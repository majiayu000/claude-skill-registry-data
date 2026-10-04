---
name: session-isolation-validator
description: Validate that builtin servers and external MCP managers maintain proper session isolation. Use when auditing session isolation, checking for cross-session state leakage, or verifying per-session MCPServiceProxy instantiation.
---

# Session Isolation Validator

Validate that LibrAgent maintains proper session isolation across all MCP servers and managers.

## Validation Rules

### Builtin Servers

- [ ] Each builtin server implements `BuiltinMCPServer` trait
- [ ] Server state is keyed by session ID
- [ ] No `lazy_static!`, `once_cell!`, or global `Mutex` for shared state
- [ ] `get_service_context()` returns session-specific data

### External MCP Managers

- [ ] `HttpSessionManager` creates isolated sessions per agent session
- [ ] `SessionMCPManager` maintains per-session `MCPServiceProxy` instances
- [ ] No singleton patterns that share state across sessions
- [ ] Stdio server processes are session-scoped

### Frontend

- [ ] `AgentSessionContext` isolates state per session
- [ ] No global React state that mixes sessions
- [ ] Event listeners for `agent:event` are session-scoped

## Audit Commands

```bash
# Find potential global state anti-patterns
grep -r "lazy_static\|once_cell\|global\|GLOBAL" src-tauri/src/mcp/
grep -r "static mut\|unsafe" src-tauri/src/mcp/

# Find session ID usage patterns
grep -r "session_id\|sessionId" src-tauri/src/mcp/ | head -50

# Verify MCPServiceProxy instantiation
grep -r "MCPServiceProxy" src-tauri/src/
```

## Key Invariants

1. **No Global State**: Complete isolation prevents cross-session interference
2. **Stateful Tools**: Planning todos, Knowledge items, Browser sessions scoped to session ID
3. **Session-Specific Workspace**: Each agent operates in isolated directory
4. **Tool State Isolation**: Each session gets isolated tool instances
