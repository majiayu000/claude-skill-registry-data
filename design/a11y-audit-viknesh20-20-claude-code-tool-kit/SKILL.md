---
name: a11y-audit
description: "Accessibility audit of UI code or a running site against WCAG 2.1 AA. Walks every WCAG criterion that maps to common patterns: keyboard reach, focus visibility, contrast, semantic HTML, ARIA, labels, alt text, motion, screen-reader sense. Severity-graded with code fixes."
---

# /a11y-audit

Walk a UI for accessibility issues against WCAG 2.1 Level AA — the legal bar in most jurisdictions and the right bar everywhere. Output is a severity-graded list with concrete code fixes, not a generic "improve accessibility" lecture.

## When to use

- Before shipping any new UI to production.
- Before a launch in EU / UK (European Accessibility Act applies June 2025).
- Before any government / education / healthcare deal — those usually require Section 508 / EN 301 549.
- After axe-core or Lighthouse flagged issues and you want a complete walk, not just the automated catches.
- When the user reports a specific accessibility complaint.

## Operating method

### 1. Confirm scope

- **What's the target?** Source code (`/path/to/component.tsx`), a route URL, a running app, or all of the above.
- **What WCAG level?** Default AA. AAA only if the user explicitly asks (some criteria have meaningful trade-offs at AAA).
- **What user agents matter?** Default: latest Chrome, Safari, Firefox + VoiceOver (Mac/iOS), NVDA (Windows). Add more if the user serves specific audiences.

### 2. Run the deterministic scans first

Whenever feasible:

- **axe-core** via Playwright or browser extension on every route.
- **Lighthouse** accessibility audit (Chrome DevTools or `lhci`).
- **`html-validate`** on rendered output to catch invalid markup that screen readers misinterpret.
- **Color-contrast checker** (axe / Stark / WCAG Contrast Checker) on every text/bg pair.

Capture the output. The automated tools catch ~30% of issues — necessary but not sufficient.

### 3. Walk WCAG 2.1 AA by relevant criteria

These are the criteria that come up in 90% of audits. Walk each that applies.

#### Perceivable

**1.1.1 Non-text Content (A)**
- Every meaningful image has `alt`. Decorative images have `alt=""`.
- Icons that convey meaning have `aria-label` or accompanying text.
- Charts/graphs have a text alternative or detailed description.

**1.3.1 Info and Relationships (A)**
- Form labels associated via `<label for=…>` or aria-labelledby.
- Tables use `<th>` with `scope`.
- Headings in order, no skipped levels.
- Lists marked up as `<ul>` / `<ol>`, not styled `<div>`s.

**1.3.2 Meaningful Sequence (A)**
- DOM order matches visual reading order (CSS flexbox / grid `order` does NOT change reading order for screen readers).

**1.3.5 Identify Input Purpose (AA)**
- Common inputs (name, email, address, payment) use correct `autocomplete` attribute.

**1.4.1 Use of Color (A)**
- Color is never the only carrier of meaning. Required fields show "*" or text in addition to red.
- Error states have an icon + text in addition to red border.

**1.4.3 Contrast Minimum (AA)**
- Body text: ≥ 4.5:1 against background.
- Large text (≥ 18pt regular / 14pt bold): ≥ 3:1.
- Common gotcha: placeholder text and disabled buttons often fail.

**1.4.4 Resize Text (AA)**
- Page works when zoomed to 200%. No content cut off, no horizontal scrolling.

**1.4.10 Reflow (AA)**
- Page works at 320px wide and 256px tall without 2D scrolling.

**1.4.11 Non-text Contrast (AA)**
- UI components and graphical objects: ≥ 3:1 against adjacent colors. Includes button borders, focus rings, form-input borders.

**1.4.12 Text Spacing (AA)**
- Page works when the user overrides line-height to 1.5×, paragraph spacing to 2×, letter-spacing to 0.12em, word-spacing to 0.16em. No content cut off.

