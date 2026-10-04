---
name: dspy-two-step-adapter
description: Use when working with reasoning models (o1, o3, o3-mini, DeepSeek-R1, Claude extended thinking) that reject system prompts or ignore formatting instructions. Common scenarios - using o1 or o3 with DSPy, getting structured output from reasoning models, two-phase prompting where a reasoning model generates freely then an extraction model parses the output, or fixing format errors from thinking models. Related - dspy-adapters, dspy-lm, ai-switching-models. Also used for dspy.TwoStepAdapter, o1 with DSPy, o3-mini DSPy, reasoning model in DSPy, DeepSeek-R1 DSPy, extended thinking DSPy, thinking model ignores format, o1 ignores my DSPy format, TwoStepAdapter setup, two-phase prompting, extraction LM, reasoning model structured output, extraction_model TwoStepAdapter, model pairing for reasoning models.
---

# Use Reasoning Models with dspy.TwoStepAdapter

Guide the user through configuring DSPy to work with reasoning models (o1, o3, o3-mini, DeepSeek-R1, Claude with extended thinking) that need special handling for structured output.

## Why reasoning models need TwoStepAdapter

Reasoning models (o1, o3, DeepSeek-R1, Claude extended thinking) behave differently from standard chat models:

- They **reject or ignore system prompts** (o1/o3 strip them)
- They **ignore formatting instructions** (the model "thinks" and produces free-form output)
- They **cannot follow ChatAdapter's field delimiters** (`[[ ## field_name ## ]]`)

`TwoStepAdapter` solves this with a two-phase approach:
1. **Phase 1 (main LM):** The reasoning model generates freely -- no formatting constraints
2. **Phase 2 (extraction LM):** A fast, cheap model parses the reasoning output into structured fields

## When to use TwoStepAdapter

| Use TwoStepAdapter when... | Use ChatAdapter (default) when... |
|---------------------------|----------------------------------|
| Using o1, o3, o3-mini | Using GPT-4o, Claude, Gemini |
| Using DeepSeek-R1 | Using any instruction-following model |
| Using Claude with extended thinking | The model follows formatting reliably |
| Model ignores your output format | Structured output works out of the box |
| Getting raw reasoning dumps instead of fields | You do not need reasoning-heavy processing |

## Step 1: Basic TwoStepAdapter setup

```python
import dspy

# The reasoning model (generates freely)
main_lm = dspy.LM("openai/o3-mini")

# The extraction model (parses into structured fields)
extraction_lm = dspy.LM("openai/gpt-4o-mini")

# Configure the adapter (only the extraction model is passed in)
adapter = dspy.TwoStepAdapter(extraction_model=extraction_lm)

# The reasoning model is the configured lm, not an adapter argument
dspy.configure(lm=main_lm, adapter=adapter)
```

Now use DSPy normally -- the adapter handles the two-phase flow transparently:

```python
qa = dspy.ChainOfThought("question -> answer")
result = qa(question="What is 127 * 389?")
print(result.answer)  # Structured output, extracted by gpt-4o-mini
```

## Step 2: Model pairing recommendations

| Reasoning model (`dspy.configure(lm=...)`) | Extraction model (`extraction_model=...`) | Notes |
|---------------------------|----------------------------------|-------|
| `openai/o1` | `openai/gpt-4o-mini` | Best reasoning + cheap extraction |
| `openai/o3` | `openai/gpt-4o-mini` | Highest capability |
| `openai/o3-mini` | `openai/gpt-4o-mini` | Cost-effective reasoning |
| `deepseek/deepseek-r1` | `openai/gpt-4o-mini` | Open-weight reasoning |
| `anthropic/claude-sonnet-4-5-20250929` (extended thinking) | `anthropic/claude-haiku-3-5-20241022` | All-Anthropic stack |

**Pairing principles:**
- The extraction LM should be **fast and cheap** -- it just parses structured fields from text
- The extraction LM must **follow formatting instructions well** (ChatAdapter-compatible)
- Cross-provider pairing is fine (o3 + Claude Haiku works)

## Step 3: Per-module adapter assignment

