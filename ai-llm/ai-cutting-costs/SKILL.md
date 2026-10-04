---
name: ai-cutting-costs
description: Reduce your AI API bill. Use when AI costs are too high, API calls are too expensive, you want to use cheaper models, optimize token usage, reduce LLM spending, route easy questions to cheap models, or make your AI feature more cost-effective. Also used for GPT-4 costs too much for production, AI bill keeps growing, how to reduce OpenAI costs, optimize LLM token usage, smart model routing saves money, prompt is too long and expensive, cheaper than GPT-4 with same quality.
---

# Cut Your AI Costs

Guide the user through reducing AI API costs without sacrificing quality. Multiple strategies, from quick wins to advanced techniques.

## Step 1: Understand where the money goes

Ask the user:
1. **Which provider/model are you using?** (GPT-4o, Claude, etc.)
2. **How many API calls per day/month?**
3. **Is there a specific module or step that's most expensive?**

### Quick cost audit

```python
import dspy

# Run your program and check token usage
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

result = my_program(question="test")
dspy.inspect_history(n=3)  # Shows token counts per call
```

## Step 2: Quick wins

### Use a cheaper model everywhere

The simplest fix — switch to a cheaper model and see if quality holds:

```python
# Instead of GPT-4o (~$5/M input tokens)
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc. — ~$0.15/M input tokens

# Or use an open-source model
lm = dspy.LM("together_ai/meta-llama/Llama-3-70b-chat-hf")  # or any provider DSPy supports
```

Always measure quality before and after with `/ai-improving-accuracy`. When you switch models, re-optimize your prompts — they don't transfer. See `/ai-switching-models` for the full workflow.

### Enable caching

DSPy caches LM calls by default. Make sure you're not disabling it:

```python
# Caching is ON by default — same inputs won't re-call the API
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc. — cached automatically

# To verify caching is working, run the same input twice
# and check that the second call is instant
```

## Step 3: Use different models for different tasks

Not every step in your pipeline needs the expensive model. Use `dspy.context` or `set_lm` to assign cheaper models to simpler steps:

```python
expensive_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
cheap_lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc.

dspy.configure(lm=expensive_lm)  # default

class MyPipeline(dspy.Module):
    def __init__(self):
        self.classify = dspy.ChainOfThought(ClassifySignature)
        self.generate = dspy.ChainOfThought(GenerateSignature)

    def forward(self, text):
        # Use cheap model for simple classification
        with dspy.context(lm=cheap_lm):
            category = self.classify(text=text)

        # Use expensive model only for complex generation
        return self.generate(text=text, category=category.label)
```

### Per-module LM assignment

```python
# Set LM on specific modules permanently
my_program.classify.set_lm(cheap_lm)
my_program.generate.set_lm(expensive_lm)
```

## Step 4: Smart routing — cheap model for easy inputs, expensive for hard ones

Instead of sending everything to the expensive model, classify inputs by difficulty and route accordingly. This is the pattern behind FrugalGPT (up to 90% cost savings matching GPT-4 quality):

### Route by complexity

```python
from typing import Literal

class ComplexityRouter(dspy.Module):
    def __init__(self):
        self.assess = dspy.Predict(AssessComplexity)
        self.simple_handler = dspy.Predict(AnswerQuestion)
        self.complex_handler = dspy.ChainOfThought(AnswerQuestion)

    def forward(self, question):
        # Use the cheap model to decide complexity
        with dspy.context(lm=cheap_lm):
            assessment = self.assess(question=question)

        # Route to the right model
        if assessment.complexity == "simple":
            with dspy.context(lm=cheap_lm):
                return self.simple_handler(question=question)
        else:
            with dspy.context(lm=expensive_lm):
                return self.complex_handler(question=question)

class AssessComplexity(dspy.Signature):
    """Assess if this question needs a powerful model or a simple one can handle it."""
    question: str = dspy.InputField()
    complexity: Literal["simple", "complex"] = dspy.OutputField(
        desc="simple = factual/straightforward, complex = reasoning/nuanced"
    )
```

### Cascading — try cheap first, fall back to expensive

```python
class CascadingPipeline(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought(AnswerQuestion)
        self.verify = dspy.Predict(CheckConfidence)

    def forward(self, question):
        # Try cheap model first
        with dspy.context(lm=cheap_lm):
            result = self.answer(question=question)
            check = self.verify(question=question, answer=result.answer)

        # If cheap model isn't confident, escalate to expensive
        if not check.is_confident:
            with dspy.context(lm=expensive_lm):
                result = self.answer(question=question)

        return result

class CheckConfidence(dspy.Signature):
    """Is this answer confident and complete, or should we escalate to a better model?"""
    question: str = dspy.InputField()
    answer: str = dspy.InputField()
    is_confident: bool = dspy.OutputField()
```

**Typical savings:** 50-90% cost reduction. Most real-world traffic is simple questions that a cheap model handles fine.

## Step 5: Reduce prompt length

Long prompts = more tokens = more cost.

### Reduce few-shot examples

```python
# Fewer demos = shorter prompts = lower cost
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=2,   # down from 4
    max_labeled_demos=2,        # down from 4
)
```

### Reduce retrieved passages

```python
# Fewer passages = shorter context
class DocSearch(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=2)  # down from 5
        self.answer = dspy.ChainOfThought(AnswerSignature)
```

### Simplify signatures

