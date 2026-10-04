---
name: dspy-better-together
description: Jointly optimize prompts and model weights using dspy.BetterTogether for maximum accuracy. Use when you have already tried prompt-only optimization and want the next level — jointly tuning prompts and model weights for maximum quality. Common scenarios - you have maxed out prompt optimization and need the next level, combining instruction tuning with weight tuning for maximum quality, making a small model match a large model through joint optimization, or squeezing the last few percent of accuracy. Related - ai-fine-tuning, ai-improving-accuracy, ai-cutting-costs. Also used for dspy.BetterTogether, joint prompt and weight optimization, beyond prompt engineering, combine fine-tuning with prompt optimization, maximum possible quality from DSPy, hybrid optimization strategy, prompt optimization hit a ceiling, fine-tune and optimize prompts at the same time, advanced DSPy optimization, best possible accuracy, what to try after MIPROv2, next level AI quality.
---

# BetterTogether: Joint Prompt + Weight Optimization

Guide the user through using `dspy.BetterTogether` to get the best possible quality by combining prompt optimization and model fine-tuning in alternating rounds. Each round builds on the improvements from the previous one, creating compounding gains that beat either approach alone.

## Step 1 — Gather context

Before generating code, confirm:

1. **Baselines already run?** What accuracy did MIPROv2 and BootstrapFinetune achieve individually? If neither has been tried, redirect to `/ai-improving-accuracy` first — BetterTogether is only worth it after individual optimizers plateau.
2. **Data size?** How many labeled examples? Need 500+ (1000+ recommended). Fewer than 500 → `/ai-improving-accuracy` instead.
3. **Fine-tunable model?** OpenAI fine-tuning API, Databricks, or local GPU? This determines whether the weight step is feasible.
4. **Compute budget?** Each strategy round takes hours. The default `"p -> w -> p"` is hours to half a day.

## What it is

BetterTogether is a DSPy optimizer that alternates between prompt optimization (instructions, few-shot examples) and weight optimization (fine-tuning). Instead of running these independently, it chains them so each phase builds on the previous one's improvements:

1. **Prompt optimization** discovers effective task decompositions and reasoning strategies
2. **Weight optimization** specializes the model to execute those discovered patterns efficiently
3. **Repeated rounds** compound the gains -- each phase benefits from the prior improvements

Research shows this consistently outperforms either approach alone, with 5-78% gains over individual techniques (arXiv 2407.10930v2). A Databricks case study on IE Bench showed GEPA alone +2.1 points, fine-tuning alone +1.9 points, but combined they achieved +4.8 points over baseline.

## When to use

- You have **500+ labeled examples** and a reliable metric
- You've already tried prompt optimization (MIPROv2) and fine-tuning (BootstrapFinetune) separately and want more
- You want the **absolute best quality** and have the compute budget for multiple optimization rounds
- Fine-tuning alone didn't close the gap to your quality target
- You need a production-grade model and can afford longer optimization time

### When NOT to use

- You have fewer than 500 examples -- use MIPROv2 or BootstrapFewShot instead (see `/ai-improving-accuracy`)
- You haven't tried prompt optimization yet -- start with `/ai-improving-accuracy`
- Your baseline is below 50% -- fix your task definition or data first
- You're still iterating on what the task is -- BetterTogether is expensive to re-run
- You don't have access to a fine-tunable model (OpenAI `gpt-4o-mini`/`gpt-4o`, or local models)

## Prerequisites

Before starting, confirm:

- [ ] **Data**: 500+ labeled examples (1000+ recommended), split 80/10/10 (train/dev/test)
- [ ] **Baseline**: Measured accuracy from prompt optimization (MIPROv2) and/or fine-tuning (BootstrapFinetune)
- [ ] **Metric**: Automated metric that scores predictions
- [ ] **Fine-tunable model**: OpenAI fine-tuning API, Databricks, or local models with GPU
- [ ] **Budget**: Multiple optimization rounds cost 2-3x more than a single optimizer run

## Basic usage

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Define your program
class Classify(dspy.Signature):
    """Classify the support ticket into a category."""
    text: str = dspy.InputField()
    category: str = dspy.OutputField()

program = dspy.ChainOfThought(Classify)

# IMPORTANT: All predictors must have explicit LMs assigned
program.set_lm(lm)

# Define your metric
def metric(example, prediction, trace=None):
    return prediction.category.strip().lower() == example.category.strip().lower()

# Prepare data
trainset = [dspy.Example(text=x["text"], category=x["category"]).with_inputs("text") for x in data]
valset = trainset[800:900]
trainset = trainset[:800]

