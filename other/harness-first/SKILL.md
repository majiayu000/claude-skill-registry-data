---
name: harness-first
description: Diagnose and fix an unreliable, expensive, or unsafe LLM agent by auditing its harness (golden set, judge, cost caps, data layer, action approvals, tracing) before blaming or swapping the model. Use when someone says an agent is "burning tokens", "hallucinating", "brittle", gives inconsistent answers, asks whether to switch to a cheaper/better model, or wants to ship an agent or prompt change to customers.
---

# Harness first

A model is an engine. Most "model problems" are a missing harness: nothing defines a correct output, nothing checks changes, nothing caps spend, the data has no agreed definitions, actions have no approval, and there are no traces to find the bad call. Audit that before touching the model.

## 1. Reproduce the symptom from evidence, not vibes

- Read the agent code the symptom touches: the loop, tool definitions, prompt assembly, data access, side-effecting tools.
- Read whatever logs/traces/transcripts exist. Aggregate them (per conversation, per tool, per error): who spends the tokens, which calls fail, which answers are wrong. A few outliers usually dominate.
- State the root cause as a mechanism with evidence (file:line, log ids, numbers you computed). "The model is bad" is not a mechanism.

Common mechanisms:
- **Token burn:** loop with no max-iterations, retry on a deterministic error, full history or a huge tool result resent every turn, no caching of stable context.
- **"Hallucination":** the agent faithfully used an ambiguous or wrong source (two tables/fields with the same name and different meaning, stale doc). Recompute both numbers yourself to prove it.
- **Brittleness:** prompt changes shipped with no regression set; behavior that only the author checked by hand.

## 2. Score the six harness parts

For each, mark **present / partial / missing** with the evidence you found:

| Part | Present means |
|---|---|
| Golden set | ~20+ cases with expected answers/constraints, drawn from real traffic, incidents, and edge cases |
| Judge | deterministic checks first (numbers, policy rules, forbidden content), LLM-rubric only for what code can't check; runs on every prompt/model/tool change |
| Cost governance | hard token/cost caps per user and per workflow, max iterations per run, graceful stop with a message |
| Data layer | read-only credentials for reads, a data dictionary that defines each metric/field the agent may use |
| Action safety | irreversible or external actions (send, pay, delete, write, refund) are reversible or gated by human approval |
| Tracing | every model and tool call logged with conversation id, workflow, input, output, tokens, cost, latency, error |

## 3. Decide before building

- **Never recommend a model swap without eval evidence.** If someone asks "should we switch models?", the answer is: fix the mechanism, then run the golden set on both models and compare quality and cost. Say what the fix alone is expected to save, with your numbers.
- **Never approve shipping a prompt/agent change without a golden-set run.** If recorded outputs exist, score them against the expected answers yourself and report failures by case id.
- Safety gaps (ungated side effects, write access on a read path, leaking internal data) are blocking, even when nobody asked about them.

## 4. Build the minimum harness, in this order

1. **Stop the bleeding:** max iterations, no retry on non-transient errors, truncate/summarize large tool output, hard per-run cost cap.
2. **Gate side effects:** approval step or draft mode for irreversible tools; read-only connection for query tools.
3. **Golden set file** (`evals/golden.jsonl` or similar): input, expected answer or constraints, source (log id / incident / policy clause). Include the cases that just failed.
4. **Judge script** that runs the golden set and prints pass/fail per case plus totals. Deterministic checks before LLM grading.
5. **Data dictionary** for every metric the agent reports (definition, source table/field, exclusions).
6. **Tracing** fields listed above, if missing.

Write real files, not a description of files. Run what can run and report the result.

## 5. Report

- One-line answer to the question actually asked (e.g. "Don't switch models yet: 3 runs stuck in a retry loop spent 71% of tokens").
- Root cause with evidence and numbers.
- Harness scorecard (the six parts).
- What you changed or created, and what you ran.
- Blocking risks, then a short prioritized next-steps list.

## Credit

The method this Skill follows comes from a public post by Mark Ajzenstadt (@mardehaym): https://x.com/mardehaym/status/2099562230647804152. The argument is theirs; the procedure, the wording and the evaluation here are Edge's own, and the author did not review them.
