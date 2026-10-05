---
name: ha:python-idioms
description: "Python/asyncio runtime patterns and idioms for Home Assistant — typed code, match/case, async composition, executor jobs, event loop. Use when designing integration modules or debugging asyncio runtime issues."
effort: medium
user-invocable: false
---

# Python Idioms

Reference for writing idiomatic Home Assistant Python code with asyncio-runtime-aware patterns. (These patterns are the HA-flavored equivalents of what a TypeScript/Node service would express with discriminated unions and `worker_threads`.)

## Iron Laws — Never Violate These

1. **NO EXECUTOR JOB WITHOUT A BLOCKING REASON** — `hass.async_add_executor_job` models blocking I/O and CPU isolation, NOT code structure (P4)
2. **EXECUTOR CROSSINGS ARE EXPENSIVE** — Batch executor work into one job; schedule loop work from a thread only via `hass.loop.call_soon_threadsafe`, never directly (P4)
3. **NARROW BEFORE YOU ACCESS** — Never reach into a value with `cast()`/`# type: ignore`/`getattr` when restructuring would let mypy prove it safe (P5)
4. **SCHEMAS AT THE BOUNDARY** — voluptuous schemas + selectors validate external input in config flows and service actions; trust typed data internally (P3, PS15)
5. **CATCH ONLY WHAT YOU CAN NAME** — Never bare/broad `except Exception` outside the config flow (P1); never log-and-raise (P2)
6. **NO STRINGLY-TYPED KEYS WHERE AN ENUM FITS** — `StrEnum`/`Literal` over magic strings; never `.get()` a key the schema guarantees (PS2)
7. **IMPORTS ARE I/O** — Imports live at module top; never import inside async paths ("we should not do imports here as that causes IO" — joostlek, P4); no module-level mutable globals (P6)
8. **LIFECYCLE-MANAGE ALL LONG-LIVED RESOURCES** — Subscriptions/tasks belong in `async_added_to_hass` via `async_on_remove`; unload symmetrically with `entry.async_on_unload` (PS4)
9. **PROTOCOL LIVES IN THE LIBRARY** — Transport, parsing, and device semantics go in a published PyPI library; the integration is glue (P11)
10. **SCRIPTS START ONLY WHAT THEY NEED** — A one-off dev script that only needs one helper must not boot a full Home Assistant instance (event loop, recorder, every loaded integration)
11. **STATE CAN CHANGE ACROSS EVERY AWAIT** — Capture what you need before awaiting; at each await point, narrate what may run while you're suspended (PS19, strong-defaults §D-6)

## asyncio Runtime Architecture (Why Home Assistant Works This Way)

- **Single-threaded event loop** — One Python thread runs all coroutines; concurrency comes from non-blocking I/O, not shared-memory threads
- **No implicit races between awaits** — But `await` yields the loop, so state can change between await points (entities removed, entries unloaded)
- **Executor pool for blocking work** — Sync library calls run in a bounded thread pool via `hass.async_add_executor_job`; long jobs starve other integrations
- **`@callback` marks loop-safe sync code** — Runs synchronously on the loop with no suspension point; must never block or await (PS19)
- **"Fail fast, retry clean"** — Setup raises `ConfigEntryNotReady` and Home Assistant retries with backoff to a known-good state; don't limp along after unknown errors (P3, P16)

## Core Principles

1. **Narrow over cast** — `match`/`case` and `isinstance` first, then restructure the types; never silence mypy (P5)
2. **Raise the right exception for expected failures** — `ServiceValidationError`/`HomeAssistantError` with translation keys for expected errors, plain raises for bugs (P3)
3. **Async/await with guard clauses** — Start with the awaited value, return early on invalid states (strong-defaults §D-3)
4. **Fail fast on the unexpected** — Handle expected errors, let unexpected ones propagate to the setup retry / service error machinery
5. **Explicit over implicit** — Type hints everywhere, exhaustive `match` with `assert_never`, no `Any` (PS20)

Guidance, not law: skip gratuitous `@typing.final` — "Our whole model is based on overriding" (frenck, CONTESTED, strong-defaults §C-4).

## Quick Decision Trees

### Control Flow

```
Need to distinguish shapes? → StrEnum/Literal + match/case (or isinstance narrowing)
Multiple async operations? → async/await with early returns
Boolean conditions? → if/else (single) or match (multiple)
```

### Error Handling

```
Expected failure? → typed HA exception with translation keys (P3)
Unexpected/bug? → raise (let setup retry / the service layer surface it)
Third-party library? → except (only here, narrowed to the library's exceptions!)
```

### Concurrency

```
Need state?
├─ No → Plain functions (or @callback if called from the loop)
├─ Per-entry fetched data → DataUpdateCoordinator; entities read coordinator.data
├─ Blocking library → hass.async_add_executor_job (one batched job)
└─ One-off async → entry.async_create_background_task / asyncio.gather
```

## Quick Patterns

```python
# match/case narrowing over an enum
def process(user: User) -> None:
    """Handle a user according to status."""
    match user.status:
        case UserStatus.ACTIVE:
            activate(user)
        case UserStatus.INACTIVE:
            deactivate(user)

# async/await for the happy path
async def async_create_order(client: ApiClient, user_id: str, product_id: str) -> Order:
    """Create an order for a user."""
    user = await client.async_get_user(user_id)
    return await client.async_create_order(user, product_id)

# Executor job for a blocking library — one batched call
data = await hass.async_add_executor_job(client.fetch_all)
```

## Common Pitfalls

| Wrong | Right |
|-------|-------|
| `len(list(mapping.keys())) == 0` | `not mapping` |
| `return -1` / `""` from `native_value` on error | `return None` — never a sentinel (P8) |
| `cast(MyData, entry.runtime_data)` | `type MyConfigEntry = ConfigEntry[MyData]` (P6) |
| `open()` / `requests.get` / `time.sleep` in `async def` | `hass.async_add_executor_job` or an async library (P4) |
| `except Exception: pass` swallowing everything | Catch the library's specific exceptions; re-raise the rest (P1) |
| Defaults and guards for cases that can't happen | Only code for proven needs — delete unreachable branches (PS9) |
| Single-use helper or constant parked in `const.py` | Inline it; `const.py` holds shared constants only (PS10) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/pattern-matching.md` - Type narrowing, match/case, StrEnum discriminants, TypeGuard
- `${CLAUDE_SKILL_DIR}/references/asyncio-runtime-patterns.md` - Event loop, executor jobs, config-entry lifecycle, reentrancy
- `${CLAUDE_SKILL_DIR}/references/error-handling.md` - HA exception taxonomy, narrow except, never-swallow
- `${CLAUDE_SKILL_DIR}/references/async-composition.md` - async/await composition, guard clauses, early returns
- `${CLAUDE_SKILL_DIR}/references/troubleshooting.md` - Production debugging (memory, blocking calls, crashes)
- `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` - Common mistakes and fixes
- `${CLAUDE_SKILL_DIR}/references/dev-scripts.md` - script.* modules, argument parsing, CLI output
- `${CLAUDE_SKILL_DIR}/references/modern-syntax-features.md` - `type` aliases, match/case, walrus, dataclasses, StrEnum (recent Python)
- `${CLAUDE_SKILL_DIR}/references/strict-type-checking.md` - mypy strict per-component, narrowing, the type gate in CI
