---
name: ui-concept-first
description: "Sets visual direction from Figma, screenshots or an existing design system for major UI implementation."
---

# UI Concept First

Establish enough visual evidence for a major new UI or redesign. Bible owns the
reference choice and product constraints; author skills own their design process.

An existing design system, verified current screenshot or selected Figma frame
can provide the target. Read `design-system-extractor` only when the reference
needs implementation constraints extracted. Do not route through `ui-router`
again for an already clear task or require a new concept for ordinary changes.

When a direction is missing, select the complete original provider exposed in
the current session: `interface.interface-design` for working app screens;
`impeccable.impeccable` with its `shape` reference for UX planning;
`product-design:ideate` for requested visual alternatives; or an exposed Figma
provider for editable design work. Use `ui-business-apps` for the business-app
owner constraints. Keep native plugin and reviewed upstream ownership; provider
files alone do not establish exposure.

Generated imagery is optional and only useful when it helps the requested
surface. Dashboard and CRM interactions may be better represented by a working
prototype or screen reference. No image-generation or recurring approval step
is required by this owner policy. Preserve the user's selected direction and
scope, and report unavailable providers or missing evidence precisely.

Use `playwright-visual-qa` when the rendered result needs visual verification;
select other `ui-qa` evidence only as the task requires.
