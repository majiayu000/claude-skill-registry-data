---
name: task-progress-tracker
description: "Use when someone asks to check project progress, see what's left, continue a task, track a task across sessions, update task status, or run /task-progress-tracker."
---

## What This Skill Does

Tracks one or more tasks in a single markdown document — structure is **Task → Phases → Steps**, and a phase is only complete when every one of its steps is complete. Progress survives beyond a single reply so work can be picked back up later.

This skill is written to behave the same way on any AI platform (Codex, Codex.ai web, Codex Cowork, ChatGPT web/desktop, Codex, or similar) rather than assuming a specific project/file API. See **Platform Behavior** below before doing anything else.

## Platform Behavior (read this first, every run)

1. **Check what's actually available in this session** — a real file system (a Read/Write/Edit-style tool that operates on an actual path), or chat-only with no durable storage this skill controls.
2. **If file tools exist:** treat a file named `task-progress-tracker.md` in the current working directory as the source of truth. Read it if present; write it after every change.
3. **If no file tools exist (chat-only platform):** there is nothing this skill can silently persist. Ask the user (clickable/numbered choice, see below) whether this is a new task or a resume. On resume, ask them to paste back the last version of the doc (or attach it, if the platform supports uploads and you can read them) — treat that pasted content exactly as if it had been read from a file.
4. **Every time the doc changes, on any platform, print the full updated doc in the reply** as plain markdown. This is the one delivery method guaranteed to work everywhere, and on a chat-only platform it's the user's only copy to save and paste back next session.
5. **Clickable questions:** use `AskUserQuestion` when that tool is present. When it isn't, present the exact same choices as a plain numbered list (`1) ... 2) ...`) and accept either a number or free text in reply. Either way: always mark the recommended option, always keep a free-text/custom path open, never make a list the only way to answer.
6. If a chat-only platform has no pasted-back doc to resume from, say so plainly once — "I can't see anything tracked in a different conversation here; paste the last doc back to resume, or say this is a new task" — rather than guessing or silently starting over.

## Formatting Standard (applies to every write)

The doc must be instantly scannable by a first-time reviewer — someone who has never seen the project should understand exact progress within seconds, without reading paragraphs. This is not optional polish; it's the point of the doc.

- **Every step and phase is a single compact checkbox line** — a marker, a short label, at most a few words of specific detail. Never a paragraph. If a step's context needs more than one line to explain, that explanation goes in a clearly labeled block (like the Decisions Log below), not inline in the checklist.
- **Specific, not generic.** A line must carry the actual noun/number/name involved — "DE + 1st Class (>€20) → GLS Service", not "handle DE shipping edge case." Compression cuts words, never facts.
- **No connective or narrative filler.** Cut phrases like "in order to", "it's worth noting that", "this step involves". State the fact directly.
- **Plain language, not internal shorthand.** The reason text inside a `(blocked by: ...)`, `(deferred: ...)`, or `SKIPPED (exception): ...` tag must read clearly to someone who has never seen this doc — a manager, a new team member, the user themselves reading it cold days later. Never rely on internal references like a bare step number ("Step 3.1") or project jargon ("current build", "v1 scope") to carry the meaning — say the actual thing in ordinary words.
- **Decisions, rules, assumptions, and success criteria are NOT compacted into one-liners** — these carry real operating rules (thresholds, exceptions, hard boundaries) that must survive in full. Group them under short bold subheadings (e.g. **Facts**, **Assumptions (TEMPORARY)**, **Architecture**, **Success Criteria**) so they're easy to scan by category, but keep each point's actual detail intact.
- If a task covers a larger fixed universe of items (e.g. a 37-step SOP where only some steps are being automated), give that universe its own checkbox table-of-contents section, separate from the phase/step tracking of the current build.
- Use `---` horizontal rules between major sections (a full-scope list if present, Decisions Log, Project Phases) so the doc reads as clearly separated blocks.
- **Mandatory tagging — no blocker, deferral, or next step lives only in prose.** A step or phase genuinely stuck on something MUST carry `(blocked by: <plain-language reason>)`. A step deliberately postponed by choice MUST carry `(deferred: <plain-language reason>)` instead — never the blocked-by tag. A real, concrete next action for a phase MUST be written as a `Next: <...>` line. This isn't optional: `progress-status` (or any other reporting done from this doc) can only surface these from the exact tags — anything left in prose only will read as missing.

