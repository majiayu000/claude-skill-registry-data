---
name: "ux-ui-design"
description: 'Design user experiences with wireframing, prototyping, user flows, accessibility, and production-ready HTML prototypes. Use when creating wireframes, building interactive prototypes, designing user flows, implementing accessibility standards, or producing HTML/CSS design deliverables.'
metadata:
 author: "AgentX"
 version: "2.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 agents: ["ux-designer", "agent-x"]
 frameworks: ["html-css", "figma", "tailwind", "bootstrap"]
 output-formats: ["html", "css", "markdown", "mermaid"]
---

# UX/UI Design & Prototyping

> **Purpose**: Create user-centered designs, wireframes, prototypes, and production-ready HTML/CSS interfaces.

---

## When to Use This Skill

- Creating wireframes or high-fidelity mockups
- Building interactive HTML/CSS prototypes
- Designing user flows and information architecture
- Implementing accessibility (WCAG) standards
- Setting up design systems or component libraries

## Prerequisites

- Basic HTML/CSS knowledge for prototyping
- Design tool access

## Decision Tree

Use this to pick the right UX approach for your task:

```
Start: What is the deliverable?
|
+- New feature / epic?
| - 1. User Research -> 2. IA -> 3. Wireframes -> 4. User Flows
| -> 5. Hi-Fi Mockups -> 6. HTML Prototype -> 7. Usability Test
|
+- Bug fix / small change?
| - Skip to step 5 (Hi-Fi) or 6 (HTML Prototype)
|
+- Design system update?
| - Jump to Design Systems - update tokens + components
|
+- Accessibility audit?
| - Jump to Accessibility - run checklist + fix
|
- Responsive issue?
 - Jump to Responsive Design - breakpoint check + fix
```

---

## Table of Contents

1. [User Research & Analysis](#user-research--analysis)
2. [Information Architecture](#information-architecture)
3. [Wireframing](#wireframing)
4. [User Flows](#user-flows)
5. [High-Fidelity Mockups](#high-fidelity-mockups)
6. [Interactive Prototypes](#interactive-prototypes)
7. [HTML/CSS Prototypes](#htmlcss-prototypes)
8. [Design Systems](#design-systems)
9. [Accessibility (A11y)](#accessibility-a11y)
10. [Responsive Design](#responsive-design)
11. [Usability Testing](#usability-testing)
12. [Best Practices](#best-practices)
13. [Tools & Resources](#tools--resources)

---

## Best Practices

### [PASS] DO

**Research & Wireframing:**
- Start with lo-fi sketches; iterate on paper first
- Use real content, never lorem ipsum in final designs
- Annotate interactions on every wireframe
- Test with diverse user demographics

**Design & Prototyping:**
- Follow the 8px spacing grid
- Design for ALL states: empty, loading, error, success
- Build production-ready HTML/CSS prototypes (mandatory)
- Use semantic HTML5 + ARIA attributes from the start
- Use CSS custom properties for all design tokens
- Validate HTML & CSS

**Collaboration:**
- Document every design decision
- Share prototypes early and gather developer feedback
- Version-control design files
- Hand off with detailed specifications

### [FAIL] DON'T

- Skip user research or design in isolation
- Leave placeholder content in final deliverables
- Ignore edge cases and error states
- Forget mobile/tablet breakpoints
- Neglect accessibility until the end
- Hardcode values instead of using design tokens
- Use large unoptimized images
- Inline all styles (use external stylesheets)
- Block rendering with synchronous scripts

---

## Tools & Resources

### Design & Wireframing

| Tool | Use Case | Link |
|------|----------|------|
| Figma | Collaborative design | [figma.com](https://figma.com) |
| Sketch | Mac design | [sketch.com](https://sketch.com) |
| Penpot | Open-source design | [penpot.app](https://penpot.app) |
| Balsamiq | Quick wireframes | [balsamiq.com](https://balsamiq.com) |
| Whimsical | Flowcharts + wireframes | [whimsical.com](https://whimsical.com) |
| Excalidraw | Hand-drawn diagrams | [excalidraw.com](https://excalidraw.com) |

### Prototyping

| Tool | Use Case | Link |
|------|----------|------|
| CodePen | Quick HTML/CSS/JS | [codepen.io](https://codepen.io) |
| Tailwind CSS | Utility-first CSS | [tailwindcss.com](https://tailwindcss.com) |
| Bootstrap | Component framework | [getbootstrap.com](https://getbootstrap.com) |

### Accessibility

| Tool | Use Case | Link |
|------|----------|------|
| WAVE | Accessibility checker | [wave.webaim.org](https://wave.webaim.org) |
| axe DevTools | Browser extension | [deque.com/axe](https://www.deque.com/axe) |
| WCAG Quick Ref | Guidelines | [w3.org/WAI](https://www.w3.org/WAI/WCAG21/quickref/) |

### Inspiration

[Dribbble](https://dribbble.com) - [Behance](https://behance.net) - [awwwards](https://awwwards.com)

---

## Reference Files

Detailed code blocks and templates are extracted into dedicated reference files:

| Reference | Contents |
|-----------|----------|
| [html-prototype-code.md](references/html-prototype-code.md) | Full HTML/CSS/JS prototype code (dashboard, modals, forms, tokens) |
| [research-templates.md](references/research-templates.md) | Persona template, user journey map template |
| [accessibility-patterns.md](references/accessibility-patterns.md) | Screen reader markup, keyboard navigation JS, ARIA patterns |
| [responsive-patterns.md](references/responsive-patterns.md) | Breakpoint CSS, responsive grid, mobile-first examples |
| [usability-testing-template.md](references/usability-testing-template.md) | Full usability test plan, script, and results template |

---

**Related Skills:**
- [Frontend/UI Development](../development/frontend-ui/SKILL.md)
- [React Framework](../development/react/SKILL.md)
- [Accessibility](../architecture/accessibility/SKILL.md)

---

**Version**: 2.0.0 - **Last Updated**: February 10, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Prototype not accessible | Run WAVE or axe-core audit, ensure ARIA labels and keyboard navigation |
| Inconsistent design across pages | Create a design token system with shared colors, spacing, typography |
| User flow too complex | Reduce steps to 3-5 maximum, add progress indicators |

## References

- [Research Ia Wireframing](references/research-ia-wireframing.md)
- [Flows Mockups Prototypes](references/flows-mockups-prototypes.md)
- [Design Systems A11y](references/design-systems-a11y.md)