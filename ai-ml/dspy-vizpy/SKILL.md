---
name: dspy-vizpy
description: Use VizPy as a drop-in prompt optimizer for DSPy. Use when you want to try VizPy, vizops, ContraPromptOptimizer, PromptGradOptimizer, a commercial alternative to GEPA, a third-party prompt optimizer, or a different optimization backend. Also used for vizpy optimizer, vizpy vs GEPA, vizpy vs MIPROv2, commercial prompt optimization, ContraPrompt for classification, PromptGrad for generation, vizpy API key, pip install vizpy, vizpy free tier.
---

# VizPy — Commercial Prompt Optimizer for DSPy

Guide the user through integrating VizPy as a drop-in prompt optimizer alongside or instead of DSPy's native optimizers (GEPA, MIPROv2).

## Step 1: Understand the optimization need

Before recommending VizPy, clarify:

1. **Classification or generation?** — ContraPromptOptimizer is for classification (fixed categories), PromptGradOptimizer is for generation (open-ended text). This determines which optimizer to use.
2. **Already tried DSPy native optimizers?** — If not, start with GEPA or MIPROv2 first. VizPy is best as a comparison or when native optimizers plateau.
3. **Data privacy constraints?** — VizPy is SaaS — training data is sent to their servers. If data cannot leave the network, use GEPA instead.
4. **How many optimization runs do they need?** — Free tier allows 10 runs/month. Pro allows 200 runs/month ($20/mo). Enterprise allows 1,000 runs/month ($200/mo).

## What is VizPy

