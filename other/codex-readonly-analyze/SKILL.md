---
name: codex-readonly-analyze
description: Use when the user asks to analyze, investigate, explain why something happens, trace architecture or behavior across files, rank plausible causes, or understand repo impact before changes; perform read-only repository analysis with evidence-vs-inference boundaries, confidence levels, and concrete file references.
---

# Codex Readonly Analyze

Answer repository questions through grounded read-only analysis. This is the native Codex adaptation of OMX `$analyze`: keep ranked synthesis, explicit confidence, concrete file references, and evidence-vs-inference separation; omit OMX runtime routing.

## Contract

- Do not edit files.
- Do not turn the answer into an implementation plan.
- Do not silently switch to fixing.
- Do not overclaim certainty.
- Do not ask the user for facts that are discoverable from the repo.
- If the answer needs current external facts, say so and use the appropriate research path.

## Workflow

1. Restate the question in one sentence.
2. Identify the smallest likely evidence surface: files, configs, tests, generated artifacts, docs, task cards, or logs.
3. Read direct evidence first with `rg`, `rg --files`, and focused file reads.
4. Expand only when competing explanations remain plausible.
5. Rank explanations by support.
6. Separate evidence, inference, and unknowns.
7. Return a concise synthesis with file references and confidence.

## Parallel Exploration

Use native subagents only when the question is broad enough to benefit from bounded independent lanes. Each lane must be read-only and answer one concrete sub-question. The main thread remains responsible for synthesis.

## Output Shape

- Question
- Ranked synthesis
- Evidence
- Inference
- Unknowns / limits
- Next discriminating read-only probe, if useful

For simple one-file questions, answer directly after enough reading.

## References

Read `references/analysis-quality-checklist.html` for the review checklist.