## Doc format

```markdown
# Task Progress Tracker

## Task: <task name>
Status: in_progress | completed
Created: <date>

**Marker key:** ✅ done · 🟡 in progress · ⬜ pending · ⚠️ skipped (exception)

### Phase 1: <phase name> — ⬜ not started / 🟡 in progress / ✅ complete
- ✅ 1.1 <short specific step label>
- ⬜ 1.2 <short specific step label>
- ⚠️ 1.3 <short specific step label> — SKIPPED (exception): <one-line plain-language reason>
- ⬜ 1.4 <short specific step label> (deferred: <one-line plain-language reason>)

### Phase 2: <phase name> — ⬜ (blocked by: Phase 1)
Next: <one-line concrete next action, optional>
- ⬜ 2.1 <short specific step label> (blocked by: <plain-language reason, e.g. "the previous step isn't finished yet">)
...

## Task: <another task name>
...
```

Marker legend: ⬜ pending, ✅ complete, ⚠️ skipped/exception (requires a reason after " — SKIPPED (exception): "). A phase's own marker is derived, never set directly: ✅ only when every step under it is ✅ or ⚠️; otherwise 🟡 if any step is ✅/⚠️, else ⬜. A deferred step (`⬜ ... (deferred: ...)`) stays ⬜ — deferring it does NOT make it count as done, and does NOT flip the phase to ✅.

Always include the "**Marker key:**" line once near the top of the doc so anyone opening it cold knows what the symbols mean.

`(blocked by: ...)` covers BOTH kinds of stuck: a genuine sequence dependency ("can't start before Phase/Step X finishes") AND an external blocker (waiting on a person, a missing access/resource, an unresolved decision). Write the reason in plain words, not a bare step reference.

`(deferred: ...)` is a separate tag for a step deliberately postponed by choice, not stuck on anything. Never use `(blocked by: ...)` for this case and never use `(deferred: ...)` for a real blocker.

`Next: <...>` is mandatory whenever there's a real, concrete next action beyond "do the next step in order." Leave it out only when there genuinely isn't one yet — this is the only field a reporting pass may read for "next action"; never invent one from step titles if this line is absent.

## Step-by-Step Workflow

### 1. Read current state

Per Platform Behavior above: read the file if file tools exist, otherwise ask new-vs-resume and get the pasted doc.

- **Doc/content doesn't exist yet:** go to step 2 (create a task).
- **Doc/content exists:** go to step 3 (resume/report).

### 2. Create a new task (first time, or user asks to track a new task)

This can happen with no history behind it, or in the middle of real work already done. Don't assume a fresh task starts at 0% — check first.

