---
name: lanekeeper-ui-from-design
description: 'How to build Lanekeeper''s React UI from the Claude Design handoff, where screens are .dc.html reference files in design/handoff/screens/. Covers inspecting a reference screen, extracting tokens into Tailwind and CSS variables, mapping parts to shadcn/ui, re-implementing without exported markup, inline scripts or styles (CSP and Trusted Types), wiring data through generated orval hooks and SSE invalidation, covering every state in the States index, keyboard maps, performance (bundle budget, lazy Monaco, virtualisation) and visual-regression tests against the reference. Use this skill for any work in web/: a new screen, a component, restyling, a state, an accessibility fix or a visual test. Use it even when the task sounds small, because screens must match the design and pass the CSP and visual gates.'
---

# Building UI from the design handoff

The design is the source of truth for how the app looks and behaves. The OpenAPI spec is the source of truth for data, and `docs/security.md` for constraints. When the design conflicts with security or a performance budget, security and performance win, and the difference is recorded in `design/DEVIATIONS.md` (D71).

## Inputs

- **`design/handoff/screens/*.dc.html`:** one reference file per screen or state, exported from Claude Design. Treat these as **reference only**. They never ship, and nothing in `web/` imports them.
- **The "Engineering handoff" page** in the handoff: tokens, the component map to shadcn, the screen inventory with routes, keyboard maps, and the States index.
- **`design/00`–`14`:** the prompts that produced the design. Read the matching one when you need the reasoning behind a screen.

## Step 1: Inspect the reference before writing code

Open the `.dc.html` file and work out how it's structured: its sections, repeated parts, states, and any CSS custom properties. Don't assume a particular format; read what's actually there. Write a short inventory into your plan. For each screen, cover:

- the route;
- the regions;
- the components, each mapped to shadcn;
- the data each region needs, mapped to OpenAPI operations;
- the states it shows;
- the keyboard shortcuts.

If the reference needs a script to render, open it only in a sandboxed browser context, such as Playwright with a strict CSP. Never execute it inside the app.

## Step 2: Tokens first

- Copy colours, spacing, radii, type sizes and the drift-state palette into `web/src/styles/tokens.css`, as CSS variables for light and dark, then reference them from the Tailwind theme.
- A token parity test compares your variables with the handoff token list. Keep it green.
- Fonts (Inter, JetBrains Mono) are self-hosted under `web/public/fonts`, with no external origins (S12).

## Step 3: Re-implement; never paste

- Build each screen from shadcn/ui components and Tailwind classes, following the component map.
- Never copy exported markup, inline `<script>`, inline `style=` attributes or event-handler attributes from the `.dc.html` file. Pasted markup breaks the CSP and Trusted Types (S12), and it rots as soon as the design changes.
- Statuses are always a colour plus an icon plus a label, never colour alone.
- Rows have fixed heights (28 or 32 px), as designed, so lists can be virtualised.

## Step 4: Data and live updates

- Use only the generated orval hooks and types; never hand-write API types. In development and tests, use the generated MSW mocks.
- Query keys include content hashes or versions where possible, so cached data is safe to reuse.
- SSE events (`/api/v1/events`) invalidate the precise query keys they affect. `Resync` refetches only the visible views.
- Writes send `X-CSRF-Token`, an `Idempotency-Key`, and the expected hash.

## Step 5: Every state, every role

Implement every state the States index lists for your screen:

- loading skeletons that match the final layout;
- empty;
- error, showing the problem title and the request id;
- permission: pending, Viewer, and no Operator role;
- agent offline ("as of" a time);
- live updates paused;
- truncated results;
- 409 (re-apply on top), 423 (editing locked) and 202 (sent for approval);
- expired token.

For roles, disable controls with a tooltip rather than hiding them. The server enforces permissions regardless.

## Step 6: Performance (P10)

- The initial JavaScript bundle stays under 250 KB gzipped. Lazy-load Monaco on the file and diff routes only.
- Virtualise trees, grids, history lists and search results with TanStack Virtual.
- Diffs render server-provided hunks, including inline ranges. Never diff 6,000-line files in the browser.

## Step 7: Verify against the design

- **Visual regression:** Playwright `toHaveScreenshot` at 1440×900, in light and dark, for each screen and state in the States index. Compare against reference images rendered from the `.dc.html` files in a sandboxed context. Keep the pixel threshold small, and agree on any increase with the design owner.
- **Keyboard:** Playwright tests that drive each screen using only the keyboard map.
- **Accessibility:** axe checks on every main screen, with no violations.
- **CSP:** a Playwright run under the production CSP, with no violation reports.
- **Deviations:** every intentional difference from the design goes in `design/DEVIATIONS.md`, with its reason (security, performance or accessibility). The design owner approves each one.

## Common mistakes

- Using hex colours in components instead of tokens. Dark mode breaks.
- Using `dangerouslySetInnerHTML` for convenience. The lint blocks it; the only exception is server-sanitised docs HTML.
- Building "pending restart" chips. The current model has four pickup states: Live, Live by HH:MM, Needs notify or restart, and Needs config-server restart.
- Showing a single tenant branch in headers. Swimlanes have a set of tenants.
- Forgetting the base-or-tenant choice and the repo path preview in the PR dialog.

`references/screen-checklist.md` has a per-screen checklist to paste into your plan.
