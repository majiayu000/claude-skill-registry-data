---
name: feynman-method
description: Run the Feynman Method to make something the user just read or learned actually stick. A three-step interactive loop — (1) map the 5 load-bearing ideas, (2) write 12-year-old model answers then have the user explain each in their own words, (3) grade their explanations and pinpoint the biggest gap. Use when the user says they "just read about X", wants to "make it stick", "really understand", "learn / retain / internalize" a topic, asks to be "quizzed" or "tested" on their understanding, mentions "Feynman" or "explain it back", or wants to study material rather than just summarize it.
---

# Feynman Method

A learning loop that converts familiarity into understanding. Reading creates familiarity; *explaining* creates understanding; *being corrected* closes the gaps. This skill runs all three.

## The non-negotiable rule: this is interactive

The skill is worthless if run as a monologue. **Stop and wait for the user's reply at the end of Step 2.** Do not pre-fill the user's explanations, do not run all three steps in one response, and do not move to Step 3 until the user has actually answered. The whole value is in the user doing the explaining.

## Voice for every step

- Write like you are talking to a smart 16-year-old (Step 1) or a 12-year-old (Steps 2–3).
- No jargon. No field background assumed. If a technical term is unavoidable, define it in plain words on the spot.
- Concrete everyday examples beat abstract definitions.

## Identify the topic first

The topic comes from what the user just read or learned. If it's clear from context (they pasted an article, named a subject, or it's the thread topic), use it. If it's ambiguous, ask one short question — *"What's the topic you want to lock in?"* — then proceed.

## Step 1 — Concept Map

Find the handful of load-bearing ideas. Most topics have dozens of facts but only ~5 ideas everything else hangs on. Surface those.

List the **5 most important ideas**. For each:

- **Definition** — one sentence, simple English.
- **Why it matters** — what it does in the real world.
- **The test question** — the one question they should be able to answer if they truly understand it.

Then continue into Step 2 in the same turn — the Step 2 model answers are useful to read before the user attempts their own — and stop at the end of Step 2's prompt.

## Step 2 — The 12-Year-Old Test

For each of the 5 ideas, write a **model answer** first, so the user has a target. Use this exact format:

```
IDEA 1: [name]
12-year-old version:
[explanation in words a 12-year-old knows]
Everyday example:
[a concrete, familiar example]
```

After all 5 model answers, ask the user to write **their own version** of each idea, in their own words, as if teaching a 12-year-old.

**Then stop. Wait for their answers before continuing.** Do not write Step 3 yet.

## Step 3 — The Gap Finder

This is the highest-value step: a book can't tell the user what they got wrong, but you can. The user has now pasted their 5 explanations. Play a **strict but kind tutor**.

For each explanation:

- Mark it **STRONG**, **WEAK**, or **WRONG**.
- If WEAK or WRONG: state exactly what they misunderstood — be specific, name the error, don't soften it into mush.
- Give the corrected version in 12-year-old words, using a **different analogy than Step 2** (a fresh angle catches what the first framing missed).
- Ask **one follow-up question** that would prove they now understand it.

Be honest in the grading. Marking a weak answer STRONG to be nice defeats the purpose — the user came here to find gaps, not to be flattered.

End with exactly this prompt:

> **Which idea should you restudy first to fix the biggest gap?**

— and give your recommendation, pointing at the single weakest spot.

## Running a fresh round

If after Step 3 the user reworks a weak idea and explains it again, re-grade just that idea (Step 3 logic) with another new analogy. Loop until each idea is STRONG.
