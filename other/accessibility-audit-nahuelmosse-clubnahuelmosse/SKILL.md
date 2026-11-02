---
name: accessibility-audit
description: Audit UI code for WCAG 2.1 AA compliance — semantics, keyboard navigation, color contrast, and ARIA. Use when auditing accessibility or the user mentions a11y, screen readers, WCAG, or keyboard support. For visual/design quality use /design-review instead.
user-invocable: true
---

# Accessibility Audit

## Core Rule

Test against WCAG 2.1 AA criteria with concrete user-impact. Never auto-edit semantic HTML or ARIA without explicit user approval.

## When to Use

Invoke with `/accessibility-audit` when:

- Building or reviewing user-facing UI components
- Preparing for an accessibility compliance review
- Fixing reported accessibility issues
- Ensuring inclusive design for all users
- Before launching a new feature with UI changes

## Default Behavior

When the user asks to audit, scan, review, or "give me a report" for accessibility / WCAG compliance, produce the full accessibility-audit report automatically using the Process and Output Format sections below. Do not require the user to specify fields.

Only modify files when the user explicitly requests implement / fix / apply / refactor. By default, this skill is **report-only**.

## Process

### Phase 1: Inventory (first-pass leads)

This pass produces **candidates**, not findings. Treat counts as leads for deeper inspection in later phases. Do not report Phase 1 raw output as the final result.

Determine the UI technology:

- **Web**: React, Vue, Angular, Svelte, plain HTML
- **Mobile**: React Native, Flutter, native iOS/Android
- **Desktop**: Electron, Tauri, native desktop

Adapt checks to the framework's accessibility patterns.

### Phase 2: Semantic Structure

Check that UI elements convey meaning:

**HTML Semantics (Web)**
- Use semantic elements (`<nav>`, `<main>`, `<article>`, `<button>`) instead of generic `<div>`/`<span>`
- Heading hierarchy is logical (h1 → h2 → h3, no skipping levels)
- Lists use `<ul>`/`<ol>`/`<dl>` not styled divs
- Forms have associated `<label>` elements
- Tables have `<thead>`, `<th>`, and `scope` attributes for data tables
- Landmarks are used correctly (one `<main>`, navigation in `<nav>`)

**Component Semantics (All frameworks)**
- Interactive elements are focusable and have accessible names
- Custom components expose correct roles to assistive technology
- Decorative elements are hidden from screen readers (`aria-hidden`, empty alt)

### Phase 3: Keyboard Navigation

Verify full keyboard operability:

- **Tab order**: logical, follows visual layout, no keyboard traps
- **Focus visibility**: all interactive elements have visible focus indicators
- **Interactive elements**: all clickable elements are reachable and operable via keyboard
- **Custom widgets**: keyboard patterns follow WAI-ARIA Authoring Practices
  - Modals: trap focus, Escape to close
  - Dropdowns: Arrow keys to navigate, Enter to select, Escape to close
  - Tabs: Arrow keys to switch, Tab to move to content
  - Sliders: Arrow keys to adjust
- **Skip links**: "Skip to main content" link for long navigation
- **No mouse-only interactions**: hover-only tooltips, drag-only sorting

### Phase 4: Visual Accessibility

Check visual design compliance:

**Color & Contrast**
- Text contrast ratio ≥ 4.5:1 (normal text) or ≥ 3:1 (large text, 18px+ or 14px+ bold)
- UI component contrast ≥ 3:1 against adjacent colors
- Information is not conveyed by color alone (add icons, patterns, or text)
- Focus indicators have sufficient contrast

**Typography & Layout**
- Text can be resized to 200% without loss of content
- No horizontal scrolling at 320px viewport width (responsive)
- Line height ≥ 1.5, paragraph spacing ≥ 2x font size
- Touch targets ≥ 44x44px (mobile)

**Motion & Animation**
- Respect `prefers-reduced-motion` media query
- No auto-playing animations longer than 5 seconds without pause control
- No content that flashes more than 3 times per second

### Phase 5: ARIA Usage

Audit ARIA implementation:

- **First rule of ARIA**: Don't use ARIA if native HTML can do it
- **Correct roles**: ARIA roles match the element's purpose
- **Required properties**: ARIA roles have all required properties (e.g., `role="slider"` needs `aria-valuenow`)
- **Live regions**: dynamic content updates announced with `aria-live`
- **Labels**: interactive elements have `aria-label` or `aria-labelledby` when visible text is insufficient
- **States**: toggle states use `aria-pressed`, `aria-expanded`, `aria-selected` correctly
- **No conflicting ARIA**: ARIA attributes don't conflict with native semantics

### Phase 6: Content Accessibility

Check content is accessible:

- **Images**: all `<img>` have `alt` text (descriptive for content, empty for decorative)
- **Forms**: error messages are programmatically associated with inputs
- **Links**: link text is descriptive (no "click here" or "read more" without context)
- **Language**: `lang` attribute set on `<html>` and on elements in different languages
- **Timeouts**: users are warned before timeouts and can extend them

## Output Format

```markdown
# Accessibility Audit Report

## Compliance Level
[Current WCAG 2.1 AA compliance estimate: Non-compliant / Partially / Mostly / Fully]

## Critical Issues (A-level violations)
| # | WCAG Criterion | Location | Issue | Fix |
|---|---------------|----------|-------|-----|
| 1 | 1.1.1 Non-text Content | file:line | Image missing alt text | Add descriptive alt |

## Major Issues (AA-level violations)
| # | WCAG Criterion | Location | Issue | Fix |
|---|---------------|----------|-------|-----|

## Minor Issues (Best practices)
| # | Category | Location | Issue | Fix |
|---|----------|----------|-------|-----|

## Component Checklist
| Component | Keyboard | Screen Reader | Contrast | Status |
|-----------|----------|--------------|----------|--------|
| Navigation | ✅/❌ | ✅/❌ | ✅/❌ | Pass/Fail |

## Recommendations
1. [Highest impact fix]
2. ...
```

## Notes

- This audit covers WCAG 2.1 AA level — AAA is aspirational and not required for most projects
- For mobile apps, apply the equivalent platform accessibility guidelines alongside WCAG
- Static code analysis catches structural issues but manual testing with screen readers is still recommended
- Non-UI projects (APIs, CLIs, libraries) do not need this audit
