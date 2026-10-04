---
name: dspy-modules
description: Build multi-step DSPy programs as composable, optimizable modules using dspy.Module and forward(). Use when composing Predict and ChainOfThought calls into a reusable pipeline, structuring a RAG pipeline as a class, creating nested DSPy modules, or designing a class-based multi-step program. Also used for dspy.Module, forward() method, custom DSPy module, compose DSPy calls, multi-step DSPy program, pipeline as a class, reusable AI components, nested DSPy modules, module design patterns, how to structure a DSPy program, class-based DSPy pipeline, self.predict in forward, modular AI pipeline, build complex DSPy programs, combine multiple DSPy calls into one module, save and load optimized module state.
---

# Build Composable AI Programs with dspy.Module

Guide the user through structuring DSPy programs as reusable, composable modules. A `dspy.Module` is the building block for all DSPy programs -- like PyTorch's `nn.Module` but for language model pipelines.

## Step 1 — Gather context

Ask before writing any code:

1. **What kind of pipeline?** (RAG, classify-then-route, iterative refinement, simple extraction?)
2. **How many sub-modules / steps?** (Single-step can skip the Module wrapper; 2+ steps benefit from it)
3. **Will you optimize this with a DSPy optimizer?** (If yes, sub-module layout as `self.` attributes is critical)
4. **Do you need async support?** (Requires `async def forward()` and `acall` — impacts design from the start)

Then build or explain the pattern that fits.

## What is dspy.Module

`dspy.Module` is the building block for multi-step DSPy programs. Declare sub-modules in `__init__` as `self.` attributes, wire them together with Python logic in `forward()`. DSPy optimizers automatically discover and tune all sub-modules in the tree.

## Composing modules -- nesting modules within modules

Modules are composable. A module can use other custom modules as sub-modules:

```python
class Summarizer(dspy.Module):
    def __init__(self):
        self.summarize = dspy.ChainOfThought("text -> summary")

    def forward(self, text):
        return self.summarize(text=text)


class AnalyzeAndSummarize(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict("text -> category")
        self.summarizer = Summarizer()  # nested custom module
        self.respond = dspy.ChainOfThought("category, summary -> response")

    def forward(self, text):
        category = self.classify(text=text).category
        summary = self.summarizer(text=text).summary
        return self.respond(category=category, summary=summary)
```

DSPy optimizers traverse the full module tree. When you optimize `AnalyzeAndSummarize`, the inner `Summarizer`'s prompts get optimized too.

## Printing module structure

Use `print()` to inspect all sub-modules and their signatures:

```python
pipeline = AnalyzeAndSummarize()
print(pipeline)
```

Output shows the module tree:

```
AnalyzeAndSummarize(
  classify = Predict(text -> category)
  summarizer = Summarizer(
    summarize = ChainOfThought(text -> summary)
  )
  respond = ChainOfThought(category, summary -> response)
)
```

This is useful for verifying your module hierarchy and debugging which sub-modules exist.

## Module state -- save and load

After optimization, save the learned state (few-shot demos, instructions) and reload it later:

```python
# Save after optimization
optimized_program = optimizer.compile(my_program, trainset=trainset)
optimized_program.save("my_program.json")

# Load into a fresh instance
loaded = MyProgram()
loaded.load("my_program.json")

# Use the loaded program -- it has the optimized prompts
result = loaded(question="What is DSPy?")
```

What gets saved:
- Few-shot demonstrations discovered by optimizers
- Optimized instructions (from MIPROv2, GEPA)
- Any state that DSPy's `Predict` modules track

What does **not** get saved:
- Python logic in `forward()` -- that's your code
- Model weights (unless you used `BootstrapFinetune`)
- The LM configuration -- you must call `dspy.configure()` before loading

## Validated outputs with Refine

Use `dspy.Refine` to enforce quality constraints on outputs through a reward function. This replaces the older `dspy.Assert`/`dspy.Suggest` pattern:

```python
class SafeQA(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.generate(question=question)


def answer_reward(args, pred):
    """Score answer quality. Returns float between 0.0 and 1.0."""
    score = 0.0

    # Hard requirement -- must provide a substantive answer
    if pred.answer.strip() and pred.answer != "I don't know":
        score += 0.6

    # Quality preference -- at least 10 words
    if len(pred.answer.split()) >= 10:
        score += 0.4

    return score


# Wrap with Refine to retry until quality threshold is met
validated_qa = dspy.Refine(
    module=SafeQA(),
    N=3,
    reward_fn=answer_reward,
    threshold=0.6,  # must at least pass the hard requirement
)
```

- **`dspy.Refine`** -- wraps a module, scores each attempt with a reward function, and retries until the threshold is met (up to N attempts). Use for requirements that must be met.
- **Graduated scores** -- return partial scores (0.0 to 1.0) to let Refine pick the best near-miss when no attempt fully succeeds.
- **`dspy.BestOfN`** -- similar to Refine but without cross-attempt feedback; use when attempts are independent.

For detailed Refine patterns and examples, see **`/dspy-refine`** and **`/dspy-best-of-n`**.

## Common patterns

### Conditional logic in forward()

Route to different sub-modules based on intermediate results:

```python
class ConditionalPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict("text -> category")
        self.simple_handler = dspy.Predict("text -> response")
        self.complex_handler = dspy.ChainOfThought("text -> response")

    def forward(self, text):
        category = self.classify(text=text).category

        if category in ("simple", "faq"):
            return self.simple_handler(text=text)
        else:
            return self.complex_handler(text=text)
```

