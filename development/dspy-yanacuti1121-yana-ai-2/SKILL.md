---
name: dspy
description: Program LM pipelines with DSPy — define Signatures (input/output fields), build Modules (ChainOfThought, ReAct, Predict), compose them into Programs, then optimize with Teleprompters (BootstrapFewShot, MIPRO, COPRO) to auto-improve prompts from examples.
triggers:
  - "dspy"
  - "dspy signature"
  - "dspy module"
  - "dspy program"
  - "dspy teleprompter"
  - "dspy chain of thought"
  - "dspy react"
  - "dspy optimize prompts"
  - "dspy bootstrap"
  - "dspy mipro"
  - "dspy lm programming"
  - "dspy few shot"
  - "prompt optimization framework"
do_not_use_for:
  - Multi-agent crew orchestration — use crewai instead
  - Structured output with Pydantic — use pydantic-ai or instructor-structured-output
  - Fine-tuning — use llamafactory instead
see_also:
  - pydantic-ai
  - instructor-structured-output
  - langgraph
---

# DSPy — Programming LM Pipelines

**Source:** stanfordnlp/dspy (MIT) — a framework for algorithmically optimizing LM prompts and weights

## Core Idea

Instead of hand-crafting prompts, you:
1. **Define** what you want (Signatures: input → output)
2. **Build** modules that use LMs (ChainOfThought, ReAct, Predict)
3. **Compile** with an optimizer that auto-writes the best prompts using examples

## Install

```bash
pip install dspy
# optional: dspy[all] for all extras
```

## Configure LM

```python
import dspy

# Anthropic
lm = dspy.LM("anthropic/claude-sonnet-4-5", api_key="your-key")
dspy.configure(lm=lm)

# OpenAI
lm = dspy.LM("openai/gpt-4o")
dspy.configure(lm=lm)

# Local / Ollama
lm = dspy.LM("ollama/llama3", api_base="http://localhost:11434")
dspy.configure(lm=lm)
```

## Signatures

Signatures declare the LM's input/output contract using type annotations and docstrings.

```python
import dspy

# Inline string signature (quick)
classify = dspy.Predict("sentence -> sentiment: Literal['positive','negative','neutral']")

# Class-based signature (recommended for complex tasks)
class SentimentClassifier(dspy.Signature):
    """Classify the sentiment of a sentence."""
    sentence: str = dspy.InputField(desc="The input sentence to classify")
    sentiment: str = dspy.OutputField(desc="One of: positive, negative, neutral")
    confidence: float = dspy.OutputField(desc="Confidence score from 0 to 1")

predictor = dspy.Predict(SentimentClassifier)
result = predictor(sentence="I love DSPy!")
print(result.sentiment, result.confidence)
```

## Core Modules

```python
import dspy

# Predict — direct LM call
predict = dspy.Predict("question -> answer")
r = predict(question="What is 2+2?")

# ChainOfThought — adds reasoning step
cot = dspy.ChainOfThought("question -> answer")
r = cot(question="If Alice has 3 apples and Bob gives her 2, how many does she have?")
print(r.reasoning)  # shows step-by-step reasoning
print(r.answer)

# ChainOfThoughtWithHint
cot_hint = dspy.ChainOfThoughtWithHint("question -> answer")
r = cot_hint(question="What is 15 * 7?", hint="Think step by step")

# ProgramOfThought — generates and executes Python code
pot = dspy.ProgramOfThought("question -> answer")
r = pot(question="What is the 10th Fibonacci number?")

# ReAct — Reasoning + Acting with tools
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    return wikipedia_api.search(query)  # your implementation

react = dspy.ReAct("question -> answer", tools=[search_wikipedia])
r = react(question="Who invented the telephone?")
```

## Building Programs (Modules)

```python
import dspy

class RAGPipeline(dspy.Module):
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question: str) -> dspy.Prediction:
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

rag = RAGPipeline()
result = rag(question="What is quantum computing?")
print(result.answer)
```

