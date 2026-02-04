---
name: practical-ui-agent
description: AI agent skill for implementing evidence-based UI improvements. Use when tasked with UI audits, design system implementation, accessibility fixes, or frontend optimization. Provides step-by-step workflows, code patterns, and validation criteria for automated execution. Triggers on UI review, accessibility audit, design system setup, CSS refactoring, form optimization, button hierarchy, color contrast, spacing system, typography scale, or WCAG compliance tasks.
---

# Practical UI Agent Skill

Executable workflows for AI agents to audit, implement, and validate UI improvements based on evidence-based design principles.

## Agent Instructions

When this skill is triggered:
1. First determine the **task type** (audit, implement, or fix)
2. Load the relevant **reference file(s)** from `/references`
3. Follow the **workflow** for that task type
4. Validate changes against the **acceptance criteria**
5. Report findings in the specified **output format**

## Task Type Detection

Analyze the user request and classify:

| User Says | Task Type | Primary Reference |
|-----------|-----------|-------------------|
| "audit", "review", "check", "analyze" | `AUDIT` | All references |
| "fix", "improve", "update", "refactor" | `FIX` | Specific to issue |
| "create", "build", "implement", "setup" | `IMPLEMENT` | design-system.md |
| "accessibility", "a11y", "WCAG" | `AUDIT` + `FIX` | accessibility.md |

---

## Workflow: AUDIT

Execute this workflow when auditing an existing UI.

### Step 1: Gather Files

```bash
# Find all CSS/SCSS files
find . -type f \( -name "*.css" -o -name "*.scss" -o -name "*.less" \) | head -50

# Find all component files
find . -type f \( -name "*.jsx" -o -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" \) | head -50

# Find HTML templates
find . -type f \( -name "*.html" -o -name "*.ejs" -o -name "*.hbs" \) | head -50
```

### Step 2: Run Checks

Execute each check and record pass/fail:

#### 2.1 Color Contrast Check
```javascript
// Look for these patterns in CSS - FLAG as potential issues:
const lowContrastPatterns = [
  /color:\s*#[a-fA-F0-9]{6}.*gray|grey/i,  // gray text
  /color:\s*rgba?\([^)]*,\s*0\.[0-6]/,      // low opacity text
  /opacity:\s*0\.[0-6]/,                     // low opacity elements
  /#[cdef][cdef][cdef]/i,                    // very light hex colors
];

// Extract all color pairs (background + text) and calculate contrast
// Minimum requirements:
// - Small text (<18px): 4.5:1
// - Large text (≥18px bold or ≥24px): 3:1
// - UI components: 3:1
```

#### 2.2 Spacing Consistency Check
```javascript
// Extract all spacing values from CSS
const spacingRegex = /(?:margin|padding|gap).*?:\s*(\d+)(?:px|rem|em)/g;

// Flag if NOT using 8pt system (8, 16, 24, 32, 48, 64, 80)
const valid8ptValues = [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80];
// Allow 4px for fine adjustments, multiples of 8 preferred
```

#### 2.3 Typography Scale Check
```javascript
// Extract all font-size values
const fontSizeRegex = /font-size:\s*(\d+(?:\.\d+)?)(px|rem|em)/g;

// Recommended scale (1.25 ratio): 12, 14, 16, 18, 22, 28, 35, 44
// Flag arbitrary values like 13px, 17px, 19px, 23px
// Flag body text < 16px
// Flag line-height < 1.4 for body text
```

#### 2.4 Button Hierarchy Check
```javascript
// Find all button elements and their styles
// Check for:
// - Multiple "primary" styled buttons in same view (FLAG)
// - Buttons without sufficient contrast (FLAG)
// - Touch targets < 44px height on mobile (FLAG)
// - Vague labels: "Submit", "Click here", "OK" (FLAG)
```

#### 2.5 Form Accessibility Check
```javascript
// For each <input>, <select>, <textarea>:
// - Has associated <label> with matching for/id (REQUIRED)
// - Placeholder is NOT the only label (FLAG if no <label>)
// - Required fields are marked (check for required attr or aria-required)
// - Error messages exist and are associated (aria-describedby)
```

### Step 3: Generate Report

