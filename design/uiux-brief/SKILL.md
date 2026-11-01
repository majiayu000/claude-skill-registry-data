---
name: uiux-brief
description: UI/UX Design Brief — Short-form stakeholder alignment document establishing design personality, differentiators, screen goals, breakpoints, and accessibility bar.
---

# SKILL: UI/UX Design Brief
## Domain: Product Design, Design Alignment, SDD Station 06

**Activation triggers:** design brief, visual design tone, design personality, breakpoint strategy, user goals per screen, a11y baseline, SDD Station 06.

---

## 1. Role & Alignment Purpose

The UI/UX Brief skill creates an executive 1-to-2 page design foundation document. Its primary objective is achieving total alignment between product management, engineering leads, and designers on aesthetics, platform constraints, and accessibility requirements *before* detailed screen mocking and component engineering begin.

---

## 2. Document Structure & Required Sections

Every generated UI/UX Brief must follow `.factory/specifications/templates/04a_uiux_brief.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD ID, Target Specification, Design Lead, Date.
- **Section 1: Executive Purpose & Design Scope:** Context and core objectives.
- **Section 2: Target Platforms & Display Environments:** Explicitly checked platforms (Desktop Web, Mobile Web, etc.).
- **Section 3: Brand Personality, Tone & Aesthetic Principles:**
  - Tone & Voice definitions.
  - Key visual differentiators.
  - Visual mood and aesthetic style.
- **Section 4: Primary User Goals by Core Screen:** Tabular mapping of Screen ID, Screen Name, Primary Goal, and Key Info.
- **Section 5: Responsive Breakpoint Matrix:** Standard 4-band breakpoint definitions (Mobile: 320-639px, Tablet: 640-1023px, Desktop: 1024-1439px, Wide: 1440px+).
- **Section 6: Accessibility & Compliance Bar:** WCAG 2.2 AA target, contrast ratios, and keyboard navigation baselines.
- **Section 7: Stakeholder Alignment Signoff.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] Clear design tone defined without contradictory adjectives.
- [ ] Core screen goals correspond with PRD personas.
- [ ] Breakpoint bands clearly demarcated with pixel ranges.
- [ ] WCAG 2.2 AA baseline formally recorded.
- [ ] Document saved to `.factory/specifications/<project>/04a_uiux_brief.md`.
