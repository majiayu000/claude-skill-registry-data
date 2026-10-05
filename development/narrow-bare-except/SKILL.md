---
name: ha:narrow-bare-except
description: "Narrow bare/broad except blocks in Home Assistant Python so real errors like TypeError, AttributeError, and KeyError propagate instead of being swallowed — and convert the expected ones into the correct HA exception. Use to audit except blocks and refactor error handling."
effort: medium
user-invocable: true
argument-hint: "[file_path | directory | --all]"
paths:
  - "**/*.py"
---

# Narrow Bare Except

Turn `except:` / `except Exception:` blocks into
`except SpecificError as err: ...` so programmer bugs propagate while known failure
modes stay handled — and, in Home Assistant code, are re-raised as the *correct* HA
exception (`UpdateFailed`, `ConfigEntryNotReady`, `ServiceValidationError`, …).

## Why this matters

Bare/broad except blocks (`except:`, `except Exception:`, `except BaseException:` with no
re-raise) swallow **every** error, including `AttributeError` from a typo'd attribute,
`NameError` from a missing import, `TypeError` from passing the wrong type, and `KeyError`
from a schema-guaranteed key. The symptom isn't a traceback — it's a silent `None`, a fake
"unavailable" state, or a coordinator that never surfaces the real fault. Bugs that should
fail a test or show up in a review become quiet degradations.

