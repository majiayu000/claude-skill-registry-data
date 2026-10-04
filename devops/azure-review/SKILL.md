---
name: azure-review
description: Review an Azure solution architecture or implementation for platform fit, reliability, security, cost, operations, performance, governance, and deployment evidence. Use for Azure design reviews and Azure readiness assessments; do not use for deployment or generic cloud reviews without Azure scope.
---

# Azure Review

Assess the Azure design against documented requirements, current authoritative Azure guidance, and observable configuration. Do not infer subscriptions, regions, quotas, service features, policy assignments, or deployed state.

## Workflow

1. Read `AGENTS.md`, `architecture/toolkit-profile.yaml` when present, requirements, ADD/C4/ADRs, infrastructure-as-code, application configuration, operational evidence, and the requested environments.
2. Inventory Azure services, regions, resource boundaries, identities, network/data flows, dependencies, scaling assumptions, availability targets, recovery targets, data residency, and cost constraints.
3. Confirm time-sensitive service capabilities, limits, regional availability, retirement notices, and recommended patterns from current official Microsoft documentation. Cite the pages and access date in a persistent review.
4. Evaluate the solution using [references/azure-review-method.md](references/azure-review-method.md), tailoring depth to the workload and applicable project profile.
5. Validate important claims against IaC, policy/configuration, tests, monitoring, or runtime evidence. Label unobserved production claims `Not verified`.
6. Separate architecture findings, deployment/configuration drift, operational-readiness gaps, and optimization opportunities. Give concrete remediation and verification steps.
7. Persist only when requested, using the configured review path or `architecture/reviews/AZR-NNN-<slug>.md`.

## Rules

- Use Azure Well-Architected guidance as a review framework, not a substitute for workload requirements or evidence.
- Treat portal screenshots, diagrams, IaC, Azure Resource Graph results, policy state, and runtime telemetry according to what each actually proves.
- Check tenant/subscription/resource-group boundaries, identity and RBAC, networking, private access, encryption/key ownership, diagnostics, backup/restore, zone/region failure, scaling, quotas, deployment safety, policy, tagging, and cost controls when applicable.
- Identify service preview status, lock-in, regional constraints, unsupported combinations, and retirement/migration risk.
- Do not change Azure resources, policies, permissions, or deployments unless separately requested and authorized.
- Never claim Microsoft validation, compliance certification, or release approval.

## Output

Lead with the Azure readiness result and blockers. Include scope and evidence freshness, workload inventory, pillar scorecard, findings by severity, resilience and recovery assessment, security/governance observations, cost and operability risks, unverified assumptions, and recommended owner/action.
