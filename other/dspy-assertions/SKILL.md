---
name: dspy-assertions
description: Legacy reference for dspy.Assert and dspy.Suggest, both removed in DSPy 3.x - use dspy.Refine or dspy.BestOfN instead. Use when maintaining a legacy DSPy 2.x codebase that uses dspy.Assert or dspy.Suggest, or migrating from Assert/Suggest to DSPy 3.x. Also used for dspy.Assert, dspy.Suggest, runtime validation for LLM output, retry on bad output, backtracking on constraint violation, guard rails in DSPy, migrate from Assert, migrate from Suggest, ImportError cannot import Assert, ImportError cannot import Suggest.
---

# Enforce Constraints with dspy.Assert and dspy.Suggest

> **REMOVED IN DSPy 3.x.** `dspy.Assert` and `dspy.Suggest` have been removed from the DSPy codebase (no `assertions.py`, no imports in `__init__.py`, `retry.py` commented out, no docs page). **Use `dspy.Refine` or `dspy.BestOfN` instead** — see `/dspy-refine` and `/dspy-best-of-n`. This skill documents the legacy API for maintaining existing codebases only.
>
> **Migration guide:**
> | Old pattern | New equivalent |
> |-------------|---------------|
> | `dspy.Assert(condition, msg)` (hard rule, retry) | `dspy.Refine(module, N=3, reward_fn=..., threshold=0.8)` |
> | `dspy.Suggest(condition, msg)` (soft rule, continue) | Lower weight in reward function (penalize but don't block) |
> | `max_backtrack_attempts=2` | `N=3` in Refine/BestOfN |
> | `DSPyAssertionError` on exhaustion | `fail_count` parameter in Refine/BestOfN |
> | Error message as feedback | Refine auto-generates feedback from reward scores |

This skill documents the legacy `dspy.Assert`/`dspy.Suggest` APIs for users with existing DSPy 2.x code. **For all new code, use `/dspy-refine` or `/dspy-best-of-n`** — these are the DSPy 3.x replacements that work today.

## Step 1 — Understand the user's situation

Determine which scenario applies before proceeding:

1. **Maintaining a legacy DSPy 2.x codebase** that already uses `dspy.Assert`/`dspy.Suggest` — use the legacy API reference below to understand behavior. The APIs work in DSPy 2.x only.
2. **Migrating to DSPy 3.x** and getting `ImportError: cannot import name 'Assert' from 'dspy'` — skip to the Migration section. Use `dspy.Refine` or `dspy.BestOfN` instead.
3. **Writing new code** — do not use Assert/Suggest at all. Go directly to `/dspy-refine` or `/dspy-best-of-n`.

## Two kinds of constraints

| | `dspy.Assert` | `dspy.Suggest` |
|---|---|---|
| **Severity** | Hard — must pass | Soft — should pass |
| **On failure** | Retries with feedback, then raises error | Logs a warning, continues execution |
| **Use for** | Format requirements, safety checks, non-negotiable rules | Style preferences, quality nudges, nice-to-haves |

```python
import dspy

class QA(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        result = self.answer(question=question)

        # Hard constraint — retries if violated
        dspy.Assert(
            len(result.answer) > 0,
            "Answer must not be empty",
        )

        # Soft constraint — logs warning but continues
        dspy.Suggest(
            len(result.answer.split()) >= 10,
            "Answer should be at least 10 words for completeness",
        )

        return result
```

## dspy.Assert(condition, message)

Call `dspy.Assert` with a boolean condition and a message. When the condition is `False`, DSPy:

1. Catches the failure
2. Appends your message to the LM's context as feedback
3. Retries the LM call that produced the failing output
4. Repeats up to `max_backtrack_attempts` times (default: 2)
5. If all retries fail, raises `DSPyAssertionError`

```python
dspy.Assert(
    result.answer != "I don't know",
    "You must provide a substantive answer based on the context",
)
```

**Write specific messages.** The message is injected back into the prompt on retry, so "Answer was 350 words, must be under 200" is far more useful than "too long."

## dspy.Suggest(condition, message)

Same signature as `Assert`, but non-blocking. When the condition is `False`:

1. The message is logged as a warning
2. Execution continues normally
3. During optimization, suggestions guide the optimizer toward better prompts

```python
dspy.Suggest(
    "however" not in result.answer.lower(),
    "Avoid hedging language like 'however' — be direct",
)
```

Use `Suggest` when the constraint improves quality but isn't a hard requirement.

## How backtracking works

When `dspy.Assert` fails inside a module's `forward()`, DSPy doesn't just retry the same call. It modifies the signature by injecting the error message as additional context, so the LM has feedback about what went wrong:

```
# Original prompt (simplified)
Question: What is DSPy?
Answer: [LM generates here]

# After assertion failure, retry prompt becomes:
Question: What is DSPy?
Previous attempt failed: "Answer was 350 words, must be under 200. Be concise."
Answer: [LM generates here with feedback]
```

This is why assertion messages should be **actionable instructions**, not just error descriptions.

### Targeting a specific module for backtracking

By default, DSPy backtracks to the most recent LM call. Use the `backtrack_module` parameter to target a specific module instead:

```python
dspy.Assert(
    is_valid_json(result.output),
    "Output must be valid JSON. Check for missing braces or trailing commas.",
    backtrack_module=self.generate,  # retry this specific module
)
```

## Common validation patterns

### Length constraints

```python
dspy.Assert(
    len(result.summary.split()) <= 50,
    f"Summary is {len(result.summary.split())} words, must be under 50",
)
```

### Format validation

```python
import re

dspy.Assert(
    re.match(r"^\d{4}-\d{2}-\d{2}$", result.date or ""),
    "Date must be in YYYY-MM-DD format",
)
```

### Content checks

```python
dspy.Assert(
    not any(phrase in result.answer.lower() for phrase in ["as an ai", "i cannot"]),
    "Do not include AI self-references in the answer",
)
```

### List output validation

```python
dspy.Assert(
    len(result.tags) >= 1,
    "Must assign at least one tag",
)
dspy.Assert(
    all(tag in VALID_TAGS for tag in result.tags),
    f"All tags must be from the valid set: {VALID_TAGS}",
)
```

### Grounding in sources

```python
# Check that the answer references at least one key term from the context
context_terms = set(word.lower() for p in context for word in p.split() if len(word) > 5)
answer_terms = set(word.lower() for word in result.answer.split())
overlap = context_terms & answer_terms
dspy.Assert(
    len(overlap) >= 3,
    "Answer must reference specific terms from the source passages",
)
```

## Using assertions with optimizers

Assertions work with all DSPy optimizers. During optimization:

- **`dspy.Assert`** failures cause the training example to be retried. If the program can't satisfy the constraint after retries, that example is skipped.
- **`dspy.Suggest`** failures are tracked as soft signals. Optimizers like `BootstrapFewShotWithRandomSearch` and `MIPROv2` prefer demo sets where suggestions are satisfied.

This means the optimizer learns prompts and demos that satisfy your constraints on the first try, reducing retries in production:

```python
program = QA()

optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=my_metric,
    max_bootstrapped_demos=4,
    num_candidate_programs=10,
)
optimized = optimizer.compile(program, trainset=trainset)
```

After optimization, the program will have few-shot demos that naturally produce outputs satisfying your assertions.

## Catching assertion errors

When all retries are exhausted, `dspy.Assert` raises `DSPyAssertionError`. Handle it at the call site:

```python
# DSPy 2.x only — this module does not exist in DSPy 3.x
from dspy.primitives.assertions import DSPyAssertionError

try:
    result = program(question="...")
except DSPyAssertionError as e:
    # Log the failure, return a fallback, etc.
    print(f"Output failed validation: {e}")
```

## When to use Assert vs. Suggest

| Scenario | Use |
|----------|-----|
| Output must be valid JSON | `Assert` |
| Answer should be concise | `Suggest` |
| No PII in output | `Assert` |
| Prefer active voice | `Suggest` |
| Must cite sources | `Assert` |
| Avoid hedging language | `Suggest` |
| Output matches expected schema | `Assert` |
| Include a confidence score | `Suggest` |

**Rule of thumb:** If a bad output reaching users would be a bug, use `Assert`. If it would just be suboptimal, use `Suggest`.

## Migration to dspy.Refine / dspy.BestOfN

Assert/Suggest have been **removed** from DSPy 3.x. All constraint enforcement should use `dspy.Refine` (iterative with feedback) or `dspy.BestOfN` (independent sampling).

The key shift is from inline boolean checks to **reward functions** that score the full output:

```python
# OLD (removed in DSPy 3.x)
dspy.Assert(len(result.answer.split()) <= 50, "Too long")
dspy.Suggest("however" not in result.answer, "Avoid hedging")

# NEW — reward function + Refine
def quality_reward(args, pred):
    score = 1.0
    if len(pred.answer.split()) > 50:      # hard rule
        score -= 0.4
    if "however" in pred.answer.lower():    # soft rule
        score -= 0.1
    return max(score, 0.0)

refined = dspy.Refine(module=my_module, N=3, reward_fn=quality_reward, threshold=0.8)
```

For full migration patterns, see `/dspy-refine` and `/dspy-best-of-n`.

**Verify the migration** by spot-checking your reward function before relying on it in production:

```python
# Confirm reward function returns expected scores
print(quality_reward(None, valid_pred))    # should be >= threshold (e.g., 0.8)
print(quality_reward(None, invalid_pred))  # should be < threshold
```

Then run a sample call through the Refine/BestOfN wrapper and inspect `result` to confirm the output meets your constraints.

## Gotchas

- **Claude writes vague assertion messages like "Invalid output".** The message is injected back into the LM prompt on retry — it IS the feedback. Write actionable instructions: "Summary is {len(words)} words, must be under 50. Remove examples and keep only the key conclusion." The more specific, the more likely the retry succeeds.
- **Claude puts assertions outside `forward()`.** `dspy.Assert` and `dspy.Suggest` only work inside a `dspy.Module.forward()` method because DSPy needs the module context for backtracking. Calling them at the top level or in a standalone function silently skips the retry mechanism.
- **Claude uses `Assert` for style preferences.** Hard assertions that fail after all retries raise `DSPyAssertionError` and crash the program. Use `dspy.Suggest` for subjective quality preferences (tone, style, verbosity) and reserve `Assert` for objective constraints (format validity, safety, schema compliance).
- **Claude does not handle `DSPyAssertionError` at the call site.** When all retry attempts are exhausted, `Assert` raises `DSPyAssertionError`. In production code, always wrap the program call in a try/except to handle validation failures gracefully with a fallback response.
- **Claude chains too many assertions, making all retries fail.** Each assertion that fails triggers a retry with feedback, but stacking 5+ strict assertions means the LM must satisfy all constraints simultaneously. If the success rate per constraint is 80%, five independent constraints yield ~33% joint success. Group related checks into one assertion with a combined message, or relax secondary constraints to `Suggest`.

## Additional resources

- [dspy.Refine API docs](https://dspy.ai/api/modules/Refine/) — recommended replacement for dspy.Assert (iterative improvement with feedback)
- [dspy.BestOfN API docs](https://dspy.ai/api/modules/BestOfN/) — recommended replacement for dspy.Suggest patterns (sample N, pick best)
- [reference.md](reference.md) — Legacy Assert/Suggest signatures, parameters, backtracking behavior, deprecation notes
- Note: the DSPy assertions guide (dspy.ai/learn/programming/7-assertions/) was removed from the docs along with the API in DSPy 3.x

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **dspy.Refine** (iterative improvement with feedback, recommended migration target) — see `/dspy-refine`
- **dspy.BestOfN** (independent sampling, pick best, replaces soft Suggest patterns) — see `/dspy-best-of-n`
- **Problem-first framing** with worked examples — see `/ai-checking-outputs`
- **Stopping hallucinations** with grounding and citations — see `/ai-stopping-hallucinations`
- **Enforcing business rules** and content policies — see `/ai-following-rules`
- **Optimizers** that learn to satisfy constraints — see `/dspy-bootstrap-rs`, `/dspy-miprov2`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
