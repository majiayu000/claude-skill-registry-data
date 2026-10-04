---
name: keep-context-lean
description: "Use when context is filling up: big command outputs, long files, repeated reads, screenshots, planning a fan-out. Send the bulk to subagents and keep only summaries in the main thread. Estimate the cost before a loop that reads a lot."
disable-model-invocation: true
kind: principle
---

# Keep context lean

Context in a session is finite and you don't get it back. Every token that comes in should be worth having there.

When it fills up, reasoning gets worse, summaries lose detail, and eventually work stops. Time and compute you can spend more of. Context you can't.

## How

- **Send bulk to subagents.** Long command output, big files, screenshots, wide searches, anything you'd have to scroll. A subagent reads it and sends back the answer. The main thread gets the summary, never the raw payload.
- **Hand subagents pointers, not pasted content.** A file path and a question, not the file. They can read it themselves.
- **Don't read what you won't use.** Read the part of the file you need. If a file isn't needed for the task in front of you, skip it.
- **Keep the always-used stuff inline.** A template or reference the skill needs every time belongs in the skill file. Splitting it out costs a read each invocation.
- **Cap the scope.** Limit files per phase, set a turn budget, plan for the cost of the mechanism itself, not just the work.
- **Do the math before a loop.** Before reading a hundred files or running a command in a loop, estimate what it'll put in context. If the number is big, that's a subagent job or a script that writes to a file you grep later.

## You still own the result

Sending work out doesn't send responsibility out with it. Read the subagent's diff, check its answer against the real thing, write your own summary. Don't pass through what it said.

## The test

Before a tool call, ask what will come back and whether you need all of it in the thread. If you only need the answer, get someone else to read the output.
