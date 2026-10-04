---
name: dspy-parallel
description: Use when you have independent LM calls that can run concurrently — batch processing, fan-out patterns, or speeding up pipelines with no data dependencies between steps. Common scenarios - processing a batch of inputs through a DSPy module concurrently, fan-out patterns where multiple independent LM calls run at once, speeding up evaluation by parallelizing predictions, or reducing wall-clock time for pipelines with no data dependencies. Related - ai-building-pipelines, ai-serving-apis. Also used for dspy.Parallel, concurrent LM calls, batch processing in DSPy, parallel DSPy execution, speed up DSPy pipeline, fan-out LM calls, concurrent predictions, parallelize evaluation, async DSPy calls, reduce latency with parallel execution, batch inference DSPy, process multiple inputs at once, throughput optimization, run DSPy modules concurrently, parallel map over inputs.
---

# Run LM Calls in Parallel with dspy.Parallel

Guide the user through using DSPy's `Parallel` module to execute multiple LM calls concurrently. `dspy.Parallel` is the built-in way to speed up batch processing and fan-out patterns without writing threading code yourself.

## What is dspy.Parallel

`dspy.Parallel` takes a list of (module, inputs) pairs and executes them concurrently using a thread pool. It handles threading, progress bars, error limits, and timeouts so you don't have to.

Use it when you have:

- **A batch of inputs** to run through the same module (classify 500 tickets, summarize 100 articles)
- **Multiple independent modules** to run on the same input (sentiment + topics + entities at once)
- **Any set of LM calls** that don't depend on each other

If call B depends on the result of call A, those two calls must be sequential. Everything else can be parallel.

## Step 1 — Clarify the use case

Before writing code, ask:

1. **Same module or mixed?** Are you running one module on many inputs (batch), or multiple different modules on the same input (fan-out)? Same-module batches can use either `dspy.Parallel` or the simpler `.batch()` method (see below). Fan-out requires `dspy.Parallel`.
2. **How many items?** Fewer than ~5 items — just call the module directly; parallelism overhead is not worth it. 5–100 items — `dspy.Parallel` with 4-8 threads. 100+ items — increase threads up to your provider rate limit.
3. **Any data dependencies?** If any call needs the output of a previous call, those must stay sequential. Confirm all pairs are truly independent before parallelizing.
4. **Error tolerance?** If any failure should abort the batch, use `max_errors`. If you want partial results, set `return_failed_examples=True`.

## Basic usage

Pass a list of `(module, inputs)` pairs. Each pair is one unit of work:

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or any LiteLLM-supported provider
dspy.configure(lm=lm)

# A module to run on every input
classify = dspy.Predict("text -> label: str")

# A batch of inputs
texts = [
    "I love this product!",
    "Terrible experience, want a refund.",
    "It's okay, nothing special.",
    "Best purchase I've made this year.",
]

# Build execution pairs: (module, inputs_dict)
exec_pairs = [(classify, {"text": t}) for t in texts]

# Run them all in parallel
parallel = dspy.Parallel(num_threads=4)
results = parallel(exec_pairs)

for text, result in zip(texts, results):
    print(f"{text[:30]:30s} -> {result.label}")
```

`results` is a list in the same order as `exec_pairs`, so `results[i]` corresponds to `exec_pairs[i]`.

## Constructor options

```python
dspy.Parallel(
    num_threads=4,               # number of concurrent threads (default: settings.num_threads)
    max_errors=5,                # stop after this many failures (default: settings.max_errors)
    return_failed_examples=False,# if True, return failures separately instead of raising
    provide_traceback=None,      # include tracebacks in error output (None = use settings default)
    disable_progress_bar=False,  # suppress the tqdm progress bar
    timeout=120,                 # max seconds per task before timeout
)
```

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `num_threads` | `int \| None` | `None` | Number of concurrent threads. Falls back to `dspy.settings.num_threads`. |
| `max_errors` | `int \| None` | `None` | Stop execution after this many errors. Falls back to `dspy.settings.max_errors`. |
| `access_examples` | `bool` | `True` | Unpack `Example` objects via `.inputs()`. Set `False` to pass raw Examples. |
| `return_failed_examples` | `bool` | `False` | When `True`, return failed examples separately instead of raising. |
| `provide_traceback` | `bool \| None` | `None` | Include Python tracebacks for failed examples. |
| `disable_progress_bar` | `bool` | `False` | Suppress the progress bar. |
| `timeout` | `int` | `120` | Max seconds per individual task. |
| `straggler_limit` | `int` | `3` | Threshold for flagging slow-running tasks. |

## `.batch()` — simpler alternative for same-module batching

Every `dspy.Module` has a built-in `.batch()` method that handles the most common case: running the same module on many inputs. If you do not need to mix different modules per item, `.batch()` is less code than `dspy.Parallel`:

```python
classify = dspy.Predict("text -> label: str")
texts = ["Great!", "Terrible.", "Meh."]

