---
name: wcag-compliance-reviewer
description: Review HTML/CSS and React/TypeScript code for WCAG 2.1 Level AA accessibility compliance. Use when the user asks to review code for accessibility, check WCAG compliance, identify accessibility issues, or audit components/pages for a11y standards. Applicable for code reviews, component development, and accessibility testing.
---

# WCAG 2.1 AA Compliance Reviewer

## Overview

Review code changes for WCAG 2.1 Level AA accessibility compliance in HTML/CSS and React/TypeScript components. This skill identifies violations, provides specific fixes, and recommends automated testing approaches.

## Review Process

Follow this structured approach when reviewing code for accessibility:

### 1. Determine WCAG Version and Source

**Default:** Use WCAG 2.1 AA from static reference (`references/wcag-aa-guidelines.md`)

**Fetch from W3C website if:**
- User asks for "latest guidelines"
- User specifies WCAG 2.2 or asks "what's new in WCAG 2.2"
- User requests "official W3C guidelines" or "pull from the website"
- Uncertain whether guidelines have been updated

**Example user phrases that trigger web fetch:**
- "Check against the latest WCAG standards"
- "Use the current W3C guidelines"
- "Review with WCAG 2.2"
- "Pull the official accessibility guidelines"

### 2. Initial Assessment

Read the code and identify:
- File types (HTML, CSS, JSX/TSX)
- Interactive elements (buttons, forms, links, custom controls)
- Dynamic content (modals, tooltips, notifications)
- Media content (images, videos, audio)

### 3. Load Relevant References

Based on the code type and complexity, load the appropriate reference files:

**WCAG Guidelines Source:**

Choose one of these approaches based on user request:

**Option A: Use static reference (default, faster)**
- `references/wcag-aa-guidelines.md` - Complete WCAG 2.1 AA success criteria
- Use when user doesn't specifically request latest/live guidelines

**Option B: Fetch from official W3C website**

Use when user:
- Explicitly asks for "latest" or "current" guidelines
- Asks to check against WCAG 2.2 or newer version
- Wants to verify against official source
- Says "pull from the website" or similar

Fetch using web_fetch:
```
WCAG 2.1 AA Quick Reference:
https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1&levels=a,aa

WCAG 2.2 AA Quick Reference (newer):
https://www.w3.org/WAI/WCAG22/quickref/?versions=2.2&levels=a,aa

Understanding WCAG 2.1:
https://www.w3.org/WAI/WCAG21/Understanding/

Understanding WCAG 2.2:
https://www.w3.org/WAI/WCAG22/Understanding/
```

After fetching, combine official guidelines with code examples from `references/common-violations.md`

**Always load when reviewing code:**
- `references/common-violations.md` - Code examples and fixes for HTML/CSS/React/TypeScript
- `references/testing-guide.md` - When user asks about testing or wants to set up automated checks

### 4. Systematic Review by WCAG Principle

Review code against the four WCAG principles in this order:

**A. Perceivable (Priority: High)**
1. Check all images for alt text (1.1.1)
2. Verify color contrast ratios (1.4.3, 1.4.11)
3. Confirm no information conveyed by color alone (1.4.1)
4. Check semantic HTML structure (1.3.1)
5. Verify proper heading hierarchy (1.3.1)
6. Check responsive reflow at 320px (1.4.10)
7. Verify text spacing compatibility (1.4.12)

**B. Operable (Priority: High)**
1. Test keyboard accessibility - all interactive elements must be keyboard operable (2.1.1)
2. Verify focus indicators are visible with 3:1 contrast (2.4.7)
3. Check focus order is logical (2.4.3)
4. Verify no keyboard traps exist (2.1.2)
5. Check skip links or landmarks for navigation (2.4.1)
6. Verify descriptive link text (2.4.4)

**C. Understandable (Priority: Medium)**
1. Check lang attribute on html element (3.1.1)
2. Verify form labels are present and associated (3.3.2)
3. Check error identification and suggestions (3.3.1, 3.3.3)
4. Verify consistent navigation patterns (3.2.3)
5. Check no context changes on focus/input (3.2.1, 3.2.2)

**D. Robust (Priority: Medium)**
1. Verify semantic HTML or proper ARIA (4.1.2)
2. Check ARIA attributes are valid (4.1.2)
3. Verify status messages use ARIA live regions (4.1.3)
4. Check all interactive elements have accessible names (4.1.2)

### 5. Categorize Issues by Severity

**Errors (Must Fix):**
- Missing alt text on images
- Insufficient color contrast (< 4.5:1 for text, < 3:1 for UI components)
- Keyboard inaccessible elements
- Missing form labels
- Invalid ARIA attributes
- Missing focus indicators
- Missing lang attribute

**Warnings (Should Fix):**
- Positive tabindex values
- autoFocus usage
- Links without descriptive text
- Potential color-only indicators
- Missing autocomplete on user data inputs