## Multi-Hop Reasoning

```python
class MultiHopQA(dspy.Module):
    def __init__(self, num_hops=3):
        self.generate_query = dspy.ChainOfThought("context, question -> search_query")
        self.retrieve = dspy.Retrieve(k=3)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")
        self.num_hops = num_hops

    def forward(self, question: str) -> str:
        context = []
        for _ in range(self.num_hops):
            query = self.generate_query(context=context, question=question).search_query
            passages = self.retrieve(query).passages
            context.extend(passages)
        return self.generate_answer(context=context, question=question).answer
```

## Assertions (Self-Refinement)

```python
import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

class TweetWriter(dspy.Module):
    def __init__(self):
        self.draft = dspy.Predict("topic -> tweet")

    def forward(self, topic: str) -> str:
        tweet = self.draft(topic=topic).tweet
        dspy.Assert(
            len(tweet) <= 280,
            "Tweet must be ≤ 280 characters. Shorten it.",
        )
        dspy.Suggest(
            "#" in tweet,
            "Consider adding a hashtag for better reach.",
        )
        return tweet

writer = assert_transform_module(
    TweetWriter(),
    backtrack_handler,
)
result = writer(topic="AI safety")
```

## Optimization (Teleprompters)

```python
import dspy
from dspy.teleprompt import BootstrapFewShot, MIPROv2

# Define metric (returns True/False or 0–1 score)
def validate_answer(example, pred, trace=None) -> bool:
    return example.answer.lower() in pred.answer.lower()

# Training data
trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="Capital of France?", answer="Paris").with_inputs("question"),
    # ... more examples
]
devset = [...]  # validation set

# --- BootstrapFewShot (fast, good default) ---
teleprompter = BootstrapFewShot(
    metric=validate_answer,
    max_bootstrapped_demos=4,   # auto-generated few-shot examples
    max_labeled_demos=16,       # labeled examples from trainset
)
optimized_program = teleprompter.compile(
    RAGPipeline(),
    trainset=trainset,
)

# --- MIPROv2 (best quality, slower) ---
teleprompter = MIPROv2(
    metric=validate_answer,
    auto="medium",  # "light" | "medium" | "heavy"
    num_threads=4,
)
optimized_program = teleprompter.compile(
    RAGPipeline(),
    trainset=trainset,
    requires_permission_to_run=False,
)

# Save and load optimized program
optimized_program.save("optimized_rag.json")
loaded = RAGPipeline()
loaded.load("optimized_rag.json")
```

## Evaluation

```python
from dspy.evaluate import Evaluate

evaluate = Evaluate(
    devset=devset,
    num_threads=4,
    display_progress=True,
    display_table=5,
)

score = evaluate(optimized_program, metric=validate_answer)
print(f"Score: {score:.1f}%")
```

## Streaming

```python
import dspy

lm = dspy.LM("anthropic/claude-sonnet-4-5", cache=False)
dspy.configure(lm=lm)

predictor = dspy.Predict("question -> answer")

for chunk in dspy.streamify(predictor)(question="Explain quantum entanglement"):
    if isinstance(chunk, str):
        print(chunk, end="", flush=True)
```

## Anti-Fake-Pass Checks

- [ ] `dspy.configure(lm=lm)` must be called before any module runs
- [ ] `dspy.Example(...).with_inputs("field")` — `.with_inputs()` marks which fields are inputs
- [ ] `dspy.Retrieve` requires a retriever configured via `dspy.configure(rm=...)`
- [ ] `BootstrapFewShot` calls the LM during compilation — not free
- [ ] `optimized_program.save()` saves prompts + demos, not weights
- [ ] `dspy.Assert` retries if violated; `dspy.Suggest` is advisory only
- [ ] Result fields accessed as attributes: `result.answer`, not `result["answer"]`
