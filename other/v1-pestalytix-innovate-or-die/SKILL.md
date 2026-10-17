---
name: innovate-or-die
description: Generate, attack, revise, and reality-test non-obvious solutions to difficult problems. Use when the user asks to innovate, rethink a strategy, find unconventional or category-changing opportunities, challenge assumptions, escape generic advice, develop testable hypotheses, or explicitly invokes "Innovate or Die" or `$innovate-or-die`.
---

# Innovate or Die

Turn an ambiguous problem into a small set of valuable, non-obvious hypotheses that survive adversarial review and can be tested.

## Load the method

Read these references completely before starting:

- [principles.md](references/principles.md)
- [innovator.md](references/innovator.md)
- [critic.md](references/critic.md)
- [reviser.md](references/reviser.md)
- [evaluator.md](references/evaluator.md)

Treat the user's request and supplied evidence as authoritative. Gather current evidence with available tools when conclusions depend on changing facts. Label facts, deductions, assumptions, and hypotheses distinctly.

## Run the workflow

1. **Frame the problem.** Identify the desired outcome, stakeholders, hard constraints, inherited constraints, and the conventional answer neighborhood. Ask a question only when missing information would materially change the search.
2. **Innovate.** Follow `references/innovator.md`. Produce a complete internal draft and candidate solution space. Do not anticipate the critic.
3. **Critique independently.** Follow `references/critic.md`. Give the critic only the original request, relevant evidence, and innovator draft. Produce the specified audit; do not rewrite the answer.
4. **Reopen and revise.** Follow `references/reviser.md`. Use the original request, draft, and audit. Search the missing territory rather than merely polishing the draft.
5. **Apply the quality gate.** Follow `references/evaluator.md`. Score every dimension. Pass only when every score is at least 4 and `critical_problems` is empty.
6. **Correct once if needed.** If the answer fails, perform one targeted revision addressing the evaluator's specific deficiencies. Do not change material merely for stylistic variety.
7. **Deliver only the strongest user-facing answer.** Omit internal drafts, audits, scores, and hidden reasoning unless the user explicitly requests them. Include assumptions, causal mechanisms, risks, and falsifiable next tests when they affect the recommendation.

## Preserve independence

For substantial requests, use separate subagents for the Innovator and Critic stages when subagents are available. Keep their contexts isolated as described above. Use additional separate passes for revision and evaluation when useful. If subagents are unavailable, perform clearly separated passes and do not let later criteria shape the initial divergent search.

Never claim that role separation proves correctness. The evaluator is a quality gate, not evidence. Prefer external evidence and small real-world tests over internal consensus.

## Shape the final answer

Lead with the strongest surviving thesis, not a catalog of ideas. Explain why it could work, what must be true, and what would falsify it. Rank alternatives only when the decision benefits from comparison. Allow a strong conventional option to win when unconventional options fail reality checks.
