---
name: pedi-layout
description: Design, implement, or review authenticated Pedi application shells with a collapsible sidebar, sticky utility header, breadcrumbs, and consistently directed page content. Use for dashboards, consoles, back-office products, or internal tools; do not use for public marketing navigation or isolated component styling.
---

# Pedi Layout

Build authenticated Pedi workspaces around one predictable spatial model: persistent navigation on the left, utilities in a sticky header, and vertically directed page content in an independent scroll region. Preserve the target repository's framework, routing, authorization, and existing component APIs.

## Required reference

Read [references/app-shell.md](references/app-shell.md) before making layout decisions. It captures the reusable pattern originally derived from Pedi Courts' authenticated application shell and is the portable source of truth for this skill.

Use [references/app-shell-example.md](references/app-shell-example.md) when concrete component composition would help. It packages a framework-oriented implementation example without Pedi Courts routes, permissions, or account assumptions.

Treat these references as canonical direction, not as code to copy blindly. Inspect the target project first and translate the pattern through its existing shell, sidebar, routing, responsive, and theming primitives.

## Workflow

1. Inspect the target project's root layout, authenticated shell, navigation source, page wrapper, overflow ownership, responsive breakpoints, and persisted sidebar state before editing.
2. Map the existing pieces to the canonical composition: shell provider, app sidebar, content inset, sticky utility header, optional breadcrumbs, then the page.
3. Keep structural responsibilities separate. The shell owns arrangement and state; the sidebar owns navigation presentation; the navigation source owns destinations and permissions; the header owns global utilities; the page owns title, description, page actions, width, and sections.
4. Establish one vertical scroll owner for the application content. Keep the desktop sidebar fixed and the header sticky within that scrolling context. Preserve the framework's scroll restoration mechanism when the document itself no longer scrolls.
5. Adapt navigation responsively: collapsible icon rail on desktop, off-canvas sheet on small screens, one mobile trigger in the header, and no duplicate desktop trigger.
6. Use the shared page wrapper for content direction and spacing. Place page-level actions beside the title on wider screens and below it on narrow screens; keep sections farther apart than controls within a section.
7. Validate expanded, collapsed, and mobile sidebar states; short and long pages; zero, one, and multiple breadcrumbs; narrow forms and full-width data views; keyboard focus; and light/dark themes supported by the product.

## Boundaries

- Preserve route generation, authorization, tenancy or branch scoping, and server-provided sidebar state. Layout work must not invent access or expose hidden destinations.
- Keep app areas separate when their auth models or available navigation differ. They may share shell primitives without sharing conditional business logic.
- Do not hard-code Pedi Courts route names, menu groups, organization models, or utility controls into another product.
- Do not introduce a second scrolling page wrapper, a second sidebar state owner, or per-page outer padding when shared primitives already own those concerns.
- Do not force the app sidebar pattern onto public, editorial, authentication, onboarding, or focused transactional screens whose primary task benefits from another shell.
- Prefer semantic theme tokens and established primitives. This skill governs composition and information direction, not a replacement visual design system.

## Completion check

- The content order is shell → sidebar + content inset → sticky header → optional breadcrumbs → page.
- Sidebar, header, breadcrumb, and page responsibilities do not overlap.
- Only the content inset scrolls on console screens, with restoration metadata where the router requires it.
- The current destination remains identifiable when navigation groups or the sidebar collapse.
- Mobile navigation is reachable as an accessible sheet and does not consume permanent horizontal space.
- Page headings, descriptions, actions, full-width data, narrow forms, and section spacing follow the shared direction.
- No product-specific routes, permissions, or account assumptions were copied from Pedi Courts without an equivalent in the target product.