Output format:
```markdown
## UI Audit Report

### Summary
- **Critical Issues**: [count]
- **Warnings**: [count]
- **Passed Checks**: [count]

### Critical Issues (Must Fix)
1. [Issue]: [File:Line] - [Description]
   **Fix**: [Specific code change]

### Warnings (Should Fix)
1. [Issue]: [File:Line] - [Description]
   **Fix**: [Specific code change]

### Passed
- ✓ [Check name]
```

---

## Workflow: IMPLEMENT Design System

Execute this workflow when setting up a new design system.

### Step 1: Create CSS Custom Properties

Create file: `design-tokens.css`

```css
:root {
  /* ==========================================================================
     SPACING SYSTEM (8pt base)
     ========================================================================== */
  --space-xs: 8px;    /* 0.5rem - icon gaps, tight grouping */
  --space-sm: 16px;   /* 1rem - related elements */
  --space-md: 24px;   /* 1.5rem - section padding */
  --space-lg: 32px;   /* 2rem - between groups */
  --space-xl: 48px;   /* 3rem - major sections */
  --space-2xl: 64px;  /* 4rem - page sections */
  --space-3xl: 80px;  /* 5rem - hero areas */

  /* ==========================================================================
     TYPOGRAPHY SCALE (1.25 ratio, 18px base)
     ========================================================================== */
  --text-xs: 0.75rem;   /* 12px - fine print only */
  --text-sm: 0.875rem;  /* 14px - captions, meta */
  --text-base: 1rem;    /* 16px - UI text */
  --text-md: 1.125rem;  /* 18px - body text */
  --text-lg: 1.375rem;  /* 22px - H4 */
  --text-xl: 1.75rem;   /* 28px - H3 */
  --text-2xl: 2.25rem;  /* 36px - H2 */
  --text-3xl: 2.75rem;  /* 44px - H1 */

  /* Line Heights */
  --leading-tight: 1.2;    /* headings */
  --leading-snug: 1.3;     /* H3, H4 */
  --leading-normal: 1.5;   /* body text minimum */
  --leading-relaxed: 1.65; /* long-form reading */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* ==========================================================================
     COLOR SYSTEM (Monochromatic + Brand)
     Replace HSL values with your brand color's hue
     ========================================================================== */
  --hue: 220; /* Base hue - change this to your brand color */
  
  /* Light mode palette */
  --color-primary: hsl(var(--hue), 70%, 50%);
  --color-primary-hover: hsl(var(--hue), 70%, 42%);
  
  --color-text-primary: hsl(var(--hue), 50%, 15%);    /* Headings: 4.5:1+ */
  --color-text-secondary: hsl(var(--hue), 20%, 40%);  /* Body: 4.5:1+ */
  --color-text-tertiary: hsl(var(--hue), 15%, 55%);   /* Meta: 4.5:1+ */
  
  --color-border: hsl(var(--hue), 15%, 75%);          /* 3:1 for UI */
  --color-border-light: hsl(var(--hue), 10%, 88%);    /* Decorative */
  
  --color-surface: hsl(var(--hue), 10%, 98%);         /* Alt background */
  --color-background: hsl(0, 0%, 100%);               /* Main background */

  /* System colors */
  --color-error: hsl(0, 70%, 50%);
  --color-error-bg: hsl(0, 70%, 97%);
  --color-warning: hsl(40, 90%, 50%);
  --color-warning-bg: hsl(40, 90%, 97%);
  --color-success: hsl(140, 60%, 40%);
  --color-success-bg: hsl(140, 60%, 97%);

  /* ==========================================================================
     SHADOWS (Elevation levels)
     ========================================================================== */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);

  /* ==========================================================================
     BORDERS
     ========================================================================== */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* ==========================================================================
     TRANSITIONS
     ========================================================================== */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;

  /* ==========================================================================
     LAYOUT
     ========================================================================== */
  --max-width-content: 65ch;  /* Optimal line length */
  --max-width-wide: 1200px;
  --min-tap-target: 44px;     /* WCAG touch target */
}
```

### Step 2: Create Base Typography

Create file: `typography.css`

