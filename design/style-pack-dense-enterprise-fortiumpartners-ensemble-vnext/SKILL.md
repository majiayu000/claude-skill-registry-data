---
name: style-pack-dense-enterprise
description: >
  Dense data and enterprise: compact tables and forms, small type, many items per screen, clear states. For data-heavy tools.
disable-model-invocation: true
---

# style-pack-dense-enterprise

A style pack for the design direction: dense data / enterprise. Chosen by name in `design.md`.

## The look

- Type: small, tabular figures for numbers, a tight scale with clear label and value roles.
- Colour: neutral surfaces; colour carries status and severity, not decoration.
- Spacing: tight rows and compact padding; align to a strict grid.
- Radius: small.
- Density: high; more rows and columns visible before scrolling.
- Motion: almost none; instant feedback.

## Do and don't

- Do: prefer tables, filters, bulk actions and visible state; keep labels and units adjacent to values.
- Don't: hide data behind hover or tabs, or pad rows for looks.

## Within the design system

This pack never overrides a token and never replaces a component. It guides the choices the
design system leaves open: layout, hierarchy, spacing between groups, emphasis and imagery. How
far those choices may depart from today's screens is the departure latitude in `design.md`; the
pack works inside that latitude. Where the system already decides something, the system wins.
