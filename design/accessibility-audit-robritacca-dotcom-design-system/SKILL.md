---
name: accessibility-audit
description: Audit a component or page for accessibility violations against WCAG 2.1 AA criteria. Use when asked for an accessibility audit, a11y check, WCAG compliance check, or "is X accessible".
icon: accessibility
displayDescription: "Audits a component or page against WCAG 2.1 AA criteria. Checks semantic HTML, ARIA usage, keyboard navigation, focus styles, and colour contrast via both source code analysis and live screenshots. Reports file and line-level findings with WCAG criterion and severity."
invoke: ["accessibility audit","a11y check on [component/page]","check WCAG compliance","is [X] accessible"]
---

# accessibility-audit

Audit a component or page for accessibility violations against WCAG 2.1 AA criteria.

## When invoked

Use this skill when asked to check accessibility, run an a11y audit, or find WCAG issues — phrases like "accessibility audit", "a11y check on [component/page]", "check WCAG compliance", "is [X] accessible".

## What is already automated — read this before auditing anything

**Axe runs against the served site and fails the build.** `scripts/validate-website-a11y.mjs` loads the route sample in `scripts/served-site.mjs` in both themes and enforces WCAG 2.1 AA, so `npm run verify` and CI already cover it. It used to run over every Storybook story too; that gate went to the design system's repo with the library, so this site's own pages are the whole surface now.

```bash
npm run verify
```

If that is green, every violation axe can detect is already absent — and re-checking icon-only button names, label association, `role="dialog"` naming or ARIA parent/child relationships by hand is duplicated effort.

**This skill exists for the three things that gate does not cover:**

