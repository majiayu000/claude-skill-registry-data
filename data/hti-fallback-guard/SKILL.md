---
name: hti-fallback-guard
description: In this repo, avoid sloppy fallback logic. Prefer explicit failures, narrow error handling, and clearly marked TODOs over fake success paths.
---

# HTI Fallback & Failure Handling

This Skill defines how to handle errors and "fallback" behavior in the **hti-zen-harness** project.

## Core Principles

When working in this repo:

1. **No fake success.**
   - Do **not** hide failures behind:
     - Silent `except Exception: pass`
     - Returning empty objects (`{}`, `[]`) or dummy values as if things worked
     - Swallowing errors and logging nothing
   - If something *really* cannot be implemented yet, mark it explicitly as such.

2. **Prefer explicit failure over magical fallback.**
   - It is *better* to:
     - Raise a clear, specific exception, or
     - Return an explicit error result / `Result`-style object
   - ...than to pretend everything is fine.

3. **Be narrow and honest with error handling.**
   - Catch **specific** exceptions (e.g., `requests.Timeout`, `ValueError`), not blanket `Exception`, unless there is a very strong reason.
   - When catching an exception, do at least one of:
     - Log it with clear context, OR
     - Re-raise it, OR
     - Convert it into a clearly named error type / return value.

4. **No "mystery fallback" branches.**
   - Avoid patterns like:
     ```python
     def get_config():
         try:
             return load_from_disk()
         except Exception:
             return {}
     ```
   - Instead, make the failure *visible*:
     ```python
     def get_config():
         try:
             return load_from_disk()
         except FileNotFoundError as e:
             raise ConfigMissingError("Config file not found") from e
     ```

## Approved Alternatives to Bad Fallbacks

When you feel tempted to add "just in case" fallback logic, use one of these patterns instead:

### 1. Explicit TODO with loud marker

If something truly can't be implemented yet:

```python
def fetch_remote_status():
    # HTI-TODO: Implement real remote status fetching.
    raise NotImplementedError("fetch_remote_status is not yet implemented for HTI harness")
```

**Guidelines:**
- Use `HTI-TODO` in comments to make search/refactoring easier.
- Do not silently return a fake value.

### 2. Logged error + re-raise

When you want extra context but don't want to hide the failure:

```python
def run_harness_step():
    try:
        return do_step()
    except HarnessStepError as e:
        logger.error("Harness step failed: %s", e)
        raise
```

### 3. Structured, explicit error result

If the calling code already uses structured results:

```python
@dataclass
class StepResult:
    ok: bool
    error: str | None = None
    data: dict[str, Any] | None = None

def run_harness_step() -> StepResult:
    try:
        data = do_step()
        return StepResult(ok=True, data=data)
    except HarnessStepError as e:
        return StepResult(ok=False, error=f"harness step failed: {e}")
```

**Rules:**
- Never set `ok=True` when something actually failed.
- Call sites should check `ok` and handle errors explicitly.

## When You Think You "Need" a Fallback

Before adding fallback code, follow this checklist:

1. **Ask: what is the correct behavior if this fails?**
   - Crash fast and loudly?
   - Retry?
   - Skip this step but continue others?

2. **If there is genuine choice, do one of:**
   - Briefly outline 2–3 options in your response and pick the safest one by default.
   - Only ask the user when the choice meaningfully affects behavior or safety.

3. **Document the behavior.**
   - If you add a fallback, document:
     - When it triggers
     - What it does
     - Why this is acceptable in HTI/Zen context

**Example:**

```python
def run_analysis():
    """
    Run analysis for the HTI Zen harness.

    Failure behavior:
      - If the upstream model call fails, we raise a clear error.
      - We do NOT silently fallback to dummy data.
    """
    ...
```

## Patterns to Avoid in This Repo

Claude should avoid generating code like:

```python
# BAD: silent swallowing
try:
    result = call_model(prompt)
except Exception:
    result = {"status": "ok"}  # Pretend success

# BAD: vague TODO fallback in production path
if not result:
    # TODO: handle better
    return {}
```

Or:

```python
# BAD: doing something random "just to return something"
def pick_model():
    try:
        return pick_best_model()
    except Exception:
        return "gpt-5"  # arbitrary default with no explanation
```

## Interaction with Testing

When writing or updating tests in this repo:

- **Prefer tests that prove we're not silently falling back.**

**Example patterns:**
- Assert that an invalid config raises a specific error.
- Assert that missing dependencies cause clear failures, not silent no-ops.
- If a fallback exists, add a test that triggers it and confirms:
  - It's documented
  - It's safe
  - It's clearly distinguishable from the normal path.

## How to Use This Skill

**Claude:**

When editing code in `hti-zen-harness`, load and follow these guidelines whenever:
- You add error handling
- You touch network / API / MCP calls
- You consider "best-effort" or "fallback" behavior

If a user asks you to "just make it work even if X fails,":
1. Explain briefly what trade-off you're making
2. Choose explicit, debuggable behavior over silent fallbacks
3. Use `HTI-TODO` markers when something is intentionally left incomplete
