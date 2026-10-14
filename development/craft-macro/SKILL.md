---
name: craft-macro
description: Crafting macros. Runtime extension of Laravel core classes.
---

# Skill: Craft Macro

> "Macros let packages add methods to classes they don't own."

## The Standard

1. **Single Macros for One-Off Methods**: Use `ClassName::macro('name', fn () => ...)` to add individual methods. Register in your service provider's `boot()`. The closure is bound to the target instance via `$this`. Keep macros small and focused -- one behavior per macro.

2. **Mixins for Grouped Methods**: Use `ClassName::mixin(new YourMixin)` when registering multiple related macros. Each method on the mixin class returns a closure that becomes the macro. This is the double-closure pattern: the mixin method is invoked by reflection, and its return value is bound to the target instance.

3. **Macros Over Subclassing**: Prefer macros when adding behavior to framework classes. You cannot subclass `Collection`, `Request`, or `Builder` -- they're resolved by the framework. Macros extend them without touching the resolution chain. This is the right tool for the job.

4. **Register in boot(), Not register()**: Macros depend on the class being loaded. Register them in `packageBooted()` or `boot()`, never in `register()`. The service provider lifecycle guarantees the target class exists at boot time.

5. **Document With @method Annotations**: Macros are invisible to static analysis and IDEs. Add `@method` annotations to a mixin class or document them in your README. Without annotations, developers discover macros by accident, not by autocomplete.

6. **Know When NOT to Macro**: Macros are runtime monkey-patching. Use them for convenience methods on framework classes. Do not use them for core package logic, complex behavior, or anything that needs testing in isolation. If the logic is complex, it belongs in your own class.

## The Anti-Patterns

| Don't                                  | Do                              | Why                                  |
|----------------------------------------|---------------------------------|--------------------------------------|
| Put business logic in macros           | Keep macros as thin wrappers    | Macros are hard to test in isolation |
| Register macros in `register()`        | Register in `boot()`            | Target class may not exist yet       |
| Add many unrelated macros to one class | Group related macros in a mixin | Cohesion matters                     |
| Skip IDE annotations                   | Add `@method` docblocks         | Discoverability is DX                |
| Subclass framework classes             | Use macros                      | Framework resolves its own classes   |

**See also:** craft-extension-point (Macroable as one of nine extension mechanisms).

## Real-World Examples

See [examples.md](examples.md).
