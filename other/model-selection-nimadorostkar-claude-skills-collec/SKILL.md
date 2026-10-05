---
name: model-selection
description: Use when choosing which LLM to use for a task. Covers matching capability to task, cost and latency trade-offs, routing between models, benchmark skepticism, and evaluating on your own data.
metadata:
  category: ai
  version: 1.0.0
  tags: [models, selection, cost, latency, routing]
---

# Model Selection

## Purpose

Choose the model that meets the task's requirements at the lowest cost and latency. Most production LLM features run on a model several times more expensive than the task requires, because nobody measured the cheaper one.

## When to Use

- Choosing a model for a new feature.
- Reducing the cost or latency of an existing feature.
- Evaluating whether a newly released model is worth migrating to.
- Designing a routing strategy across several models.

## Capabilities

- Task-to-capability matching.
- Cost and latency modeling at real volume.
- Routing: cheap model first, escalate on difficulty.
- Benchmark interpretation and its limits.
- Migration and re-evaluation.

## Inputs

- The task, and the accuracy it genuinely requires.
- Volume, latency budget, and cost budget.
- An evaluation set — without one, this is guesswork.

## Outputs

- A model choice justified by measurement on your data.
- A cost and latency projection at real volume.
- A routing strategy, where one is warranted.

## Workflow

1. **Start with the cheapest plausible model** — Not the best one. Measure it on your evaluation set. Escalate only if it fails, and only as far as necessary.
2. **Measure on your data, not on benchmarks** — A model that leads on MMLU may be worse at your specific extraction task. Public benchmarks measure general capability, and your task is not general.
3. **Model the cost at real volume** — A per-call cost difference that looks trivial becomes the dominant line item at a million calls a month. Do the arithmetic before choosing.
4. **Consider routing** — Send everything to a small model; escalate the cases it flags as low-confidence to a larger one. This frequently captures most of the accuracy at a fraction of the cost.
5. **Re-evaluate on model updates** — Provider models change under the same name. A prompt tuned six months ago on a model that has since been updated may no longer be optimal.

## Best Practices

- The most common mistake is defaulting to the most capable model for everything. Classification, extraction, and routing tasks are usually solved by a small model at a tenth of the cost and a fifth of the latency.
- Public benchmarks are contaminated and gamed. They are a rough capability ordering, not a prediction of performance on your task.
- Latency matters more than cost for user-facing features, and cost matters more than latency for batch processing. Optimize for the one that binds.
- A cheaper model with better prompting often beats a more expensive model with worse prompting. Improve the prompt before upgrading the model.
- Test the failure mode, not just the accuracy. A small model that fails loudly is safer than a large one that fails plausibly.
- Do not hard-code the model name across the codebase. Configure it, so migration is a config change rather than a search-and-replace.

## Examples

**Measuring rather than assuming:**

```text
Task: extract structured fields from support emails. 800,000/month.

Model         Accuracy   p95 latency   Cost/1k calls   Monthly cost
-----------   --------   -----------   -------------   ------------
Small          91.2%        340ms          $0.42            $336
Medium         96.8%        890ms          $3.10          $2,480
Large          97.4%       2,100ms        $15.00         $12,000

The large model buys 0.6 accuracy points over the medium for 5x the cost and
2.4x the latency. It is not a serious candidate.

The real question is whether 91.2% is sufficient. It is not — the failures
concentrate on emails with attachments and multi-issue threads.

Routing solution:
  - Small model handles everything, and returns a confidence score.
  - The 14% of cases below the confidence threshold escalate to medium.

  Effective accuracy:  96.5%   (within 0.3 points of medium-for-everything)
  Monthly cost:        $336 + (0.14 x $2,480) = $683
  p95 latency:         410ms   (most requests never touch the medium model)

Chosen: routing. 96.5% accuracy at $683/month, versus 96.8% at $2,480.
```

**Routing implemented:**

```python
async def extract(email: str) -> Extraction:
    result = await small_model.extract(email)

    # Escalate on the model's own uncertainty, or on a structural signal
    # that we know correlates with failure.
    needs_escalation = (
        result.confidence < 0.75
        or email_has_attachment(email)
        or count_distinct_issues(email) > 1
    )

    if needs_escalation:
        metrics.increment("extraction.escalated")
        return await medium_model.extract(email)

    return result
```

## Notes

- The routing threshold should be tuned on the evaluation set by plotting accuracy against escalation rate. There is usually a knee where a small increase in escalation buys most of the remaining accuracy.
- Structural escalation signals (has an attachment, exceeds a length, contains a table) are often better predictors of failure than the model's own confidence score, and they are free to compute.
- When a provider releases a new model, the correct response is to run your evaluation set against it, not to migrate on the announcement. Sometimes the newer model is worse at your specific task.
