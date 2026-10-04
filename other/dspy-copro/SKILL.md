---
name: dspy-copro
description: Use when you want to optimize instructions by generating many candidates and picking the best — useful when few-shot demos alone are not enough and you want to tune the task description itself. Common scenarios - your current task instructions produce mediocre results, you want to automatically generate and test many instruction variants, the task is hard to describe in one sentence, or few-shot examples alone are not improving quality enough. Related - ai-improving-accuracy, dspy-gepa, dspy-miprov2. Also used for dspy.COPRO, instruction optimization, optimize task description, generate better prompts automatically, prompt engineering automation, find the best instruction for my task, automatic prompt generation, instruction tuning without fine-tuning, COPRO vs MIPROv2, when to optimize instructions vs demos, instruction search, prompt optimization by generating candidates, systematic prompt improvement.
---

# Instruction Optimization with dspy.COPRO

Guide the user through using `dspy.COPRO` to automatically generate, evaluate, and select the best instructions for their DSPy program's signatures.

## Step 1 — Gather context

Before writing code, ask:

1. **What does your program do?** Which module does it use — `Predict`, `ChainOfThought`, a custom `dspy.Module`? What are the input/output fields?
2. **How many labeled training examples do you have?** COPRO needs 20-200. Below 20 the search is unreliable; above 200, consider MIPROv2 for joint instruction + demo optimization.
3. **Do you have an evaluation metric already, or do you need help writing one?** COPRO requires a metric — exact match, semantic similarity, LM-as-judge, etc.
4. **Do you want instructions only, or also few-shot demos?** If demos would help, use `dspy.MIPROv2` instead — it jointly optimizes both and typically outperforms COPRO.

## What is COPRO

`dspy.COPRO` (Collaborative Prompting) is a DSPy optimizer that improves your program by finding better instructions for each signature. Instead of you hand-writing prompt instructions, COPRO generates many candidate instructions, evaluates each one against your metric, and keeps the best.

Key properties:

- **Generates instruction candidates** -- uses an LM to propose alternative instructions for each predictor in your program
- **Evaluates each candidate** -- scores every candidate against your metric on the training set
- **Iterates in depth** -- runs multiple rounds, using top performers from round N to inform candidates in round N+1
- **Tunes instructions and prefixes** -- optimizes both the signature docstring (instruction) and output field prefixes
- **Works with any program** -- optimizes all predictors in a program sequentially

## When to use COPRO

Use `dspy.COPRO` when:

- You want to systematically search for better instructions rather than hand-tuning prompts
- You have a metric and 20-200 training examples
- Your program has one or a few predictors that need better instructions
- You want to explore a wide range of instruction phrasings (use high `breadth`)

Do **not** use COPRO when:

- You also want to optimize few-shot examples -- use `dspy.MIPROv2` instead (it tunes both instructions and demos)
- You have very few examples (<20) and want a lightweight optimizer -- use `dspy.GEPA` instead
- You want to fine-tune model weights -- use `dspy.BootstrapFinetune`
- You just need few-shot examples without instruction changes -- use `dspy.BootstrapFewShot`

## Basic usage

Three things are needed: a program, a metric, and training data.

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 1. Define a program
classify = dspy.ChainOfThought("text -> label")

# 2. Define a metric
def metric(example, prediction, trace=None):
    return prediction.label.lower() == example.label.lower()

# 3. Prepare training data
trainset = [
    dspy.Example(text="Love this product!", label="positive").with_inputs("text"),
    dspy.Example(text="Terrible experience.", label="negative").with_inputs("text"),
    # ... 20-200 examples
]

# 4. Optimize with COPRO
optimizer = dspy.COPRO(
    metric=metric,
    breadth=10,
    depth=3,
)
optimized = optimizer.compile(
    classify,
    trainset=trainset,
    eval_kwargs=dict(num_threads=4, display_progress=True),
)

