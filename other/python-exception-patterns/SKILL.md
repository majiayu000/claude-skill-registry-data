---
name: python-exception-patterns
description: >
  Use this when designing the errors module of a new Python SDK, reviewing code
  that raises bare Exception / RuntimeError or uses bare-except / except
  BaseException, refactoring async code that mishandles CancelledError, or
  documenting Raises: blocks on public API. Covers a single MotadataError base
  with shallow typed subclasses (NetworkError, TimeoutError, AuthError,
  RateLimitError, ValidationError, ServerError, ClientError), raise X from y
  chaining vs from None suppression, the Error suffix rule, except-narrowing
  away from BaseException so asyncio.CancelledError propagates, full-sentence
  exception messages, __cause__ vs __context__, ExceptionGroup / except*
  handling for TaskGroup, and accurate Raises: docstring blocks.
  Triggers: Exception, raise, raise from, except, ExceptionGroup, BaseException, traceback, __cause__, __context__, BaseSDKError.
---

# python-exception-patterns (v1.1.0)

## Rationale

A Python SDK's exception hierarchy is part of its public API. Every `except SomeError:` clause a consumer writes is a binding contract: the SDK must never silently change the type, base class, or condition under which the error is raised. A loose hierarchy ("raise RuntimeError everywhere") forces the consumer into `except Exception:` — which masks real bugs. A noisy hierarchy ("RetryableNetworkErrorAfterTimeoutOnFirstAttempt") forces them into a giant `try/except/except/except` ladder. The pack's convention strikes the middle: a small base + small set of typed sub-classes covering the common discriminations consumers actually want to make.

This skill is cited by `code-reviewer-python` (exception design), `refactoring-agent-python` (R-2 exception chaining, R-3 bare except), `sdk-api-ergonomics-devil-python` (E-4 exception design), `sdk-convention-devil-python` (C-8), `python-asyncio-patterns` (CancelledError handling), `network-error-classification` (cross-language analog).

## Activation signals

- Designing the exception module of a new SDK (`<pkg>/errors.py` or equivalent).
- Code review surfaces `raise Exception(...)` or `raise RuntimeError(...)`.
- Code review surfaces `except Exception:` without re-raise.
- Code review surfaces `raise NewError(...)` (no `from`) inside an `except:` block.
- Quick start has an `except (TypeA, TypeB, TypeC):` ladder.

## Hierarchy convention

```python
# motadatapysdk/errors.py
"""Exception hierarchy for the motadata SDK.

All exceptions raised by the public API inherit from MotadataError. Consumers
catch the base class for blanket handling, or the specific subclass for typed
discrimination.
"""
from __future__ import annotations


class MotadataError(Exception):
    """Base class for every exception raised by motadatapysdk.

    Catch this class to handle any SDK-originated error.
    """


class ConfigError(MotadataError, ValueError):
    """Configuration is invalid (missing required field, out-of-range value).

    Inherits from ValueError so existing ``except ValueError:`` consumers in
    config-parsing code still catch it.
    """


class NetworkError(MotadataError):
    """Network communication failed.

    Subclasses discriminate the failure mode: TimeoutError, ConnectionError,
    DNSError. Catch NetworkError to handle any wire-level failure.
    """


class TimeoutError(NetworkError, builtins.TimeoutError):  # type: ignore[name-defined]
    """Request exceeded the configured timeout.

    Inherits from builtins.TimeoutError so existing ``except TimeoutError:``
    consumers still catch it.
    """


class ConnectionError(NetworkError, builtins.ConnectionError):  # type: ignore[name-defined]
    """Could not establish or maintain a connection."""


class AuthError(MotadataError):
    """Authentication or authorization failed.

    The SDK does NOT discriminate 401 vs 403 by default — both surface as
    AuthError, since the appropriate caller response is the same (refresh creds,
    surface to user). If the application needs to discriminate, inspect
    ``error.status_code``.
    """

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(MotadataError):
    """Server rejected the request as rate-limited.

    The ``retry_after_s`` attribute carries the server's Retry-After hint when
    provided; otherwise None.
    """

    def __init__(self, message: str, *, retry_after_s: float | None = None) -> None:
        super().__init__(message)
        self.retry_after_s = retry_after_s


class ValidationError(MotadataError, ValueError):
    """Caller-supplied input failed validation."""


class ServerError(MotadataError):
    """Server returned a 5xx response."""

    def __init__(self, message: str, *, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


class ClientError(MotadataError):
    """Server returned a 4xx response (other than 401/403/429).

    Subclasses or callers inspect ``status_code``.
    """

    def __init__(self, message: str, *, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code
```

