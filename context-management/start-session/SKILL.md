---
name: start-session
description: Open a session in this therapy workspace — load the frame, the working agreement, open threads, recent sessions and a scoped background brief, then hand the floor over. Use at the start of any session, or when the user says "let's start", "I'm back", "where were we".
---

# start-session

Orientation. Read-only: this skill writes nothing.

## Procedure

1. **Read the frame.** `context/issue.md`, `context/working-agreement.md`, `context/goals.md`.
   The working agreement overrides your defaults for the rest of the session — tone, pacing,
   what not to do, how sessions end.

2. **Read what's open.** `threads/INDEX.md`, then the two most recent files in `sessions/`. If
   `sessions/` is empty, this is a first session — say so and skip to step 5.

3. **Load background context, scoped.** Follow `memory/README.md`. Use only the scopes in
   `memory/config.yaml`. If `config.yaml` does not exist, say so once and continue without
   background context — do not fall back to any model-managed memory, and do not read the
   whole store.

4. **Report what you loaded**, in at most four lines:
   - how long since the last session, and what it was about
   - which threads are open
   - which background entries you loaded (by title)
   - anything explicitly left hanging last time ("you said you'd think about X")

5. **Hand over.** One question: what today is for. Then wait.

## Rules

- Do not summarise the whole history back at them. They were there.
- Do not open with a question from a previous session's action list unless they ask for it.
- If the last session ended badly, or ended with them asking to stop, do not reopen it. Note
  that you have it and let them decide.
- If more than a month has passed, ask whether the frame in `context/issue.md` still fits before
  anything else. Frames go stale quietly.
- Never begin with a disclaimer about not being a therapist. It is in the README, they know, and
  saying it every session is its own kind of unhelpful.
