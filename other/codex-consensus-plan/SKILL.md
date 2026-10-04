---
name: codex-consensus-plan
description: Use when the user wants a decision-complete plan before implementation, especially for code, thesis, experiment, documentation, or workflow changes; produce a native Codex Planner-Architect-Critic consensus plan with ADR, risks, and verification.
---

# Codex Consensus Plan

Create an implementation-ready plan after gathering enough facts. The plan should leave no important decisions to the implementer.

This is the native Codex adaptation of OMX `$ralplan` / `$plan --consensus` as of upstream `oh-my-codex` main `f947e3a`: keep RALPLAN-DR, Planner -> Architect -> Critic discipline, re-review, ADR output, and verification-first handoff; replace `.omx/plans`, `omx question`, and automatic execution handoff with native Codex planning, repo notes, and explicit next-lane recommendations.

## Intake

1. Inspect the relevant repo, docs, configs, task cards, prior decisions, and existing patterns.
2. Identify confirmed facts, assumptions, and unresolved human choices.
3. If ambiguity is still high, run a short `$codex-deep-interview` style pass before planning.
4. Ask only questions that materially change scope, design, risk, or acceptance. If a default is safe, choose it and record it.

## Consensus Loop

Use the roles even when implemented by the main thread. Use native subagents only when they are available and the user/environment supports that workflow.

1. Planner drafts the plan.
   - Right-size the plan to the task; do not force five steps.
   - Include a compact RALPLAN-DR before review.
2. Architect reviews for soundness.
   - Provide the strongest steelman counterargument to the favored option.
   - Name at least one real tradeoff tension.
   - Offer synthesis when possible.
   - For high-risk work, flag principle violations.
3. Critic reviews only after the Architect pass.
   - Check principle-option consistency.
   - Check alternatives were fairly considered.
   - Check risk mitigation clarity.
   - Check testable acceptance criteria and concrete verification.
   - In deliberate/high-risk mode, require a pre-mortem and expanded test plan.
4. Re-review until approved or bounded.
   - If the Critic would reject or iterate, revise and repeat Architect -> Critic.
   - Cap at 5 loops. If consensus is not reached, present the best plan with unresolved objections.

## RALPLAN-DR

Include this compact deliberation summary:

- Principles: 3-5 constraints that should guide the decision.
- Decision drivers: top 3 factors.
- Viable options: at least 2 when possible, with bounded pros/cons.
- Chosen direction: the preferred option and why.
- Rejected alternatives: invalidation rationale when only one option remains.

Use deliberate mode for auth/security, migrations, destructive or irreversible changes, production incidents, compliance/PII, public API breaks, major UX redesigns, or research claims that will become durable decisions.

## ADR

The final plan must include an ADR:

- Decision
- Drivers
- Alternatives considered
- Why chosen
- Consequences
- Follow-ups

## Verification And Handoff

- State exact checks, screenshots, builds, tests, link checks, rendered artifacts, or manual acceptance criteria.
- For UI or visual artifacts, route verification to `$codex-visual-acceptance`.
- For implementation-to-evidence, recommend `$codex-completion-loop`.
- For explicitly parallel work, recommend `$codex-native-subagent-team` with ownership boundaries.
- Do not auto-execute after planning unless the user has separately asked to continue.

## Output Shape

Use a compact plan with:

- Summary
- Context and assumptions
- RALPLAN-DR
- Architect review
- Critic review
- ADR
- Key changes
- Test plan
- Risks and non-goals
- Next lane

When the surrounding mode requires a special plan wrapper, follow that mode's wrapper exactly.

## References

Read `references/plan-rubric.html` for a concise plan quality checklist.
