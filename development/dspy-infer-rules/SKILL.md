---
name: dspy-infer-rules
description: Use when you want to extract interpretable decision logic from labeled examples — generating explicit rules that explain patterns in your data. Common scenarios - extracting business rules from labeled classification examples, understanding why a model makes certain predictions, generating human-readable decision criteria from data, building interpretable classifiers, or documenting implicit labeling logic from annotators. Related - ai-following-rules, ai-sorting. Also used for dspy.InferRules, extract rules from examples, interpretable AI decisions, understand classification logic, generate decision rules from labels, explainable AI with DSPy, turn labeled data into explicit rules, human-readable classification rules, rule extraction from training data, when you need to explain why AI decided, interpretable model logic, audit AI decision process, regulatory compliance explainability, extract patterns from labeled data.
---

# Extracting Decision Rules with dspy.InferRules

Guide the user through using `dspy.InferRules` to discover explicit, human-readable rules from labeled examples and inject them into program instructions.

## Step 1 — Gather context

Ask before writing code:

1. **What is the task?** Classification, routing, content moderation, or triage? InferRules works best on tasks with consistent, describable patterns — not creative or open-ended generation.
2. **How many labeled examples?** InferRules needs at least ~20 examples; 40-100 is typical. If fewer than ~20, building a larger labeled set first is more valuable than optimizing.
3. **Do you have a separate validation set, or should we split training data?** A dedicated validation set gives better rule evaluation and leaves more examples for training. Relevant if the total dataset is under ~50 examples.
4. **Why do you need interpretable rules?** Regulatory compliance, stakeholder sign-off, debugging, or human-in-the-loop editing? This shapes how aggressively to tune `num_rules` and `num_candidates`.

## What is dspy.InferRules

`dspy.InferRules` is a DSPy optimizer that analyzes your training examples and extracts natural-language rules describing the decision patterns it finds. These rules are then appended to the instructions of each predictor in your program. The result is a compiled program whose prompts contain explicit, interpretable decision logic -- not opaque few-shot examples.

It inherits from `BootstrapFewShot`, so it first bootstraps demonstrations and then goes further by inducing rules from those demonstrations.

Key properties:

- **Extracts human-readable rules** -- the discovered logic is plain English, not weights or embeddings
- **Builds on BootstrapFewShot** -- bootstraps demonstrations first, then induces rules from them
- **Generates multiple candidates** -- creates several rule-enhanced programs and picks the best one on a validation set
- **Enhances instructions** -- appends discovered rules directly to each predictor's signature instructions
- **Gracefully handles context limits** -- iteratively removes examples if they exceed the LM's context window

## When to use InferRules

Use `dspy.InferRules` when:

- You have labeled examples and want to understand the patterns behind them
- Interpretability matters -- you need to explain decisions to stakeholders or auditors
- Your task has consistent, describable rules (classification, routing, moderation, triage)
- You want to improve a program's instructions without manually writing rules
- You need a compiled program that works without few-shot demonstrations at inference time

Do **not** use InferRules when:

- You have very few examples (fewer than ~20) -- rules need enough data to generalize
- The task has no consistent patterns (creative writing, open-ended generation)
- You want to tune few-shot examples only -- use `dspy.BootstrapFewShot` instead
- You want full prompt + demo optimization -- use `dspy.MIPROv2` instead
- You need weight tuning -- use `dspy.BootstrapFinetune`

## Basic usage

Three things are needed: a DSPy program, a metric function, and a training set.

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or any LiteLLM-supported provider

# 1. Define a program
classify = dspy.ChainOfThought("text -> label")

# 2. Define a metric
def exact_match(example, pred, trace=None):
    return pred.label.strip().lower() == example.label.strip().lower()

# 3. Prepare training data
trainset = [
    dspy.Example(text="Server is down again", label="urgent").with_inputs("text"),
    dspy.Example(text="Update my billing info", label="normal").with_inputs("text"),
    dspy.Example(text="Site is completely broken", label="urgent").with_inputs("text"),
    dspy.Example(text="How do I change my password?", label="normal").with_inputs("text"),
    # ... more labeled examples
]

