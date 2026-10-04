---
name: dspy-refine
description: Iterative self-improvement with dspy.Refine -- wraps any module, scores each attempt with a reward function, generates feedback on failures, and retries until a quality threshold is met. Use when you want outputs to improve through self-critique, need iterative revision of drafts, or want the LM to learn from its own mistakes within a single request. Also used for self-critique and revise, iterative improvement loop, generate then evaluate then fix, AI self-editing, multi-draft generation, revise until good enough, critique-driven refinement, when first draft is not good enough.
---

# Iterative Self-Improvement with dspy.Refine

## Step 1: Understand the use case

Before writing code, clarify:

1. **What module are you wrapping?** (ChainOfThought, Predict, ReAct, custom module?)
2. **What makes a good output?** Can you express quality as a numeric score?
3. **How many retries are acceptable?** (cost/latency budget)
4. **Is feedback useful?** Would knowing why attempt 1 failed help attempt 2? If not, consider `dspy.BestOfN` instead.

## When to use Refine (and when not to)

> **Migrating from dspy.Assert / dspy.Suggest?** Both were removed in DSPy 3.x. `dspy.Refine` is their replacement and handles feedback-driven retries natively — no custom retry loop needed.

Use `dspy.Refine` when:

- Outputs must meet measurable quality criteria (format, length, accuracy)
- The LM can improve with feedback -- writing, format compliance, multi-criteria quality
- Quality is worth 2-5x cost for N attempts

Do **not** use Refine when:

- You have no clear way to score outputs -- use `dspy.ChainOfThought` instead
- You need human-in-the-loop feedback -- build a custom module with a human review step
- Speed matters more than quality -- use a single `dspy.Predict` call
- Attempts are independent and feedback would not help -- use `dspy.BestOfN`

## Basic usage

Three things are needed: a module to wrap, a reward function, and a threshold.

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# 1. Define the module to refine
qa = dspy.ChainOfThought("question -> answer")

# 2. Define a reward function
# Takes (args_dict, prediction) -> float
def concise_answer(args, pred):
    """Reward one-word answers."""
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

# 3. Wrap with Refine
refined_qa = dspy.Refine(
    module=qa,
    N=3,
    reward_fn=concise_answer,
    threshold=1.0,
)

