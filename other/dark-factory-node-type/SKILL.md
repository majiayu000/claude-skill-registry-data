---
name: dark-factory-node-type
description: "Guide for implementing, registering, and testing new pipeline node types and handlers in the Dark Factory DOT runner."
---

# Adding a New Node Type in Dark Factory

Use this skill when extending the Dark Factory pipeline engine with a new node type, custom execution handler, or graph shape mapping in `runner/handlers.py`.

## When to use

- Adding a new handler function to `runner/handlers.py`.
- Registering a custom handler in `TYPE_REGISTRY` or `REGISTRY`.
- Referencing a new handler in `.dot` pipeline graphs via `type="..."` or custom node shape.
- Writing echo-backend unit tests to exercise custom handler outcomes and state mutations.

## Procedure

1. **Implement the handler:**
   Implement `_my_handler(node, ctx) -> Result` in `runner/handlers.py`.

2. **Register the handler:**
   Register in `TYPE_REGISTRY` (preferred — keyed by `type="..."`) or `REGISTRY` (keyed by DOT shape).

3. **Reference from a pipeline graph:**
   Reference from a `.dot` file with `mynode [type="my_handler", ...]`.

4. **Add echo-backend unit tests:**
   Echo-backend tests should drive paths via `ctx.state["<node>.outcome"]` — see `tests/test_gates.py`.
