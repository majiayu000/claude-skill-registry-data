---
name: responsive-ui
description: Create, review, and fix responsive user interfaces across mobile, tablet, laptop, and desktop sizes. Use when Codex needs to work on dashboards, admin portals, landing pages, forms, booking screens, reports, settings, profile pages, tables, data lists, mobile-first screens, customer-facing pages, shop owner screens, rider workflows, staff portals, internal tools, modal-heavy interfaces, card layouts, navigation menus, filter/search screens, layout overflow, spacing, text wrapping, touch targets, responsive forms, responsive tables, drawers, modals, and screen-specific usability.
---

# Responsive UI

Use this skill when a screen must remain usable and professional across real device sizes.

## Core Rule

Responsive UI should adapt to the user's task on each device. Do not treat desktop layout as complete unless mobile, tablet, laptop, and desktop behavior have been considered or the limitation is clearly stated.

## Workflow

1. Understand the screen and target users:
   - screen name, user role, main task, likely devices, mobile-first or desktop-first assumption, customer-facing or internal use, and whether the screen has dense data
2. Inspect existing responsive patterns:
   - breakpoints, CSS framework, Tailwind utilities, media queries, grid/flex patterns, layout components, mobile navigation, responsive tables, responsive forms, modal behavior, and dashboard layouts
3. Identify screen sizes or layout cases to consider:
   - small mobile, large mobile, tablet, small laptop, desktop, mobile app safe areas, orientation, and keyboard-open behavior when forms are involved
4. Review page layout:
   - container width, horizontal overflow, spacing, grid behavior, flex wrapping, columns, sidebar, header, footer, alignment, and scroll behavior
5. Review navigation:
   - sidebar collapse, drawers, bottom nav, tabs, breadcrumbs, back buttons, header actions, active states, and whether critical actions stay reachable
6. Review cards, dashboard widgets, and dense information:
   - stacking, grid collapse, readable numbers, label wrapping/truncation, icon sizing, spacing, and information priority
7. Review tables and data lists:
   - horizontal scroll, card-list mobile alternative, hidden low-priority columns, row actions, filters, pagination, sticky headers, and readable text wrapping
8. Review forms:
   - full-width inputs on mobile, label readability, visible errors, usable selects/date inputs, keyboard behavior, reachable submit action, and two-column-to-one-column stacking
9. Review buttons and touch targets:
   - tap area, spacing, icon-only buttons, disabled states, primary action visibility, destructive action placement, and mobile thumb reach when relevant
10. Review text overflow:
   - long names, emails, addresses, IDs, labels, button text, titles, table cells, error messages, and empty states
11. Review modals, drawers, and overlays:
   - width, height, scrolling, close button, keyboard behavior, form actions, full-screen or bottom-sheet mobile behavior, and off-screen overflow
12. Review images, media, icons, spacing, density, and scroll behavior.
13. Review responsive data priority:
   - primary information, secondary information, collapsed details, actions moved into menus, and detail-page handoff
14. Check accessibility and mobile usability basics.
15. Consider performance impact from duplicated desktop/mobile markup, heavy tables, large images, and unnecessary responsive state.
16. Add tests or manual responsive QA checks where practical.
17. Run relevant checks discovered from project scripts or docs.
18. Summarize devices considered, layout changes, navigation, tables/lists, forms, overlays, text overflow, checks, risks, and follow-up recommendations.

Read `references/responsive-ui-checklist.md` for breakpoint guidance, component-level checks, responsive table strategies, mobile usability checks, manual QA checklist, and the final report format.

## Non-Negotiable Rules

- Do not assume desktop layout is enough.
- Do not ignore mobile users.
- Do not create unexpected horizontal page scroll.
- Do not hide critical actions without an alternative.
- Do not make tap targets too small on mobile.
- Do not rely on hover-only interactions for mobile.
- Do not let long text break layouts.
- Do not use fixed widths that fail on small screens unless justified.
- Do not create modals that overflow off-screen.
- Do not make tables unusable on mobile.
- Do not introduce a new layout system unless approved.
- Do not break existing design system conventions.
- Do not sacrifice the main user task for decoration.
- Do not claim responsive support without checking common screen sizes or explaining the limitation.

## Output Contract

When using this skill, provide:

1. Screen reviewed or improved.
2. Target users and device assumptions.
3. Screen sizes considered.
4. Layout changes by desktop, tablet, and mobile.
5. Navigation behavior.
6. Cards, tables, lists, forms, buttons, text, and overlay behavior.
7. Accessibility and usability notes.
8. Files changed.
9. Tests/checks or manual responsive QA.
10. Risks and follow-up recommendations.
