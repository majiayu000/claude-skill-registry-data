---
name: hammerspoon-driver
description: Apply the macOS driver's Hammerspoon and Lua invariants. Use when writing, editing, or reviewing Lua under macos/.
---

# Hammerspoon driver foot-guns

Universal code rules live in `AGENTS.md`; the strict convention lint is the
formatting authority. This skill covers only the Hammerspoon and Lua semantics
that have actually broken this driver — every item below is a bug we shipped,
and most of them shipped **green**.

The unit suite never loads `init.lua` (running it needs a live Hammerspoon), so
boot-path logic is only reachable through static source tests — that is why so
many guards here are meta-tests rather than behavioural ones
(`tests/meta/test_lua_sources_compile.lua` exists because a stray `end` in
`init.lua` shipped with CI green).

## An unpinned `hs.task` is collected, SIGTERMed, and never calls back

An `hs.task` held only by a local is garbage-collected the moment the enclosing
function returns. Hammerspoon translates that collection into a signal to the
subprocess, so the process dies mid-run and **its completion callback never
fires**. Nothing is logged, nothing throws: whatever the task was supposed to
finish simply never happens.

Every call site must pin the task in a long-lived table before `:start()` and
release it inside the callback. The canonical root is `M._active_tasks`
(`adapters/shell_runner.lua:33`, pinned at `:194`, released at `:143`); a child
module may pin into a root injected by its parent (`active_tasks_gc_root`,
`ui/menu/menu_llm/models_manager_mlx.lua:213`).

**The broad guard is file-granular, not call-site-granular.**
`tests/unit/meta/test_gc_retention.lua` walks every driver `.lua` and only asks
whether a file that constructs a task contains an ownership spelling. One
pinned task can therefore mask an unpinned sibling. The historical
`models_manager_mlx.check_task` defect is fixed and now has a dedicated guard in
`test_fresh_regressions_2026_07_21.lua`; do not report it as live. Still inspect
every construction/start/callback/teardown chain individually.

## `local x` declared AFTER the closure that uses it binds the nil global

In Lua a `local`'s scope starts _after_ its declaration statement. A closure
written above the `local` does not capture it as an upvalue — the name resolves
to `_G.x`, i.e. `nil`. The code reads perfectly; at call time the value is nil.

The recurring shape is the `hs.task` GC pin, because the callback needs the very
handle the constructor is returning:

```lua
-- WRONG — `task` inside the callback is the nil global
local task = hs.task.new(bin, function() _active_tasks[task] = nil end, args)

-- RIGHT — forward-declare, then assign
local task
task = hs.task.new(bin, function()
    if task then _active_tasks[task] = nil end   -- nil-guard: _active_tasks[nil] raises
end, args)
```

Both halves matter. Without the split you get `nil`; without `if task then` you
get `table index is nil` thrown _inside_ an async callback, where it is
invisible (next section). `platform/remap/watchers.lua:148-149` is the
reference shape.

This has bitten three times and one 2026-06-20 pass fixed **nine** sites at once,
so treat any new one as wrong until you have checked the declaration order.
Regression tests for this class must compare **source indices** (`src:find("local
task") < src:find("hs.task.new")`), never merely assert that the using line
exists — a grep-shaped test stayed green over the live bug.

## The `hs.` purity ratchet counts comments — a docstring can fail CI

`tests/meta/test_port_adapter_coverage.lua` counts every **line** matching
`%f[%w]hs%.` (and `io.open` / `os.execute`) across `macos/modules/` and
`macos/lib/` only — `adapters/`, `ui/` and root `init.lua` are outside the scan —
and fails if the total rises above a baseline. It is a raw line scan with **no
comment stripping** (`:337-358`), so a docstring that names `hs.timer.new`
increments the counter exactly like a real call.

Two consequences:

- Moving OS-calling code from `ui/` into `modules/` raises the count without
  adding a single OS call. So does documenting a foot-gun.
- **Never quote the baselines from memory.** Read `LUA_HS_BASELINE` and
  `LUA_IO_OS_BASELINE` at `:247-248`; they move on nearly every pass and a stale
  number sends people chasing a delta that does not exist.

Prefer routing the call through an adapter and naming the _adapter_ in the
comment. If a comment genuinely must name the `hs.` API, bump the baseline **with
a note saying it is a comment, not a call**, and prove it with
`git diff -- modules lib`. Never bump silently.

Corollary: `adapters/` is the OS-isolation layer, not "exactly the 20 ports".
Relocating `shell_runner` / `toml_cache` / `json_codec` into `lib/` for folder
parity with Windows spikes both counters and is rejected by this ratchet.

## Errors thrown inside async callbacks vanish

A throw inside an `hs.timer` callback is swallowed whole by Hammerspoon's
runloop; a throw inside an `hs.task` / `ShellRunner` completion callback is eaten
by the `pcall` that invokes it. In both cases the callback body **aborts at the
failing line** and every later statement silently never runs. This is how
Ollama predictions stopped appearing for weeks with no error anywhere.

`lib/logger.lua:994-1044` `install_runtime_error_capture()` mitigates part of it:
it wraps `hs.timer.{doAfter,new,doEvery,delayed.new}` callbacks in `xpcall`
(logging ERROR + traceback) and tees `print()` into the file log. **Do not remove
it.** Two limits worth knowing:

- It is installed at `init.lua:198`, after the log path is resolved. Anything
  scheduled before that line is unguarded.
- It covers `hs.timer` constructors and `print()` — nothing else. Eventtaps are
  not covered. `adapters/shell_runner.lua` and `adapters/http_client.lua` now
  contain visible `xpcall` boundaries; the latter is guarded by
  `test_http_client_reports_callback_throws.lua`. Re-read the live adapter before
  claiming a callback error is swallowed: this fact changed after the original
  audit.

Because of this, a regression test for anything async must encode the root cause
**behaviourally**. A "the call chain exists" grep is a false green; two
regressions have already hidden behind one.

## `hs.fs.dir` returns TWO values, and throws

`hs.fs.dir(path)` returns an iterator **and** a directory state object that the
iterator requires as its first argument (real Hammerspoon checks a `<<directory>>`
userdata metatable and aborts with _"directory metatable expected, got nil"_ on
the first step). It also **throws** on a missing or permission-denied directory.

So `local ok, it = pcall(hs.fs.dir, dir)` followed by `for x in it do` drops the
state and crashes at boot. The only blessed form is the iterator expression
directly in a generic-for, inside a pcall'ed closure — already centralised in
`lib/fs_dir.lua:42-55`. Use `fs_dir.entries(dir)` rather than re-deriving it.

Guard: `tests/meta/test_fs_dir_iterator_contract.lua` asserts per file that every
`hs.fs.dir` reference flows into a generic-for (`:135-148`), that `fs_dir.entries`
wraps its loop in pcall (`:167-176`), and pins the test stub to the faithful
`(iterator, state)` arity (`:194-208`).

That last assertion is the real lesson: the original `hs` stub returned a single
stateless iterator, so the buggy pattern "worked" and CI stayed green over a
guaranteed production crash. **A stub must model the real API's return arity and
its state requirement.** A second trap compounded it — an earlier meta-test
asserted the _buggy spelling_ was present. Assert the invariant, never a
particular phrasing of the code.

## `os.exit()` does NOT run `hs.shutdownCallback`

`hs.shutdownCallback` (`init.lua:781`) is the single place that stops modules,
restores system overrides, tears down the Karabiner bridge, flushes the keylogger
and kills helper processes. `os.exit()` terminates the Lua state immediately and
**never invokes it**.

There are two quit paths and both `os.exit`: the menubar Quit
(`ui/menu/init.lua:767`) and the `script_quit` gesture/shortcut
(`modules/gestures/actions.lua:560`). Each therefore has to replicate the
teardown by hand — Karabiner kill through the ownership-respecting
`karabiner.kill()`, `menu_llm.terminate_helper_processes()` +
`terminate_orphan_mlx_server()`, and `keylogger.stop()` for the flush.

The failure mode is invisible at quit time and shows up later: a detached
`mlx_lm.server` and helper daemons surviving indefinitely, or the last minutes of
keystrokes lost. Every one of those lines was added as a _missed sibling_ of a
fix applied to only one of the two paths.

**Whenever you add a teardown step, add it to all three sites** — the shutdown
callback and both `os.exit` paths. Guards:
`tests/meta/test_init_shutdown_quit_ke.lua`,
`test_menu_quit_karabiner_ownership.lua`, `test_menu_quit_mlx_teardown.lua`.

## Other traps

- **No blocking work inside an `hs.eventtap` callback.** macOS disables an
  overrun tap. `hs.timer.doAfter(0, …)` leaves the originating callback but runs
  later on the same Hammerspoon main loop; it is suitable for a short ordered
  handoff, not for shell, filesystem, Accessibility, or heavy work. Blocking
  work needs an owned asynchronous task/native worker and a completion
  protocol. Guards include
  `tests/unit/meta/test_interactive_actions_do_not_block_runloop.lua` and
  `tests/unit/modules/diagnostics/test_crash_report_deferred_off_hot_path.lua`.
- **`string.format("%q", path)` is not shell quoting.** `%q` escapes for a _Lua_
  literal and leaves `$`, backticks and `!` live for `/bin/sh`. Every driver path
  is user-configurable. Use `text_utils.shell_quote`. Guard:
  `tests/meta/test_shell_quoting_not_lua_q.lua` (it found 41 sites in 15 files).
- **`%` in a gsub REPLACEMENT raises.** Any outside-world value (app name, magic
  key, URL fragment, release tag) used as a gsub replacement must go through
  `text_utils.escape_gsub_replacement`. This class has bitten four times. Guard:
  `tests/meta/test_gsub_replacement_escaping.lua`.
- **Splitting a stateful module?** Add it to the force-reload list in
  `tests/helpers/init.lua`. Modules capture `local hs = hs` at require time, so a
  cached instance silently ignores a freshly injected stub and assertions see
  stale state.

## Guard the whole class

The recurring failure on this driver is not the missing guard — it is the ONE
sibling site that was missed. Widening a guard has paid off four times: the
`hs.task` GC pin was an 8-file allowlist until converting it to a whole-tree scan
found 5 unpinned files nobody had reported. When you fix any item above, grep the
entire driver for the same pattern and fix them together.
