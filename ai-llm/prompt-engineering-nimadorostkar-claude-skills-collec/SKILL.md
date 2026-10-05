---
name: prompt-engineering
description: Use when writing or improving prompts for a language model. Covers instruction structure, examples, reasoning elicitation, output formatting, and systematically diagnosing why a prompt fails.
metadata:
  category: ai
  version: 1.0.0
  tags: [prompting, llm, few-shot, chain-of-thought, evaluation]
---

# Prompt Engineering

## Purpose

Write prompts that produce the right output reliably, and diagnose the ones that do not. Prompt engineering is an empirical discipline: the model's actual behavior, measured, beats any theory about what should work.

## When to Use

- Writing a prompt for a production feature.
- A prompt that works most of the time and fails unpredictably.
- Reducing token cost or latency without losing quality.
- Migrating a prompt between models.

## Capabilities

- Instruction design: role, task, constraints, and output contract.
- Few-shot examples, and selecting the ones that teach the boundary.
- Reasoning elicitation for tasks that need it.
- Output formatting and structured extraction.
- Failure diagnosis and systematic iteration.

## Inputs

- The task, and what a correct output looks like.
- Real failure cases from the current prompt.
- Constraints: latency, cost, and the model available.

## Outputs

- A prompt with an explicit output contract.
- An evaluation set of inputs with expected outputs.
- A measured success rate, before and after.

## Workflow

1. **Define correct before writing the prompt** — Twenty real inputs and their correct outputs. Without this, "improving" a prompt is a matter of opinion and you will optimize for the last example you looked at.
2. **State the task, the constraints, and the output shape** — Be specific about what to do, what not to do, and exactly what format the answer takes.
3. **Add examples that teach the boundary** — Two or three examples covering the ambiguous cases, not the obvious ones. An example of the hard case is worth ten of the easy one.
4. **Elicit reasoning only where it helps** — For multi-step reasoning, ask the model to work through it before answering. For classification and extraction, it adds latency and cost without improving accuracy.
5. **Measure, change one thing, measure again** — On the evaluation set. A change that improves one example and silently breaks three others is a regression that feels like progress.
6. **Handle the failure mode** — Decide what happens when the model returns something unparseable, refuses, or hallucinates a field. That path will be taken.

## Best Practices

- Specificity beats politeness. "Return exactly one of: approve, reject, escalate" outperforms "please try to categorize this appropriately".
- Put the instructions before the data for short inputs, and after for long ones — models attend more reliably to the end of a long context.
- Negative instructions are weakly followed. "Do not include a preamble" works less well than "Begin your response with the JSON object."
- Structured output (a JSON schema, a tool call) is far more reliable than asking for JSON in prose and hoping. Use the API's native mechanism.
- Long, elaborate prompts accumulate contradictions. When a prompt exceeds a page, look for instructions that conflict — the model is following one of them.
- Prompt improvements do not transfer across models. Re-measure after any model change; a prompt tuned for one is not tuned for another.

## Examples

**A prompt with an explicit contract and a boundary example:**

```text
You classify customer support messages for routing.

Categories (choose exactly one):
- billing      — charges, invoices, refunds, payment methods
- technical    — errors, outages, broken functionality, integration problems
- account      — login, permissions, plan changes, cancellation
- other        — anything not clearly covered above

Rules:
- If a message spans two categories, choose the one the customer needs
  resolved first to be unblocked.
- If the message is too vague to classify with confidence, return "other"
  with confidence below 0.5. Do not guess.

Respond with JSON only, matching this schema:
{"category": "billing|technical|account|other", "confidence": 0.0-1.0, "reason": "<one sentence>"}

Examples:

Message: "I was charged twice for March and I can't log in to check."
{"category": "account", "confidence": 0.8, "reason": "The double charge matters, but they cannot access the account to act on it, so access is the blocker."}

Message: "hey"
{"category": "other", "confidence": 0.2, "reason": "No classifiable content."}
```

The first example is the one that earns its place: it teaches the tie-break rule in a way the prose alone does not.

**Diagnosing a failing prompt systematically:**

```text
Symptom: the classifier returns "billing" for technical messages ~15% of the time.

Hypotheses, tested one at a time against the 40-case evaluation set:

H1: The category definitions overlap.
    Test: read them. "billing" says "payment methods"; several technical
    messages are about a broken payment *integration*.
    Result: CONFIRMED. Baseline 85% -> 94% after clarifying that integration
    failures are technical regardless of subject matter.

H2: Reasoning would help.
    Test: add "Think step by step before answering."
    Result: no accuracy change, +340ms latency, +180 tokens. REVERTED.

H3: More examples would help.
    Test: 6 examples instead of 2.
    Result: 94% -> 96%. Kept. Diminishing returns past 6 (tested 10: 96%).

Final: 96%, at lower cost than the baseline.
```

## Notes

- The measurement set is the entire discipline. A prompt engineer without an evaluation set is guessing with extra confidence.
- "Think step by step" is not free and is not universally helpful. It reliably improves multi-step arithmetic and logic; it reliably does nothing for classification. Measure rather than assume.
- Prompt injection is a real vulnerability when user content enters a prompt. Never let user text be interpreted as instructions — delimit it clearly and treat the model's output as untrusted.
