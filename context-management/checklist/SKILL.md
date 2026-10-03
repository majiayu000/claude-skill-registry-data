---
name: checklist
description: Q&A checklist to run BEFORE starting any new work (new project, feature, model, document, tool). Several rounds of questions agree on goal, direction, don'ts, scope, done-criteria and constraints; the agreement is saved as a BRIEF, approved, and checked against at the end. Also run on "checklist", "ask me first", "let's set the direction", "questions first", "문답", "체크리스트". Works in the user's language.
argument-hint: "[what you want to do, one line]"
---

# checklist — ask before you build

Goal: reach an agreement the user can **see and correct** before doing the work. Questions are not a ritual;
each one should pull out a decision that changes the direction or quality of the result.

**Language:** write every question, option, summary, BRIEF body, field file and rule in the language of the
user's latest message. This file is in English only for maintenance. Built-in field files are in English —
translate their questions when you ask them. BRIEF front-matter keys stay in English (the hook reads them).

**Paths:** the session context lists them under "checklist paths". If it doesn't (skill installed without the plugin),
use `~/.claude/checklist/rules.md`, `~/.claude/checklist/fields/`, `~/.claude/checklist/briefs/`, and the `fields/` folder
next to this file for built-in fields.

## 0. Classify — say it first
Say in one line: "Treating this as new work — questions first" or "This continues BRIEF X — proceeding as agreed".
For a continuation, read the BRIEF and start working. When unsure, treat it as new work.

## 1. Research first (read-only, before asking)
**Don't ask for facts — look them up. Ask only for decisions.**
- Folder structure, existing files, repos, README / CLAUDE.md, memory, related BRIEFs (paths are in the session context)
- Installed tools and versions, programs that are open
- Use what you find to make options **concrete** (e.g. "There are 3 draft specs in ./docs — which one do we start from?").
- If research takes long, ask the questions that don't depend on it first.

## 2. Question rounds — always enough of them
For new work, **at least 3 rounds**, more if needed. One round = one AskUserQuestion call (up to 4 questions).

Treat the decisions as a tree: earlier answers change later questions. Put in one round only the questions that
can be answered now; defer anything whose options depend on another answer in the same round.

| Round | Cover |
|---|---|
| 1 | **Goal and output**: what and why, final form, who uses it, which field, starting material |
| 2 | **Direction and don'ts**: preferred approach / style / tech, references, priority (speed / quality / simplicity), forbidden list |
| 3 | **Field questions**: from the matching field file (see below), only what research couldn't settle |
| 4 | **Scope, done-criteria, constraints**: in / out this time, how we verify "done", deadline, environment, where to save |

Finding the field file: look in the user fields folder first, then the built-in fields folder (both listed in the
session context under "Known fields"). Pick the closest match; if nothing fits, ask general questions for that field.

Writing questions:
- **Put the recommended answer first, labelled "(Recommended)"** (in the user's language), with a one-line reason.
  Picking only the recommendations should still give a good result.
- Options must be **concrete** (numbers, file names, examples). No "whatever works" options.
- **Don'ts are always multiSelect**, offering the common mistakes and over-work typical of this field.
- Done-criteria must be **checkable sentences** ("looks nice" → "loads under 1 s on the test page, zero console errors").
- If an answer has "?", ambiguity or a contradiction, write your interpretation and confirm it next round. Don't fill gaps with guesses.
- If an answer conflicts with memory or the user rules, point out the conflict and ask.
- After each round, show "What I understand so far" in 2–4 lines, then continue.

## 3. Summary and corrections
When every branch is settled, show a summary split into two parts:
- **What you told me** — decisions from answers
- **My assumptions (please confirm)** — things I filled in without an answer. If not empty, confirm them in the last question.

Last question: "Proceed as is / I have changes (Other)". Apply changes and summarize again.
**Before approval: no file edits, installs, generation, or sending anything out.**

## 4. Save the BRIEF
Once approved, save it in the `brief-template.md` format to `<BRIEFs folder>/YYYY-MM-DD_<project>_<short-title>.md`
and tell the user the path. `cwd` in the front matter is the absolute work folder (the next session opened there
gets pointed to it automatically).

## 5. Learn the field
- If no field file matched: after the BRIEF is saved, draft `<user fields folder>/<field>.md` from the questions you
  actually asked and the don'ts the user picked (format: like the built-in field files, in the user's language).
  Show the draft and save it **only if the user approves**.
- If a field file matched but this round produced new useful questions, propose appending just those lines.

## 6. While working
- If you're about to break a "don't" in the BRIEF, stop and ask.
- When a new decision comes up, ask, then add one line to the BRIEF's "Decision log".
- If scope grows, stop and say so (a size that went up never goes back down).
- Repeated corrections or "from now on…" from the user → propose a user rule (see the session rules).

## 7. Done check — always before reporting done
Re-read the BRIEF and report as a table:

| Done-criterion | Result | Evidence (measurement, screenshot, file) |
|---|---|---|
| … | ✅ / ❌ / ⚠️ not verified | … |

- Check each "don't" in one line: not broken.
- If anything is ❌ or ⚠️, don't call it done; list it as remaining work.
- Only when the user says it's finished, set the BRIEF front matter to `status: done` (never close it yourself).
