---
name: council-consensus
description: Use for multi-perspective analysis with both Codex and Gemini exploring different viewpoints. Triggers on "council perspectives", "pros and cons from council", "council evaluate options", "what are the tradeoffs", "council consensus".
---

# Council Consensus Skill

Multi-perspective analysis with both Codex and Gemini, each exploring for/against/neutral viewpoints for comprehensive evaluation.

## When to Use

- Evaluating technology choices
- Architecture decisions
- Trade-off analysis
- When user needs pros and cons
- Comparing different approaches
- Decision-making support

## Reasoning Level

**high** (default for balanced analysis)

## Execution

1. Identify the topic/question for consensus
2. Gather relevant context

3. For each model, request stance-based analysis:
   ```
   Analyze this topic from multiple perspectives:

   Topic: <topic or decision>

   Please provide:
   1. **FOR** arguments - Best case for this approach
   2. **AGAINST** arguments - Concerns and risks
   3. **NEUTRAL** assessment - Objective analysis
   4. **Recommendation** - Your balanced conclusion
   ```

4. Run **BOTH** commands in parallel:

   **Codex:**
   ```bash
   codex exec --sandbox read-only -c model_reasoning_effort="high" "<prompt>"
   ```

   **Gemini:**
   ```bash
   gemini -s -y -o json "<prompt>"
   ```

5. Synthesize multi-model, multi-perspective analysis

## Response Format

```markdown
## AI Council Consensus Analysis

### Codex (GPT-5.2) Perspectives:

**FOR:**
- [Pro arguments]

**AGAINST:**
- [Con arguments]

**NEUTRAL:**
- [Objective observations]

**Recommendation:** [Codex's conclusion]

---

### Gemini Perspectives:

**FOR:**
- [Pro arguments]

**AGAINST:**
- [Con arguments]

**NEUTRAL:**
- [Objective observations]

**Recommendation:** [Gemini's conclusion]

---

### Council Consensus:

**Unanimous FOR:** [Points both models agree are advantages]

**Unanimous AGAINST:** [Concerns both models share]

**Divergent Views:** [Where the models disagree]

**Cross-Model Insights:**
- [Unique insights from combining perspectives]

**Council Recommendation:**
[Synthesized recommendation based on all perspectives from both models]

**Confidence Level:** [High if both agree, Medium if partial agreement, Low if divergent]

---
*Session IDs: Codex=[id], Gemini=[id]*
```