```css
/* ==========================================================================
   BASE TYPOGRAPHY
   ========================================================================== */

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: var(--text-md);
  line-height: var(--leading-normal);
  color: var(--color-text-secondary);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
  color: var(--color-text-primary);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  margin-top: 0;
}

h1 {
  font-size: var(--text-3xl);
  letter-spacing: -0.02em;
  margin-bottom: var(--space-lg);
}

h2 {
  font-size: var(--text-2xl);
  letter-spacing: -0.01em;
  margin-bottom: var(--space-md);
}

h3 {
  font-size: var(--text-xl);
  line-height: var(--leading-snug);
  margin-bottom: var(--space-sm);
}

h4 {
  font-size: var(--text-lg);
  line-height: var(--leading-snug);
  margin-bottom: var(--space-sm);
}

p {
  margin-top: 0;
  margin-bottom: var(--space-md);
  max-width: var(--max-width-content);
}

/* Long-form content */
.prose {
  font-size: var(--text-md);
  line-height: var(--leading-relaxed);
}

.prose p {
  margin-bottom: var(--space-md);
}

/* Small text */
.text-sm {
  font-size: var(--text-sm);
}

.text-xs {
  font-size: var(--text-xs);
}

/* Links */
a {
  color: var(--color-primary);
  text-decoration: underline;
  text-underline-offset: 2px;
}

a:hover {
  color: var(--color-primary-hover);
}

/* Remove underline for nav/card links */
.nav a,
.card a {
  text-decoration: none;
}
```

### Step 3: Create Button System

Create file: `buttons.css`

```css
/* ==========================================================================
   BUTTON SYSTEM - Three weights
   ========================================================================== */

/* Base button styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  
  min-height: var(--min-tap-target);
  padding: var(--space-xs) var(--space-sm);
  
  font-family: inherit;
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  
  transition: 
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast);
}

/* Focus state - WCAG compliant */
.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* ==========================================================================
   PRIMARY - One per view, most important action
   ========================================================================== */
.btn-primary {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

/* ==========================================================================
   SECONDARY - Less important actions
   ========================================================================== */
.btn-secondary {
  background-color: transparent;
  border-color: var(--color-border);
  color: var(--color-text-primary);
}

.btn-secondary:hover {
  border-color: var(--color-text-secondary);
  background-color: var(--color-surface);
}

/* ==========================================================================
   TERTIARY - Least important actions
   ========================================================================== */
.btn-tertiary {
  background-color: transparent;
  border-color: transparent;
  color: var(--color-primary);
  padding-left: var(--space-xs);
  padding-right: var(--space-xs);
}

.btn-tertiary:hover {
  background-color: var(--color-surface);
}

/* ==========================================================================
   DESTRUCTIVE - Delete, remove actions
   ========================================================================== */
.btn-destructive {
  background-color: transparent;
  border-color: var(--color-border);
  color: var(--color-error);
}

.btn-destructive:hover {
  background-color: var(--color-error-bg);
  border-color: var(--color-error);
}

/* ==========================================================================
   SIZES
   ========================================================================== */
.btn-sm {
  min-height: 36px;
  padding: 6px var(--space-xs);
  font-size: var(--text-sm);
}

.btn-lg {
  min-height: 52px;
  padding: var(--space-sm) var(--space-md);
  font-size: var(--text-md);
}

/* ==========================================================================
   DISABLED STATE - Use sparingly, prefer validation on click
   ========================================================================== */
.btn:disabled,
.btn[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Icon sizing within buttons */
.btn svg {
  width: 1.25em;
  height: 1.25em;
  flex-shrink: 0;
}
```

### Step 4: Create Form System

Create file: `forms.css`

