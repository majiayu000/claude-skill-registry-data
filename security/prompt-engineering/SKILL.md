---
name: prompt-engineering
description: Design and evaluate prompts or LLM workflows on representative tasks. Triggers on "prompt engineering", "提示词工程".
---

# Prompt Engineering

## When to use

- Design and evaluate prompts or LLM workflows on representative tasks.

**Not for:** skill-authoring for skills; research for model comparisons.

## Steps

1. Define inputs, expected outcomes, trust boundaries, failure costs and representative cases.

2. Establish the existing baseline; add minimal instructions addressing observed gaps and verify current provider behavior.

3. Specify output validation and actual tool permissions, budgets and termination; prompt text alone is not a security boundary.

4. Run representative and adversarial cases; compare quality, latency and cost and report limitations.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/design/PROMPT.md` for a maintained workflow.

## Verify

- Revisions have a stated baseline and rubric; invalid output and untrusted input are handled and unrun cases are explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/prompt-architecture.md](references/prompt-architecture.md) — prompt component breakdown, few-shot patterns, structured-output techniques, model selection matrix, eval-harness setup, guardrail catalog
