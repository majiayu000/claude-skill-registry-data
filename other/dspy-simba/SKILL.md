---
name: dspy-simba
description: Optimize a DSPy program in small conservative steps using dspy.SIMBA (Stochastic Introspective Mini-Batch Ascent). Use when your program already works and you want to push accuracy higher without breaking what works, you need safe incremental improvement for a production program, or aggressive optimizers like MIPROv2 cause regressions. Also used for conservative optimization, incremental improvement, do not break what works, small targeted optimization, safe optimization for production, avoid regressions during optimization, production-safe optimizer, gentle optimization, when MIPROv2 changes too much, preserve existing quality, stable optimization, risk-averse prompt tuning, optimize without regressions.
---

# Small-Step Optimization with dspy.SIMBA

Guide the user through using `dspy.SIMBA` (Stochastic Introspective Mini-Batch Ascent) to optimize DSPy programs through incremental, targeted improvements rather than large sweeping changes.

## Step 1: Gather context

Before writing code, ask 2-4 of these to right-size the optimizer setup:

1. **What does your program currently do, and what metric are you optimizing?** (accuracy, F1, LM-as-judge, etc.) — affects whether to use binary vs float metric.
2. **Does the program already work reasonably well, or are you starting from scratch?** — SIMBA is designed for incremental improvement on a working baseline, not cold-start optimization.
3. **How many labeled training examples do you have?** — SIMBA needs at least 30-50; mini-batch size (`bsize`) should be smaller than your dataset.
4. **Is this a production program where regressions are unacceptable?** — affects `num_candidates`, `max_demos`, and whether to add a regression check before saving.

## What is dspy.SIMBA

`dspy.SIMBA` is a DSPy optimizer that improves programs by analyzing mini-batches of examples, identifying where the program struggles most, and making small targeted fixes -- either adding demonstrations or generating self-reflective rules. Instead of rewriting the entire prompt at once, SIMBA takes conservative steps, focusing on the examples with the highest output variability.

Key properties:

- **Mini-batch driven** -- samples small batches from the training set each iteration, rather than evaluating the entire dataset
- **Variability-focused** -- identifies the hardest examples by measuring output variability (gap between best and worst scores)
- **Two improvement strategies** -- adds few-shot demonstrations or generates introspective rules based on failure analysis
- **Maintains a program pool** -- keeps multiple candidate programs and probabilistically selects from the best performers
- **Incremental by design** -- each step makes a small, targeted change rather than overhauling the entire program

## When to use SIMBA

Use `dspy.SIMBA` when:

- You want conservative, incremental optimization that avoids regressions
- Your program already works reasonably well and you want to push accuracy higher
- You have a moderate dataset (50-500 examples) and want efficient optimization
- You need stability -- production systems where large prompt changes are risky
- You want to understand which examples are hardest for your program

Do **not** use SIMBA when:

- You are starting from scratch with no working program -- use `dspy.BootstrapFewShot` first
- You want maximum prompt optimization in one shot -- use `dspy.MIPROv2` instead
- You need to fine-tune model weights -- use `dspy.BootstrapFinetune`
- Your dataset is very small (fewer than 30 examples) -- mini-batch sampling needs enough data

## Basic usage

Three things are needed: a DSPy program, a metric function, and a training set.

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 1. Define your program
classify = dspy.ChainOfThought("text -> label")

# 2. Define a metric
def metric(example, prediction, trace=None):
    return prediction.label.lower() == example.label.lower()

# 3. Build training data
trainset = [
    dspy.Example(text="Great product!", label="positive").with_inputs("text"),
    dspy.Example(text="Terrible service.", label="negative").with_inputs("text"),
    # ... more examples
]

# 4. Optimize with SIMBA
optimizer = dspy.SIMBA(metric=metric)
optimized = optimizer.compile(classify, trainset=trainset)

# 5. Use the optimized program
result = optimized(text="This exceeded my expectations!")
print(result.label)

