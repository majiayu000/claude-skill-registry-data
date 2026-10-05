---
name: gcp-service-adoption
description: Use for Google, Google Cloud, or GCP capability adoption work. Evaluate whether a requested feature should use a Google Cloud managed service, determine whether an existing Google Cloud or GCP project can host it or a new project is warranted, identify required API/IAM/networking/observability setup, and define rollout tracking including cost estimates, budgets, and budget alerts.
metadata:
  short-description: Google Cloud and GCP service adoption
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/gcp-service-adoption/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/gcp-service-adoption/SKILL.md`
> Source of truth: `registry/skills/gcp-service-adoption/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# GCP Service Adoption

Use this skill when a user wants to add a Google or Google Cloud capability to a project and needs more than API syntax.
This skill is for service selection, project placement, governance, and rollout readiness.

## Use this skill for

- Map a product need to a Google Cloud managed service
- Handle Google, Google Cloud, or GCP project/service adoption questions
- Check whether existing GCP projects can host the workload
- Decide whether to reuse a project or create a new one
- Identify required API enablement, IAM, secret, networking, and observability setup
- Define cost estimation, budgets, threshold alerts, and follow-up tracking

## Do not use this skill for

- Generic GCP tutorials with no concrete project decision
- Deep implementation inside an already chosen service SDK
- One-off CLI help where only a single `gcloud` command is needed

## Workflow

### 1. Map the requested capability to candidate GCP services

Read [references/service-mapping.md](references/service-mapping.md).
Produce one primary service recommendation and at most two alternatives.
When the primary service is one of the common profiles below, load the matching playbook as well:

- [references/cloud-run.md](references/cloud-run.md)
- [references/vertex-ai.md](references/vertex-ai.md)
- [references/cloud-storage.md](references/cloud-storage.md)
- [references/secret-manager.md](references/secret-manager.md)

### 2. Inventory existing GCP context

Read [references/project-selection.md](references/project-selection.md).
If the request spans multiple local repositories that each need different Google capabilities, also read [references/multi-project-google-bootstrap.md](references/multi-project-google-bootstrap.md).
If local CLI access exists, run `scripts/gcp_inventory.py` first.
If a target project and service are both known, run `scripts/gcp_project_readiness.py --project <id> --service <profile>` for a deterministic gap report.
If the goal is to go from capability to an initial project decision in one pass, run `scripts/gcp_adoption_assess.py --capability "<need>"`.

Minimum inventory:

- active account
- active project
- available projects
- available billing accounts
- existing enabled APIs for the candidate target project if known

### 3. Decide reuse versus new project

Use the reuse/new-project decision table in [references/project-selection.md](references/project-selection.md).
Bias toward reuse only when ownership, billing, IAM boundary, and operational fit are already clear.

### 4. Produce the enablement checklist

Use [references/project-selection.md](references/project-selection.md) and tailor the checklist to the chosen service.
Always cover:

- APIs to enable
- IAM roles and service accounts
- secrets and credentials
- networking constraints
- logging, monitoring, and auditability
- labels or tags for cost attribution

### 5. Produce the billing and budget plan

This step is mandatory.
Read [references/billing-governance.md](references/billing-governance.md).
Read [references/pricing-and-budget-apis.md](references/pricing-and-budget-apis.md) when live pricing lookup, budget inspection, or budget payload generation is needed.
If a rough monthly range is known, use `scripts/budget_plan_template.py` to generate the initial governance artifact.
If the adoption report needs to be formalized, use `scripts/adoption_report_template.py` and then fill in the checklist sections from the readiness output.
If live budget work is in scope, prefer `scripts/gcp_budget_api.py` in dry-run mode first.
If live pricing lookup is in scope, use `scripts/gcp_pricing_api.py`.

### 6. Define rollout tracking

Read [references/operations-tracking.md](references/operations-tracking.md).
The result should identify owners, review cadence, metrics, and budget alert handling.

## Output contract

For each adoption decision, output these sections in order:

1. Requested capability
2. Recommended GCP service
3. Existing-project fit
4. Reuse or new-project decision
5. Required setup checklist
6. Cost and budget plan
7. Ongoing tracking plan

Use [references/adoption-output-template.md](references/adoption-output-template.md) when you want a stable response skeleton.

## Reference loading guide

- Load [references/service-mapping.md](references/service-mapping.md) first for service choice.
- Load the matching service playbook when the chosen primary service is covered.
- Load [references/project-selection.md](references/project-selection.md) when project inventory or placement is in scope.
- Load [references/multi-project-google-bootstrap.md](references/multi-project-google-bootstrap.md) when several local repos need different Google projects or credential patterns.
- Always load [references/billing-governance.md](references/billing-governance.md) before finalizing the recommendation.
- Load [references/pricing-and-budget-apis.md](references/pricing-and-budget-apis.md) when live pricing or live budget administration enters scope.
- Load [references/operations-tracking.md](references/operations-tracking.md) when defining post-rollout ownership and review.
- Load [references/adoption-output-template.md](references/adoption-output-template.md) when drafting the final structured recommendation.
- Prefer `scripts/gcp_adoption_assess.py` as the default entrypoint when capability mapping, existing-project evaluation, and reuse/new-project decision are all in scope.
