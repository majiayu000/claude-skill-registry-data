---
name: ai-reasoning
description: Make AI solve hard problems that need planning and multi-step thinking. Use when your AI fails on complex questions, needs to break down problems, requires multi-step logic, needs to plan before acting, gives wrong answers on math or analysis tasks, or when a simple prompt is not enough for the reasoning required. Covers ChainOfThought, ProgramOfThought, MultiChainComparison, and Self-Discovery reasoning patterns in DSPy., AI gives shallow answers, LLM does not think before answering, chain of thought prompting, make AI show its work, AI fails at math, complex analysis with LLM, multi-step problem solving, AI reasoning errors, LLM logic mistakes, think step by step DSPy, AI cannot do basic arithmetic, deep reasoning with language models, self-consistency for better answers, tree of thought.
---

# Build AI That Reasons Through Hard Problems

Guide the user through making AI solve problems that need more than a simple answer. When a task requires planning, multi-step logic, or choosing the right approach, basic prompting fails. DSPy gives you composable reasoning strategies.

## Step 1: Does the task need advanced reasoning?

Use this decision tree:

| Task type | Example | Best approach |
|-----------|---------|---------------|
| Simple lookup / classification | "Is this email spam?" | `dspy.Predict` |
| Needs explanation or logic | "Why did the build fail?" | `dspy.ChainOfThought` |
| Math, counting, computation | "What's the total after discounts?" | `dspy.ProgramOfThought` |
| Needs to compare approaches | "Which database is best for this?" | `dspy.MultiChainComparison` |
| Complex multi-step, novel problems | "Plan a migration strategy" | Self-Discovery pattern |

If the user isn't sure, **start with `ChainOfThought`** — it's the right default for most tasks.

## Step 2: Basic reasoning patterns

### ChainOfThought — think step by step

The workhorse. Adds intermediate reasoning before the final answer:

```python
import dspy

class AnalyzeBug(dspy.Signature):
    """Analyze the bug report and determine root cause."""
    bug_report: str = dspy.InputField(desc="The bug report with error details")
    root_cause: str = dspy.OutputField(desc="The most likely root cause")
    fix_suggestion: str = dspy.OutputField(desc="Suggested fix")

analyzer = dspy.ChainOfThought(AnalyzeBug)
result = analyzer(bug_report="Users see 500 errors after deploying v2.3...")
print(result.reasoning)  # shows step-by-step thinking
print(result.root_cause)
```

### ProgramOfThought — write code to compute the answer

When the answer requires calculation, let the AI write and execute code:

```python
class CalculateMetrics(dspy.Signature):
    """Calculate business metrics from the provided data."""
    data_description: str = dspy.InputField(desc="Description of the data and what to calculate")
    result: str = dspy.OutputField(desc="The calculated result")

calculator = dspy.ProgramOfThought(CalculateMetrics)
result = calculator(data_description="Revenue was $50k in Jan, $63k in Feb, $58k in March. What's the average monthly growth rate?")
```

`ProgramOfThought` generates Python code, runs it in a sandbox, and returns the output. Use this for anything involving math, dates, data manipulation, or counting.

### MultiChainComparison — generate multiple answers, pick the best

When quality matters more than speed, reason multiple ways and compare:

```python
class RecommendApproach(dspy.Signature):
    """Recommend the best technical approach for this problem."""
    problem: str = dspy.InputField()
    recommendation: str = dspy.OutputField()

recommender = dspy.MultiChainComparison(RecommendApproach)
result = recommender(problem="We need to add real-time notifications to our app")
# Internally generates multiple chains of thought, then picks the best
```

### When to use each

```python
class SmartReasoner(dspy.Module):
    """Route to the best reasoning strategy based on the task."""
    def __init__(self):
        self.classify = dspy.Predict("question -> task_type: str")
        self.cot = dspy.ChainOfThought("question -> answer")
        self.pot = dspy.ProgramOfThought("question -> answer")
        self.mcc = dspy.MultiChainComparison("question -> answer")

    def forward(self, question):
        task_type = self.classify(question=question).task_type.lower()

        if "math" in task_type or "calcul" in task_type or "count" in task_type:
            return self.pot(question=question)
        elif "compare" in task_type or "recommend" in task_type or "best" in task_type:
            return self.mcc(question=question)
        else:
            return self.cot(question=question)
```

## Step 3: Self-Discovery pattern

For genuinely hard problems where the AI needs to figure out *how* to think, not just think harder. Inspired by Self-Discover prompting research.

The 4-stage pipeline:

1. **Select** — pick relevant reasoning strategies from a library
2. **Adapt** — tailor those strategies to the specific task
3. **Plan** — create a structured reasoning plan
4. **Execute** — follow the plan to produce the answer

