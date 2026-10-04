---
name: dspy-multi-chain-comparison
description: Use when you want higher accuracy by generating multiple reasoning chains and selecting the best answer — trading speed for quality on critical outputs. Common scenarios - high-stakes decisions where you want multiple reasoning paths compared, classification tasks where one chain of thought is not reliable enough, improving accuracy by generating several answers and selecting the best-reasoned one, or tasks where different reasoning approaches yield different answers. Related - ai-reasoning, ai-improving-accuracy, dspy-chain-of-thought. Also used for dspy.MultiChainComparison, compare multiple reasoning chains, select best reasoning path, multi-path reasoning, vote across chain-of-thought outputs, more reliable than single CoT, deliberation for hard problems, when one reasoning chain is not enough, robust reasoning through comparison, ensemble reasoning, trade speed for accuracy on critical tasks.
---

# Get Better Answers by Comparing Multiple Reasoning Chains

Guide the user through using `dspy.MultiChainComparison` to improve answer quality. Instead of relying on a single chain of thought, you generate several independent reasoning chains yourself and then hand them to this module, which selects the best final answer by comparing them.

## Step 1 — Gather context

Before generating code, clarify:

1. **What is your signature?** What inputs does your task take and what output do you want? (example: `"problem -> recommendation"` or a class-based `dspy.Signature`)
2. **How many chains (M)?** Start with M=3 unless latency or cost is constrained. Increase to M=5 for high-stakes tasks where you have evidence that a single ChainOfThought is unreliable.
3. **Are you wrapping in a `dspy.Module`?** Wrapping both the generator and the comparison step in a module enables optimizer tuning of both prompts.
4. **Do you need selective routing?** If only some inputs are complex enough to warrant MultiChainComparison, an adaptive router (classify difficulty → fast CoT or multi-chain) reduces cost significantly.

## What is MultiChainComparison

`dspy.MultiChainComparison` is a DSPy module that:

1. **Takes M pre-generated reasoning chains** -- you generate these yourself first (one `ChainOfThought` call with `n=M`), then pass them in
2. **Compares the candidates** -- a single comparison/synthesis LM call evaluates all chains and picks the best answer
3. **Returns a single answer** -- the output looks the same as any other DSPy module

Important: `MultiChainComparison` does NOT generate the chains for you. You generate the M completions first, then pass them as the first positional argument to the module. The module itself makes exactly **1 LM call** -- the synthesis step.

Think of it as getting multiple opinions from different experts, then having a judge pick the most convincing one. The diversity of reasoning paths surfaces better answers than any single chain alone.

## When to use MultiChainComparison

Use it when:

- **Quality matters more than speed** -- you can afford extra LM calls for a better answer
- **Tasks have genuine ambiguity** -- multiple valid approaches exist and you want the best one
- **Single CoT is unreliable** -- the model sometimes reasons poorly and you want redundancy
- **High-stakes decisions** -- recommendations, diagnoses, critical analysis where being wrong is costly

Do NOT use it when:

- **Latency is critical** -- generating M chains (one `ChainOfThought` call with `n=M`) plus the comparison call is slower than a single `ChainOfThought`
- **The task is straightforward** -- simple classification, extraction, or lookup does not benefit from multiple chains
- **Cost is a hard constraint** -- generating M chains plus the synthesis call costs more than a single `ChainOfThought`
- **You need deterministic output** -- the comparison step adds variability

## Basic usage

Using `MultiChainComparison` is a **two-step** process. First you generate M reasoning chains yourself with one `ChainOfThought` call (set `n=M`), then you pass the resulting `.completions` list as the first positional argument to the `MultiChainComparison` instance:

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Step 1: generate M=5 reasoning chains yourself (one ChainOfThought call with n=M)
generate = dspy.ChainOfThought("problem -> recommendation", n=5)
completions = generate(
    problem="We need to migrate from MongoDB to PostgreSQL for our 50GB dataset with complex joins"
).completions  # list of M completions

