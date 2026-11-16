---
name: exception-catalog
description: Use when adding an error class or reusing one, or translating an SDK or library exception at a boundary. Owns the single catalog file, its root and bare subclasses, the stable codes, the inherited `context` dict, translation with `from exc`, the ban on swallowing a failure, best-effort compensation as the one case a scope that re-raises stops a second failure, and a failure after a committed write, which is stopped rather than re-raised. The status a transport answers with is mapped at that transport's boundary, never carried by the class; where the error is logged is `python-logging`.
---

# Exception Catalog

Every project in this style has **exactly one file** where its own exceptions are defined. It holds a
root error plus one bare subclass per named error, so the catalog stays auditable in a single read and
nothing raises a type that was invented at the call site.

Where that file sits is the only thing that varies, and one obligation settles it for any project
shape: **one catalog module, at a place every part of the codebase may import from without creating a
cycle, named for what it holds.** The catalog imports nothing of the project's own, so anything may
import it; put it wherever the project's own import direction makes that true. It is a module,
`exceptions.py` — never `exceptions/__init__.py`, because an `__init__.py` holds only imports and
`__all__` (`python-packaging`); `from myapp.exceptions import …` reads the same either way. The root
class is named for the project, and every other class in the file descends from it.

Where an architecture family fixes that place — `hex-architecture`, in the `pyhouse-hex` plugin, or
`flat-layered`, in the `pyhouse-flat` plugin — follow it; otherwise the obligation decides: a
framework-shaped tree puts the module where every one of the framework's units already imports from,
a distributable package puts it at its own root because the classes its callers catch are part of the
published surface, and a command-line tool puts it above the command modules that raise from it. One
file either way — the reason for a single file is that the catalog stays auditable in one read, and
that reason is not architectural.

The **shape** below is identical in every case: **`code` and the inherited `context` are the whole
shape** — the catalogue knows no transport (rules 6 and 13).

## When to use vs. neighbours

- A new named error is needed to express a rule violation → this skill. **First confirm no existing class
  already serves the rule** — scan `__all__` for a semantic match and read the candidate's body; if one
  fits, reuse it rather than minting a near-duplicate.
- Where a database driver's error is translated, and the field and constraint name its context
  carries → `persistence`; the translator itself is the family's data-access skill's —
  `hex-persistence`, in the `pyhouse-hex` plugin, or `flat-persistence`, in the `pyhouse-flat`
  plugin — which references this skill for the target class name, or, with no family installed, the
  project's own data-access code, under this skill's rules 8–11.
- Translating an HTTP or SDK error inside a client class → this skill's rules 8–10; the client class
  itself is the family's — `flat-layered`, in the `pyhouse-flat` plugin, or `hex-capability-adapter`, in
  the `pyhouse-hex` plugin — or the project's own layout.
- The status a new class answers with on an HTTP route, and advertising it → the boundary's map
  (`hex-restapi-app`, then `hex-restapi-endpoint`, in the `pyhouse-hex` plugin; `flat-entrypoint`'s
  `HTTP.md`, in `pyhouse-flat`).
- Where the error is logged and by whom → `python-logging`.
- The exit code a class answers with on a command line → `python-cli`'s map.
- Whether an undo step's own failure may be stopped while another failure propagates, or a failure
  after a committed write → this skill, **Swallowing, stopping, and best-effort compensation**; the
  handler shape that does either is the architecture family's (`hex-application`, in the `pyhouse-hex`
  plugin, is one).
- Why this one file is exempt from one-class-per-module → `python-packaging`.
- What the error class itself should be called → `naming`.
- Rendering a caught error as an HTTP response body, and the central handler that does it → `hex-restapi-app`, in the `pyhouse-hex` plugin, or `flat-entrypoint`'s HTTP shape, in the `pyhouse-flat` plugin; this skill owns the class and its `code`, not the rendering and not the status a transport maps it to.

## File shape (the contract every entry obeys)

- `__all__` **after the imports**, alphabetized — `python-packaging` owns module layout and forbids
  `__all__` above the imports. This file is stdlib-only and has no imports, so it opens the file;
  that is the same rule, not an exception to it.
