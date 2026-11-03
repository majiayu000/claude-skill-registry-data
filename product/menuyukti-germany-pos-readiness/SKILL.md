---
name: menuyukti-germany-pos-readiness
description: >
  Reusable, evidence-based engineering readiness audit for
  MenuYukti POS operating in Germany. Evaluates fiscalization,
  VAT, payments, transaction integrity, GDPR technical controls,
  security, offline reliability, architecture, testing, and
  production operations. Generates readiness scores, launch
  decisions, audit comparisons, and remediation roadmaps.
---

# MenuYukti Germany POS Readiness Audit

**Skill version:** `1.0.0`  
**Scoring version:** `1.0.0` (see [references/scoring-methodology.md](references/scoring-methodology.md))  
**Regulatory reference version:** `1.0.0`  
**Purpose:** Engineering readiness assessment — **not** legal or fiscal certification.

Invoke this skill when the user asks for a Germany POS readiness audit, fiscalization readiness review, German launch gate, delta readiness comparison, or focused POS compliance engineering audit.

## Do not run an audit unless requested

Creating or updating this skill is not an audit. Run an audit only when the user explicitly asks for FULL, DELTA, or FOCUSED mode.

## Primary questions every audit must answer

1. How ready is MenuYukti POS to operate commercially in Germany?
2. Which German market requirements are technically implemented?
3. Which critical engineering capabilities are missing?
4. Which vulnerabilities or architectural risks could prevent launch?
5. How has readiness changed since the previous audit?
6. What engineering tasks should be completed next?
7. What is the minimum remaining work for a controlled German launch?

Every comparable audit produces an evidence-backed score **0–100** from the **current repository state**. Never reuse prior conclusions without re-verification.

## Audit execution safety (mandatory)

**Read-only** with respect to application source and operational systems.

| Allowed                                                          | Forbidden without explicit approval                                           |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Repository inspection                                            | Application source modification                                               |
| Safe static analysis                                             | Production DB changes                                                         |
| Safe local tests                                                 | Destructive commands                                                          |
| Report generation under `backlog/docs/audits/germany-readiness/` | Live payment or fiscal transactions                                           |
| Historical comparison                                            | Production deployment, dependency installs, sending sensitive data externally |

Record any test that could not run and why.

## Audit modes

### FULL AUDIT

Inspect the entire repository and all readiness categories.

Use before initial Germany launch, after major releases/architecture changes, or before major production decisions.

Produce all reports, overwrite `backlog/docs/audits/germany-readiness/latest/`, and write an immutable snapshot under `history/`.

### DELTA AUDIT

Compare current codebase to the previous comparable full (or last full-baseline) audit.

Identify: improvements, resolved issues, new problems, regressions, score changes, new launch blockers, remaining critical risks.

Inspect relevant Git changes and **revalidate** affected workflows. Do not assume a finding is resolved because code changed.

Recalculate only categories with sufficient current evidence; label other category scores **historical**. Never silently publish a partial reassessment as a new comprehensive score.

### FOCUSED AUDIT

Target one or more scopes:

`fiscalization` | `vat` | `payments` | `transaction-integrity` | `security` | `gdpr` | `offline` | `reliability` | `localization` | `architecture` | `testing` | `devops` | `observability`

Generate findings for the scope. **Do not** replace the most recent full-audit baseline scorecard as if it were a new full audit. Store focused outputs under `history/` with mode `FOCUSED` and update `progress.md` only for scoped notes.

## Category weights (fixed — scoring v1.0.0)

| Category                             |   Weight |
| ------------------------------------ | -------: |
| German fiscal compliance engineering |      20% |
| VAT and financial correctness        |      10% |
| Payments and transaction integrity   |      15% |
| GDPR and security engineering        |      15% |
| POS operational reliability          |      15% |
| German localization                  |       5% |
| Architecture and maintainability     |       5% |
| Automated testing and QA             |       5% |
| DevOps and production operations     |       5% |
| Observability and recovery           |       5% |
| **TOTAL**                            | **100%** |

`Overall = Σ(CategoryScore × Weight / 100)`

If any weighted category lacks sufficient evidence, report **provisional** overall score or `UNKNOWN` and state whether a reliable overall score can be calculated.

## Evidence rules

Never score from feature names, UI screens, TODOs, docs claims, columns, endpoints, or flags alone.

Trace each requirement through the **business workflow**. For every finding record fields in [references/audit-report-schema.md](references/audit-report-schema.md).

**Statuses:** `VERIFIED` | `IMPLEMENTED_NOT_TESTED` | `PARTIAL` | `MISSING` | `UNKNOWN` | `NOT_APPLICABLE`

Do not invent evidence. Distinguish code inspection, automated tests, and production operational verification.

## Launch decision (independent of score)

Emit exactly one: `GO` | `CONDITIONAL GO` | `NO-GO` | `INSUFFICIENT EVIDENCE`

- Confirmed unresolved critical risks in fiscal integrity, payment correctness, severe data loss, or exploitable critical security → **block** unconditional launch (`NO-GO` or `CONDITIONAL GO` with blockers listed).
- Unverified mandatory controls → cannot be unconditional `GO`.
- High score cannot override blockers.
- Legal/fiscal external verification remains separate from this engineering gate.

## Execution workflow

Copy and track:

```text
Audit Progress:
- [ ] 1. Confirm mode (FULL | DELTA | FOCUSED) and scopes
- [ ] 2. Capture git metadata (branch, SHA, dirty flag)
- [ ] 3. Load prior comparable audit (if any) from history/
- [ ] 4. Refresh regulatory refs if network available; flag unverified sources
- [ ] 5. Inspect POS surfaces (see Repo map)
- [ ] 6. Score each in-scope category with check IDs from scoring-methodology.md
- [ ] 7. Evaluate all 15 critical failure scenarios (FULL; subset for FOCUSED)
- [ ] 8. Compute launch decision
- [ ] 9. Write reports from templates/ into latest/ + history/
- [ ] 10. Update progress.md (FULL / comparable DELTA only)
- [ ] 11. Validate report completeness against audit-report-schema.md
```

### Repo map (MenuYukti POS starting points)

| Area                 | Paths                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Fiscalization        | `apps/graphql/services/pos_fiscal*.py`, `pos_fiscalization.py`, `data_sources/models/pos_fiscal_process.py` |
| Orders / payments    | `apps/graphql/services/pos_orders.py`, `schema/mutations/pos_orders.py`, `schema/types/pos_order.py`        |
| Tax / money          | `apps/graphql/services/pos_tax.py`, `pos_money.py`                                                          |
| Audit trail          | `apps/graphql/services/pos_audit.py`, `data_sources/models/pos_audit_event.py`                              |
| Register / sequences | `data_sources/models/pos_register.py`, `pos_bill_sequence.py`                                               |
| Migrations           | `apps/graphql/alembic/versions/*pos*`                                                                       |
| Tests                | `apps/graphql/tests/` (POS-related)                                                                         |
| Clients              | `apps/web`, `apps/mobile-app` (POS UI/API consumers only — no direct DB)                                    |

Expand search as needed; do not limit evidence to this map.

### Critical failure scenarios (minimum set)

1. Internet disconnects during checkout
2. Payment succeeds but order update fails
3. Payment request is duplicated
4. TSE service unavailable
5. Fiscal transaction fails
6. Two cashiers edit one order
7. POS restarts during payment
8. Database unavailable
9. Refund after fiscalization
10. Receipt printer disconnects
11. Duplicate payment webhook
12. Offline transactions synchronize
13. Tax configuration changes
14. Tenant isolation challenged
15. Backup restoration vs transaction consistency

Details: [references/pos-transaction-integrity.md](references/pos-transaction-integrity.md), [references/pos-offline-reliability.md](references/pos-offline-reliability.md).

## Report outputs

**Canonical output root:** `backlog/docs/audits/germany-readiness/`

```text
backlog/docs/audits/germany-readiness/
├── latest/          # overwritten by FULL (and comparable DELTA that publishes a new baseline)
├── history/YYYY-MM-DD_HH-mm_<commit>/   # immutable
└── progress.md
```

Fill templates from `templates/`. Machine-readable snapshot: `history/.../audit.json` per [references/audit-report-schema.md](references/audit-report-schema.md).

Historical audits are **immutable**. Never overwrite prior `history/` snapshots. Use stable finding IDs across audits.

**Do not implement remediation tasks** unless the user separately requests implementation.

## Progressive disclosure (read when needed)

| Topic                                         | File                                                                                   |
| --------------------------------------------- | -------------------------------------------------------------------------------------- |
| Fiscal / KassenSichV / TSE / DSFinV-K         | [references/germany-fiscal-requirements.md](references/germany-fiscal-requirements.md) |
| VAT / restaurant tax engineering              | [references/germany-vat-requirements.md](references/germany-vat-requirements.md)       |
| GDPR + security technical checklist           | [references/gdpr-security-checklist.md](references/gdpr-security-checklist.md)         |
| Payments / integrity / failure scenarios      | [references/pos-transaction-integrity.md](references/pos-transaction-integrity.md)     |
| Offline / sync / reliability                  | [references/pos-offline-reliability.md](references/pos-offline-reliability.md)         |
| Architecture / tests / DevOps / observability | [references/engineering-quality.md](references/engineering-quality.md)                 |
| Scoring rubric & check IDs                    | [references/scoring-methodology.md](references/scoring-methodology.md)                 |
| JSON + markdown report schema                 | [references/audit-report-schema.md](references/audit-report-schema.md)                 |

### Templates

- [templates/executive-summary.md](templates/executive-summary.md)
- [templates/scorecard.md](templates/scorecard.md)
- [templates/findings-register.md](templates/findings-register.md)
- [templates/compliance-gap-analysis.md](templates/compliance-gap-analysis.md)
- [templates/failure-scenario-matrix.md](templates/failure-scenario-matrix.md)
- [templates/engineering-roadmap.md](templates/engineering-roadmap.md)
- [templates/audit-comparison.md](templates/audit-comparison.md)

## How to invoke

| Mode    | Example user phrasing                                                     |
| ------- | ------------------------------------------------------------------------- |
| FULL    | “Run a FULL Germany POS readiness audit”                                  |
| DELTA   | “Run a DELTA Germany POS readiness audit vs last full audit”              |
| FOCUSED | “Run a FOCUSED Germany POS readiness audit on fiscalization and payments” |

After each FULL (or comparable DELTA that republishes baseline), update `progress.md` with score delta, P0 changes, regressions, and launch-decision changes. If scoring methodology version changed, do **not** show an unqualified score comparison.
