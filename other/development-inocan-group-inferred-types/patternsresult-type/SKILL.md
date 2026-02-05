---
name: patterns/result-type
description: Result Type Pattern (C-Specific) pattern for C development
---

# Result Type Pattern (C-Specific)

Return struct containing success/failure status plus value or error. Explicit error handling without exceptions. Caller must check result.

## ikigai Application

**Core type:** `res_t` used throughout:
```c
res_t result = ik_cfg_load(ctx, path, &cfg);
if (!result.ok) {
    // Handle error, result.error contains message
}
```

**Macros:**
- `OK(value)` - Construct success result
- `ERR(msg)` - Construct error result
- `TRY(expr)` - Propagate error if failed
- `CHECK(cond, msg)` - Return error if condition false

**Benefits:**
- Errors can't be ignored (must check `.ok`)
- Error context propagates up call stack
- No hidden control flow (unlike exceptions)

**See:** `project/error_handling.md` for patterns.
