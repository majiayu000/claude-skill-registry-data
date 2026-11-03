---
name: google-design-md
description: >
  Standardized format and tools for describing design systems in single machine-readable,
  human-friendly DESIGN.md files combining YAML frontmatter design tokens and markdown prose.
license: Apache-2.0
---

# Google DESIGN.md Specification & Skill

Use this skill when creating, updating, or validating a `DESIGN.md` file that governs an AI agent's frontend implementation.

## DESIGN.md Structure

A valid `DESIGN.md` file contains two integrated layers:

### 1. Machine-Readable Tokens (YAML Frontmatter)
```yaml
---
name: "Acme Design System"
version: "1.0.0"
colors:
  primary: "#0A84FF"
  primary_foreground: "#FFFFFF"
  canvas: "#090A0F"
  surface: "#141721"
  border: "#232838"
  text_primary: "#F3F4F6"
  text_secondary: "#9CA3AF"
typography:
  font_display: "Space Grotesk, sans-serif"
  font_body: "Inter, sans-serif"
  scale:
    xs: "0.75rem"
    sm: "0.875rem"
    base: "1rem"
    lg: "1.125rem"
    xl: "1.25rem"
    "2xl": "1.5rem"
radii:
  sm: "4px"
  md: "8px"
  lg: "12px"
  full: "9999px"
spacing:
  unit: "4px"
---
```

### 2. Human-Readable Guidelines (Markdown Prose)
- **Tone & Mood**: Define aesthetic archetype (e.g. brutalist, hyper-minimal, cyber, swiss).
- **Layout Rules**: Max widths, grid structure, hierarchy, z-index conventions.
- **Component Patterns**: Button states, form styling, modal behavior, card elevation.
- **Forbidden Patterns**: Explicit list of AI slop to avoid (e.g., generic centered heroes, cliché gradients, excessive card wrapping).
