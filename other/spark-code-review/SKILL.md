---
name: spark-code-review
description: Use when a Spark implementation needs an evidence-based review for correctness, ownership, compatibility, failure handling, maintainability, and unnecessary complexity.
---

# Spark code review

Review the actual diff and reachable behavior. Treat unnecessary complexity as
an engineering defect when it creates permanent surface area, duplicated
semantics, state, lifecycle, or failure modes without a corresponding invariant.

Use `spark-change-scope` first when the owner and acceptance boundary are not
already explicit. Use `spark-find-simplifications` when a finding needs an
equivalence-preserving removal plan.

## Procedure

1. Reconstruct the intended behavior, acceptance boundary, and authoritative owner from code, tests, and contracts.
2. Read the complete changed functions plus callers and consumers that establish externally observable behavior.
3. Check state ownership, dependency direction, protocol translation, compatibility reads/writes, authorization, cancellation, retries, recovery, persistence, and cleanup as applicable.
4. Apply the deletion test to every new helper, type, interface, schema, config field, cache, queue, adapter, compatibility path, background loop, and test utility:
   - What semantic distinction or invariant does it add?
   - Is the same fact already represented or enforced elsewhere?
   - Could it be deleted or inlined without changing required behavior?
   - Does it create another state owner, synchronization point, failure mode, or compatibility burden?
   - Is it repairing stale state instead of fixing the authoritative mutation path?
   - Is it current required behavior or speculative scaffolding?
5. Reconstruct cross-owner invariants. A locally correct component still fails review when its composition violates the claimed system property.
6. Inspect tests as production engineering. Flag wrappers with no semantic payload, fixtures that outweigh the behavior under test, and assertions that fossilize invented semantics for unspecified inputs.
7. Check bounded collection logic for `limit` before downstream filtering or skipping; prove that the limit is applied on the dimension whose fairness or completeness is claimed.
8. Run focused diagnostics when static inspection cannot settle a claim.
9. Report only actionable findings caused by the change. Prefer deletion, consolidation into the authoritative owner, or an existing primitive over another abstraction.

## Complexity findings

Report these when the diff provides concrete evidence:

- zero-semantic indirection: forwarding wrappers, re-exports, getters, or test helpers that add no policy, conversion, ownership boundary, or invariant;
- duplicated semantics: the same schema, validator, predicate, authority rule, mapping, or state transition encoded in multiple places;
- speculative scaffolding: public APIs, config, state, `NOT_IMPLEMENTED` methods, or compatibility machinery added only for possible future work;
- parallel truth: another aggregate, queue, cache, projection, ledger, or lifecycle for facts already owned elsewhere;
- reconciliation-as-design: polling, periodic scans, or unrelated mutations used to repair state the authoritative update path can keep consistent;
- invented semantics: implementation and tests defining behavior for invalid or unspecified inputs without a product requirement;
- governance instead of simplification: adding budgets, ratchets, exceptions, or facades to manage an avoidable abstraction;
- security-shaped metadata: caller-constructible labels presented as authority or proof rather than provenance metadata;
- local correctness with global inconsistency: a component satisfies its local contract while breaking a higher-level invariant.

Do not report formatting or personal style preferences. A small helper is useful
when it owns a real invariant, and validation belongs at an untrusted boundary.
Missing future functionality is not a defect; surface area added today solely
for that future may be. Added state, lifecycle, synchronization, or public
surface is not merely style.

Do not accept tests that assert prompt wording unless exact representation is
the contract. Stop with `needs-decision` when correctness or ownership depends
on an unresolved product choice.

Return `findings`, `verifiedBehaviors`, `residualRisks`, and `verdict`. Each
finding includes `severity`, `category`, `evidence`, `impact`, `deletionTest`,
and `repairDirection`. Category is `correctness | security | ownership |
compatibility | complexity`.
