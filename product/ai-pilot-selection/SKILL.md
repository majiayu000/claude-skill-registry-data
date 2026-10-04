---
name: ai-pilot-selection
description: Select and design AI pilots with clear hypotheses, success metrics, guardrails, and decision rules. Use when Codex is asked to choose AI pilots, compare pilot candidates, define pilot scope, create a pilot scorecard, or decide what AI experiment to run first.
license: MIT
---

# AI Pilot Selection

## Core Workflow

1. Define the business decision the pilot should inform.
2. Compare candidate pilots by value, feasibility, risk, measurability, adoption
   readiness, and time to learn.
3. Define hypothesis, users, workflow, data, tools, baseline, success metrics,
   guardrails, decision rules, and owner.
4. Keep pilot scope small enough to learn without creating hidden production
   dependency.
5. Identify governance, security, privacy, people, customer, and legal review
   needs before launch.
6. State continue, revise, scale, or stop criteria.

## Safety Rules

- Do not treat a pilot as production approval.
- Do not recommend autonomous actions without explicit review and controls.
- Do not invent baseline metrics, ROI, data access, or user adoption.
- Escalate pilots involving sensitive data, customer impact, employment impact,
  regulated decisions, production systems, or security controls.

## Deliverable Shape

For AI pilot selection, provide:

- Candidate comparison
- Selected pilot and rationale
- Hypothesis
- Scope and non-goals
- Metrics and guardrails
- Governance review needs
- Decision rules
- Owner and timeline

## References

- Read `references/ai-pilot-selection-checklist.md` when selecting, scoping, or
  reviewing AI pilots and experiments.
