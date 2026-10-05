---
name: analytical-thinking
description: >
  Use this skill when the user asks for analytical thinking (including naming it
  or directing use/apply/run with obvious misspellings; decisive) or wants a
  structured breakdown—decomposing the problem, defining metrics and
  hypotheses, organizing evidence, and synthesizing findings with explicit
  uncertainty. Use for quant-style reasoning framing, root-cause trees, decision
  tables, or comparable structure, including informal or incomplete data asks.
  Skip when they want open-ended idea spray with no measurement or hypothesis
  angle, or a short verdict with no decomposition requested.
license: MIT
metadata:
  author: ysskrishna
  version: "2026.5.17"
---

# Analytical Thinking

Clarity beats cleverness. End with answers tied to structure and stated confidence.

**How to run it with this skill:** one clearly headed section per step in this order: Frame → Decompose → Hypotheses → Evidence → Synthesis. Insert **Options matrix** only when Setup calls for it (after Evidence, before Synthesis).

---

## Setup (run before starting)

In one short block:

1. **Analytical question** — precise, ideally falsifiable
2. **Default pass** — Frame → Decompose → Hypotheses → Evidence → Synthesis (state this line)

If data availability or definitions are missing, ask at most 3 questions in one message, then proceed. Note any remaining gaps or working guesses in plain language (no bracket tags in Setup).

If the user is **choosing among concrete alternatives**, after **Evidence** insert **Options matrix**: rows = options, columns = criteria (state weights if any), qualitative scores (− / 0 / +) with one-line justification per cell — then finish with **Synthesis**.

---

## The Steps

### Frame

**Question type** (estimate, compare, explain, predict, optimize). **Unit of analysis** and **baseline** (even if hypothetical).

### Decompose

Tree or table: factors, drivers, or workstreams. Each child node should be **MECE-ish** (mutually exclusive where it matters; collectively exhaustive enough for the decision).

### Hypotheses

Ranked **H1, H2, H3** — what would we expect to observe if each were true? What would **falsify** each?

### Evidence

For each hypothesis: **Observation:** … — **Strength note:** one short sentence on how much this observation supports or undermines the hypothesis and the main limit (no Strong/Moderate/Weak labels). **Caveat:** …

If no real data, run a **thought experiment** section instead — label bullets `[THEORETICAL]`.

### Synthesis

1. **Answer** — direct response to the analytical question
2. **Key uncertainty** — what single unknown swings the answer most
3. **Next data / step** — what to collect or run next

---

## Execution Rules

1. Do not conflate **Hypotheses** and **Evidence** in the same bullet list.
2. Numbers: if inputs are guessed, show **ranges** and label `[ESTIMATED]`.
3. Prefer **structure** over long prose.

---

## Checklist (verify before responding)

- [ ] Setup: analytical question + default pass (note if Options matrix used)
- [ ] Frame states question type and baseline
- [ ] Decompose is scannable (tree or table)
- [ ] Hypotheses have falsifiers
- [ ] Evidence (or `[THEORETICAL]`) mapped to hypotheses
- [ ] Synthesis: answer, uncertainty, next step