# Step 2: pass the completions to MultiChainComparison to synthesize the best answer
compare = dspy.MultiChainComparison("problem -> recommendation", M=5)
result = compare(
    completions,
    problem="We need to migrate from MongoDB to PostgreSQL for our 50GB dataset with complex joins",
)
print(result.recommendation)
```

Make sure `M` on the `MultiChainComparison` instance matches the number of completions you generated (`n` on the `ChainOfThought` generator).

With a class-based signature -- same two-step pattern:

```python
import dspy

class TechRecommendation(dspy.Signature):
    """Recommend the best technical approach for this problem."""
    problem: str = dspy.InputField(desc="Technical problem or decision to make")
    constraints: str = dspy.InputField(desc="Budget, timeline, or technical constraints")
    recommendation: str = dspy.OutputField(desc="The recommended approach with justification")

inputs = dict(
    problem="Our API response times are over 2 seconds under load",
    constraints="Small team, no budget for new infrastructure",
)

# Step 1: generate the chains
generate = dspy.ChainOfThought(TechRecommendation, n=3)
completions = generate(**inputs).completions

# Step 2: compare and synthesize
compare = dspy.MultiChainComparison(TechRecommendation, M=3)
result = compare(completions, **inputs)
print(result.recommendation)
```

## How it works internally

The work is split across two steps -- the first is yours, the second is the module's:

1. **You generate the chains** -- one `ChainOfThought` call with `n=M` produces M completions, each with its own `reasoning` and output fields. This is a single LM call (the provider returns M samples).
2. **You pass the completions in** -- `compare(completions, **inputs)` hands the M pre-generated chains to `MultiChainComparison`.
3. **The module runs one comparison step** -- a single LM call sees all candidate chains and selects/synthesizes the best answer.

The comparison step is the key differentiator. Rather than picking randomly or voting, the model actively evaluates the quality of each reasoning chain before choosing. `MultiChainComparison` itself contributes exactly **1 LM call** -- the synthesis. It does not generate the chains.

```
Input --> ChainOfThought(n=M) --> reasoning_1 + answer_1 --|
                                  reasoning_2 + answer_2 --|--> MultiChainComparison --> best answer
                                  reasoning_3 + answer_3 --|   (1 synthesis LM call)
       (1 LM call returning M completions)
```

## Configuring the number of chains

By default, `MultiChainComparison` expects 3 chains. `M` tells the module how many completions to expect (it must match the `n` you used when generating them). You can adjust `M` and `temperature`:

```python
# Constructor signature
dspy.MultiChainComparison(signature, M=3, temperature=0.7, **config)
```

- `M` — number of reasoning chains the module expects to receive (default 3); set the `ChainOfThought` generator's `n` to the same value.
- `temperature` — sampling temperature for the comparison step (default 0.7). When generating chains, set the temperature on the `ChainOfThought` generator; higher values produce more diverse chains, which gives the comparison step more to work with.

Guidelines for choosing M (the chains are 1 `ChainOfThought` call with `n=M`; `MultiChainComparison` adds 1 synthesis call):

| M value | LM calls | Best for |
|---------|----------|----------|
| 2 | 2 (1 generate call + 1 synthesis) | Slight quality boost over single CoT |
| 3 | 2 (1 generate call + 1 synthesis) | Good default, balances quality and cost |
| 5 | 2 (1 generate call + 1 synthesis) | High-stakes tasks where accuracy is critical |
| 7+ | 2 (1 generate call + 1 synthesis) | Diminishing returns for most tasks |

## Using MultiChainComparison in a module

Wrap it in a `dspy.Module` to combine with other steps:

```python
import dspy
from typing import Literal

