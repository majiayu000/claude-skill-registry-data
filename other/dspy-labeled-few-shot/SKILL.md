---
name: dspy-labeled-few-shot
description: Attach hand-curated labeled examples as few-shot demonstrations using dspy.LabeledFewShot — no bootstrapping, no metric, no LM calls at compile time. Use when you have hand-picked high-quality examples and want to inject them directly as prompt demos without bootstrapping. Common scenarios - expert-curated examples you trust more than bootstrapped ones, hand-picked demonstrations for high-stakes tasks, using existing labeled data directly without bootstrapping, or full control over which examples appear in the prompt. Related - dspy-bootstrap-few-shot, dspy-knn-few-shot, ai-generating-data. Also used for dspy.LabeledFewShot, hand-picked examples in prompt, curated demonstrations, use my own examples directly, manual few-shot setup, expert-labeled demonstrations, no bootstrapping just my examples, static few-shot with labeled data, gold standard examples, controlled few-shot demos, fixed example set in prompt.
---

# Hand-Picked Demonstrations with dspy.LabeledFewShot

Guide the user through using `dspy.LabeledFewShot` -- the simplest DSPy optimizer. It takes labeled examples you provide and attaches them as few-shot demonstrations to your program's predictors. No bootstrapping, no metric, no LM calls during optimization.

## Step 1 — Gather context

Before writing code, ask:

1. **How many hand-picked examples do you have?** This sets a good `k` value — typically 25-50% of trainset size, capped at the default of 16.
2. **Are these examples hand-curated or programmatically generated?** If generated, `dspy.BootstrapFewShot` may be better — it evaluates examples against a metric and keeps only the ones that help.
3. **Does your program have multiple predictors with different signatures?** Every predictor gets the same demos, so all fields across all signatures must exist in the training examples.
4. **Have you measured zero-shot accuracy yet?** Useful to know the baseline before adding demonstrations.

## What is LabeledFewShot

`dspy.LabeledFewShot` is an optimizer that takes a set of labeled training examples and injects them directly as few-shot demonstrations into every predictor in your DSPy program.

- **No metric required** -- unlike other optimizers, it does not evaluate or filter examples
- **No LM calls during compilation** -- it just copies your examples into the prompt
- **Deterministic** -- uses a fixed random seed (0) for reproducible example selection
- **Fast** -- compilation is instant because there is no search or bootstrapping step

Under the hood, `compile()` creates a copy of your program, iterates over each predictor, and assigns up to `k` examples from your training set as that predictor's `demos`.

## When to use LabeledFewShot

| Use `LabeledFewShot` when... | Use something else when... |
|---|---|
| You have hand-curated, high-quality examples | You want the optimizer to discover good examples (`BootstrapFewShot`) |
| You want a quick baseline before trying fancier optimizers | You need instruction tuning too (`MIPROv2`) |
| You need full control over which demonstrations the LM sees | You have enough data to let DSPy search (`BootstrapFewShotWithRandomSearch`) |
| Your task is simple enough that a few good examples suffice | Quality requires filtering examples by a metric |
| You want deterministic, reproducible behavior | You want the optimizer to explore different combinations |

**Rule of thumb:** Use `LabeledFewShot` as your first optimization step. If accuracy is not high enough, upgrade to `BootstrapFewShot` which evaluates examples against a metric and keeps only the ones that work.

## API reference

### Constructor

