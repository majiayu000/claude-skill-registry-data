---
name: timermeet-ui-designer
description: Improve TimerMeet's GUI -- simplicity, clarity, layout, and performance-conscious widget choices. Use when the user asks to make the interface simpler, clearer, less cluttered, nicer, or easier to understand, or to add/rearrange a UI control.
---

# TimerMeet UI Designer

## Overview

Keep TimerMeet's interface simple, clear, and fast, built entirely in plain `tkinter`/`ttk`. This skill governs *how* to change the GUI; business logic and validation belong in `app.py`, never in `main_window.py`/`alarm_ui.py`.

## Hard rules

1. **No CustomTkinter or any themed widget toolkit, ever.** Tried and reverted once already (v2.0.0 → v2.0.1) for adding 20+ seconds to startup with a real-sized meeting list.
2. **Never call `root.update()`/`root.update_idletasks()` synchronously**, for any reason. This caused the v2.1.0 startup freeze. Let `mainloop()` process pending work on its own.
3. **Mind the per-meeting widget budget.** Each meeting card is rendered once per visible meeting; every extra widget in `_render_card` is a real, multiplying cost with a real-sized list (dozens of meetings), not a rounding error.
4. **Reuse, don't reinvent.** Use the existing color constants and `_button()`/`_entry()`/`_make_option_menu()`/`_ScrollablePanel` helpers in `main_window.py`.
5. **Every string goes through i18n.** Add new keys to both `translations["es"]` and `translations["en"]` in `i18n.py` -- `tests/test_i18n.py` enforces they never drift apart.

## Workflow

1. Read `SDD.md`'s "Arquitectura: backend y frontend sí están separados" section and `.claude/skills/timermeet-python-builder/references/module-map.md` first.
2. Prefer merging/removing over adding (see `references/design-notes.md` for the widget-count budget and the project's track record of fixing real bugs by simplifying, not adding).
3. Implement the smallest widget-tree diff that satisfies the request.
4. Run `python -m py_compile timermeet_app/*.py` and `python -m unittest discover -s tests` -- the i18n parity test catches a missed translation key immediately.
5. Smoke-test with `python timermeet.py` (see `.claude/skills/timermeet-python-builder/references/validation.md`): confirm it opens fast, stays responsive, and the changed screen behaves as expected. You cannot see the rendered window -- if a layout/spacing request is ambiguous, describe what you changed and ask for confirmation rather than iterating blindly.
6. Update `SDD.md` if the change affects user-visible behavior (not just styling).

## References

- `references/design-notes.md` -- color palette, spacing conventions, and the widget-count budget.
