---
name: recursive-thinking
description: Adversarial review workflow for pressure-testing an existing candidate plan, diagnosis, design, argument, proposal, or recommendation. Use when the user asks to challenge its assumptions, run a premortem, play devil's advocate, red-team a non-security decision, or identify what would change the conclusion. Do not use for open-ended exploration (use thinking) or exploit-focused security review (use security as primary).
---

# Recursive Thinking

Challenge an existing candidate hard enough to improve, qualify, or reject it before action.

Use this as an orthogonal workflow skill alongside the relevant domain or repository skills. It can be invoked directly whenever a candidate exists; a prior **thinking** pass is not required. If no candidate exists, use **thinking** to frame the decision first.

This workflow produces a concise, evidence-based audit trail. It does not require a step-by-step reasoning transcript.

## Routing boundaries

- Use **security** as primary when red-teaming means exploit discovery, abuse paths, authentication, authorization, secrets, or trust boundaries.
- Use **tester-mindset** as primary when the main artifact is a test strategy, oracle, or edge-case inventory.
- Keep language, backend, UI, documentation, prompt, and story skills primary for reviews of their artifacts; add this workflow only when adversarial pressure-testing is materially useful.
- Do not use this for simple lookups, routine execution, or open-ended idea generation.

## Optional `n`

If the user supplies `n`, treat it as the maximum number of distinct challenge lenses, not recursion depth. Do not ask for `n`, invent a default, or expand weak branches to satisfy the count. Without `n`, use only as many lenses as the decision needs.

## Grounding

Keep conclusions, evidence, and assumptions distinguishable. Apply labels only where they clarify a material claim:

- **Observed:** directly supported by a cited source, file, test, log, or supplied fact.
- **Inferred:** derived from observations plus a named assumption.
- **Unknown:** unresolved, with the evidence that would resolve it.

For diagnosis and review, cite concrete evidence. For strategy or design, state verification or falsification conditions for the most important assumptions. Do not convert plausibility into observation.

## Workflow

1. **Define the candidate and success target.** State what is being challenged and what a better outcome means.
2. **Inspect the evidence.** Gather relevant artifacts, constraints, tests, history, and domain guidance before critiquing.
3. **Choose distinct challenge lenses.** Cover only material angles such as objective mismatch, hidden assumptions, contrary evidence, alternatives, failure modes, incentives, interfaces, reversibility, or verification. Include at least one strong countercase to the current conclusion.
4. **Select high-yield probes.** Prioritize questions likely to change confidence, the recommendation, the next action, or the validation plan. Replace repetitive or cosmetic questions.
5. **Deepen selectively.** Probe with the most useful form of `why`, `how`, `what evidence`, `what fails`, `what trade-off`, or `what would change the conclusion`. Continue only while another probe could produce a decision-relevant delta.
6. **Reconcile the result.** Name contradictions instead of smoothing them over. State which assumptions survived, weakened, or failed and whether the candidate should proceed, change, wait for evidence, or be rejected.
7. **Recommend the next action.** Give the smallest action that addresses the strongest concern, plus what should not happen yet.

## Stop rule

Stop when another probe is unlikely to change confidence, the recommendation, the next action, or the evidence needed. A single decisive failure can end a branch; no minimum depth is required.

## Output

Lead with the result, not the question tree:

1. **Verdict** — proceed, revise, gather evidence, or reject, with a confidence basis.
2. **Strongest countercase** — the best argument against the candidate.
3. **Material findings** — evidence, assumptions, contradictions, and failure modes that changed the assessment.
4. **What would change the conclusion** — decisive missing evidence or thresholds.
5. **Next action** — what to do and what not to do yet.

When the user explicitly requests `n`, include no more than `n` distinct findings or lenses. Show deeper question-and-answer branches only when the user asks for that presentation.

## Avoid

- mechanical question trees or repeated rephrasings
- confirmation deepening that only defends the initial candidate
- authority laundering that labels inference as observation
- false precision in confidence claims
- generic philosophy disconnected from evidence or action
- replacing a specialized domain review with a generic red-team pass