# 6. Save for later
optimized.save("optimized_classifier.json")
```

## How small-step optimization works

SIMBA's optimization loop proceeds through repeated small steps:

### Step 1: Trajectory sampling

SIMBA runs the current program pool on a mini-batch of examples. Each program runs with distinct LM configurations to produce diverse outputs, scored by your metric.

### Step 2: Bucket analysis

Examples are grouped and sorted by **output variability** -- the gap between the best and worst scores across runs. High-variability examples are where the program is inconsistent and has the most room for improvement.

### Step 3: Strategy application

For each high-variability example, SIMBA applies one of two strategies:

- **Demonstration injection** -- takes a successful output for a hard example and adds it as a few-shot demonstration, teaching the program by example
- **Introspective rules** -- uses the LM to analyze why certain examples fail, then generates natural-language rules (instructions) that address the failure patterns

### Step 4: Candidate evaluation

New candidate programs (with the added demos or rules) are evaluated on a fresh mini-batch. This prevents overfitting to the examples used for rule generation.

### Step 5: Pool registration

The best-performing candidates are added to the program pool. Future iterations select source programs using softmax sampling weighted by average scores -- favoring better programs while still exploring alternatives.

This cycle repeats for `max_steps` iterations, with each step making a small, targeted improvement.

## Constructor parameters

```python
dspy.SIMBA(
    *,                              # All parameters are keyword-only
    metric,                         # Scoring function (required)
    bsize=32,                       # Mini-batch size
    num_candidates=6,               # New candidates per iteration
    max_steps=8,                    # Number of optimization iterations
    max_demos=4,                    # Max demonstrations per predictor
    prompt_model=None,              # LM for generating rules (defaults to global LM)
    teacher_settings=None,          # Teacher model configuration dict
    demo_input_field_maxlen=100000, # Char limit for demo input fields
    num_threads=None,               # Parallel execution threads
    temperature_for_sampling=0.2,   # Temperature for trajectory sampling
    temperature_for_candidates=0.2, # Temperature for source program selection
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric` | `Callable` | (required) | Function `(example, prediction, trace=None) -> float` that scores outputs |
| `bsize` | `int` | `32` | Number of examples per mini-batch. Larger batches give more stable estimates but cost more LM calls |
| `num_candidates` | `int` | `6` | Candidate programs generated per iteration. More candidates explore more strategies but cost more |
| `max_steps` | `int` | `8` | Total optimization iterations. Each step samples a fresh mini-batch and produces new candidates |
| `max_demos` | `int` | `4` | Maximum few-shot demonstrations added to any predictor. Keeps prompts from growing too large |
| `prompt_model` | `dspy.LM` | `None` | LM used for generating introspective rules. Falls back to the globally configured LM if not set |
| `teacher_settings` | `dict` | `None` | Configuration dict for the teacher model |
| `demo_input_field_maxlen` | `int` | `100000` | Max characters for demo input fields. Reduce for tasks with very long inputs to keep prompts manageable |
| `num_threads` | `int` | `None` | Number of parallel threads for evaluation. Defaults to `dspy.settings.num_threads` |
| `temperature_for_sampling` | `float` | `0.2` | Temperature when running programs on mini-batches. Lower values produce more deterministic outputs |
| `temperature_for_candidates` | `float` | `0.2` | Temperature for softmax selection of source programs from the pool. Lower values favor the top performers |

### Choosing parameter values

**`bsize` (mini-batch size):**

| Value | Use case |
|-------|----------|
| 16 | Small datasets (50-100 examples), faster iterations |
| 32 | Default, good balance for most tasks |
| 64 | Larger datasets, more stable gradient estimates |

**`max_steps`:**

| Value | Use case |
|-------|----------|
| 4-6 | Quick optimization pass, limited budget |
| 8 | Default, enough steps for meaningful improvement |
| 12-16 | Longer optimization for complex programs or larger datasets |

**`num_candidates`:**

| Value | Use case |
|-------|----------|
| 3-4 | Budget-conscious, smaller search space |
| 6 | Default, reasonable exploration |
| 8-10 | Wider search when you have LM budget to spare |

## Key methods

### compile()

Runs the optimization loop and returns the best program found.

```python
optimized = optimizer.compile(program, trainset=trainset, seed=0)
```

The `seed` parameter (default `0`) controls random sampling for reproducible results.

The returned program includes two additional attributes:

- **`candidate_programs`** -- list of scored alternative programs discovered during optimization. Useful for ensemble strategies or analyzing what SIMBA tried.
- **`trial_logs`** -- per-batch metrics from each optimization step. Useful for understanding how performance evolved.

### get_params()

Returns the optimizer's configuration as a dictionary. Useful for logging and experiment tracking.

```python
params = optimizer.get_params()
print(params)
# {'bsize': 32, 'num_candidates': 6, 'max_steps': 8, ...}
```

## Inspecting optimization results

After optimization, examine what SIMBA found:

```python
optimizer = dspy.SIMBA(metric=metric)
optimized = optimizer.compile(program, trainset=trainset)

# Check the candidate pool
for i, (prog, score) in enumerate(optimized.candidate_programs):
    print(f"Candidate {i}: score={score:.3f}")

# Review trial logs to see improvement over time
for step, log in enumerate(optimized.trial_logs):
    print(f"Step {step}: {log}")
```

## Comparison with other optimizers

| Aspect | `dspy.SIMBA` | `dspy.MIPROv2` | `dspy.BootstrapFewShot` |
|--------|-------------|----------------|------------------------|
| **Strategy** | Small incremental steps on mini-batches | Full instruction + demo optimization | Bootstrap few-shot examples |
| **Change size** | Small, targeted per iteration | Can rewrite entire instructions | Adds demonstrations only |
| **Risk of regression** | Low -- changes are conservative | Higher -- rewrites can miss edge cases | Low -- additive only |
| **Data needed** | 50-500 examples | 200+ examples | 50+ examples |
| **Cost** | Moderate (mini-batch sampling) | Higher (full search) | Lower (single pass) |
| **Best for** | Incremental improvement, production stability | Maximum prompt quality | Quick first optimization |
| **Introspection** | Yes -- analyzes failures | Yes -- generates instructions | No |

### Optimization workflow

A common approach is to layer optimizers:

1. **Start with `BootstrapFewShot`** to get a working baseline with good demonstrations
2. **Then run SIMBA** to incrementally improve by targeting the hardest examples
3. **Optionally run `MIPROv2`** if you need maximum quality and can tolerate larger changes

```python
# Step 1: Bootstrap baseline
bootstrap = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
baseline = bootstrap.compile(program, trainset=trainset)

# Step 2: Incrementally improve with SIMBA
simba = dspy.SIMBA(metric=metric, max_steps=8)
improved = simba.compile(baseline, trainset=trainset)
```

## Typical improvement trajectory

Expect incremental gains per step rather than a single large jump:

| Stage | Example score | Notes |
|-------|-------------|-------|
| Unoptimized baseline | ~60-70% | Raw program with no demos or instructions |
| After BootstrapFewShot | ~75-85% | Good demos added, biggest single jump |
| After SIMBA (4-8 steps) | ~80-90% | Incremental +3-8% from targeting hard examples |

The exact numbers depend on your task, data, and LM. SIMBA shines on the incremental step — it finds the examples your program is inconsistent on and fixes those specifically.

## Gotchas

1. **Claude uses binary 0/1 metrics with SIMBA.** SIMBA measures output variability (gap between best and worst scores) to find hard examples. With binary metrics, the variability is either 0 or 1 -- SIMBA cannot distinguish "almost right" from "completely wrong." Return floats between 0.0 and 1.0 so SIMBA can rank examples by difficulty meaningfully.
2. **Claude runs SIMBA on an unoptimized program.** SIMBA makes small incremental improvements -- it is not designed for large jumps from a blank slate. Run `BootstrapFewShot` first to establish a baseline with good demonstrations, then run SIMBA on the bootstrapped program to push accuracy higher.
3. **Claude sets `max_demos` too high.** Each demo added by SIMBA increases prompt length. With `max_demos=10` and multi-paragraph examples, prompts can exceed context limits or degrade quality from demo overload. Keep `max_demos` at 4-6 (the default is 4).
4. **Claude uses the same LM for `prompt_model` and the main program.** SIMBA's introspective rules are generated by analyzing failures and writing natural-language instructions. If your main LM is small (e.g., `gpt-4o-mini`), the rule quality suffers. Set `prompt_model` to a stronger model for rule generation while keeping the cheaper model for the main program.
5. **Claude ignores `candidate_programs` and `trial_logs` on the result.** After `compile()`, the returned program has `candidate_programs` (list of scored alternatives) and `trial_logs` (per-step metrics). Inspecting these reveals whether optimization plateaued, which strategies worked, and whether alternative candidates might be better for specific inputs.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Quick-start optimization** with few-shot examples -- see `/ai-improving-accuracy`
- **Evaluating your program** before and after optimization -- see `/dspy-evaluate`
- **Building the program to optimize** -- see `/dspy-chain-of-thought` or `/dspy-modules`
- **Preparing training data** -- see `/dspy-data`
- **Full prompt + instruction optimization** (higher ceiling, more data) -- see `/dspy-miprov2`
- **Evolution-based prompt optimization** (reflection-driven, ~50 examples) -- see `/dspy-gepa`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.SIMBA API docs](https://dspy.ai/api/optimizers/SIMBA/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
