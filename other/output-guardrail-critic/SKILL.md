---
name: output-guardrail-critic
description: Review AI agent guardrail configurations and execution results for coverage gaps, threshold calibration, and safety gate completeness
triggers:
  - review guardrails
  - guardrail review
  - output safety
  - guardrail coverage
version: 0.1.0
---

# Output Guardrail Critic

## When to Use
Use when you have an existing guardrail configuration or execution results and need an evidence-backed review before deployment. Best for finding coverage gaps, threshold calibration issues, and safety gate problems.

**Trigger patterns:**
- "Review these guardrails"
- "Are our output filters sufficient?"
- "Check guardrail coverage for this agent"
- "Review the safety gates before we deploy"

## What It Does
Reviews guardrail configurations and/or execution results with a 6-phase investigation protocol covering:
- Output quality gates (hallucination, citation, format, completeness)
- Safety gates (secret leakage, PII exposure, harmful content, bias)
- Runtime approval gates (human-in-the-loop coverage for high-consequence/irreversible actions)
- Configuration coverage and threshold calibration
- 3 perspectives: security engineer, end user, compliance officer

## Invocation
```
/output-guardrail-critic
```

Or via meta-router:
```
/meta-critic "review guardrails for [agent description]"
```

## Input
Provide one or both of:
1. Guardrail configuration (YAML, JSON, or descriptive)
2. Guardrail execution results (trigger logs, false positive reports)

Also helpful:
- Agent purpose and deployment context
- Compliance requirements
- Known false positive complaints

## Output
- Quality gate and safety gate review tables
- Configuration coverage assessment
- Multi-perspective findings (security, user, compliance)
- Severity-rated findings with evidence
- Verdict: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT

## Companion Skills
- **input-guardrail-planner** — when REVISE/REJECT, route back for guardrail redesign
- **security-threat-model-planner** — if the review reveals the agent needs a broader threat model
- **proposal-critic** — for reviewing the overall guardrail strategy at a higher level