1. **Colour contrast — excluded from the automated gate entirely.** `color-contrast` is switched off in `scripts/validate-website-a11y.mjs` by a settled decision of Rob's. **Read that override's comment first**: it is the authoritative record of why, and the single place the details belong. Since the 2026-08-20 accessible-teal split the shipped pairs the rule used to fail all clear AA; the rule stays off because the action colour is a token consumers re-point to their own palettes, so the gate would be judging a value the system does not own. That makes contrast — every pair, everywhere — the manual auditor's job, and **the single highest-value thing to audit**: nothing else checks it. Never propose re-enabling the rule without asking Rob first.
2. **What axe cannot see.** Axe catches roughly a third of WCAG issues. It cannot tell whether alt text is *meaningful*, whether focus order makes sense, or whether a helper message *should* have been associated with its control. (Behavior a story's `play` function asserts *is* covered — `Dialog.stories.tsx` proves the modal focus trap, restore, and stacked Escape in CI — so the manual job is the overlays with no play coverage yet.) (Two such bugs once shipped undetected until a manual survey found them: Dropdown announced neither its helper text nor its error state. Both were since fixed by moving Dropdown onto `Field`, but it took the manual survey, not axe, to find them.)
3. **Website pages beyond the automated sample.** A page-level axe pass (`scripts/validate-website-a11y.mjs`, in `verify` and CI) now runs against the served site in both themes with the same rule set — but only over the route sample in `scripts/served-site.mjs`, at one desktop viewport. Full-site sweeps, mobile viewports, and any page outside that sample remain this skill's job.

Report a finding as **already-enforced** if the page-level axe pass would have caught it; that tells the reader the gate is working rather than implying a gap.

## Instructions

1. **Determine scope.** Accept one of:
   - A website page URL (e.g. `/components/button`) → audits the live rendered page

2. **Read the source files.** For each page in scope, read its `page.tsx` and `page.module.css` before taking screenshots.

3. **Structural audit (from source code).** Most items here are already enforced by axe — spend your effort on the ones marked **[manual]**, which it cannot evaluate:

   **Semantic HTML & ARIA:**
   - Interactive elements use correct roles (`button`, `link`, `checkbox`, etc.) — never a `<div onClick>` without `role` and `tabIndex`
   - Icon-only `<button>` elements have `aria-label` describing their action
   - **[manual]** `<img>` elements have *meaningful* `alt` text — axe only checks that the attribute exists; decorative images use `alt=""`
   - Form inputs are associated with `<label>` via `htmlFor`/`id`, or have `aria-label`
   - Modals and dialogs use `role="dialog"` and `aria-modal="true"`, with `aria-labelledby` pointing to the title
   - Lists use `<ul>`/`<ol>` + `<li>`, not `<div>` stacks
   - Heading hierarchy is logical — no h3 before h2, no skipped levels

   **Keyboard Navigation:**
   - **[manual]** All interactive elements are reachable by Tab, in an order that makes sense — axe cannot judge order
   - Custom interactive components handle `onKeyDown` for Enter/Space (buttons) and arrow keys (any component with roving or list focus — radio groups, segmented controls, listboxes, tablists)
   - **[manual where no `play` function covers it]** Modal/dialog *actually* traps focus while open and restores it to the trigger on close — axe sees the attributes, not the behaviour. The modal overlays share one behavior implementation (design.md's Components intro owns the contract), so a real trap/restore defect there is a finding against all of them, not one
   - Escape key closes dismissible overlays (any floating panel — tooltips, popovers, menus, dialogs, pickers)

   **Focus Styles:**
   - Every interactive element has a `:focus-visible` rule in its CSS
   - Focus ring uses the teal action token (`--color-action-primary-bg`) — design.md's teal rules are the authoritative list of sanctioned uses. Flag any `outline: none` without a visible replacement

   **Motion** (axe evaluates none of this):
   - **[manual]** Anything that animates for more than five seconds, or loops indefinitely, can be paused, stopped, or hidden (WCAG 2.2.2). CSS motion satisfies this through the reduced-motion block in `tokens-motion.css`, which carries two mechanisms and whose own header comment owns the contract: token collapse for token-consuming CSS, and a universal `*` guard that also covers hardcoded and `ds-allow(motion)`-sanctioned literal timings (an infinite loop on an off-scale duration is still guarded). Read it there rather than assuming which half applies
   - **[manual]** Animation driven from JavaScript is **outside that guard** — a `requestAnimationFrame` loop cannot be seen by CSS, so each one has to check `prefers-reduced-motion` itself. Enumerate the JS-side checks with a grep for `prefers-reduced-motion` across `website/src` — the grep is the inventory, not any list written here (the site's ambient background, which renders a single static frame under the preference, is one illustration; more exist and new ones keep arriving) — and confirm each still honours the preference rather than assuming the token layer covers it. That grep has one known blind spot: the recharts-backed charts animate their marks in from JavaScript but never contain the string — their guard is recharts' own `isAnimationActive: 'auto'` default, and design.md's chart-set spec owns the contract (a literal `true` would override the guard). Run a second grep for `isAnimationActive` across `website/src` — a clean result means the default guard holds everywhere; any explicit override is a finding to check against that spec
   - **[manual]** Motion triggered by interaction (parallax, cursor-reactive effects) is disabled under reduced motion, or is not essential (WCAG 2.3.3)

4. **Visual audit (from screenshots).** Start the preview server and screenshot the target in both light and dark mode (follow the `visual-review` skill pattern). Check:
   - **Colour contrast (the priority — nothing automated covers this):** compute the ratio for every foreground/background pair actually rendered, not just body text. Flag anything below 4.5:1 for normal text or 3:1 for large text and UI components (WCAG 1.4.3 / 1.4.11). Note which token is used. Nothing is pre-exempt: the `color-contrast` axe rule is off for every pair (see Key context point 1), so every rendered pair is this audit's job; the shipped action pairings' AA clearance is recorded in that override's comment, so cross-check against it before flagging one of them.
   - **Text sizing:** No text visually below ~12px (WCAG 1.4.4)
   - **Focus visibility:** Confirm focus rings are clearly visible in both light and dark themes

   Stop the server when done.

5. **For each issue, report:**

   ```
   website/src/components/FilterMenu/FilterMenu.tsx:84 — WCAG 4.1.2 Name, Role, Value [Critical]
   Trigger button has no accessible name. Icon-only button needs aria-label="Open filters".
   ```

   (The example is fictional by design — `FilterMenu` is not a real component; it illustrates the report shape only.)

   Severity:
   - **Critical** — blocks keyboard or screen reader users entirely
   - **Moderate** — degrades experience significantly
   - **Minor** — best practice violation, low direct impact

6. **Summarise:**
   - `X critical · Y moderate · Z minor`
   - If clean: "No accessibility violations found. Component meets WCAG 2.1 AA."
