---
name: ahk-driver
description: Apply the Windows driver's AutoHotkey v2 invariants. Use when writing, editing, or reviewing any .ahk file.
---

# AutoHotkey v2 foot-guns

Universal code rules live in `AGENTS.md`; the strict convention lint is the
formatting authority. This skill covers only the language semantics that have
caused real bugs here — every item below is a bug we actually shipped.

## Encoding — non-negotiable

Every `.ahk` file is **UTF-8 with BOM + LF**. Never write one with a tool that
strips the BOM or rewrites line endings (`cat >>`, some shell redirects).
Verify with `npm run test:ahk-encoding`.

Failure signature: a mid-file parse abort. The runner exits with **no results
file at all**, which reads as "the tests vanished" rather than "the tests
failed". If a suite produces nothing, suspect encoding first.

## The escape character is the backtick, not the backslash

Inside a double-quoted string, a literal quote is `` `" ``. **`\"` is invalid**
and aborts the parse with the same silent signature as above. `""` is AHK v1
syntax and is also wrong.

Simplest defence when embedding quotes: use a single-quoted AHK string.

```ahk
Assert(InStr(Src, 'Features["hotstrings"]') > 0, "…")   ; clean
```

## `Map[missing_key]` throws

Reading an absent key raises. Any lookup on a key that is not guaranteed present
must use `.Get(key, default)` or be guarded by `.Has(key)`.

```ahk
if (!Features.Has(id))          ; guard
Features["x"].Get(id, false)    ; or default
```

This was the single most common finding class in the 2026-07-20 audit (F43 alone
covered 30 leaf reads).

## `IsSet()` before dereferencing a pre-pump global

Globals seeded in `ErgoptiPlus.ahk`'s pre-pump block do not exist yet during
early boot, and **never exist at all under the headless test harness**, which
loads `lib/` and `adapters/` but not `ErgoptiPlus.ahk`.

```ahk
if !IsSet(Features)
    return false
```

When you add a pre-pump global that library code reads, mirror it in
`tests/test_stubs.ahk` — otherwise you break the suite with an unset-global error
far from your change. (This is exactly how F14 broke 10 hotstring tests.)

## `#Include` executes top-level globals at its include position

A file's top-level `global X := …` runs **where the `#Include` sits** in the
auto-execute flow, not at first use. So a sentinel-seeding file included _after_
the loader that fills those values will silently re-zero them on every boot.

Order matters: constants/sentinels first, loaders after. `#Include` also dedupes
by resolved path, so a second include is a no-op, not a re-run.

## `::` hotkeys register at LOAD time

Wrapping a hotkey definition in a runtime `if` is **dead decoration** — the
hotkey registers unconditionally regardless of the condition.

```ahk
; WRONG — registers always
if (Cond) {
    SC11D & SC038:: DoThing()
}

; RIGHT — #HotIf is re-evaluated live on every press
#HotIf Cond
SC11D & SC038:: DoThing()
#HotIf
```

## `Suspend()` only disarms hotkeys

InputHook callbacks, `SetTimer` ticks and `OnMessage` handlers keep firing while
suspended. Every one of those paths needs an explicit `A_IsSuspended` guard, or
the driver keeps acting while the user believes it is paused.

See `project-suspend-pause-invariant` in `docs/memory/windows-ahk.md`.

## Other traps

- **`"0" = false` is TRUE.** Never compare a `String|false` return against
  `false`; type-check with `is String`.
- **`Critical()` is thread-scoped.** Safe in production hotkey callbacks, but it
  leaks into the main thread when a test calls the function directly, silently
  hanging background timers. Do not wrap file I/O or menu rebuilds in it.
- **Never swallow errors.** `try … catch` with an empty body violates the
  fail-fast contract in `AGENTS.md`. Log via the project logger (see the
  `logger` skill) or let it propagate to the global `OnError` handler.

## Guard the whole class

Per `project-ahk-invariant-incomplete-application` in
`docs/memory/windows-ahk.md`, the
recurring failure here is not the missing guard — it is the ONE sibling site that
was missed. When you fix one of the above, grep for every other occurrence of the
same pattern and fix them together.
