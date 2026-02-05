---
name: patterns/vtable
description: Vtable Pattern (C-Specific) pattern for C development
---

# Vtable Pattern (C-Specific)

Struct of function pointers enabling polymorphism. Different implementations provide different function pointer sets. Callers invoke through vtable.

## ikigai Application

**LLM providers:**
```c
typedef struct {
    res_t (*send)(void *impl, ...);
    res_t (*stream)(void *impl, ...);
    void (*cleanup)(void *impl);
} ik_provider_vtable_t;

typedef struct {
    ik_provider_vtable_t *vt;
    void *impl;  // OpenAI ctx, Anthropic ctx, etc.
} ik_llm_client_t;
```

**Layer system:** Each layer type provides render/resize functions.

**Benefits:**
- Runtime polymorphism without inheritance
- Swap implementations transparently
- Mock implementations for testing

**Convention:** Vtable struct named `*_vtable_t`, instance holds `vt` pointer plus `impl` context.
