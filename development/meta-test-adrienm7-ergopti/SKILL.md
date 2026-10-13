---
name: meta-test
description: Write resilient AHK tests that inspect driver source. Use when a test scans source instead of calling behavior directly.
---

# Writing source-scanning meta-tests

Meta-tests live in `static/ergopti_plus/windows/tests/meta/` and assert
structural invariants — "this hotkey is gated by `#HotIf`", "this constant is
included before that loader" — that no runtime call can check.

## Always read source through the helpers

Defined in `tests/test_framework.ahk`:

| Helper                        | Returns                                    |
| ----------------------------- | ------------------------------------------ |
| `_DriverSourceConcat()`       | the whole driver source, concatenated      |
| `_DriverSourceNoComments()`   | same, with comments stripped               |
| `_DriverFuncBody(Name)`       | one function's body                        |
| `_DriverDirConcat(RelDir)`    | every file under one directory             |
| `_StripFullLineComments(Src)` | comment-stripped copy of any source string |

**Never hardcode a path like `"platform/remap/lalt.ahk"`.** A CI ratchet
(`tools/test/test-no-pinned-source-reads.cjs`) fails the build when the count of
location-pinned reads rises above `BASELINE = 20`.

**Never raise that baseline to make a change pass** — convert the test to a
helper read instead. Raising it is the ratchet equivalent of weakening a test.

Why this works: each file's content is contiguous inside the concatenation, so
relative order and "nearest preceding `#HotIf`" assertions stay valid even after
the file is moved or renamed. State that reasoning in a comment — it is not
obvious to the next reader.

## The same rule on macOS — and it is automated

Lua tests use `helpers.read_driver_source(symbol)`, never
`helpers.driver_root() .. "modules/foo/bar.lua"`. The twin ratchet is
`tools/test/test-no-pinned-source-reads-lua.cjs`.

You should not have to think about this: **the pre-commit hook blocks a staged
Lua test that introduces a pinned read**, and `npm run fix:pinned-reads`
converts it for you. `npm run lint:pinned-reads` surveys the whole tree.

The one thing the fixer will not do for you is guess. `read_driver_source`
returns _every_ production file containing the symbol, concatenated — so a
selector matching two files changes what a position-comparing assertion means,
silently. The fixer therefore proves a candidate declaration is unique across
the production tree before using it, and refuses when none is
(`_on_config_changed` is assigned in two files — a real case). When it refuses,
make the assertion order-independent first, then convert by hand.

## Trap 1 — comments shift your positions

A **comment** containing the token you scan for silently breaks naive `InStr`
position assertions. Your own module header describing `Bundle_Init()` becomes
the first match, and the test asserts about prose instead of code.

Defences, in order of preference:

1. Scan `_DriverSourceNoComments()` / `_StripFullLineComments(...)`.
2. Reword the comment so it does not contain the literal token.

This trap cost three separate red runs during the 2026-07-20 fix campaign.

## Trap 2 — quotes and escapes

See the `ahk-driver` skill: the escape is the backtick, `\"` aborts the parse
with no results file. Prefer single-quoted AHK strings when the assertion needs
to embed quotes.

## Trap 3 — zero-width regex matches

A regex that can match empty backtracks to zero width and makes a lookahead pass
spuriously. When asserting "every X is followed by Y", prefer **counting both
sides and comparing** over one clever pattern:

```ahk
; robust: pairing by count, not by lookahead
AssertEqual(CountOccurrences(Src, "try TapHoldTrack"),
            CountOccurrences(Src, "HookDispatcher._TrackFault("),
            "every tracked call must route failures through _TrackFault")
```

## Registration

`tests/run_all.ahk` uses one explicit `#Include` per test file — adding a file to
the directory is **not** enough. Add its `#Include` or the test never runs, and a
"passing" suite proves nothing about your fix.

## Structure

```ahk
_XYZ_MyInvariant() {
    Src := _DriverSourceConcat()
    Assert(Src != "", "driver source must be readable for the XYZ meta-test")
    ; … assertions …
}
Test("area: human-readable invariant description", _XYZ_MyInvariant)
```

The module header must explain the **mechanism** the test protects and cite the
finding it came from — a bare assertion with no rationale gets deleted by the
next person who trips over it.

Assertions available: `Assert`, `AssertEqual`, `AssertTrue`, `AssertFalse`,
`AssertContains`, `AssertThrows`.
