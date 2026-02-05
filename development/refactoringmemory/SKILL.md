---
name: refactoring/memory
description: Memory Refactoring (talloc) refactoring skill
---

# Memory Refactoring (talloc)

talloc-specific refactoring patterns for ikigai. Focus on ownership, hierarchy, and error context lifetime.

## Pattern 1: Fix Error Context Lifetime

**Smell:** Error allocated on context that gets freed before error is returned.

```c
// BROKEN - use-after-free
res_t ik_foo_init(void *parent, foo_t **out) {
    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    res_t result = ik_bar_init(foo, &foo->bar);  // Error on foo
    if (is_err(&result)) {
        talloc_free(foo);  // FREES THE ERROR!
        return result;     // Crash
    }
}
```

**Fix A (Preferred):** Pass parent for error allocation:

```c
res_t ik_foo_init(void *parent, foo_t **out) {
    bar_t *bar = NULL;
    res_t result = ik_bar_init(parent, &bar);  // Error survives on parent
    if (is_err(&result)) return result;

    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    talloc_steal(foo, bar);
    foo->bar = bar;
    *out = foo;
    return OK(*out);
}
```

**Fix B (Fallback):** Reparent error before freeing:

```c
res_t ik_foo_init(void *parent, foo_t **out) {
    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    res_t result = ik_bar_init(foo, &foo->bar);
    if (is_err(&result)) {
        talloc_steal(parent, result.err);  // Save error
        talloc_free(foo);
        return result;
    }
}
```

## Pattern 2: Introduce Temp Context

**Smell:** Intermediate allocations leak or complicate cleanup.

```c
// BEFORE - manual cleanup of each allocation
res_t process(void *ctx, input_t *in) {
    char *buf1 = talloc_array(ctx, char, 1024);
    char *buf2 = talloc_array(ctx, char, 2048);
    parsed_t *p = talloc(ctx, parsed_t);
    // ... work ...
    talloc_free(buf1);
    talloc_free(buf2);
    talloc_free(p);
    return OK(result);
}
```

**After:** Use temp context for intermediate work:

```c
res_t process(void *ctx, input_t *in) {
    void *tmp = talloc_new(ctx);

    char *buf1 = talloc_array(tmp, char, 1024);
    char *buf2 = talloc_array(tmp, char, 2048);
    parsed_t *p = talloc(tmp, parsed_t);
    // ... work ...

    // Steal result to ctx if needed
    if (keep_result) talloc_steal(ctx, result);

    talloc_free(tmp);  // Clean all intermediates
    return OK(result);
}
```

**Critical:** Errors must be on `ctx`, not `tmp`. Pass `ctx` to functions that might fail.

## Pattern 3: Add Missing Context Parameter

**Smell:** Function allocates internally without context parameter.

```c
// BEFORE - hidden allocation
char *format_message(const char *fmt, ...) {
    char *buf = malloc(1024);  // Who frees this?
    // ...
    return buf;
}
```

**After:** Accept context, return on caller's hierarchy:

```c
char *ik_format_msg(void *ctx, const char *fmt, ...) {
    char *buf = talloc_array(ctx, char, 1024);
    // ...
    return buf;  // Caller owns via ctx
}
```

## Pattern 4: Fix Orphaned Allocations

**Smell:** Allocation on NULL or wrong parent.

```c
// BEFORE - orphaned
void *ctx = talloc_new(NULL);  // Root context in non-main function
```

**After:** Receive parent from caller:

```c
res_t ik_module_init(void *parent, module_t **out) {
    module_t *mod = talloc_zero_(parent, sizeof(module_t));
    // mod is child of parent, freed when parent freed
}
```

## Pattern 5: Convert malloc to talloc

**Smell:** Raw malloc/free in codebase.

```c
// BEFORE
char *buf = malloc(size);
// ... use buf ...
free(buf);
```

**After:**

```c
char *buf = talloc_array(ctx, char, size);
// ... use buf ...
// Freed automatically with ctx, or explicitly:
talloc_free(buf);
```

## Pattern 6: Proper Child Relationships

**Smell:** Struct fields allocated on wrong context.

```c
// BEFORE - fields are siblings, not children
res_t init(void *ctx, foo_t **out) {
    foo_t *foo = talloc_zero_(ctx, sizeof(foo_t));
    foo->name = talloc_strdup(ctx, name);  // Sibling of foo!
    foo->data = talloc_array(ctx, char, size);  // Sibling of foo!
}
```

**After:** Fields are children of struct:

```c
res_t init(void *ctx, foo_t **out) {
    foo_t *foo = talloc_zero_(ctx, sizeof(foo_t));
    foo->name = talloc_strdup(foo, name);  // Child of foo
    foo->data = talloc_array(foo, char, size);  // Child of foo
    // Now talloc_free(foo) frees everything
}
```

## Refactoring Checklist

1. **Search for `malloc(`** - Convert to talloc
2. **Search for `talloc_new(NULL)`** - Should only be in main()
3. **Search for `talloc_free` after `is_err`** - Check error context lifetime
4. **Review `_init` functions** - Ensure ctx parameter, proper child allocation
5. **Check struct field allocation** - Fields should be children of struct
6. **Look for cleanup code** - Can it be simplified with temp context?