- The **root** defines `code: str` with its annotation and default, plus the `__init__` accepting
  `(message, context=None)` and storing `self.context`.
- Every subclass declares its attributes as **bare class attributes**, no type annotation; the type is
  inherited from the root's annotation.
- **No subclass overrides `__init__`.** Every subclass automatically accepts `(message, context=None)`.
- A subclass may inherit from another subclass when it is a genuine refinement, in which case it inherits
  the parent's values unless it overrides them.
- Order: `__all__`, then the root, then direct subclasses, then refinements.

## Template — stdlib exceptions

In `myapp/exceptions.py`:

```python
__all__ = [
    "MyappError",
    "NotFoundError",  # only where a lookup can miss
    "UpstreamError",  # only where the project calls an external system
]


class MyappError(Exception):
    code: str = "MYAPP_ERROR"

    def __init__(self, message: str, context: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.context: dict[str, object] = context if context is not None else {}


class NotFoundError(MyappError):  # only where a lookup can miss
    code = "NOT_FOUND"


class UpstreamError(MyappError):  # only where the project calls an external system
    code = "UPSTREAM_ERROR"
```

That is the entire class body of each entry. No `__init__`, no fields, no methods.

### A custom subclass and its raise site

Each named error is a bare subclass of the root — or of the most specific existing parent, when one is
a semantic match (a refinement inherits every value it does not override):

```python
class FooNotFoundError(NotFoundError):
    code = "FOO_NOT_FOUND"
```

Custom exceptions still carry `context`. The raise site passes a `context` dict whose keys express the
structured detail:

```python
raise FooNotFoundError("foo not found", {"foo_id": str(foo_id)})
```

### What `context` carries

`context` is not a free-form debug bag. It carries the **stable identifying inputs of the failed
operation** — the id, key or field the operation was about — plus the upstream code or status where the
failure came from one, and nothing else. Two readers depend on that set: the test at the raise site
asserts on the keys, and the layer that logs the error renders them as its fields, so a key that churns
breaks a test and a dashboard at once.

Three consequences:

- **The raise site and its test agree on one key set**, and that set is as stable as the `code` beside
  it. Renaming a key is the same class of change as renaming the `code`.
- **A key names the input or the upstream's own code, never prose about the failure.**
  `{"foo_name": foo.name}` — not `{"detail": "..."}`, `{"msg": "..."}` or a stringified exception.
- **No secret goes in `context`.** A password, token, key or connection string placed there reaches the
  log line and, where the project renders errors, the response body — by construction, because both
  render `context` verbatim. This is the same ban `python-logging` states for a log line, and `context` is
  the path around it.

The skill does not enumerate the keys for each class; it fixes what kind of key belongs there and that
the set does not drift.

## Translation at the boundary

A library or SDK exception must not escape the module that called the library. The boundary catches it,
raises the catalog's own type, and **chains the cause**:

```python
try:
    response = await http.get(url)
    response.raise_for_status()
except httpx2.HTTPError as exc:
    raise UpstreamError(f"failed to fetch foo {foo_id}", {"foo_id": str(foo_id)}) from exc
```

`from exc` is not optional. It preserves `__cause__`, which is what a test asserts to prove the
translation happened rather than the error being manufactured, and what a reader needs to see the real
failure. Suppress it deliberately with `from None` only when the internal cause must not leak — for
instance turning a lookup miss into an authentication failure.

Structured detail rides in `context`, not in new fields, under the key contract above.

### The fallback is mandatory

A translation that recognises some failures must still answer for the ones it does not. When no case
matches, the boundary **still raises a catalogue class** — the generic upstream or client error, chosen
by what the failure is rather than by what was matched:

```python
except QuxSdkError as exc:
    if exc.status == 404:
        raise NotFoundError("foo not found", {"foo_id": str(foo_id)}) from exc
    raise UpstreamError("qux service failed", {"foo_id": str(foo_id), "status": exc.status}) from exc
```

