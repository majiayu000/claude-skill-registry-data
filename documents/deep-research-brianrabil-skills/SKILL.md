---
name: plan-mode-deep-research
description: Investigate a consequential or contested question across multiple primary sources. Use when a quick lookup is insufficient because evidence conflicts, versions differ, or the decision depends on several linked claims.
license: MIT
---

# Deep Research

Build a defensible answer, including the evidence that challenges it.

1. Break the decision into questions and record what would confirm or overturn each likely answer. Set the relevant time window, versions, platforms, and source boundaries before searching.
2. Gather primary evidence for every question. Follow documentation into release notes, code, issue discussions, or original data when needed. Record source date and applicability; do not count repeated summaries of one source as independent support.
3. Seek counterexamples and competing explanations. Reconcile conflicts using version, environment, methodology, and source authority. If reconciliation fails, preserve the disagreement and state what observation would settle it.
4. Present the conclusion, an evidence table or concise claim-to-source map, alternatives considered, confidence, and unresolved gaps. Finish only when each decision-critical claim is supported, refuted, or clearly unresolved.

Keep this investigation read-only unless the user separately authorizes changes. If one official page answers the question, use `plan-mode-research` or `plan-mode-read-docs` instead.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
