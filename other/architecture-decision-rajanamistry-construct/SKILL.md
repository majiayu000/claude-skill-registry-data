---
name: architecture-decision
description: Compare technical options and draft an architecture decision with constraints, contracts, tradeoffs and revisit triggers. Use before choosing system boundaries, technologies, storage or integrations. Read-only analysis unless artifact writing is explicitly requested.
---

# Architecture decision

Status: Draft. Not yet verified in a documented practical example.

Input: decision to make, product requirements, current system, quality attributes and constraints. Inspect the relevant source and existing decisions first. A proposed architecture is not evidence of an implemented system.

## Procedure

1. **Constrain.** State the problem and measurable needs for security, reliability, performance, accessibility and maintenance. Mark budget, scale and team capability assumptions. Identify who accepts the decision.
2. **Compare.** Include the current or simplest viable solution and credible alternatives. Compare complexity, operability, total cost, compatibility, migration effort and reversibility. Avoid choosing services or technology because they are fashionable.
3. **Contract.** Define module ownership, interfaces, data model and invariants, data flows and integration boundaries. Address authentication, authorization, secrets and data lifecycle with the security owner.
4. **Stress.** Walk through failure, timeout, retry, duplicate request, concurrency, dependency outage and recovery. Name observability, scalability limits and migration/rollback constraints. Propose a bounded test for the highest-risk assumption.
5. **Record.** Return a proposed decision, alternatives rejected, consequences, evidence, open questions, owner and triggers for revisiting it. Split approved implementation with `planner`, not inside the decision record.

## Output skeleton

```markdown
# Decision: <question>
Status: proposed | accepted by <human owner> | superseded
Context and constraints: <facts and labelled assumptions>
Options and tradeoffs: <including the simple baseline>
Proposed decision and rationale: <why this fits>
Contracts and failure behavior: <boundaries, invariants, recovery>
Validation: <experiment, limits, result or not run>
Consequences and revisit triggers: <costs and changed assumptions>
Evidence: <public sources or allowed repository paths, revision and date>
```

Do not mark a decision accepted without recorded human approval. No purchases, infrastructure changes, credential use or migrations are authorized by this procedure. Write a record only to a user-approved destination; otherwise return it in the reply.
