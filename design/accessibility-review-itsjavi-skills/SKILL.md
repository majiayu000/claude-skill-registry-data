---
name: accessibility-review
description:
  Run a WCAG 2.2 AA accessibility audit on a design, mockup, prototype or rendered page and report findings without
  changing code. Trigger with "audit accessibility", "check a11y", "is this accessible?", or when reviewing a design for
  color contrast, keyboard navigation, target size, or screen reader behavior before handoff. To fix accessibility
  issues in HTML or component code, use fix-web-accessibility.
---

# Accessibility Review

Audit a design or page for WCAG 2.2 AA accessibility compliance, honoring an explicit project conformance target when
one exists.

Audit the design, page, screenshot, file or description the user provides. If nothing is provided, ask for it. This
skill produces an audit report. When the user also wants code fixed, hand the findings to fix-web-accessibility when
available, which applies the same WCAG 2.2 AA target.

## WCAG 2.2 AA Quick Reference

### Perceivable

- **1.1.1** Non-text content has alt text
- **1.3.1** Info and structure conveyed semantically
- **1.4.3** Contrast ratio >= 4.5:1 (normal text), >= 3:1 (large text)
- **1.4.11** Non-text contrast >= 3:1 (UI components, graphics)

### Operable

- **2.1.1** All functionality available via keyboard
- **2.4.3** Logical focus order
- **2.4.7** Visible focus indicator
- **2.4.11** Focus not obscured by sticky headers, banners or overlays
- **2.5.7** Dragging movements have a single-pointer alternative
- **2.5.8** Target size >= 24x24 CSS pixels, or enough spacing around smaller targets. For touch interfaces, recommend
  44x44 (2.5.5, Level AAA) or the platform guideline as best practice, not as an AA failure

### Understandable

- **3.2.1** Predictable on focus (no unexpected changes)
- **3.2.6** Help mechanisms appear in a consistent place
- **3.3.1** Error identification (describe the error)
- **3.3.2** Labels or instructions for inputs
- **3.3.7** Previously entered information is not requested again in the same process
- **3.3.8** Authentication does not rely on a cognitive test without an alternative

### Robust

- **4.1.2** Name, role, value for all UI components

## Common Issues

1. Insufficient color contrast
2. Missing form labels
3. No keyboard access to interactive elements
4. Missing alt text on meaningful images
5. Focus traps in modals
6. Missing ARIA landmarks
7. Auto-playing media without controls
8. Time limits without extension options

## Testing Approach

1. Automated scan (catches ~30% of issues)
2. Keyboard-only navigation
3. Screen reader testing (VoiceOver, NVDA)
4. Color contrast verification
5. Zoom to 200% — does layout break?

## Output

```markdown
## Accessibility Audit: [Design/Page Name]

**Standard:** WCAG 2.2 AA | **Date:** [Date]

### Summary

**Issues found:** [X] | **Critical:** [X] | **Major:** [X] | **Minor:** [X]

### Findings

#### Perceivable

| #   | Issue   | WCAG Criterion   | Severity    | Recommendation |
| --- | ------- | ---------------- | ----------- | -------------- |
| 1   | [Issue] | [1.4.3 Contrast] | 🔴 Critical | [Fix]          |

#### Operable

| #   | Issue   | WCAG Criterion   | Severity | Recommendation |
| --- | ------- | ---------------- | -------- | -------------- |
| 1   | [Issue] | [2.1.1 Keyboard] | 🟡 Major | [Fix]          |

#### Understandable

| #   | Issue   | WCAG Criterion | Severity | Recommendation |
| --- | ------- | -------------- | -------- | -------------- |
| 1   | [Issue] | [3.3.2 Labels] | 🟢 Minor | [Fix]          |

#### Robust

| #   | Issue   | WCAG Criterion            | Severity | Recommendation |
| --- | ------- | ------------------------- | -------- | -------------- |
| 1   | [Issue] | [4.1.2 Name, Role, Value] | 🟡 Major | [Fix]          |

### Color Contrast Check

| Element     | Foreground | Background | Ratio | Required | Pass? |
| ----------- | ---------- | ---------- | ----- | -------- | ----- |
| [Body text] | [color]    | [color]    | [X]:1 | 4.5:1    | ✅/❌ |

### Keyboard Navigation

| Element   | Tab Order | Enter/Space | Escape     | Arrow Keys |
| --------- | --------- | ----------- | ---------- | ---------- |
| [Element] | [Order]   | [Behavior]  | [Behavior] | [Behavior] |

### Screen Reader

| Element   | Announced As   | Issue            |
| --------- | -------------- | ---------------- |
| [Element] | [What SR says] | [Problem if any] |

### Priority Fixes

1. **[Critical fix]** — Affects [who] and blocks [what]
2. **[Major fix]** — Improves [what] for [who]
3. **[Minor fix]** — Nice to have
```

## Tips

1. **Start with contrast and keyboard** — These catch the most common and impactful issues.
2. **Test with real assistive technology** — My audit is a great start, but manual testing with VoiceOver/NVDA catches
   things I can't.
3. **Prioritize by impact** — Fix issues that block users first, polish later.