```python
from pydantic import BaseModel, Field

# Reasoning strategy library
REASONING_STRATEGIES = [
    "Break the problem into smaller sub-problems",
    "Think about edge cases and exceptions",
    "Work backwards from the desired outcome",
    "Consider analogies to simpler problems",
    "Identify constraints and requirements first",
    "Generate multiple hypotheses and evaluate each",
    "Think about what information is missing",
    "Check if the problem has been solved before in a different context",
    "Separate facts from assumptions",
    "Consider the problem from different stakeholder perspectives",
]

class SelectStrategies(dspy.Signature):
    """Select the most relevant reasoning strategies for this task."""
    task: str = dspy.InputField(desc="The problem to solve")
    available_strategies: list[str] = dspy.InputField()
    selected_strategies: list[str] = dspy.OutputField(
        desc="2-4 most relevant strategies for this task"
    )

class AdaptStrategies(dspy.Signature):
    """Adapt the selected strategies to this specific task."""
    task: str = dspy.InputField()
    strategies: list[str] = dspy.InputField(desc="Selected reasoning strategies")
    adapted_strategies: list[str] = dspy.OutputField(
        desc="Strategies rewritten for this specific problem"
    )

class ReasoningStep(BaseModel):
    step_number: int
    strategy: str = Field(description="Which reasoning strategy this step uses")
    description: str = Field(description="What to do in this step")

class CreatePlan(dspy.Signature):
    """Create a structured step-by-step reasoning plan."""
    task: str = dspy.InputField()
    adapted_strategies: list[str] = dspy.InputField()
    plan: list[ReasoningStep] = dspy.OutputField(desc="Ordered reasoning steps")

class ExecutePlan(dspy.Signature):
    """Execute the reasoning plan to solve the task."""
    task: str = dspy.InputField()
    plan: list[ReasoningStep] = dspy.InputField()
    step_results: list[str] = dspy.OutputField(desc="Result of each reasoning step")
    final_answer: str = dspy.OutputField(desc="The final answer based on all reasoning")

class SelfDiscoveryReasoner(dspy.Module):
    def __init__(self):
        self.select = dspy.ChainOfThought(SelectStrategies)
        self.adapt = dspy.ChainOfThought(AdaptStrategies)
        self.plan = dspy.ChainOfThought(CreatePlan)
        self.execute = dspy.ChainOfThought(ExecutePlan)

    def forward(self, task):
        # Stage 1: Select relevant strategies
        selected = self.select(
            task=task,
            available_strategies=REASONING_STRATEGIES,
        ).selected_strategies

        # Stage 2: Adapt to this task
        adapted = self.adapt(
            task=task,
            strategies=selected,
        ).adapted_strategies

        # Stage 3: Create reasoning plan
        plan = self.plan(
            task=task,
            adapted_strategies=adapted,
        ).plan

        # Stage 4: Execute the plan
        result = self.execute(task=task, plan=plan)

        return dspy.Prediction(
            strategies=selected,
            plan=plan,
            step_results=result.step_results,
            answer=result.final_answer,
        )
```

## Step 4: Structured reasoning plans

For complex tasks, force the AI to show its work in a structured format:

```python
class ReasoningTrace(BaseModel):
    step: str = Field(description="What this reasoning step does")
    observation: str = Field(description="What was observed or concluded")
    confidence: float = Field(description="0.0-1.0 confidence in this step")

class StructuredReasoner(dspy.Module):
    def __init__(self):
        self.reason = dspy.ChainOfThought(ReasonWithTrace)

    def forward(self, question):
        result = self.reason(question=question)

        return result

class ReasonWithTrace(dspy.Signature):
    """Solve the problem step by step, showing reasoning at each stage."""
    question: str = dspy.InputField()
    trace: list[ReasoningTrace] = dspy.OutputField(desc="Step-by-step reasoning trace")
    answer: str = dspy.OutputField(desc="Final answer based on the reasoning trace")
```

## Step 5: Evaluate reasoning quality

Don't just check the final answer — evaluate the reasoning process:

### Judge intermediate steps

```python
class JudgeReasoning(dspy.Signature):
    """Judge whether the reasoning process is sound."""
    question: str = dspy.InputField()
    reasoning_steps: list[str] = dspy.InputField(desc="The steps taken to reach the answer")
    answer: str = dspy.InputField()
    steps_are_logical: bool = dspy.OutputField(desc="Each step follows from the previous")
    no_logical_leaps: bool = dspy.OutputField(desc="No unjustified jumps in reasoning")
    answer_follows: bool = dspy.OutputField(desc="The answer follows from the reasoning")

def reasoning_quality_metric(example, prediction, trace=None):
    # Check final answer correctness
    correct = prediction.answer.strip().lower() == example.answer.strip().lower()

    # Also check reasoning quality
    judge = dspy.Predict(JudgeReasoning)
    quality = judge(
        question=example.question,
        reasoning_steps=prediction.step_results if hasattr(prediction, 'step_results') else [prediction.reasoning],
        answer=prediction.answer,
    )

    reasoning_score = (
        quality.steps_are_logical + quality.no_logical_leaps + quality.answer_follows
    ) / 3

    # Weight: 60% correct answer, 40% good reasoning
    return (0.6 * correct) + (0.4 * reasoning_score)
```

### Compare reasoning approaches

Test which reasoning strategy works best for your task:

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(devset=devset, metric=reasoning_quality_metric, num_threads=4)

