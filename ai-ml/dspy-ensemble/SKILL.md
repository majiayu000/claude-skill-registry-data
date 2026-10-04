---
name: dspy-ensemble
description: Combines multiple optimized DSPy programs into a single ensemble via majority voting, averaging, or custom reduce functions using dspy.Ensemble. Use when you have run multiple optimization passes and want to combine the best programs for more reliable outputs, when majority voting across programs would improve accuracy, when one program alone is not reliable enough, or when different optimizers found different strengths you want to combine. Also used for dspy.Ensemble, combine multiple optimized programs, majority voting across models, ensemble of DSPy programs, voting for reliability, reduce variance with multiple programs, aggregate predictions, combine outputs from different optimizers, when one program is not reliable enough, model committee, ensemble for production robustness, multiple programs one answer, ai-improving-accuracy cross-optimizer, ai-making-consistent multiple programs.
---

# Combine Programs with dspy.Ensemble

Guide the user through using DSPy's `Ensemble` optimizer to combine multiple optimized programs into a single ensemble that aggregates their outputs. This is useful when you have run several optimization passes (different optimizers, different hyperparameters, different random seeds) and want to combine them for more robust predictions.

## Step 1 — Gather context

Before generating code, ask:

1. **How many optimized programs do you have?** (Ensemble only makes sense with 2+. If you have one, consider `dspy.BestOfN` instead.)
2. **What do the outputs look like?** Categorical labels or short answers → use `dspy.majority`. Numeric scores → use a custom averaging reduce_fn. Complex structured outputs → design the reduce_fn around the key field.
3. **Do you have latency or cost constraints?** If yes, set `size=N` to run only a subset of programs per call rather than all of them.
4. **Are the programs already compiled, or do you need to optimize them first?** If not yet compiled, generate the optimization step too.

## What is Ensemble

`dspy.Ensemble` is an optimizer (teleprompter) that takes a list of DSPy programs and returns a single `EnsembledProgram`. When you call the ensembled program, it runs each constituent program on the same inputs and aggregates the results using a reduce function you provide.

```
Program A ──┐
Program B ──┼──> Run all ──> reduce_fn ──> Single output
Program C ──┘
```

Unlike other optimizers that tune prompts or weights, Ensemble does not change the programs themselves. It combines their outputs at inference time.

## When to use Ensemble

- **You ran multiple optimization passes** (e.g., several BootstrapFewShot runs with different seeds) and want to combine the best of each
- **You want majority voting** -- run several programs and pick the most common answer for higher reliability
- **You want to average numeric outputs** -- combine scores or probabilities from multiple models
- **Different optimizers produced different strengths** -- one program is good at precision, another at recall, and you want both
- **You need a quick reliability boost** -- ensembling is a well-known technique to reduce variance

Do **not** use Ensemble when:
- You only have one program (nothing to ensemble)
- Latency is critical -- ensembling runs every program, multiplying your inference time
- Cost is a hard constraint -- you pay for every program in the ensemble
- Your programs produce complex structured outputs that are hard to aggregate

## Basic usage

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# 1. Define your base program
qa = dspy.ChainOfThought("question -> answer")

# 2. Create a training set and metric
trainset = [
    dspy.Example(question="What is the capital of France?", answer="Paris").with_inputs("question"),
    dspy.Example(question="What is 2 + 2?", answer="4").with_inputs("question"),
    # ... more examples
]

def exact_match(example, pred, trace=None):
    return pred.answer.strip().lower() == example.answer.strip().lower()

# 3. Run multiple optimization passes to get different programs
programs = []
for i in range(3):
    optimizer = dspy.BootstrapFewShot(
        metric=exact_match,
        max_bootstrapped_demos=4,
        max_labeled_demos=4,
    )
    optimized = optimizer.compile(qa, trainset=trainset)
    programs.append(optimized)

# 4. Combine with Ensemble using majority voting
ensemble_optimizer = dspy.Ensemble(reduce_fn=dspy.majority, size=None)
ensemble_program = ensemble_optimizer.compile(programs)

