---
name: dspy-chain-of-thought
description: Use when the task benefits from intermediate reasoning before producing an answer — multi-step logic, analysis, math, or complex classification where direct prediction fails. Common scenarios - classification tasks where the model needs to reason about edge cases, math word problems, multi-step analysis, complex question answering, legal or medical reasoning, any task where thinking before answering improves quality. Related - ai-reasoning, dspy-predict, dspy-multi-chain-comparison. Also used for dspy.ChainOfThought, CoT prompting in DSPy, think step by step, show your reasoning, intermediate reasoning steps, LLM gives wrong answer without thinking, reasoning before output, make AI explain its logic, step-by-step problem solving, when to use ChainOfThought vs Predict, add reasoning to any DSPy module, let the model think, chain of thought for classification.
---

# Step-by-Step Reasoning with dspy.ChainOfThought

Guide the user through using DSPy's `ChainOfThought` module -- the go-to module for tasks that benefit from intermediate reasoning before producing an answer.

## Step 1: Gather context

Before writing any code, ask:

1. **What are the input and output fields?** Paste or describe your signature — inline string or class-based. This determines how to structure the module.
2. **What kind of task is this?** Classification, extraction, analysis, decision-making, or multi-step reasoning? Tasks where a human would need to think before answering benefit most from CoT.
3. **Have you tried `dspy.Predict` already?** If so, what went wrong — wrong answers, missing nuance, or poor edge-case handling? This shapes whether to demonstrate optimization too.

## What is ChainOfThought

`dspy.ChainOfThought` is a drop-in replacement for `dspy.Predict` that automatically injects a `reasoning` field before your output fields. Same signature, one-word swap -- the LM reasons step-by-step before answering. The `reasoning` field is always available on the result even though your signature doesn't declare it.

## When CoT helps

ChainOfThought improves accuracy when the task requires the LM to work through intermediate steps before arriving at an answer:

- **Multi-step logic** -- math, puzzles, conditional reasoning
- **Analysis and judgment** -- "Is this code buggy?", "Should we approve this loan?"
- **Classification with nuance** -- when the label depends on weighing multiple factors
- **Explanation-heavy tasks** -- anything where you want to see *why* the LM chose its answer
- **Complex extraction** -- parsing ambiguous data where the LM needs to resolve conflicts

**Rule of thumb:** If a human would need to think through the problem before answering, use ChainOfThought.

## When NOT to use CoT

ChainOfThought adds latency and token cost because the LM generates extra reasoning text. Skip it when:

- **Simple lookups** -- "What is the capital of France?" No reasoning needed.
- **Direct extraction** -- pulling a name or date from structured text. `Predict` is enough.
- **Speed-critical paths** -- if you need sub-second responses and the task is straightforward, use `Predict`.
- **High-volume, low-complexity** -- processing thousands of simple items where reasoning adds cost without improving accuracy.

When in doubt, start with `ChainOfThought` and switch to `Predict` later if profiling shows the reasoning is unnecessary.

## Passing reasoning downstream

```python
class ReviewDecision(dspy.Module):
    def __init__(self):
        self.analyze = dspy.ChainOfThought("application -> decision: str, risk_level: str")
        self.summarize = dspy.Predict("decision, reasoning -> summary")

    def forward(self, application):
        analysis = self.analyze(application=application)
        # Pass the reasoning to the next step
        summary = self.summarize(
            decision=analysis.decision,
            reasoning=analysis.reasoning,
        )
        return dspy.Prediction(
            decision=analysis.decision,
            risk_level=analysis.risk_level,
            reasoning=analysis.reasoning,
            summary=summary.summary,
        )
```

## Predict vs ChainOfThought

| | `dspy.Predict` | `dspy.ChainOfThought` |
|---|---|---|
| **Output fields** | Only what the signature declares | Signature fields + `reasoning` |
| **Latency** | Lower | Higher (generates reasoning tokens) |
| **Cost** | Lower | Higher (more output tokens) |
| **Accuracy on complex tasks** | Lower | Higher |
| **Accuracy on simple tasks** | Same | Same (but wastes tokens) |
| **Best for** | Lookups, extraction, simple classification | Analysis, judgment, multi-step problems |

## Combining CoT with typed outputs

ChainOfThought works with all the same type constraints as Predict -- `Literal`, `int`, `float`, `bool`, `list[str]`, and Pydantic models.

```python
import dspy
from pydantic import BaseModel
from typing import Literal

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class RiskAssessment(BaseModel):
    risk_score: float
    factors: list[str]
    recommendation: Literal["approve", "review", "deny"]

class AssessRisk(dspy.Signature):
    """Assess the risk level of a financial transaction."""
    transaction_details: str = dspy.InputField()
    assessment: RiskAssessment = dspy.OutputField()

assessor = dspy.ChainOfThought(AssessRisk)
result = assessor(
    transaction_details="Wire transfer of $50,000 to a new recipient in a high-risk jurisdiction"
)
print(result.reasoning)                   # detailed risk analysis
print(result.assessment.risk_score)       # 0.85
print(result.assessment.factors)          # ["high amount", "new recipient", "high-risk jurisdiction"]
print(result.assessment.recommendation)   # "review"
```

The LM reasons through the problem first, then produces the structured output. The reasoning happens before type enforcement, so the LM has space to think before committing to typed fields.

## Optimizing CoT with few-shot examples

ChainOfThought benefits significantly from optimization. When you run an optimizer, DSPy discovers high-quality reasoning traces and uses them as few-shot demonstrations:

```python
import dspy
from dspy.evaluate import Evaluate

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Your CoT module
classifier = dspy.ChainOfThought("ticket_text -> priority: str, team: str")

# Training data
trainset = [
    dspy.Example(
        ticket_text="Site is down for all users",
        priority="critical",
        team="infrastructure",
    ).with_inputs("ticket_text"),
    dspy.Example(
        ticket_text="Typo on the pricing page",
        priority="low",
        team="content",
    ).with_inputs("ticket_text"),
    # ... more examples
]

# Metric
def ticket_metric(example, prediction, trace=None):
    priority_correct = prediction.priority == example.priority
    team_correct = prediction.team == example.team
    return priority_correct + team_correct

# Optimize -- the optimizer generates and selects good reasoning traces
optimizer = dspy.BootstrapFewShot(metric=ticket_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(classifier, trainset=trainset)

# The optimized program now includes few-shot examples with reasoning
result = optimized(ticket_text="Users can't upload files larger than 10MB")
print(result.reasoning)  # higher quality reasoning, guided by learned demos
print(result.priority)
print(result.team)

# Save for production
optimized.save("ticket_classifier.json")
```

What optimization does for ChainOfThought:
- **Bootstraps reasoning traces** -- the optimizer runs the module on training examples, keeps the traces that led to correct answers, and includes them as few-shot demonstrations
- **Improves consistency** -- the LM sees examples of good reasoning patterns before generating its own
- **Works with all optimizers** -- `BootstrapFewShot`, `MIPROv2`, `BootstrapFewShotWithRandomSearch` all support CoT modules

**Verify improvement before shipping:** Always compare accuracy before and after optimization:

```python
evaluator = dspy.evaluate.Evaluate(devset=devset, metric=ticket_metric, num_threads=4)
baseline = evaluator(classifier)
optimized_score = evaluator(optimized)
print(f"Baseline: {baseline:.1f}%  →  Optimized: {optimized_score:.1f}%")
dspy.inspect_history(n=1)  # confirm reasoning trace appears before output fields
```

Typical results: `BootstrapFewShot` with 3-5 demos improves accuracy by 10–25 percentage points on classification and judgment tasks. `MIPROv2` can yield an additional 10–20 points on top of that.

## Using CoT inside custom modules

ChainOfThought is a sub-module like any other. Use it in `dspy.Module` for multi-step pipelines:

```python
import dspy

class CodeReviewer(dspy.Module):
    def __init__(self):
        self.find_issues = dspy.ChainOfThought("code -> issues: list[str], severity: str")
        self.suggest_fix = dspy.ChainOfThought("code, issues -> fixed_code: str")

    def forward(self, code):
        analysis = self.find_issues(code=code)

        if analysis.severity == "none":
            return dspy.Prediction(
                issues=[],
                severity="none",
                fixed_code=code,
                reasoning=analysis.reasoning,
            )

        fix = self.suggest_fix(code=code, issues=analysis.issues)

        return dspy.Prediction(
            issues=analysis.issues,
            severity=analysis.severity,
            fixed_code=fix.fixed_code,
            reasoning=analysis.reasoning,
        )
```

Both sub-modules use CoT because code review and fix suggestion both benefit from step-by-step thinking. When optimized, DSPy tunes each sub-module's reasoning independently.

## Gotchas

- **Claude adds `reasoning` as an explicit output field in the signature.** DSPy injects it automatically — declaring it yourself creates a duplicate field that confuses the prompt. Just use `dspy.ChainOfThought("question -> answer")` and access `result.reasoning` on the output.
- **Claude uses ChainOfThought for simple extraction tasks where Predict is sufficient.** CoT adds ~100-300 tokens of overhead per call. For tasks like pulling a name from structured text or simple lookups, use `dspy.Predict` instead — CoT adds cost without improving accuracy on straightforward tasks.
- **Claude sets `max_tokens` too low, truncating reasoning before output fields.** The reasoning trace is generated before the actual output fields. If `max_tokens` is tight, the LM runs out of space mid-reasoning and never produces the output fields, causing parse failures. Leave headroom — at least 500 tokens beyond what you expect the output fields to need.
- **Claude forgets that `reasoning` is available on the result object.** After calling a ChainOfThought module, the reasoning trace is always at `result.reasoning` even though the signature does not declare it. Claude sometimes re-derives reasoning or asks the LM to explain its answer in a separate call when the trace is already there.
- **Claude uses `rationale_field` to rename the reasoning field but does not update downstream references.** `dspy.ChainOfThought(sig, rationale_field=dspy.OutputField(prefix="Thinking:"))` changes the prompt prefix, but the field is still accessed as `result.reasoning` on the output. Claude sometimes tries to access `result.thinking` or `result.rationale` after renaming, which fails silently (returns `None`).

## Additional resources

- [dspy.ChainOfThought API docs](https://dspy.ai/api/modules/ChainOfThought/)
- [reference.md](reference.md) — constructor parameters, methods, rationale field customization
- [examples.md](examples.md) — bug analysis, release decisions, classification with justification

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Predict** for simple calls without reasoning -- see `/dspy-predict`
- **Signatures** for defining input/output contracts -- see `/dspy-signatures`
- **Modules** for building multi-step programs with CoT sub-modules -- see `/dspy-modules`
- **Reasoning patterns** for broader strategies (decomposition, self-correction) -- see `/ai-reasoning`
- **MultiChainComparison** when one reasoning path is unreliable -- generates N chains and selects the best-reasoned answer -- see `/dspy-multi-chain-comparison`
- **Best-of-N** for sampling N independent outputs and picking the best via a reward function -- see `/dspy-best-of-n`
- **Refine** for iterative improvement with feedback until quality meets a threshold -- see `/dspy-refine`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