Reasoning for the layered base classes:

- **Single base** (`MotadataError`) — every SDK exception inherits from it. Consumers can catch the base to handle "any SDK error" without enumerating types.
- **Multiple-inheritance with stdlib bases** where the meaning aligns (`TimeoutError(NetworkError, builtins.TimeoutError)`, `ValidationError(MotadataError, ValueError)`). Consumers using `except TimeoutError:` (the stdlib one) still catch the SDK's typed timeout. This is the Python "be a duck" version of Go's typed errors.
- **Typed attributes** on subclasses (`status_code`, `retry_after_s`) carry context the message string can't. Always typed; never `**kwargs` blob.
- **Modest depth** — 1 to 2 layers from the base. Avoid deep chains like `MotadataError → NetworkError → HTTPError → HTTPClientError → HTTPClientError401`. Consumers don't write `except HTTPClientError401:` — they write `except AuthError:`.

## Rule 1 — `raise X from y` for every wrap

Never `raise NewError(...)` from inside an `except OldError as e:` block without explicit chaining:

```python
# WRONG — chain implicit; traceback notes "During handling..." but the cause
# is not pin-pointed and `e.__cause__` is None.
try:
    response = await self._http.get(url)
except aiohttp.ClientConnectionError:
    raise NetworkError(f"connection failed for {url}")

# RIGHT — explicit cause chain
try:
    response = await self._http.get(url)
except aiohttp.ClientConnectionError as e:
    raise NetworkError(f"connection failed for {url}") from e

# RIGHT — explicit suppression (rare; only when the original is genuinely
# unhelpful and would mislead the consumer)
try:
    parse(...)
except SyntaxError:
    raise ValidationError("invalid request body") from None
```

`raise X from y` populates `X.__cause__ = y`; consumers that walk the chain (and most logging frameworks) display BOTH levels. `raise X from None` explicitly suppresses the original's traceback for cases where surfacing it would be confusing.

## Rule 2 — Class name MUST end in `Error`

PEP 8 §Exception Names. `NetworkError` not `NetworkException`. The `Error` suffix is the language convention; `Exception` is reserved for the stdlib base. Caught by `sdk-convention-devil-python` C-10.

## Rule 3 — Never raise bare `Exception` / `RuntimeError` from public API

```python
# WRONG
raise Exception("session is closed")
raise RuntimeError(f"unexpected status: {status}")

# RIGHT — typed; the consumer can catch the specific class
raise InvalidStateError("session is closed")
raise ServerError(f"unexpected status: {status}", status_code=status)
```

`Exception` and `RuntimeError` are FINE for genuinely-internal helper code where the only consumer is the SDK itself (e.g., a pre-condition the SDK author KNOWS is met). For anything that crosses the public API boundary, raise a typed SDK error.

## Rule 4 — `except` is not a catch-all

```python
# WRONG — swallows everything including KeyboardInterrupt
try:
    do_thing()
except:
    pass

# WRONG — swallows everything except KeyboardInterrupt/SystemExit, but still
# masks real bugs (TypeError, AttributeError, ImportError)
try:
    do_thing()
except Exception:
    pass

# RIGHT — narrow type
try:
    do_thing()
except SpecificError as e:
    log.warning("expected failure", exc_info=e)

# RIGHT — broad except WITH re-raise (e.g., for cleanup or logging)
try:
    do_thing()
except Exception as e:
    log.exception("unexpected failure")
    raise
```

A bare `except:` (no class) catches `BaseException`, which includes `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`. This breaks Ctrl-C handling and async cancellation. Always specify a type, even if it's `Exception`.

#### Refactoring recipe — `except BaseException` even with a preceding `CancelledError` arm

A common-but-fragile pattern is to "handle" the cancellation problem by writing a preceding `except asyncio.CancelledError: raise` arm and then a broad `except BaseException as e:` arm to catch "everything else, including unknown failure modes from a user-supplied callback". This compiles, runs, and looks defensible. **It is not.**

The pattern is fragile under future edits: if a maintainer drops or reorders the `CancelledError` arm (refactor, mechanical lint fix, accidental `except Exception → BaseException` widening), the broad arm silently swallows cancellation. Async cancellation propagation depends on the *combination* of two arms holding their relative positions; that invariant is not enforceable mechanically and is invisible to a code reviewer reading either arm in isolation.

