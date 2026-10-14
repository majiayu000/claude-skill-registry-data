---
name: lcd
description: "Suggest the lowest-cost diagnostic print or log statement for a suspected bug in a LeetCode-style or coding-interview attempt, without revealing the fix. Use when explicitly invoked on attached, pictured, or pasted code."
---

# LCD

Identify the single cheapest observation that most sharply tests the likely broken invariant.

## Inspect the attempt

1. Read the visible problem, constraints, code, line numbers, errors, outputs, and relevant thread context.
2. Infer the language, attempted algorithm, likely invariant, and smallest set of values that distinguishes the plausible causes.
3. Ask one focused question only when cropped code or a missing problem rule makes the diagnostic unsafe.

## Return only

1. The exact source line, or a labeled `pasted line N` or `visible line N`, and whether to insert before or after the neighboring statement.
2. A snippet of at most three lines containing the diagnostic.
3. One short sentence naming the value or pattern that would confirm the suspected bug.

Prefer a single statement. If one statement cannot distinguish the plausible causes, say so and give at most two. Do not provide the fix, rewrite logic, add a debugging framework, or run the code.

## Compose

Base skills, ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

When a prompt names several, the least-revealing one sets the response contract, whatever order they were typed in. Overlays — `visualize`, `low-level`, and `quiz` — change how an answer is delivered, never how much it reveals.

Let an overlay influence what the diagnostic tests only where it fits the three-part output above. Never add a second answer block or reveal the repair.

Do not edit, run, or submit the user's code without permission. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.
