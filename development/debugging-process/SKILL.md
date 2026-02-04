---
name: debugging-process
description: Provides systematic debugging methodology for thorough root cause analysis with evidence-based investigation. Use this skill when investigating code, analyzing bugs, tracing errors, or understanding unexpected behavior.
---

# Debugging Process

## Instructions

### Core Principles

1. **Real-Time Reporting**: Share findings immediately with `file:line` references. Report "Checking [X] at [location]" → "Found [Y], suggests [Z]"
2. **Root Cause First**: Use 5 Whys technique. Fix the source, not symptoms.

### Investigation Pattern

```
1. "Investigating [X] by checking [Y]"
2. "Found [this] at [location:line]. Suggests [interpretation]"
3. "Based on this, checking [next location]"
4. Root cause identified → Apply fix
```

### Anti-Patterns

- Adding try-catch without understanding why it throws
- Null-checks everywhere instead of understanding cause
- Guessing solutions (e.g., setTimeout hoping it helps)
- Presenting only conclusions without evidence

### DO / DON'T

**DO**: Use `file:line` references, share evidence progressively, trace to origin, explain causal chain

**DON'T**: Rush to fix, hide investigation process, fix symptoms not causes

## Examples

### 5 Whys Example

```
Problem: App crashes on submit
Why? → Exception in validation
Why? → Receives null value
Why? → Form data not initialized
Why? → Component mounts before API response
Why? → Race condition
→ Fix: Correct initialization order
```
