---
name: intent-brief
description: Evidence-first intent elicitation. Scouts before asking, assumes visibly, grills only one-way doors, ends in a commander's-intent brief.
disable-model-invocation: true
---

Elicit my intent with minimal interrogation; my attention is the scarce resource.

1. Reconnoitre before asking: codebase precedent, git history, ADRs and CONTEXT.md, prior conversations, upstream docs, the web. Facts and precedent are yours to find; only preferences and values are mine.
2. Present an assumption ledger. Default on two-way doors; management by exception, silence is consent.
3. Grill only one-way doors with high value of information, in dependency order, one at a time. The decision surface the reconnaissance reveals sets how many there are. Each with recommendation, confidence, strongest alternative, evidence. Prefer a concrete exemplar (edge case, signature, mock) to an abstract question. Defer the rest to the last responsible moment.
4. Run a brief pre-mortem.
5. Stop when residual VOI is negligible. Emit a commander's-intent brief: purpose, end state, constraints, no-gos, key decisions (one-way doors as ADRs), accepted assumptions, open questions, risks.

Do not act until I confirm the brief.
