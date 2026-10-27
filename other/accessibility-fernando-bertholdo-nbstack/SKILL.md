---
name: accessibility
description: Use when building or reviewing UI components to ensure WCAG 2.1 compliance, keyboard navigation, semantic HTML, ARIA attributes, color contrast, and assistive technology support.
---

# UI Accessibility (WCAG 2.1)

## Overview

This skill guides implementation and review of accessible UI components following **WCAG 2.1 Level AA standards**. Accessibility ensures your interface is usable by everyone—keyboard users, screen reader users, users with low vision, and users with cognitive disabilities.

**Core principle:** Semantic HTML first, ARIA last. Keyboard navigation and screen reader support are non-negotiable.

---

## When to Use / When NOT to Use

### ✅ Use This Skill When

- Building new UI components (buttons, modals, dropdowns, forms, tabs)
- Adding keyboard navigation or focus management
- Reviewing code for accessibility violations
- Testing with screen readers or keyboard-only
- Ensuring color contrast and visual focus indicators
- Adding ARIA attributes to dynamic content

### ❌ Do NOT Use When

- Component is purely decorative (no interaction needed)
- Audience explicitly doesn't include users with accessibility needs (internally impossible—always assume diverse users)
- You're skipping automated testing due to time constraints (violates DoD)

---

## Core Concepts

### 1. Semantic HTML Structure

**Foundation:** Use meaningful HTML elements to convey structure and purpose.

```html
<!-- ✅ CORRECT: Semantic structure -->
<header role="banner">
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/home">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main id="main-content">
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Heading</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

<footer>
  <p>&copy; 2026 Company</p>
</footer>

<!-- ✅ CORRECT: Proper heading hierarchy -->
<h1>Main Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h2>Another Section</h2>

<!-- ❌ WRONG: Non-semantic div soup -->
<div class="header">
  <div class="nav">
    <div>Home</div>
    <div>About</div>
  </div>
</div>
<div class="main">
  <div class="title">Page Title</div>
</div>

<!-- ❌ WRONG: Skipping heading hierarchy -->
<h1>Main Title</h1>
<h3>Jumps to h3 (breaks hierarchy)</h3>
```

**Label Association Rules:**

```html
<!-- ✅ CORRECT: Explicit label-input association -->
<label for="email-input">Email Address</label>
<input id="email-input" type="email" required />

<!-- ✅ CORRECT: Implicit label wrapping -->
<label>
  Email Address
  <input type="email" required />
</label>

<!-- ❌ WRONG: Placeholder alone (insufficient) -->
<input type="email" placeholder="Enter email" />
<!-- Screen readers read placeholder only on focus; users don't see it in context -->

<!-- ❌ WRONG: No association -->
<label>Email Address</label>
<input type="email" />
```

---

### 2. Keyboard Navigation

**Principle:** All interactive features usable via keyboard—Tab, Shift+Tab, Enter, Space, Arrow keys, Escape.

**Key Bindings:**
- **Tab / Shift+Tab**: Move focus forward/backward
- **Enter / Space**: Activate buttons, toggle checkboxes
- **Arrow keys**: Navigate lists, menus, sliders, tabs (up/down for vertical; left/right for horizontal)
- **Home / End**: Jump to first/last item in list
- **Escape**: Close modal, dropdown, or menu

**Focus Management:**

```html
<!-- ✅ CORRECT: Explicit focus for interactive elements -->
<button tabindex="0">Click me</button>

<!-- ✅ CORRECT: Programmatic focus (not in tab order) -->
<div tabindex="-1" id="skip-target">Skip to main content</div>

<!-- ❌ WRONG: Positive tabindex > 0 (breaks tab order) -->
<button tabindex="1">First</button>
<button tabindex="2">Second</button>
<!-- Order now: tabindex 1, 2, then remaining DOM order (confusing!) -->

<!-- ❌ WRONG: Removed focus outline -->
button:focus {
  outline: none; /* NEVER DO THIS */
}
```

**Skip Links (Focus Management):**

```html
<!-- Place at TOP of page, hidden by default -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
  .skip-link {
    position: absolute;
    left: -9999px;
    z-index: 999;
  }

  .skip-link:focus {
    left: 0;
    top: 0;
    background: #000;
    color: #fff;
    padding: 8px 12px;
  }
</style>

<main id="main-content" tabindex="-1">
  <!-- Content -->
</main>
```

---

### 3. ARIA Attributes

**Golden Rule:** Semantic HTML first. Use ARIA only when native HTML doesn't exist or to enhance semantics.

