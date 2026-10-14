---
name: quiz
description: "Run adaptive medium-difficulty retrieval and transfer practice based on a current LeetCode-style or coding-interview problem, and grade the answers. Use when explicitly invoked after a problem, attempt, or solution is available in the thread."
---

# Quiz

Test the most valuable unresolved reasoning without leaking a stronger solution.

## Build the next question

1. Inspect the problem, attempt, demonstrated reasoning, misconceptions, and active disclosure ceiling.
2. Read [references/quiz-design.md](references/quiz-design.md).
3. Select the highest-value unresolved invariant, counterexample, representation tradeoff, correctness hazard, hidden complexity cost, or changed constraint.
4. Ask one medium-difficulty multiple-choice question with three or four plausible misconception-based options, then stop without revealing the answer.

After the user answers:

1. Say `Correct` or `Not quite`.
2. Explain the governing invariant or mechanism in two to four sentences.
3. Explain why the strongest distractor fails.
4. Ask one adapted next question.

Prefer prediction and transfer over vocabulary recall. Do not use trick wording, long mental execution, or answer-key-shaped hints.

## Compose

Base skills, ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

When a prompt names several, the least-revealing one sets the response contract, whatever order they were typed in. `quiz` is an overlay: it changes how an answer is delivered, never how much it reveals. Preserve the active ceiling in the stem and in every option.

- With `visualize`, build one self-contained interactive HTML quiz of four to six questions, answers hidden until submission, and visuals only where state or spatial reasoning materially helps.
- With `low-level`, test the consequences of representation, equal-Big-O implementation choices, runtime hazards, hidden space, or amortized costs.
- With `follow-up`, ask exactly one tailored question and stop.
- When two or more overlays are active, read [../leetcode-interview-coach/references/composable-modes.md](../leetcode-interview-coach/references/composable-modes.md) if it is installed.

Do not edit, run, or submit the user's code without permission. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.
