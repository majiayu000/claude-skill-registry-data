---
name: forge-a11y
description: "Playbook for WCAG 2.2 audits: axe, keyboard (gebruik bij toegankelijkheid)."
# Q3 fix-round original description (listing budget): "Playbook for WCAG 2.2 audits: axe, keyboard, focus, contrast (gebruik bij toegankelijkheid)."
---

<!--
  Source: https://github.com/wshobson/agents
  Upstream paths: plugins/accessibility-compliance/skills/wcag-audit-patterns/SKILL.md and
    plugins/accessibility-compliance/skills/screen-reader-testing/SKILL.md (main, path commit seen 7e2fb55,
    2026-10-30; read 2026-11-02)
  License: MIT -- complete terms in LICENSE next to this file (Copyright (c) 2024 Seth Hobson)
  Forge adaptation note: conformance levels, the severity tiers, native-HTML-before-ARIA, the common-mistakes list
  and the screen-reader test matrix and widget scenarios are rewritten in Forge's words; no upstream file is
  shipped verbatim (references/details.md upstream was not read or copied). The WCAG 2.2 new-criteria list, the
  axe and Playwright recipes, keyboard/contrast checks and gates are Forge-native. Upstream content was treated
  as untrusted data: no scripts, install commands or dynamic-context lines were taken over.
-->

# Forge playbook — Accessibility (WCAG 2.2)

## When to use
- Use for: an accessibility audit of a page, component or app; fixing a11y findings; adding automated a11y
  checks to a test suite; preparing an accessibility statement (for example for the EU Accessibility Act).
- Not for: visual design direction (`frontend-design`, `forge-craft`), general web quality and SEO
  (`forge-website`), writing the test suite itself (`forge-testing`).

**Do not duplicate — defer to:** `forge-website` (a11y is one of its audits; this file is the method),
`forge-testing` (where the automated checks live), `forge-code-review` (severity flow for findings).

## Hard rules
- **Target WCAG 2.2 level AA** unless the owner names another level. AA is what most laws and procurement ask.
- **Automation is not an audit.** Automated tools find roughly a third to a half of issues. A pass from axe or
  Lighthouse is never reported as "accessible"; keyboard and screen-reader checks are required.
- **Native HTML before ARIA.** A `<button>` beats `<div role="button" tabindex="0">`. ARIA only fills gaps,
  and wrong ARIA is worse than none.
- **Every finding names the criterion** (number + name), the element (selector or file:line), the impact on a
  real user, and the fix.
- **Never remove focus outlines without a visible replacement, never disable zoom, never use colour alone**
  to carry meaning.
- **Honest scope:** say which pages, states, browsers and screen readers were actually tested and which were
  not. No "fully compliant" claim from a partial audit.

## Severity
| Tier | Meaning | Examples |
|---|---|---|
| Critical | blocks a task for some users | no keyboard access to a control, functional image without text alternative, form field without a label, focus trapped |
| Serious | major difficulty | contrast below AA, no skip link on long navigation, missing page title, focus not visible, target too small |
| Moderate | friction | missing `lang`, vague link text ("click here"), skipped heading levels, missing autocomplete on personal fields |
| Minor | polish | redundant title attributes, decorative image announced |

Critical and Serious map to HIGH in `forge-code-review` and block completion of a UI work package.

## Workflow
1. **Scope:** list the pages and states (empty, loading, error, success, modal open, mobile menu open).
2. **Automated pass:** axe in the browser or in Playwright on every page and state
   (`references/axe-and-tools.md`). Fix obvious hits first.
3. **Keyboard pass:** Tab through everything (`references/keyboard-focus-contrast.md`).
4. **Visual checks:** contrast, 200% and 400% zoom / reflow at 320 CSS px, text spacing, reduced motion.
5. **Screen-reader pass:** at least one desktop and one mobile pairing (`references/screen-readers.md`).
6. **WCAG 2.2 additions:** check the new criteria in `references/wcag22.md`.
7. **React or Next code:** review components against `references/react-patterns.md` (label and error
   wiring, widget keyboard patterns, dialogs and focus restore).
8. **Write up** findings by severity with criterion, element, user impact and fix; re-test after fixes and keep
   an automated axe check in the test suite as a regression guard.

## Domain gates
- Zero axe violations of impact critical/serious on the scoped pages, or each one listed with a reason.
- Every interactive element reachable and operable by keyboard, with a visible focus indicator, in a logical order.
- Text contrast at least 4.5:1 (3:1 for large text and for UI component boundaries and focus indicators).
- Forms: every field has a programmatic label; errors are announced and say how to fix them.
- Page has a unique `<title>`, `lang`, one `h1` and a logical heading outline, and landmarks.
- Dynamic updates (toasts, validation, cart count) are announced via a live region.

## Safety and honesty
- Never claim legal compliance; report the WCAG level and scope tested. Legal sign-off is the owner's call.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews):
  `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/wcag22.md` — POUR, levels and the criteria that are new in WCAG 2.2.
- `references/axe-and-tools.md` — axe in the browser, in Playwright and on the CLI; Lighthouse caveats.
- `references/keyboard-focus-contrast.md` — keyboard, focus management, contrast, zoom and motion checks.
- `references/screen-readers.md` — screen-reader matrix, modes, widget patterns to verify.
- `references/react-patterns.md` — React/Next code patterns: label and error wiring, combobox and accordion
  keys, native dialog and focus restore, reduced motion, anti-pattern table.

## Provenance
- **wshobson/agents** — see the source comment at the top of this file (MIT, Copyright (c) 2024 Seth
  Hobson; full terms in `LICENSE`).
- **ECC `skills/frontend-a11y/SKILL.md`** — pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`; MIT, Copyright (c) 2026 Affaan Mustafa (same MIT terms as
  `LICENSE`). Taken (rewritten) into `references/react-patterns.md`: label-to-input wiring, required and
  error wiring, accordion and combobox keyboard handling, modal focus save and restore, the reduced-motion
  hook, the anti-pattern list and checklist. Corrected while adopting: the combobox sample (no
  `aria-activedescendant`, listbox nested in the combobox), `role="alert"` on every inline error,
  `role="status"` mixed with `aria-live="assertive"`, and the focus-restore effect; the native `<dialog>`
  with `showModal()` replaces the default focus-trap dependency. Excluded: the CodeRabbit/ESLint
  tooling mentions and the related-skills links to ECC skills Forge does not ship.
