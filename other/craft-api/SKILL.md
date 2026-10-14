---
name: craft-api
description: Crafting API surfaces. Entry points, fluent builders, progressive disclosure.
---

# Skill: Craft API

> "The best API is the one developers already know how to use before reading the docs."

## The Standard

1. **One Obvious Entry Point**: Every package has one clear "start here." Never two equally-valid paths to the same thing.

   | Style                     | Example                          | When                                       |
   |---------------------------|----------------------------------|--------------------------------------------|
   | Trait method              | `$model->addMedia($file)`        | Package augments a model                   |
   | Static factory            | `QueryBuilder::for(User::class)` | Package is standalone                      |
   | `::make()` schema builder | `TextInput::make('name')`        | Declarative UI/component system (Filament) |
   | Manager / driver          | `Notification::driver('slack')`  | Multi-implementation service               |
   | Helper function           | `activity()->log('...')`         | Universal utility, used everywhere         |
   | Constructor               | `new UserData(name: 'John')`     | Value objects, DTOs                        |

2. **Fluent Builders**: Configuration methods return `$this`. Terminal methods return the result. Configuration accumulates, execution happens once. The terminal method name makes the action explicit.

3. **Terminal Method Pattern**: Configure, then execute. The builder is inert until the terminal method fires. Never mix configuration with execution.

4. **Progressive Disclosure**: Four layers. Each additive.

   - **Layer 1 -- Zero-config**: Works immediately. One method call.
   - **Layer 2 -- Common customization**: Named collections, custom properties, guard specification.
   - **Layer 3 -- Power user**: Custom filters, responsive images, batch logging. Full control.
   - **Layer 4 -- Framework extension**: Implement contracts, extend base classes, swap implementations.

5. **Named Constructors**: Static factory methods for value objects and declarations. Every common case gets its own factory. `AllowedFilter::exact()`, `::partial()`, `::scope()`, `::callback()`.

6. **`Conditionable` and `Tappable` Traits**: Add `Conditionable` to builders for fluent conditional logic (`when()`, `unless()`) without breaking method chains. Add `Tappable` for inspection/side-effects mid-chain.

7. **Method Naming**: Consistent verb prefixes across the entire package.

   | Prefix           | Contract               | Example                            |
   |------------------|------------------------|------------------------------------|
   | `has`            | Returns `bool`         | `hasRole()`, `hasMedia()`          |
   | `get`            | Returns the value      | `getMedia()`, `getTranslation()`   |
   | `set`            | Assigns the value      | `setTranslation()`, `setLocale()`  |
   | `add`            | Appends                | `addMedia()`, `addLogChange()`     |
   | `find`           | Looks up by identifier | `findByName()`, `findById()`       |
   | `sync`           | Replaces all           | `syncRoles()`, `syncPermissions()` |
   | `clear`          | Removes all            | `clearMediaCollection()`           |
   | `using` / `with` | Fluent configuration   | `usingName()`, `withProperties()`  |
   | `scope`          | Query scope            | `scopeRole()`, `scopePermission()` |

   Break these conventions and developers lose trust in the API.

8. **Type-Rich Signatures**: Accept everything reasonable. Return types on everything. Union types are a feature, not a smell.

9. **IDE Coverage**: Comprehensive `@throws` on every method that can throw. Full `@template` and `@mixin` coverage. Generics on builders, `@mixin` annotations on proxied classes. The IDE experience is mandatory.

## The Anti-Patterns

| Don't                                              | Do                                          | Why                                              |
|----------------------------------------------------|---------------------------------------------|--------------------------------------------------|
| Two equally-valid entry points                     | One obvious path                            | Ambiguity erodes confidence                      |
| Builder methods that execute                       | Separate configuration from execution       | Side effects in configuration are invisible bugs |
| Return `void` from fluent methods                  | Return `$this` or `static`                  | Breaks method chaining                           |
| Missing return type annotations                    | Explicit types on every method              | IDE and static analysis depend on it             |
| Inconsistent verb prefixes                         | Follow the naming table above               | Predictability is the API contract               |
| Accept only `string` when `BackedEnum` makes sense | Union types: `string` or `BackedEnum`       | Meet developers where they are                   |
| Manual conditional logic in chains                 | Use `Conditionable` trait                   | `when()` and `unless()` are cleaner              |

**See also:** craft-trait (trait-based entry points), decide-facade (choosing the right entry point pattern).

## Real-World Examples

See [examples.md](examples.md).
