---
name: Accessibility Check
description: "Audit frontend code for WCAG 2.1 AA compliance. Triggers on phrases like 'a11y check', 'accessibility audit', 'check WCAG', or when reviewing JSX/TSX components in the frontend/ tree. Reports ARIA misuse, semantic-HTML gaps, keyboard-trap risks, color-contrast smells, and missing alt text with file:line citations and USWDS-aligned fix suggestions."
---

## Purpose

Provide fast, local, deterministic WCAG 2.1 AA feedback on Next.js/React components before they reach CI or manual QA. The skill does not replace axe-core or Pa11y CI; it catches the top-N recurring a11y defects early and names the exact fix.

## When to Invoke

- A developer is editing a component under `frontend/src/components/` or `frontend/src/app/`.
- A PR touches JSX/TSX and the author says "a11y check" or "accessibility audit".
- A reviewer wants a structured a11y report on a file or changed range.
- Before requesting accessibility sign-off on a feature flagged for launch.

## When NOT to Invoke

- For non-frontend files (API, Terraform, Alembic).
- As a substitute for axe-core runs in CI — this is fast feedback, not certification.
- On generated files (`.next/`, `node_modules/`, snapshots).

## Inputs

- **target**: active file, an explicit path (e.g. `frontend/src/components/search/SearchBar.tsx`), or `git diff` range.
- **scope** (optional): `file` (default) or `changed` (only the added lines from the current diff).

## Procedure

1. Resolve target file(s). If none provided, use the active editor file. Refuse non-`.tsx|.ts|.jsx|.js` files.
2. Read the file(s). Collect component names, JSX elements, handlers.
3. Run the following deterministic checks:
   - `<img>` and `next/image` without `alt=`
   - `<button>` nested in `<a>` or vice versa
   - Clickable `<div>`/`<span>` without `role` + `tabIndex={0}` + key handler
   - Form controls without associated `<label htmlFor>` or `aria-label`
   - `aria-*` attributes on elements that do not support them (cross-reference ARIA-in-HTML allowed list)
   - Missing `lang` on any custom `<html>` usage
   - Heading-order skips within the same component (h1 to h3)
   - Icon-only buttons without `aria-label`
   - `onClick` without keyboard equivalent (`onKeyDown`/`onKeyUp`)
   - Color literals (`#xxxxxx`) bypassing USWDS tokens — flag for contrast review
4. Cross-reference against `documentation/rules/frontend-*.md` for project-specific directives.
5. Emit the Output Format below. Do not modify files.

## Outputs

```
Accessibility Check — frontend/src/components/search/SearchBar.tsx
WCAG target: 2.1 AA

Findings (3):
  [ERROR] L42  Icon-only <button> missing aria-label
          Fix:  <button aria-label="Clear search"> ...
          WCAG: 4.1.2 Name, Role, Value
  [WARN]  L58  onClick on <div> without keyboard handler
          Fix:  convert to <button type="button"> or add onKeyDown
          WCAG: 2.1.1 Keyboard
  [INFO]  L71  Hard-coded color #0050d8 — use USWDS token
          Fix:  color-primary (token in frontend/src/styles/_uswds-theme.scss)

Summary: 1 error, 1 warning, 1 info. Block merge: yes.
```

Exit convention: `error` count > 0 → block; `warn` → comment; `info` → advisory.

## Safety

- Read-only. Never rewrites files.
- Never claims the component is "fully accessible" — this is a lint-grade pass, not an audit.
- Flags but does not resolve contrast ratios; defers to USWDS tokens.
- Never invents ARIA roles. If uncertain, recommends removing the attribute.
- PII: never emit component text content containing user data in reports.

## Examples

**Example 1 — Active file audit**
Developer opens `OpportunityCard.tsx` and types "a11y check". Skill reports a missing `alt` on the agency logo `next/image` and flags `<div onClick>` on the card wrapper; suggests `<article>` with `<button>` inside.

**Example 2 — Diff-scoped audit**
`/skill-accessibility-check scope=changed` before pushing. Skill reads `git diff --unified=0` for staged changes and reports only on added lines, useful for hot-fix PRs.

**Example 3 — Cross-referenced with conventions**
Finding includes a link back to `documentation/rules/frontend-components.md` when a violation matches a MUST directive there.

## Related

- `.cursor/agents/visual-regression.md` — pairs well for launch QA.
- `.cursor/skills/skill-cross-browser-checklist/` — run together before release.
- `/check-conventions` — catches non-a11y frontend rule violations.
