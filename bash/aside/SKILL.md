---
name: aside
description: Mid-task side question handler. Freezes the active task state, answers a side question without state mutation, then resumes the task exactly where it stopped. Lighter than /checkpoint save. Use when user says "aside", "quick question", "side question", "while we're at it", "before you continue", or interrupts mid-implementation with an unrelated question. For new scope, use /plan; for a retro, use /retro; for a true context switch, use /checkpoint save.
argument-hint: "/aside <question>"
allowed-tools: "Read, Grep, Glob, AskUserQuestion"
disallowed-tools: "Write, Edit, MultiEdit, Bash"
sensitive: false
---

Sidebar conversation that preserves the in-flight task. Read-only by design: no file edits, no shell commands. Answer, then return to the work that was interrupted.

## Overview

Mid-task interruptions are a documented source of dropped work. The common failure modes are forgetting where work stopped, mixing the side answer's state into the main task, and silently switching scope without the user noticing. This skill defines an answer-only protocol: freeze, answer, resume.

## When to Use

- User asks a clarifying question while implementation is in progress
- User asks "before you continue, what about X?" or "quick question"
- A side topic arises that does not change the active task's scope
- Read-only investigation is enough to answer

Do NOT use when:
- The interruption changes the active task's scope (use `/plan` instead)
- The interruption ends the task (use `/checkpoint save` instead)
- The question requires editing files (use the normal flow, not aside)
- The user is asking for a retrospective (use `/retro`)

## Process

1. **Freeze.** State the active task in one sentence and the immediate next step that was about to execute. Do not edit, do not run shell commands.
2. **Answer.** Read-only investigation (Read, Grep, Glob, ToolSearch) followed by a direct answer. Keep the answer scoped to the question.
3. **Confirm scope unchanged.** Ask whether the answer changes anything about the active task. If yes, exit aside and surface the scope change explicitly.
4. **Resume.** Restate the active task and the immediate next step, then continue exactly where step 1 froze.

## Common Rationalizations

- "I will just make a small edit to demonstrate": no edits in aside. If demonstration requires edits, the side question is not a side question.
- "I will skip the freeze step, it is obvious": the freeze IS the value. Skipping it is how mid-task state gets lost.
- "I can answer this without reading anything": aside still requires verification per CLAUDE.md Anti-Hallucination. Read the file before answering.
- "The user will remember where we were": the user does not need to. The skill does that work.

## Red Flags

- About to call `Write`, `Edit`, `MultiEdit`, or `Bash` while in aside
- About to answer without naming the active task first
- About to resume without restating the next step
- Side answer that turns into a sub-implementation
- More than one round-trip of aside without re-confirming the active task is unchanged

## Verification

- Active task is named in writing before the answer
- Answer cites a file path or grep result (no fabrication)
- Scope-change confirmation question was asked at step 3
- Resume statement repeats the immediate next step verbatim
- No write operations occurred between freeze and resume
