---
name: milestone
description: Work on the next (or a named) step from docs/ROADMAP.md in learning mode — plan, explain concepts, implement a small slice, verify, then update the roadmap and learning log. Use when the user says "next step", "continue", "let's do 1.4", or similar.
argument-hint: "[step id, e.g. 1.4] [--you-drive]"
---

# /milestone: one roadmap step, learning mode

## 1. Orient
- Read `docs/ROADMAP.md`. If an id was given, use that step. Otherwise use the first unchecked step.
- Read the relevant CLAUDE.md (`backend/` or `mobile/`) and any docs the step touches (`DATA_MODEL.md`, `ARCHITECTURE.md`).
- Look at the current code so the plan fits what exists.

## 2. Brief (then wait)
Post a short brief and **wait for the go-ahead** before writing code:
- **Goal:** what will exist and work at the end of this step.
- **Concepts you'll meet:** 2–5 Java/Spring (or RN) concepts, each one line, with a Go/TS analogy where it helps.
- **Plan:** the files to create or change, in order.
- **Your turn?** If the step has a 🧑‍💻 marker or a self-contained piece, offer to let the user write it, giving a precise spec
  (signature, behavior, a hint) and saying you'll review it with `/java-review`.

If invoked with `--you-drive`, the user writes all of the code: give them the spec and hints, then review.

## 3. Build in small increments
- Make the change in 1–3 small chunks. After each chunk, explain the non-obvious lines, especially annotations
  ("what does `@Transactional` actually do here?").
- Follow `backend/CLAUDE.md` / `mobile/CLAUDE.md` strictly. Don't add anything the step doesn't need.
- If a decision in the docs turns out wrong, stop and propose the change rather than silently deviating.

## 4. Verify
- Backend: `./mvnw test` (or `verify` when there are integration tests). Run the app and `curl` the endpoint when relevant.
- Mobile: `npm run typecheck && npm run lint && npm test`. Tell the user what to look at in the simulator.
- Report failures honestly, with output.

## 5. Wrap up
- Tick the step in `docs/ROADMAP.md`.
- Append an entry to `docs/learning/LEARNING_LOG.md` (concepts, where to look, one gotcha, one link).
- Suggest a commit message. **Do not commit or push**: the developer does that themselves.
- Give a one-line preview of the next step, then stop.
