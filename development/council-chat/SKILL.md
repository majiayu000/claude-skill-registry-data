---
name: council-chat
description: Use when user wants to ask the AI council a question, get multiple AI perspectives, or consult with both Codex and Gemini. Triggers on phrases like "ask council", "council opinion", "what do the AIs think", "ask both models".
---

# Council Chat Skill

General consultation with both Codex (GPT-5.2) and Gemini for questions, opinions, and analysis.

## When to Use

- User asks for the council's opinion
- User wants multiple AI perspectives
- User explicitly mentions "council" or "both models"
- User asks for consultation on a technical question

## Reasoning Level

Default: **high**

If user mentions "quick" or "brief", use medium.
If user mentions "deep" or "thorough", use xhigh.

## Execution

1. Identify the question or topic
2. Gather relevant context (read files if needed)
3. Run **BOTH** commands in parallel:

   **Codex:**
   ```bash
   codex exec --sandbox read-only -c model_reasoning_effort="high" "<question with context>"
   ```

   **Gemini:**
   ```bash
   gemini -s -y -o json "<question with context>"
   ```

4. Collect both responses
5. Synthesize into unified response

## Response Format

```markdown
## AI Council Response

### Codex (GPT-5.2) Says:
[Codex's analysis]

### Gemini Says:
[Gemini's analysis]

### Council Synthesis:
**Agreement:** [Points both models agree on]
**Divergence:** [Where they differ]
**Recommendation:** [Synthesized recommendation based on both]

---
*Session IDs: Codex=[id], Gemini=[id]*
```