# Build a list of Examples
examples = [dspy.Example(text=t).with_inputs("text") for t in texts]

# Run in parallel -- same as dspy.Parallel under the hood
results = classify.batch(examples, num_threads=4)
for r in results:
    print(r.label)
```

`.batch()` accepts all the same concurrency parameters as `dspy.Parallel`:

```python
results = classify.batch(
    examples,
    num_threads=4,
    max_errors=5,
    return_failed_examples=True,
    provide_traceback=None,
    timeout=120,
)
# With return_failed_examples=True: returns (results, failed_examples, exceptions)
```

**When to use `.batch()` vs `dspy.Parallel`:**

| Need | Use |
|------|-----|
| Same module, many inputs | `.batch()` — simpler API |
| Different modules per input (fan-out) | `dspy.Parallel` — required |
| Mix modules and share an exec loop | `dspy.Parallel` — more control |

## Configuring concurrency

Start with a thread count that matches your rate limits, not your CPU cores. LM calls are I/O-bound (waiting on HTTP responses), so you can safely use many threads:

```python
# Conservative -- good starting point
parallel = dspy.Parallel(num_threads=4)

# Aggressive -- if your provider allows high concurrency
parallel = dspy.Parallel(num_threads=16)

# Match your provider's rate limit
# e.g., 60 requests/min = ~1/sec, so 4-8 threads keeps the pipeline full
parallel = dspy.Parallel(num_threads=8)
```

If you hit rate-limit errors (HTTP 429), reduce `num_threads` or add retry logic in your LM configuration.

## Input formats

`Parallel` accepts inputs as dictionaries, `dspy.Example` objects, or tuples:

```python
module = dspy.Predict("question -> answer")

# Dict inputs (most common)
pairs = [(module, {"question": "What is DSPy?"})]

# dspy.Example inputs
example = dspy.Example(question="What is DSPy?").with_inputs("question")
pairs = [(module, example)]

# Both work the same way
parallel = dspy.Parallel(num_threads=2)
results = parallel(pairs)
```

## Aggregating results

Results come back as a list. Aggregate however your application needs:

```python
import dspy

classify = dspy.Predict("text -> label: str, confidence: float")
texts = ["Great!", "Terrible.", "Meh.", "Amazing!", "Awful."]

parallel = dspy.Parallel(num_threads=4)
results = parallel([(classify, {"text": t}) for t in texts])

# Count labels
from collections import Counter
label_counts = Counter(r.label for r in results)
print(label_counts)  # Counter({'positive': 2, 'negative': 2, 'neutral': 1})

# Filter by confidence
high_confidence = [
    (text, r.label)
    for text, r in zip(texts, results)
    if r.confidence > 0.8
]

# Build a summary dict
output = [
    {"text": t, "label": r.label, "confidence": r.confidence}
    for t, r in zip(texts, results)
]
```

## Error handling

By default, `Parallel` raises an exception after `max_errors` failures. To handle errors gracefully, use `return_failed_examples=True`:

```python
parallel = dspy.Parallel(
    num_threads=4,
    max_errors=10,
    return_failed_examples=True,
    provide_traceback=True,
)

results, failed_examples, exceptions = parallel(exec_pairs)
```

When `return_failed_examples=True`, the return value is a 3-tuple:

- **`results`** -- list of successful predictions (same length as successes)
- **`failed_examples`** -- list of `(module, inputs)` pairs that failed
- **`exceptions`** -- list of exceptions corresponding to each failure

Handle failures after the batch completes:

```python
results, failed, errors = parallel(exec_pairs)

print(f"Succeeded: {len(results)}, Failed: {len(failed)}")

# Retry failures with a fallback module
if failed:
    fallback = dspy.ChainOfThought("text -> label: str")
    retry_pairs = [(fallback, inputs) for _, inputs in failed]
    retry_results = parallel(retry_pairs)
```

### Setting an error budget

Use `max_errors` to fail fast when too many calls are failing (e.g., provider outage):

```python
# Stop the whole batch if more than 5 calls fail
parallel = dspy.Parallel(num_threads=4, max_errors=5)

try:
    results = parallel(exec_pairs)
except Exception as e:
    print(f"Batch aborted: {e}")
```

### Timeouts

The `timeout` parameter sets a per-task time limit in seconds. Tasks that exceed this are terminated:

```python
# Give each task up to 60 seconds
parallel = dspy.Parallel(num_threads=4, timeout=60)
```

## Using different modules per item

Each pair can use a different module. This is useful for fan-out patterns where you run multiple analyses on the same input:

```python
import dspy