```css
/* ==========================================================================
   FORM SYSTEM
   ========================================================================== */

/* Form layout */
.form-group {
  margin-bottom: var(--space-md);
}

/* Labels */
.form-label {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--color-text-primary);
}

/* Required indicator */
.form-label[data-required]::after {
  content: " *";
  color: var(--color-error);
}

/* Optional indicator */
.form-label-optional::after {
  content: " (optional)";
  font-weight: var(--font-normal);
  color: var(--color-text-tertiary);
}

/* Hint text - above field */
.form-hint {
  display: block;
  margin-bottom: var(--space-xs);
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
}

/* ==========================================================================
   INPUT FIELDS
   ========================================================================== */
.form-input,
.form-select,
.form-textarea {
  display: block;
  width: 100%;
  min-height: var(--min-tap-target);
  padding: var(--space-xs) var(--space-sm);
  
  font-family: inherit;
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--color-text-primary);
  
  background-color: var(--color-background);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  
  transition: border-color var(--transition-fast);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* Placeholder - must have sufficient contrast */
.form-input::placeholder {
  color: var(--color-text-tertiary);
}

/* Textarea */
.form-textarea {
  min-height: 120px;
  resize: vertical;
}

/* Select */
.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--space-sm) center;
  padding-right: var(--space-xl);
}

/* ==========================================================================
   FIELD WIDTHS - Match expected input length
   ========================================================================== */
.form-input-xs { max-width: 80px; }   /* CVV, 2-char state */
.form-input-sm { max-width: 120px; }  /* ZIP, year */
.form-input-md { max-width: 200px; }  /* Phone */
.form-input-lg { max-width: 320px; }  /* Email */
/* Full width is default */

/* ==========================================================================
   CHECKBOXES & RADIOS
   ========================================================================== */
.form-check {
  display: flex;
  align-items: flex-start;
  gap: var(--space-xs);
  min-height: var(--min-tap-target);
  padding: calc((var(--min-tap-target) - 1.5em) / 2) 0;
}

.form-check-input {
  flex-shrink: 0;
  width: 1.25em;
  height: 1.25em;
  margin-top: 0.125em;
  
  accent-color: var(--color-primary);
  cursor: pointer;
}

.form-check-label {
  cursor: pointer;
  user-select: none;
}

/* ==========================================================================
   ERROR STATES
   ========================================================================== */
.form-input-error,
.form-select-error,
.form-textarea-error {
  border-color: var(--color-error);
  background-color: var(--color-error-bg);
}

.form-error-message {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  margin-top: var(--space-xs);
  font-size: var(--text-sm);
  color: var(--color-error);
}

/* Error icon */
.form-error-message::before {
  content: "";
  flex-shrink: 0;
  width: 1em;
  height: 1em;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%23dc2626'%3E%3Cpath fill-rule='evenodd' d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-size: contain;
}

/* ==========================================================================
   SUCCESS STATES
   ========================================================================== */
.form-input-success {
  border-color: var(--color-success);
}
```

### Step 5: Validate Implementation

Run these checks after implementation:

```javascript
// Validation script
const validationChecks = {
  // Check 1: All buttons have accessible names
  buttons: () => {
    const buttons = document.querySelectorAll('button, [role="button"], .btn');
    return Array.from(buttons).every(btn => {
      const text = btn.textContent?.trim() || btn.getAttribute('aria-label');
      return text && text.length > 0;
    });
  },
  
  // Check 2: All form inputs have labels
  formLabels: () => {
    const inputs = document.querySelectorAll('input, select, textarea');
    return Array.from(inputs).every(input => {
      if (input.type === 'hidden') return true;
      const id = input.id;
      const label = document.querySelector(`label[for="${id}"]`);
      const ariaLabel = input.getAttribute('aria-label');
      const ariaLabelledBy = input.getAttribute('aria-labelledby');
      return label || ariaLabel || ariaLabelledBy;
    });
  },
  
  // Check 3: No multiple primary buttons in same section
  buttonHierarchy: () => {
    const sections = document.querySelectorAll('section, article, form, .card, [role="dialog"]');
    return Array.from(sections).every(section => {
      const primaryBtns = section.querySelectorAll('.btn-primary');
      return primaryBtns.length <= 1;
    });
  },
  
  // Check 4: Touch targets meet minimum size
  touchTargets: () => {
    const interactive = document.querySelectorAll('button, a, input, select, [role="button"]');
    return Array.from(interactive).every(el => {
      const rect = el.getBoundingClientRect();
      return rect.height >= 44 && rect.width >= 44;
    });
  }
};
```

---

## Workflow: FIX Specific Issues

### Fix: Low Contrast Text

**Detection pattern:**
```css
/* Find these patterns */
color: #999;
color: #aaa;
color: #bbb;
color: #ccc;
color: gray;
color: darkgray;
color: rgba(0,0,0,0.4);
color: rgba(0,0,0,0.5);
```

**Fix pattern:**
```css
/* Replace with */
color: var(--color-text-secondary);  /* For body text: min 4.5:1 */
color: var(--color-text-tertiary);   /* For meta text: min 4.5:1 */
```

### Fix: Inconsistent Spacing

**Detection pattern:**
```css
/* Find arbitrary values */
margin: 13px;
padding: 17px;
gap: 11px;
margin-bottom: 23px;
```

**Fix pattern:**
```css
/* Replace with 8pt system tokens */
margin: var(--space-sm);      /* 16px */
padding: var(--space-md);     /* 24px */
gap: var(--space-sm);         /* 16px */
margin-bottom: var(--space-md); /* 24px */
```