1. Ask the user for a short task description (free text — this is genuine open-ended content, don't offer clickable options for it).
2. Draft a phase/step breakdown from that description: logical phases, each with a handful of concrete, checkable steps, each written as one compact specific line per the Formatting Standard above. Tag genuine dependencies/blockers as `(blocked by: ...)`, deliberately postponed steps as `(deferred: ...)`, and add `Next:` lines — only where real, never invented.
3. **Backfill scan:** Codex can only see what's visible in the current conversation, plus whatever files it can actually read on this platform — there's no cross-session memory to query on most platforms. Use whatever's visible to guess which drafted steps are already complete. If there's nothing to find, skip straight to a 0%-complete draft — don't fabricate signal that isn't there.
4. **Scope check:** if the draft exceeds roughly 25 steps total, pause before showing it — tell the user the task looks too large for one tracked plan and suggest splitting it. This is a soft pause — if they want one big plan anyway, keep going. (A fixed reference list like a full SOP's total step count is a separate table-of-contents section and doesn't count against this cap.)
5. Show the drafted breakdown as a clickable/numbered confirmation (per Platform Behavior): one question per phase (or one combined question if the plan is small), listing each step as an option, with steps Codex believes are already done pre-selected. The user adjusts the selection to match reality before anything is saved. Keep a plain confirm/edit fallback for the phase/step wording itself, separate from the completion checkboxes.
6. Once confirmed: if file tools exist, re-read the file first (in case it changed since — see Concurrency below), then write the merged result. If chat-only, just finalize the doc in the reply.
7. Print a one-line summary reflecting the real starting point, e.g. `Tracking "<task name>" — Phase 2 of <N> — 45% — <N> steps to go.` (not always 0%, if the backfill scan found completed work).

### 3. Resume an existing task and report status

1. Parse the doc's tasks/phases/steps and compute: current phase, percent of steps complete (per task, and overall if multiple tasks), and any exceptions.
2. Print a one-line summary at the top of the reply, e.g.: `"<task name>" — Phase 2 of 4 — 60% — 3 steps left.` If multiple tasks are in progress, one line per task.
3. If the user named a specific task, report only that task; otherwise cover all tasks with status `in_progress`.

### 4. During the conversation: inferring and recording progress

- When work described in the conversation clearly completes a step, mark it ✅ in the working copy of the doc and state out loud which step was just marked complete (e.g. "Marking step 2.3 (\"draft the landing copy\") as done.") so the user can correct it if wrong.
- Never infer a whole phase as complete directly — a phase's marker is always derived from its steps. If every step in a phase is done, the phase is done as a side effect, not a separate judgment call.
- If a step or phase turns out unnecessary or can't be completed as planned, mark it ⚠️ skipped with a required one-line plain-language reason — ask the user for the reason if it isn't already clear, don't invent one.
- If a step is being deliberately postponed rather than skipped for good, tag it `(deferred: <plain-language reason>)` instead — it stays ⬜, not ⚠️.
- **Dependency check:** before marking a step ✅, check whether it declares `(blocked by: ...)`. If its blocker isn't ✅/⚠️ yet, flag this to the user instead of silently checking it off — completing steps out of order is allowed if the user confirms it, but shouldn't happen unnoticed.
- **Contradiction handling:** if something in the conversation conflicts with a step or phase already marked ✅/⚠️, don't silently overwrite the old mark. Reopen it (set back to ⬜ or 🟡), tell the user plainly what changed and why, and only then proceed.
- **Whenever a phase or step becomes genuinely stuck, gets deliberately postponed, or its concrete next action becomes clear or changes:** update its `(blocked by: ...)` tag, `(deferred: ...)` tag, and/or `Next:` line at the same time you save other changes, always in plain language a first-time reader can follow.
- If new information adds or changes a rule/fact/assumption (not a step), add or update it under the relevant Decisions Log subheading — don't fold it into a step's checkbox line.
- Save changes promptly (don't batch many turns of progress into one save) — see Saving below.

### 5. Saving (every write)

1. If file tools exist: re-read the file immediately before writing, even if it was just read this turn — something else may have changed it since. Merge this session's changes on top of the freshly-read content; if the same step was changed differently elsewhere, keep the freshly-read version's value and tell the user about the conflict rather than silently overwriting it. Then write the merged result.
2. If no file tools exist: there's nothing to re-read — print the fully merged doc in the reply and tell the user this reply is now the copy to save and paste back next time.

## Notes / Guardrails

- Don't fabricate step completion. If it's unclear whether something is actually done, ask rather than guessing.
- Don't create a new task without the user's confirmation of the drafted breakdown, including the pre-ticked completion guesses — both the plan and the "already done" claim are the user's to approve, not just Codex's to assume.
- Don't remove or renumber existing phases/steps of a task the user didn't ask to change; adding an exception or new step to an in-progress task is fine, silently restructuring it is not. A formatting pass may rewrite a step's wording to be more compact and specific, but must never change its count, order, or meaning.
- **Never let a real blocker, a deliberate deferral, or a next action sit only in prose without also adding the matching tag.** This is the single most common way this doc silently under-reports status — check for it on every write.
- **Never write these tags in internal shorthand.** Spell out the actual thing in ordinary words every time, even if it costs a few extra words.
- **Never confuse blocked with deferred.** `(blocked by: ...)` means something outside your control is stopping progress (flag it, it's a real risk). `(deferred: ...)` means it was a deliberate choice to postpone (calm, not a risk).
- Always use the ✅ / 🟡 / ⬜ / ⚠️ markers (never plain `[x]`/`[ ]`/`[~]`/`[!]`) when writing or displaying this doc's content.
- **Track and report only — never do the task's actual work uninvited.** Checking progress or updating the doc is not license to start performing the underlying task's steps unless the user separately asks for that.
- This skill is intentionally self-contained: it doesn't call, assume, or depend on any other skill's output. If another skill (like `progress-status`) happens to read the same doc format, that's a convention it chose independently, not a dependency this skill maintains.
