---
name: ai-choosing-architecture
description: Pick the right DSPy module and architecture for your AI feature. Use when you are not sure whether to use Predict, ChainOfThought, ReAct, or a pipeline, need to choose between DSPy patterns, want architecture advice for your AI feature, or are deciding between a single module and a multi-step pipeline. Also use for which DSPy module should I use, Predict vs ChainOfThought, when to use ReAct, single module vs pipeline, DSPy architecture decision, CoT vs PoT vs ReAct, do I need a pipeline, module selection guide, DSPy pattern selection, how to structure my DSPy program.
---

# Choose the Right DSPy Architecture

## When NOT to use this skill

- Already know what module to use — go to the matching `/dspy-*` skill
- Fixing errors in existing code — use `/ai-fixing-errors`
- Learning a specific module — use the matching `/dspy-*` skill
- Need a project plan, not an architecture decision — use `/ai-planning`

---

## Step 1: Answer 3 questions

Before recommending anything, get answers to these three questions from the user (or infer them from context):

1. **What goes in and what comes out?** Input type and format, output type and format.
2. **Does the AI need external tools?** Search, APIs, databases, calculators, code execution?
3. **How complex is the reasoning?** Simple mapping, moderate analysis, complex multi-step logic?

---

## Step 2: Pick the module

Walk the decision tree:

```
Does it need tools?
├── Yes: Does it need to write and run code?
│   ├── Yes → CodeAct
│   └── No → ReAct
└── No: How complex is the reasoning?
    ├── Simple (direct mapping) → Predict
    ├── Moderate (needs explanation) → ChainOfThought
    ├── Complex (math/computation) → ProgramOfThought
    └── Very complex (compare approaches) → MultiChainComparison
```

**Module tradeoff summary:**

| Module | Accuracy | Latency | Cost | Best for |
|---|---|---|---|---|
| Predict | Baseline | 1x | 1x | Simple classification, extraction, formatting |
| ChainOfThought | +10-30% | 1.5-2x | 1.5-2x | Most tasks — default choice when unsure |
| ProgramOfThought | +20-40% on math | 2-3x | 2-3x | Math, computation, data manipulation |
| ReAct | Varies | 3-10x | 3-10x | Tasks requiring external information or actions |
| CodeAct | Varies | 3-10x | 3-10x | Tasks requiring code generation and execution |
| MultiChainComparison | +5-15% | 3-5x | 3-5x | When you need the best possible single answer |
| BestOfN | +5-10% | Nx | Nx | When you have a reward function and acceptance threshold |

For the full module list including Refine, RLM, and Parallel, see [reference.md](reference.md).

---

## Step 3: Single module vs pipeline

Use this table to decide whether one module is enough or a pipeline is warranted:

| Signal | Single module | Pipeline |
|---|---|---|
| Input maps directly to output | Yes | -- |
| Task has distinct phases (classify then generate) | -- | Yes |
| Different parts need different LM capabilities | -- | Yes |
| Need to validate intermediate results | -- | Yes |
| Simple input-output with clear signature | Yes | -- |
| Need to combine retrieval + generation | -- | Yes |

**Rule of thumb:** start with a single module. Add pipeline stages only when you have measured a quality gap that a single module cannot close.

**Verification:** After implementing the chosen architecture, run `dspy.Evaluate(devset, metric=your_metric)` on 20-50 examples to confirm the module choice was correct before optimizing.

---

## Step 4: Architecture-to-optimizer pairing

| Architecture | First optimizer | Best optimizer | Why |
|---|---|---|---|
| Single Predict | BootstrapFewShot | MIPROv2 | Simple, fast to optimize |
| Single ChainOfThought | BootstrapFewShot | MIPROv2 | Reasoning benefits from good demos |
| ReAct agent | BootstrapFewShot | BootstrapFewShot | Agents are hard to optimize, start simple |
| Multi-module pipeline | BootstrapFewShot | MIPROv2 | End-to-end optimization tunes all stages |
| Pipeline with fine-tuning | BootstrapFinetune | BetterTogether | Weight tuning for max quality |

---

## Step 5: Generate the recommendation

Output the recommendation in this format:

