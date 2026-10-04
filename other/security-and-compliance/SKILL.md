---
name: security-and-compliance
description: Use when user mentions "security review", "compliance", "SOC 2", "GDPR", "PII", "threat model", when the system handles sensitive data, when preparing for an audit or certification, when assessing risk before launch, or when a STRIDE threat model is needed for a new component.
---

# Security and Compliance

## Overview

Read `.forge/architecture.md` and `.forge/contracts/` to produce `.forge/security.md` — a comprehensive security and compliance assessment. The output must identify every data store, every trust boundary, and every regulatory requirement before any code is written.

## When to Use

- `.forge/architecture.md` exists and the system handles user data
- Regulatory requirements apply (GDPR, CCPA, SOC 2, HIPAA, PCI-DSS)
- System has multi-tenant data or PII
- Pre-launch security gate or investor due diligence

## When NOT to Use

- No architecture exists — run `architecture-and-contracts` first
- Looking for code-level vulnerabilities — use `code-review-and-quality` security axis
- Emergency security incident — that's incident response, not planning

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll handle security after MVP" | Security retrofits cost 10x. Design it in now |
| "We don't have PII" | Email addresses are PII. User IDs linked to behavior are PII. Audit first |
| "Our cloud provider handles compliance" | Shared responsibility model — your provider secures infra, you secure data and access |
| "SOC 2 is only for enterprise sales" | Any B2B buyer with a security team will ask. Start the roadmap early |
| "Encryption at rest is enough" | Encryption without key management is theater. Who holds the keys? |

## Red Flags

- No data classification scheme (what's sensitive vs. public)
- Multi-tenant system with no Row-Level Security or tenant isolation plan
- PII inventory is empty ("we don't store PII" without audit)
- Vendor list has no security assessment
- Threat model is missing or covers fewer than 5 attack vectors
- "We'll encrypt everything" without specifying what, how, and who manages keys

## Core Process

### Step 1: Authentication model

Define: identity provider, session management, token format, expiry policy, MFA requirements, credential storage. Map auth flow for every user type in the PRD.

### Step 2: Data isolation

For multi-tenant systems: tenant isolation strategy (separate DBs, shared DB with RLS, schema-per-tenant). For single-tenant: user-level access controls. Document: how is tenant A prevented from seeing tenant B's data?

### Step 3: PII inventory

Audit every data store. For each:
- What PII is stored (name, email, phone, address, payment, behavioral)
- Retention policy (how long, deletion trigger)
- Access controls (who can read, who can write)
- Encryption status (at rest, in transit)

### Step 4: Regulatory scan

Based on the PII inventory and target market:
- Which regulations apply (GDPR, CCPA, HIPAA, PCI-DSS, SOC 2)?
- What consent mechanisms are required?
- What data subject rights must be supported (access, deletion, portability)?
- What breach notification requirements exist?

### Step 5: Encryption audit

For each data flow and store:
- In transit: TLS version, certificate management
- At rest: encryption algorithm, key management (who holds keys, rotation policy)
- Application-level: field-level encryption for highly sensitive data

### Step 6: Vendor assessment

Every third-party service or API:
- What data do they receive?
- What is their security posture (SOC 2, ISO 27001, BAA)?
- What happens to data if the vendor is breached?
- Is there a DPA (Data Processing Agreement)?

### Step 7: Certification roadmap

Based on regulatory scan and sales requirements:
- Which certifications to pursue and in what order
- Timeline and estimated cost
- Gaps between current posture and certification requirements

### Step 8: STRIDE threat model

For each trust boundary in the architecture:
- **S**poofing: can an attacker impersonate a user or service?
- **T**ampering: can data be modified in transit or at rest?
- **R**epudiation: can actions be denied without audit trail?
- **I**nformation disclosure: can unauthorized parties access sensitive data?
- **D**enial of service: can the system be overwhelmed?
- **E**levation of privilege: can a user gain unauthorized access?

Prioritize by likelihood × impact. Top 5 threats get specific mitigations.

## Output

Write `.forge/security.md` with all sections above. Prepend a `forge:meta` header (`generated_by: security-and-compliance`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md, .forge/contracts/*]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <hash>, .forge/contracts/<each-resolved>.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

After writing: "Security assessment written to `.forge/security.md`."

### Step 9: File feedback for architecture-impacting findings

`.forge/security.md` is downstream of `.forge/architecture.md`. Findings that imply architecture changes (add a WAF, change a data store, add an API gateway, introduce a secrets manager, refactor tenant isolation) cannot be auto-cascaded — they require a human decision.

For each such finding, invoke the `feedback` skill to file `.forge/feedback/<timestamp>-secure.md`:
- `target_artifact: .forge/architecture.md`
- `severity: NEEDS_REVIEW` (not FEEDBACK_PENDING — the user decides whether to absorb the change)
- `finding:` what was discovered + the threat being mitigated
- `recommended_change:` the specific architectural addition (component, placement, integration point)

Do NOT edit `architecture.md` directly. The user reviews the entry and either runs `/architect` to absorb the change or marks the entry DEFERRED with reasoning.

The same protocol applies for `scalability-analysis` when it recommends architectural changes (sharding strategy, read replicas, cache tier insertion).

## Verification

- [ ] `.forge/architecture.md` read before starting
- [ ] Every data store has a retention policy
- [ ] PII inventory covers all user-facing data
- [ ] Every third-party vendor assessed
- [ ] STRIDE threat model covers at least 5 attack vectors with mitigations
- [ ] Certification roadmap has specific timelines
- [ ] Multi-tenant isolation strategy is explicit (if applicable)
- [ ] `.forge/security.md` written
- [ ] For every finding that implies architecture changes (WAF, gateway, data-store swap, isolation refactor): a `feedback` entry was filed targeting `.forge/architecture.md` with severity `NEEDS_REVIEW`. No direct edits to `architecture.md`.
