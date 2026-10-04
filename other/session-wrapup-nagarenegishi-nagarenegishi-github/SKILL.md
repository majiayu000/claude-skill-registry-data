---
name: session-wrapup
description: >
  Close out a working session: update `docs/progress.md`, report uncommitted
  and unpushed work, and list the session's decisions and open threads.
  Read-only on git — never commits, stages, or pushes.
disable-model-invocation: true
---

# Session Wrapup

Close out the current session: run the three steps below in order. Never commit, stage, or push — all git checks are read-only.

## 1. Update docs/progress.md

Record what this session completed:

- Read `docs/progress.md` first and match its existing entry format exactly — heading style, date format, level of detail.
- If the file does not exist, create it with a short dated entry in a minimal format.
- Record completed work only; in-progress work belongs in the open-threads report (step 3).
- Write entries following the `human-writing` skill.

## 2. Report git state

Read-only checks:

- `git status` — list uncommitted changes; when the conversation makes it clear, group them as session work versus unrelated or pre-existing.
- `git log @{upstream}..HEAD --oneline` — list unpushed commits. If the branch has no upstream, say so instead of guessing.
- Leave commit decisions to the user; suggest a commit message if the uncommitted work forms one coherent change.

## 3. List open threads and decisions

From this session's conversation, report:

- **Decisions made** — choices with lasting effect (approach picked, alternative rejected, convention adopted), each in one line with the reason.
- **Open threads** — work started but unfinished, questions raised but not answered, TODOs mentioned in passing, follow-ups promised.
- **Suggested next step** — the single most useful thing to start the next session with.

Skip empty categories rather than padding them.

## Output

Present steps 2 and 3 in chat as the wrapup report. Write no file other than `docs/progress.md`.