```
## Architecture Recommendation

**Module:** dspy.ChainOfThought (or whatever was chosen)
**Why:** [1-2 sentences tying the module to the task]
**Skeleton:**
[minimal code showing the module or pipeline structure]

**Optimizer path:**
1. Start with BootstrapFewShot (quick baseline)
2. Move to MIPROv2 if accuracy needs to improve

**Alternative considered:** [what else was considered and why it was not chosen]
```

---

## Skeleton code templates

### 1. Single Predict (simplest)

```python
import dspy

class MyTask(dspy.Signature):
    """One sentence describing the task."""
    input_text: str = dspy.InputField()
    output_label: str = dspy.OutputField()

predictor = dspy.Predict(MyTask)
result = predictor(input_text="...")
print(result.output_label)
```

### 2. Single ChainOfThought (default choice)

```python
import dspy

class MyTask(dspy.Signature):
    """One sentence describing the task."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

cot = dspy.ChainOfThought(MyTask)
result = cot(question="...")
print(result.answer)
```

### 3. ReAct with tools

```python
import dspy

def search(query: str) -> str:
    """Search external knowledge base."""
    ...

def lookup(term: str) -> str:
    """Look up a term in a database."""
    ...

class MyAgentTask(dspy.Signature):
    """Answer questions using search and lookup tools."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

agent = dspy.ReAct(MyAgentTask, tools=[search, lookup])
result = agent(question="...")
print(result.answer)
```

### 4. Two-stage pipeline (classify then generate)

```python
import dspy

class Classify(dspy.Signature):
    """Classify the input into a category."""
    text: str = dspy.InputField()
    category: str = dspy.OutputField()

class Generate(dspy.Signature):
    """Generate a response given the category and original text."""
    text: str = dspy.InputField()
    category: str = dspy.InputField()
    response: str = dspy.OutputField()

class ClassifyThenGenerate(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(Classify)
        self.generate = dspy.ChainOfThought(Generate)

    def forward(self, text: str) -> dspy.Prediction:
        category = self.classify(text=text).category
        response = self.generate(text=text, category=category).response
        return dspy.Prediction(category=category, response=response)
```

### 5. Three-stage RAG pipeline (retrieve, reason, generate)

```python
import dspy

retriever = dspy.Retrieve(k=3)

class Reason(dspy.Signature):
    """Given context passages, identify the key facts relevant to the question."""
    question: str = dspy.InputField()
    context: list[str] = dspy.InputField()
    key_facts: str = dspy.OutputField()

class Answer(dspy.Signature):
    """Answer the question using the identified key facts."""
    question: str = dspy.InputField()
    key_facts: str = dspy.InputField()
    answer: str = dspy.OutputField()

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = retriever
        self.reason = dspy.ChainOfThought(Reason)
        self.answer = dspy.ChainOfThought(Answer)

    def forward(self, question: str) -> dspy.Prediction:
        passages = self.retrieve(question).passages
        key_facts = self.reason(question=question, context=passages).key_facts
        answer = self.answer(question=question, key_facts=key_facts).answer
        return dspy.Prediction(answer=answer, passages=passages)
```

---

## Gotchas

1. **Defaulting to ChainOfThought for everything.** Predict is better for simple classification or extraction where reasoning adds noise, not signal. If the correct output is a fixed label from a known set, CoT can hallucinate reasoning that leads it astray.

2. **Using ReAct when a pipeline suffices.** ReAct is for tasks that need dynamic tool selection at runtime. If you know the steps upfront (e.g., always retrieve then answer), use a pipeline — it is cheaper, faster, and easier to optimize.

3. **Over-engineering with MultiChainComparison.** MCC runs 3-5x the cost of a single pass. Only reach for it after measuring that single-pass accuracy is insufficient for your use case.

4. **Building a pipeline before proving a single module works.** Always start with the simplest module that could work. Measure it on your eval set. Add pipeline stages only when you have a specific, measured quality gap.

5. **Ignoring cost implications early.** A ReAct agent with 10 tool calls costs roughly 10x a single Predict call. Factor cost and latency into architecture decisions before you build, not after.

---

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- For full module comparison tables and complete code templates, see [reference.md](reference.md)
- For worked architecture decisions with real examples, see [examples.md](examples.md)
- Ready to build? Use the matching `/dspy-*` skill for your chosen module
- Need to implement a pipeline? Use `/ai-building-pipelines`
- Want to plan the full project? Use `/ai-planning`
- Need to review existing code? Use `/ai-auditing-code`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
