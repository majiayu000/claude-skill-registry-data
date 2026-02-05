---
name: council-thinkdeep
description: Use for deep multi-step investigation and analysis with both Codex and Gemini. Triggers on "council deep analysis", "investigate with council", "council thorough investigation", "have the council think deeply".
---

# Council ThinkDeep Skill

Multi-step investigation and deep reasoning with both Codex (GPT-5.2) and Gemini using extra-high reasoning.

## When to Use

- Complex problems requiring step-by-step analysis
- Architecture decisions
- Performance deep-dives
- Security analysis
- When user asks for "deep", "thorough", or "comprehensive" council analysis

## Reasoning Level

**xhigh** (always - this skill is for deep analysis)

## Execution

1. Understand the problem fully
2. Gather all relevant files and context
3. Formulate a structured prompt:
   ```
   Investigate this step by step. Form hypotheses, test them, and build confidence.

   Question: <user's question>

   Context:
   <relevant file contents>

   Please:
   1. Break down the problem
   2. Form initial hypotheses
   3. Analyze each hypothesis
   4. Reach a well-reasoned conclusion
   ```

4. Run **BOTH** commands in parallel:

   **Codex:**
   ```bash
   codex exec --sandbox read-only -c model_reasoning_effort="xhigh" "<prompt>"
   ```

   **Gemini:**
   ```bash
   gemini -s -y -o json "<prompt>"
   ```

5. Synthesize the comprehensive analyses

## Response Format

```markdown
## AI Council Deep Analysis

### Codex (GPT-5.2) Analysis:
**Problem Breakdown:**
[Step-by-step analysis]

**Hypotheses Explored:**
[Each hypothesis and findings]

**Conclusion:**
[Final recommendation with confidence level]

---

### Gemini Analysis:
**Problem Breakdown:**
[Step-by-step analysis]

**Hypotheses Explored:**
[Each hypothesis and findings]

**Conclusion:**
[Final recommendation with confidence level]

---

### Council Synthesis:
**Shared Insights:** [What both models discovered]
**Unique Perspectives:** [Insights unique to each model]
**Combined Recommendation:** [Synthesized recommendation]
**Confidence:** [High/Medium/Low based on agreement]

---
*Session IDs: Codex=[id], Gemini=[id]*
```