### Loops in forward()

Process a list of items or iterate until a condition is met:

```python
class BatchProcessor(dspy.Module):
    def __init__(self):
        self.process_item = dspy.ChainOfThought("item -> result")

    def forward(self, items: list[str]):
        results = []
        for item in items:
            result = self.process_item(item=item)
            results.append(result.result)
        return dspy.Prediction(results=results)
```

### Iterative refinement

Keep improving until quality is sufficient:

```python
class Refiner(dspy.Module):
    def __init__(self, max_rounds=3):
        self.draft = dspy.ChainOfThought("task -> output")
        self.critique = dspy.ChainOfThought("task, output -> feedback, is_good: bool")
        self.revise = dspy.ChainOfThought("task, output, feedback -> output")
        self.max_rounds = max_rounds

    def forward(self, task):
        result = self.draft(task=task)

        for _ in range(self.max_rounds):
            check = self.critique(task=task, output=result.output)
            if check.is_good:
                break
            result = self.revise(
                task=task,
                output=result.output,
                feedback=check.feedback,
            )

        return result
```

### Error handling

Wrap sub-module calls to handle failures gracefully:

```python
class ResilientModule(dspy.Module):
    def __init__(self):
        self.primary = dspy.ChainOfThought("question -> answer")
        self.fallback = dspy.Predict("question -> answer")

    def forward(self, question):
        try:
            return self.primary(question=question)
        except Exception:
            return self.fallback(question=question)
```

### Returning custom predictions

Use `dspy.Prediction` to return structured results from `forward()`:

```python
class MultiOutput(dspy.Module):
    def __init__(self):
        self.analyze = dspy.ChainOfThought("text -> sentiment, topics: list[str]")
        self.summarize = dspy.ChainOfThought("text -> summary")

    def forward(self, text):
        analysis = self.analyze(text=text)
        summary = self.summarize(text=text)

        return dspy.Prediction(
            sentiment=analysis.sentiment,
            topics=analysis.topics,
            summary=summary.summary,
        )
```

### Setting different LMs per sub-module

Assign cheaper models to simpler steps:

```python
expensive_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
cheap_lm = dspy.LM("openai/gpt-4o-mini")  # or any smaller model

pipeline = MyProgram()
pipeline.classify.set_lm(cheap_lm)
pipeline.generate.set_lm(expensive_lm)
```

## Batch processing

Use `batch()` to process multiple examples in parallel:

```python
pipeline = MyProgram()
examples = [dspy.Example(question=q).with_inputs("question") for q in questions]
results = pipeline.batch(examples, num_threads=4, timeout=120)
```

## When NOT to use dspy.Module

Skip the class if you only need a single LM call and will never optimize or save it — call `dspy.Predict` or `dspy.ChainOfThought` directly:

```python
# Fine for one-off scripts and notebooks
predict = dspy.ChainOfThought("question -> answer")
result = predict(question="What is DSPy?")
```

Wrap in a Module when you need any of: re-use across the codebase, DSPy optimizer traversal, `save()`/`load()` state, `batch()` parallelism, or programmatic inspection via `named_predictors()`.

## Choosing a forward() pattern

| Pattern | Use when | Key property |
|---------|----------|-------------|
| Sequential steps | Each step's output feeds the next | Simplest; fully optimizable |
| Conditional routing | Different paths based on intermediate result | Cheap classifier directs to specialized handler |
| Loop / retry | Quality check drives iteration count | `max_rounds` param prevents infinite loops |
| `dspy.Refine` wrapper | Retry is boilerplate — just need a reward function | Delegates retry logic to DSPy |
| Nested modules | Reusable sub-pipeline across multiple parent modules | Optimizers traverse nested trees automatically |

## Verification

```python
# Check module tree before optimizing -- catch missing self. attributes early
print(pipeline)

# Confirm all Predict instances are discoverable
print(pipeline.named_predictors())   # should list every sub-module

# Smoke-test on one example before running batch
result = pipeline(**example.inputs())
assert hasattr(result, "answer"), "forward() must return a Prediction with expected fields"
```

## Gotchas

1. **Claude stores sub-modules in a plain list instead of as `self.` attributes.** Optimizers discover sub-modules by traversing `self.` attributes in `__init__`. A `Predict` stored in a local variable or a plain `list` is invisible to optimization. Use a `dict` assigned to `self.` — DSPy traverses dicts for parameters.
2. **Claude puts `dspy.configure()` inside `forward()`.** Configure once at startup. Calling it per-forward adds overhead and causes unexpected behavior during optimization.
3. **Claude names `forward()` args differently from training example fields.** When an optimizer traces your module, it passes inputs from training examples to `forward()`. Mismatched argument names cause silent failures. Use the same field names as your `dspy.Example` inputs.
4. **Claude creates a module with no `forward()` method.** Every `dspy.Module` subclass must implement `forward()`. Without it, calling the module raises an error.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Signatures** define inputs and outputs for each sub-module -- see `/dspy-signatures`
- **Predict** is the simplest sub-module for direct LM calls -- see `/dspy-predict`
- **ChainOfThought** adds step-by-step reasoning -- see `/dspy-chain-of-thought`
- **Multi-step pipelines** with real-world patterns -- see `/ai-building-pipelines`
- **Optimizing modules** to improve accuracy -- see `/ai-improving-accuracy`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.Module API docs](https://dspy.ai/api/modules/Module/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
