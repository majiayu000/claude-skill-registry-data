---
name: dspy-ragas
description: Use Ragas to evaluate DSPy RAG pipelines with decomposed metrics. Use when you want to evaluate RAG quality, measure faithfulness, context precision, context recall, response relevancy, or diagnose retriever vs generator issues. Also used for ragas, pip install ragas, ragas evaluate, RAG evaluation, faithfulness metric, context precision, context recall, answer relevancy, answer correctness, decomposed RAG metrics, ragas dspy, DSPyOptimizer ragas, ragas dspy extras, EvaluationDataset, ragas vs dspy.Evaluate, which RAG metric, retriever vs generator quality.
---

# Ragas — Decomposed RAG Evaluation for DSPy

Guide the user through evaluating DSPy RAG pipelines with Ragas, an evaluation framework that decomposes RAG quality into independent metrics for retriever and generator.

## Step 1: Understand the evaluation need

Before setting up Ragas, clarify:

1. **Do you have a RAG pipeline already?** Ragas evaluates retriever + generator quality — you need a working pipeline first.
2. **Do you have ground-truth answers?** Some metrics (Faithfulness, ResponseRelevancy) are reference-free; others (ContextPrecision, ContextRecall) need reference answers.
3. **What are you diagnosing?** If you just need an accuracy score, use `dspy.Evaluate`. Ragas shines when you need to know *whether the retriever or generator* is the weak link.

## What is Ragas