# Use it -- same interface as the wrapped module
result = refined_qa(question="What is the capital of Belgium?")
print(result.answer)  # "Brussels"
```

## Constructor parameters

```python
dspy.Refine(
    module,          # dspy.Module -- required
    N,               # int -- required, max attempts
    reward_fn,       # Callable[[dict, Prediction], float] -- required
    threshold,       # float -- required, target reward score
    fail_count=None, # int | None -- max failures before error (defaults to N)
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `module` | `dspy.Module` | required | The module whose outputs you want to refine |
| `N` | `int` | required | Maximum number of attempts. Each attempt uses temperature=1.0 with a different rollout ID |
| `reward_fn` | `Callable[[dict, Prediction], float]` | required | Scores a prediction. Receives `(args, pred)` where `args` is the input kwargs dict and `pred` is the module's output. Returns a `float` |
| `threshold` | `float` | required | Target score. Refine returns immediately when an attempt meets or exceeds this value |
| `fail_count` | `int \| None` | `None` (→ `N`) | Maximum allowed failures before raising an error |

## Writing reward functions

The reward function is the core of Refine. It receives two arguments:

1. **`args`** -- a dict of the inputs passed to the module (e.g., `{"question": "What is..."}`)
2. **`pred`** -- the module's prediction object (access fields like `pred.answer`, `pred.reasoning`)

It must return a `float`. Higher is better.

### Simple binary reward

```python
def valid_json(args, pred):
    """Accept only valid JSON outputs."""
    import json
    try:
        json.loads(pred.output)
        return 1.0
    except (json.JSONDecodeError, TypeError):
        return 0.0
```

### Graduated reward

Return partial scores to help Refine pick the best attempt even when none fully succeed:

```python
def quality_score(args, pred):
    """Score answer quality on multiple criteria."""
    score = 0.0
    answer = pred.answer

    # Criterion 1: not empty
    if answer.strip():
        score += 0.3

    # Criterion 2: reasonable length (20-200 words)
    word_count = len(answer.split())
    if 20 <= word_count <= 200:
        score += 0.4

    # Criterion 3: addresses the question
    if args["question"].split()[0].lower() in answer.lower():
        score += 0.3

    return score
```

### Using external validation

```python
import re

def valid_email_extraction(args, pred):
    """Reward valid email addresses extracted from text."""
    emails = pred.emails if isinstance(pred.emails, list) else []
    if not emails:
        return 0.0
    email_pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
    valid_count = sum(1 for e in emails if re.match(email_pattern, e))
    return valid_count / len(emails)
```

## How iteration count (N) works

Each attempt runs the wrapped module at temperature=1.0 with a different rollout ID, producing diverse outputs. Refine's selection logic:

1. Run the module and score the output with `reward_fn`
2. If the score meets or exceeds `threshold`, return immediately
3. If not, generate feedback from the failure and try again
4. After N attempts, return the attempt with the highest reward score

**Choosing N:**

| N value | Use case | Cost |
|---------|----------|------|
| 2-3 | Format validation, simple constraints | Low overhead |
| 3-5 | Quality criteria, multi-factor scoring | Moderate |
| 5-10 | High-stakes outputs, strict requirements | Higher cost, better results |

The sweet spot for most use cases is **N=3 to N=5**. Beyond 5, diminishing returns are common unless the reward function is very specific.

In practice, Refine with N=3 and a graduated reward function typically moves a pipeline from a 40-60% baseline pass rate (outputs meeting your quality bar on the first try) to 75-90%. The exact gain depends on how achievable the threshold is and how much the feedback mechanism can guide the LM toward improvement.

## The feedback mechanism

What makes Refine different from random retries is **feedback generation**. When an attempt fails to meet the threshold:

1. Refine examines why the attempt scored below the threshold
2. It generates natural-language feedback describing the shortcoming
3. This feedback is included in the prompt for the next attempt
4. The LM uses this feedback to produce a better output

This means later attempts are informed by earlier failures. Attempt 3 knows what went wrong in attempts 1 and 2.

You do not write the feedback logic -- Refine handles it automatically based on your reward function's scores.

## Refine vs BestOfN -- when to use which

Both modules run a wrapped module multiple times and select the best output, but they work differently:

| Aspect | `dspy.Refine` | `dspy.BestOfN` |
|--------|--------------|----------------|
| **Feedback** | Generates feedback from failures, improving subsequent attempts | No feedback -- each attempt is independent |
| **Attempts** | Sequential (each informed by previous) | Independent (can be parallel) |
| **Early stopping** | Returns on first success meeting threshold | Also returns on first success meeting threshold |
| **Best for** | Iterative improvement, complex quality criteria | Sampling diversity, simple pass/fail |
| **Cost pattern** | Often fewer calls (feedback improves later attempts) | All attempts independent, no learning between them |

**Use Refine when** the LM can improve with feedback -- writing tasks, format compliance, multi-criteria quality.

**Use BestOfN when** attempts are independent and feedback would not help -- creative generation, sampling diverse options, simple binary checks.

## Wrapping custom modules

Refine works with any `dspy.Module`, not just built-in ones:

```python
class Summarizer(dspy.Module):
    def __init__(self):
        self.summarize = dspy.ChainOfThought("article -> summary")

    def forward(self, article):
        return self.summarize(article=article)


def good_summary(args, pred):
    """Score summary quality."""
    summary = pred.summary
    article = args["article"]
    score = 0.0

    # Shorter than original
    if len(summary) < len(article) * 0.3:
        score += 0.5

    # At least 2 sentences
    if summary.count('.') >= 2:
        score += 0.5

    return score


refined_summarizer = dspy.Refine(
    module=Summarizer(),
    N=3,
    reward_fn=good_summary,
    threshold=0.8,
)

result = refined_summarizer(article="Long article text here...")
print(result.summary)
```

## Gotchas

- **Claude uses binary reward functions (0 or 1) instead of graduated scores.** Binary rewards mean Refine cannot distinguish between a near-miss and a total failure when no attempt hits the threshold. Use graduated floats (0.0 to 1.0) with partial credit for each criterion so Refine returns the best near-miss.
- **Claude puts LM calls inside reward functions for "smarter" scoring.** The reward function runs on every attempt (up to N times), so an LM call inside it doubles or triples your cost. Use deterministic checks (regex, AST parsing, length checks) in reward functions. Reserve LM-as-judge for the final evaluation after Refine returns.
- **Claude sets threshold=1.0 with multi-criteria reward functions.** If your reward function scores 4 weighted criteria, achieving a perfect 1.0 is unlikely. Refine then burns through all N attempts and returns a near-miss anyway. Set the threshold to 0.8 or the realistic "good enough" score for your criteria.
- **Claude confuses Refine with BestOfN and uses them interchangeably.** The key difference is feedback: Refine generates feedback from failures and feeds it into subsequent attempts (sequential, improving). BestOfN runs independent attempts with no cross-attempt learning. Use Refine when later attempts can learn from earlier failures; use BestOfN when attempts are inherently independent.
- **Claude wraps a Predict module with Refine for tasks that need reasoning.** Refine improves outputs through feedback, but `dspy.Predict` does not expose a `reasoning` field. Use `dspy.ChainOfThought` as the inner module so the feedback loop has reasoning to critique and improve.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **BestOfN** for independent sampling without feedback -- see `/dspy-best-of-n`
- **Chain of thought reasoning** as the inner module -- see `/dspy-chain-of-thought`
- **Checking and validating outputs** with assertions -- see `/ai-checking-outputs`
- **Improving accuracy** with optimization -- see `/ai-improving-accuracy`
- **Writing content** that benefits from iterative refinement -- see `/ai-writing-content`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.Refine API docs](https://dspy.ai/api/modules/Refine/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)
