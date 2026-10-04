---
name: apple-app-store-readiness
description: "Plan, audit, or prepare an App Store candidate. Use for release scope, storefront metadata, privacy disclosures, review access, TestFlight, and explicit submission or release gates."
---

# App Store readiness

## Inputs

Identify the requested stage and authority, platform/product set, actual release promise, account model, business model, service dependencies, candidate source/build, and available App Store Connect evidence.

## Rules

- **STORE-001 — Separate stages.** Prepare, upload, process, TestFlight, submit, approve, and release are different gates. Readiness is not permission to publish; existing scoped approval remains usable until changed or revoked.
- **STORE-002 — Audit the real promise.** The binary, metadata, screenshots, services, and review instructions must describe the same complete experience.
- **STORE-003 — Recheck current requirements.** Consult current Apple requirements for toolchains, privacy, business model, region, and review; do not hard-code remembered policy as permanent law.
- **STORE-004 — Make review reproducible.** Provide live services, working links, access, sample data, and instructions for material dependencies.
- **STORE-005 — Bind evidence to a candidate.** Track source, version/build, archive/upload identity, platform set, and test results together.

## Workflow

1. Freeze the smallest complete release scope and identify unsupported promises.
2. Reconcile identity, public surfaces, privacy, monetization, and account/deletion behavior.
3. Inspect the exact candidate and its runtime/device evidence.
4. Prepare truthful storefront material and the review packet.
5. Reconcile current receipts and prior authorization, perform the authorized stage, and record resulting service state.

## Verify

Check core journey, denied/offline paths, linked services, privacy-policy access, required account deletion, purchases where applicable, screenshots, and reviewer access. Separate repository inspection from actual App Store Connect status.

## Output

Report each gate as passed, failed, not applicable, not authorized, or unverified, with exact candidate evidence and blockers in release order.

## References

Read the [playbook](references/app-store-readiness-patterns.md) for decisions, failure cases, and source links.

For review packets, cli adapters, and release ledgers, read the [focused reference](references/review-and-release-ledger.md).
