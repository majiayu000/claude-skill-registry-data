---
name: ui-inspector
description: Gather DOM inventory, computed styles, token usage, accessibility findings, and responsiveness data from a live or static implementation as structured evidence before redlining. Always run before ui-redline — redlining without inspector evidence produces opinions, not facts.
status: draft
---

# UI Inspector

A skill for turning a live or static implementation into an evidence report. It does not judge the implementation — it describes it. The judgment happens in `ui-redline`. The inspector's job is to ensure every redline decision is grounded in a measured fact rather than a remembered impression.

## When to use this skill

Use this skill when:
- An implementation exists (live browser, running dev server, or static HTML/CSS) and the user wants to compare it against a spec.
- The user is about to run `ui-redline` and needs an evidence base to redline against.
- A previous redline cycle is complete and the user wants to verify fixes — re-run the inspector to capture the updated state.

Do **not** use this skill when:
- No implementation exists yet. There is nothing to inspect. Run `ui-generate-code` or build the feature first.
- The user only wants to review or improve the spec itself. Use `ui-spec-linter` for that.
- The user wants a quick visual sanity check without a structured report. This skill produces a full evidence report — overkill for a 30-second eyeball pass.

## Core principle

**Redlining without evidence produces opinions. Redlining with evidence produces facts.** An opinion says "the button looks too small." A fact says "the button's computed `padding` is `4px 8px`; the spec calls for `space.3` (12px) × `space.5` (20px)." The inspector exists to replace the opinion with the fact. It collects; it does not conclude.

## What to inspect

### 1. DOM inventory

List every interactive element on the inspected UI Scope by type. The goal is a census, not a summary — every element that a user can act on must appear in the table.

For each element, record:
- Element type (button, input, select, link, checkbox, radio, ARIA role widget, etc.)
- CSS selector or identifying attribute (ID, class, `data-testid`, or `aria-label`)
- Semantic role (`<button>`, `role="button"`, `<a href>`, `role="link"`, etc.)
- Whether semantic markup is present or the element is div-soup

Flag any interactive element that lacks semantic markup (e.g., a `<div>` with an `onClick` handler but no `role`, `tabindex`, or `aria-*` attributes). This is not a judgment — it is an observation for `ui-redline` to classify.

### 2. Computed styles sample

For the 5–10 most visually significant elements (primary CTA, main heading, body text, card surface style, input field, navigation item — whichever apply), record the browser-computed values at the primary breakpoint.

Collect for each element:
- Computed text color (hex or `rgb()`)
- Background color (hex or `rgb()`)
- Font size (px)
- Font weight (numeric)
- Border radius (px)
- Padding (top right bottom left, px)
- Margin (top right bottom left, px)
- Box shadow (full value or "none")

Do not round or approximate — record the exact computed value. If a value is `0px`, record `0px`, not "none" or blank.

### 3. Token usage check

Determine whether the implementation uses CSS custom properties (design tokens) or hard-coded literal values.

**Signs of token usage:**
- `color: var(--color-text-primary)` — token used
- `padding: var(--space-4)` — token used

**Signs of literal values:**
- `color: #1a1a1a` — literal, should be a token
- `padding: 16px` — literal, may or may not match a token value

Record:
- Number of CSS custom property (`var(--*)`) references found in the inspected stylesheet(s) or inline styles
- Every literal color value found (hex, `rgb()`, `hsl()`, named colors other than `inherit`/`transparent`/`currentColor`)
- Every literal spacing value found (px values in `padding`, `margin`, `gap`, `width`, `height`) that does not use a CSS variable

Do not evaluate whether literals are "correct" — record them as observations. `ui-redline` decides whether they violate the system spec.

### 4. Accessibility scan

Record every accessibility issue discovered via the browser accessibility tree, axe-core output, or manual inspection. Use the four-column format below.

**WCAG criteria to cover at minimum:**

| Criterion | What to check |
|---|---|
| 1.1.1 Non-text content | Every `<img>` has a non-empty `alt` attribute (or `alt=""` if decorative) |
| 1.3.1 Info and Relationships | Form inputs are programmatically associated with labels |
| 1.4.3 Contrast (Minimum) | Text contrast ≥ 4.5:1 (AA); large text ≥ 3:1 |
| 2.1.1 Keyboard | All interactive elements reachable by Tab |
| 2.4.3 Focus Order | Tab order matches visual reading order |
| 2.4.7 Focus Visible | Focus-visible indicator present on all interactive elements |
| 4.1.2 Name, Role, Value | Interactive elements have accessible names and appropriate ARIA roles |