The canonical form when intent is "catch any user-hook failure but propagate cancellation" is:

```python
# WRONG — fragile-by-construction (this run's _pool.py L247/L381/L451/L536)
try:
    await user_hook()
except asyncio.CancelledError:
    raise
except BaseException as e:                  # one upstream edit and cancellation is swallowed
    log.exception("user hook failed")
    raise UserHookError("hook raised") from e
```

```python
# RIGHT — drop BaseException to Exception; CancelledError already does not match
try:
    await user_hook()
except Exception as e:                      # asyncio.CancelledError is BaseException-subclass-only
    log.exception("user hook failed")       # since 3.8; never matches this arm
    raise UserHookError("hook raised") from e
```

The narrowing from `BaseException` to `Exception` is the entire fix. Since Python 3.8, `asyncio.CancelledError` derives directly from `BaseException` (not `Exception`); a single `except Exception:` arm catches every "user-hook failure" the broad arm meant to catch AND lets cancellation propagate. The preceding `except CancelledError: raise` arm becomes redundant — delete it; do not leave it in place "for safety". Defense-in-depth here is anti-defense: it encourages future authors to widen the broad arm because "cancellation is already handled above".

**`BaseException` is appropriate in exactly one situation in SDK code: a finally-style cleanup block that re-raises unconditionally** (and even there, prefer `try/finally` over `try/except BaseException`). Anywhere else — and *especially* when paired with a preceding `CancelledError` arm — `BaseException` is the wrong tool. Caught by `code-reviewer-python` and `refactoring-agent-python` R-3 (bare-except narrowing).

## Rule 5 — Cancellation is special (asyncio)

`asyncio.CancelledError` inherits from `BaseException` (not `Exception`) since Python 3.8. This is INTENTIONAL: a generic `except Exception:` does NOT catch cancellation, which is correct behavior — async cancellation MUST propagate.

```python
# RIGHT — cancellation propagates
try:
    await self._step()
except Exception as e:                  # does NOT catch CancelledError
    log.warning("step failed", exc_info=e)
    raise NetworkError("step failed") from e

# WRONG — swallows cancellation
try:
    await self._step()
except BaseException:                   # catches CancelledError
    log.warning("anything")
    return                              # caller's TaskGroup hangs forever
```

If you specifically need to catch cancellation for cleanup, do so AND re-raise:

```python
try:
    await self._step()
except asyncio.CancelledError:
    self._cleanup_partial()             # idempotent cleanup
    raise                               # ALWAYS re-raise CancelledError
```

(See also `python-asyncio-patterns` Rule 4.)

## Rule 6 — Exception messages are sentences

```python
# WRONG — fragmented
raise NetworkError("Connection failed")
raise ValidationError(f"bad: {value}")
raise AuthError(f"401 {response.text}")

# RIGHT — full sentence; includes the relevant context the consumer needs
raise NetworkError(f"failed to connect to {url} after {attempts} attempts")
raise ValidationError(f"topic must match [a-z][a-z0-9-]+, got {value!r}")
raise AuthError(f"server rejected token (status 401)", status_code=401)
```

Use `repr()` (`{value!r}`) for values that may contain whitespace, control characters, or be empty — repr makes the issue obvious. Never log full credentials in messages.

## Rule 7 — `__cause__` vs `__context__`

- `__cause__` is set by `raise X from Y` — explicit chain.
- `__context__` is set automatically when `raise X` happens inside an `except` block — implicit chain.

Consumers and loggers usually display BOTH. The display order:
- `Y` → `... During handling of the above exception, another exception occurred: ...` → `X` (when `from` was NOT used).
- `Y` → `... The above exception was the direct cause of the following exception: ...` → `X` (when `from Y` was used).

The two phrasings have different meanings. "Direct cause" is the explicit, intentional case. ALWAYS use `from Y` when wrapping; don't rely on the implicit `__context__` chain.

## Rule 8 — `ExceptionGroup` from TaskGroup (Python 3.11+)

When a `TaskGroup` has multiple failing tasks, the body's exception is an `ExceptionGroup`:

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(op1())
    tg.create_task(op2())
# If both fail, the await on __aexit__ raises ExceptionGroup
# containing both exceptions.

# Consumer — except* (PEP 654) for typed extraction
try:
    async with asyncio.TaskGroup() as tg:
        ...
except* NetworkError as eg:
    for e in eg.exceptions:
        log.warning("network failure", exc_info=e)
except* ValidationError as eg:
    ...
