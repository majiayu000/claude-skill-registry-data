---
name: input-guardrail-planner
description: Design input validation guardrails for AI agent systems — risk taxonomy, tripwire configs, evaluation benchmarks
triggers:
  - guardrail
  - input validation
  - agent safety
  - tripwire
  - content filter
version: 0.1.0
---

# Input Guardrail Planner

## When to Use
Use when you know you need input validation guardrails for an AI agent but not yet the right design. Best for turning risk concerns into a concrete guardrail architecture before implementation.

**Trigger patterns:**
- "Design guardrails for this agent"
- "What input filters do we need?"
- "Plan input validation for the agent system"
- "How should we handle prompt injection / PII / toxicity?"

## What It Does
Designs a guardrail architecture covering 5 risk categories (topic drift, toxicity, PII, injection, adversarial prompts) with:
- Risk taxonomy grounded in the actual agent architecture
- Tripwire-pattern guardrail configurations (YAML-driven)
- Precision/recall-calibrated thresholds
- Runtime approval gates (human-in-the-loop) for high-consequence/irreversible actions — the dynamic complement to static `disallowedTools`
- Evaluation benchmark design for each guardrail
- Implementation task list with TDD rhythm

## Invocation
```
/input-guardrail-planner
```

Or via meta-router:
```
/meta-plan "design input guardrails for [agent description]"
```

## Input
Provide:
1. Agent purpose and capabilities
2. Target audience and trust level
3. Data sensitivity classification
4. Any existing guardrails or filters
5. Compliance requirements (if applicable)

## Output
- Risk Assessment table (5 categories)
- YAML guardrail configurations with threshold justification
- Execution architecture (parallel/sequential)
- Evaluation benchmarks per guardrail
- Assumption Register (VERIFIED/REASONABLE/FRAGILE)
- Implementation tasks

## Companion Skills
- **output-guardrail-critic** — review guardrail configurations for coverage gaps after design
- **proposal-critic** — review the full guardrail design for feasibility and completeness
- **security-threat-model-planner** — if the agent needs a broader threat model first
