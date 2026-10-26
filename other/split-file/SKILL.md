---
name: split-file
description: Break a file over 800 lines into a package directory without changing its import path. Use when the LOC gate flags a file, when asked to "split this up", "break this file down", or when a module has become hard to navigate.
---

# Splitting a big file

Full rationale in `docs/system/rules/70-file-organisation.md`. This is the procedure.

## The decision, already made

A file that outgrows 800 lines becomes **a package directory in the same
place, keeping its import path**:

```
frontend/pages/trading.py          →   frontend/pages/trading/
                                           __init__.py     render() only
                                           _open_trades.py
                                           _signals.py
                                           _manual_order.py
```

`from frontend.pages.trading import render` keeps working. No caller, test or
route registration changes.

**Not** sibling files (`trading_signals.py` next to `trading.py`) — that is
what produced 60+ flat `core_*.py` files in the old layout, whose
relationships you could only learn by reading all of them.

## Before you touch anything: is it tested?

**A split is only safe when tests can tell you it worked.**

If the file has no tests, **writing them is the task** — say so and stop.
`backend/src/controllers/remote/` (2,116 lines of token issuance and admin
authority) is the live example: it has zero tests, so it is explicitly not to
be split until it has some. The line ceiling does not outrank "can we tell if
this broke".

## Check for module-level state

```bash
grep -n "^\s*global " <file>
```

If the file rebinds a module global, splitting **forks that state** — each
module gets its own copy and writes land in the wrong one. Either move the
state into a small state module both halves import, or do not split.

## Procedure

**1. Convert to a package. Commit this alone.**

```bash
mkdir frontend/pages/trading
git mv frontend/pages/trading.py frontend/pages/trading/__init__.py
pytest tests/ -q
git commit -m "frontend/pages/trading: convert to a package (pure move)"
```

A pure move is recorded by git as a rename, so the next diff is readable.

**2. Move one section per commit.**

Pick seams by cohesion, not line count. If you cannot name the section in
three words, it is not a section. Prefix files with `_` — they are internals
of the package, not public API.

```bash
pytest tests/ -q      # after EVERY section, not at the end
```

**3. Keep `__init__.py` to the public name.**

For a page that is `render()`. Anything a sibling section needs gets imported
explicitly — never re-exported "just in case", which is how a package's
surface silently becomes everything it contains.

**4. Verify.**

```bash
python -m tools.checks all
```

The check that matters most for a split is **undefined names**. Moving code
verbatim moves its *body*, not the module-level constants and imports it reads.
Those stay behind, and nothing fails until that exact line runs — see
`docs/todo/bugs/018`, where four cluster splits left 15 names behind and the
suite stayed green for two days. To run it alone:

```bash
python -m tools.refactor_audit.undefined_names backend frontend tools
```

The LOC gate should now show one fewer oversized file. If it shows the same
count, the split did not actually reduce anything and you have added
directories for nothing.

## Do not

- bundle a split with a behaviour change — if it breaks you cannot tell which
  half did it
- split a file you cannot test
- "improve" code while moving it. Move first, verified. Improve after, with
  its own tests.

## Current queue

**Measured 2026-09-01.** Three files in the tree exceed 800 lines, and two are
permanently exempt:

| File | Lines | |
|---|---|---|
| `backend/src/runtime.py` | 1,507 | exempt — at its design floor |
| `mt5_bridge.py` | 1,344 | exempt — separate interpreter |
| `backend/src/services/cluster/remote/server.py` | 1,204 | the only one left |

Everything the old version of this list named is done. `frontend/pages/trading.py`,
`settings.py`, `app.py` and `history.py` are all packages, and no file under
`frontend/` exceeds 800 lines. `backend/src/controllers/remote/` and
`controllers/sync/` do not exist.

`cluster/remote/server.py` is **not** blocked on tests any more — it is at 64%
coverage and its connection front door is tested
(`tests/remote/test_connection_auth.py`). It is blocked on the "check for
module-level state" step above: it rebinds six sets of globals and five test
files patch that state, so a split would fork it. Move the state into one
module both halves import, with its own tests, before moving any code.

See `docs/system/rules/70-file-organisation.md` for the full status.
