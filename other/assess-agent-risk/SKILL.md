---
name: assess-agent-risk
description: Assess or review an AI agent's financial, operational, reputational, legal, security, privacy, regulatory, and human-impact risk. Use when classifying an agent, producing an inherent and residual risk assessment, defining governance tiers, evaluating controls, mapping risks to evals, screening a use case before launch, or reassessing a material agent change.
---

# Assess Agent Risk

Produce a scenario-based, evidence-linked assessment. Keep execution class,
governance tier, residual risk, and launch decision distinct.

## Workflow

1. Establish the assessed agent version, intended and prohibited uses, users,
   affected parties, jurisdictions, environment, owners, and execution class.
2. Inventory models, data, prompts, skills, tools, MCP servers, workflows,
   privileges, approvals, providers, and downstream consumers.
3. Screen for prohibited uses and binding legal, regulatory, contractual, and
   internal-policy floors. Treat unknown applicability as unresolved.
4. Identify credible normal-use, misuse, adversarial, dependency-failure,
   authorization, retry, concurrency, operator, and control-failure scenarios.
5. Assess all eight dimensions. Give every material scenario a stable ID,
   primary dimension, affected parties, cause, consequence, and owner.
6. Score inherent impact and likelihood before risk-reducing controls. Record
   tier, confidence, rationale, assumptions, and evidence gaps.
7. Identify preventive, detective, and recovery controls. Credit only controls
   supported by implementation and effectiveness evidence.
8. Score residual impact and likelihood. Do not lower impact unless a control
   truly reduces blast radius, duration, population, or reversibility.
9. Set the governance tier to the highest inherent scenario, regulatory or
   policy floor, or capability floor. Never average dimensions or scenarios.
10. Link each material scenario to eval cases, hard gates, production
    indicators, alerts, runbooks, and reassessment triggers.
11. Record treatment, accountable acceptance, conditions, expiry, and a `go`,
    `conditional_go`, or `no_go` recommendation. Never accept risk on behalf of
    the accountable human authority.

Read [the assessment standard](references/standard.md) before assigning scores.
Use [the examples](references/examples.md) to calibrate scenarios and avoid
confusing execution class with governance tier.

## Required Output

Return or update:

- assessment scope and regulatory screen;
- scenario register covering all eight dimensions;
- inherent and residual scores with confidence and rationale;
- controls with owners and evidence references;
- governance tier, mandatory floors, and launch recommendation;
- risk-to-eval and risk-to-monitoring traceability;
- accepted risks, conditions, owners, expiry, and next review date;
- open questions and missing evidence.

Use the repository's canonical risk-assessment template when one exists. Mark
unsupported claims and incomplete fields explicitly rather than inventing
evidence.

## Guardrails

- Do not treat the matrix as a legal or regulatory classification.
- Do not let a low average obscure one material scenario.
- Do not reduce residual risk for planned or untested controls.
- Do not equate human review with effective control without testing authority,
  timing, information, workload, and override behavior.
- Do not infer low likelihood solely because no incident has yet been observed.
- Do not declare a critical residual scenario launchable.
- Do not let the assessed agent or model approve its own risk.

## Completion Check

Confirm that an independent reviewer can trace every material rating to a
scenario, rationale, control, evidence item, owner, eval, production signal,
decision, and review date.
