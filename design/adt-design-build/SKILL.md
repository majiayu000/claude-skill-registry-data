---
name: design-build
description: Composite skill — design, scaffold, build, and verify a UI in one workflow. Chains ui-ux-pro-max or web-design-guidelines (audit/principles) → shadcn or tailwind-design-system (component scaffold) → impeccable or frontend-design (build) → webapp-testing (verify). Use when the task is "build this page", "design and implement X", or any new UI surface.
triggers:
  - design-build
  - ui-build-requests
  - composite skill
  - audit
  - design
---

# Design Build

End-to-end UI workflow that runs design, scaffolding, implementation, and verification
in one chained pass instead of four separate skill invocations.

## Auto-invocation triggers

- User asks to "build", "implement", "design and code", or "create a page/screen/component"
- Work involves new UI surface (route, screen, modal, dashboard tile)
- Existing UI is being significantly redesigned, not just edited

## Workflow

### Phase 1 — Design context (always)
- If the project has design tokens/system: invoke `web-design-guidelines` (audit-mode)
  to extract the relevant patterns
- If greenfield aesthetic decision: invoke `ui-ux-pro-max` or `frontend-design` for
  art-direction guidance
- Output: brief on visual hierarchy, palette, typography choices, layout pattern

### Phase 2 — Scaffold (always)
- If shadcn/components.json present: invoke `shadcn` to add required components
- Else if Tailwind: invoke `tailwind-design-system` to generate the structural
  primitives
- Else: scaffold from project conventions detected in repo

### Phase 3 — Build (always)
- Invoke `impeccable` for production UI work, or `frontend-design` for art-directed
  / experimental UI
- Implement against the Phase 1 design + Phase 2 scaffold
- Use real project conventions (file layout, import paths, state lib)

### Phase 4 — Verify (always)
- Invoke `webapp-testing` for browser-level verification: snapshot, accessibility
  check (axe-core), console errors, responsive breakpoints
- If accessibility violations or console errors: loop back to Phase 3 with the report

## Reconciliation

Output a build summary:
```
DESIGN BUILD — <surface name>
  Design:    <patterns chosen, source skill>
  Scaffold:  <components added>
  Built:     <files created/modified>
  Verified:  <a11y score, console clean Y/N, breakpoints tested>
  Screenshot: <path>
```

## Outputs / Evidence

- Design rationale (1 paragraph)
- Files created/modified
- Browser screenshot at primary breakpoint
- Accessibility report
- Console clean confirmation

## Failure / Stop Conditions

- Phase 1 cannot detect design system AND the user gave no aesthetic direction → ask
  one consolidated question (visual style + reference) before continuing
- Phase 4 finds blocking a11y violations → fix in Phase 3, do not declare done
- Browser/Playwright not available → Phase 4 falls back to static checks; mark verify
  as partial, recommend manual smoke test
