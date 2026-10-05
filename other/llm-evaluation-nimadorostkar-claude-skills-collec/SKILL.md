---
name: llm-evaluation
description: Use when measuring the quality of an LLM feature. Covers building an evaluation set, choosing metrics, LLM-as-judge and its pitfalls, regression testing prompts, and evaluating in production.
metadata:
  category: ai
  version: 1.0.0
  tags: [evaluation, eval, llm-judge, testing, metrics]
---

# LLM Evaluation

## Purpose

Know whether an LLM feature is getting better or worse. Without evaluation, every prompt change is a guess, and the confidence that a change helped is indistinguishable from the confidence that it did not.

## When to Use

- Before iterating on any prompt or model in production.
- Comparing models, prompts, or retrieval strategies.
- Setting up regression testing for an LLM feature.
- Deciding whether a quality complaint is real or anecdotal.

## Capabilities

- Evaluation-set construction from real usage.
- Metric selection: exact match, similarity, rubric-based, task-specific.
- LLM-as-judge, with the controls that make it trustworthy.
- Regression testing in CI.
- Online evaluation and production monitoring.

## Inputs

- Real inputs from actual usage, not invented ones.
- A definition of correct — which is the hard part.
- The current behavior, as a baseline.

## Outputs

- An evaluation set that includes the hard cases.
- A metric that correlates with what users actually care about.
- A baseline score, and a gate that catches regressions.

## Workflow

1. **Build the set from real usage** — Fifty to two hundred real inputs, including the failures. An evaluation set of invented examples measures your imagination, not the system.
2. **Define correct precisely** — For extraction, the exact expected output. For open-ended generation, a rubric with concrete criteria. "A good summary" is not a criterion; "mentions all three decisions and no facts absent from the source" is.
3. **Choose the cheapest sufficient metric** — Exact match where possible. String or semantic similarity next. LLM-as-judge only where the output is genuinely open-ended.
4. **Validate the judge** — Have a human grade fifty cases. If the judge disagrees with the human more than about 15% of the time, the judge is not measuring what you think.
5. **Baseline, then change one thing** — Measure. Change one variable. Measure again on the same set. Anything else is not evidence.
6. **Gate in CI** — A prompt change that drops the score below the threshold fails the build, exactly like any other regression.

## Best Practices

- The evaluation set must contain the cases that fail today. A set on which the system already scores 100% cannot measure improvement.
- LLM-as-judge is biased toward longer answers, toward its own outputs, and toward the first option presented. Randomize the order, control for length, and validate against human judgment before trusting it.
- A single aggregate score hides everything. Break it down by input category — a change that improves the average while destroying one category is a regression for those users.
- Never evaluate on the examples in your prompt. That measures memorization.
- Evaluate the whole pipeline and the components separately. A RAG system's failure is either retrieval or generation, and the aggregate score does not tell you which.
- Track the score over time. LLM quality changes silently when the provider updates the model.

## Examples

**A rubric-based judge, validated against humans:**

```python
JUDGE_PROMPT = """\
You are grading a customer support summary against the original conversation.

Score each criterion independently, 0 or 1:

1. COMPLETE:  Every action item in the conversation appears in the summary.
2. GROUNDED:  Every statement in the summary is supported by the conversation.
              A single invented fact scores 0.
3. RESOLUTION: The summary correctly states whether the issue was resolved.
4. CONCISE:   The summary is under 100 words and contains no filler.

Conversation:
{conversation}

Summary:
{summary}

Respond with JSON only:
{{"complete": 0|1, "grounded": 0|1, "resolution": 0|1, "concise": 0|1, "notes": "<brief>"}}"""


# The judge must be validated before it is trusted.
def validate_judge(human_graded: list[Case]) -> float:
    agreement = sum(
        judge(c.conversation, c.summary) == c.human_score for c in human_graded
    ) / len(human_graded)

    if agreement < 0.85:
        raise ValueError(
            f"Judge agrees with humans only {agreement:.0%} of the time. "
            "It is measuring something else. Fix the rubric before using it."
        )
    return agreement
```

**A regression gate that stops a bad prompt from shipping:**

```python
def test_summarization_quality_has_not_regressed():
    results = [evaluate(case) for case in load_eval_set("support-summaries-v3")]

    grounded = mean(r.grounded for r in results)
    complete = mean(r.complete for r in results)

    # Hallucination is the failure that matters most: it is a hard floor.
    assert grounded >= 0.98, f"Grounding regressed to {grounded:.2%} (floor: 98%)"
    assert complete >= 0.90, f"Completeness regressed to {complete:.2%} (floor: 90%)"

    # And the breakdown, because an average hides a category collapse.
    by_category = group_by(results, key=lambda r: r.case.category)
    for category, group in by_category.items():
        score = mean(r.overall for r in group)
        assert score >= 0.85, f"Category '{category}' regressed to {score:.2%}"
```

## Notes

- The most common evaluation mistake is a set that is too easy. If a change to the prompt does not move the score, either the change did nothing or the set cannot detect it — check which.
- Judge models are cheaper and faster than humans and roughly as consistent, once validated. The validation step is not optional; an unvalidated judge is a random number generator with good grammar.
- Online evaluation — sampling real production outputs and grading them — catches the drift that an offline set never will, because production inputs change and your evaluation set does not.