sentiment = dspy.Predict("text -> sentiment: str")
topics = dspy.Predict("text -> topics: list[str]")
summary = dspy.ChainOfThought("text -> summary: str")

text = "DSPy is a framework for programming language models..."

# Fan out: three different modules, same input
exec_pairs = [
    (sentiment, {"text": text}),
    (topics, {"text": text}),
    (summary, {"text": text}),
]

parallel = dspy.Parallel(num_threads=3)
results = parallel(exec_pairs)

combined = {
    "sentiment": results[0].sentiment,
    "topics": results[1].topics,
    "summary": results[2].summary,
}
```

## When to use Parallel vs a sequential loop

| Scenario | Use | Why |
|----------|-----|-----|
| Process 100+ items through the same module | `Parallel` | Massive speedup from concurrent HTTP requests |
| Run 3 independent analyses on one input | `Parallel` | All three calls happen at once |
| Pipeline where step 2 needs step 1's output | Sequential loop | There's a data dependency |
| Single LM call | Neither | No benefit from parallelism |
| Processing 2-3 items | Either works | Overhead is negligible either way |

### Sequential loop (before)

```python
# Slow: each call waits for the previous one to finish
results = []
for text in texts:
    result = classify(text=text)
    results.append(result)
```

### Parallel (after)

```python
# Fast: all calls run concurrently
parallel = dspy.Parallel(num_threads=8)
results = parallel([(classify, {"text": t}) for t in texts])
```

For a batch of 100 items with ~1 second per LM call:
- Sequential: ~100 seconds
- Parallel (8 threads): ~13 seconds

## Parallel inside a module

Wrap `Parallel` usage inside a `dspy.Module` for clean composition:

```python
class BatchClassifier(dspy.Module):
    def __init__(self, num_threads=4):
        self.classify = dspy.Predict("text -> label: str, confidence: float")
        self.num_threads = num_threads

    def forward(self, texts: list[str]):
        parallel = dspy.Parallel(num_threads=self.num_threads)
        exec_pairs = [(self.classify, {"text": t}) for t in texts]
        results = parallel(exec_pairs)

        return dspy.Prediction(
            labels=[r.label for r in results],
            confidences=[r.confidence for r in results],
        )

# Usage
classifier = BatchClassifier(num_threads=8)
result = classifier(texts=["Great!", "Terrible.", "Meh."])
print(result.labels)  # ["positive", "negative", "neutral"]
```

This keeps the parallelism as an implementation detail. Callers don't need to know about threading -- they just pass a list and get a list back.

## Gotchas

1. **Claude writes a `for` loop instead of using `dspy.Parallel`.** When asked to process a batch of inputs, Claude defaults to a sequential loop. For any batch of 5+ independent LM calls, use `dspy.Parallel` — it is dramatically faster because LM calls are I/O-bound.
2. **Claude sets `num_threads` to match CPU cores.** LM calls are network-bound (waiting on HTTP responses), not CPU-bound. Thread count should match your provider rate limit, not your CPU count. 8-16 threads is typical even on a 4-core machine.
3. **Claude forgets that `return_failed_examples=True` changes the return type.** Without it, `parallel(pairs)` returns a flat list. With it, it returns a 3-tuple `(results, failed_examples, exceptions)`. Destructure accordingly or the code will break.
4. **Claude nests Parallel inside Parallel without considering total concurrency.** An inner `Parallel(num_threads=3)` inside an outer `Parallel(num_threads=4)` creates up to 12 concurrent LM calls. This can exceed provider rate limits. Calculate the total: `outer_threads * inner_threads`.
5. **Claude uses `dspy.Parallel` for 1-2 items.** The threading overhead is not worth it for fewer than ~5 items. Just call the module directly.
6. **Skipping result order verification.** `dspy.Parallel` preserves input order — `results[i]` corresponds to `exec_pairs[i]`. Verify this with a quick sanity check: zip `results` with your original inputs and confirm the first few items align before processing the full batch.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Modules** are the building blocks you pass to Parallel -- see `/dspy-modules`
- **Batch classification** (sort items into categories at scale) -- see `/ai-sorting`
- **Multi-step pipelines** that combine sequential and parallel stages -- see `/ai-building-pipelines`
- **Async API serving** (non-blocking DSPy in FastAPI / asyncio) -- see `/ai-serving-apis`
- **Evaluation** uses its own threading via `num_threads` -- see `/dspy-evaluate`
- For worked examples (batch classification, multi-aspect analysis), see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.Parallel API docs](https://dspy.ai/api/modules/Parallel/)
- For constructor signatures and method reference, see [reference.md](reference.md)
- For worked examples (batch classification, multi-aspect analysis), see [examples.md](examples.md)
