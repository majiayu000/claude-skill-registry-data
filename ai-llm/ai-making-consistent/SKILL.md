---
name: ai-making-consistent
description: Make your AI give the same answer every time. Use when AI gives different answers to the same question, outputs are unpredictable, responses vary between runs, you need deterministic AI behavior, or your AI is unreliable. Also used for same input gives different output every time, prompt sensitivity causes output changes with minor wording tweaks, reordering examples shifts accuracy dramatically, same prompt gives different results every run, AI is non-deterministic, need reproducible AI results, LLM output keeps changing, how to make LLM deterministic, consistent JSON from LLM, reduce output variance, AI flaky in production, stable AI outputs for production.
---

# Make Your AI Consistent

Guide the user through making their AI give reliable, predictable outputs. This is different from "wrong answers" — the AI might be right 80% of the time but unpredictably different each run.

## When consistency does NOT matter

- **Creative generation** — blog posts, marketing copy, brainstorming. Variation is a feature, not a bug.
- **Already accurate** — if the AI gives the right answer 95%+ of the time and downstream code handles minor format differences, do not over-constrain.
- **Human-in-the-loop** — if a person reviews every output, slight variation is harmless.

If the AI is consistent but *wrong*, use `/ai-improving-accuracy` instead — consistency without accuracy just means reliably wrong.

## Step 1: Diagnose the inconsistency

Ask the user:
1. **What is varying?** (the answer itself, the format, the length, the level of detail?)
2. **How bad is it?** (slightly different wording vs. completely different answers)
3. **Does it matter for your use case?** (sometimes variation is fine, sometimes it breaks downstream code)

### Quick test: run the same input 5 times

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini", temperature=0)  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

results = []
for i in range(5):
    result = my_program(question="What is the capital of France?")
    results.append(result.answer)
    print(f"Run {i+1}: {result.answer}")

# Check consistency
unique = set(results)
print(f"\n{len(unique)} unique answers out of 5 runs")
```

If outputs vary, apply the fixes below in order — each one adds a layer of consistency.

## Step 2: Consistency techniques

| Technique | Fixes | Effort | Impact |
|-----------|-------|--------|--------|
| `temperature=0` | Random sampling variation | One line | High — fixes most issues |
| `Literal` types | Category string variation ("positive" vs "Positive") | Signature change | High for classification |
| Pydantic models | Structural format variation | Model definition | Medium for complex outputs |
| `dspy.Refine` | Length, format, content drift | Reward function | Medium — catches edge cases |
| `BootstrapFewShot` | Style and pattern variation | Optimization run | High — teaches consistent patterns |
| Caching | Identical input re-runs | Enabled by default | Perfect for repeated inputs |

### Set temperature to 0

The single biggest consistency fix. Temperature controls randomness:

```python
lm = dspy.LM("openai/gpt-4o-mini", temperature=0)  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)
```

Some providers may still have slight variation at temperature=0 due to floating point non-determinism, but it is minimal.

### Constrain output types with Literal

```python
from typing import Literal

class Classify(dspy.Signature):
    """Classify the text."""
    text: str = dspy.InputField()
    # BAD: label: str — AI can say "positive", "Positive", "pos", "POSITIVE", etc.
    # GOOD: locked to exact values
    label: Literal["positive", "negative", "neutral"] = dspy.OutputField()
```

### Use Pydantic models for structured output

```python
from pydantic import BaseModel, Field

class StructuredOutput(BaseModel):
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    tags: list[str]

class MySignature(dspy.Signature):
    """Process the input."""
    text: str = dspy.InputField()
    result: StructuredOutput = dspy.OutputField()