# 4. Compile with InferRules
optimizer = dspy.InferRules(metric=exact_match, num_rules=10)
compiled = optimizer.compile(classify, trainset=trainset)

# 5. Use the compiled program -- instructions now contain discovered rules
result = compiled(text="Database connection pool exhausted")
print(result.label)
```

After compilation, inspect the rules that were injected:

```python
# View the enhanced instructions for each predictor
for name, predictor in compiled.named_predictors():
    print(f"Predictor: {name}")
    print(f"Instructions: {predictor.signature.instructions}")
    print()
```

## How InferRules extracts rules

The compilation process has five stages:

1. **Data splitting** -- Splits `trainset` 50/50 into training and validation sets (unless you provide `valset` separately)
2. **Bootstrap demonstrations** -- Runs the parent `BootstrapFewShot.compile()` to collect successful input-output demonstrations
3. **Rule induction** -- For each predictor, feeds the bootstrapped demonstrations into a `RulesInductionProgram` that generates natural-language rules describing the patterns
4. **Candidate generation** -- Repeats the rule induction `num_candidates` times with different samples to produce diverse rule sets
5. **Validation and selection** -- Scores each candidate program on the validation set using your metric and returns the highest-scoring one

The induced rules look like plain English statements, for example:

> "If the text mentions system failures, outages, or data loss, classify as urgent."
> "If the text is a routine account or billing question, classify as normal."

These rules are appended to the predictor's existing instructions, giving the LM explicit decision logic to follow.

## Constructor parameters

```python
dspy.InferRules(
    num_candidates=10,   # Number of candidate programs to evaluate
    num_rules=10,        # Number of rules to induce per predictor
    num_threads=None,     # Thread count for parallel evaluation
    teacher_settings=None,  # Config for the teacher model
    metric=...,          # Evaluation metric (required, via kwargs)
    max_errors=...,      # Max allowed errors during evaluation (optional, via kwargs)
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `num_candidates` | `int` | `10` | Number of candidate rule-enhanced programs to generate. More candidates increase the chance of finding better rules but cost more LM calls |
| `num_rules` | `int` | `10` | Number of rules to induce per predictor. More rules capture finer patterns but risk overfitting or exceeding context limits |
| `num_threads` | `int` | `None` | Number of threads for parallel evaluation. `None` uses the default |
| `teacher_settings` | `dict` | `None` | Configuration for the teacher model used during bootstrapping |
| `metric` | `Callable` | -- | Evaluation function `(example, prediction, trace) -> float`. Passed via kwargs |
| `max_errors` | `int` | -- | Maximum errors allowed before stopping evaluation. Passed via kwargs |

## The compile method

```python
compiled_program = optimizer.compile(
    student,              # Your DSPy program to optimize (required)
    trainset=trainset,    # Training examples (required)
    valset=None,          # Validation examples (optional -- auto-split if not provided)
)
```

If `valset` is not provided, `compile` automatically splits `trainset` 50/50 into training and validation sets. Providing your own `valset` gives you more control over evaluation.

## Interpretability benefits

InferRules stands apart from other optimizers because its output is human-readable:

| Optimizer | Output | Interpretable? |
|-----------|--------|----------------|
| `BootstrapFewShot` | Few-shot examples in the prompt | Somewhat -- you can read the examples |
| `MIPROv2` | Optimized instructions + few-shot | Partially -- instructions are readable but auto-generated |
| `BootstrapFinetune` | Updated model weights | No -- weights are opaque |
| **`InferRules`** | **Explicit natural-language rules** | **Yes -- you can read, audit, and edit the rules** |

This makes InferRules a good fit for:

- **Regulated industries** where you must explain how decisions are made
- **Debugging** -- read the rules to understand what the optimizer learned
- **Human-in-the-loop refinement** -- edit or remove rules that are wrong before deploying
- **Documentation** -- the rules serve as a specification of your system's behavior

## Tuning num_candidates and num_rules

**`num_candidates`** controls how many different rule sets are generated and compared:

| Value | Use case |
|-------|----------|
| 3-5 | Quick iteration, prototyping |
| 10 (default) | Good balance of quality and cost |
| 15-20 | High-stakes applications, when you need the best possible rules |

**`num_rules`** controls how many rules are induced per predictor:

| Value | Use case |
|-------|----------|
| 3-5 | Simple binary tasks (spam/not-spam) |
| 10 (default) | Multi-class tasks, moderate complexity |
| 15-20 | Tasks with many edge cases or subtle distinctions |

More rules is not always better. Too many rules can overwhelm the LM's context or introduce contradictions. Start with the defaults and adjust based on validation scores.

## Providing a separate validation set

For more control, provide your own validation set:

```python
optimizer = dspy.InferRules(metric=exact_match, num_rules=10, num_candidates=10)
compiled = optimizer.compile(
    classify,
    trainset=train_examples,
    valset=val_examples,
)
```

This is recommended when:

- Your dataset has a natural train/val split
- You want to ensure specific edge cases appear in validation
- You want a larger training set for rule induction (the 50/50 auto-split may leave too few training examples)

## Saving and loading compiled programs

```python
# Save the compiled program (includes the discovered rules in instructions)
compiled.save("compiled_with_rules.json")

# Load it later
from your_module import YourProgram
loaded = YourProgram()
loaded.load("compiled_with_rules.json")

# The loaded program has the same enhanced instructions
result = loaded(text="New input here")
```

## Verify and compare against baseline

Always measure whether InferRules actually helps — it sometimes matches or underperforms the unoptimized baseline on complex tasks.

```python
import dspy

evaluator = dspy.Evaluate(devset=testset, metric=exact_match, display_progress=True)

baseline_score = evaluator(classify)          # unoptimized program
optimized_score = evaluator(compiled)         # InferRules-compiled program

print(f"Baseline:  {baseline_score:.1%}")
print(f"InferRules: {optimized_score:.1%}")
print(f"Delta: {optimized_score - baseline_score:+.1%}")
```

If `optimized_score` is not meaningfully higher than `baseline_score`, fall back to `dspy.BootstrapFewShot` — it is simpler and often just as accurate. Also compare against plain `dspy.MIPROv2` if you have enough budget: MIPROv2 sometimes produces better raw accuracy even when interpretability is not the priority.

## Gotchas

1. **Claude skips inspecting the discovered rules.** After `optimizer.compile()`, always print the enhanced instructions with `predictor.signature.instructions`. InferRules can generate incorrect or contradictory rules. Read them, edit or remove bad ones before deploying.
2. **Claude sets `num_rules` too high.** More rules is not always better. Too many rules overwhelm the LM's context window or introduce contradictions. Start with 10 (the default) and only increase if validation scores improve. Reduce if you see contradictory behavior.
3. **Claude does not compare against BootstrapFewShot.** InferRules adds complexity. Research shows it sometimes matches or underperforms the baseline — a 2025 study found InferRules achieved the same 87% accuracy as the unoptimized prompt on a code generation task. Always compare against plain BootstrapFewShot; if few-shot examples alone match InferRules accuracy, use the simpler approach.
4. **Claude forgets that InferRules splits trainset 50/50 automatically.** If you have 40 examples and do not pass `valset`, InferRules uses only 20 for training — often too few for good rule induction. Pass `valset` explicitly to control the split.
5. **Claude uses InferRules for open-ended or creative tasks.** InferRules works best on tasks with consistent, describable patterns (classification, routing, triage). For creative writing or open-ended generation where there are no consistent rules to discover, it adds noise. Use BootstrapFewShot or MIPROv2 instead.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Bootstrapping few-shot examples** as the foundation -- see `/ai-improving-accuracy`
- **Full prompt optimization** with MIPROv2 -- see `/ai-improving-accuracy`
- **Evaluating your program** to measure rule quality -- see `/dspy-evaluate`
- **Data preparation** for training and validation sets -- see `/dspy-data`
- **Signatures and instructions** that InferRules modifies -- see `/dspy-signatures`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.InferRules API docs](https://dspy.ai/api/optimizers/InferRules/)
- [DSPy optimizer selection guide](https://dspy.ai/diving-deeper/choosing-an-optimizer/)
- For constructor signatures and method reference, see [reference.md](reference.md)
- For worked examples (ticket classification, content moderation), see [examples.md](examples.md)