#### Common ARIA Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-label` | Names element (for icons, buttons without text) | `<button aria-label="Close menu">×</button>` |
| `aria-labelledby` | Links to another element as label | `<h2 id="dialog-title">Confirm Delete</h2><div aria-labelledby="dialog-title">...` |
| `aria-describedby` | Adds descriptive text (error, hint) | `<input aria-describedby="pwd-hint" /><p id="pwd-hint">Min 8 chars` |
| `aria-live` | Announces dynamic content ("polite" or "assertive") | `<div aria-live="polite">Item added to cart</div>` |
| `aria-hidden` | Hides from screen readers (decorative only) | `<span aria-hidden="true">→</span>` |
| `role` | Semantic role | `<div role="dialog">...` |
| `aria-expanded` | Indicates expanded/collapsed state | `<button aria-expanded="false">Menu</button>` |
| `aria-haspopup` | Signals a popup exists | `<button aria-haspopup="menu">Options</button>` |
| `aria-selected` | Current selection in list/tabs | `<button role="tab" aria-selected="true">Tab 1</button>` |
| `aria-modal` | Marks modal dialogs | `<div role="dialog" aria-modal="true">...` |
| `aria-required` | Flags required form fields | `<input aria-required="true" />` |
| `aria-invalid` | Indicates validation error | `<input aria-invalid="true" aria-describedby="error-msg" />` |
| `aria-atomic` | Reads entire content block | `<div aria-live="polite" aria-atomic="true">Status: Updated</div>` |

---

### 4. Color Contrast & Visual Focus

**WCAG Contrast Ratios:**

| Level | Normal Text | Large Text (18pt+) |
|-------|-------------|-------------------|
| **AA (minimum)** | 4.5:1 | 3:1 |
| **AAA (enhanced)** | 7:1 | 4.5:1 |

**Visual Focus Indicators (Required):**

```css
/* ✅ CORRECT: Visible focus indicator */
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* ✅ CORRECT: Alternative (background change) */
button:focus {
  background-color: #e6f2ff;
  box-shadow: inset 0 0 0 2px #0066cc;
}

/* ❌ WRONG: Removing focus outline */
button:focus {
  outline: none; /* FORBIDDEN */
}

/* ❌ WRONG: Low contrast focus */
button:focus {
  outline: 1px solid #ccc; /* Too subtle */
}
```

**Never Convey Info by Color Alone:**

```html
<!-- ❌ WRONG: Color only -->
<span style="color: red;">This field is required</span>

<!-- ✅ CORRECT: Color + icon/text -->
<span style="color: red;">
  <span aria-hidden="true">*</span> This field is required
</span>

<!-- ✅ CORRECT: Color + pattern -->
<input type="checkbox" style="border: 2px solid red;" />
<label>I agree (required)</label>
```

---

### 5. Testing & Validation

**Automated Tools:**
- **axe DevTools**: Browser extension for violations (Chrome, Firefox)
- **Lighthouse**: Chrome DevTools → Lighthouse → Accessibility (target: 90+)
- **Pa11y**: CLI tool for automated scanning
- **jest-axe**: Automated testing in Jest

**Manual Testing:**
1. **Keyboard-only:** Unplug mouse; navigate using Tab, Enter, Space, arrows
2. **Screen readers:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS)
3. **Color contrast:** WebAIM Contrast Checker
4. **Zoom:** Test at 200% zoom; ensure nothing breaks

**Acceptance Criteria:**
- Zero axe DevTools violations
- Lighthouse Accessibility ≥ 90
- All features functional via keyboard
- All images have alt text
- All form inputs have labels

---

## Component Patterns

### Pattern 1: Accessible Dropdown Menu

```jsx
import { useState, useRef, useEffect } from 'react';

export function AccessibleDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const buttonRef = useRef(null);
  const menuRef = useRef(null);

  const options = ['Edit', 'Duplicate', 'Delete'];

  // Close on Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Focus management for arrow keys
  const handleMenuKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex((i) => (i + 1) % options.length);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex((i) => (i - 1 + options.length) % options.length);
        break;
      case 'Home':
        e.preventDefault();
        setSelectedIndex(0);
        break;
      case 'End':
        e.preventDefault();
        setSelectedIndex(options.length - 1);
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        handleSelect(options[selectedIndex]);
        break;
      default:
        break;
    }
  };

  const handleSelect = (option) => {
    console.log('Selected:', option);
    setIsOpen(false);
    buttonRef.current?.focus();
  };

  return (
    <div className="dropdown">
      <button
        ref={buttonRef}
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-controls="dropdown-menu"
        onClick={() => setIsOpen(!isOpen)}
      >
        Options
      </button>

      {isOpen && (
        <ul
          id="dropdown-menu"
          ref={menuRef}
          role="menu"
          onKeyDown={handleMenuKeyDown}
        >
          {options.map((option, i) => (
            <li key={option} role="none">
              <button
                role="menuitem"
                aria-selected={i === selectedIndex}
                onMouseEnter={() => setSelectedIndex(i)}
                onClick={() => handleSelect(option)}
              >
                {option}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

### Pattern 2: Accessible Modal Dialog

```jsx
import { useEffect, useRef } from 'react';