class RiskAssessment(dspy.Signature):
    """Assess the risk level of this proposed change."""
    change_description: str = dspy.InputField(desc="What is being changed")
    system_context: str = dspy.InputField(desc="The system being modified")
    risk_level: Literal["low", "medium", "high", "critical"] = dspy.OutputField()
    risk_factors: str = dspy.OutputField(desc="Key risks identified")
    mitigation: str = dspy.OutputField(desc="Recommended mitigation steps")

class ChangeReviewer(dspy.Module):
    def __init__(self, M=3):
        self.M = M
        self.classify = dspy.Predict("change_description -> change_type: str")
        # Generator produces M chains; MCC synthesizes the best answer
        self.generate = dspy.ChainOfThought(RiskAssessment, n=M)
        self.assess = dspy.MultiChainComparison(RiskAssessment, M=M)

    def forward(self, change_description, system_context):
        change_type = self.classify(change_description=change_description).change_type
        inputs = dict(
            change_description=f"[{change_type}] {change_description}",
            system_context=system_context,
        )
        # Step 1: generate M reasoning chains
        completions = self.generate(**inputs).completions
        # Step 2: compare and synthesize the best answer
        result = self.assess(completions, **inputs)
        return dspy.Prediction(
            change_type=change_type,
            risk_level=result.risk_level,
            risk_factors=result.risk_factors,
            mitigation=result.mitigation,
        )

# Usage
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

reviewer = ChangeReviewer()
result = reviewer(
    change_description="Drop the users_v1 table and migrate all queries to users_v2",
    system_context="Production e-commerce platform with 10k daily active users",
)
print(f"Risk: {result.risk_level}")
print(f"Factors: {result.risk_factors}")
print(f"Mitigation: {result.mitigation}")
```

## Cost and latency tradeoffs

The two-step pattern trades speed and cost for quality. The chain generation is 1 `ChainOfThought` call (with `n=M`) and `MultiChainComparison` adds 1 synthesis call. Here is a rough comparison with M=3:

| Aspect | ChainOfThought | Generate (n=3) + MultiChainComparison |
|--------|---------------|---------------------------|
| LM calls | 1 | 2 (1 generate call returning 3 chains + 1 synthesis) |
| Latency | 1x | ~2x (the generate call returns M samples in one round trip) |
| Cost | 1x | ~M+1 tokens worth (M sampled completions + 1 synthesis) |
| Quality | Good | Better on ambiguous/complex tasks |

Note: even though there are only 2 LM calls, the generate call samples M completions, so token cost scales with M (roughly M generations + 1 synthesis).

Strategies to manage cost:

- **Use a cheaper model for chains, an expensive model for comparison** -- the comparison step benefits most from a strong model, while the chains can be sampled cheaply:

```python
cheap_lm = dspy.LM("openai/gpt-4o-mini")  # or any smaller model
expensive_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# Generate the M chains with the cheap model
generate = dspy.ChainOfThought("problem -> recommendation", n=5)
generate.set_lm(cheap_lm)

# Run the synthesis/comparison with the expensive model
compare = dspy.MultiChainComparison("problem -> recommendation", M=5)
compare.set_lm(expensive_lm)

problem = "Our API response times are over 2 seconds under load"
completions = generate(problem=problem).completions
result = compare(completions, problem=problem)
print(result.recommendation)
```

- **Use MultiChainComparison selectively** -- route only hard tasks through it:

```python
class AdaptiveReasoner(dspy.Module):
    def __init__(self, M=3):
        self.M = M
        self.classify_difficulty = dspy.Predict("question -> difficulty: str")
        self.fast = dspy.ChainOfThought("question -> answer")
        self.generate = dspy.ChainOfThought("question -> answer", n=M)
        self.compare = dspy.MultiChainComparison("question -> answer", M=M)

    def forward(self, question):
        difficulty = self.classify_difficulty(question=question).difficulty.lower()
        if "hard" in difficulty or "complex" in difficulty:
            completions = self.generate(question=question).completions
            return self.compare(completions, question=question)
        return self.fast(question=question)