If axe-core is available, include a count of violations by impact level (critical, serious, moderate, minor).

### 5. Responsiveness check

At the primary breakpoint and at least one secondary breakpoint, record how the layout behaves.

For each breakpoint tested:
- Viewport width used
- Whether horizontal scrollbar appears (yes/no)
- Whether primary action is in the top half of the viewport (yes/no)
- Whether any text is clipped or overflow hidden (yes/no)
- Whether the layout matches the blueprint's specified reflow verb (stacked, collapsed, hidden, resized) — record as "matches", "partial", or "does not match"

---

## Report Header Requirements

Every inspector report must include these frontmatter fields:

```yaml
inspection_method: live-authenticated | live-unauthenticated | static-source
runtime_verified: true | false
partial: true | false
```

If `runtime_verified: false`, the report is based on static code inspection and must include a confidence breakdown:

```
Confidence breakdown:
- Verified by source: <N> findings
- Inferred from source: <N> findings
- Requires live DOM: <N> findings (not verified)
```

For static-only runs, include this additional block in frontmatter to make runtime limits explicit:

```yaml
inspection_mode: static-source
runtime_verified: false
browser_access: unavailable
deferred_checks:
	- keyboard focus order
	- hover and focus states
	- computed runtime layout
	- responsive drawer or modal behavior
	- console errors
```

---

## Browser access policy

Do not assume Playwright is installed.

Before using live browser inspection:
1. Detect whether Playwright is available in the current repository.
2. Detect whether the app can run locally and a target route is reachable.
3. If unavailable, continue in static mode and mark runtime checks as deferred.
4. Do not install Playwright or modify package files unless the user explicitly asks for setup or patch mode.

If Playwright is missing, state this clearly:

```text
Playwright is not installed in this repo. I can continue in static inspection mode, or you can install Playwright to enable live browser inspection.
```

Recommended install commands for JavaScript and TypeScript repositories:

```bash
npm install -D @playwright/test
npx playwright install
```

For Linux CI:

```bash
npx playwright install --with-deps
```

---

## Tooling: three paths

Choose the path that matches what is available. Record the chosen path in the report header. All three paths produce the same evidence report schema — the only difference is the confidence level that can be claimed for each finding.

### Path A — AI model with browser tooling (Playwright, Puppeteer, browser MCP)

The inspector can be run fully by an AI model in an environment that provides browser automation. Steps:

1. Open the target URL at the primary breakpoint viewport size.
2. Run `document.querySelectorAll('button, input, select, textarea, a[href], [role="button"], [role="link"], [tabindex]')` and enumerate results into the DOM inventory.
3. For each element in the computed styles sample, call `window.getComputedStyle(el)` and record the required properties.
4. Scan all stylesheets for `var(--*)` references and literal color/spacing values.
5. If axe-core is available, inject it and call `axe.run()`. Otherwise run the manual WCAG checks above.
6. Resize to each secondary breakpoint and observe layout behavior.

