---
name: app-flow-mapping
description: App Flow Mapping — Maps end-to-end user journeys, screen progression, decision branches, error/empty states, and enforces zero-orphan-screen parity with UI/UX specs.
---

# SKILL: App Flow Mapping
## Domain: Interaction Design, Navigation Architecture, SDD Station 06

**Activation triggers:** user flow, navigation tree, screen map, user journey, state transitions, interaction graph, SDD Station 06.

---

## 1. Role & Engineering Law

The App Flow Mapping skill models the complete navigation and state topology of the application.  
It enforces the **Zero Orphan Screen Law**:
- Every screen referenced in the UI/UX artifacts (`uiux-brief`, `uiux-specification`) must appear in the App Flow Document screen inventory.
- Every screen defined in the App Flow Document must have a corresponding detailed specification in the UI/UX Specification.
- No navigation dead-ends or undocumented screens are permitted.

---

## 2. Document Structure & Required Sections

Every generated App Flow Document must follow `.factory/specifications/templates/03_app_flow.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD ID, Target Specification, Lead Designer, Date.
- **Section 1: Flow Architecture Overview:** Context and scope.
- **Section 2: Navigable Journey Flowchart (Mermaid):**
  - Fully valid Mermaid `flowchart TD` or `flowchart LR` diagram showing:
    - User entry points
    - Screen transition nodes (`SCR-01`, `SCR-02`, etc.)
    - Decision branch labels
    - Error fallback paths and retry loops
    - Empty state branches
    - Exit / completion nodes
- **Section 3: End-to-End User Journey Walkthroughs:**
  - Written walkthrough per primary journey (`J-01`, `J-02`, etc.).
  - Explicit specification of happy paths, decision logic, and error/empty/offline states.
- **Section 4: Screen Inventory Map:**
  - Complete table: `Screen ID | Screen Name | Route / Path | Inbound Navigation | Outbound Navigation | Associated Journeys`.
- **Section 5: Verification & Consistency Signoff.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] Valid Mermaid flowchart diagram compiles without syntax errors.
- [ ] Every primary user journey has a written step-by-step narrative.
- [ ] Error, empty, and network-offline states explicitly documented.
- [ ] Screen Inventory Table exactly matches the screens in `.factory/specifications/<project>/04b_uiux_specification.md`.
- [ ] Document saved to `.factory/specifications/<project>/03_app_flow.md`.