You can use TwoStepAdapter for specific modules while using ChatAdapter elsewhere:

```python
import dspy

# Default: fast model with ChatAdapter
fast_lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=fast_lm)

# Reasoning model for hard problems
reasoning_lm = dspy.LM("openai/o3-mini")
extraction_lm = dspy.LM("openai/gpt-4o-mini")
reasoning_adapter = dspy.TwoStepAdapter(extraction_model=extraction_lm)


class Pipeline(dspy.Module):
    def __init__(self):
        # Simple classification -- uses default ChatAdapter
        self.classify = dspy.Predict("text -> category")

        # Hard reasoning -- uses TwoStepAdapter
        self.analyze = dspy.ChainOfThought("text, category -> analysis")
        self.analyze.adapter = reasoning_adapter
        self.analyze.lm = reasoning_lm

    def forward(self, text):
        category = self.classify(text=text).category
        analysis = self.analyze(text=text, category=category).analysis
        return dspy.Prediction(category=category, analysis=analysis)
```

## Step 4: Handling extended thinking (Claude)

Claude with extended thinking uses a budget parameter instead of a separate model:

```python
import dspy

# Claude with extended thinking enabled
thinking_lm = dspy.LM(
    "anthropic/claude-sonnet-4-5-20250929",
    thinking={"type": "enabled", "budget_tokens": 10000},
)

# Extraction model
extraction_lm = dspy.LM("anthropic/claude-haiku-3-5-20241022")

adapter = dspy.TwoStepAdapter(extraction_model=extraction_lm)

# The thinking model is the configured lm, not an adapter argument
dspy.configure(lm=thinking_lm, adapter=adapter)

# Works transparently -- thinking model reasons, haiku extracts structure
solver = dspy.ChainOfThought("problem -> solution")
result = solver(problem="Prove that sqrt(2) is irrational")
```

## Step 5: When NOT to use TwoStepAdapter

Do not use TwoStepAdapter when:

- **The model already follows formatting** -- standard models (GPT-4o, Claude, Gemini) work fine with ChatAdapter
- **You need minimum latency** -- two LM calls instead of one adds overhead
- **The task is simple** -- reasoning models are overkill for classification or extraction
- **Cost is critical** -- you pay for both the reasoning call and the extraction call

If the model follows ChatAdapter format reliably, TwoStepAdapter adds cost and latency for no benefit.

## Gotchas

1. **Claude uses ChatAdapter for o1/o3 models.** Reasoning models reject ChatAdapter formatting. If you see raw reasoning dumps without structured fields, switch to TwoStepAdapter.
2. **Claude sets extraction_lm to the same reasoning model.** The extraction model should be fast and cheap (gpt-4o-mini, Claude Haiku). Using o3 for extraction wastes money and is slower.
3. **Claude forgets to set both `lm` and `adapter` on per-module assignment.** When assigning TwoStepAdapter to a specific module, set both `module.lm = reasoning_lm` and `module.adapter = dspy.TwoStepAdapter(extraction_model=...)`. There is no `main_lm` constructor arg -- the reasoning model is the module's `lm`, and only the extraction model goes to the adapter. Missing either causes the wrong model or wrong adapter to be used.
4. **TwoStepAdapter is not needed for DeepSeek-V3.** Only DeepSeek-R1 (the reasoning variant) needs it. DeepSeek-V3 follows formatting like a standard chat model.
5. **Claude wraps extended thinking in TwoStepAdapter incorrectly.** For Claude extended thinking, pass `thinking={"type": "enabled", "budget_tokens": N}` to the LM constructor, not as a separate parameter.

## Additional resources

- [dspy.ai/api/adapters/TwoStepAdapter](https://dspy.ai/api/adapters/TwoStepAdapter/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **All adapters** overview -- see `/dspy-adapters`
- **ChatAdapter** deep dive -- see `/dspy-chatadapter`
- **LM configuration** and provider setup -- see `/dspy-lm`
- **Switching models** without breaking prompts -- see `/ai-switching-models`
- **Install `/ai-do` if you do not have it** -- it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
