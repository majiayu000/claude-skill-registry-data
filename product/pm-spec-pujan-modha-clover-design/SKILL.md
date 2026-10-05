---
name: pm-spec
description: |
  Product requirements document (PRD) with user stories, acceptance criteria,
  wireframes, and release checklist. Use for "PRD", "spec", "requirements".
triggers:
  - "prd"
  - "product spec"
  - "requirements"
  - "spec document"
  - "feature spec"
df:
  mode: document
  platform: desktop
  scenario: product
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# PM Spec Skill

Produce a product requirements document.

## Sections
1. **Header**: feature name, author, date, status (draft/review/approved).
2. **Overview**: 1-paragraph summary + 3–5 bullet goals.
3. **User stories**: table — as a [role] I want [action] so that [benefit].
4. **Acceptance criteria**: numbered list with ✓ checkboxes.
5. **Wireframes**: placeholder blocks labeled "Mobile / Desktop / Edge case".
6. **Open questions**: highlighted box.
7. **Release checklist**: table — item | owner | status.
8. **Appendix**: related docs, metrics, rollback plan.

## Rules
- Clean, scannable. Hierarchy via heading size, not color.
- Wireframes: gray placeholder blocks with labels, not detailed mockups.
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS.