Never return the raw exception, never re-raise it unchanged, and never swallow it with `pass` or a bare
`return None`. An untranslated leak is the failure this whole skill exists to prevent, and it is worse
than the original error: a third-party type crossing a layer defeats every `except` clause written
against the catalogue, so a recognisable conflict is rendered as an unexplained crash and a swallowed
one becomes a silent wrong answer.

### Swallowing, stopping, and best-effort compensation

**To swallow a failure is to catch it and neither re-raise it nor log it as the scope that stops it.**
A swallowed failure leaves no trace: nothing above sees it and nothing records it, so the operation
reads as a success it was not. It is never done. **Stopping a failure is different and legitimate** —
the scope that catches it, logs it once under `python-logging`'s allocation and carries on (a loop
containing one failed run and moving to the next) is the scope every failure is traced to, and it is
exactly where the log line belongs.

**Best-effort compensation is the one case where a scope that re-raises also stops a failure.** A scope
that has already caused an externally visible effect — an object uploaded, a message published, a
reservation taken — and then fails on a later step undoes the effect before letting the failure go. The
undo runs **while that failure is already propagating**, and it can fail too. Letting the undo's error
escape would replace the fault that actually happened with a report about the cleanup, so **the undo's
own failure is stopped in the scope that re-raises the original, on three conditions, all required**:

1. **It is stopped only by the scope that caught the original failure and will re-raise it** — the
   only scope that knows a failure is propagating. The undo it calls raises like any other call; a
   method that drops its own failure in case some caller is compensating hides it from every caller
   that is not.
2. **That scope logs the undo's failure once** — the only record that an effect outlived the operation
   that made it. The event's level, fields and shape are `python-logging`'s (**A failed undo under
   compensation**).
3. **The original failure is re-raised unchanged**, and only the undo call sits inside the inner
   `try` — never the original operation, and never a bare `except: pass`.

**A failure after a committed write is stopped rather than re-raised, where the effect is not part of
what the operation changed** — a notification, a publish, disposing of what the write replaced. Raised,
it tells the caller a change that happened did not, and the caller's retry repeats it or conflicts. The
scope stops the effect's failure and logs it once, or hands the effect to something that retries it,
and a hand-off made after the write is held to the same rule. A task started and never awaited is not a
hand-off; it swallows its failure. An effect that must not be lost does not run after the write: it is
recorded atomically with the write and delivered by something that retries it, under
`at-least-once-delivery` rule 6. An operation idempotent under redelivery may instead fail whole; its
redelivery is the hand-off that reruns the effect. A second store's write that is part of what the
operation changed is not such an effect: it is made whole under `persistence` rule 3, and its failure
propagates.

Everywhere else a failure a scope catches is re-raised, translated, or stopped and logged by the scope
that stops it — never dropped. A translation's unmatched branch raises; it does not get to stop anything.

## Rules

1. **Never define an exception outside the catalog file.** Not beside the code that raises it, not in a
   client module, not in a test helper. New classes are added to the catalog or not at all. There is
   one catalog, the module `exceptions.py` — never `exceptions/__init__.py`, which holds only imports
   and `__all__` — placed where every part of the codebase may import it; a package that cannot import
   it is answered by moving the one file, never by adding a second.
2. **Never inherit from bare `Exception` or a stdlib exception** except for the root itself. Everything
   else inherits from the root or one of its subclasses.
3. **`code` is a stable contract.** Once shipped, never rename or reassign one — clients, dashboards and
   alerts key on it. If the meaning changes, add a new class with a new code and deprecate the old one
   separately.
4. **Subclasses do not override `__init__` or add fields.** Structured detail goes through the inherited
   `context` dict at the raise site.
5. **Subclass attributes use bare assignment.** `code = "X"`, not `code: str = "X"`.
6. **The catalogue carries no transport's outcome.** A status, an exit code or any other outcome is
   mapped from the class at the boundary that speaks that transport, so a second transport adds a
   second map rather than a second field on every class.
