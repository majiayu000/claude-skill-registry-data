---
name: session-end
description: >
  At session end, write the one-file session baton (docs/session/baton.md):
  a high-level summary of what this session was about, the goal, and the single
  next task. Overwrites the file — no change lists, no task lists, no detail.
  Read-only on git; writes only the baton. Use `session-wrapup` for git state
  and progress.md.
disable-model-invocation: true
---

# Session End

Overwrite `docs/session/baton.md` following `docs/session/template.md`. Write
nothing else.

## Steps

1. Read `docs/session/template.md` for the shape, and the current
   `docs/session/baton.md` if it exists — carry its **Goal** forward.
2. Overwrite `docs/session/baton.md` — never append; it holds only the last session.
3. Fill each section, then set `_Last updated:_` to today's date.

## Rules that keep it high-level

- **This session**: 2–3 sentences of prose. No change list, no file names, no
  detail — that lives in `docs/progress.md` and the code.
- **Goal**: the standing objective. Carry it forward unchanged until it is reached.
- **Next task**: exactly one thing — one paragraph, not a list. If several loom,
  pick the next and drop the rest. Write `None` when there is no clear next task.
- **Read first**: the one doc the next session must read. Write `None` when there
  is nothing.

## Boundaries

- Read-only on git — never commit, stage, or push.
- Write only `docs/session/baton.md`. For git state and `docs/progress.md`, that is
  `session-wrapup`.
- Write the baton through the `human-writing` skill.
