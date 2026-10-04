---
name: human-ai-async-work-planner
description: Plan what the human should do while Codex or another AI/code agent is running. Use before or during long-running AI tasks, background coding-agent work, tests, builds, rendering, searches, generation, benchmark jobs, or any workflow where the user may have their own queue, hidden context, limited attention, or interruptible tasks to advance asynchronously.
---

# Human AI Async Work Planner

Use this skill to turn AI waiting time into a respectful human-side plan. The goal is not to maximize productivity or spawn more agents; it is to ask whether the human has their own queue, protect the active AI task from conflicting edits, and choose an interruptible next action.

## Role In The Calling Task

Run this skill as a pre-flight or waiting-state companion for another task:

1. The calling task identifies that AI work may take noticeable time.
2. This skill checks the human-side queue and hidden context.
3. This skill returns a short human lane, AI lane, do-not-touch boundary, and return checkpoint.
4. The original task continues; this skill does not replace the task skill, completion loop, or subagent plan.

Do not use this skill as a generic time-management coach. Keep the advice local to the current AI run and the user's stated situation.

## Trigger Heuristics

Use this skill when any of these are true:

- Codex is about to run a task that may take more than about 1 minute.
- The task involves tests, builds, PDF/PPT render QA, browser screenshots, image generation, web research, benchmark jobs, repo scans, or long file generation.
- The user asks what they can do while the AI is running.
- The user may have external commitments, material only they can supply, or decisions only they can make.
- The AI result will need human review, acceptance criteria, source material, or follow-up prompts.

Skip this skill when the expected wait is very short, the next step requires the user's immediate approval, or asking would interrupt a simple task more than it helps.

## Human Queue Check

Start by respecting that the human's waiting time may not belong to the current AI task. Ask one concise question when the answer would change the recommendation:

```text
I may be running for about <time>. Do you have another real-world or project task you want to advance during that window, or should I suggest something related to this AI task?
```

If the user names another task, convert it into an interruptible micro-plan. If the user has no separate task, suggest work that prepares for reviewing or continuing the current AI task.

## Use Deep Interview Sparingly

Call or emulate `codex-deep-interview` only for missing human-side context that materially changes the plan. Ask at most one question at a time, and usually no more than three total.

Useful human-side facts:

- available time window
- current energy level
- whether the user wants deep work, light work, admin work, or rest
- external deadlines, meetings, messages, advisor/client expectations, or real-world constraints
- materials the AI does not have yet
- what the user wants to judge when the AI returns

Do not ask for discoverable facts. Inspect files, task state, logs, or repo context yourself when available.

## Waiting Window Rules

Use the expected wait to choose a humane task size:

- Under 30 seconds: do not context-switch; just wait or observe.
- 1-5 minutes: choose tiny tasks such as writing the next acceptance question, checking a source path, or making a note.
- 5-20 minutes: choose bounded tasks such as drafting review criteria, finding missing material, outlining follow-up prompts, or answering messages.
- Over 20 minutes: choose a separate task only if it has a clear pause point and a return checkpoint.

Prefer tasks that are interruptible, non-conflicting, and either feed the current AI task or preserve the user's own priorities.

## Conflict Boundaries

Always name what the human should not touch while the AI is running:

- files or artifacts the AI is currently editing or generating
- conclusions that depend on unfinished AI output
- shared stage artifacts that require confirmation order
- commands that could invalidate the AI run, such as deleting temp output, changing branches, or rewriting inputs

If the human-side task would conflict with the AI lane, recommend a different task or ask the human to pause the AI first.

## Output Format

Return a compact plan:

```text
AI lane:
- <what Codex/AI is doing>

Expected wait:
- <rough duration or unknown>

Human queue check:
- <user has separate task / no separate task / not asked because...>

Human lane:
- <1-4 interruptible actions>

Do not touch:
- <files, artifacts, branches, claims, or external state to avoid>

Return checkpoint:
- <when the human should come back>

Resume prompt:
- <short prompt the user can send when they return>
```

## Hook Relationship

A hook can remind Codex to consider this skill, but should not be treated as a reliable way to execute the skill body.

Use `UserPromptSubmit` hooks to inject lightweight `additionalContext`, such as:

```text
If this prompt starts a long-running AI task, consider using $human-ai-async-work-planner before execution to ask whether the user has another task queue and to define a return checkpoint.
```

This skill includes an optional helper hook:

```text
scripts/human_ai_async_user_prompt_hook.ps1
```

Register that script in `~/.codex/hooks.json` for a user-level advisory hook, or in `<repo>/.codex/hooks.json` for a project-only advisory hook. Keep it advisory: it emits `additionalContext`; it should not deny tools or block execution.

Do not use a global hook to force this skill for every prompt. That would create friction on short tasks. If a hook is used, keep it advisory and pattern-limited to long-running task language such as "run", "benchmark", "render", "generate", "search", "build", "test", "while you work", "background", or "long task".

Use blocking hooks only for safety or stage gates, not for ordinary waiting-time planning.