### Fix: Missing Form Labels

**Detection pattern:**
```html
<!-- FLAG: Placeholder as only label -->
<input type="email" placeholder="Email">

<!-- FLAG: No label association -->
<label>Email</label>
<input type="email">
```

**Fix pattern:**
```html
<!-- Correct: Associated label -->
<label for="email" class="form-label">Email</label>
<input type="email" id="email" class="form-input">

<!-- Alternative: aria-label -->
<input type="email" aria-label="Email address" class="form-input">
```

### Fix: Multiple Primary Buttons

**Detection pattern:**
```html
<!-- FLAG: Two primaries in same form -->
<form>
  <button class="btn-primary">Save</button>
  <button class="btn-primary">Save & Continue</button>
</form>
```

**Fix pattern:**
```html
<!-- Correct: One primary, one secondary -->
<form>
  <button class="btn-primary">Save & Continue</button>
  <button class="btn-secondary">Save draft</button>
</form>
```

### Fix: Small Touch Targets

**Detection pattern:**
```css
/* Find small interactive elements */
.icon-btn {
  width: 24px;
  height: 24px;
}

a.small-link {
  padding: 4px;
  font-size: 12px;
}
```

**Fix pattern:**
```css
/* Ensure 44px minimum tap area */
.icon-btn {
  width: 24px;
  height: 24px;
  /* Add padding to reach 44px tap target */
  padding: 10px;
  margin: -10px;
}

a.small-link {
  padding: 12px 8px;
  font-size: 14px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
}
```

---

## Decision Trees

### When User Says "Make it look better"

```
1. Run AUDIT workflow
2. Prioritize fixes by impact:
   a. CRITICAL: Accessibility failures (contrast, labels, focus)
   b. HIGH: Spacing inconsistencies, typography scale
   c. MEDIUM: Button hierarchy, color system
   d. LOW: Decorative improvements
3. Implement fixes in priority order
4. Validate each change
```

### When User Says "Set up a design system"

```
1. Check if design tokens exist
   ├─ YES → Audit existing tokens against recommendations
   └─ NO → Implement Step 1-4 from IMPLEMENT workflow
2. Check if component styles exist
   ├─ YES → Audit for consistency with tokens
   └─ NO → Create buttons.css, forms.css, typography.css
3. Document usage guidelines
```

### When User Says "Fix accessibility"

```
1. Run automated checks:
   - Color contrast (4.5:1 text, 3:1 UI)
   - Form labels
   - Focus indicators
   - Touch target sizes
2. For each failure:
   a. Identify the specific element
   b. Apply the corresponding fix pattern
   c. Validate the fix
3. Generate accessibility report
```

---

## Output Formats

### Audit Report Format

```markdown
## UI Audit: [Project Name]
**Date**: [ISO date]
**Scope**: [Files/components audited]

### Critical Issues ([count])
| Issue | Location | Current | Recommended | Fix |
|-------|----------|---------|-------------|-----|
| Low contrast | btn.css:42 | #999 (2.8:1) | #595959 (7:1) | `color: var(--color-text-secondary)` |

### Warnings ([count])
...

### Passed Checks
- ✓ Button hierarchy
- ✓ Form labels
...
```

### Implementation Checklist Format

```markdown
## Design System Implementation

- [ ] Created design-tokens.css
- [ ] Created typography.css
- [ ] Created buttons.css
- [ ] Created forms.css
- [ ] Updated existing components to use tokens
- [ ] Validated contrast ratios
- [ ] Validated touch targets
- [ ] Tested keyboard navigation
```

---

## Reference Files

Load these for detailed implementation guidance:

| File | Use When |
|------|----------|
| [accessibility.md](references/accessibility.md) | WCAG compliance, screen readers, focus states |
| [color-system.md](references/color-system.md) | Palette creation, contrast calculation, dark mode |
| [spacing-system.md](references/spacing-system.md) | 8pt grid, spacing tokens, layout decisions |
| [typography-system.md](references/typography-system.md) | Type scale, line height, font selection |
| [buttons.md](references/buttons.md) | Three-weight system, states, destructive actions |
| [forms.md](references/forms.md) | Input patterns, validation, error display |
| [copywriting.md](references/copywriting.md) | Labels, error messages, microcopy |
