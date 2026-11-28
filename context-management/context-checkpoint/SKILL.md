---
name: context-checkpoint
description: Externalize working state to a checkpoint file so long tasks survive context compaction, interruption, and handoff. Use at the start of any task expected to exceed ~30 minutes, touch many files, or run many commands; whenever a phase completes, the plan changes, or a dead end is confirmed; and immediately after any compaction or session resume, before editing. Not for short single-file edits.
---

# context-checkpoint

Weak checkpointing looks like: forty minutes of decisions living only in conversation history, then a compaction, then a confident post-compaction session redoing step 2 while overwriting completed step 4. Strong checkpointing keeps ground truth in a file a cold reader could resume from in under a minute.

## 1. Create the file at task start

Write `checkpoint.md` in the session scratchpad (or a gitignored `.claude/` path in the repo — never a tracked file). Contents, in this order:

- **Goal** — one line, in the user's words.
- **Acceptance** — the concrete command or observation that proves done (e.g. the exact test command).
- **Steps** — ordered, each with a status marker: `[ ]` todo, `[x]` done, `[-]` dead end.
- **Decisions** — "chose X over Y because Z". The *why* is what evaporates first.
- **Resume point** — see §3. Empty at start.

Tell the user the path once; don't narrate every update.

## 2. Update at phase boundaries, not continuously

Rewrite the file when a step completes, the plan changes, a dead end is confirmed, or you're about to start something long-running or risky. Record dead ends with what was tried and the evidence it failed, so they aren't retried. Don't checkpoint every edit — noise hides the signal.

## 3. Make the resume point executable

The resume section contains, verbatim: the last command you ran and its current output (trimmed to the failing lines), the `file:line` you were editing, and the next single concrete action. "Continue the migration" is useless after compaction; "run `<test cmd> -k utf8`; still failing at `ingest.py:214` null check; next: guard `row.name` before `.encode`" resumes in seconds.

## 4. After compaction or resume, trust the file over the summary

Before any edit in a resumed session: re-read the checkpoint, run `git status` and `git diff --stat`, and reconcile them. The compacted summary is lossy; the file and the diff are ground truth. Where they disagree, the diff wins and the file gets corrected. Never redo a step marked `[x]` without evidence it is actually undone.

## 5. Commit at safe points

When the work is committable and committing is within your brief, a described commit is the strongest checkpoint there is (see git-hygiene). Don't let 400 lines of uncommitted work ride on one fragile context; at minimum list "uncommitted: files A, B, C" in the resume point.

## Exit check

At the end of the task the checkpoint holds the final state and the report can be written from it alone. If the task is handed off unfinished, the resume point is the handoff.
