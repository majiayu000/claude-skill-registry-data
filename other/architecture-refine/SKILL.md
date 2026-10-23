---
name: architecture-refine
description: Settle open product or system architecture decisions with the user, one question at a time, before a plan or contract update. Use when a design has choices that only the user can make, such as tradeoffs in ownership, persistence, deployment, or migration; not for proposing a complete design, which belongs to system-design.
---

# Architecture Refinement

Settle only the architecture decisions that the user's next step needs, and record each decision with its reason.

## Interaction loop

1. Read the relevant code, documents, and constraints. Find facts yourself. Ask the user only about choices.
2. List the open decisions. Take first the decision that other decisions depend on or that costs most to reverse, such as a storage model, a public contract, or a tenancy boundary.
3. Ask one question. Put several constraints in one question only when the decision cannot be judged without all of them.
4. Give two or three concrete options with their main tradeoffs. Recommend one and give the reason.
5. Evaluate the user's answer and state its consequence for the design. If the answer conflicts with a constraint or an earlier decision, say so before you continue.
6. Repeat while an open decision still changes the user's next deliverable.

Test each option against runtime boundaries, ownership, persistence, deployment, operations, security, migration, rollback, and support burden. Prefer the smallest design that works. Reject flexibility that leaves behavior undefined.

Do not write a plan, edit a specification, run extended research, implement code, or write repository context. Use `plan-create`, `spec-update`, `technical-spike`, or `repo-context-document` for those outputs.

## Result

Finish when the decisions for the next step are settled, the user ends the session, or a named blocker needs another workflow. Report each accepted decision with its reason, the rejected options, the non-goals, the open risks, and the remaining blockers.
