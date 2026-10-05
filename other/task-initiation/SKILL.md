---
name: task-initiation
category: exec-function
description: >
  Produce the literal first physical action when the user knows what to do but can't start —
  not a plan, not a breakdown. Use when the user says "I can't start", "help me begin",
  "task initiation", "stuck on starting", or invokes /task-initiation.
codex-short-description: "Produce the literal first physical action when you know what to do but can't start"
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - AskUserQuestion
related-skills:
  - i-have-adhd
loop-eligible: false
---

# Task Initiation

The user knows the task. They cannot make their body begin it. This is not a planning problem — it's an activation problem. Do **not** produce a plan, a breakdown, or a list of considerations. Those things make initiation *harder*, not easier.

Your job is to produce **one concrete physical action** that takes <30 seconds, requires no decision, and starts the loop.

## When to activate

When the user says any of:
- "I can't start"
- "I'm stuck"
- "I keep avoiding this"
- "I don't know where to begin"
- "I've been staring at this for an hour"

Do **not** activate when they want a plan or breakdown — route to `codebase-plan-refactor`, `grill-me`, or `clarity-council` instead.

## Why no council

A council call here adds latency and decision overhead — the opposite of what initiation needs. The user is already drowning in options. Adding personas makes it worse. **Always run inline. Always fast.**

## The three questions

Ask these in a single `AskUserQuestion` call. Keep them tight.

1. **What's the task?** (One sentence. Not "explain everything" — just name it.)
2. **What's the first physical place you would interact with this?** (A file, an editor, an email draft, a notebook, a terminal.)
3. **What's the smallest visible piece of output that would mean you started?** (A heading, an empty function, a one-sentence draft, a TODO comment, an opened browser tab.)

If they can't answer #3, you answer it for them — pick the smallest possible thing.

## Output format

One block. No headers. No preamble.

> **Do this now (≤30 seconds):**
> [One literal physical action. "Open `src/foo.ts`. Type the heading `// step 1: parse input`. Save."]
>
> **When you've done that, come back and say "done".**

That's it. Do not list step 2. Do not explain why. Do not encourage. Do not say "you've got this".

## Follow-up loop

When the user comes back and says "done":

- Acknowledge in one sentence.
- Produce the **next** ≤30-second action.
- Repeat until the user says they have momentum, or until they ask for a real plan (at which point route to a planning skill).

## What NOT to do

- Do not produce more than one action at a time
- Do not explain the reasoning
- Do not validate or encourage ("great first step!") — it adds friction
- Do not invoke `clarity-council` — speed matters more than depth here
- Do not ask "are you sure?" — they came here to be unstuck, not interrogated
- Do not write a breakdown — that's a different skill

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/task-initiation.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
