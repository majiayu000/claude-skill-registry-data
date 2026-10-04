---
name: timermeet-python-builder
description: Implement and modify the TimerMeet Python desktop app (plain tkinter/ttk + Windows MCI audio + plyer). Use when changing timers, alarms, recurrence, persistence, translations, or UI behavior in timermeet_app/, timermeet.py, or tests/.
---

# TimerMeet Python Builder

## Overview

Implement features and fixes in TimerMeet's Python desktop app without regressing alarm reliability -- the entire reason this app exists is that its PHP/JS predecessor's reminders depended on a browser tab staying open.

## Workflow

1. Read `SDD.md` before changing behavior that affects product scope or validation (or hand off to the `timermeet-spec-driver` skill first).
2. Identify the right module (see `references/module-map.md`) and implement the smallest change that satisfies the request, reusing existing helpers rather than re-deriving logic.
3. Run the verification commands (see `references/validation.md`) before finishing.
4. Use the `timermeet-code-commenter` skill on any new non-obvious logic.
5. Bump `timermeet_app/__init__.py::__version__` when user-visible behavior changes, and update `README.md`/`SDD.md` to match.
6. If the change should ship as a compiled binary, use the `timermeet-exe-packager` skill to rebuild `TimerMeet.exe`.

## Hard constraints

- No network listener, HTTP server, or browser dependency -- ever.
- No `eval`/`exec`/`pickle`, no shell-string `subprocess`/`os.system`.
- Every URL-opening path goes through `timermeet_app.security.is_http_url()`.
- Every disk write goes through `timermeet_app.security.atomic_write_text()` (directly or via `storage.py`).
- Keep the Tkinter main thread non-blocking -- background threads or `root.after()`, never a blocking sleep on the UI thread.
- Comment only code that would otherwise be hard to parse quickly; don't over-engineer beyond the request.

## References

- `references/module-map.md` -- what lives in each `timermeet_app/*.py` file.
- `references/validation.md` -- the exact commands to run before calling a change done.
