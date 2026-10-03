---
name: open-design-ui-library
description: >
  Use the local OpenDesign design-system library when building, redesigning,
  or reviewing UI. Triggers: making UI, frontend design, SaaS UI, dashboard,
  landing page, mobile app, design system, make it look better. Skip when the
  task is backend-only or the user supplied a stricter design spec.
---

# OpenDesign UI Library

Goal: use proven product design systems and craft rules from `sources/open-design` before inventing UI styling.

## When To Use

- Building a new page, app, dashboard, mobile flow, deck, or marketing surface.
- Improving an existing UI that looks generic, noisy, or "AI-generated."
- Choosing CSS tokens, typography, spacing, component shape, and interaction states.

## Workflow

1. Identify the product surface: dashboard, SaaS landing, docs, pricing, mobile, content/editorial, or workflow tool.
2. If editing an existing app, inspect its local tokens, theme, component
   primitives, screenshots, or visual tests before loading external inspiration.
3. Read `references/open-design-ui-library.md` and choose one source design system, plus at most one secondary influence.
4. If the fit is unclear, use the catalog in `references/open-design-ui-library.md` before reading source files.
5. Load only the matching `sources/open-design/design-systems/<slug>/DESIGN.md` file and any needed craft file from `sources/open-design/craft/`.
6. Translate the system into local tokens/components instead of copying brand assets, marks, or proprietary copy.
7. Apply craft gates before finalizing:
   - no default purple/blue gradient hero unless the selected system calls for it
   - no emoji feature icons
   - no invented metrics
   - no filler copy
   - visible focus states and labelled inputs for interactive UI
8. Validate visually with screenshots when a browser target is available.

## Output

```md
Design system used:
Reference files:
Key tokens/components applied:
Existing local design system preserved or mapped:
Craft checks:
Validation:
```

## Skip When

- The user provided a Figma/design spec that must be followed exactly.
- The task is backend, data, CLI, infra, or test-only.
- The requested UI is intentionally unstyled or wireframe-only.

## Validation

- The selected design-system reference is named.
- Existing local tokens/components are preserved, or the mapping is stated.
- UI changes are checked in a browser/screenshot when available.
- Accessibility basics are present: focus states, labels, contrast, and non-overlapping text.