# Run BetterTogether with defaults
optimizer = dspy.BetterTogether(metric=metric)
compiled = optimizer.compile(program, trainset=trainset, valset=valset)
```

By default, BetterTogether uses:
- **`p`**: `BootstrapFewShotWithRandomSearch` for prompt optimization
- **`w`**: `BootstrapFinetune` for weight optimization
- **Strategy**: `"p -> w -> p"` (prompts, then weights, then prompts again)

## How it combines prompt and weight tuning

BetterTogether executes a **strategy string** that defines the order of optimization phases:

```
"p -> w -> p"
 |    |    |
 |    |    +-- Re-optimize prompts for the fine-tuned model
 |    +------- Fine-tune weights using the optimized prompts
 +------------ Optimize prompts first (instructions + few-shot)
```

At each step:

1. Shuffle the trainset (prevents overfitting to data order)
2. Run the designated optimizer on the current best program
3. Evaluate the result on the validation set
4. Record the candidate program and score
5. Move to the next step in the strategy

After all steps, BetterTogether returns the **best-scoring candidate** across all phases (ties broken by earlier position).

### Why alternating works

- Prompt optimization finds the right "recipe" -- effective instructions, good examples, useful reasoning patterns
- Weight optimization bakes those patterns into the model so it executes them reliably and cheaply
- Re-optimizing prompts after fine-tuning discovers new strategies that the specialized model can now handle

## Custom optimizers

Pass your own optimizers as keyword arguments. The keys become identifiers in the strategy string:

```python
optimizer = dspy.BetterTogether(
    metric=metric,
    p=dspy.GEPA(metric=metric, auto="medium"),
    w=dspy.BootstrapFinetune(metric=metric),
)

program.set_lm(lm)
compiled = optimizer.compile(
    program,
    trainset=trainset,
    valset=valset,
    strategy="p -> w -> p",
)
```

You can use any DSPy Teleprompter as an optimizer. Common choices:

| Key | Optimizer | Best for |
|-----|-----------|----------|
| `p` | `GEPA` | Instruction tuning, fewer examples |
| `p` | `MIPROv2` | Best general prompt optimization |
| `p` | `BootstrapFewShotWithRandomSearch` | Fast prompt optimization (default) |
| `w` | `BootstrapFinetune` | Weight optimization (default) |

## Key parameters

### Constructor: `BetterTogether(metric, **optimizers)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `metric` | `Callable` | Evaluation function `(example, prediction, trace=None) -> numeric` |
| `**optimizers` | keyword args | Custom optimizers. Keys become strategy identifiers (e.g., `p=GEPA(...)`, `w=BootstrapFinetune(...)`) |

### Compile: `optimizer.compile(student, *, trainset, ...)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `student` | `Module` | required | Program to optimize. **All predictors must have LMs via `set_lm()`** |
| `trainset` | `list[Example]` | required | Training examples |
| `valset` | `list[Example]` | `None` | Validation set. If `None`, splits from trainset |
| `valset_ratio` | `float` | `0.1` | Fraction of trainset to use as valset when `valset=None` |
| `strategy` | `str` | `"p -> w -> p"` | Optimizer execution order using keys from constructor |
| `teacher` | `Module` or `list[Module]` | `None` | Optional teacher program(s) for distillation |
| `num_threads` | `int` | `None` | Parallel threads for evaluation |
| `shuffle_trainset_between_steps` | `bool` | `True` | Shuffle trainset before each step |
| `seed` | `int` | `None` | Random seed for reproducibility |
| `optimizer_compile_args` | `dict` | `None` | Per-optimizer custom compile arguments |

### Return value

The compiled program has two extra attributes:

- `candidate_programs`: List of dicts with `'program'`, `'score'`, `'strategy'` keys, sorted by score descending
- `flag_compilation_error_occurred`: Boolean indicating if any step failed

## Strategy patterns

| Strategy | Rounds | Use case |
|----------|--------|----------|
| `"p -> w -> p"` | 3 | Default. Best balance of quality and cost |
| `"p -> w"` | 2 | Simpler, cheaper. Good starting point |
| `"w -> p"` | 2 | When your model needs weight tuning first |
| `"p -> w -> p -> w"` | 4 | Maximum quality, highest cost |

## Computational cost

BetterTogether runs multiple optimization rounds, so it costs more than individual optimizers:

| Strategy | Approximate cost | Time |
|----------|-----------------|------|
| `"p -> w"` | 1x prompt opt + 1x fine-tune | Hours |
| `"p -> w -> p"` (default) | 2x prompt opt + 1x fine-tune | Hours to half a day |
| `"p -> w -> p -> w"` | 2x prompt opt + 2x fine-tune | Half a day to a day |

Fine-tuning is the expensive part. Each fine-tuning round involves:
- Bootstrapping traces from training data
- Uploading traces to the fine-tuning provider
- Waiting for fine-tuning to complete (minutes to hours depending on provider)
- Evaluating the fine-tuned model

### Reducing cost

- Start with `"p -> w"` to see if two rounds are enough
- Use a smaller valset (but keep at least 50-100 examples)
- Use `optimizer_compile_args` to limit individual optimizer budgets

## BetterTogether vs individual optimizers

| Approach | Data needed | Quality | Cost | When to use |
|----------|-------------|---------|------|-------------|
| MIPROv2 alone | 200+ | Good | Low | First optimization attempt |
| BootstrapFinetune alone | 500+ | Better | Medium | When prompts hit a ceiling |
| BetterTogether | 500+ | Best | High | When you need maximum quality |

**Rule of thumb**: Try MIPROv2 first. If you're still short of your quality target, try BootstrapFinetune. If you need more, use BetterTogether.

## Important requirements

1. **Explicit LM assignment**: All predictors in your program must have LMs assigned via `set_lm()`. Global `dspy.configure(lm=...)` is not enough for BetterTogether.

```python
program = dspy.ChainOfThought(MySignature)
program.set_lm(lm)  # Required
```

2. **Fine-tunable model**: The weight optimizer needs a model that supports fine-tuning (OpenAI, Databricks, or local models with GPU).

3. **Validation data**: Provide either an explicit `valset` or set `valset_ratio > 0`. Without validation data, BetterTogether returns the latest program instead of the best one.

4. **Strategy keys must match**: Keys in the strategy string must match the keyword argument names from the constructor.

## Inspecting results

After compilation, examine all candidate programs:

```python
compiled = optimizer.compile(program, trainset=trainset, valset=valset)

# See all candidates ranked by score
for candidate in compiled.candidate_programs:
    print(f"Strategy step: {candidate['strategy']}, Score: {candidate['score']:.1f}%")

# Check if any errors occurred
if compiled.flag_compilation_error_occurred:
    print("Warning: one or more optimization steps failed")
```

## Error handling

BetterTogether has built-in resilience. If any optimization step fails:

- It logs the error and continues to the next step
- Returns the best program found before the failure
- Sets `flag_compilation_error_occurred = True` on the result

Always check this flag in production workflows.

## Gotchas

- **Claude forgets `set_lm()` and relies on global `dspy.configure()`.** BetterTogether requires every predictor to have an explicit LM assignment via `program.set_lm(lm)`. Without it, the weight optimizer cannot identify which model to fine-tune and raises an error. Always call `set_lm()` on the program before `compile()`.
- **Claude jumps straight to BetterTogether without trying simpler optimizers first.** BetterTogether costs 2-3x more than a single optimizer and takes hours. If you have not tried MIPROv2 or BootstrapFinetune individually first, start there — BetterTogether is only worth it when individual optimizers have plateaued.
- **Claude omits the validation set.** Without a `valset` (or `valset_ratio > 0`), BetterTogether returns the latest program instead of the best-scoring one across all phases. Always provide a valset or leave `valset_ratio=0.1` so the optimizer can select the best candidate.
- **Claude uses the same trainset for both training and validation.** If `valset` overlaps with `trainset`, the optimizer selects based on inflated scores. Use a held-out split or let BetterTogether auto-split via `valset_ratio`.
- **Claude does not check `flag_compilation_error_occurred` after compile.** If a fine-tuning step fails silently (API timeout, quota exceeded), BetterTogether returns the best program found before the failure. Always check `compiled.flag_compilation_error_occurred` and inspect `compiled.candidate_programs` to verify which steps completed.

## Additional resources

- [dspy.BetterTogether API docs](https://dspy.ai/api/optimizers/BetterTogether/)
- [reference.md](reference.md) — constructor parameters, compile() method, key behaviors
- [examples.md](examples.md) — combined optimization workflow, two-phase strategy with custom optimizers

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- For the full fine-tuning workflow, see `/ai-fine-tuning`
- For prompt optimization alone, see `/ai-improving-accuracy`
- For evaluation and metrics, see `/dspy-evaluate`
- For data preparation, see `/dspy-data`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
