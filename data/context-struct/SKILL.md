---
name: patterns/context-struct
description: Context Struct Pattern (C-Specific) pattern for C development
---

# Context Struct Pattern (C-Specific)

Pass state explicitly as struct pointer parameter rather than using globals. First parameter to functions is context containing state and dependencies.

## ikigai Application

**Core pattern:** Every module uses this:
- `ik_repl_ctx_t` - REPL state
- `ik_term_ctx_t` - Terminal state
- `ik_scrollback_t` - Scrollback state
- `ik_env_t` - Runtime environment (planned)

**Convention:** Context is first parameter after talloc context:
```c
res_t ik_scrollback_append(ik_scrollback_t *ctx, const char *line);
```

**Benefits:**
- No global state
- Multiple instances possible
- Explicit dependencies
- Testable (inject mock contexts)

**See:** `project/explicit_context.md` for `ik_env_t` design.