Preflight for Path A:
1. Detect package manager lockfile (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb`).
2. Check `package.json` for `@playwright/test` or `playwright`.
3. Check that Playwright browser binaries are installed.
4. Check that the app starts and target route is reachable.
5. If checks fail, switch to Path C and list deferred checks.

### Path B — Developer copying DevTools output (manual path)

If browser automation is not available, a developer runs the inspector manually:

1. **DOM inventory:** Open DevTools Elements panel. Filter for interactive elements. Paste the relevant HTML into the evidence report.
2. **Computed styles:** Select each element in DevTools → Computed tab. Screenshot or copy the relevant properties.
3. **Token usage:** DevTools → Sources → search stylesheets for `var(--`. Count references. Search for hex patterns `#[0-9a-f]{3,6}` and list findings.
4. **Accessibility:** DevTools → Accessibility panel for individual element checks. Or run axe DevTools browser extension.
5. **Responsiveness:** Toggle device toolbar. Test at each breakpoint. Screenshot each state.

### Path C — Static source-code inspection

Use this path when no live browser or running dev server is available — for example, when the route is auth-gated, when CI access is unavailable, or when running in an environment with no browser tooling.

In static inspection, all evidence is gathered by reading source files directly (component files, stylesheets, CSS-in-JS, utility class lists, ARIA attributes in JSX/HTML). The output is structurally identical to Paths A and B but every finding must carry an explicit **confidence label**.

**Confidence labels for static inspection:**

| Label | Meaning |
|---|---|
| `exact — source` | Value read directly from source (e.g., a hard-coded `className="rounded-md"` or `style={{ padding: '16px' }}`). Reliable. |
| `inferred — source` | Value derived from a utility class, theme token lookup, or CSS variable without a live computed value (e.g., `p-4` inferred as `16px` via Tailwind scale). Reliable but not browser-verified. |
| `deferred — needs live DOM` | Could not be established from static analysis alone (e.g., styles applied conditionally at runtime, animations, pseudo-states). Must be re-verified with a live browser. |

Steps for static inspection:

1. **DOM inventory:** Read component JSX/TSX/HTML. List every interactive element (button, input, link, role widget) found. Note whether semantic markup is present or absent in the source.
2. **Computed styles sample:** Read className lists, inline styles, and CSS files. For utility class frameworks (Tailwind, etc.), translate classes to computed values using the framework's scale. Label each value `exact — source` or `inferred — source`.
3. **Token usage:** Search stylesheets and component files for `var(--)` references. Search for literal color and spacing values. Label each finding.
4. **Accessibility:** Read ARIA attributes, `alt` attributes, label associations, and `tabIndex` values in source. Note that hover/focus visual states, screen reader announcements, and keyboard navigation order cannot be verified statically — record as `deferred — needs live DOM`.
5. **Responsiveness:** Read responsive class variants (e.g., `md:grid-cols-2`) and media queries. Infer reflow behavior. Label as `inferred — source`.

All three paths produce the same evidence report schema. Note which path was used in the report header.

---

## Evidence report schema

Produce the evidence report in this exact structure. Save it as `inspector-report.md` in the `redlines/` directory of the spec package. If multiple inspection runs exist, add a date suffix: `inspector-report-<YYYY-MM-DD>.md`.

```markdown
---
spec_type: inspector-evidence
spec_id: <slug>
based_on: <spec package name or "none — no linked spec">
created: <YYYY-MM-DD>
inspection_method: <"automated (Playwright)" | "automated (Puppeteer)" | "automated (browser MCP)" | "manual (DevTools)" | "static source-code" | "hybrid (static + manual)">
status: draft
---

# Inspector Evidence Report

**URL / file inspected:** <url or file path>
**Inspection date:** <YYYY-MM-DD>
**Spec package linked:** <spec package name or "none">
**Inspection method:** <see frontmatter>
**Primary breakpoint tested:** <e.g. 1280px desktop>

---

## 1. DOM Inventory

| Element type | Selector | Semantic role | Semantic markup present? | Notes |
|---|---|---|---|---|
| button | #submit-btn | `<button>` | Yes | — |
| div | .card-click-area | none | No | Has onClick but no role or tabindex |

**Total interactive elements found:** N
**Elements missing semantic markup:** N (list selectors)

---

## 2. Computed Styles Sample

_Note: If static source-code inspection was used, add a Confidence column to every row (`exact — source` / `inferred — source` / `deferred — needs live DOM`)._

| Element | Selector | Text color | Bg color | Font size | Font weight | Border radius | Padding (T R B L) |
|---|---|---|---|---|---|---|---|
| Primary CTA | #submit-btn | #ffffff | #1d4ed8 | 16px | 600 | 6px | 12px 24px 12px 24px |

**Breakpoint at time of capture:** <e.g. 1280px>

---

## 3. Token Usage

**CSS custom properties (`var(--)`) detected:** N references across N files
**Literal color values found:**
- `#1a1a1a` — found in `components/button.css` line 14
- `rgb(239, 68, 68)` — found in `components/form.css` line 42

**Literal spacing values found (px in padding/margin/gap):**
- `padding: 8px 16px` — found in `components/card.css` line 7

---

## 4. Accessibility Findings

**Inspection method:** <axe-core | manual WCAG checks | DevTools Accessibility panel>
<If axe-core:> **axe-core violation summary:** Critical: N | Serious: N | Moderate: N | Minor: N

| Severity | Element | Selector | Issue | WCAG criterion |
|---|---|---|---|---|
| critical | Image | img.hero-photo | Missing alt attribute | 1.1.1 |
| serious | Input | #email-input | No associated label | 1.3.1 |
| moderate | Link | a.nav-item:nth-child(3) | Contrast ratio 3.2:1 (fails AA for small text) | 1.4.3 |

---

## 5. Responsiveness

| Breakpoint | Viewport width | Horizontal scroll? | Primary action in top half? | Text clipped? | Blueprint reflow match? |
|---|---|---|---|---|---|
| Desktop (primary) | 1280px | No | Yes | No | Matches |
| Tablet | 768px | No | Yes | No | Partial — sidebar does not collapse as specified |
| Mobile | 375px | Yes | No | Yes | Does not match |

**Notes:** <any additional observations about layout behavior>

---

## 6. Inspector notes

<Any observations that do not fit the structured tables above — e.g., "the loading state could not be inspected because the API endpoint is mocked", "dark mode was not tested because the spec does not address it.">

**This report contains evidence only. No judgments about correctness or severity are made here. Pass this report to `ui-redline` for evaluation against the spec.**
```

---

## Anti-pattern rules

1. **Do not make judgment calls in the evidence report.** "The button color is wrong" is a judgment. "The button's computed background is `#2563eb`; the spec token `color.action.primary` resolves to `#1d4ed8`" is evidence. Save the judgment for `ui-redline`.
2. **Do not skip the DOM inventory even if it seems obvious.** The DOM inventory is the foundation of the evidence report. An inspector that skips it is an inspector that cannot account for missing or extraneous elements.
3. **Do not approximate computed values.** Record `border-radius: 6px`, not "slightly rounded." The difference between 6px and 8px is a nit; the difference between "slightly rounded" and 6px is unresolvable.
4. **Do not omit literal values because they happen to match a token value.** If an element uses `padding: 16px` instead of `var(--space-4)`, record the literal even if 16px equals `space.4`. Token usage and token correctness are separate questions.
5. **Do not run the inspector against a spec instead of an implementation.** The inspector reads code and browsers, not markdown. If there is no implementation, say so and stop.
6. **Do not omit confidence labels in static inspections.** When Path C is used, every finding in the computed styles, token usage, accessibility, and responsiveness sections must carry a confidence label. An unlabeled static finding gives `ui-redline` no way to know whether the value was browser-verified or inferred.

---

## Acceptance criteria for this skill's output

An evidence report produced by this skill is acceptable only if every one of these is true:

- [ ] All five sections (DOM Inventory, Computed Styles, Token Usage, Accessibility Findings, Responsiveness) are present, even if some contain "None found" or empty tables.
- [ ] The inspection method (automated or manual, tool, or static source-code) is declared in both the frontmatter and the report header.
- [ ] If static source-code inspection was used (Path C), every computed value carries a confidence label (`exact — source`, `inferred — source`, or `deferred — needs live DOM`).
- [ ] Every computed style value is the exact browser-computed value — no approximations, no rounding, no prose descriptions substituted for numeric values.
- [ ] The DOM inventory accounts for every interactive element on the inspected UI Scope — not just a representative sample.
- [ ] The Token Usage section lists every literal color and spacing value found, not just a count. A count alone is not actionable.
- [ ] The report contains zero judgment statements. Every sentence describes a measurement or observation. Evaluations ("this is wrong", "this is correct") are absent.
- [ ] If a section could not be completed (e.g., loading state was not triggerable), the reason is recorded in §6 Inspector notes rather than the section being silently omitted.

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill in Path C (static source-code) mode against a React/TypeScript component reproduces findings consistent with `examples/spec-recovery-create/redlines/inspector-report.md`.
- [ ] All three caption input implementations are identified and documented in the DOM Inventory.
- [ ] The hard-coded `setTimeout(3000)` AI timeout is identified in the Computed Styles / notable values section.
- [ ] The `<MobileCreateRedirect />` separate component is identified in the Responsiveness section.

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/` (or equivalent) produces a report that passes every Acceptance criteria item above.
- [ ] At least one `deferred — needs live DOM` confidence label appears (since settings-page is a static spec, not live).

### Regression: zero judgment statements

- [ ] Reviewing the output with a fresh reader: every sentence is a measurement or observation. No "this is broken", "this is correct", or evaluative language appears.

### Path A / Path B evidence (live DOM)

- [ ] When run against a live URL with DevTools, the Token Usage section lists every literal hex value found (not just a count).
- [ ] The Accessibility Findings table uses the standard severity scale from `shared/references/severity-scale.md`.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-inspector` has been updated to `"status": "stable"`.
- [ ] README minimum viable workflow step 6 (`ui-inspector`) and the clarifying note are both present.
- [ ] README Skill Map table has been updated to show `stable`.