# Test different approaches
cot = dspy.ChainOfThought("question -> answer")
pot = dspy.ProgramOfThought("question -> answer")
self_disc = SelfDiscoveryReasoner()

print("ChainOfThought:", evaluator(cot))
print("ProgramOfThought:", evaluator(pot))
print("SelfDiscovery:", evaluator(self_disc))
```

## Step 6: Optimize reasoning

### BootstrapFewShot per stage

For multi-stage reasoning (like Self-Discovery), optimize each stage. Typical improvement: 15-30% on reasoning quality metrics (e.g., a ChainOfThought module going from 62% to 81% on a multi-step QA task after 4 bootstrapped demos):

```python
optimizer = dspy.BootstrapFewShot(
    metric=reasoning_quality_metric,
    max_bootstrapped_demos=4,
)
optimized = optimizer.compile(SelfDiscoveryReasoner(), trainset=trainset)
```

### MIPROv2 for instruction tuning

Automatically discover better instructions for the reasoning prompts:

```python
optimizer = dspy.MIPROv2(metric=reasoning_quality_metric, auto="medium")
optimized = optimizer.compile(SelfDiscoveryReasoner(), trainset=trainset)
```

### GEPA for reflective analysis

GEPA analyzes traces of successful and failed attempts to generate better instructions:

```python
optimizer = dspy.GEPA(metric=reasoning_quality_metric)
optimized = optimizer.compile(SelfDiscoveryReasoner(), trainset=trainset)
```

## Key patterns

- **Default to ChainOfThought** — it's the right choice for most tasks that need reasoning
- **ProgramOfThought for computation** — let the AI write code for math, dates, counting
- **MultiChainComparison for high stakes** — generate multiple answers and pick the best
- **Self-Discovery for novel problems** — dynamically select how to think, not just what to think
- **Evaluate the reasoning, not just the answer** — good reasoning produces reliably correct answers
- **Structured traces** — JSON reasoning steps make debugging and optimization easier

### Other reasoning-capable modules

| Module | When to consider |
|--------|-----------------|
| `dspy.BestOfN` | Generate N completions, return the one scoring highest on a metric — simpler than MultiChainComparison when you have a good metric |
| `dspy.Refine` | Iteratively improve an answer using feedback — good for tasks where a first draft is easy but polish is hard |
| `dspy.RLM` | Reasoning Language Model — uses test-time compute scaling for verified reasoning (math proofs, code correctness) |
| `dspy.Parallel` | Run multiple modules concurrently — combine with reasoning modules to parallelize sub-problems |

## Gotchas

- **Adding a `reasoning` field to your signature when using ChainOfThought.** DSPy injects the reasoning field automatically. Adding your own creates a duplicate that confuses the LM and produces garbled output. Just define your task-specific input/output fields and let `dspy.ChainOfThought` handle the rest.
- **Using ProgramOfThought for everything involving numbers.** ProgramOfThought generates and executes Python code, which requires a sandbox and adds latency. For simple numeric comparisons or estimates that do not need exact computation, ChainOfThought is faster and sufficient. Reserve ProgramOfThought for actual arithmetic, date math, or data manipulation.
- **Forgetting that MultiChainComparison makes N separate LM calls.** Each chain is an independent call, so cost and latency scale linearly. For latency-sensitive paths, consider using a single ChainOfThought wrapped with `dspy.Refine` instead of MultiChainComparison with 3-5 chains.
- **Building a Self-Discovery pipeline without optimizing each stage separately.** When you call `BootstrapFewShot` on a multi-stage module, it optimizes end-to-end but the intermediate stages (select, adapt, plan) often get weak demos. Evaluate intermediate outputs during development to catch silent degradation in early stages.
- **Using string matching to route between reasoning strategies.** The `SmartReasoner` pattern with `if "math" in task_type` is brittle — LMs produce unpredictable classification labels. Use `dspy.Predict` with `Literal` types for routing, or better yet, let the optimizer discover which strategy works best via `dspy.Evaluate` comparisons.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **ChainOfThought** for the core reasoning module — see `/dspy-chain-of-thought`
- **ProgramOfThought** for code-generating computation — see `/dspy-program-of-thought`
- **MultiChainComparison** for multi-path reasoning — see `/dspy-multi-chain-comparison`
- **Signatures** for defining input/output contracts — see `/dspy-signatures`
- **Refine** for constraining reasoning quality with reward functions — see `/dspy-refine`
- **Simple calls without reasoning** — see `/dspy-predict`
- Need AI to call APIs and use tools? See `/ai-taking-actions`
- Need multi-step pipelines with predetermined stages? See `/ai-building-pipelines`
- Measure and improve your reasoning system — see `/ai-improving-accuracy`
- Not sure which skill to use? Try `/ai-do`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.ChainOfThought API docs](https://dspy.ai/api/modules/ChainOfThought/)
- [dspy.ProgramOfThought API docs](https://dspy.ai/api/modules/ProgramOfThought/)
- [dspy.MultiChainComparison API docs](https://dspy.ai/api/modules/MultiChainComparison/)
- For worked examples (complex questions, data analysis, planning), see [examples.md](examples.md)
- For condensed API reference, see [reference.md](reference.md)
