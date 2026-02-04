---
name: codex-debug
description: Use for systematic debugging and root cause analysis with Codex. Triggers on "codex debug", "codex root cause", "have codex investigate this bug", "codex find the issue".
---

# Codex Debug Skill

Systematic debugging and root cause analysis with Codex (gpt-5.2).

## When to Use

- Debugging complex bugs
- Finding root causes of issues
- Investigating mysterious errors
- Performance issue diagnosis
- Race conditions or timing issues

## Reasoning Level

**xhigh** (debugging requires deep analysis)

## Execution

1. Gather all relevant information:
   - Error messages
   - Stack traces
   - Relevant code files
   - Reproduction steps
2. Formulate a debugging prompt:
   ```
   Debug this issue systematically.

   Issue: <description>

   Error/Symptoms:
   <error messages, behavior>

   Relevant Code:
   <file contents>

   Please:
   1. Identify possible causes
   2. Analyze each potential root cause
   3. Determine the most likely cause
   4. Suggest a fix
   ```
3. Run: `codex exec -c model_reasoning_effort="xhigh" "<prompt>"`
4. Return the debugging analysis with fix recommendation

## Response Format

```
**Codex Debug Analysis:**

**Issue Summary:**
[What's happening]

**Root Cause Investigation:**
[Step-by-step analysis of potential causes]

**Most Likely Cause:**
[Primary hypothesis with evidence]

**Recommended Fix:**
[Specific fix with code if applicable]

**Session ID:** [id]
```