**Recommendations (Best Practices):**
- Use semantic HTML over ARIA when possible
- Add descriptive page titles
- Implement skip links
- Use ARIA landmarks consistently

### 6. Provide Specific Fixes

For each issue identified:

1. **Quote the problematic code** from the user's file
2. **Explain the WCAG violation** with specific success criterion reference
3. **Provide corrected code** using examples from `common-violations.md`
4. **Explain why the fix works** in terms of assistive technology interaction

Example format:
```
❌ Issue: Missing alt text (WCAG 1.1.1 - Level A)

Line 23:
<img src="logo.png">

✅ Fix:
<img src="logo.png" alt="Company Name Logo">

Why: Screen readers announce "logo.png" without alt text, which is not meaningful. The alt text provides the image's purpose.
```

### 7. Recommend Testing Approach

Based on the code complexity, recommend appropriate testing tools from `references/testing-guide.md`:

**For all reviews, recommend:**
- eslint-plugin-jsx-a11y for linting during development
- Browser extension (axe DevTools or WAVE) for quick checks

**For component libraries or complex UIs, additionally recommend:**
- jest-axe for component testing
- Keyboard navigation testing
- Screen reader testing with NVDA/VoiceOver

**For full applications, additionally recommend:**
- pa11y-ci or Lighthouse CI for automated testing
- Comprehensive manual testing checklist

### 8. Summary Output Format

Structure the review output as follows:

```
# Accessibility Review Summary

## Issues Found: X errors, Y warnings

### Critical Issues (Errors)
[List each error with line number, rule, and fix]

### Warnings
[List each warning with line number, rule, and fix]

### Recommendations
[List best practice improvements]

## Testing Recommendations
[Specific tools and approaches for this codebase]

## Quick Wins
[Easy fixes that provide significant accessibility improvements]
```

## Quick Reference Checklist

Use this for rapid reviews:

**Images & Media:**
- [ ] All images have alt text
- [ ] Decorative images use alt="" or aria-hidden="true"
- [ ] Complex images have longer descriptions

**Forms:**
- [ ] All inputs have labels (label, aria-label, or aria-labelledby)
- [ ] Errors are associated with fields (aria-describedby, aria-invalid)
- [ ] Required fields are marked
- [ ] Autocomplete attributes on user data inputs

**Keyboard & Focus:**
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible (3:1 contrast)
- [ ] No positive tabindex values
- [ ] Logical focus order
- [ ] No keyboard traps in modals/dialogs

**Color & Contrast:**
- [ ] Text contrast ≥ 4.5:1 (normal text)
- [ ] Text contrast ≥ 3:1 (large text: 18pt+ or 14pt+ bold)
- [ ] UI component contrast ≥ 3:1
- [ ] Information not conveyed by color alone

**Structure & Semantics:**
- [ ] Semantic HTML (header, nav, main, article, footer)
- [ ] Proper heading hierarchy (h1-h6, no skipped levels)
- [ ] Lists use ul/ol/dl
- [ ] Buttons use <button>, links use <a>
- [ ] lang attribute on <html> element

**ARIA:**
- [ ] ARIA used only when necessary (prefer semantic HTML)
- [ ] ARIA attributes are valid
- [ ] ARIA states update dynamically
- [ ] Status messages use live regions
- [ ] Custom controls have proper roles and states

**Dynamic Content:**
- [ ] Modals trap focus and restore on close
- [ ] Status updates announced (aria-live)
- [ ] Loading states indicated
- [ ] Error messages clear and helpful

## Code Examples for Common Patterns

### Accessible Button with Icon
```tsx
// ✅ Good - TypeScript
<button onClick={handleDelete} aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>
```

### Accessible Modal
```tsx
// ✅ Good - Focus trap and restoration
<div 
  role="dialog" 
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Modal Title</h2>
  <button onClick={onClose}>Close</button>
  {children}
</div>
```

### Form with Error Handling
```tsx
// ✅ Good - Associated error, proper ARIA
<label htmlFor="email">Email:</label>
<input 
  type="email" 
  id="email"
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : undefined}
/>
{error && (
  <div id="email-error" role="alert">
    {error}
  </div>
)}
```

## Using the Automated Checker Script

For initial scanning of files, use the provided Python script:

```bash
python scripts/check_wcag.py path/to/component.tsx
```

This performs static analysis to catch common issues like:
- Missing alt text
- onClick without keyboard handlers
- Missing form labels
- Focus outline removal
- Potential contrast issues

**Note:** The script catches ~30% of issues. Always perform comprehensive manual review using the full checklist above.

## Resources

### scripts/
- `check_wcag.py` - Automated accessibility checker for HTML/CSS/React/TypeScript files

### references/
- `wcag-aa-guidelines.md` - Complete WCAG 2.1 Level AA success criteria organized by principle
- `common-violations.md` - Common accessibility violations with before/after code examples for HTML/CSS and React/TypeScript
- `testing-guide.md` - Automated testing tools, setup instructions, and manual testing checklists
