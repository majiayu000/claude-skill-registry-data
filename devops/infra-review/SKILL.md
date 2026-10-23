---
name: infra-review
description: Review infrastructure-as-code and rendered deployment configuration without modifying it. Use before plan, apply, or deploy when targeting, replacement, state, availability, cost, ordering, or recovery blast radius may change.
---

# Infrastructure Review

Find the infrastructure changes that can destroy, replace, expose, or disrupt something before anyone applies them, using only evidence that changes nothing.

## Workflow

1. Identify the comparison target, the path from source to rendered configuration, the tools and their versions, and the affected environment. Refer to environments with redacted identifiers.
2. Rank the changed resources by blast radius, then read their full definitions and dependency order.
3. Check targeting, replacement or destruction, state and migration safety, data protection, recovery from a partial apply, availability, disruption, capacity, and material cost.
4. Prefer plan output that already exists, such as a plan from CI. Read replacements and deletions from the machine-readable plan, not from its summary. For Terraform or OpenTofu: `terraform show -json <planfile> | jq -r '.resource_changes[] | select(.change.actions | index("delete")) | "\(.address) \(.change.actions | join(","))"'` lists every resource that the plan deletes or replaces.
5. Run a new plan, render, diff, or dry run only when it is authorized and the repository supports it. A local `terraform plan` needs cloud credentials and takes a state lock by default, which writes to the backend and blocks other runs.
6. Before you claim that a change replaces or destroys a resource, confirm the provider's behavior for that attribute in its local version or its documentation.
7. Delegate exploit analysis to `security-review`, dependency provenance to `dependency-review`, CI mechanics to `ci-review`, and cross-cutting runtime readiness to `rollout-readiness-review`.

Never apply, deploy, install, upgrade, delete, destroy, or modify cloud state. Do not expose sensitive plan output or add policy frameworks for the review.

## Result

Report each finding with its severity, exact location, redacted environment, concrete blast radius, failure path, smallest correction, evidence, and uncertainty. Mark confirmed public exposure, privilege escalation, secret leakage, unprotected destruction, unsafe state migration, and missing recovery as blocking findings; this is advice, not authority to block an operation. Also report the scope, the destructive effects, the cost impact, the checks run, and the confidence limits, or state that nothing was found.
