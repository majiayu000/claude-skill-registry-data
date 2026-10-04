---
name: debug
description: Systematic root-cause analysis for bugs, errors, and unexpected behavior
triggers:
  - debug this
  - why is this failing
  - root cause
  - investigate
  - ultradebug
---

# Debug

Systematic 7-step debugging. Don't guess — trace.

## Steps

1. **Reproduce** — get a minimal, reliable reproduction
2. **Locate** — find the exact file, line, and call path where it breaks
3. **Hypothesize** — list 2-3 competing explanations
4. **Evidence** — for each hypothesis: what would confirm or rule it out
5. **Test** — run the fastest confirming/ruling test first
6. **Fix** — change exactly what the evidence points to
7. **Verify** — confirm fix resolves the issue, run full test suite

## Rules

- Never change code before you know the root cause
- Read the actual error message — don't skim it
- Check assumptions: is the value what you think it is? Add a log
- Distinguish "symptom" from "cause" — fix the cause
- If stuck after 3 hypotheses, add instrumentation before guessing more

## Output

```text
Root cause: <one sentence>
Location:   <file>:<line>
Fix:        <what to change and why>
```
