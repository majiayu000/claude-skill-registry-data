---
name: sota-privacy-compliance
description: State-of-the-art privacy and compliance engineering guidance for building privacy-respecting systems and auditing existing code for privacy/compliance gaps. Use when work involves privacy, GDPR, PII, personal data, consent, data retention, deletion, DSAR (data subject access requests), SOC 2, ISO 27001, HIPAA, PCI DSS, compliance evidence, data residency/sovereignty, data classification, anonymization/pseudonymization, breach notification, or EU AI Act obligations — whether designing new data flows, implementing user-rights features (export/delete), preparing for an audit, or reviewing a codebase for places personal data is over-collected, under-protected, retained forever, or impossible to delete.
---

# SOTA Privacy & Compliance Engineering

Engineering-facing privacy and compliance architecture: how to design, build, and
audit systems so that data protection is a property of the code and infrastructure,
not a binder of policy documents. Compliance that lives in schemas, TTLs, IAM
policies, and CI checks survives staff turnover and audit scrutiny; compliance that
lives in wiki pages does not.

> **This is engineering guidance, not legal advice.** Regulations change, vary by
> jurisdiction, and turn on facts about your business that code review cannot see.
> Regulatory facts below were verified against primary sources as of June 2026 —
> re-verify deadlines and statuses before relying on them, and route legal
> interpretation (lawful basis selection, contract terms, breach reportability
> decisions) to qualified counsel or your DPO. This skill tells you how to build
> the machinery those decisions require.

**Related skills — reference, don't duplicate:**
- `sota-databases` rules/06 — DB-level PII mechanics (column encryption, row-level security, GDPR-friendly schema design)
- `sota-secrets-management` — credentials, KMS, key rotation (crypto-shredding depends on it)
- `sota-observability` — log redaction and PII-safe telemetry pipelines
- `sota-threat-modeling` — LINDDUN privacy threat modeling methodology
- `sota-code-security` / `sota-devsecops` — vulnerability management, supply chain (SOC 2/ISO control overlap)

## BUILD mode

When designing or implementing systems that touch personal data:

1. **Inventory first.** Before writing a schema or integrating a vendor, classify
   every field you intend to collect and record where it flows (rules/01). The
   cheapest control is the field you never store.
2. **Annotate at the source.** Schemas, structs, and API contracts carry
   classification and purpose annotations; tooling derives the data map from code,
   not the other way around (rules/01, rules/02).
3. **Build user rights as features, not afterthoughts.** Export, deletion, and
   consent are product capabilities with APIs, state machines, and tests — design
   them with the first table, because retrofitting deletion into a 200-table
   schema with denormalized copies is a quarter-long project (rules/03).
4. **Automate retention.** Every datastore gets a TTL, lifecycle rule, or
   partition-drop schedule at creation time. "We'll clean it up later" is how
   seven-year-old PII ends up in a breach disclosure (rules/03).
5. **Emit evidence as a byproduct.** Access reviews, change approvals, and config
   baselines should fall out of normal engineering workflow (PRs, IaC, IdP logs)
   so audits are queries, not scrambles (rules/05).