```

## Optimizing MultiChainComparison

`MultiChainComparison` modules are optimizable like any other DSPy module. Because the chains are generated by a separate `ChainOfThought` step, wrap both steps in a `dspy.Module` so the optimizer can tune the prompts for both the generation and the comparison/synthesis steps:

```python
def quality_metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()

class CompareReasoner(dspy.Module):
    def __init__(self, M=3):
        self.generate = dspy.ChainOfThought("question -> answer", n=M)
        self.compare = dspy.MultiChainComparison("question -> answer", M=M)

    def forward(self, question):
        completions = self.generate(question=question).completions
        return self.compare(completions, question=question)

program = CompareReasoner(M=3)

optimizer = dspy.BootstrapFewShot(metric=quality_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(program, trainset=trainset)

# Save for production
optimized.save("optimized_mcc.json")
```

For best results with MIPROv2:

```python
optimizer = dspy.MIPROv2(metric=quality_metric, auto="medium")
optimized = optimizer.compile(program, trainset=trainset)
```

Typical improvement range (task-dependent): a single `ChainOfThought` baseline often scores 60-70% on hard reasoning tasks; M=3 chains without optimization typically adds 5-10 points; M=3 with `BootstrapFewShot` adds another 5-8 points on top of that; M=3 with `MIPROv2` can push further still. Always measure on your specific devset with `dspy.Evaluate` — actual gains depend heavily on how ambiguous the task is and how much diversity M chains actually introduce.

## When NOT to use MultiChainComparison

Pick a simpler alternative when:

| Situation | Use instead |
|-----------|-------------|
| Simple classification or extraction | `dspy.Predict` |
| Needs reasoning but latency matters | `dspy.ChainOfThought` |
| Math or computation tasks | `dspy.ProgramOfThought` |
| Need tool use or API calls | `dspy.ReAct` |
| Want retries with self-correction | `dspy.Refine` + `ChainOfThought` |

MultiChainComparison is most valuable when the problem genuinely benefits from diverse perspectives -- not when there is a single clearly correct approach.

## Gotchas

1. **Claude calls MultiChainComparison directly with raw inputs.** `MultiChainComparison` does NOT generate the chains. You must generate M completions first (`dspy.ChainOfThought(sig, n=M)`), grab `.completions`, then pass that list as the first positional argument: `compare(completions, **inputs)`. Calling `compare(problem=...)` without completions is wrong.
2. **Claude forgets to sample diverse chains.** Diversity comes from the `ChainOfThought` generator. Generate with `n=M` and a non-zero temperature on the generator — with `temperature=0` the chains are near-identical and the comparison step adds cost with no quality gain. Keep the default `temperature=0.7` or higher.
3. **Claude uses MultiChainComparison for simple tasks.** For straightforward classification, extraction, or lookup, the generate-plus-synthesize pattern adds cost with no quality improvement. Use `dspy.Predict` or `dspy.ChainOfThought` for simple tasks and reserve MultiChainComparison for genuinely ambiguous or high-stakes decisions.
4. **Claude sets M too high.** Beyond M=5, diminishing returns set in quickly — each additional chain adds a sampled generation but contributes marginal diversity. Start with M=3 and only increase if evaluation shows improvement. Also keep `M` on the module equal to the generator's `n`.
5. **Claude ignores the cost during optimization.** Optimizing a wrapper module that generates M chains plus a synthesis call means every trial makes 2 LM calls and samples M completions. With many trials this adds up. Use `auto="light"` for MIPROv2 or keep trial counts low.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **ChainOfThought** is the single-chain version and the right default -- see `/dspy-chain-of-thought`
- **Reasoning strategies** including when to pick MultiChainComparison vs other approaches -- see `/ai-reasoning`
- **Improving accuracy** with evaluation and optimization -- see `/ai-improving-accuracy`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.MultiChainComparison API docs](https://dspy.ai/api/modules/MultiChainComparison/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
