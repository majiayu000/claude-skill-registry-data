---
name: timermeet-python-debugging
description: Diagnose TimerMeet crashes, freezes, leaks, and race conditions -- read the log, reproduce narrowly, isolate the real mechanism, make the smallest fix, then re-verify with the correct metric. Use before touching code in response to any unexplained bug report.
---

# TimerMeet Python debugging

## Overview

Diagnosis before modification. This project has a documented history of fixes that looked complete but weren't, because the verification used the wrong measurement (see `.claude/skills/timermeet-python-builder/references/module-map.md`'s "Recurring footgun" section: the v2.7.0 calendar-rebind leak fix was believed complete for three versions because `root._tclCommands` is blind to plain-`.bind()` leaks). Don't repeat that mistake -- confirm with the metric that actually measures the thing you're claiming is fixed.

## Workflow

1. **Read the report and the log first.** `data/timermeet.log` (via each module's `logging.getLogger(__name__)`) durably records exceptions even after the window closes -- check it before forming any hypothesis.
2. **Check Windows-level signals if relevant.** A "Not Responding" window title is Windows' own signal of a blocked Tk mainloop, not a vague crash -- if reported, go straight to suspecting a synchronous `root.update()`/`root.update_idletasks()` call (see below).
3. **Identify the causing module** using `.claude/skills/timermeet-python-builder/references/module-map.md`'s ownership table -- don't guess across files that don't own the behavior in question.
4. **Reproduce narrowly.** Prefer a small, isolated script or an existing test run in isolation (`python -m unittest tests.test_alarm_queue -v`, or a real `tk.Tk()` root built the same way `tests/test_alarm_queue.py::setUp` does) over running the whole app.
5. **Isolate the actual cause**, not a correlated symptom -- form a specific, falsifiable hypothesis ("this `.bind()` call re-registers a Tcl command on every render and nothing releases the old one") and confirm it directly.
6. **Make the smallest fix** that addresses the confirmed cause.
7. **Validate the fix** with the correct metric -- see below for the two most common categories in this codebase.

## Common failure classes here, and how to actually confirm each

### GUI freeze / "Not Responding"

Grep for `root.update()` or `root.update_idletasks()` outside the single documented exception in `TimerMeetApp.__init__` (made only when the "Cargando…" placeholder exists, nothing else built). This exact call, made after the real widget tree exists, caused the v2.1.0 startup freeze: it forces Tk to drain its entire pending idle/geometry queue synchronously, and Windows marks the window "Not Responding" for however long that takes. The fix is virtually always deletion, not a replacement call.

### Tcl command leak (memory growth over a long-running session)

- For a `bind_all()` case: `root._tclCommands` is a valid metric (confirmed correct for `_ScrollablePanel`'s v2.8.0 leak, since `bind_all()` routes its funcid through `self._root()`).
- For a **plain** `.bind()` on any widget other than root: `root._tclCommands` is **blind** to this -- 500 leaked plain-`.bind()` commands moved it by exactly 0 in direct measurement. Use `tests/testutils.py::count_tcl_commands()` (`info commands`, interpreter-wide) instead.
- Confirm against **real** re-render/navigation calls (e.g. `TimerMeetApp.handle_week_next()`), not just calling the render function in isolation with unchanged data -- a dirty-check/signature gate can hide a leak that only shows up on a genuinely-triggered re-render (this is exactly what made the v2.7.0 fix look complete when it wasn't).
- The reusable fix, once confirmed: `main_window._rebind(widget, sequence, handler, previous_funcid)`, which calls `widget.deletecommand(previous_funcid)` before rebinding (widget itself for plain `.bind()`, `widget._root()` for `bind_all()` -- confirmed empirically to differ between the two).

### Race conditions / thread issues

Check whether a callback that legitimately runs on a non-Tk thread (pystray tray callbacks, background audio work) touches a Tkinter widget directly. The fix is always to marshal through `root.after(0, ...)` before any widget access, never a lock around the widget call.

### Alarm misbehavior (missed, duplicated, or wrong-meeting alert)

Start with `alarm_ui.py::AlarmController`'s docstring and its FIFO `_queue` -- a real historical bug here was two meetings due in the same 1-second heartbeat tick silently destroying the first one's not-yet-seen overlay. If the report resembles that shape, check whether `notify()`/`_present()`/`dismiss()`'s queue hand-off logic was altered.

## After the fix

Hand off to `timermeet-qa-validator` (or the `timermeet-regression-testing` skill directly) to confirm the fix holds under the correct metric -- not just that the original repro no longer reproduces once.
