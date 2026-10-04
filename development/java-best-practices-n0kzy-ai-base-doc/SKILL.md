---
name: java-best-practices
description: >-
  Modern Java 17+ / 25 coding standards for this project. Use when writing, reviewing,
  or refactoring Java code. Triggers on: new classes, code review, instanceof,
  sealed/record types, nullability, naming, exception handling, or any Java file edit.
---

# Java Best Practices

## Core Principles

- **Clarity over cleverness**: readable code > "smart" code.
- **Immutable by default**: `final` fields, `record` for DTOs, unmodifiable collections.
- **Fail fast**: validate inputs early, use specific exceptions.
- **Null safety**: `@Nonnull` / `@Nullable` annotations on every public method parameter and return.

## Java 17+ / 25 Patterns

### Use Modern Language Features

| Feature | When |
|---------|------|
| `record` | Immutable data carriers (DTOs, configs, results) |
| Sealed classes | Controlled type hierarchies (spell types, executor types) |
| Pattern matching `instanceof` | `if (spell instanceof MovementSpell ms)` — NO raw cast |
| `switch` expressions | Replace `if/elif` chains on enums or sealed types |
| Text blocks `"""` | Multi-line strings, JSON templates |
| `var` | Only when type is obvious from RHS (e.g., `var map = new HashMap<>()`) |

### Anti-Patterns to AVOID

```java
// ❌ BAD: raw instanceof + cast
if (spell instanceof MovementSpell) {
    MovementSpell ms = (MovementSpell) spell;
}

// ✅ GOOD: pattern matching
if (spell instanceof MovementSpell ms) {
    ms.getIntensity();
}

// ❌ BAD: bare catch
catch (Exception e) { }

// ✅ GOOD: log or rethrow
catch (Exception e) {
    LOGGER.atWarning().log("Context: %s", e.getMessage());
}

// ❌ BAD: mutable DTO
public class SpellResult {
    public boolean success;
    public String message;
}

// ✅ GOOD: record
public record SpellResult(boolean success, String message) {}
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Class / Interface | PascalCase | `SpellExecutor`, `MovementSpell` |
| Method / Field | camelCase | `castSpell()`, `spellModule` |
| Constant | UPPER_SNAKE | `MAX_MANA`, `DEFAULT_COOLDOWN` |
| Package | lowercase | `com.magistere.wizardingtales.casting` |
| Enum value | PascalCase or UPPER_SNAKE | `SpellType.PROJECTILE` |

## Null Handling

1. Annotate ALL public method parameters: `@Nonnull` or `@Nullable`
2. Never return `null` from a method without `@Nullable` annotation
3. Validate `@Nonnull` params at method entry for public API
4. Prefer `Optional<T>` for query methods that may not find a result
5. Use `Objects.requireNonNull()` for constructor params

## Exception Strategy

| Layer | Strategy |
|-------|----------|
| Public API | `IllegalArgumentException` / `IllegalStateException` with message |
| Internal logic | Specific domain exceptions (`SpellCastException`) |
| External calls (I/O, sound) | Catch + log, never silent swallow |
| Constructors | `Objects.requireNonNull()` for required params |

## Collections

- Prefer `Map.of()`, `List.of()`, `Set.of()` for small immutable collections
- Use `Collections.unmodifiableMap()` when wrapping mutable maps for external API
- Prefer `EnumMap<SpellType, V>` over `HashMap<SpellType, V>` for enum keys
- Use `computeIfAbsent()` instead of `containsKey()` + `put()`

## Logging

- Use `HytaleLogger.forEnclosingClass()` — never `System.out.println()` in production code
- Parameterized messages: `LOGGER.atInfo().log("Spell %s cast by %s", spellId, playerId)`
- Log at appropriate levels: `atFine()` for debug, `atInfo()` for lifecycle, `atWarning()` for recoverable errors

## Thread Safety

- Game state mutations ONLY through `CommandBuffer`
- Use `world.execute(() -> ...)` for deferred world operations
- Never store mutable shared state without synchronization

## Verification

Before marking Java work done:

```bash
./gradlew build
./gradlew test
```

Check for: compilation errors, deprecation warnings, unchecked cast warnings.