```python
# Verbose — costs more tokens
class Verbose(dspy.Signature):
    """Given the following text, carefully analyze the content and provide a detailed classification."""
    text: str = dspy.InputField(desc="The full text content to be analyzed and classified")
    label: str = dspy.OutputField(desc="The classification label for this text")

# Concise — same quality, fewer tokens
class Concise(dspy.Signature):
    """Classify the text."""
    text: str = dspy.InputField()
    label: str = dspy.OutputField()
```

## Step 6: Fine-tune a cheap model (advanced)

The biggest cost saver: train a small cheap model to do what the expensive model does. Distill from an expensive teacher to a cheap student:

```python
# Build and optimize with the expensive model, then fine-tune a cheap one
optimizer = dspy.BootstrapFinetune(metric=metric, num_threads=24)
finetuned = optimizer.compile(my_program, trainset=trainset, teacher=teacher_optimized)
```

**Requirements:** 500+ training examples, a fine-tunable model.
**Typical savings:** 10-50x cost reduction with 85-95% quality retention.

For the complete model distillation workflow (decision framework, prerequisites, BetterTogether, troubleshooting), see `/ai-fine-tuning`.

## Step 7: Use `Predict` instead of `ChainOfThought` where possible

`ChainOfThought` adds a reasoning step which uses extra tokens. For simple tasks, `Predict` may be sufficient:

```python
# ChainOfThought — more tokens, better for complex tasks
classifier = dspy.ChainOfThought(ClassifySignature)

# Predict — fewer tokens, fine for simple tasks
classifier = dspy.Predict(ClassifySignature)
```

Test with `/ai-improving-accuracy` to make sure quality doesn't drop.

### Saturation-aware early stopping

When running prompt optimization (especially with GEPA or MIPROv2), monitor for score plateaus. Stopping early when the optimizer saturates can save 30-40% of optimization compute. See `/dspy-gepa` for saturation diagnosis details.

## Strategy comparison

| Strategy | Savings potential | Complexity | Key requirement |
|----------|------------------|------------|-----------------|
| Switch to cheaper model | 10–30x lower per-call cost | Low | Re-run optimizer after switch |
| Enable/verify caching | 50–90% on repeated traffic | Trivial | Deterministic inputs (`temperature=0`) |
| Per-module LM assignment | 50–80% | Low | Identify which steps are simple vs complex |
| Smart routing / cascading | 50–90% | Medium | A classifier or confidence check step |
| Reduce prompt length | 20–50% | Low | Fewer demos, smaller `k`, concise signatures |
| Fine-tune a cheap model | 10–50x | High | 500+ labeled examples, fine-tunable model |

## Cost reduction checklist

1. Switch to a cheaper model (measure quality first)
2. Verify caching is enabled
3. Use cheap models for simple steps, expensive for complex
4. Route easy inputs to cheap models, hard ones to expensive (Step 4)
5. Reduce few-shot examples (2 instead of 4)
6. Reduce retrieved passages
7. Use `Predict` instead of `ChainOfThought` for simple tasks
8. Fine-tune a cheap model for production (if 500+ examples available)

## Gotchas

- **Don't re-optimize prompts on the old model after switching.** Claude tends to keep the expensive model's optimized prompts when switching to a cheaper model. Prompts don't transfer between models — always re-run your optimizer after changing the LM. See `/ai-switching-models`.
- **Don't use `ChainOfThought` for the complexity router itself.** The router in Step 4 should use `dspy.Predict`, not `dspy.ChainOfThought` — adding reasoning to the routing step defeats the purpose of saving tokens on easy inputs.
- **Don't cut demos to zero and expect quality to hold.** Reducing `max_bootstrapped_demos` from 4 to 2 is fine; setting it to 0 removes all few-shot learning and quality collapses. Keep at least 1-2 demos.
- **Don't forget to measure before and after every cost change.** Claude often applies multiple cost optimizations at once without baselining. Run `dspy.evaluate` before each change so you can attribute quality drops to the specific optimization that caused them.
- **Don't cache non-deterministic calls and expect reproducibility.** If `temperature > 0`, cached results lock in one sample. Set `temperature=0` for deterministic caching, or disable caching for calls where you want diversity.

## When NOT to optimize costs

Do not cut costs if you have not baselined quality first. Optimizing costs on a system that already underperforms just locks in bad results at a lower price. Fix accuracy first with `/ai-improving-accuracy`, then reduce costs.

Do not route to cheap models if your traffic is uniformly complex. The routing pattern (Step 4) saves money when most inputs are easy — if 90% of your inputs genuinely need the expensive model, routing adds latency and complexity for minimal savings.

Do not fine-tune to save money if your use case changes frequently. Fine-tuned models are frozen in time — if your categories, policies, or domain shift monthly, the retraining cost and lag outweigh the per-call savings. Use prompt optimization instead.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Multi-step pipelines** with per-stage model assignment — see `/ai-building-pipelines`
- **Measure quality** before and after cost cuts — see `/ai-improving-accuracy`
- **Debug breakage** from cost optimization — see `/ai-fixing-errors`
- **Switch models** without breaking prompts — see `/ai-switching-models`
- **DSPy modules** (Predict vs ChainOfThought tradeoffs) — see `/dspy-modules`
- **Fine-tuning** workflow and decision framework — see `/ai-fine-tuning`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (model switching, cascading, end-to-end ticket triage), see [examples.md](examples.md)
- For DSPy API quick reference (dspy.LM, BootstrapFewShot, set_lm, configure_cache), see [reference.md](reference.md)
