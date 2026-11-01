---
name: trd-authoring
description: Technical Requirement Document (TRD) Authoring — Translates product requirements into engineering specifications with strict PRD traceability.
---

# SKILL: Technical Requirement Document (TRD) Authoring
## Domain: Systems Engineering, Architecture, SDD Station 02 / 03

**Activation triggers:** technical requirements, engineering spec, system design criteria, PRD translation, TRD, SDD Station 02.

---

## 1. Role & Engineering Law

The TRD Authoring skill translates user-facing Product Requirement Documents (PRDs) into concrete engineering-facing technical specifications.  
It enforces the **Traceability Law**:
- Every technical requirement (`[TRD-xxx]`) MUST explicitly map back to at least one `[FR-xxx]` or `[NFR-xxx]` requirement from the parent PRD.
- Free-standing technical assertions that cannot cite a parent PRD requirement are rejected.

---

## 2. Document Structure & Required Sections

Every generated TRD must follow `.factory/specifications/templates/02_trd.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD ID, Target Specification, Lead Architect, Date.
- **Section 1: System Engineering Scope & Overview:** Technical objective, runtime versions, container standards.
- **Section 2: Technical Requirements:**
  - `[TRD-INT-xxx]`: Integrations and protocols (REST, WebSocket, gRPC).
  - `[TRD-DAT-xxx]`: Data persistence, storage volumes, and transaction guarantees.
  - `[TRD-API-xxx]`: API contracts, serialization formats, idempotency semantics.
  - `[TRD-RUN-xxx]`: Platform constraints, memory limits, CPU quotas, process lifecycle.
  - `[TRD-SEC-xxx]`: Security, token validation, crypto standards, and PII protection.
- **Section 3: Technical Risks & Mitigations:** Matrix of failure modes, severity, likelihood, and architectural mitigations.
- **Section 4: Requirements Traceability Matrix (PRD → TRD):**
  - Tabular mapping: `TRD Item ID | Summary | Source PRD Requirement ID | Verification Station`.
- **Section 5: Quality Gate G1 Signoff.**

---

## 3. Validation Checklist (Quality Gate G1 & G0.5 Pre-Condition)

- [ ] Parent PRD ID exists and is verified in `.factory/specifications/<project>/01_prd.md`.
- [ ] Every TRD requirement has a unique prefixed ID (`[TRD-INT-xxx]`, `[TRD-DAT-xxx]`, etc.).
- [ ] Requirements Traceability Matrix has 100% coverage with zero unlinked TRD items.
- [ ] Environment requirements explicitly specify Development, Staging, and Production targets.
- [ ] Document saved to `.factory/specifications/<project>/02_trd.md`.
