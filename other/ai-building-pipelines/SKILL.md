---
name: ai-building-pipelines
description: Chain multiple AI steps into one reliable pipeline. Use when your AI task is too complex for one prompt, you need to break AI logic into stages, combine classification then generation, do multi-step reasoning, build a compound AI system, orchestrate multiple models, or wire AI components together. Also used for LangChain LCEL alternative, how to chain LLM calls together, one prompt is not enough, multi-step AI workflow, AI pipeline that actually works in production, prompt chaining keeps breaking, DAG of LLM calls, extract then classify then generate, compound AI system design, how to combine multiple AI steps without spaghetti code.
---

# Build a Multi-Step AI Pipeline

Guide the user through breaking a complex AI task into multiple steps that feed into each other. One prompt can't do everything — compound AI systems dramatically outperform single calls by decomposing problems.

## Step 1: Understand the pipeline

Ask the user:
1. **What's the end-to-end task?** (e.g., "read a support ticket, classify it, draft a response")
2. **What are the natural stages?** (classification, retrieval, generation, verification?)
3. **Does any step need special tools?** (search, database, calculator?)
4. **Does data flow linearly, or do steps branch/loop?**

## Step 2: Design the stages

### The core pattern — compose DSPy modules

Every stage is a DSPy module. Wire them together in `forward()`:

```python
import dspy

class SupportPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.ChainOfThought(ClassifyTicket)
        self.retrieve = dspy.Retrieve(k=3)
        self.draft = dspy.ChainOfThought(DraftResponse)

    def forward(self, ticket):
        # Stage 1: Classify
        classification = self.classify(ticket=ticket)

        # Stage 2: Retrieve relevant docs
        docs = self.retrieve(classification.category + " " + ticket).passages

        # Stage 3: Draft response using classification + docs
        return self.draft(
            ticket=ticket,
            category=classification.category,
            context=docs,
        )
```

Each stage has its own signature:

```python
from typing import Literal

CATEGORIES = ["billing", "technical", "account", "general"]

class ClassifyTicket(dspy.Signature):
    """Classify the support ticket."""
    ticket: str = dspy.InputField()
    category: Literal[tuple(CATEGORIES)] = dspy.OutputField()

class DraftResponse(dspy.Signature):
    """Draft a helpful response to the support ticket."""
    ticket: str = dspy.InputField()
    category: str = dspy.InputField()
    context: list[str] = dspy.InputField(desc="Relevant help articles")
    response: str = dspy.OutputField(desc="Professional support response")
```

## Step 3: Common pipeline patterns

### Classify → Route → Specialize

Different categories get different handling:

```python
class RoutedPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.ChainOfThought(ClassifyInput)
        self.handlers = {
            "simple": dspy.Predict(SimpleAnswer),
            "complex": dspy.ChainOfThought(DetailedAnswer),
            "research": dspy.ChainOfThought(ResearchAnswer),
        }

    def forward(self, question):
        category = self.classify(question=question).category
        handler = self.handlers.get(category, self.handlers["simple"])
        return handler(question=question)
```

### Generate → Verify → Refine

Generate a first draft, check it, then improve:

```python
class GenerateAndRefine(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(GenerateDraft)
        self.verify = dspy.ChainOfThought(CheckQuality)
        self.refine = dspy.ChainOfThought(ImproveDraft)

    def forward(self, task):
        # Stage 1: Generate
        draft = self.generate(task=task)

        # Stage 2: Verify
        check = self.verify(task=task, draft=draft.output)

        # Stage 3: Refine if needed
        if not check.is_good:
            refined = self.refine(
                task=task,
                draft=draft.output,
                feedback=check.feedback,
            )
            return refined

        return draft
```

### Ensemble — ask multiple times, pick the best

Generate several candidates and select the best one (the pattern behind AlphaCode and Medprompt):

```python
class EnsemblePipeline(dspy.Module):
    def __init__(self, num_candidates=5):
        self.generators = [dspy.ChainOfThought(GenerateAnswer) for _ in range(num_candidates)]
        self.judge = dspy.ChainOfThought(PickBestAnswer)

    def forward(self, question):
        # Stage 1: Generate multiple candidates
        candidates = []
        for gen in self.generators:
            result = gen(question=question)
            candidates.append(result.answer)

        # Stage 2: Pick the best
        return self.judge(
            question=question,
            candidates=candidates,
        )

class PickBestAnswer(dspy.Signature):
    """Pick the best answer from the candidates."""
    question: str = dspy.InputField()
    candidates: list[str] = dspy.InputField(desc="Multiple answer candidates")
    best_answer: str = dspy.OutputField(desc="The most accurate and complete answer")
    reasoning: str = dspy.OutputField(desc="Why this answer was chosen")
```

### Parallel fan-out → merge

Process different aspects independently, then combine:

```python
class ParallelAnalysis(dspy.Module):
    def __init__(self):
        self.sentiment = dspy.ChainOfThought(AnalyzeSentiment)
        self.topics = dspy.ChainOfThought(ExtractTopics)
        self.entities = dspy.ChainOfThought(ExtractEntities)
        self.summarize = dspy.ChainOfThought(CombineAnalysis)

    def forward(self, text):
        # Fan out — run in parallel (DSPy can parallelize these)
        sent = self.sentiment(text=text)
        topics = self.topics(text=text)
        entities = self.entities(text=text)

        # Merge results
        return self.summarize(
            text=text,
            sentiment=sent.sentiment,
            topics=topics.topics,
            entities=entities.entities,
        )
```

### Loop — iterative refinement

Keep improving until a condition is met:

