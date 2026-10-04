---
name: timermeet-regression-testing
description: Validate TimerMeet after a change -- startup, windows, buttons, alarms, sound, timers, Teams, calendar, notifications, settings, persisted state, and clean shutdown. Use after any code or UI change, before reporting it done.
---

# TimerMeet regression testing

## Overview

TimerMeet's core value proposition is alarm reliability (see SDD.md's rationale for the PHP->Python rewrite). Regression testing here is not generic "does it run" -- it's specifically about not silently weakening an alert path. Pair with the `timermeet-qa-validator` agent, which owns the PASS/FAIL/BLOCKED reporting format.

## What to validate, and how

| Area | How to check |
|---|---|
| App startup | `python timermeet.py`, confirm no exception lands in `data/timermeet.log`, window appears within a few seconds (no freeze -- see design-notes.md's startup-freeze history). |
| Windows/navigation | List/gadget/calendar/week views switch via `set_active_view`/`set_gadget_mode` without a second `Tk()`/`Toplevel` appearing; each view's own nav (month/week prev-next, today button) still moves the displayed range. |
| Buttons | Grep the button's `command=` target in `main_window.py`/`app.py` to confirm it's still wired to a real handler, not orphaned by a rename. |
| Alarms | `python -m unittest tests.test_alarm_queue -v` (covers the FIFO queue/hand-off logic with a real `tk.Tk()` root); manually trigger one (shortest reminder, `setNowButton`) to see the overlay, its flash, and both buttons. |
| Sound | Confirm `audio.AlarmPlayer.play` still has its `winsound.Beep` fallback intact if you touched `audio.py` -- a failing MP3 must never mean silence. |
| Timers | Confirm every `root.after(...)` job your change touches is cancelled via `after_cancel` on its teardown path (`alarm_ui.py::AlarmController.dismiss` is the reference example -- it cancels `_flash_job`/`_title_blink_job`/`_relift_job`/`_countdown_job` in one loop). |
| Teams | Any `webbrowser.open()` call site goes through `security.is_http_url()` first (grep to confirm no new bare call site was added). |
| Calendar | `python -m unittest tests.test_calendar_day_click tests.test_context_menu tests.test_week_view tests.test_week_selection tests.test_week_column_mode tests.test_header_layout -v` if `main_window.py`'s calendar/week rendering changed. |
| Notifications | `notifications.py`'s OS toast is best-effort by design -- confirm it degrading/failing doesn't affect the sound/overlay channels (they must never depend on it). |
| Settings/persistence | `python -m unittest tests.test_storage tests.test_merge tests.test_companies tests.test_retention -v` if `storage.py`/`retention.py` changed -- these cover merge-on-save and the two cleanup functions, both real historical bug sources. |
| Clean shutdown | Close the app while no alarm is active, then again with one active (confirm `dismiss(run_callback=False, advance_queue=False)`'s shutdown path in `alarm_ui.py` doesn't try to build a new Toplevel against a dying root). |

## Full regression pass

```powershell
python -m py_compile timermeet_app/*.py timermeet.py build_exe.py
python -m unittest discover -s tests -v
python timermeet.py   # manual smoke test; close after confirming no log exception
```

## Never test against live data

Before running any script that calls `handle_save`/`handle_delete`/`storage.save_meetings`/etc. against real data, copy `data/meetings.json` first. A real meeting has been lost this way once already during testing -- see [[feedback_never_test_against_live_data]].

## When something fails

Report the specific failing test/behavior and hand off to the `timermeet-debugger` agent for root-causing rather than guessing at a fix -- see that agent's diagnose-before-modifying discipline.
