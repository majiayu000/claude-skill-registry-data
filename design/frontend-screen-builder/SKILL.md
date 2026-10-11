---
name: frontend-screen-builder
description: Build or update functional frontend pages and mobile screens that fit an existing application. Use when Codex needs to create dashboards, admin pages, customer pages, shop owner pages, rider screens, staff portals, booking screens, profile pages, settings, reports, forms, search pages, landing pages, detail pages, list pages, approval pages, payment screens, notification screens, onboarding screens, or internal tools with routing, navigation, API integration, state management, authentication, permissions, loading states, error states, empty states, responsive behavior, tests, and documentation.
---

# Frontend Screen Builder

Use this skill when a task requires building or changing an application screen, not just a visual mockup.

## Core Rule

Inspect the existing frontend architecture, similar screens, routing, design system, state management, API usage, auth behavior, and test patterns before creating or modifying a screen.

## Workflow

1. Understand the screen requirement:
   - screen name, user role, business purpose, main actions, data shown, data submitted, route or navigation entry, success behavior, error behavior, empty state, and permissions
2. Inspect existing frontend structure:
   - `pages`, `screens`, `routes`, `navigation`, `components`, `layouts`, `hooks`, `services`, `api`, `store`, `context`, `styles`, `theme`, `assets`, `types`, `utils`, and tests
3. Inspect similar screens:
   - reports, dashboards, forms, detail pages, list pages, admin pages, mobile screens, or workflow screens with similar behavior
4. Identify routing or navigation changes:
   - web routes, layout wrapper, protected route guard, sidebar/menu entry, breadcrumbs, page title, URL/query params, mobile stack/tab/drawer registration, route params, and back behavior
5. Follow existing design and styling conventions:
   - component library, tokens, spacing, typography, button styles, form fields, cards, tables, badges, icons, modals, loading indicators, empty states, and breakpoints
6. Define the layout before editing:
   - header, filters, summary, table/list, form, detail section, actions, status badges, pagination, tabs, modal, footer actions, and state containers
7. Define data requirements:
   - API endpoint or local source, request params, response fields, loading behavior, error behavior, empty behavior, refresh behavior, cache behavior, pagination/filtering/sorting, and user context
8. Use the existing API and state management pattern:
   - fetch wrapper, Axios instance, React Query/SWR hook, Redux/Zustand action, context provider, generated client, or mobile service
9. Implement required UI states:
   - loading, success/data, empty, error, unauthorized, submitting, disabled, and retry states
10. Implement forms and validation when applicable:
   - required fields, defaults, input types, validation, submit behavior, duplicate submit prevention, API validation errors, success feedback, reset, and dirty-state handling
11. Implement user actions:
   - create, edit, delete, save, cancel, approve, reject, assign, filter, search, sort, export, refresh, retry, navigate, open/close modal
12. Handle auth and permissions:
   - frontend permission checks for user experience, backend permission checks for security, role-specific navigation, scoped data, and restricted actions
13. Handle responsive and accessibility basics:
   - small screens, tablet/desktop, table overflow, button wrapping, keyboard behavior, safe area, touch targets, labels, semantic controls, focus states, contrast, and accessible errors
14. Add or update tests where practical.
15. Update documentation when the screen adds a meaningful workflow.
16. Run relevant checks discovered from project scripts or docs.
17. Summarize the screen, route, data source, UI states, actions, permissions, files changed, checks, risks, and follow-up work.

Read `references/screen-builder-checklist.md` for screen planning questions, state checklists, test ideas, and the final report format.

## Non-Negotiable Rules

- Do not create screens before inspecting existing frontend patterns.
- Do not introduce a new design style or UI library without a clear reason.
- Do not build static-only UI when the screen requires real data.
- Do not ignore loading, error, empty, unauthorized, or submitting states.
- Do not hardcode API URLs when the project uses API client utilities.
- Do not rely only on frontend permission checks for security.
- Do not expose sensitive data in the UI.
- Do not skip responsive behavior when the app supports multiple screen sizes.
- Do not duplicate components unnecessarily.
- Do not make unrelated refactors while building the screen.
- Do not claim the screen is complete if it is unconnected, untested, or intentionally UI-only without saying so.

## Output Contract

When using this skill, provide:

1. Screen created or updated.
2. User role and use case.
3. Route or navigation path.
4. Existing patterns followed.
5. Data source and API integration.
6. UI states handled.
7. User actions implemented.
8. Auth, permission, responsive, and accessibility notes.
9. Files changed.
10. Tests/checks or manual verification.
11. Risks and follow-up recommendations.
