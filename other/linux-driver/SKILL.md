---
name: linux-driver
description: Apply the Linux driver's LuaJIT, evdev, ydotool, and tap-hold engine invariants. Use when writing, editing, or reviewing the Linux driver.
---

# Linux driver foot-guns

Universal code rules live in `AGENTS.md`; the strict convention lint is the
formatting authority. This file covers what has actually gone wrong, or is
provably wrong today, in the Linux driver.

**Rewritten 2026-08-06.** Every technical section of the previous version
described a defect that had since been fixed — the grab, the dead evdev decoder,
the missing ShellRunner, the race test's apostrophe hole, kanata's device flag.
A skill is loaded automatically and read as current, so a stale one is worse
than none: it sends the next reader to repair code that is already correct, and
its warnings argue against decisions the driver has since made deliberately.
Verify before you trust anything here, and rewrite it when you find it wrong.

## What still holds

### CI runs LuaJIT and exercises both event backends

`npm run test:linux` probes `luajit`, then `lua5.4`, then `lua`. Develop against
5.4 locally and you are not testing what gates the merge.

- **`utf8` is absent under LuaJIT.** `tests/run.lua` installs `compat.utf8`
  before any test module loads. Under 5.4 the shim is redundant, so a module
  that depends on its exact shape breaks only on LuaJIT.
- **No bitwise operators.** LuaJIT is 5.1-based; `&`, `<<` and `//` are 5.3+.
  `device_finder.lua` spells the EV_KEY bit test out arithmetically for exactly
  this reason. A `&` compiles fine on 5.4 and is a syntax error in CI.
- **`os.execute` return type.** 5.1/LuaJIT return a number, 5.2+ return `true`.
  Every call site must accept both (`result == true or result == 0`).
- **The unit lane installs `luv`** and admits its real event-loop and file-event
  integrations. Polling tests explicitly load the dependency as absent, so
  installed libraries cannot silently change the branch under test. **`lfs`
  remains optional**, so test discovery can still shell out.
- Plain `lua5.1` is not viable: `goto` is 5.2+.

### A `local` declared after the function that reads it is a nil global

The single most repeated defect in this driver — **five occurrences**, two of
them on 2026-08-06 alone. The function binds the nil GLOBAL instead of the
local, and the read silently does nothing: no error, no log, just a counter that
stays at zero or a state that never applies.

Declare module state in the state section at the top, above every reader. This
has its own entry in `docs/memory/linux-web-release.md`
(`project-lua-closure-before-local-nil-global`).

### A value must be named at EVERY boundary it crosses

Nine defects in one session had one shape: a value computed correctly and lost
at a boundary that drops whatever it does not name by hand — the writer's
`allowed` set, `get_app_stats`'s projection, the reader's code-to-table map, an
i18n envelope. Nothing errors; the symptom is a panel of zeroes, which reads as
"nobody uses this feature".

When adding a value that must reach the database or a page, grep the whole path
for anything that ENUMERATES fields and add it to every one. Then test the
join, not the units: this driver has shipped a walk and a writer that were each
correct in isolation while the flush called neither.

### Writing a table nobody reads is the same blank panel as not writing it

Both halves land in the same change, or the second half looks like the first
half not working. The same rule applies to adapters: `adapters/notifier.lua` was
deleted once under ADR-008 for having no callers — the file made the port matrix
answer "does Linux notify?" affirmatively by inspection while the practical
answer was no.

### Hardware is still unverified in CI

The Linux e2e job is stubbed — no real evdev, no real ydotool. `EVIOCGRAB` and a
ydotool injection have never run in this repo's CI. Treat every runtime claim as
verified by reading, and validate on real hardware before shipping.

`tests/hardware/` exists for exactly this and is the right home for anything a
runner cannot answer.

## What was fixed, so you do not go looking

- **The grab.** `--grab` is now the DEFAULT (`opts.grab = true`); `--no-grab` is
  the escape hatch. `get_mode()` returns `"intercept"` in production. The old
  warning that turning it on "makes normal typing vanish entirely" is obsolete —
  the pass-through was built.
- **The evdev struct decoder.** `M.new`, `parse_event` and the byte-order
  helpers were dead code with a test that asserted nothing. Both are gone;
  `input_reader` now exports `get_layouts` and `resolve_char` only.
- **`adapters/shell_runner.lua` exists.** New shell-outs go through it. There
  are still ~150 direct `io.popen`/`os.execute` sites outside it; migrating one
  is welcome, re-deriving quoting at a new site is not.
- **The race test's apostrophe hole.** It has a case named "types an apostrophe
  like any other character".
- **kanata is gone (2026-09-24).** The tap-holds and the navigation layer
  used to run in kanata, which needed a newer glibc than Debian 12 and Ubuntu
  22.04 ship, was never started by the daemon, and broke its whole config on
  the first free-text action. Its generator, golden file, `kanata.kbd`, the
  kanata submenu and the parity gate are deleted. `device_finder` no longer
  prefers a remap daemon's output; it still drops `/devices/virtual/` so the
  daemon cannot read its own uinput device back.

## Tap-holds run in the daemon (`platform/remap/`)

- **`tap_hold_engine.lua`** is pure: evdev events in, events out, with the
  Windows semantics (hold taken at key-down; a tap only within the key's
  threshold, no sooner than the minimum tap duration, with no other key
  pressed, repeated or released, no click and no wheel in between). Keep it
  free of I/O so it stays testable. Time reaches it only through `tick(now)`:
  RCtrl's one-shot Shift is held only past its threshold, as on Windows, so
  the keyboard hook ticks it before each key event, at that event's stamp,
  and from its pump once every queued event is dispatched, on an estimate of
  the events' clock that must never run ahead (the kernel stamps on the wall
  clock, and without luv the daemon's clock counts whole seconds). While a
  key holds the layer no other key is a tap-hold, as no Windows one is: each
  is the layer's key, itself, or nothing for LAlt tapping Backspace. Per-key
  Windows rules (a tap with no hold, the Backspace logic of LAlt and RCtrl)
  are tables in the engine, each citing its `.ahk` block. The minimum tap
  duration applies to every tap that waits for its release; Windows checks
  it only for LShift, LCtrl, RShift, CapsLock holding the layer and LAlt
  holding it with a tap other than Backspace. That difference is known and
  not yet decided: do not copy either side to the other without the
  maintainer.
- **`tap_hold_loader.lua`** lays the user's `tap_hold.toml` over
  `_shared/tap_hold/defaults.toml` key by key and field by field, but only
  when the file says `inherit_defaults = true`; otherwise it starts from no
  keys, so an empty file is the keyboard's own behaviour.
  A hold modifier drops the default layer and the reverse; `tap_action = ""`
  is the native key and `"none"` swallows it; a malformed user file is
  reported, never half-applied.
- **`tap_hold_writer.lua`** writes only the keys the user changed, through the
  shared TOML codec, via temp file then rename, and refuses to overwrite a file
  that does not parse. Then it reloads the manager. The section-wide restore
  and clear are not writer commands: `infra/tap_hold_scope.lua` renders them
  through `render_scope()` (the preset written explicitly, never inherited)
  and publishes both files in the shared scope transaction.
- **`tap_hold_manager.lua`** is the single owner of "is a tap-hold active":
  the feature switch, the file's `enabled` flag and the daemon's pause meet
  in one place. It installs the engine only through
  `keyboard_hook.set_remapper()`, which releases everything the previous
  engine held before swapping — so switching off, pausing, reloading or
  stopping while CapsLock is down cannot leave Ctrl pressed. Never hand the
  hook an engine any other way.