```

`except*` is PEP 654 syntax (3.11+); it splits the group by type. SDK code that orchestrates fan-out via TaskGroup MAY raise `ExceptionGroup` from its public API — document that in the docstring's `Raises:` block.

## Rule 9 — Document `Raises:` accurately

Every public function's docstring lists which exceptions it raises (Google-style):

```python
async def publish(self, topic: str, payload: bytes) -> None:
    """Publish ``payload`` to ``topic``.

    Args:
        topic: Destination topic.
        payload: Bytes to publish.

    Raises:
        ValidationError: If ``topic`` is empty or contains forbidden characters.
        NetworkError: If the underlying connection failed.
        TimeoutError: If the configured timeout elapsed before completion.
        AuthError: If the server rejected the credentials.
    """
```

If the function may also propagate `asyncio.CancelledError` (and most async functions can), document it ONLY when something specific happens at cancellation:

```python
    Raises:
        ...
        asyncio.CancelledError: Cancellation aborts the in-flight HTTP request
            and rolls back any partial transactional state.
```

Caught by `documentation-agent-python` for accuracy.

## GOOD: full async function with proper exception flow

```python
async def publish(self, topic: str, payload: bytes) -> None:
    """Publish ``payload`` to ``topic``.

    Raises:
        ValidationError: If ``topic`` is empty.
        NetworkError: On wire-level failure.
        TimeoutError: On configured timeout expiry.
        AuthError: On 401/403 response.
        ServerError: On 5xx response.
    """
    if not topic:
        raise ValidationError("topic must not be empty")

    try:
        async with asyncio.timeout(self._config.timeout_s):
            async with self._session.post(self._url(topic), data=payload) as resp:
                if resp.status in (401, 403):
                    raise AuthError(
                        f"server rejected request ({resp.status})",
                        status_code=resp.status,
                    )
                if 500 <= resp.status < 600:
                    raise ServerError(
                        f"server returned {resp.status}",
                        status_code=resp.status,
                    )
                resp.raise_for_status()
    except builtins.TimeoutError as e:        # asyncio.timeout maps to this
        raise TimeoutError(
            f"publish to {topic!r} exceeded {self._config.timeout_s}s"
        ) from e
    except aiohttp.ClientConnectionError as e:
        raise ConnectionError(
            f"connection lost while publishing to {topic!r}"
        ) from e
    except aiohttp.ClientResponseError as e:
        raise ClientError(
            f"client error: {e.message}", status_code=e.status,
        ) from e
```

Demonstrated: typed errors per failure class (rule 3), `from e` on every wrap (rule 1), full-sentence messages (rule 6), `Raises:` block (rule 9), cancellation propagates implicitly (rule 5).

## BAD anti-patterns

```python
# 1. Wrap without from
try:
    response = http.get(url)
except aiohttp.ClientError:
    raise NetworkError("failed")               # __cause__ is None

# 2. Bare Exception in public API
raise Exception("session is closed")          # untyped

# 3. except: pass
try:
    do_thing()
except:                                        # catches everything
    pass

# 4. except Exception swallow
try:
    do_thing()
except Exception:
    pass                                       # caller gets None back

# 5. except BaseException
try:
    await something()
except BaseException:                          # catches CancelledError
    cleanup()

# 6. Exception name no Error suffix
class NetworkException(Exception): ...        # PEP 8 violation

# 7. Single deep hierarchy
class HTTPClientError401(HTTPClientError): ... # consumer never catches this depth

# 8. Lying Raises:
async def fetch(...) -> bytes:
    """Raises:
        NetworkError: On wire-level failure.
    """
    return await self._http.get(...)            # also raises TimeoutError, AuthError;
                                                # docstring is incomplete

# 9. Logging credentials
raise AuthError(f"failed for token {token}")   # token in message; leaks to logs

# 10. Catching to hide
try:
    self._validate(input)
except ValidationError:
    self._validate(default_input)              # silently uses default; surprises caller
```

## Cross-references

- `python-asyncio-patterns` (Rule 4) — `CancelledError` semantics.
- `python-mypy-strict-typing` — typed exception attributes (`status_code: int | None`).
- `python-doctest-patterns` — `Raises:` block in docstrings.
- `network-error-classification` (shared) — how to classify wire errors as retriable / fatal / auth.
- `idempotent-retry-safety` (shared) — when an exception is safe to retry on.
- `sdk-convention-devil-python` C-8 — design-rule enforcement at D3.
- `refactoring-agent-python` R-2 (exception chaining), R-3 (bare except narrowing).
