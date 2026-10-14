---
name: best
description: "Reveal and teach one to three interview-canonical complete solutions to a LeetCode-style problem, including derivation, correctness, complexity, tradeoffs, and code. Use only when explicitly invoked, because this workflow intentionally reveals full solutions."
---

# Best

Treat explicit invocation as authorization to reveal the complete interview-ready solution space.

## Inspect the problem

1. Read the visible problem, constraints, attempted code, language, and relevant thread context.
2. Infer the strongest useful language choice from the user's attempt.
3. Ask one focused question only when a missing problem rule changes the correct solution set. Otherwise state the assumption and proceed.

## Teach canonical solutions

1. Present one to three genuinely distinct interview-worthy approaches, strongest default first. Omit redundant inferior variants.
2. For each approach, give:
   - the recognition cue;
   - a short derivation;
   - a compact correctness argument and the important edge cases;
   - time and auxiliary-space complexity; and
   - concise benefits, tradeoffs, and when to choose it.
3. Provide clean standalone code in the user's language when code materially aids learning. Return it unmarked: this is a solution taught from scratch, not a patch against a file the user already has, so `NEW` and `MOD` markers would land on every line and distinguish nothing.
4. End with two or three interview-ready sentences the user could say aloud to justify the chosen approach.

Emphasize derivation and proof rather than memorized pattern labels.

## Compose

Base skills, ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

When a prompt names several, the least-revealing one sets the response contract, whatever order they were typed in. Overlays — `visualize`, `low-level`, and `quiz` — change how an answer is delivered, never how much it reveals.

`best` is the highest rung, so any other base skill named alongside it lowers the ceiling and this skill defers to it. Do not reveal canonical solutions under a lower ceiling.

Do not edit, run, or submit the user's code without permission. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.
