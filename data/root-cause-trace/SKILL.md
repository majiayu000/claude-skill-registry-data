---
name: root-cause-trace
description: Use when errors occur deep in execution and you need to trace back to the original trigger. Applies 5-step investigation — observe, hypothesize, trace backwards, binary search, prove.
---

# Root Cause Tracing

> ultrathink — use extended reasoning for root cause analysis.

## Process

### 1. Observe — Gather All Evidence
- Read the **full error message** and stack trace
- Check logs at multiple levels (application, database, message broker)
- Note the **exact** error, not a paraphrase
- Determine: is this error the root cause, or a symptom?

### 2. Hypothesize — Form Multiple Theories
- Generate at least 3 possible root causes
- Rank by probability based on the evidence
- Consider: timing, data flow, state mutations, race conditions

### 3. Trace Backwards
- Start from the error location
- Walk the call chain backwards through the code
- At each step, verify: is the data correct here? Where did it come from?

### 4. Isolate — Binary Search
- If the trace is long, check the midpoint
- Is the data correct at the midpoint? → Problem is downstream
- Is the data wrong at the midpoint? → Problem is upstream
- Narrow until you find the exact point where data goes wrong

### 5. Verify — Prove the Root Cause
- Can you reproduce the error with specific input?
- Does fixing the identified root cause prevent the error?
- Are there other code paths that could trigger the same issue?

## Anti-Patterns
- ❌ **Don't guess** — trace with evidence
- ❌ **Don't fix symptoms** — find the root cause
- ❌ **Don't assume "it works on my machine"** — check environment differences
- ❌ **Don't add try/catch to silence errors** — fix the cause