```python
dspy.LabeledFewShot(k=16)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `k` | `int` | `16` | Maximum number of demonstration examples to include per predictor |

### compile()

```python
optimizer.compile(student, *, trainset, sample=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `student` | `dspy.Module` | required | The DSPy program to optimize |
| `trainset` | `list[dspy.Example]` | required | Labeled examples to use as demonstrations |
| `sample` | `bool` | `True` | `True` = randomly sample `k` examples; `False` = take the first `k` sequentially |

**Returns:** A copy of `student` with demonstrations attached to each predictor.

If `trainset` is empty, the student is returned unmodified.

## Basic usage

```python
import dspy
from typing import Literal

# Configure any LM provider
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# 1. Define your signature
class ClassifyIntent(dspy.Signature):
    """Classify the user message into an intent category."""
    message: str = dspy.InputField(desc="User message")
    intent: Literal["question", "complaint", "praise", "request"] = dspy.OutputField()

# 2. Build your program
classify = dspy.Predict(ClassifyIntent)

# 3. Create hand-picked training examples
trainset = [
    dspy.Example(message="How do I reset my password?", intent="question").with_inputs("message"),
    dspy.Example(message="This is broken and I want a refund", intent="complaint").with_inputs("message"),
    dspy.Example(message="Your team was incredibly helpful!", intent="praise").with_inputs("message"),
    dspy.Example(message="Please update my billing address", intent="request").with_inputs("message"),
    dspy.Example(message="What formats do you export to?", intent="question").with_inputs("message"),
    dspy.Example(message="The app crashes every time I open it", intent="complaint").with_inputs("message"),
]

# 4. Compile with LabeledFewShot
optimizer = dspy.LabeledFewShot(k=4)
optimized = optimizer.compile(classify, trainset=trainset)

# 5. Use the optimized program -- it now includes few-shot demos in every call
result = optimized(message="Can you send me last month's invoice?")
print(result.intent)  # request
```

**Verify it worked:** Run a few test inputs and inspect `dspy.inspect_history(n=1)` to confirm demos appear in the prompt. If the prompt looks identical to the zero-shot version, check that `.with_inputs()` is called on every training example.

## How example selection works

When `sample=True` (the default):
- DSPy randomly selects `k` examples from `trainset` using a fixed seed (0)
- Every predictor in your program gets the same set of demos
- The selection is reproducible across runs because of the fixed seed

When `sample=False`:
- DSPy takes the first `k` examples from `trainset` in order
- Use this when the order of your examples matters or you want exact control

If your trainset has fewer than `k` examples, all examples are used.

## Choosing k

The `k` parameter controls how many demonstrations appear in the prompt.

- **Smaller k (2-4):** Lower token cost, faster inference. Good when your examples are diverse and high-quality.
- **Larger k (8-16):** More context for the LM. Good when the task has many edge cases or subtle distinctions.
- **Default (16):** A reasonable starting point. Reduce if you hit token limits or want faster responses.

Keep in mind that each demonstration adds tokens to every LM call. For long input/output fields, use a smaller `k` to stay within context limits.

## Using sample=False for ordered examples

When you want precise control over which examples appear, disable sampling:

```python
# Place your best, most representative examples first
trainset = [
    dspy.Example(message="What's your return policy?", intent="question").with_inputs("message"),
    dspy.Example(message="This product is defective", intent="complaint").with_inputs("message"),
    dspy.Example(message="Love the new feature!", intent="praise").with_inputs("message"),
    dspy.Example(message="Please cancel my subscription", intent="request").with_inputs("message"),
    # ... more examples, ordered by importance
]

optimizer = dspy.LabeledFewShot(k=4)
optimized = optimizer.compile(classify, trainset=trainset, sample=False)
# The first 4 examples are used as demos, in order
```

## Saving and loading an optimized program

After compilation, save the optimized program so you can reuse it without recompiling:

```python
# Save
optimized.save("intent_classifier.json")

# Load later
loaded = dspy.Predict(ClassifyIntent)
loaded.load("intent_classifier.json")
result = loaded(message="How do I upgrade my plan?")
```

## Multi-predictor programs

`LabeledFewShot` attaches demos to every predictor in your program. This works with multi-step pipelines too:

```python
class SupportRouter(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(ClassifyIntent)
        self.respond = dspy.ChainOfThought("message, intent -> response")

    def forward(self, message):
        intent = self.classify(message=message).intent
        return self.respond(message=message, intent=intent)

router = SupportRouter()

# Both self.classify and self.respond get demos from the same trainset
optimizer = dspy.LabeledFewShot(k=3)
optimized_router = optimizer.compile(router, trainset=trainset)
```

Note: every predictor receives demos from the same trainset. If your predictors have different signatures, make sure your training examples include all fields needed across all predictors, or consider compiling predictors separately.

## When to upgrade to BootstrapFewShot

`LabeledFewShot` is a great starting point, but it has limitations:

1. **No quality filtering** -- it uses your examples as-is, even if some are misleading or ambiguous
2. **No metric evaluation** -- it cannot tell which examples actually help the LM perform better
3. **Same demos for all predictors** -- it does not tailor demonstrations per predictor

**Typical improvement:** Adding 4-8 curated demos with `LabeledFewShot` often improves task accuracy by 5-15% over zero-shot. If that is not enough, `BootstrapFewShot` commonly adds another 10-20% by filtering to only the examples that led to correct outputs.

`dspy.BootstrapFewShot` addresses all three. It runs your program on each training example, evaluates with a metric, and keeps only the demonstrations that led to correct outputs. The upgrade is straightforward:

```python
# Before: LabeledFewShot (no metric needed)
optimizer = dspy.LabeledFewShot(k=4)
optimized = optimizer.compile(program, trainset=trainset)

# After: BootstrapFewShot (needs a metric)
def metric(example, prediction, trace=None):
    return prediction.intent == example.intent

optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(program, trainset=trainset)
```

## Gotchas

1. **Claude forgets `.with_inputs()` on training examples.** Without `.with_inputs("field_name")`, DSPy does not know which fields are inputs vs labels. The demonstrations appear malformed in the prompt — the LM sees all fields as input, which confuses it. Always call `.with_inputs()` on every `dspy.Example` in your trainset.
2. **Claude uses LabeledFewShot when the user needs metric-driven selection.** LabeledFewShot uses examples as-is with no quality filtering. If the user mentions "accuracy is low" or "some examples are noisy," recommend `BootstrapFewShot` instead — it evaluates examples against a metric and keeps only the ones that help.
3. **Claude sets `k` larger than the trainset without explaining the behavior.** When `k` exceeds `len(trainset)`, DSPy silently uses all available examples. This is fine, but Claude should tell the user: "You have 5 examples and k=16, so all 5 will be used as demos."
4. **Claude creates separate trainsets for multi-predictor programs.** `LabeledFewShot` assigns the same demos to every predictor. If predictors have different signatures, the examples need all fields across all signatures, or the user should compile predictors separately. Claude sometimes splits the trainset incorrectly — explain the shared-demo behavior.

## Additional resources

- [dspy.LabeledFewShot API docs](https://dspy.ai/api/optimizers/LabeledFewShot/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Creating training examples** (dspy.Example, with_inputs, datasets) -- see `/dspy-data`
- **Defining signatures** (inline and class-based, typed fields) -- see `/dspy-signatures`
- **BootstrapFewShot** (metric-driven selection, filters demos by correctness) -- see `/dspy-bootstrap-few-shot`
- **KNNFewShot** (dynamically selects demos per input via similarity) -- see `/dspy-knn-few-shot`
- **Improving accuracy** with optimized demos -- see `/ai-improving-accuracy`
- **Evaluating your program** to measure if LabeledFewShot is enough -- see `/dspy-evaluate`
- **Building modules** with multiple predictors -- see `/dspy-modules`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
