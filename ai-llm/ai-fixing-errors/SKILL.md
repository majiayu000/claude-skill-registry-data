---
name: ai-fixing-errors
description: Fix broken AI features. Use when your AI is throwing errors, producing wrong outputs, crashing, returning garbage, not responding, or behaving unexpectedly. Also use when you get Could not parse LLM output errors, DSPy program crashes, LLM timeout or rate limit errors, API key not working with DSPy, JSON parse error from LLM, model returns empty response, AI works sometimes but fails other times, intermittent LLM failures, debug DSPy pipeline, context window exceeded, token limit error, AI feature stopped working overnight, production AI errors.
---

# Fix Your Broken AI

Systematic approach to diagnosing and fixing AI features that aren't working.

## Step 1 — Gather context

Before debugging, ask the user:

1. What error message or unexpected behavior are you seeing? (paste the traceback or describe the output)
2. Did this work before, or is it a new feature that has never worked?
3. Are you using an optimizer, or is this a zero-shot / few-shot program?
4. What LM provider and model are you using?

## Step 2 — Quick Diagnostic Checklist

### 1. Is the AI provider configured?

```python
import dspy

# Check current config
print(dspy.settings.lm)  # Should show your LM, not None

# If None, configure it:
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)
```

**Common issues:**
- Forgot to call `dspy.configure(lm=lm)`
- API key not set in environment
- Wrong model name format (should be `provider/model-name`)

### 2. Does the AI respond at all?

```python
# Test the AI provider directly
lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
response = lm("Hello, respond with just 'OK'")
print(response)
```

### 3. Is the task definition correct?

```python
# Check your signature defines the right fields
class MySignature(dspy.Signature):
    """Clear task description here."""
    input_field: str = dspy.InputField(desc="what this contains")
    output_field: str = dspy.OutputField(desc="what to produce")

# Verify by inspecting
print(MySignature.fields)
```

**Common issues:**
- Missing `dspy.InputField()` / `dspy.OutputField()` annotations
- Wrong type hints (use `str`, `list[str]`, `Literal[...]`, Pydantic models)
- Vague or missing docstring (the docstring IS the task instruction)

### 4. Are you passing the right inputs?

```python
# Check that input field names match
result = my_program(question="test")  # field name must match signature

# Wrong:
result = my_program(q="test")  # 'q' doesn't match 'question'
result = my_program("test")    # positional args don't work
```

### 5. Is the output being parsed?

```python
result = my_program(question="test")
print(result)                    # see all fields
print(result.answer)             # access specific field
print(type(result.answer))       # check type
```

**Common issues with typed outputs:**
- `Literal` type doesn't match any of the provided options
- Pydantic model validation fails
- List output returns string instead of list

## Inspect What the AI Actually Sees

The most powerful debugging tool — shows exactly what prompts were sent and what came back:

```python
# Show the last 3 AI calls
dspy.inspect_history(n=3)
```

This shows:
- The full prompt sent to the AI
- The AI's raw response
- How DSPy parsed the response

**What to look for:**
- Is the prompt clear? Does it describe the task well?
- Is the AI's response in the expected format?
- Are few-shot examples (if any) helpful or misleading?

## Common Errors and Fixes

### `AttributeError: 'NoneType' has no attribute ...`
**Cause:** AI provider not configured.
**Fix:** Call `dspy.configure(lm=lm)` before using any module.

### `ValueError: Could not parse output`
**Cause:** AI output doesn't match expected format.
**Fix:**
- Check `dspy.inspect_history()` to see what the AI returned
- Simplify your output types
- Add clearer field descriptions
- Use `dspy.ChainOfThought` instead of `dspy.Predict` (reasoning helps formatting)

### `TypeError: forward() got an unexpected keyword argument`
**Cause:** Input field name mismatch.
**Fix:** Make sure you're passing keyword arguments that match your signature's `InputField` names.

### Search/retriever returns empty results
**Cause:** Retriever not configured or wrong endpoint.
**Fix:**
```python
# Test retriever directly
rm = dspy.ColBERTv2(url="http://...")
results = rm("test query", k=3)
print(results)

# Or if using a custom retriever function, call it directly to verify
```

### Optimizer makes things worse
**Cause:** Bad metric, too little data, or overfitting.
**Fix:**
- Manually verify your metric on 10-20 examples
- Add more training data
- Reduce `max_bootstrapped_demos`
- Use a validation set to check for overfitting

