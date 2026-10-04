---
name: apple-privacy-system-integrations
description: "Design or audit protected-data access and system boundaries. Use for permissions, purpose strings, privacy manifests, data minimization, retention, deletion, disclosures, and account changes."
---

# Apple privacy and integration safety

## Inputs

Inventory the user purpose, exact data categories, source and destination, operators, permissions, storage, projections, retention, and deletion. Identify which integrations are essential versus supplementary.

## Rules

- **PRIV-001 — Describe actual boundaries.** No developer server does not mean no storage or sharing. Include local files, system stores, cloud containers, SDKs, logs, and derived data.
- **PRIV-002 — Request minimum access in context.** Use truthful purpose text and framework-supported states. Do not invent an authorization signal the framework intentionally withholds.
- **PRIV-003 — Keep artifacts distinct.** Entitlements, purpose strings, privacy manifests, store disclosures, and consent serve different purposes; validate each applicable layer.
- **PRIV-004 — Preserve truthful outcomes.** Denial, no data, revoked access, account mismatch, unavailable service, and retry are not interchangeable success states.
- **PRIV-005 — Complete the data lifecycle.** Define minimization, secure storage, logging, retention, export, deletion, and stale-projection cleanup before adding persistence or transfer.

## Workflow

1. Map data flows through the app, frameworks, extensions, devices, cloud, and third parties.
2. Verify current framework permission contracts and official privacy requirements.
3. Implement scoped access, typed states, safe fallback, and deletion/reconciliation behavior.
4. Update the applicable declarations and disclosures from the actual behavior.
5. Test transitions and inspect built products plus exposed system surfaces.

## Verify

Exercise first use, denial, partial scope, revocation, no data, account change, offline retry, and deletion where supported. Check logs and projections for unintended sensitive fields. Pair with project governance and device validation for artifact/runtime proof.

## Output

Return the data-flow contract, permission behavior, required artifacts, tested failure paths, and unresolved privacy or compliance questions. Do not claim legal certification.

## References

Read the [playbook](references/privacy-system-patterns.md) for decisions, failure cases, and source links.

For data inventory across tools and system surfaces, read the [focused reference](references/integration-data-inventory.md).
