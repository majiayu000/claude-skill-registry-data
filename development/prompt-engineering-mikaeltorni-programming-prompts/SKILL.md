---
name: prompt_engineering
description: >-
  v0.0.36 — Use when asked for prompt_engineering or when creating or editing AI
  instructions in prompt Markdown, including skills and judges. Keep prompts
  simple and improve the prompt and judge together using real model evaluations.
---

# Prompt engineering

Use for AI prompt Markdown, not ordinary documentation.

1. Read existing cases, benchmark results and failures. Reuse the suite; if missing,
   save a few inputs, independent expected results and a small runner.
2. Revise the main prompt and judge together. Keep both short, general and
   consistent. The judge checks requested behavior without extra requirements.
3. Calibrate the judge with a fixed, independently written correct/incorrect pair;
   do not ask a model to generate these controls. Keep calibration small and use
   the saved cases for broader coverage. Run the saved main
   prompt on every case and judge its answers too. For exact outputs, compare the
   candidate with the independent expected answer. Return reason and verdict in
   separate fields; parse only the verdict. Actually call both models; fail on any
   wrong answer or decision. Equality checks cannot replace model judge calls.
4. Reuse one evaluation path. Send saved instructions plus clearly marked input;
   keep candidate and reference in separate fields. Input contains only case text.
   Avoid nested shell quoting and extra dependencies. For Codex, send stdin with:
   `codex exec -m MODEL -c 'model_reasoning_effort="low"' --output-last-message FILE - >/dev/null`
   Read FILE only; helpers return only the answer or parsed verdict, not logs or
   explanation. Save answers and verdicts. Keep the returned session ID and use
   its continuation tool until exit or timeout; an empty command does not wait.
   Do not interrupt a running evaluation because of retry warnings.

If a check fails, inspect the submitted text, repair the cause, update both prompts
and rerun the same cases until all pass. Report unfinished checks only for genuine
execution blockers; recovered warnings with completed responses are not blockers.
