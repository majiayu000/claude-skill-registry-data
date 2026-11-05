---
name: word-vomit
description: Turn a dump of the user's raw feedback, ideas, wishes and bug notes into planned work. Checks what is already planned, finds conflicts with the plans and the code, asks clarifying and priority questions with recommendations, updates or adds units in the planning batches, and records everything in planning/word-vomit/. Use when the user types /word-vomit or pastes a loose list of thoughts and wants it planned.
---

# Word vomit

The user pastes loose thoughts. Turn them into clear, placed, approved planning work. Planning only: never change code, never start implementation agents.

Read `planning/AGENTS.md`, `planning/batches/README.md` and `planning/EFFORT.md` first; their rules apply (no time estimates, effort scores, dependencies always in an earlier batch, one protocol or format change per batch, units done completely). The code repo is read only here.

## Steps

1. **Save the input first.** Create `planning/word-vomit/YYYY-MM-DD-<slug>.md` with the text verbatim under `## What was said`. Never edit the user's words.
2. **Split it into items.** One idea, wish, bug or opinion per item. Restate each in one plain line; mark guesses as guesses.
3. **Check the planning** for each item (`BATCHES.md`, `batches/`, `batches/proposed/`, `BACKGROUND.md`, `LATER.md`, `USER.md`, `DECISIONS.md`, `PLAN.md`, `research/`): **planned** (name the unit and batch), **partly planned** (what is missing), **decided otherwise** (quote the decision), or **new**. Use read-only subagents when there are many items; ask them for file:line evidence.
4. **Find conflicts**: between items; with units, decisions or the plan; with the code (architecture rules, existing systems, formats, protocols; give file:line). For each: the options and a recommendation with the reason.
5. **Ask the user** with AskUserQuestion, at most 4 questions per call, each standing on its own, the recommended option first and marked "(Recommended)". Ask about each conflict, each unclear item, and the **priority** of each new or changed item: breaking, user feel, user feature, developer tool, platform, or later. Repeat until nothing is unclear.
6. **Update the plans.**
   - Planned or partly planned: fold the item into the unit (steps, tests), re-score its effort, add `Added YYYY-MM-DD (word vomit <slug>): <what> because <why>`.
   - New: write a unit file (shape in `batches/README.md`) with steps, tests first, files, risks, effort. Split an enormous unit. Shared background goes to `BACKGROUND.md`.
   - Place by the answered priority (rules in `batches/README.md`); "later" goes to `LATER.md`. Update the batch tables and `BATCHES.md`.
   - A changed decision: update `DECISIONS.md` with the date and the reason.
   - An item about the workflow itself (how planning, batches, reports, reviews or passes work): change the rule, skill or number it is about, and log it in `DECISIONS.md` under "Workflow changes".
   - Run `python3 tools/check-links.py` and commit the planning repo, naming the word-vomit file.
7. **Write the record** in the word-vomit file: `## Items` (table: #, item, status before, result), `## Conflicts`, `## Questions and answers` (table: question, options with the recommendation first, answer), `## Changes` (each file, what and why). Add one line to `planning/word-vomit/README.md`, newest first.
8. **Report**: a short table of each item and where it is now, the decisions made, anything open, and one next action.