7. **`code` values are `SCREAMING_SNAKE_CASE`**, and every one is unique across the catalog.
8. **Every library exception is translated at its boundary, with `from exc`.** A third-party type
   escaping the module that called the library is a leak, and a translation without `from exc` loses
   the cause and becomes unprovable.
9. **Prefer the most specific existing class.** A refinement beats its parent; a near-duplicate of an
   existing class is a reuse, not a new entry.
10. **The fallback is mandatory.** A translation that matches some failures still raises a catalogue
    class for the ones it does not — never the raw exception returned or re-raised, never a `pass`. A
    partial translation is an untranslated leak with extra steps.
11. **`context` carries the operation's stable identifying inputs**, plus the upstream code or status
    where there is one — never the library exception's class name, which names the dependency rather
    than the failure and changes when it does. The raise site and its test agree on that key set and it does not churn, because
    the test asserts on it and the layer that logs the error renders it as fields.
12. **No secret in `context`.** A token, key, password or connection string placed there reaches the log
    line, and the response body where the project renders one, by construction — both render `context`
    verbatim. `python-logging` bans the same values from a log line; this is the path around it.
13. **A caught error is rendered in exactly one place, off the exception's own attributes.** Whatever
    the project shows the outside world — a response body, a message on stderr and an exit code, a
    failure record — one scope produces it, reading the body off `code`, `str(exc)` and `context`, so a
    new class renders correctly the day it is added. The transport's outcome is the one thing that scope
    maps from the class, through the class's ancestry to its nearest mapped parent and else to the
    root's outcome, so a new refinement answers as its parent until it is mapped itself. Where the entrypoint
    serves HTTP that scope is a central handler — `hex-restapi-app`, in the `pyhouse-hex` plugin, and
    `flat-entrypoint`'s `HTTP.md`, in the `pyhouse-flat` plugin, are examples. A library renders nothing
    and lets the class reach its importer intact.
14. **Where the project verifies its caller's credential, one class covers every credential rejection**
    — bad, missing, expired or unverifiable (`UnauthorizedError`) — and a second covers a known caller
    who is not permitted (`ForbiddenError`); never a parallel class for either. A dependency rejecting the project's own credential is an
    upstream failure and is translated as one. A project that verifies nobody has neither class.
15. **A failure is never swallowed** — caught and dropped (`pass`, a bare `return`, a default value)
    with neither a re-raise nor a log line from the scope that stops it; it reads as a success. A caught
    failure is re-raised, translated, or stopped and logged once, and a failure of an effect after a
    committed write, outside what the operation changed, is stopped and logged or handed to something
    that retries it — re-raised only where the operation is idempotent under redelivery
    (`at-least-once-delivery`). Best-effort compensation is the one case where a scope that re-raises
    also stops a failure, on the three conditions in **Swallowing,
    stopping, and best-effort compensation**: the undo's failure is stopped by the scope that caught the
    original, never inside the undo method in case a caller is compensating, and never raised in place
    of the original. Never a bare `except: pass`.

## Inlined typing / import rules

- Stdlib-only in the catalog — no third-party imports. No `from __future__ import annotations`.
- The root's class attributes carry annotations; subclasses do not re-annotate.
- The root's `__init__` is fully annotated, including `-> None`.
- `context` is `dict[str, object]`, not `dict[str, Any]` — `object` forces narrowing at the point of
  consumption (`python-style`).

## Hard stops

- Translating a database driver's error at a repository boundary → stop, use `persistence` for where
  it binds and what its context carries, and the family's data-access skill for the translator
  (`hex-persistence`, in `pyhouse-hex`, or `flat-persistence`, in `pyhouse-flat`), or, with no family
  installed, the project's own data-access code, under this skill's rules 8–11; they name the target
  class from here.
- Rendering a caught error as an HTTP response, or writing the central HTTP handler → stop, use
  `hex-restapi-app` (in `pyhouse-hex`) or `flat-entrypoint`'s HTTP shape (in `pyhouse-flat`). Any other
  transport's rendering and outcome map follow rule 13 here.
- Deciding where an error is logged and by whom → stop, use `python-logging`.
- Choosing what an error class is called → stop, use `naming`.