The Erlang [Secure Coding Guide](https://www.erlang.org/doc/system/secure_coding.html) makes
the same case at the BEAM level — rule **LNG-002** ("Do Not Use `catch`") warns that a
legacy catch-all form conflates normal returns and different failure classes. A bare `except`
in Python is the direct analogue: `except Exception:` conflates a `ClientConnectionError` a
coordinator should turn into `UpdateFailed` with an `AttributeError` that means the code is
wrong.

> Orientation: this skill is the Python analogue of narrowing a bare `catch` in a typed
> language — same discipline (trace the body, name the exact exceptions, re-raise the rest),
> different exception hierarchy and re-raise targets.

## Iron Laws

1. **Never catch bare/broad `Exception` outside the config flow** (P1). Every except must
   name the exact expected exceptions before handling. Carve-outs where a broad catch is
   allowed: `config_flow.py`, background tasks (`hass.async_create_task` wrappers),
   top-level setup handlers, and the coordinator base class (which already handles broad
   catches around `_async_update_data`). "It's not allowed to catch the bare exception
   outside the config flow." — edenhaus,
   https://github.com/home-assistant/core/pull/167872#discussion_r3064082478
2. **Never log-and-raise** (P2, MartinHjelmare's #1 correction). The exception carries the
   message; the handler decides whether to log. Don't put `_LOGGER.error(...)` immediately
   before `raise` in the same except block. "Don't both log and raise an exception. Let the
   handler of the exception decide" — MartinHjelmare,
   https://github.com/home-assistant/core/pull/152121#discussion_r2343364995
3. **Raise the correct HA exception with a translation key** (P3). A narrowed except that
   just re-raises the library error is only half the job — convert it: `UpdateFailed`
   /`ConfigEntryAuthFailed` in a coordinator, `ConfigEntryNotReady`/`ConfigEntryAuthFailed`
   in setup, `ServiceValidationError` (user error) / `HomeAssistantError` (device/API
   failure) in a service handler, with `translation_domain=`/`translation_key=`. "Raise
   `ServiceValidationError` here in the service action handler with a translated error
   message." — MartinHjelmare,
   https://github.com/home-assistant/core/pull/155465#discussion_r2797370954
4. **Only code that can raise goes in the try block** (PS1, joostlek). Assignments, returns,
   and pure logic move out — a fat try block hides which line the except actually guards.
   "Only have things in the try block that can raise" — joostlek,
   https://github.com/home-assistant/core/pull/152000#discussion_r2392011186
5. **Cover every error the code path can actually raise, and never the programmer-bug ones.**
   Narrowing that drops a real exception type is a behavioral regression; narrowing that
   includes `AttributeError`/`NameError`/`TypeError` from a genuine bug hides exactly what
   this skill surfaces (see the taxonomy for the dual-use exceptions).

## The core transform

```python
# Before — masks programmer bugs
def parse(body: str) -> Any:
    try:
        return json.loads(body)
    except Exception:
        return {}


# After — catches only what can actually fail here
def parse(body: str) -> Any:
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {}
```

In HA runtime code the narrowed except usually *raises the right thing* rather than returning
a fallback:

```python
async def _async_update_data(self) -> MyData:
    try:
        return await self.client.get_data()
    except MyAuthError as err:
        raise ConfigEntryAuthFailed from err  # P3 — triggers reauth
    except MyConnectionError as err:
        raise UpdateFailed(  # P3 — translated; base class logs once (P2, P12)
            translation_domain=DOMAIN, translation_key="update_failed"
        ) from err
```

## Workflow

The skill operates in three modes depending on scope:

1. **Single file** — `/ha:narrow-bare-except path/to/file.py`
2. **Directory** — `/ha:narrow-bare-except homeassistant/components/<domain>/`
3. **Whole project** — `/ha:narrow-bare-except --all`

Whatever the scope, follow this sequence.

### Step 1 — Find the sites

```bash
grep -rn "except Exception" <scope> | head -200
grep -rn "except\s*:" <scope> | head -200
grep -rn "except BaseException" <scope> | head -200
```

For each hit, read the surrounding lines to classify:

- `except:` / `except Exception:` / `except BaseException:` with no re-raise, in a normal
  runtime module — bare, needs narrowing
- The same in a **carve-out** (`config_flow.py`, a background-task wrapper, a top-level setup
  handler, or the coordinator base) — allowed by P1, skip (but still apply P2: no
  log-and-raise)
- `except SpecificError:` — already typed, skip
- `except (ErrorA, ErrorB) as err:` — already typed tuple, skip

### Step 2 — Determine the error set for each bare site

Read the `try` body and trace what each call can raise. Don't guess from the function name —
verify. Consult order:

1. **Check `${CLAUDE_SKILL_DIR}/references/taxonomy.md`** for the work type (JSON, device/API
   library, decimal math, file I/O, aiohttp, subprocess, voluptuous validation, etc.). Most
   sites map cleanly to one row.
2. **Grep the dependency's exceptions** when a library isn't in the taxonomy — the protocol
   library owns its exception hierarchy (P11):

   ```bash
   grep -rn "class .*Error" $(python -c "import mylib, os; print(os.path.dirname(mylib.__file__))")/*.py | head
   ```

3. **Check `raise` statements in the code path itself** — if the body explicitly raises a
   custom exception, include it.

Priorities: cover everything the code can actually raise, exclude programmer-bug exceptions
(Iron Law #5), and prefer specific types over `OSError`/`Exception`.

### Step 3 — Apply the narrowing (and raise the right HA exception)

Shrink the try block to only the raising line (PS1), name the exact exceptions, and re-raise
everything else. Where the block is in a coordinator/setup/service context, convert the
expected exception into the correct HA type with a translation key (P3) — never log-and-raise
(P2). For files with ≥3 except blocks sharing a taxonomy, hoist to a module-level tuple of
exception types — see `${CLAUDE_SKILL_DIR}/references/patterns.md`.

### Step 4 — Verify

After changes in each file (or cluster of files), run the dev loop in order:

```bash
ruff format <files_changed>
ruff check <files_changed> --fix
mypy homeassistant/components/<domain>/
pytest tests/components/<domain>/ --cov=homeassistant.components.<domain> --cov-report term-missing
```

`ruff check` catches typos in exception class names via `F821` (undefined name) and flags any
remaining blind excepts via `BLE001` (see `references/patterns.md` for enabling it as a
regression guard).

## Scope

This skill narrows bare `except` blocks. It does not:

- Auto-narrow blindly — behavior preservation matters; trace each call path first
- Touch already-narrowed excepts (`except SpecificError:`) — those are correct
- Touch the P1 carve-outs (config flow, background tasks, top-level setup, coordinator base) —
  a broad catch there is legitimate; only apply P2 (no log-and-raise) to them
- Restructure `try`/`except` into a result object or contextlib.suppress refactor — that's a
  larger change (see the `python-idioms` skill's error-handling guidance)

## References

- `${CLAUDE_SKILL_DIR}/references/taxonomy.md` — verified exception types per work category
  (JSON, device/API libraries, decimal, file I/O, aiohttp, subprocess, voluptuous, service
  schemas), plus the dual-use exceptions to trace before including
- `${CLAUDE_SKILL_DIR}/references/patterns.md` — special patterns: coordinator/setup/service
  re-raise (P2/P3), `errno` checks over broad file catches, exception-tuple hoisting for ≥3
  sites, partitioning large cleanups into separate PRs (PR1), the `BLE001` regression guard
- [Erlang Secure Coding Guide — LNG-002: Do Not Use `catch`](https://www.erlang.org/doc/system/secure_coding.html)
  — language-agnostic rationale for preferring narrow, typed error handling over the
  legacy catch-all form
