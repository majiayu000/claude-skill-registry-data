---
name: follow-up
description: "Ask one hard interviewer-style follow-up about the current coding-interview attempt, then wait for the user's answer. Use when explicitly invoked after a problem, approach, or solution is on the table."
---

# Follow-Up

Ask exactly one challenging but answerable follow-up, then stop.

## Choose the question

1. Read the current problem context: the attempt, its result status, the stated complexity, and any reasoning already demonstrated.
2. If the code has not been run, prefer an adversarial case, an invariant, or a failure prediction.
3. If correctness is uncertain, probe correctness or proof before optimization.
4. If the solution works, probe changed constraints, alternative data structures, scaling, complexity bounds, language behavior, or test design.

Do not answer the question until the user attempts it or explicitly asks for the answer. Return no preamble, hint, coaching, second question, or solution.

## Compose

Base skills, ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

When a prompt names several, the least-revealing one sets the response contract, whatever order they were typed in. Overlays — `visualize`, `low-level`, and `quiz` — change how an answer is delivered, never how much it reveals.

`follow-up` is the lowest rung, so it outranks every other base skill. `quiz` may make the single question multiple-choice. `low-level` may make it systems-aware. `visualize` may add only the minimum visual context needed to state it. Under every combination, ask exactly one question and stop without revealing its answer.

Do not edit, run, or submit the user's code without permission. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.
