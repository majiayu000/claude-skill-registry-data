---
name: python-debug
description: Debug Python code using tracebacks, pdb, and structured logging.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: debugging
  since: "2025-02-24"
---

## What I do

I guide you through three core Python debugging workflows:
1. **Reading tracebacks** — parse the error, find the root cause, identify common exception types
2. **Interactive debugging with pdb** — set breakpoints, step through execution, inspect state
3. **Structured logging** — configure logging for visibility in tests and production

A reusable logging configuration template is available in `assets/logging_config.py`.

## When to use me

Use when you:
- See an unexpected exception and need to find the root cause
- Want to step through execution to understand what's happening
- Need to add logging to a module for ongoing observability
- Are setting up debugging infrastructure for a new project

## Example usage

"Help me read this traceback and find what's causing the KeyError"
"Set a breakpoint before the loop in `process_items` and inspect each item"
"Add structured logging to `src/services/payment.py`"

## How to respond

- **Tracebacks**: identify root cause first, then walk the relevant frames — don't narrate the whole stack
- **pdb**: show the minimal breakpoint placement and the commands needed for the specific situation — don't dump the full command reference
- **Logging**: write the actual config for the target module; offer to apply `assets/logging_config.py` if they need a reusable setup

## Debugging workflow

### 1. Problem analysis
- Identify the specific exception or erroneous output and location
- Confirm expected vs actual behavior before diving into code
- Trace the execution flow (call stack, async context) to locate the breakpoint

### 2. Debugging strategy
- Add targeted logging statements or instrument the offending function
- Use `pdb.set_trace()` or `breakpoint()` just before key transitions
- Inspect relevant state (locals, instance attributes) without overwhelming output
- Suggest tooling like `pytest -k <test>` with `-vv` or `python -m pdb` as needed

### 3. Solution approach
- Outline possible fixes, describe trade-offs (performance, readability, backward compatibility)
- Reference specific modules, classes, or helpers that need the change
- Provide clear before/after snippets and explain why the fix resolves the failure

### 4. Prevention
- Recommend additional tests that exercise the fixed path (unit, integration, regression)
- Suggest alerting/logging improvements to detect similar issues earlier
- Highlight architectural changes (e.g., safer defaults, input validation) to avoid repeats
- Identify any code smells uncovered during debugging (hidden state, silent failures)

## Debug checklist
- [ ] Established expected vs actual behavior
- [ ] Traced execution flow to locate the root cause
- [ ] Recommended logging/breakpoints to observe the failure
- [ ] Proposed concrete fix(es) with trade-off analysis
- [ ] Added prevention steps (tests, logging, validation) to avoid regressions