# 5. Use the ensemble like any module
result = ensemble_program(question="What is the capital of Germany?")
print(result.answer)
```

## Constructor parameters

```python
dspy.Ensemble(
    reduce_fn=None,     # Function to aggregate outputs from all programs
    size=None,          # How many programs to sample (None = use all)
    deterministic=False,  # Must be False (deterministic mode not yet implemented)
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `reduce_fn` | `Callable \| None` | Aggregation function applied to the list of outputs. If `None`, returns the raw list of predictions. |
| `size` | `int \| None` | Number of programs to randomly sample from the ensemble. `None` means use all programs. |
| `deterministic` | `bool` | Reserved for future use. Must be `False`. |

### compile method

```python
ensemble_optimizer.compile(programs)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `programs` | `list[dspy.Module]` | List of DSPy programs to ensemble |

Returns an `EnsembledProgram` that runs the selected programs and applies `reduce_fn`.

## Reduce functions

The reduce function determines how outputs from multiple programs are combined into a single result.

### dspy.majority (built-in)

The most common reduce function. It picks the most frequent output value across all programs -- majority voting.

```python
ensemble = dspy.Ensemble(reduce_fn=dspy.majority)
```

Use `dspy.majority` when:
- Outputs are categorical (classification labels, short factual answers, yes/no)
- You want the most robust answer -- the one most programs agree on

### Custom reduce: averaging numeric outputs

```python
def average_scores(predictions):
    """Average a numeric output field across all predictions."""
    scores = [float(p.score) for p in predictions]
    avg = sum(scores) / len(scores)
    # Return a Prediction-like object with the averaged score
    return predictions[0].__class__(score=str(avg))

ensemble = dspy.Ensemble(reduce_fn=average_scores)
```

### Custom reduce: weighted voting

```python
def weighted_vote(predictions):
    """Pick the answer backed by the most programs, with confidence weighting."""
    from collections import Counter
    votes = Counter(p.answer for p in predictions)
    winner = votes.most_common(1)[0][0]
    # Return a prediction with the winning answer
    return predictions[0].__class__(answer=winner)

ensemble = dspy.Ensemble(reduce_fn=weighted_vote)
```

### No reduce function

If you pass `reduce_fn=None`, the ensembled program returns the raw list of predictions from all programs. This is useful when you want to implement custom post-processing logic outside the ensemble.

```python
ensemble = dspy.Ensemble(reduce_fn=None)
ensemble_program = ensemble.compile(programs)

# Returns a list of predictions
all_predictions = ensemble_program(question="What is DSPy?")
# Process them yourself
for pred in all_predictions:
    print(pred.answer)
```

## Combining different optimizers

One of the most powerful uses of Ensemble is combining programs from different optimization strategies. Each optimizer may find different strengths.

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question -> answer")

# Program 1: Optimized with BootstrapFewShot
opt1 = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
prog1 = opt1.compile(qa, trainset=trainset)

# Program 2: Optimized with MIPROv2
opt2 = dspy.MIPROv2(metric=metric, auto="light")
prog2 = opt2.compile(qa, trainset=trainset)

# Program 3: Optimized with BootstrapFewShotWithRandomSearch
opt3 = dspy.BootstrapFewShotWithRandomSearch(
    metric=metric,
    max_bootstrapped_demos=4,
    num_candidate_programs=5,
)
prog3 = opt3.compile(qa, trainset=trainset)

# Ensemble all three
ensemble = dspy.Ensemble(reduce_fn=dspy.majority)
combined = ensemble.compile([prog1, prog2, prog3])

result = combined(question="What is the tallest mountain?")
print(result.answer)
```

This approach works because different optimizers explore different parts of the prompt space. BootstrapFewShot finds good demonstrations, MIPROv2 finds good instructions, and combining them via voting smooths out individual weaknesses.

## Sampling with size

When you have many optimized programs (e.g., from a large random search), you can use `size` to randomly sample a subset at inference time. This reduces cost while still benefiting from diversity.

```python
# You have 10 programs from BootstrapFewShotWithRandomSearch
programs = [...]  # 10 optimized programs

# Only run 3 of them per inference call (randomly sampled)
ensemble = dspy.Ensemble(reduce_fn=dspy.majority, size=3)
ensemble_program = ensemble.compile(programs)
```

Each call to `ensemble_program` randomly picks 3 of the 10 programs, runs them, and applies majority voting. This balances diversity against cost.

## Cost and latency considerations

Ensemble multiplies your inference cost and latency by the number of programs (or `size` if set):

| Programs | Cost multiplier | Latency (sequential) |
|----------|-----------------|----------------------|
| 3 | 3x | 3x |
| 5 | 5x | 5x |
| 10 | 10x | 10x |

Ways to manage this:
- **Use `size` to cap the number of programs** run per inference call
- **Use cheaper models** for the ensemble members and reserve expensive models for critical paths
- **Ensemble at evaluation time only** to pick the single best program, then deploy that one program in production
- **Parallelize** if your infrastructure supports concurrent LM calls -- the programs are independent

## Ensemble vs BestOfN

Both combine multiple outputs, but they work differently:

| | Ensemble | BestOfN |
|---|---------|---------|
| **What it combines** | Different optimized programs | Multiple runs of the same program |
| **Selection method** | Voting / averaging across programs | Reward function picks the best single run |
| **Diversity source** | Different prompts/demos from optimization | Temperature sampling of the same prompt |
| **When to use** | You have multiple optimized programs | You have one program and a scoring metric |
| **Optimizer type** | Combines at the program level | Combines at the inference level |

You can even stack them: ensemble multiple optimized programs, then wrap the ensemble with BestOfN for additional quality.

## Expected improvement

Ensemble typically adds 3-10 percentage points of accuracy over the best individual program when programs are genuinely diverse (different optimizers, different seeds, different LMs). Near-zero gains when programs are nearly identical — run `dspy.Evaluate` on each individual program first and confirm they have meaningfully different failure modes before committing to ensemble inference cost.

## Gotchas

- **Claude passes a single program instead of a list to `compile()`.** `Ensemble.compile()` expects a `list[dspy.Module]`, not a single module. Always wrap even two programs in a list: `ensemble.compile([prog1, prog2])`.
- **Claude forgets that each ensemble member uses its own LM context.** Programs optimized under different `dspy.configure(lm=...)` calls retain their LM binding. You do not need to re-configure the LM before calling the ensemble -- each program already knows which LM to use.
- **Claude sets `deterministic=True` expecting reproducible sampling.** The `deterministic` parameter is reserved but not yet implemented -- setting it to `True` raises an error. Leave it at the default `False`.
- **Claude uses Ensemble when BestOfN is the right tool.** Ensemble combines different optimized programs. If you have one program and want to run it multiple times with temperature sampling and pick the best output, use `dspy.BestOfN` instead.
- **Claude builds a custom reduce function that returns a raw string instead of a Prediction.** The `reduce_fn` receives a list of `dspy.Prediction` objects and must return a `dspy.Prediction` (or compatible object). Returning a plain string breaks downstream field access.

## Additional resources

- [Ensemble API docs](https://dspy.ai/api/optimizers/Ensemble/)
- [reference.md](reference.md) -- constructor parameters, compile method, reduce function protocol
- [examples.md](examples.md) -- worked examples with majority voting and multi-model ensembles

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **BestOfN** for picking the best from multiple runs of a single program -- see `/dspy-best-of-n`
- **BootstrapFewShot** for generating the programs to ensemble -- see `/ai-improving-accuracy`
- **MIPROv2** for instruction optimization -- see `/ai-improving-accuracy`
- **Evaluate** for measuring ensemble quality with metrics -- see `/dspy-evaluate`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
