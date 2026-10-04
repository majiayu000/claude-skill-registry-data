---
name: a11y
version: 1.0.0
description: |
  Accessibility audit for frontend changes — WCAG 2.2 AA, screen-reader
  compatibility, keyboard navigation, focus management, ARIA correctness, color
  contrast, and reduced-motion. Static diff-scoped analysis (safe to auto-run) plus
  an optional dynamic axe pass against a running app. Use when asked to "check
  accessibility", "a11y audit", "screen reader check", "WCAG", "is this
  accessible", "keyboard navigation", "ARIA review", or after heavy frontend work.
triggers:
  - a11y
  - accessibility audit
  - screen reader check
  - wcag
  - is this accessible
  - keyboard navigation check
  - aria review
argument-hint: '<optional: paths/globs to scope, or a dev URL for the dynamic pass>'
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Task
  - WebFetch
---

# /a11y

Audit frontend changes for accessibility. Two layers:

- **Static (safe to auto-run, diff-only):** read the changed JSX/TSX/Vue/Svelte/
  HTML/CSS and flag accessibility defects from the markup itself — no browser, no
  external tools.
- **Dynamic (recommend / opt-in):** when a dev URL is reachable, run an
  axe-core / Chrome DevTools MCP pass for computed contrast, focus order, and the
  screen-reader accessibility tree — things you can't see from source alone.

## Hard rules

- **Ground every finding in evidence:** file:line, the offending element, the WCAG
  success criterion (e.g. 1.1.1, 2.4.3, 4.1.2), and the concrete user impact
  ("screen-reader users hear an unlabeled button", "keyboard users can't reach X").
- **Severity by user impact, not by rule pedantry.** A control no screen-reader or
  keyboard user can operate is CRITICAL; a missing `lang` attribute is LOW.
- **Smallest correct fix.** Prefer native semantics (`<button>`, `<label>`, `<nav>`)
  over ARIA bolted onto a `<div>`. The first rule of ARIA: don't use ARIA if a
  native element does the job.
- **Scope to the diff.** Audit changed components, not the whole app.

## When this is worth running (the trigger)

Run on **heavy frontend changes likely to affect assistive tech**, not every style
tweak. Trigger when the diff includes any of:

- new/changed **interactive components** (buttons, links, menus, tabs, dialogs,
  tooltips, accordions, comboboxes, drag-drop)
- **forms** (inputs, labels, validation, error messaging)
- **images / media / icons** (alt text, decorative vs informative, captions)
- **ARIA** attributes, `role=`, `tabindex`, or `aria-*` props
- **focus / keyboard** handling (`onKeyDown`, `focus()`, focus traps, route changes,
  modal open/close)
- **color / contrast** changes in styles, or conveying state by color alone
- **motion / animation** (autoplay, transitions, parallax)

A pure copy/spacing CSS change with none of the above does **not** need `/a11y`.

## What to check (WCAG 2.2 AA, screen-reader first)

1. **Semantics & landmarks** — real `<button>`/`<a>`/`<nav>`/`<main>`; one `<h1>`,
   no skipped heading levels; lists are lists. (1.3.1, 2.4.1)
2. **Name, role, value** — every control has an accessible name (visible `<label>`,
   `aria-label`, or text); custom widgets expose correct role + state. Flag
   `<div onClick>` with no role/tabindex/keyboard handler. (4.1.2)
3. **Images & icons** — informative images have meaningful `alt`; decorative ones
   have `alt=""`/`aria-hidden`; icon-only buttons have an accessible name. (1.1.1)
4. **Forms** — every input has an associated `<label for>`/`aria-labelledby`; errors
   are programmatically tied (`aria-describedby`) and announced; `autocomplete`
   where relevant. (1.3.1, 3.3.1, 3.3.2)
5. **Keyboard** — all interactive elements reachable and operable by keyboard;
   visible focus indicator; logical focus order; no keyboard traps; skip link for
   repeated nav. (2.1.1, 2.4.3, 2.4.7, 2.1.2)
6. **Focus management** — on modal/dialog open, focus moves in and is trapped; on
   close, focus returns to the trigger; on SPA route change, focus/announce the new
   view. (2.4.3)
7. **Screen-reader announcements** — dynamic updates use `aria-live`/`role=status`;
   visually-hidden text (`sr-only`) where context is visual-only;
   `aria-hidden` never on focusable content. (4.1.3)
8. **Color & contrast** — text ≥ 4.5:1 (≥ 3:1 large), UI/graphics ≥ 3:1; never
   convey meaning by color alone (pair with icon/text). (1.4.3, 1.4.11, 1.4.1)
9. **Motion & reduced motion** — honor `prefers-reduced-motion`; no autoplay > 5s
   without controls; nothing flashes > 3×/sec. (2.3.1, 2.2.2)
10. **Reflow & zoom** — usable at 200% zoom / 320px without loss of content; no
    `user-scalable=no`; touch targets ≥ 24×24px. (1.4.10, 1.4.4, 2.5.8)

## Steps

1. **Scope** — resolve the changed frontend files (or `$ARGUMENTS` globs). If none
   match the trigger, say so and stop.
2. **Static pass** — Grep/Read the changed files for the defect signatures in each
   dimension above. Record findings with file:line + WCAG criterion + impact.
3. **Dynamic pass (if a dev URL is given or in `CLAUDE.md`/`package.json`)** — load
   the affected routes and run axe-core via the `chrome-devtools` MCP (or a project
   axe runner). Report computed contrast failures, focus-order issues, and
   accessibility-tree gaps the static pass can't see. If no URL is reachable, record
   **dynamic pass SKIPPED (no dev server)** — don't silently drop it.
4. **Report** — group by severity; give the smallest fix per finding (prefer native
   semantics). Draft the corrected markup as a code block; do not apply it.

## Report format

```markdown
# Accessibility audit — <scope> @ <date>

## CRITICAL (blocks assistive-tech users)
- <file:line> — <element> — WCAG <criterion> — <impact> — <fix>

## SERIOUS / MODERATE / MINOR
- …

## Dynamic pass
- axe: N violations (or: SKIPPED — no dev server)
```

## Anti-patterns (do not do)

- Adding ARIA to "fix" something a native element already does correctly.
- Flagging style-only diffs with no interactive/semantic/contrast change.
- Reporting "low contrast" without the measured ratio (use the dynamic pass).
- Applying fixes — this audits and drafts; the user (or `/design-review`) applies.

## Related commands

- `/design-audit` — broader visual/UX audit; `/a11y` is the deeper accessibility
  layer. Run them together on UI changes.
- `/web-perf` — the performance counterpart for frontend changes.
- `/design-review` — *fixes and commits* visual + a11y issues this audit finds.
- `/qa-only` — functional browser QA; pairs with `/a11y` (works + accessible).
