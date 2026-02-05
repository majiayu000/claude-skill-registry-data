---
name: accessibility
description: WCAG 2.2 AA compliance, ARIA patterns, screen reader compatibility, and inclusive design patterns
sasmp_version: "1.3.0"
bonded_agent: html-expert
bond_type: PRIMARY_BOND
version: "2.0.0"

# Skill Metadata
category: accessibility
complexity: advanced
dependencies:
  - html-basics
  - semantic-html

# Parameter Validation
parameters:
  audit_level:
    type: string
    required: true
    enum: ["A", "AA", "AAA"]
    default: "AA"
  component_type:
    type: string
    enum: [interactive, form, navigation, media, content, widget]
  output_format:
    type: string
    default: "report"
    enum: [report, fixes, both]

# Retry Configuration
retry:
  max_attempts: 3
  backoff_ms: [1000, 2000, 4000]
  retryable_errors: [AUDIT_TIMEOUT, EXTERNAL_TOOL_ERROR]
---

# Accessibility Skill

WCAG 2.2 compliance and ARIA implementation for inclusive, accessible web experiences.

## 🎯 Purpose

Provide atomic, single-responsibility operations for:
- WCAG 2.2 Level A/AA/AAA auditing
- ARIA roles, states, and properties
- Keyboard navigation patterns
- Screen reader optimization
- Focus management
- Color contrast verification

---

## 📥 Input Schema

```typescript
interface AccessibilityInput {
  operation: 'audit' | 'fix' | 'pattern' | 'explain';
  audit_level: 'A' | 'AA' | 'AAA';
  markup?: string;
  component_type?: ComponentType;
  context?: {
    user_agents: string[];     // Target screen readers
    focus_management: boolean;
    color_scheme: 'light' | 'dark' | 'both';
  };
}

type ComponentType =
  | 'interactive'   // Buttons, links, controls
  | 'form'          // Form elements
  | 'navigation'    // Menus, breadcrumbs
  | 'media'         // Images, video, audio
  | 'content'       // Text, headings, lists
  | 'widget';       // Custom components
```

## 📤 Output Schema

```typescript
interface AccessibilityOutput {
  success: boolean;
  wcag_level: 'A' | 'AA' | 'AAA';
  score: number;              // 0-100
  issues: A11yIssue[];
  fixes: A11yFix[];
  passed_criteria: string[];
  failed_criteria: string[];
}

interface A11yIssue {
  criterion: string;          // e.g., "1.4.3"
  level: 'A' | 'AA' | 'AAA';
  impact: 'critical' | 'serious' | 'moderate' | 'minor';
  element: string;
  message: string;
  fix: string;
}
```

---

## 🛠️ WCAG 2.2 Quick Reference

### The Four Principles (POUR)

```
┌─────────────────────────────────────────────────────────────┐
│                        WCAG POUR                             │
├────────────────┬────────────────┬────────────────┬──────────┤
│   PERCEIVABLE  │   OPERABLE     │ UNDERSTANDABLE │  ROBUST  │
├────────────────┼────────────────┼────────────────┼──────────┤
│ Text alt       │ Keyboard       │ Readable       │ Compatible│
│ Captions       │ Enough time    │ Predictable    │ Parsing  │
│ Adaptable      │ Seizures       │ Input assist   │          │
│ Distinguishable│ Navigable      │                │          │
│                │ Input modality │                │          │
└────────────────┴────────────────┴────────────────┴──────────┘
```

### WCAG 2.2 New Success Criteria (AA)

| Criterion | Name | Requirement |
|-----------|------|-------------|
| 2.4.11 | Focus Not Obscured | Focus never completely hidden |
| 2.5.7 | Dragging Movements | Alternative to drag operations |
| 2.5.8 | Target Size (Minimum) | 24x24px minimum touch targets |
| 3.2.6 | Consistent Help | Help in same relative location |
| 3.3.7 | Redundant Entry | Don't re-ask for same info |
| 3.3.8 | Accessible Authentication | No cognitive tests for login |

---

## 🎨 ARIA Patterns

### 1. Interactive Widgets

#### Button

```html
<!-- Native button (preferred) -->
<button type="button">Click me</button>

<!-- Custom button (when native not possible) -->
<div role="button"
     tabindex="0"
     aria-pressed="false"
     onkeydown="handleKeydown(event)">
  Toggle
</div>
```

#### Dialog (Modal)

```html
<div role="dialog"
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

#### Tabs

```html
<div role="tablist" aria-label="Settings">
  <button role="tab"
          aria-selected="true"
          aria-controls="panel-1"
          id="tab-1">
    General
  </button>
  <button role="tab"
          aria-selected="false"
          aria-controls="panel-2"
          id="tab-2"
          tabindex="-1">
    Privacy
  </button>
</div>

<div role="tabpanel"
     id="panel-1"
     aria-labelledby="tab-1">
  General settings content...
</div>

<div role="tabpanel"
     id="panel-2"
     aria-labelledby="tab-2"
     hidden>
  Privacy settings content...