**1.4.13 Content on Hover or Focus (AA)**
- Tooltips dismissible (Esc), hoverable (mouse can move into them), persistent (don't disappear during read).

#### Operable

**2.1.1 Keyboard (A)**
- Every interactive element reachable by Tab.
- All actions doable without a mouse.

**2.1.2 No Keyboard Trap (A)**
- Once focus enters a component, it can leave by Tab/Shift-Tab/Esc.

**2.1.4 Character Key Shortcuts (A)**
- Single-key shortcuts can be turned off, remapped, or only fire on focus.

**2.4.1 Bypass Blocks (A)**
- Skip-to-content link as first focusable element.
- Or proper landmarks (`<main>`, `<nav>`, `<aside>`).

**2.4.2 Page Titled (A)**
- Every page has a unique `<title>`.

**2.4.3 Focus Order (A)**
- Tab order matches visual reading order.

**2.4.4 Link Purpose (A)**
- Link text describes destination ("Read API docs" not "Click here").

**2.4.6 Headings and Labels (AA)**
- Headings describe section content.
- Form labels describe purpose.

**2.4.7 Focus Visible (AA)**
- Focus indicator visible. **Never** `outline: none` without a replacement ring.
- Focus ring contrast ≥ 3:1 against any background.

**2.5.5 Target Size (AAA but worth checking) → 2.5.8 Target Size Minimum (AA in 2.2)**
- Touch targets ≥ 24×24 CSS px (WCAG 2.2 AA), ideally ≥ 44×44 (Apple HIG).

#### Understandable

**3.1.1 Language of Page (A)**
- `<html lang="en">` (or correct ISO code).

**3.1.2 Language of Parts (AA)**
- Foreign-language phrases marked up: `<span lang="fr">déjà vu</span>`.

**3.2.1 On Focus (A)**
- Focusing an element does not change context (no auto-submit, no auto-navigation).

**3.2.2 On Input (A)**
- Changing an input's value does not change context (no auto-submit on dropdown change without warning).

**3.3.1 Error Identification (A)**
- Errors identified in text, not just by color or icon.

**3.3.2 Labels or Instructions (A)**
- Every input has a visible label or programmatic label.

**3.3.3 Error Suggestion (AA)**
- Error messages include how to fix the error.

**3.3.4 Error Prevention (Legal, Financial, Data) (AA)**
- For irreversible actions: confirm + reversible OR confirm + checkable summary.

#### Robust

**4.1.2 Name, Role, Value (A)**
- Custom interactive components have proper role, name, state.
- Use semantic HTML (`<button>`) over `<div role="button">` whenever possible.

**4.1.3 Status Messages (AA)**
- Status changes (toasts, validation results, loading completion) announced via `aria-live`.

### 4. Walk patterns common to most apps

Beyond per-criterion walkthrough, check these patterns:

- **Modals**: focus trapped within while open, focus returned on close, Esc closes, click-outside closes (or aria-hidden on background, role="dialog", aria-labelledby on title).
- **Menus / dropdowns**: arrow-key navigation, Esc closes, Home/End navigation, type-ahead.
- **Forms**: label association, error linkage via aria-describedby, error focus on submit failure, required-field marking.
- **Tabs**: arrow-key navigation, role="tablist" + role="tab" + role="tabpanel", aria-selected.
- **Disclosure (accordion / details)**: aria-expanded, focusable trigger.
- **Carousels**: keyboard reachable, autoplay pausable, current slide indicated.
- **Custom controls**: any `div` that responds to clicks should be a `button` instead.

### 5. Test with a screen reader (live audit)

If auditing a running app, use a screen reader for at least one critical flow:

- **Mac/iOS**: VoiceOver (Cmd+F5 / triple-click home).
- **Windows**: NVDA (free) or JAWS.
- **Linux**: Orca.

Listen to: page title, landmarks, headings, link list, form fields, error messages. If the experience makes no sense, the audit isn't done.

### 6. Severity grading

- **Critical** — blocks a user with disability from completing a core task. Pre-auth modals with no keyboard access, forms with no labels, color-only error states.
- **High** — significantly impairs but workaround exists. Missing skip link, low-contrast body text, missing alt on key images.
- **Medium** — friction for some users. Tooltip not dismissible by Esc, missing aria-live on toast.
- **Low** — defense-in-depth. Lang attribute on parts, foreign-phrase markup.

### 7. Output format

```
## Scope
- Target: <files / routes>
- WCAG level: 2.1 AA
- Tools used: axe-core, Lighthouse, manual VoiceOver walk on /signup, /checkout

## Verdict: PASS | CONDITIONAL | FAIL

## Findings (severity-ordered)

### Critical (N)
1. **No keyboard access to "Add to cart" button** (WCAG 2.1.1).
   - File: `src/components/ProductCard.tsx:42`
   - Issue: `<div onClick={...}>` instead of `<button>`. Not reachable by Tab.
   - Fix:
     ```tsx
     // Before
     <div className="add-btn" onClick={handleAdd}>Add to cart</div>
     // After
     <button type="button" className="add-btn" onClick={handleAdd}>Add to cart</button>
     ```

2. **Modal traps focus on screen readers** (WCAG 2.4.7, 4.1.2).
   - File: `src/components/Modal.tsx:18`
   - Issue: …
   - Fix: use `react-focus-lock` or implement focus trap manually.

### High (N)
…

### Medium (N)
…

### Low (N)
…

## Patterns audited
- [x] Modals — 2 issues
- [x] Forms — 4 issues
- [x] Color contrast — 1 issue
- [x] Keyboard navigation — 3 issues
- [x] Focus visibility — 1 issue
- [x] Skip link — missing
- [x] Heading hierarchy — clean
- [x] Alt text — 2 missing

## Screen reader walk
- [x] /signup with VoiceOver — 1 issue (form errors not announced)
- [x] /checkout with VoiceOver — 0 issues

## Recommended next moves
1. Fix all Critical (1 day).
2. Fix High in priority order (1 week).
3. Add axe-core to CI to catch regressions.
4. Schedule a screen-reader walk per release for top 3 flows.
```

## Boundaries

- Don't claim "accessible" without a screen-reader walk on at least one flow.
- Don't write a fix you haven't verified would work — read the actual component code first.
- Don't audit categories that don't apply (no point checking video captions if there's no video).
- Don't recommend AAA criteria when the user asked for AA — AAA has trade-offs.
- Don't ignore the user's specific concerns. If they reported a complaint, prioritize that pattern.
- Always cite the WCAG criterion (e.g., "WCAG 2.4.7") so the team can search the standard.
