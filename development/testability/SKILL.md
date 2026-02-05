---
name: testability
description: Refactoring patterns for hard-to-test code
---

# Testability

## Philosophy

Code that's hard to test is telling you something about its design. Coverage gaps are opportunities to improve architecture, not problems to silence.

**Fix the design, don't silence the messenger.**

## Refactoring Patterns

### 1. Extract Pure Logic from I/O

```c
// BEFORE: Hard to test
res_t process_config(const char *path) {
    char *content = read_file(path);
    // ... parsing logic ...
}

// AFTER: Pure logic extracted
res_t parse_config(const char *content, config_t *out);  // Testable
res_t load_config(const char *path, config_t *out) {     // Thin wrapper
    char *content = read_file(path);
    return parse_config(content, out);
}
```

### 2. Infallible Functions → void

If a function cannot fail, don't pretend it can:

```c
// BEFORE: Fake error path (untestable)
res_t init_defaults(config_t *c) {
    c->timeout = 30;
    return OK_RES;
}

// AFTER: Honest signature
void init_defaults(config_t *c) {
    c->timeout = 30;
}
```

### 3. OOM Checks → Single-Line PANIC

When allocations PANIC on failure, downstream checks become unreachable:

```c
// BEFORE: 3 lines, 2 exclusions
result_t res = allocate_something();
if (is_err(&res)) {                // LCOV_EXCL_LINE
    return res;                     // LCOV_EXCL_LINE
}

// AFTER: 1 line, 1 exclusion
result_t res = allocate_something();
if (is_err(&res)) PANIC("allocation failed"); // LCOV_EXCL_BR_LINE
```

### 4. Unreachable Else → PANIC

```c
// BEFORE: Unreachable else
if (condition_always_true) {
    handle();
} else {
    return ERR(...);  // LCOV_EXCL_LINE
}

// AFTER: Assert invariant
if (condition_always_true) {
    handle();
} else {
    PANIC("Invariant violated");  // LCOV_EXCL_BR_LINE
}
```

### 5. Reduce Conditional Complexity

```c
// BEFORE: Deep nesting
if (a) {
    if (b) {
        if (c) { /* action */ }
    }
}

// AFTER: Early returns
if (!a) return;
if (!b) return;
if (!c) return;
// action
```

### 6. Parameterize Behavior

```c
// BEFORE: Hardcoded, can't test timeout
void wait_for_response(void) {
    sleep(30);
}

// AFTER: Testable
void wait_for_response(int timeout_sec) {
    sleep(timeout_sec);
}
```

### 7. Wrap Vendor Functions

When vendor functions have inline branches we can't cover:

```c
// BEFORE: Can't test yyjson_doc_get_root returning NULL
yyjson_val *root = yyjson_doc_get_root(doc);
if (!root) return ERR(...);  // "Can't happen"

// AFTER: Wrapper allows mocking
yyjson_val *root = yyjson_doc_get_root_(doc);  // Wrapped
if (!root) return ERR(...);  // Testable with mock
```

## When to Refactor vs Mock

| Situation | Action |
|-----------|--------|
| Our code is complex | Refactor |
| External library call | Mock via wrapper |
| System call | Mock via wrapper |

**Rule:** Refactor our code, mock external dependencies.

## Related Skills

- `coverage` - Policy (100% requirement)
- `lcov` - Finding specific gaps
- `mocking` - Testing external dependencies