### `dspy.Refine` not meeting threshold / exhausting attempts
**Cause:** Reward function threshold is too strict, or the module cannot produce outputs that score high enough.
**Fix:**
- Check if the threshold is realistic for your graduated reward function (e.g., `0.8` rather than `1.0` for multi-criteria scoring)
- Make the reward function more descriptive by returning partial scores rather than binary 0/1
- Ensure the module can reasonably produce outputs that satisfy the reward criteria
- Increase `N` to give more retry attempts, or use `dspy.BestOfN` for independent sampling

## Advanced Debugging

### Enable verbose tracing

DSPy records all LM calls automatically. Run your program, then inspect:

```python
result = my_program(question="test")
dspy.inspect_history(n=5)  # shows every prompt + response in order
```

For structured logging or production-level tracing, see `/ai-tracing-requests`.

### Inspect module structure

```python
# Print the module tree
print(my_program)

# See all named predictors
for name, predictor in my_program.named_predictors():
    print(f"{name}: {predictor}")
```

### Test individual components

Break your pipeline into pieces and test each one:

```python
class MyPipeline(dspy.Module):
    def __init__(self):
        self.step1 = dspy.ChainOfThought("question -> search_query")
        self.step2 = dspy.Retrieve(k=3)
        self.step3 = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        query = self.step1(question=question)
        print(f"Step 1 output: {query.search_query}")  # Debug

        context = self.step2(query.search_query)
        print(f"Step 2 retrieved: {len(context.passages)} passages")  # Debug

        answer = self.step3(context=context.passages, question=question)
        print(f"Step 3 output: {answer.answer}")  # Debug

        return answer
```

### Compare prompts before/after optimization

```python
# Before optimization
baseline = MyProgram()
baseline(question="test")
print("=== BASELINE PROMPT ===")
dspy.inspect_history(n=1)

# After optimization
optimized = MyProgram()
optimized.load("optimized.json")
optimized(question="test")
print("=== OPTIMIZED PROMPT ===")
dspy.inspect_history(n=1)
```

## Gotchas

- **Jumping to code changes before reading `dspy.inspect_history()`.** Claude tends to guess at fixes based on the error message alone. Always inspect the actual prompt and response first — the root cause is usually visible in the raw LM output (wrong format, truncated response, misunderstood instruction).
- **Treating parse errors as LM problems when they are signature problems.** When DSPy cannot parse the output, Claude often tries switching models or adding retry logic. The real fix is usually to simplify the output type, add field descriptions, or switch from `Predict` to `ChainOfThought` so the model has space to reason before producing structured output.
- **Rewriting the whole program instead of isolating the broken component.** Claude tends to refactor everything when one step fails. Test each predictor in the pipeline individually by calling it directly — the bug is typically in one specific step.
- **Adding `try/except` around DSPy calls to swallow errors.** This hides the real problem. DSPy errors (especially `ValueError` from parsing) are diagnostic — they tell you exactly what the LM returned vs what was expected. Fix the root cause instead of catching and retrying.
- **Forgetting that optimized programs load stale demos.** When a program worked before but breaks after changes, Claude often misses that `.load()` restores old few-shot demos that no longer match the current signature. Re-optimize or clear the saved state after signature changes.

## When NOT to use this skill

- **No errors, just low accuracy** — use `/ai-improving-accuracy` instead. This skill fixes crashes and parse failures, not quality problems.
- **Need to set up a new AI feature from scratch** — use `/ai-do` to get routed to the right building skill. This skill assumes you already have code that is broken.
- **Performance or cost issues without errors** — use `/ai-cutting-costs` or `/ai-making-consistent` depending on the problem.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Measure and improve accuracy after fixing errors — see `/ai-improving-accuracy`
- Trace a specific request end-to-end (every LM call, retrieval, latency) — see `/ai-tracing-requests`
- Monitor AI in production to catch errors early — see `/ai-monitoring`
- Understand DSPy modules (Predict, ChainOfThought, ReAct) — see `/dspy-modules`
- Iterative output refinement with feedback — see `/dspy-refine`
- Sample N outputs and pick the best — see `/dspy-best-of-n`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples and debugging walkthroughs, see [examples.md](examples.md)
- For complete error index, see [reference.md](reference.md)