</div>
```

### 2. Live Regions

```html
<!-- Polite announcement (waits for pause) -->
<div aria-live="polite" aria-atomic="true">
  3 items in cart
</div>

<!-- Assertive announcement (interrupts) -->
<div role="alert" aria-live="assertive">
  Error: Please fix the form errors
</div>

<!-- Status message -->
<div role="status" aria-live="polite">
  File uploaded successfully
</div>
```

### 3. Form Patterns

```html
<form>
  <!-- Required field -->
  <label for="email">Email (required)</label>
  <input type="email"
         id="email"
         name="email"
         required
         aria-required="true"
         aria-describedby="email-hint email-error">
  <p id="email-hint">We'll never share your email</p>
  <p id="email-error" role="alert" aria-live="polite"></p>

  <!-- Field with error -->
  <label for="password">Password</label>
  <input type="password"
         id="password"
         aria-invalid="true"
         aria-errormessage="pwd-error">
  <p id="pwd-error" role="alert">
    Password must be at least 8 characters
  </p>

  <!-- Checkbox group -->
  <fieldset>
    <legend>Notifications</legend>
    <label>
      <input type="checkbox" name="notify" value="email">
      Email
    </label>
    <label>
      <input type="checkbox" name="notify" value="sms">
      SMS
    </label>
  </fieldset>
</form>
```

---

## ⚠️ Error Handling

### Error Codes

| Code | Description | WCAG | Recovery |
|------|-------------|------|----------|
| `A11Y001` | Missing alt text | 1.1.1 | Add descriptive alt |
| `A11Y002` | Low color contrast | 1.4.3 | Adjust colors to 4.5:1 |
| `A11Y003` | Missing form label | 1.3.1 | Add `<label>` or aria-label |
| `A11Y004` | No keyboard access | 2.1.1 | Add tabindex, handlers |
| `A11Y005` | Missing skip link | 2.4.1 | Add skip to main content |
| `A11Y006` | Empty link/button | 2.4.4 | Add accessible text |
| `A11Y007` | Missing page title | 2.4.2 | Add descriptive `<title>` |
| `A11Y008` | Missing lang attr | 3.1.1 | Add lang to `<html>` |
| `A11Y009` | Focus not visible | 2.4.7 | Add focus styles |
| `A11Y010` | Target too small | 2.5.8 | Increase to 24x24px |

### Impact Levels

| Impact | Description | Examples |
|--------|-------------|----------|
| **Critical** | Blocks access completely | No keyboard, missing alt |
| **Serious** | Major barrier | Low contrast, no labels |
| **Moderate** | Significant difficulty | Missing skip link |
| **Minor** | Inconvenience | Suboptimal reading order |

---

## 🔍 Troubleshooting

### Problem: Screen reader not announcing content

```
Debug Checklist:
□ Element has accessible name?
□ ARIA role correct?
□ aria-hidden not incorrectly set?
□ Content not CSS display:none?
□ Live region set up correctly?
```

### Problem: Keyboard navigation broken

```
Debug Checklist:
□ All interactive elements focusable?
□ Tab order logical?
□ No keyboard traps?
□ Focus visible?
□ Custom widgets have key handlers?
□ Arrow key navigation for widgets?
```

### Problem: Form not accessible

```
Debug Checklist:
□ All inputs have labels?
□ Required fields marked?
□ Errors announced via live region?
□ Error linked with aria-errormessage?
□ Fieldsets for groups?
□ Autocomplete attributes set?
```

### Keyboard Navigation Patterns

| Component | Keys | Action |
|-----------|------|--------|
| Buttons | Enter, Space | Activate |
| Links | Enter | Navigate |
| Checkboxes | Space | Toggle |
| Radio buttons | Arrow keys | Move selection |
| Tabs | Arrow keys | Switch tabs |
| Menus | Arrow, Enter, Esc | Navigate, select, close |
| Dialogs | Esc, Tab | Close, move focus |
| Listbox | Arrow, Enter | Navigate, select |

---

## 📊 Audit Scoring

| Category | Weight | Checks |
|----------|--------|--------|
| Perceivable | 25% | Alt text, contrast, captions |
| Operable | 30% | Keyboard, focus, timing |
| Understandable | 25% | Labels, errors, consistency |
| Robust | 20% | Valid HTML, ARIA usage |

**Score Interpretation:**
- 90-100: Excellent (WCAG AA likely compliant)
- 70-89: Good (some issues to address)
- 50-69: Moderate (significant work needed)
- <50: Poor (major accessibility barriers)

---

## 📋 Usage Examples

```yaml
# Audit markup for WCAG AA
skill: accessibility
operation: audit
audit_level: "AA"
markup: "<form>...</form>"

# Get accessible pattern
skill: accessibility
operation: pattern
component_type: widget
context:
  user_agents: ["NVDA", "VoiceOver"]

# Fix accessibility issues
skill: accessibility
operation: fix
audit_level: "AA"
markup: "<img src='photo.jpg'>"
output_format: both
```

---

## 🔗 References

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Checklist](https://webaim.org/standards/wcag/checklist)
- [Deque axe Rules](https://dequeuniversity.com/rules/axe/)
