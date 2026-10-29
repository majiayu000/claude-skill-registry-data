---
name: progress-status
description: "Use when someone asks for a status table, progress summary, progress report, task status overview, or runs /progress-status."
---

## What This Skill Does

Turns whatever progress/task-tracking information is already available into a manager-ready status table (specific enough that the user can read it straight to a manager with no improvising) and a one-line summary. Pure reporting — never writes anything back, never re-judges whether a recorded status still matches reality; that judgment belongs to whatever produced the tracking data in the first place.

This skill doesn't assume a specific file, tool, or other skill produced its input. It works the same way on any AI platform: find the source data (Step 1), read whatever structure it has (Step 2), report (Steps 3+).

## Step 1: Find the source data

Ask (clickable question where `AskUserQuestion` is available, plain numbered list with a free-text fallback otherwise) where the progress data is:

1. Already visible earlier in this conversation — **(Recommended when that's true)**
2. A file at a path the user gives — only offer this if a file-read tool actually exists in this session
3. The user will paste it in now

If a specific task/project name was given (e.g. via `$ARGUMENTS`), use it to filter once the source is found — error with the list of task names actually present rather than guessing if the named one isn't there.

If there is no matching content at all, say so in one line and stop. No empty table, no invented status.

## Step 2: Recognize structure, without requiring one exact schema

Many sources will use a checkbox-style convention: ✅ done / 🟡 in progress / ⬜ pending / ⚠️ skipped markers, with `(blocked by: ...)`, `(deferred: ...)`, and `Next: ...` tags. If the source already looks like that, read it exactly per the Column Rules below.

If the source uses some other shape (a plain checklist, a prose status update, a different tool's export), map it onto the same table shape as best you can, and say plainly in the reply which cells were read directly from an explicit marker versus inferred. If a cell genuinely can't be determined, use `—` rather than guessing — see the compaction rule below.

## Step 3: Report

1. Identify which tasks to report: the one named, if given (see Step 1); otherwise every task/item marked in-progress.
2. For each task, first print a one-line summary, then the table.

   **Summary line format:** `<N>% complete — <On track / At risk> — <blocker count> blocker(s)<: compact blocker list, or nothing if zero>`
   - `<On track / At risk>`: **At risk** if any not-yet-done phase carries a `(blocked by: ...)` tag or an explicit blocker note pointing at something outside the normal phase-to-phase sequence (an external dependency, a missing access/resource, a person who hasn't answered, etc.) — not just "waiting on the previous phase to finish." A `(deferred: ...)` tag never counts toward this. Otherwise **On track**.
   - Blocker list: the compact blocker fragment (same style as the table's Blocker column) for each at-risk phase, semicolon-separated. Omit the colon and list entirely if there are zero blockers. Deferred items are never included — they're not blockers.
   - Example: `56% complete — At risk — 2 blockers: no automation-safe OMS login yet; awaiting more form responses from domain expert`

   **Table format:**

   | Phase | Status | % | Blocker | Next Action |
   |---|---|---|---|---|
   | <phase name> | Done / In progress / Not started / Skipped (exception) | <phase's own step completion %> | <compact reason, or —> | <compact recommended action, or —> |

   Column rules — grounded only in what the source actually states, never inventing new information:
   - **Status:** ✅ → **Done**, ⚠️ → **Skipped (exception)** (Blocker column carries the recorded reason instead of a blocker), 🟡 → **In progress**, ⬜ → **Not started**.
   - **%:** steps marked ✅ or ⚠️ in that phase, divided by total steps in that phase, as a whole-number percentage. A Done phase is always 100%; a Not started phase is always 0%. A `(deferred: ...)` step doesn't count toward this percentage.
   - **Blocker — a compact fragment, ~10-15 words, not a sentence, always in plain language.** The three sources for this, nothing else: an unmet `(blocked by: ...)` tag, a `SKIPPED (exception): <reason>` text, or — when neither applies — a `(deferred: ...)` tag. Compress to the bare fact — names/IDs, dates, and who/what is involved always survive; never carry over bare internal references ("Step 3.1", "current build") without spelling out what they mean.
     - `(blocked by: ...)` / `SKIPPED` → phrase as a blocker, e.g. `Waiting on Step 1.2`. Counts toward the summary line's blocker total.
     - `(deferred: ...)` → phrase as a deferral, always starting with **"Deferred:"**, e.g. `Deferred: paused reviewing leftover form answers, only needed for later steps`. Never counts toward the blocker total or At-risk call.
     - Use `—` when none of the three applies.
   - **Next Action — sourced only from an explicit `Next:` line, if present.** Quote or lightly compact it (~10-15 words max). Never invent a next action from a step's title or description when no `Next:` line exists — the cell is `—` in that case.
3. Head each task's summary+table with the task name: `### <task name>`.
4. If more than one task is being reported, print each as its own headed summary+table, in the order encountered — never merge into one table.
5. Nothing else in the chat reply beyond the summary line(s) and table(s). No restating the table in prose, no extra commentary paragraph.

## Step 4: Delivering a copy (optional)

Printing the table and summary directly in the reply always works and is the primary deliverable. If a file-write tool actually exists in this session and the user wants a saved copy, write it to a local file and say where — there's no platform-specific "file card" or delivery mechanism assumed beyond that.

## Notes / Guardrails

- Never resave, edit, or reformat the original source you read from — this skill only reports.
- Don't re-judge or flag drift on a recorded status — trust the source as read. That judgment belongs upstream, to whatever produced the tracking data.
- Blocker and Next Action cells (and the summary line's blocker list) are compact fragments capped at ~10-15 words each — dash/colon punctuation, dropped subjects, no filler — never a full sentence, and never internal shorthand a first-time reader wouldn't follow. `No automation-safe OMS login — build blocked` is usable; a bare label with no consequence ("OMS login") is not; neither is a bare internal reference ("Step 3.1") with no plain-language explanation.
- If the source doesn't clearly state a blocker, deferral, next step, or reason, use `—` rather than guessing or padding.
- Never phrase a `(deferred: ...)` tag as if it were a blocker, and never phrase a `(blocked by: ...)` tag as if it were a deferral.
- The On track / At risk call and the blocker/next-action text must all trace to something actually stated in the source. If it's ambiguous whether something is a real external blocker, treat it as On track rather than inventing risk that isn't documented.
- This skill is intentionally self-contained: it doesn't call, assume, or require any other skill to have produced its input. If the source happens to follow the same checkbox/tag convention `task-progress-tracker` uses, that's because it's a sensible convention to reuse on its own merits — not a dependency between the two skills.