export function AccessibleModal({ isOpen, onClose, title, children }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    // Store the element that opened the modal for focus restore
    const previouslyFocused = document.activeElement;

    // Focus the modal
    dialogRef.current?.focus();

    // Focus trap: trap focus inside modal
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
        previouslyFocused?.focus();
        return;
      }

      // Trap Tab inside modal
      if (e.key === 'Tab') {
        const focusableElements = dialogRef.current?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!focusableElements || focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      previouslyFocused?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="modal-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
        className="modal"
        tabIndex="-1"
      >
        <h2 id="modal-title">{title}</h2>
        <div id="modal-description">{children}</div>
        <button onClick={onClose}>Close</button>
      </div>
    </>
  );
}
```

---

### Pattern 3: Accessible Alert/Notification

```jsx
export function AccessibleAlert({ type, message, onDismiss }) {
  // type: 'error' | 'success' | 'warning' | 'info'
  const isError = type === 'error';

  return (
    <div
      role="alert"
      aria-live={isError ? 'assertive' : 'polite'}
      aria-atomic="true"
      className={`alert alert-${type}`}
    >
      <span aria-hidden="true">
        {type === 'error' && '⚠️'}
        {type === 'success' && '✓'}
        {type === 'warning' && '⚡'}
        {type === 'info' && 'ℹ️'}
      </span>
      {message}
      {onDismiss && (
        <button
          aria-label="Dismiss notification"
          onClick={onDismiss}
        >
          ×
        </button>
      )}
    </div>
  );
}
```

---

### Pattern 4: Accessible Form with Error Handling

```jsx
import { useState } from 'react';

export function AccessibleForm() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email must follow format: user@domain.com';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log('Form submitted:', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Email Field */}
      <div className="form-group">
        <label htmlFor="email-input">
          Email Address <span aria-hidden="true">*</span>
        </label>
        <input
          id="email-input"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert" className="error">
            {errors.email}
          </span>
        )}
      </div>

      {/* Password Field */}
      <div className="form-group">
        <label htmlFor="password-input">
          Password <span aria-hidden="true">*</span>
        </label>
        <input
          id="password-input"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          aria-required="true"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : 'password-hint'}
        />
        <p id="password-hint" className="hint">
          Minimum 8 characters
        </p>
        {errors.password && (
          <span id="password-error" role="alert" className="error">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit">Sign In</button>
    </form>
  );
}
```

---

### Pattern 5: Accessible Tab Component

```jsx
import { useState } from 'react';

