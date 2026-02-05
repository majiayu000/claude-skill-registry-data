---
name: council-debug
description: Use for systematic debugging and root cause analysis with both Codex and Gemini. Triggers on "council debug", "council root cause", "have council investigate this bug", "council find the issue".
---

# Council Debug Skill

Systematic debugging and root cause analysis with both Codex (GPT-5.2) and Gemini.

## When to Use

- Complex bugs requiring investigation
- Mysterious errors or failures
- Performance issues
- Race conditions or timing problems
- When user asks for debugging help from the council

## Reasoning Level

**xhigh** (always - debugging requires deep analysis)

## Execution

1. Gather all relevant context:
   - Error messages
   - Stack traces
   - Relevant code files
   - Logs if available

2. Formulate a debugging prompt:
   ```
   Debug this issue systematically:

   Problem: <description of the bug>

   Error: <error message/stack trace>

   Relevant Code:
   <code snippets>

   Please:
   1. Identify potential root causes
   2. Analyze each possibility
   3. Determine the most likely cause
   4. Suggest a fix
   ```

3. Run **BOTH** commands in parallel:

   **Codex:**
   ```bash
   codex exec --sandbox read-only -c model_reasoning_effort="xhigh" "<prompt>"
   ```

   **Gemini:**
   ```bash
   gemini -s -y -o json "<prompt>"
   ```

4. Synthesize debugging insights

## Response Format

```markdown
## AI Council Debug Report

### Codex (GPT-5.2) Diagnosis:
**Potential Causes:**
1. [Cause with likelihood]
2. [Cause with likelihood]

**Root Cause Analysis:**
[Detailed analysis]

**Suggested Fix:**
[Code or steps to fix]

---

### Gemini Diagnosis:
**Potential Causes:**
1. [Cause with likelihood]
2. [Cause with likelihood]

**Root Cause Analysis:**
[Detailed analysis]

**Suggested Fix:**
[Code or steps to fix]

---

### Council Synthesis:
**Agreed Root Cause:** [If both agree]
**Conflicting Theories:** [If they differ]
**Recommended Fix:** [Synthesized fix strategy]
**Confidence Level:** [Based on agreement]

---
*Session IDs: Codex=[id], Gemini=[id]*
```
