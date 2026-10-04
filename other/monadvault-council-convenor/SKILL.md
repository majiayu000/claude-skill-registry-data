---
name: monadvault-council-convenor
description: "Design and synthesize MonadVault councils across multiple models, expert roles, or engaged Monads. Use when a Steward asks for a council, panel, debate, independent second opinions, devil's-advocate review, multiple perspectives on a decision, member roles and prompts, preserved dissent, a synthesis rubric, a chair summary, or privacy and budget guardrails for a multi-participant run."
---

# MonadVault Council Convenor

## Overview

Use this skill to design a Council run before spending tokens or invoking external participants. The goal is independent perspective, not a louder single answer.

## Routing

- Use this skill for council membership, independent prompts, dissent, and synthesis design.
- Use `monadvault-cost-route-planner` when the main question is whether a council is affordable or necessary.
- Use `monadvault-privacy-sentinel` when member context may expose sensitive information.

## Workflow

1. Frame the decision or question in one paragraph.
2. Decide if a Council is warranted. Use a single route for simple drafting, extraction, or low-stakes brainstorming.
3. Select council type:
   - model council for multiple model perspectives
   - role council for simulated lenses
   - engaged Monad council when the Steward has active access and terms permit it
4. Assign members clear jobs: strategist, skeptic, privacy reviewer, domain specialist, implementer, or chair.
5. Write member prompts that avoid leaking other members' answers before independence is complete.
6. Define synthesis rules:
   - what consensus means
   - what dissent must be preserved
   - what evidence is required
   - what the chair may decide
7. Add cost and privacy guardrails before execution.

## Output Contract

Return:

- `Council question`
- `Why council`
- `Members`
- `Independent prompts`
- `Synthesis rubric`
- `Budget guardrails`
- `Privacy guardrails`
- `Final chair prompt`

Use [council-run-template.md](references/council-run-template.md) for a runnable prompt pack.

## Guardrails

- Do not convene external or engaged Monads unless access and permissions are explicit.
- Do not include private memory in all member prompts by default; scope context per member.
- Preserve minority warnings instead of averaging them away.
- Ask for a cost estimate when the requested council may be expensive.
