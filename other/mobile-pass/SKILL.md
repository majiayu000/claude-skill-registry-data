---
name: mobile-pass
description: Makes ChefFlow UI work mobile-first and proves affected routes on phone viewports before build closeout. Use when building, queueing, reviewing, or verifying any user-facing page, layout, form, table, modal, navigation, or interaction flow that mobile users may touch.
user-invocable: true
---

# Mobile Pass

ChefFlow's primary runtime assumption is that real users are often on phones. Treat mobile defects as product defects, not polish.

## When To Use

Use this skill for any work that touches:

- Public, chef, client, admin, staff, or partner UI.
- Navigation, dashboards, lists, tables, cards, forms, dialogs, drawers, sheets, menus, search, filters, uploads, onboarding, checkout, booking, messaging, or settings.
- Queue specs or build prompts for UI work.
- Finish-gate verification for fired queue items with visible behavior.

Skip only for backend-only changes with no user-visible surface, and say why.

## Intake And Queue Spec

Before queueing UI work, add mobile shape to the spec:

- Primary mobile user journey and the first screen they land on.
- Affected routes and roles.
- Required actions that must be reachable with touch.
- Small-screen acceptance criteria for layout, scrolling, forms, dialogs, tables, sticky controls, empty states, and errors.
- Mobile verification command using `node scripts/mobile-pass.mjs`.

If the user gives a casual idea, follow Build Queue First: clarify the mobile outcome before queueing or building.

## Build Philosophy

Start from the phone workflow, then expand to desktop.

- Prioritize scanability, short labels, reachable primary actions, and predictable back/close behavior.
- Prefer stacked sections, compact controls, drawers/sheets, and horizontal table alternatives that preserve meaning.
- Keep touch targets usable, required actions visible, and destructive actions confirmed.
- Avoid hover-only affordances, desktop-only sidebars, clipped sticky footers, and hidden submit buttons.
- Check soft keyboard behavior for forms and search.
- Check loading, empty, error, and permission states at mobile widths.

## Required Verification

For fired UI queue items, mobile proof is blocking before done.

1. Confirm the canonical app server is the one being verified: `http://localhost:3100`.
2. Hard refresh affected routes on a mobile viewport.
3. Run a focused mobile pass:

```powershell
node scripts/mobile-pass.mjs --routes "/,/chefs" --scope public --mode quick
```

For authenticated/app routes, include role-qualified routes when useful:

```powershell
node scripts/mobile-pass.mjs --routes "chef:/dashboard,chef:/clients" --scope all --mode quick --queue-id BQ-123 --append-proof-pack
```

Then require the mobile gate in closeout:

```powershell
node .agents/skills/build-queue/scripts/build-queue.mjs finish-check --ids BQ-123 --require-mobile
```

Use `--mode full` for broad route, layout-system, shell, navigation, or design-system changes.

## Proof Pack Requirements

The proof pack must include:

- Mobile acceptance evidence.
- Exact URL verified, normally `http://localhost:3100`.
- Routes and roles covered.
- Mobile pass report path from `reports/mobile-pass/`.
- Screenshot/audit directory from `reports/mobile-audit/`.
- Console, network, runtime, and horizontal-overflow result.
- Any unresolved mobile risks or partial-work notes.

Do not move a fired UI queue item to `done` when mobile proof is missing, stale, or failing.

## Review Checklist

- No horizontal page overflow at phone widths.
- No clipped text, controls, or modal content.
- Primary action is visible and reachable.
- Forms can be completed with the soft keyboard open.
- Tables/lists preserve key data and actions.
- Navigation open/close works with touch.
- Loading, empty, error, and permission states fit.
- Screenshots prove the route actually changed and rendered.
