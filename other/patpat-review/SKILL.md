---
name: patpat-review
description: Independently challenge an implementation, diff, or verification claim without editing. Use after meaningful changes, for explicit code review, or when high-risk evidence needs a separate skeptical pass.
---

# Patpat Review

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [proof over proxy](../patpat-loop/principles/proof-over-proxy.md), and [preserve safety](../patpat-loop/principles/preserve-safety.md). Apply the [independent review playbook](../patpat-loop/playbooks/independent-review.md).

Remain read-only. Inspect the objective, proof contract, exact diff or artifact, raw verification receipts, and affected contracts. When an independent reviewer is available and authorized, give it the evidence without the implementer's intended conclusion. When extra read-only reviewers are available and authorized, give each the same intent, diff, and integrity rubric from a distinct independent-angle. Consensus outweighs a lone finding. Bucket the synthesized verdict Act on / Consider / Noted / Dismissed. Do not auto-apply.

Run the playbook's solution-integrity audit before general quality review. Reject evidence laundering, unexplained assertion weakening, hardcoded fixture answers, and proof that bypasses the claimed authoritative surface. Bind evidence to the exact candidate revision or reproducible working-tree snapshot; require a committed head only for commit- or delivery-bound claims.

## Findings and reporting

When the main issue is a change in shape, prefer a diff-shaped or tree explanation from [earned representation](../patpat-loop/references/earned-representation.md) over long prose. Report findings first, ordered by `blocker`, `high`, `medium`, then `low`. Tie every finding to a file, symbol, behavior, or receipt and explain the concrete impact. Exclude speculative style preferences. For each accepted issue, recommend the smallest safe correction and required re-verification.

State `no findings` only after checking correctness, solution integrity, regressions, contracts, safety, performance implications, side effects, generated noise, and evidence mismatch. Review does not replace verification and never authorizes merge or delivery.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
