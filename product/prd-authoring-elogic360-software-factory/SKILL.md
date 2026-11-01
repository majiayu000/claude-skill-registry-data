---
name: prd-authoring
description: Product Requirement Document (PRD) Authoring — Separates numbered functional requirements with explicit acceptance criteria from strictly measurable non-functional requirements.
---

# SKILL: Product Requirement Document (PRD) Authoring
## Domain: Product Discovery, Requirements Engineering, Spec-Driven Development (SDD)

**Activation triggers:** new product proposal, feature request, user stories, acceptance criteria, non-functional requirements, PRD, SDD Station 02.

---

## 1. Role & Engineering Law

The PRD Authoring skill generates formal, unambiguous Product Requirement Documents.  
It strictly obeys the **Separation of Concerns Law**:
1. **Functional Requirements (`[FR-xxx]`):** Define what the system does from a user/business capability perspective. Every FR must have at least one explicit, numbered Acceptance Criterion (`[AC-FR-xxx-y]`).
2. **Non-Functional Requirements (`[NFR-xxx]`):** Define how the system performs. Every NFR must be strictly measurable (latency, availability, security, accessibility, data integrity). Qualitative assertions ("system should be responsive", "easy to use") are strictly forbidden and fail Quality Gate 0.5.

---

## 2. Document Structure & Required Sections

Every generated PRD must follow `.factory/specifications/templates/01_prd.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Target Specification, Authors, Date.
- **Section 1: Executive Summary & Problem Statement:** Clear description of user pain point and product vision.
- **Section 2: Target Users & Personas:** Tabular persona mapping with pain points.
- **Section 3: Goals & Non-Goals:** Explicit boundaries preventing scope creep.
- **Section 4: Functional Requirements:**
  - Formatted as `### [FR-xxx]: Title`
  - Priority (High/Medium/Low)
  - User Story: "As a [persona], I want to [action] so that [benefit]"
  - Detailed Description
  - Acceptance Criteria: `[AC-FR-xxx-y]` checkboxes.
- **Section 5: Non-Functional Requirements:**
  - Formatted in a structured table with ID, Category, Target Metric, Baseline/Threshold, Measurement Method.
- **Section 6: Constraints & Dependencies:** Platform, regulatory, and cost ceilings.
- **Section 7: Quality Gate G0 Signoff.**

---

## 3. Validation Checklist (Quality Gate G0 & G0.5 Pre-Condition)

- [ ] Every functional requirement has a unique `[FR-xxx]` ID.
- [ ] Every functional requirement contains at least one testable `[AC-FR-xxx-y]` acceptance criterion.
- [ ] Every non-functional requirement has a unique `[NFR-xxx]` ID and an objective metric (e.g. `p95 < 250ms`, `uptime >= 99.9%`).
- [ ] No qualitative placeholders ("fast", "user-friendly", "scalable") exist without quantifiable metrics.
- [ ] Document saved to `.factory/specifications/<project>/01_prd.md`.