VizPy is a commercial SaaS prompt optimization service ([vizpy.vizops.ai](https://vizpy.vizops.ai)) that provides two optimizers for DSPy programs:

- **ContraPromptOptimizer** — for classification tasks (sentiment, routing, tagging)
- **PromptGradOptimizer** — for generation tasks (summarization, content creation, Q&A)

Both optimize the **instruction string only** — the same limitation as `dspy.GEPA`. They do NOT optimize few-shot demos, Pydantic field descriptions, or model weights.

### Pricing

| Tier | Optimization runs/month | Cost |
|------|------------------------|------|
| Free | 10 | $0 |
| Pro | 200 | $20/mo |
| Enterprise | 1,000 | $200/mo |

## When to use VizPy

Use VizPy when:

- You want to compare a commercial optimizer against DSPy's native ones
- You've tried GEPA and want a different instruction-tuning approach
- You want ContraPrompt's contrastive approach for classification tasks
- You want PromptGrad's gradient-inspired approach for generation tasks

Do NOT use VizPy when:

- You need few-shot demo optimization — use `dspy.BootstrapFewShot` or `dspy.MIPROv2`
- You need to optimize Pydantic field descriptions — VizPy only tunes instructions (same as GEPA). See the workaround in `/dspy-gepa`
- You need to tune model weights — use `dspy.BootstrapFinetune`
- You want a fully open-source solution — use `dspy.GEPA` or `dspy.MIPROv2`

## Setup

```bash
pip install vizpy
```

Set your API key:

```python
import vizpy
vizpy.api_key = "your-vizpy-api-key"  # from vizpy.vizops.ai/dashboard
```

Or via environment variable:

```bash
export VIZPY_API_KEY="your-vizpy-api-key"
```

## ContraPromptOptimizer (classification)

Best for tasks with a fixed set of output categories.

```python
import dspy
import vizpy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 1. Define your classifier
classify = dspy.ChainOfThought("text -> label")

# 2. Prepare training data
trainset = [
    dspy.Example(text="Great product!", label="positive").with_inputs("text"),
    dspy.Example(text="Terrible service.", label="negative").with_inputs("text"),
    # ... 50+ examples recommended
]

# 3. Define a metric — must return vizpy.Score, not plain float or bool
def vizpy_metric(example, prediction, trace=None):
    correct = prediction.label.lower() == example.label.lower()
    return vizpy.Score(
        value=1.0 if correct else 0.0,
        is_success=correct,
        feedback="" if correct else f"Expected '{example.label}', got '{prediction.label}'.",
    )

# 4. Optimize with VizPy
optimizer = vizpy.ContraPromptOptimizer(metric=vizpy_metric)
optimized = optimizer.optimize(classify, train_examples=trainset)

# 5. Use the optimized program
result = optimized(text="This exceeded my expectations!")
print(result.label)

# 6. Save
optimized.save("vizpy_optimized_classifier.json")
```

### How ContraPrompt works

ContraPromptOptimizer uses contrastive examples — it identifies cases where the current instruction fails and generates instruction candidates that distinguish between confusing categories. This is particularly effective when categories are semantically close (e.g., "billing" vs "account" tickets).

## PromptGradOptimizer (generation)

Best for open-ended generation tasks where output quality is on a spectrum.

```python
import dspy
import vizpy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 1. Define your generator
summarize = dspy.ChainOfThought("article -> summary")

# 2. Prepare training data
trainset = [
    dspy.Example(
        article="Long article text here...",
        summary="Expected summary."
    ).with_inputs("article"),
    # ... 50+ examples
]

# 3. Define a metric (can be AI-as-judge)
class AssessQuality(dspy.Signature):
    """Assess if the summary captures key points accurately."""
    article: str = dspy.InputField()
    gold_summary: str = dspy.InputField()
    predicted_summary: str = dspy.InputField()
    score: float = dspy.OutputField(desc="0.0 to 1.0")

def metric(example, prediction, trace=None):
    judge = dspy.Predict(AssessQuality)
    result = judge(
        article=example.article,
        gold_summary=example.summary,
        predicted_summary=prediction.summary,
    )
    correct = float(result.score) >= 0.7
    return vizpy.Score(
        value=float(result.score),
        is_success=correct,
        feedback="" if correct else f"Quality score {result.score:.2f} below threshold.",
    )

# 4. Optimize with VizPy
optimizer = vizpy.PromptGradOptimizer(metric=metric)
optimized = optimizer.optimize(summarize, train_examples=trainset)

# 5. Use
result = optimized(article="New article text...")
print(result.summary)
```

### How PromptGrad works

PromptGradOptimizer uses gradient-inspired optimization — it estimates how instruction changes affect output quality scores and iteratively adjusts the instruction in the direction that improves the metric. This works well for generation tasks where quality is continuous rather than binary.

## VizPy vs DSPy native optimizers

| Aspect | VizPy ContraPrompt | VizPy PromptGrad | dspy.GEPA | dspy.MIPROv2 |
|--------|-------------------|-----------------|-----------|-------------|
| **Best for** | Classification | Generation | Both | Both |
| **What it tunes** | Instructions only | Instructions only | Instructions only | Instructions + demos |
| **Data needed** | ~50 examples | ~50 examples | ~50 examples | ~200 examples |
| **Expected improvement** | 5-18% | 5-18% | 5-15% | 15-35% |
| **Cost** | Free tier (10 runs) | Free tier (10 runs) | ~$0.50 (LM calls) | ~$5-15 (LM calls) |
| **Open source** | No (SaaS) | No (SaaS) | Yes | Yes |
| **Feedback-driven** | Contrastive examples | Gradient-inspired | Textual feedback | Scalar scores |
| **Pydantic field desc** | No | No | No | No |

### Decision guide

```
Want instruction-only optimization?
|
+- Classification task?
|  +- Want open-source? -> dspy.GEPA
|  +- Want to try commercial? -> vizpy.ContraPromptOptimizer
|
+- Generation task?
|  +- Want open-source? -> dspy.GEPA
|  +- Want to try commercial? -> vizpy.PromptGradOptimizer
|
+- Want instructions AND demos? -> dspy.MIPROv2
```

## Switching between VizPy and GEPA

VizPy optimizers produce standard DSPy programs — `save()`, `load()`, and `Evaluate` all work identically after optimization. The optimizer API differs slightly from GEPA:

```python
# With GEPA — uses .compile(), standard DSPy metric (dict with score + feedback)
def gepa_metric(gold, pred, trace=None, **kw):
    correct = pred.label.lower() == gold.label.lower()
    return {"score": float(correct), "feedback": "" if correct else f"Expected '{gold.label}'."}

optimizer = dspy.GEPA(metric=gepa_metric, auto="light")
optimized = optimizer.compile(program, trainset=trainset)

# With VizPy ContraPrompt — uses .optimize(), vizpy.Score metric
def vizpy_metric(example, pred, trace=None):
    correct = pred.label.lower() == example.label.lower()
    return vizpy.Score(value=float(correct), is_success=correct,
                       feedback="" if correct else f"Expected '{example.label}'.")

optimizer = vizpy.ContraPromptOptimizer(metric=vizpy_metric)
optimized = optimizer.optimize(program, train_examples=trainset)
```

## Important limitations

1. **Instruction-only optimization** — VizPy does NOT optimize Pydantic `Field(description=...)`, `InputField(desc=...)`, or `OutputField(desc=...)`. Same limitation as GEPA. See `/dspy-gepa` for a workaround (flatten field descriptions into the instruction).

2. **SaaS dependency** — your training data is sent to VizPy's servers for optimization. Check your data privacy requirements.

3. **No offline mode** — requires internet access and a valid API key.

4. **Free tier limits** — 10 optimization runs per month. Each `.optimize()` call counts as one run.

## Verifying the optimization

After running `.optimize()`, compare baseline vs optimized. Note: `dspy.Evaluate` expects a float metric, not a `vizpy.Score` — extract `.value`:

```python
from dspy.evaluate import Evaluate

# Wrap vizpy_metric for dspy.Evaluate (extracts the float .value)
eval_metric = lambda ex, pred, trace=None: vizpy_metric(ex, pred).value

evaluator = Evaluate(devset=devset, metric=eval_metric, num_threads=4)

# Baseline
baseline_score = evaluator(program)
print(f"Baseline: {baseline_score}")

# After VizPy optimization
optimized_score = evaluator(optimized)
print(f"Optimized: {optimized_score}")
print(f"Improvement: {optimized_score - baseline_score:.1f}%")
```

If the optimized score is not higher, the instruction change may not help this task. Try a different optimizer (GEPA, MIPROv2) or add few-shot demos with MIPROv2.

## Gotchas

- **Claude writes a plain float or bool VizPy metric.** VizPy metrics must return `vizpy.Score(value=float, is_success=bool, feedback=str)` — not a plain `float`, `bool`, or dict. Without `feedback`, ContraPrompt cannot generate contrastive improvement rules and optimization silently degrades. Standard DSPy metrics and GEPA dict metrics are not compatible. Always use `vizpy.Score`.
- **Claude uses VizPy for few-shot demo optimization.** VizPy only tunes the instruction string, not demos. If the user needs demos, use `dspy.BootstrapFewShot` or `dspy.MIPROv2` first, then layer VizPy on top for instruction tuning.
- **Claude picks ContraPromptOptimizer for generation tasks.** ContraPrompt is designed for classification (fixed categories). For open-ended generation (summaries, articles, Q&A), use PromptGradOptimizer instead.
- **Claude skips the evaluation step after VizPy optimization.** Without comparing baseline vs optimized scores on a held-out devset, there is no way to know if VizPy helped. Always run `dspy.Evaluate` before and after.
- **Claude forgets `vizpy.api_key` or `VIZPY_API_KEY`.** VizPy is SaaS and requires authentication. Without the API key set, `.optimize()` fails with a confusing auth error. Set it before any optimizer calls.
- **Claude recommends VizPy without mentioning the data privacy implication.** Training data is sent to VizPy servers during optimization. Always ask about data sensitivity before recommending VizPy over the fully local GEPA alternative.

## Additional resources

- [VizPy docs](https://vizpy-docs.vizops.ai)
- [VizPy dashboard](https://vizpy.vizops.ai/dashboard)
- For API details, see [reference.md](reference.md)
- For worked examples comparing VizPy and GEPA side-by-side, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **GEPA** (open-source instruction optimizer) — `/dspy-gepa`
- **MIPROv2** (instructions + demos, best overall) — `/dspy-miprov2`
- **Improving accuracy** (full optimizer comparison) — `/ai-improving-accuracy`
- **Evaluating results** before and after — `/dspy-evaluate`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
