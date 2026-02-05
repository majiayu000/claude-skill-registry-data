---
name: patterns/composite
description: Composite Pattern pattern for C development
---

# Composite Pattern

Compose objects into tree structures. Individual objects and compositions treated uniformly through common interface.

## ikigai Application

**Layer system:** Layers (scrollback, separator, input, spinner) compose into layer stack. Each implements same render interface:
```c
typedef struct {
    void (*render)(void *layer, ik_render_ctx_t *render);
    void (*resize)(void *layer, int width, int height);
} ik_layer_vtable_t;
```

**Rendering:** REPL iterates layers, calls render on each. Doesn't care if layer is simple or composite.

**Future uses:**
- Nested UI components
- Tool result trees
- Message threading/nesting

**Benefit:** Add new layer types without changing render loop.
