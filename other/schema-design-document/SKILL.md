---
name: schema-design-document
description: Schema & Database Design Document Authoring — Creates entity catalogs, live-synced Mermaid ERDs, indexing strategies, migration sequences, and PII retention policies with automated schema drift detection.
---

# SKILL: Schema & Database Design Document Authoring
## Domain: Data Architecture, Relational Modeling, SDD Station 04 / 05

**Activation triggers:** database schema, ERD, entity relationship, migrations, indexes, DDL, table design, PII retention, SDD Station 04.

---

## 1. Role & Engineering Law

The Schema Design Document skill produces authoritative physical and logical data model specifications.  
It enforces the **Database-to-Code Consistency Law**:
- The ERD and table specifications must never be hand-drawn prose left to drift.
- The document must record a `Live Schema Hash` derived from active migration files and live database catalogs.
- If migration files are modified without updating this document, or vice versa, Quality Gate 0.5 and the Database Gate fail immediately.

---

## 2. Document Structure & Required Sections

Every generated Schema Document must follow `.factory/specifications/templates/05_schema_document.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent TRD ID, Target Specification, Database Engine, Live Schema Hash, Data Architect, Date.
- **Section 1: Data Model Architecture Overview:** Scope and transactional semantics.
- **Section 2: Entity-Relationship Diagram (ERD):**
  - Machine-generated Mermaid `erDiagram` showing all tables, primary keys (`PK`), foreign keys (`FK`), unique keys (`UK`), attributes, and relationships (`||--o{`, `||--||`, etc.).
- **Section 3: Entity Catalog & Attribute Specifications:**
  - Per-entity table with Column Name, Type, Nullability, Default, Constraints/Flags, and Description.
- **Section 4: Indexing Strategy & Performance Rationale:**
  - Table, Index Name, Columns, Type (B-tree, GIN, BRIN), and explicit Query Rationale.
- **Section 5: Migration Sequence & Rollback Plan:**
  - Step-by-step migration files with forward `Apply` and reverse `Rollback` DDL.
- **Section 6: Seed & Test Fixture Strategy:**
  - Deterministic fixture models and teardown isolation rules.
- **Section 7: Data Retention, Privacy & Security:**
  - Explicit `PII-DIRECT` and `SECRET` tagging on columns, encryption-at-rest, retention horizons.
- **Section 8: Verification & Drift Check Signoff.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] Mermaid `erDiagram` is syntactically valid and matches table attribute definitions.
- [ ] Every foreign key has a corresponding parent primary key.
- [ ] Every index specifies an explicit query pattern justification.
- [ ] PII and sensitive columns are explicitly tagged and masked.
- [ ] Document saved to `.factory/specifications/<project>/05_schema_document.md`.
