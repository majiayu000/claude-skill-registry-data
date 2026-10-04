---
name: cloud-arch
description: "Multi-account patterns, networking, and well-architected trade-offs. Use when designing cloud systems."
---

# Cloud Arch

Structured guidance for **cloud architecture** (accounts, networking, well-architected trade-offs): confirm triggers, propose the stages below, and adapt if the user wants a lighter pass.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions **cloud architecture** or closely related work
- They want a structured workflow rather than ad-hoc tips
- They are preparing a review, rollout, or stakeholder communication

**Initial offer:**
Explain the four stages briefly and ask whether to follow this workflow or work freeform. If they decline, continue in their preferred style.

## Workflow Stages

### Stage 1: Clarify context & goals

Anchor on **accounts, networking, identity**. Ask what success looks like, constraints, and what must not break. Capture unknowns early.

### Stage 2: Design or plan the approach

Translate goals into a concrete plan around **data and encryption**. Compare alternatives and explicit trade-offs; avoid implicit assumptions.

### Stage 3: Implement, validate, and harden

Execute with verification loops tied to **scalability patterns**. Prefer small steps, measurable checks, and rollback points where risk is high.

### Stage 4: Operate, communicate, and iterate

Close the loop with **operational model**: monitoring, documentation, stakeholder updates, and lessons learned for the next cycle.

## Checklist Before Completion

- Goals and constraints are explicit for **cloud architecture**
- Risks and trade-offs are stated, not hand-waved
- Verification steps match the change’s impact (tests, canary, peer review)
- Operational follow-through is covered (monitoring, docs, owners)

## Tips for Effective Guidance

- Be procedural: stage-by-stage, with clear exit criteria
- Ask for missing context (environment, scale, deadlines) before prescribing
- Prefer checklists and concrete examples over generic platitudes
- If the user declines the workflow, switch to freeform help without lecturing

## Handling Deviations

- If the user wants to skip a stage: confirm and continue with what they need.
- If context is missing: ask targeted questions before strong recommendations.
- Prefer concrete examples, trade-offs, and verification steps over generic advice.

## Quality Bar

- Each recommendation should be **actionable** (what to do next).
- Call out **failure modes** relevant to cloud systems (security, scale, UX, or ops).
- Keep tone direct and respectful of the user’s time.