6. **Know your regimes.** Check rules/04 for which regulations the system triggers
   (data types × subjects' locations × sector) before architecture freezes — data
   residency and breach-clock requirements shape topology.

## AUDIT mode

When reviewing an existing codebase/infrastructure for privacy and compliance gaps:

**Process:** (1) Build or obtain the data inventory — grep schemas, API payloads,
log statements, analytics events, object storage for personal data (rules/01 has
discovery patterns). (2) Trace lifecycle per data category: collection → purpose →
storage → sharing → retention → deletion. (3) Test user rights paths end-to-end
(does deletion actually propagate?). (4) Check evidence trails for auditable
controls. (5) Map findings to applicable regimes (rules/04).

**Severity conventions:**

| Severity | Meaning | Examples |
|---|---|---|
| CRITICAL | Active violation with regulatory/breach exposure; fix now | PII in world-readable bucket; deletion endpoint that doesn't delete; special-category data collected without any consent record; cardholder PANs stored unencrypted in app DB |
| HIGH | Violation likely under normal operation or on first DSAR/audit/breach | No deletion propagation to backups/analytics; consent not versioned or not propagated to processors; no retention enforcement anywhere; PII in logs shipped to third party without DPA |
| MEDIUM | Gap that degrades posture or audit readiness | Classification annotations missing; data map stale/manual; soft-delete only with no purge job; access reviews manual and undocumented |
| LOW | Hardening/hygiene | Cookie banner lacks granular toggles; export format not machine-readable; missing purpose comments on schema fields |

**Finding format:**

```
[SEVERITY] <title>
Location: <file:line / table / bucket / service>
Data: <what personal data, what classification tier>
Regimes: <GDPR Art. X / CCPA / HIPAA / PCI DSS req N / SOC 2 CC-N — as applicable>
Issue: <what is wrong, lifecycle stage affected>
Impact: <realistic consequence: fine exposure, breach scope, audit failure, DSAR failure>
Fix: <concrete engineering remediation>
Evidence: <how you verified — query, code path, test>
```

Report findings grouped by data lifecycle stage (collection / storage / sharing /
retention / deletion), not by file — that is how regulators and auditors think.

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-data-inventory-classification.md](rules/01-data-inventory-classification.md) | Starting any privacy work; building/auditing a data map; defining classification tiers; hunting PII in schemas, logs, buckets, backups, analytics; mapping flows to processors |
| [rules/02-privacy-by-design.md](rules/02-privacy-by-design.md) | Designing schemas/APIs that touch personal data; minimization and purpose limitation in code; choosing pseudonymization vs anonymization vs tokenization; exposing aggregate stats; evaluating re-identification risk; anti-bot fingerprinting; blocking remote content (IP leakage, HTML email); duress/panic mode for at-risk users |
| [rules/03-consent-and-user-rights.md](rules/03-consent-and-user-rights.md) | Building consent management, cookie/tracker governance, DSAR export, deletion (hard/soft/crypto-shred + propagation), or retention automation; auditing whether user rights actually work |
| [rules/04-regulatory-landscape.md](rules/04-regulatory-landscape.md) | Determining which regimes apply; GDPR engineering mechanics (lawful basis, transfers, DPIA, 72h); US state laws; HIPAA; PCI DSS 4.x scoping; EU AI Act timeline; DORA/NIS2; data residency architecture |
| [rules/05-audit-ready-engineering.md](rules/05-audit-ready-engineering.md) | Preparing for SOC 2 / ISO 27001; automating evidence; mapping controls to engineering practice; vendor/subprocessor management; policy-as-code; avoiding common audit findings |
| [rules/06-incident-breach-readiness.md](rules/06-incident-breach-readiness.md) | Building breach response capability; classification (is it reportable?); notification clocks per regime; forensics-friendly logging without privacy violations; post-incident obligations |

## Top 10 non-negotiables

1. **No unmapped personal data.** Every field of personal data has a recorded
   classification, purpose, owner, retention period, and list of systems it flows
   to. Unmapped data is unprotectable data.
2. **Collect the minimum.** Each field collected must trace to a specific,
   documented purpose. A field without a purpose is deleted, not "kept just in
   case" — it is pure liability with zero value.
3. **Deletion must actually delete.** A deletion request propagates to primary
   stores, replicas, caches, search indexes, analytics, ML training sets, and is
   handled for backups (expiry or crypto-shred). A soft-delete flag alone is a
   finding, not a deletion architecture.
4. **Retention is enforced by machines.** TTLs, object lifecycle rules, partition
   drops — running and monitored. A retention policy with no automated enforcement
   is fiction.
5. **Consent is versioned, granular, revocable state** — recorded with timestamp,
   policy version, and scope; checked at point of use; revocation propagates to
   processors. Never inferred, never a boolean column named `gdpr_ok`.
6. **No PII in logs, URLs, or analytics events** unless explicitly classified,
   redaction-tested, and retention-bounded (see sota-observability for pipeline
   mechanics). Logs are the most common shadow copy of personal data.
7. **Pseudonymized ≠ anonymous.** Data that can be re-linked (hashed emails,
   "anonymized" user IDs, quasi-identifier combinations) is still personal data.
   Treat claimed anonymization as a re-identification risk to verify, not a label
   to trust.
8. **Encrypt personal data at rest and in transit, with keys you can destroy.**
   Key-per-user or key-per-tenant where deletion/residency demands it
   (crypto-shredding); keys managed per sota-secrets-management.
9. **Cross-border flows are deliberate.** Know which regions data lives in and
   transits; region-pin where required; every processor/subprocessor has a DPA and
   appears in the data map before the first byte flows.
10. **Evidence or it didn't happen.** Access reviews, consent records, deletion
    proofs, DPIAs, breach timelines — generated and retained automatically. If you
    cannot produce the artifact in minutes, the control will fail its audit.
