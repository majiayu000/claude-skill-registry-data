---
name: menu
description: Show the user what Alterbrain can do, grouped by goal with example prompts, which add-ons are installed or available to build, and answer "How do I…?" questions from the plain-language guides; use for "what can you do", "/menu", "help me get started", "how do I…" or when the user seems lost.
model: sonnet
effort: low
argument-hint: "[a group like study, email, jobs | how do I …]"
---

# Menu

Show what Alterbrain can do, in a short list the user can scan in ten seconds.

## When to use

- "What can you do?", "What can I ask?", "/menu", "I'm lost", "help me get started".
- "How do I …?" questions about using Alterbrain (tasks, Obsidian, updates, privacy, costs, git).
- After onboarding, to suggest first things to try.

## Before you start

1. No clarify needed: this skill only reads.
2. Read, quickly:
   - `references/groups.md` (the eight groups, their example prompts for studying and for working, and which groups to hide);
   - `config/brain.json`: `learner.kind` (if it is missing or empty, treat it as `mba` when `packs` lists `mba` or a `school` block exists; older installs) and `packs`;
   - whether any `vault/20_areas/courses/*/course.md` exists (names only);
   - the list of folders in `.claude/skills/` (installed skills; `my-*` ones are the user's own);
   - `system/blueprints/*.md` frontmatter only (`title`, `kind`, `status`, `risk`, `cost`);
   - `state/built.json` if it exists (blueprints already built);
   - `node system/scripts/routines.mjs list --json` if `vault/90_routines/` exists (scheduled jobs: names and status only; exit code 1 means something needs attention (an overdue, invalid or unreadable routine note), so read the output, it is not a crash; only skip it if it prints nothing usable);
   - `state/onboarding.json` status (only to add one line if setup is unfinished).
3. Never load the full text of every skill or blueprint. Frontmatter and first lines are enough.

## Steps

1. **Pick the mode from the argument.**
   - Empty, "what can you do", "help": **overview** (step 2).
   - A group name (study, assignments, email, jobs or contacts, documents, knowledge, build, settings): **one group** (step 3). A group that is hidden for this user (assignments, for someone who is working and has no course) gets one line: "Those are for coursework. Add a course with `/course new` and they appear."
   - Starts with "how do I", "how can I", "where is", "why does": **how-to** (step 4).
   - Anything else that is really a request ("draft an email"): don't show the menu. Do the request (or hand it to the right skill).
2. **Overview.** Output, in this shape and no longer than about 40 lines:
   ```
   Here's what I can do. Copy any example, or just ask in your own words.

   Study: /course, /study, /ask, /framework
     • "Explain opportunity cost using my own lecture notes."
     • …two more
   Assignments: /assignment
     …
   (the groups from references/groups.md that apply to this user)

   Your own skills: /my-case-summary (built 2026-10-01)        ← only if any my-* exist

   Available to build (say "build <name>"):
     Email: Email extras · Gmail send with approval · Outlook and Microsoft 365
     Study: Study extras · Smarter flashcard timing · Zotero
     …

   Ask "how do I …?" any time. Guides: tasks, Obsidian, safety, updates, privacy, costs.
   ```
   Rules:
   - **Pick the prompts by kind** (`references/groups.md`, "Which prompts to show"): the work variant for `professional`, the study variant for every other kind or an unknown one.
   - **Courses and Assignments** (`/course`, and the whole Assignments group) only when the kind is not `professional` or a course note exists.
   - Show installed skills by their `/name`. Leave out a skill that is not installed.
   - **Routines:** if any exist, one line under the groups: `Your routines: 3 active, 1 overdue (say "check my routines")`; add ", 1 note to repair" when the output lists an unreadable note. None: leave it out; if the user asks what routines are, say they are scheduled jobs (a weekly contacts check, a morning brief) kept as notes in `vault/90_routines/`, run by the Claude app, and show `routines.mjs suggest`.
   - Self-built skills: list `.claude/skills/my-*` and `.claude/agents/my-*.md` with a few plain words from their description.
   - **Available to build:** blueprints with `status: "available"` that are not listed in `state/built.json`. Use the plain `title`, grouped as in `references/groups.md`. Add "(higher risk)" after titles with `risk: "high"`. Do not explain each one here.
   - If onboarding is not `minimum_done` or `complete`, end with one line: "Setup isn't finished yet. Say `/onboard` when you have a few minutes."
3. **One group.** Show the group's skills with one plain sentence each (from their `description`), the three example prompts, and the related blueprints with their `cost` and `risk` in a few words. End with: "Want me to start one of these?"
4. **How-to.**
   1. List `system/docs/guides/*.md`. Read the frontmatter `title` and `summary` of each.
   2. Pick the one or two guides that match the question. Read only those.
   3. Answer in at most 8 short lines, in the guide's words where possible, as steps if it is a procedure.
   4. End with: "Full guide: `system/docs/guides/<file>.md`".
   5. No guide fits: answer briefly from what you know of Alterbrain (`system/core.md`), say "I don't have a guide for that yet", and if it is a repeated need, mention `/propose`.
5. **Offer one next step.** One line, matched to what you know about the user (courses in `vault/20_areas/courses/`, projects in `vault/10_projects/`, goals in `USER.md`). For example: "Your <course> assignment is due Friday. Want to start it with `/assignment new`?" Or, with no courses: "Your <project> is due Friday. Want me to list the next steps?"

## Outputs

- A short message in chat. Nothing is written to files. No tasks are created.

## Safety

- Read-only. Never build, install or change anything from the menu; hand over to `/build`, `/reconfigure` or the named skill, which ask first.
- "Check my routines" is a request, not a menu mode: run `node system/scripts/routines.mjs list` and `overdue`, show the result in plain words (name, schedule, host, last run, last result) and the fix for anything overdue. Read-only.
- Never show a blueprint as installed unless it is in `state/built.json`.
- Keep it short. If the answer is longer than the screen, cut it and offer "Want the details?"
