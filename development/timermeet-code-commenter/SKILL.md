---
name: timermeet-code-commenter
description: Add or review comments and docstrings in TimerMeet's Python code so a reader can tell what each non-obvious part does and why. Use when the user asks to "explain the code", "comment every part", "quiero saber qué hace cada parte del código", or before/after a change to logic-heavy modules (recurrence.py, storage.py, audio.py).
---

# TimerMeet Code Commenter

## Overview

Make TimerMeet's Python code self-explanatory to someone who didn't write it, without burying the logic in noise. This skill governs *how* to comment, not *what* to build.

## Rules

1. **Comment the why, not the what.** A reader can already see `for meeting in self.meetings:` -- they can't see *why* the loop skips a record, or why a constant is `9 * DAY_MS` and not `7 * DAY_MS`. Every comment should answer a question the code itself can't.
2. **One-line module docstring purpose + a short "why this exists" paragraph** at the top of each file, referencing the original JS/PHP source function it replaced when relevant (e.g. "Port of `addRecurrenceToDate()`").
3. **Function/method docstrings** for anything with a non-obvious contract: what it mutates, what it returns on the "nothing to do" path, and any invariant the caller must preserve (e.g. `extend_series_if_needed`'s idempotency guarantee).
4. **No comments on self-evident code.** Don't add `# increment counter` above `count += 1`. If removing a comment wouldn't confuse a future reader, remove it.
5. **Flag every deliberate simplification** versus the original web app inline, at the point where it diverges (e.g. `audio.py`'s MP3-loops-from-start-instead-of-sub-clip note, `i18n.py`'s `# desktop-adapted` markers). A silent behavioral difference from the ported spec is worse than an ugly comment.
6. **Never restate the current task/PR in a comment** ("fixed for issue #12", "added per user request") -- that belongs in the commit message, not the source, and rots as the codebase evolves.

## Workflow

1. If asked to comment "everything", start from `timermeet_app/recurrence.py` and `timermeet_app/storage.py` (highest logic density, highest regression risk) before UI files.
2. Read the function fully before writing its docstring -- don't guess behavior from the name.
3. Cross-check any claim about the original app's behavior against `legacy-php/assets/app.js` rather than assuming; if you can't verify it, say "ported from the legacy web app" without over-claiming precision.
4. After adding comments, re-run `python -m py_compile` on touched files (a docstring edit can still break syntax if quoting goes wrong) and `python -m unittest discover -s tests`.