# 5. Use the optimized program
result = optimized(text="The quality exceeded my expectations.")
print(result.label)
```

## Constructor parameters

```python
dspy.COPRO(
    prompt_model=None,      # LM for generating candidates (defaults to configured LM)
    metric=None,            # Evaluation function (required)
    breadth=10,             # Number of candidates per iteration (must be >1)
    depth=3,                # Number of optimization iterations
    init_temperature=1.4,   # Temperature for candidate generation
    track_stats=False,      # Collect optimization statistics
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt_model` | `dspy.LM` | `None` | LM used to generate instruction candidates. If `None`, uses the globally configured LM |
| `metric` | `Callable` | `None` | Scoring function with signature `(example, prediction, trace=None) -> float/bool`. Required |
| `breadth` | `int` | `10` | Number of candidate instructions generated per iteration. Higher = wider search, more LM calls |
| `depth` | `int` | `3` | Number of optimization rounds. Each round refines candidates from the previous round |
| `init_temperature` | `float` | `1.4` | Temperature for generating candidates. Higher = more diverse candidates |
| `track_stats` | `bool` | `False` | When `True`, collects per-iteration statistics (max, average, min, std dev of scores) |

## Compile method

```python
optimized = optimizer.compile(
    student,           # Program to optimize (modified in-place)
    trainset=trainset, # Training examples
    eval_kwargs={},    # Extra kwargs for dspy.Evaluate
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `student` | `dspy.Module` | The program to optimize. COPRO modifies it in-place and also returns it |
| `trainset` | `list[dspy.Example]` | Training examples for evaluating candidates |
| `eval_kwargs` | `dict` | Passed to `dspy.Evaluate` -- commonly `num_threads`, `display_progress`, `display_table` |

The returned program has additional metadata:

- `optimized.candidate_programs` -- dict of all evaluated candidates with their scores
- `optimized.total_calls` -- total LM API calls made during optimization
- `optimized.results_best` / `optimized.results_latest` -- per-iteration best/latest scores (only present when `track_stats=True`)

## The breadth parameter

`breadth` controls how many instruction candidates COPRO generates per iteration. It is the most important tuning knob.

| Breadth | Candidates per round | Total candidates (depth=3) | Use case |
|---------|---------------------|---------------------------|----------|
| 5 | 4 new + 1 base | ~15 | Quick test, cheap |
| 10 (default) | 9 new + 1 base | ~30 | Good balance |
| 20 | 19 new + 1 base | ~60 | Thorough search |
| 50 | 49 new + 1 base | ~150 | Exhaustive, expensive |

The first iteration generates `breadth - 1` new candidates from the base instruction. Subsequent iterations generate new candidates informed by the best performers so far.

**Cost note:** Each candidate is evaluated on the full `trainset`, so total LM calls scale as `breadth * depth * len(trainset)`. With breadth=10, depth=3, and 100 training examples, expect roughly 3,000 evaluation calls plus candidate generation calls.

## How COPRO generates candidates

COPRO follows a seeding-and-refinement loop:

1. **Seed phase (iteration 0):** Takes the existing instruction from each signature. Generates `breadth - 1` alternative instructions using temperature-controlled sampling from the prompt model.

2. **Evaluate phase:** Scores every candidate instruction by swapping it into the program and running the metric against the full training set. Duplicate (instruction, prefix) pairs are skipped.

3. **Refine phase (iterations 1 through depth-1):** Takes the top-performing candidates from the previous round. Generates new candidates informed by what worked and what did not.

4. **Multi-predictor handling:** When a program has multiple predictors, COPRO optimizes them sequentially. It locks in the best instruction for predictor 1 before moving to predictor 2, so later predictors benefit from earlier improvements.

5. **Selection:** After all iterations, the instruction with the highest metric score is selected for each predictor.

## Tracking optimization statistics

Enable `track_stats=True` to see how candidates perform across iterations:

```python
optimizer = dspy.COPRO(
    metric=metric,
    breadth=15,
    depth=3,
    track_stats=True,
)
optimized = optimizer.compile(
    my_program,
    trainset=trainset,
    eval_kwargs=dict(num_threads=4),
)
```

When `track_stats` is enabled, COPRO logs per-iteration statistics including max, average, min, and standard deviation of candidate scores. This helps you understand whether the search is converging or whether more breadth/depth would help.

## Using a separate prompt model

You can use a stronger (or cheaper) LM specifically for generating instruction candidates:

```python
# Use a strong model to generate candidates, evaluate with the production model
candidate_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
production_lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc.

dspy.configure(lm=production_lm)

optimizer = dspy.COPRO(
    prompt_model=candidate_lm,
    metric=metric,
    breadth=10,
    depth=3,
)
optimized = optimizer.compile(my_program, trainset=trainset, eval_kwargs={})
```

This is useful when you want a capable model to brainstorm instructions but evaluate and run with a cheaper model.

## Comparison with GEPA and MIPROv2

| Aspect | COPRO | GEPA | MIPROv2 |
|--------|-------|------|---------|
| **What it tunes** | Instructions + prefixes | Instructions | Instructions + few-shot demos |
| **Search strategy** | Breadth-first candidate generation | Evolutionary (genetic programming) | Bayesian optimization |
| **Data needed** | 20-200 examples | 20-100 examples | 50-500 examples |
| **Key parameter** | `breadth` (candidates per round) | Population/generations | `auto` ("light"/"medium"/"heavy") |
| **Cost** | Moderate (breadth * depth * trainset evals) | Low-moderate | Moderate-high |
| **Best for** | Exploring many instruction variants | Few examples, feedback-driven instruction tuning | Best overall prompt optimization |

**When to pick COPRO over alternatives:**

- You want explicit control over the search process (breadth, depth, temperature)
- You want to inspect all candidate instructions and their scores
- You care about instructions specifically, not few-shot examples
- You want a middle ground between GEPA (feedback-driven, competitive with MIPROv2) and MIPROv2 (heavyweight)

**When to pick MIPROv2 instead:**

- You want the best overall results (MIPROv2 optimizes both instructions and demos)
- You prefer an `auto` setting over manual tuning of search parameters
- You have enough data (200+) for MIPROv2 to shine

**When to pick GEPA instead:**

- You have very few examples (<50)
- You want evolutionary search rather than breadth-first generation
- You want something lightweight and fast

## Gotchas

- **Claude sets `breadth=1` which silently breaks optimization.** `breadth` must be greater than 1 — with breadth=1 there are no alternative candidates to evaluate. Use at least breadth=5 for a meaningful search.
- **Claude forgets that `compile()` modifies the student in-place.** Unlike most optimizers, COPRO mutates the program you pass to `compile()`. If you need the original program for baseline comparison, clone it first or create a fresh instance before calling `compile()`.
- **Claude passes `eval_kwargs` as positional instead of keyword.** The `compile()` signature is `compile(student, *, trainset, eval_kwargs)` — `trainset` and `eval_kwargs` are keyword-only. Always use `optimizer.compile(program, trainset=trainset, eval_kwargs={})`.
- **Claude uses COPRO when MIPROv2 would be better.** COPRO only optimizes instructions. If the task also benefits from few-shot demonstrations (most tasks do), MIPROv2 optimizes both and typically outperforms COPRO. Use COPRO when you specifically want instruction-only optimization or need to inspect all candidate instructions.
- **Claude skips the `eval_kwargs` parameter.** COPRO requires `eval_kwargs` to be passed to `compile()`, even if empty. Omitting it causes a TypeError. Always include `eval_kwargs={}` or `eval_kwargs=dict(num_threads=4)`.

## Additional resources

- [COPRO API docs](https://dspy.ai/api/optimizers/COPRO/)
- [reference.md](reference.md) — constructor parameters, compile method, candidate inspection
- [examples.md](examples.md) — worked examples with breadth search and configuration comparison

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Improving accuracy end-to-end** (metrics, evaluation, optimizer selection) -- see `/ai-improving-accuracy`
- **MIPROv2 for combined instruction + demo optimization** -- see `/dspy-miprov2`
- **GEPA for lightweight instruction tuning** -- see `/dspy-gepa`
- **Writing evaluation metrics** -- see `/dspy-evaluate`
- **Preparing training data** -- see `/dspy-data`
- **Signatures and instructions** -- see `/dspy-signatures`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