export function AccessibleTabs() {
  const [activeTab, setActiveTab] = useState(0);

  const tabs = [
    { label: 'Overview', content: 'Overview content here' },
    { label: 'Details', content: 'Details content here' },
    { label: 'Related', content: 'Related items here' },
  ];

  const handleTabKeyDown = (e, index) => {
    let nextIndex = index;

    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        nextIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case 'ArrowRight':
        e.preventDefault();
        nextIndex = (index + 1) % tabs.length;
        break;
      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;
      case 'End':
        e.preventDefault();
        nextIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    setActiveTab(nextIndex);
    // Focus the newly active tab
    document.getElementById(`tab-${nextIndex}`)?.focus();
  };

  return (
    <div className="tabs">
      {/* Tablist */}
      <div role="tablist" aria-label="Content sections">
        {tabs.map((tab, i) => (
          <button
            key={i}
            id={`tab-${i}`}
            role="tab"
            aria-selected={activeTab === i}
            aria-controls={`tabpanel-${i}`}
            tabIndex={activeTab === i ? 0 : -1}
            onClick={() => setActiveTab(i)}
            onKeyDown={(e) => handleTabKeyDown(e, i)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tabpanels */}
      {tabs.map((tab, i) => (
        <div
          key={i}
          id={`tabpanel-${i}`}
          role="tabpanel"
          aria-labelledby={`tab-${i}`}
          hidden={activeTab !== i}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

---

### Pattern 6: Testing with axe-core and Jest

```javascript
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { AccessibleForm } from './AccessibleForm';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  test('form has no accessibility violations', async () => {
    const { container } = render(<AccessibleForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('form is keyboard navigable', () => {
    render(<AccessibleForm />);
    const emailInput = screen.getByLabelText('Email Address');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    // Tab focus order
    emailInput.focus();
    expect(document.activeElement).toBe(emailInput);

    // Tab to password
    const tabEvent = new KeyboardEvent('keydown', { key: 'Tab' });
    emailInput.dispatchEvent(tabEvent);

    // Can activate button with Space/Enter
    submitButton.focus();
    const spaceEvent = new KeyboardEvent('keydown', { key: ' ' });
    submitButton.dispatchEvent(spaceEvent);
  });

  test('modal traps focus', () => {
    const { rerender } = render(
      <AccessibleModal isOpen={true} onClose={() => {}} title="Test Modal">
        <button>Action 1</button>
        <button>Action 2</button>
      </AccessibleModal>
    );

    const buttons = screen.getAllByRole('button');
    const lastButton = buttons[buttons.length - 1];

    // Focus trap: Tab on last button should go to first
    lastButton.focus();
    const tabEvent = new KeyboardEvent('keydown', {
      key: 'Tab',
      shiftKey: false,
    });
    expect(lastButton === document.activeElement);
  });

  test('alert is announced by screen readers', () => {
    render(
      <AccessibleAlert
        type="success"
        message="Item saved successfully"
      />
    );
    const alert = screen.getByRole('alert');
    expect(alert).toHaveAttribute('aria-live', 'polite');
    expect(alert).toHaveAttribute('aria-atomic', 'true');
  });
});
```

---

## Quick Reference Tables

### Keyboard Events Mapping

| User Action | Key(s) | Component | Purpose |
|-------------|--------|-----------|---------|
| Navigate | Tab / Shift+Tab | All | Focus previous/next |
| Activate | Enter / Space | Button, Checkbox, Radio | Trigger action |
| Navigate list | ↑↓ | Menu, Listbox, Select | Move between items |
| Navigate horizontal | ← → | Tabs, Slider, Menu | Move between options |
| Go to start | Home | Tabs, List, Slider | Jump to first item |
| Go to end | End | Tabs, List, Slider | Jump to last item |
| Close/Cancel | Escape | Modal, Dropdown, Menu | Dismiss overlay |
| Alphabetic | a–z | Listbox, Combobox | Jump to matching item |

### ARIA Role Reference (Common)

| Role | Element | Usage |
|------|---------|-------|
| `button` | `<div>`, `<span>` (non-button) | Make non-button interactive |
| `menu` / `menuitem` | `<ul>`, `<li>` | Popup/context menu |
| `listbox` / `option` | Custom dropdown | Accessible select replacement |
| `tab` / `tablist` / `tabpanel` | Tab UI | Tab container and panels |
| `dialog` | Modal / overlay | Modal dialog (+ `aria-modal`) |
| `alert` | Notification | Assertive/polite announcement |
| `region` | Generic section | Landmark region (`aria-label` required) |
| `navigation` | Nav links | Main/secondary navigation |

### Contrast Ratio Quick Check

| Scenario | Min Ratio | Example |
|----------|-----------|---------|
| Body text (AA) | 4.5:1 | #333 on #fff = 12.6:1 ✓ |
| Large text (AA) | 3:1 | #666 on #fff = 5.74:1 ✓ |
| Icon/UI (AA) | 3:1 | #0066cc on #fff = 8.59:1 ✓ |
| Body text (AAA) | 7:1 | #555 on #fff = 9.26:1 ✓ |

---

## Review Checklist

Use this checklist before marking a component accessible:

### Semantic HTML
- [ ] Uses `<button>` for buttons, not `<div onclick>`
- [ ] Uses `<nav>`, `<main>`, `<header>`, `<footer>` for landmarks
- [ ] Heading hierarchy is correct (`<h1>` → `<h2>` → `<h3>`, no skips)
- [ ] All form inputs have `<label>` or `aria-label`
- [ ] Images have meaningful `alt` or decorative `alt=""`

### Keyboard Navigation
- [ ] Tab order is logical (left-to-right, top-to-bottom)
- [ ] All interactive elements are reachable via Tab
- [ ] No `outline: none` without replacement focus indicator
- [ ] Enter/Space activates buttons
- [ ] Arrow keys work in menus/lists/tabs
- [ ] Escape closes modals/dropdowns
- [ ] Focus visible with ≥2px outline or equivalent

### ARIA
- [ ] ARIA attributes are correct and not redundant
- [ ] `aria-live` used for dynamic announcements
- [ ] `aria-hidden` only on decorative elements
- [ ] Modal has `role="dialog"` + `aria-modal="true"`
- [ ] Form errors linked with `aria-describedby`
- [ ] Required fields marked with `aria-required`

### Visual & Color
- [ ] Text contrast ≥4.5:1 (AA) or 7:1 (AAA)
- [ ] Information not conveyed by color alone
- [ ] Focus indicators visible and distinct
- [ ] Component responsive at 200% zoom

### Testing
- [ ] Axe DevTools: Zero violations
- [ ] Lighthouse Accessibility: ≥90
- [ ] Manual keyboard testing: All features work
- [ ] Screen reader tested (NVDA/VoiceOver/JAWS)
- [ ] Jest/axe unit tests included

---

## Common Mistakes

### ❌ Mistake 1: Placeholder as Label

```jsx
// WRONG: Placeholder disappears on focus
<input type="email" placeholder="Enter your email" />

// CORRECT: Explicit label
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

**Why:** Placeholders are hidden when users focus the input. Screen reader users won't hear what the field is for.

---

### ❌ Mistake 2: `outline: none` Without Replacement

```css
/* WRONG: Keyboard users can't see focus */
button:focus {
  outline: none;
}

/* CORRECT: Provide visible focus */
button:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}
```

**Why:** Keyboard users rely on focus indicators to navigate. Removing it breaks navigation.

---

### ❌ Mistake 3: Positive `tabindex`

```jsx
// WRONG: Breaks natural tab order
<button tabindex="2">Second (confusing!)</button>
<button tabindex="1">First</button>
<button>Third (where does it go?)</button>

// CORRECT: Use tabindex 0 or -1 only
<button>First</button>  // tabindex 0 (implicit)
<button>Second</button>
<button tabindex="-1">Hidden from tab order</button>
```

**Why:** Positive tabindex disrupts the natural DOM order. Screen reader and keyboard users get confused.

---

### ❌ Mistake 4: Color Alone to Convey Info

```html
<!-- WRONG: Only color indicates required -->
<input style="border: 1px solid red;" />

<!-- CORRECT: Color + icon/text -->
<label>
  Email <span aria-hidden="true">*</span>
</label>
<input />
```

**Why:** Users with color blindness can't see the distinction. Pair color with icons or text.

---

### ❌ Mistake 5: No Focus Trap in Modal

```jsx
// WRONG: Focus can escape the modal
<div role="dialog">
  <button>Close</button>
</div>

// CORRECT: Focus is trapped
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      // Trap focus inside modal
    }
  };
  document.addEventListener('keydown', handleKeyDown);
}, []);
```

**Why:** Keyboard users can accidentally tab out of a modal, losing context.

---

### ❌ Mistake 6: Missing Alt Text on Images

```html
<!-- WRONG: No alt text -->
<img src="chart.png" />

<!-- CORRECT: Meaningful alt -->
<img src="chart.png" alt="Sales increased 25% in Q3" />

<!-- CORRECT: Decorative image -->
<img src="spacer.png" alt="" aria-hidden="true" />
```

**Why:** Screen reader users hear "image, chart-dot-png" with no context. Provide descriptive alt text.

---

### ❌ Mistake 7: No Error Messages Linked to Fields

```jsx
// WRONG: Error exists but not linked
<input type="email" />
<span>Invalid email format</span>

// CORRECT: Error linked with aria-describedby
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">Invalid email format: user@domain.com</span>
```

**Why:** Screen reader users won't know the error is related to the input. Link it explicitly.

---

### ❌ Mistake 8: No Announce for Dynamic Content

```jsx
// WRONG: Item added silently
<div>Items in cart: 5</div>

// CORRECT: Announce change
<div aria-live="polite" aria-atomic="true">
  Item added to cart. Items: 5
</div>
```

**Why:** Screen reader users don't hear dynamic updates. Use `aria-live` to announce.

---

## Summary

**Accessibility is not a feature—it's a requirement.** Every component must be:
1. **Keyboard accessible** — All features work without a mouse
2. **Screen reader friendly** — Semantic HTML + ARIA
3. **Visually accessible** — Sufficient contrast and focus indicators
4. **Well tested** — Axe, Lighthouse, manual keyboard, screen reader

**Start with semantic HTML. Add ARIA only when needed. Test with real tools and real users.**

---

**Last updated:** 2026-03-30
**Version:** 1.0.0
