---
name: assess-multi-agent-risk
description: Create or update a scenario-based risk assessment for a multi-agent system. Use when evaluating composition risk, emergent behavior, authority laundering, shared-state poisoning, false consensus, runaway delegation, dynamic membership, correlated failure, or governance tier and launch decisions.
---

# Assess Multi-Agent Risk

Assess risks created or amplified by composition while retaining all member-level risks.

## Workflow

1. Load the System Spec, member risk assessments, graph, policies, data flows, evals, and operating context.
2. Establish the governance floor from members, prohibited uses, data, effects, jurisdictions, and applicable regimes.
3. Write concrete scenarios across coordination, authority, security, privacy, reliability, financial, legal, regulatory, reputational, and human-impact dimensions.
4. Include injection propagation, confused deputy, authority laundering, shared-state poisoning, collusion, false consensus, recursive exhaustion, dynamic admission, duplicate effects, and partial completion where applicable.
5. Score inherent impact and likelihood with the published matrix; do not average scenarios.
6. Link preventive, detective, and corrective controls to implementation and eval evidence.
7. Score residual risk only after verified controls. Derive system tier and go, conditional-go, or no-go separately.
8. Check cross-artifact consistency with the project's own validation tooling or CI, and cite its output as evidence.

## Required Output

Produce a versioned system assessment with member references, scope, scenarios, controls, evidence, residual risks, acceptance, monitoring indicators, review date, and accountable decision.

Read [the risk standard](references/standard.md) and use [the examples](references/examples.md).

## Guardrails

- System risk cannot be lower than its required member or regulatory floor.
- Never reduce residual risk for an unverified control.
- Do not merge distinct affected parties or harms into one averaged score.
- Dynamic membership is a supply-chain and runtime admission boundary.

## Completion Check

Every material composition failure has an owner, measurable control evidence, an eval case, an indicator, and an explicit treatment decision.