```

### Add output constraints with Refine

```python
class ConsistentResponder(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(MySignature)

    def forward(self, text):
        return self.respond(text=text)

def consistency_reward(args, pred):
    score = 1.0
    # Hard constraint — large penalty if violated
    if len(pred.answer) >= 200:
        score -= 0.8
    # Soft constraint — small penalty if not met
    if not pred.answer.endswith("."):
        score -= 0.1
    return max(score, 0.0)

validated = dspy.Refine(
    module=ConsistentResponder(),
    N=3,
    reward_fn=consistency_reward,
    threshold=0.9,
)
```

### Optimize to lock in patterns

Optimization teaches consistent patterns through few-shot examples:

```python
optimizer = dspy.BootstrapFewShot(
    metric=consistency_metric,
    max_bootstrapped_demos=4,
)
optimized = optimizer.compile(my_program, trainset=trainset)
```

For best consistency, make your metric penalize inconsistency:

```python
def consistency_metric(example, prediction, trace=None):
    correct = prediction.answer.lower().strip() == example.answer.lower().strip()
    right_length = 5 <= len(prediction.answer.split()) <= 30
    no_hedging = not any(w in prediction.answer.lower() for w in ["maybe", "perhaps"])
    return correct and right_length and no_hedging
```

### Use caching for identical inputs

DSPy caches LM calls by default (in-memory + on-disk). For identical inputs, you always get the same output:

```python
# First call — hits the API
result1 = my_program(question="What is Python?")

# Second call with same input — returns cached result (instant, identical)
result2 = my_program(question="What is Python?")

# Disable caching if needed
dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)
```

## Step 3: Verify consistency

After applying fixes, measure improvement:

```python
from collections import Counter

def measure_consistency(program, input_data, n_runs=10):
    """Run the same inputs multiple times and measure output stability."""
    results = []
    for _ in range(n_runs):
        result = program(**input_data)
        results.append(str(result.answer).strip().lower())

    counts = Counter(results)
    most_common_count = counts.most_common(1)[0][1]
    consistency_rate = most_common_count / n_runs
    print(f"Consistency: {consistency_rate:.0%} ({len(counts)} unique answers in {n_runs} runs)")
    return consistency_rate

# Before fixes: ~60% consistency
# After temperature=0: ~95% consistency
# After temperature=0 + Literal types: ~99% consistency
```

## Gotchas

- **Claude sets `temperature=0` but forgets the LM already exists.** If `dspy.configure(lm=lm)` was called earlier in the code with a different LM, setting temperature on a new LM does not affect existing modules. Always reconfigure after changing the LM.
- **`dspy.Refine` retries burn tokens.** When the reward threshold is not met, `dspy.Refine` retries up to N times. For high-volume classification, a poorly tuned threshold can multiply your API costs by N. Monitor token usage after adding Refine wrappers.
- **Caching masks inconsistency during development.** DSPy caches by default, so repeated test runs return identical results even if the program would be inconsistent with fresh calls. Disable caching when measuring consistency: `dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)`.
- **`Literal` types only work with static values, not runtime lists.** Claude writes `Literal[my_list]` which fails. For dynamic categories from a database or config, use `Literal[tuple(categories)]` to convert at definition time.
- **BootstrapFewShot demos can actually increase variation if the demos themselves are inconsistent.** If your training examples have varied formatting (some with periods, some without), the bootstrapped demos teach that variation. Clean your training data format before optimizing.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Improving accuracy** when the AI is consistent but wrong -- see `/ai-improving-accuracy`
- **Fixing errors** when the AI is crashing or throwing exceptions -- see `/ai-fixing-errors`
- **Following rules** to enforce format and policy constraints -- see `/ai-following-rules`
- **Signatures** for defining typed input/output contracts -- see `/dspy-signatures`
- **ChainOfThought** for the reasoning module used in constrained pipelines -- see `/dspy-chain-of-thought`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples, see [examples.md](examples.md)
- For full API reference, see [reference.md](reference.md)
- [dspy.LM API docs](https://dspy.ai/api/models/LM/) for temperature and caching configuration
- [DSPy caching tutorial](https://dspy.ai/tutorials/cache/) for cache configuration details