[Ragas](https://github.com/explodinggradients/ragas) is an open-source evaluation framework (12.9k+ GitHub stars, Apache 2.0) purpose-built for RAG pipelines. Instead of a single accuracy score, it breaks evaluation into decomposed metrics:

| Metric (ragas 0.4+ class) | What it measures | Needs ground truth? | Evaluates |
|--------------------------|-----------------|--------------------:|-----------|
| **Faithfulness** | Is the answer grounded in retrieved context? | No | Generator |
| **ResponseRelevancy** | Does the answer address the question? | No | Generator |
| **ContextPrecision** | Are relevant docs ranked higher? | Yes (reference) | Retriever |
| **ContextRecall** | Did retrieval find all relevant info? | Yes (reference) | Retriever |
| **FactualCorrectness** | Is the answer factually correct vs reference? | Yes (reference) | End-to-end |

This decomposition tells you *where* your RAG pipeline fails — retriever or generator — so you know what to fix.

## When to use Ragas vs dspy.Evaluate

| Use case | Tool |
|----------|------|
| **Diagnose retriever vs generator issues** | Ragas — decomposed metrics isolate the problem |
| **Measure overall pipeline accuracy** | `dspy.Evaluate` with SemanticF1 or exact match |
| **Optimization objective** (BootstrapFewShot, MIPROv2) | `dspy.Evaluate` — Ragas metrics are too slow for inner-loop optimization |
| **Evaluate before and after optimization** | Both — use `dspy.Evaluate` for the score that was optimized, Ragas for deeper analysis |
| **Reference-free evaluation** | Ragas Faithfulness + ResponseRelevancy — no ground truth needed |

**Best practice:** Use `dspy.Evaluate` with a fast metric (SemanticF1) as your optimization objective, then use Ragas for post-optimization analysis to understand *why* your pipeline performs the way it does.

## Setup

```bash
# Core Ragas (evaluation only)
pip install ragas

# With DSPy optimizer support (uses MIPROv2 internally)
pip install "ragas[dspy]"
```

Ragas requires an LLM for its metrics. By default it uses OpenAI (`OPENAI_API_KEY`), but you can configure any LLM via LangChain wrappers.

## Evaluating a DSPy RAG pipeline with Ragas

### Step 1: Collect predictions from your DSPy pipeline

Run your DSPy RAG pipeline on a set of questions and collect the inputs, retrieved contexts, and generated answers:

```python
import dspy

# Your DSPy RAG pipeline
class RAG(dspy.Module):
    def __init__(self, retriever):
        self.retrieve = retriever
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return dspy.Prediction(
            answer=self.generate(context=context, question=question).answer,
            context=context,
        )

# Collect predictions
results = []
for example in devset:
    pred = rag(question=example.question)
    results.append({
        "user_input": example.question,
        "response": pred.answer,
        "retrieved_contexts": pred.context,
        "reference": example.answer,  # ground truth, if available
    })
```

### Step 2: Build a Ragas EvaluationDataset

```python
from ragas import EvaluationDataset, SingleTurnSample

samples = [
    SingleTurnSample(
        user_input=r["user_input"],
        response=r["response"],
        retrieved_contexts=r["retrieved_contexts"],
        reference=r.get("reference"),  # optional for some metrics
    )
    for r in results
]
dataset = EvaluationDataset(samples=samples)
```

### Step 3: Run evaluation

```python
from ragas import evaluate
from ragas.metrics.collections import (
    Faithfulness,
    ResponseRelevancy,   # was AnswerRelevancy in ragas <0.4
    ContextPrecision,
    ContextRecall,
    FactualCorrectness,  # was AnswerCorrectness in ragas <0.4
)

# Pick metrics based on what you have
# Without ground truth: Faithfulness + ResponseRelevancy
# With ground truth: add ContextPrecision, ContextRecall, FactualCorrectness
result = evaluate(
    dataset=dataset,
    metrics=[
        Faithfulness(),
        ResponseRelevancy(),
        ContextPrecision(),
        ContextRecall(),
        FactualCorrectness(),
    ],
)

print(result)
# {'faithfulness': 0.87, 'response_relevancy': 0.92, 'context_precision': 0.75,
#  'context_recall': 0.68, 'factual_correctness': 0.81}
```

### Step 4: Interpret results

```
Faithfulness low (< 0.8)?
  → Generator is hallucinating beyond retrieved context
  → Fix: add assertions, use GroundedRAG pattern (/ai-stopping-hallucinations)

ContextPrecision low (< 0.7)?
  → Retriever returns relevant docs but ranks them poorly
  → Fix: tune k, try hybrid search, re-rank (/dspy-qdrant)

ContextRecall low (< 0.7)?
  → Retriever misses relevant documents entirely
  → Fix: improve chunking, add more docs, try different embeddings (/ai-searching-docs)

ResponseRelevancy low (< 0.8)?
  → Generator answers don't address the question
  → Fix: improve signatures, optimize with MIPROv2 (/dspy-miprov2)

FactualCorrectness low but Faithfulness high?
  → Generator is faithful to context but context is wrong
  → Focus on retriever improvements
```

## Using a custom LLM with Ragas

By default Ragas uses OpenAI (`OPENAI_API_KEY`). Ragas v0.4+ supports multiple LLM backends via Instructor or LiteLLM adapters:

```python
from ragas.llms import llm_factory
from openai import OpenAI  # or: from anthropic import Anthropic, etc.

client = OpenAI()  # reads OPENAI_API_KEY
evaluator_llm = llm_factory("gpt-4o-mini", client=client)
# or Anthropic: llm_factory("claude-sonnet-4-5-20250929", client=Anthropic())
# or LiteLLM:   llm_factory("bedrock/anthropic.claude-3-sonnet", provider="litellm", client=litellm.completion)

result = evaluate(
    dataset=dataset,
    metrics=[Faithfulness(), ResponseRelevancy()],
    llm=evaluator_llm,
)
```

**Note:** `LangchainLLMWrapper` is legacy. If you see old examples using it, switch to `llm_factory()` instead.

## Per-sample scores

Get scores for each sample to find problem areas:

```python
from ragas.metrics.collections import Faithfulness, ContextRecall
result = evaluate(dataset=dataset, metrics=[Faithfulness(), ContextRecall()])

# Convert to pandas DataFrame
df = result.to_pandas()
print(df[["user_input", "faithfulness", "context_recall"]])

# Find worst-performing samples
worst = df.nsmallest(5, "faithfulness")
for _, row in worst.iterrows():
    print(f"Q: {row['user_input']}")
    print(f"  Faithfulness: {row['faithfulness']:.2f}")
```

## DSPyOptimizer (advanced)

Ragas includes a `DSPyOptimizer` that uses MIPROv2 internally to optimize Ragas's own metric prompts. This can improve evaluation accuracy for domain-specific data.

```bash
pip install "ragas[dspy]"
```

```python
from ragas.metrics.collections import Faithfulness
from ragas.integrations.dspy import DSPyOptimizer

# Optimize the Faithfulness metric's internal prompts
metric = Faithfulness()
optimizer = DSPyOptimizer(metric=metric)

# Requires a labeled dataset where you know the correct faithfulness scores
optimized_metric = optimizer.optimize(dataset=labeled_eval_dataset)

# Use the optimized metric for more accurate evaluation
result = evaluate(dataset=dataset, metrics=[optimized_metric])
```

This is advanced — only needed if Ragas's default metrics don't align well with your domain's definition of faithfulness, relevancy, etc.

## Ragas in a DSPy development workflow

```
1. Build RAG pipeline          → /ai-searching-docs or /dspy-retrieval
2. Create devset               → /dspy-data
3. Evaluate with dspy.Evaluate → /dspy-evaluate (SemanticF1 as optimization target)
4. Optimize with MIPROv2       → /dspy-miprov2
5. Deep analysis with Ragas    → this skill (diagnose retriever vs generator)
6. Fix weak components         → /ai-stopping-hallucinations, /dspy-qdrant, /ai-improving-accuracy
7. Re-evaluate with both       → confirm improvements
```

## Gotchas

1. **Ragas metrics call an LLM** — each metric makes multiple LLM calls per sample. A 100-sample evaluation with 5 metrics = ~500 LLM calls. Budget for the cost.
2. **Don't use Ragas as an optimizer objective** — it's too slow for inner-loop optimization. Use DSPy's built-in metrics for `compile()`, then Ragas for analysis.
3. **ContextPrecision and ContextRecall need ground truth** — if you do not have reference answers, use Faithfulness + ResponseRelevancy (reference-free).
4. **Claude uses deprecated Ragas APIs from older tutorials.** Ragas 0.4 made three breaking changes: (1) metric imports moved from `ragas.metrics` to `ragas.metrics.collections` — `from ragas.metrics import Faithfulness` now triggers `DeprecationWarning` and will break in v1.0; always use `from ragas.metrics.collections import Faithfulness`; (2) metric class renames — `AnswerRelevancy` → `ResponseRelevancy`, `AnswerCorrectness` → `FactualCorrectness`; (3) `EvaluationDataset`/`SingleTurnSample` replaced the `datasets.Dataset` approach. If Claude generates code using `Dataset`, `LangchainLLMWrapper`, `ground_truths`, or `from ragas.metrics import MetricName`, it is using deprecated APIs.
5. **Claude installs `ragas` without checking the version.** Ragas v0.4+ has significant API changes from v0.2/v0.3. Pin the version in requirements (`ragas>=0.4`) to avoid mixing old and new APIs.

## Additional resources

- [Ragas quickstart — RAG evaluation](https://docs.ragas.io/en/stable/getstarted/rag_eval/)
- [Ragas available metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [Ragas custom LLM configuration](https://docs.ragas.io/en/stable/howtos/customizations/customize_models/)
- [Ragas GitHub](https://github.com/explodinggradients/ragas)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **DSPy's built-in evaluation** (SemanticF1, exact match, LM-as-judge) — `/dspy-evaluate`
- **Building RAG pipelines** — `/ai-searching-docs`
- **Retrieval modules and vector DBs** — `/dspy-retrieval`, `/dspy-qdrant`
- **Stopping hallucinations** (when Faithfulness is low) — `/ai-stopping-hallucinations`
- **Optimizing RAG accuracy** — `/ai-improving-accuracy`, `/dspy-miprov2`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