```python
class IterativeRefiner(dspy.Module):
    def __init__(self, max_iterations=3):
        self.generate = dspy.ChainOfThought(GenerateDraft)
        self.evaluate = dspy.ChainOfThought(EvaluateDraft)
        self.improve = dspy.ChainOfThought(ImproveDraft)
        self.max_iterations = max_iterations

    def forward(self, task):
        draft = self.generate(task=task)

        for i in range(self.max_iterations):
            evaluation = self.evaluate(task=task, draft=draft.output)
            if evaluation.score >= 0.9:
                break
            draft = self.improve(
                task=task,
                draft=draft.output,
                feedback=evaluation.feedback,
            )

        return draft
```

## Step 4: Use different models per stage

Not every stage needs the same model. Use cheap models for simple steps:

```python
expensive_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
cheap_lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc.

pipeline = SupportPipeline()

# Cheap model for classification (simple task)
pipeline.classify.lm = cheap_lm

# Expensive model for drafting (needs quality)
pipeline.draft.lm = expensive_lm
```

See `/ai-cutting-costs` for more cost optimization strategies.

## Step 5: Test and optimize the full pipeline

The beauty of DSPy pipelines: you optimize the whole thing end-to-end, not each step separately.

```python
def pipeline_metric(example, prediction, trace=None):
    # Score the final output quality
    return prediction.response.lower().strip() == example.response.lower().strip()

# Optimizes prompts for ALL stages together
optimizer = dspy.MIPROv2(metric=pipeline_metric, auto="medium")
optimized = optimizer.compile(pipeline, trainset=trainset)
```

## Key patterns

- **Decompose the problem** — if a task has distinct phases (understand, retrieve, generate, verify), make each one a module
- **Each stage gets its own signature** — clear inputs and outputs make the pipeline debuggable
- **Wire in `forward()`** — the `forward` method is your orchestration logic
- **Optimize end-to-end** — DSPy optimizers tune all stages together to maximize the final metric
- **Debug stage by stage** — use `dspy.inspect_history()` to see what each step did
- **Assign models per stage** — cheap models for simple tasks, expensive for complex ones

## When to use LangGraph instead

DSPy pipelines are great for stateless, linear-ish flows. But some problems need more:

| If your pipeline... | Use |
|---------------------|-----|
| Steps run in a fixed order | DSPy pipeline (this skill) |
| Steps branch based on results | DSPy pipeline with `if/else` in `forward()` |
| Needs cycles (retry loops, agent loops) | **LangGraph** `StateGraph` with DSPy modules as nodes |
| Needs persistent state across calls | **LangGraph** with checkpointing |
| Needs human approval mid-pipeline | **LangGraph** `interrupt_before` |
| Coordinates multiple independent agents | **LangGraph** supervisor pattern |

### Quick example: DSPy module as a LangGraph node

```python
import dspy
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class PipelineState(TypedDict):
    input_text: str
    category: str
    output: str

# DSPy modules
classifier = dspy.ChainOfThought("text -> category")
generator = dspy.ChainOfThought("text, category -> output")

# Wrap as LangGraph nodes
def classify_node(state: PipelineState) -> dict:
    result = classifier(text=state["input_text"])
    return {"category": result.category}

def generate_node(state: PipelineState) -> dict:
    result = generator(text=state["input_text"], category=state["category"])
    return {"output": result.output}

# Build graph
graph = StateGraph(PipelineState)
graph.add_node("classify", classify_node)
graph.add_node("generate", generate_node)
graph.add_edge(START, "classify")
graph.add_edge("classify", "generate")
graph.add_edge("generate", END)
app = graph.compile()
```

This gives you LangGraph's state management and routing with DSPy's optimizable prompts. For more, see `/ai-building-chatbots` (stateful conversations) and `/ai-coordinating-agents` (multi-agent systems).

## Gotchas

- **Optimize the full pipeline, not individual modules** — optimizing modules in isolation then composing them gives worse results than optimizing the whole pipeline end-to-end with `dspy.BootstrapFewShot` or `dspy.MIPROv2`. A single `MIPROv2(auto="medium")` call on the full pipeline typically improves accuracy 15-25% over unoptimized baselines.
- **Error propagation is silent** — if an early module returns garbage, later modules process it without complaint. Use `dspy.Refine` around key stages to catch bad intermediate outputs with a reward function.
- **Do not overuse ChainOfThought** — not every module in a pipeline needs reasoning. Use `dspy.Predict` for simple steps (extraction, formatting) and reserve `ChainOfThought` for steps that actually benefit from reasoning. Unnecessary reasoning adds latency and cost.
- **Pipeline order affects optimization** — DSPy optimizers trace through your `forward()` method. If module A's output feeds module B, the optimizer sees this dependency. Reordering modules or adding conditional logic changes what the optimizer can learn.
- **Test intermediate outputs, not just final output** — add metrics that check each stage's output independently. A pipeline can produce correct final output for wrong reasons, which breaks when inputs change.

## Additional resources

- For worked examples (minimal pipeline, routing, Refine, production content moderation), see [examples.md](examples.md)
- For DSPy API quick-reference (Module, Predict, ChainOfThought, Refine, BestOfN, MIPROv2, save/load), see [reference.md](reference.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Verification between stages** — see `/ai-checking-outputs`
- **Assign different models per stage** — see `/ai-cutting-costs`
- **Identify where to split your task** — see `/ai-decomposing-tasks`
- **Content generation pipelines** — see `/ai-writing-content`
- **Complex reasoning patterns** — see `/ai-reasoning`
- **Measure and improve pipeline accuracy** — see `/ai-improving-accuracy`
- **Composing DSPy modules** — see `/dspy-modules`
- **Iterative refinement with feedback** — see `/dspy-refine`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
