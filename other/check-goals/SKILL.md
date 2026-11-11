---
name: check-goals
description: >-
  Use when the user asks whether the goals of the CURRENT session are met —
  lists everything they asked for, gathers evidence for each item and reports
  met or not met, changing nothing. Not for auditing how the session went — use
  reflect.
---

<!-- GENERATED FROM framework/atoms/check-goals.md via scripts/generate-skill-composites.ts — DO NOT EDIT BY HAND -->

# Check Session Goals

## Overview

Compares what the user asked for in this session with what exists now. Every
goal gets a status backed by evidence gathered at check time, and the report
opens with one verdict line. The check reads; it never repairs.

## Context

<context>
A session usually ends when the agent says "done". That sentence is a claim,
and so is a ticked box in a task file. This skill replaces the claim with a
check: it restates each goal in the user's words, looks at the project as it
is now, and says which goals hold. It answers WHAT was delivered. HOW the
session went — mistakes, wasted context, rules to tighten — is a different
question and belongs to the reflection skills.
</context>

## Rules & Constraints

<rules>
1. **Read-only**: do NOT fix an unmet goal, edit a file, tick or untick a
   checkbox, commit, or push. Commands that only read or verify (tests, a
   project check, `grep`, `git status`) are allowed. If such a command leaves
   files behind, say which.
2. **Goals come from the user**: a goal is something the user asked for in
   this session, or an item of a task file the session worked on. Your own
   ideas, nice-to-haves and side fixes are not goals. Never invent a goal to
   have something to report.
3. **A claim is not evidence**: your earlier "done", a ticked checkbox and a
   passing run from before later edits prove nothing. Evidence is what you
   observe now.
4. **Three honest statuses**: when a goal cannot be checked from here, it is
   `not verified` — never `met`.
5. **Planning**: track the goals with a task management tool (e.g.
   `todo_write`, `todowrite`, `Task`) when there are more than three.
</rules>

## Instructions

<step_by_step>

1. **List the goals of the session**
   - Go through the user's messages in this session in order, the invocation message included. Each thing the user asked for is one goal. Write it in the user's own words, shortened only where nothing is lost.
   - A later instruction replaces an earlier one it contradicts. A goal the user cancelled is kept in the list with the status `withdrawn` and is not checked.
   - A message that only answers your question, approves a step or picks an option adds no goal of its own; it shapes the goal it belongs to.
   - If the session worked on a task file (the `tasks` role from the project instructions), every item of its Definition of Done is a goal as well. Merge an item with the user's request it restates.
   - If you kept a task list in this session, an entry the user asked for and you never finished is a goal.
   - No goal found — the session held only questions and answers, or the conversation is not available to you → say so in one line and skip to the last step. Do NOT ask the user to dictate the goals.

2. **Gather evidence for each goal — now**
   - Choose the cheapest observation that would fail if the goal were not met:
     - a Definition-of-Done item with an evidence command → run that command;
     - a change in behaviour → run the test that covers it, or the project's check command once for all goals it covers;
     - a file, section or setting that must exist → read it or `grep` for it;
     - an answer, an explanation or a report the user asked for → find the message that delivered it;
     - something outside this machine (a deploy, a sent message, a CI run) → query it if a command for that exists.
   - Reuse a result from earlier in this session only when no file it depends on changed afterwards. Otherwise run it again.
   - Run independent read-only commands together where the tool allows it.
   - Do not stop at the first unmet goal: check all of them.

3. **Give each goal one status**
   - `met` — the observation from step 2 confirms it. Name the observation: the command and its result, or the file and line.
   - `not met` — the observation contradicts it, or part of the goal is missing. Say exactly what is missing. A partly delivered goal is `not met`.
   - `not verified` — nothing available here can confirm or refute it. Say what the user can run or look at to settle it.
   - `withdrawn` — the user cancelled it in this session.
   - A ticked checkbox whose evidence command fails is `not met`, and the report says that the box is ticked.

4. **List the loose ends — apart from the goals**
   - Run `git status --porcelain` and, if the branch has an upstream, `git rev-list --count @{u}..HEAD`.
   - Report, each in one line and only when present: uncommitted changes made in this session; commits not pushed; background processes or sessions this session started that still run; a question of the user you never answered; a follow-up you promised and did not do.
   - A loose end does not change the status of a goal. Uncommitted work is not an unmet goal unless the user asked for a commit.

5. **Compose the report**
   - First line, exactly one of:
     - `Goals: all met (<N> of <N>)`
     - `Goals: NOT all met — <K> not met, <U> not verified, of <N>`
     - `Goals: none found in this session`
   - Withdrawn goals are not counted in `<N>`.
   - Then one entry per goal: the goal in the user's words, its status, and the evidence. Put `not met` first, then `not verified`, then `met`, then `withdrawn`.
   - Then the loose ends from step 4, or `Loose ends: none`.
   - Do not soften the verdict: no "essentially done", no "all met except". One unmet goal makes the first line `NOT all met`.

6. **TOTAL STOP**
   - Send the report from step 5 to the user as your final message; it is the whole output. Do not start on an unmet goal, and do not commit or push anything.
   - If a goal is `not met`, you may offer in one line to finish it. Then stop and wait for the user.
</step_by_step>

## Verification

<verification>
- [ ] Every goal traces to a user message or a Definition-of-Done item of this session; none was invented.
- [ ] Evidence for every `met` goal was observed after the last relevant change, and is named in the report.
- [ ] A goal that could not be checked is `not verified`, not `met`.
- [ ] The first line of the report is one of the three verdict lines.
- [ ] Nothing was edited, ticked, committed or pushed.
</verification>
