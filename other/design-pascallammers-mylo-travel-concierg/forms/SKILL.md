---
name: forms
description: HTML-first form patterns with CSS-only validation. Use when building accessible forms with the form-field custom element, output element for messages, and native HTML5 validation.
allowed-tools: Read, Write, Edit
---

# Forms Skill

This skill provides patterns for building accessible, semantic forms using HTML-first techniques with CSS-only validation feedback.

## Philosophy

Forms should work **without JavaScript**. HTML5 provides robust validation, and CSS pseudo-classes (`:user-valid`, `:user-invalid`) enable visual feedback. The `<output>` element provides semantic validation messaging with built-in accessibility support.

---

## The `<form-field>` Pattern

The `<form-field>` custom element groups each form control with its label and validation message:

```html
<form-field>
  <label for="email">Email</label>
  <input type="email"
         id="email"
         name="email"
         required
         aria-describedby="email-message"/>
  <output id="email-message"
          for="email"
          aria-live="polite">
    Please enter a valid email address
  </output>
</form-field>
```

### Element Structure

```
form-field
├── label          (required, with for attribute)
├── input/textarea/select (required, with id matching label)
└── output         (optional, for validation/help messages)
```

### Component Responsibilities

| Element | Purpose | Key Attributes |
|---------|---------|----------------|
| `<form-field>` | Groups field components | `data-valid`, `data-invalid` for state styling |
| `<label>` | Accessible field label | `for` (matches input `id`) |
| `<input>` | Form control | `id`, `name`, validation attrs, `aria-describedby` |
| `<output>` | Validation/help message | `id`, `for`, `aria-live="polite"` |

---

## Why `<output>` for Validation Messages

The `<output>` element is semantically ideal for validation messages:

1. **Purpose-built**: Represents the result of a calculation or user action (validation result)
2. **Native association**: Has `for` attribute to link to input(s) being validated
3. **Accessible**: Works naturally with `aria-live` for screen reader announcements
4. **Semantic distinction**: Clearly different from static help text or error divs
5. **No JavaScript required**: Can show different states via CSS

### Comparison with Alternatives

| Approach | Semantics | Accessibility | Flexibility |
|----------|-----------|---------------|-------------|
| `<output>` | Result of action | Native support | Excellent |
| `<span class="error">` | None | Manual ARIA needed | Poor |
| `<div class="message">` | None | Manual ARIA needed | Poor |
| `aria-errormessage` | Error only | Good | Errors only |

---

## HTML5 Validation Attributes

Use native validation attributes for client-side validation:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `required` | Field must have value | `<input required/>` |
| `minlength` | Minimum character count | `<input minlength="2"/>` |
| `maxlength` | Maximum character count | `<input maxlength="100"/>` |
| `pattern` | Regex pattern | `<input pattern="[A-Za-z]+"/>` |
| `type` | Input type validation | `type="email"`, `type="url"` |
| `min`/`max` | Number/date range | `<input type="number" min="0" max="100"/>` |

---

## CSS-Only Validation Styling

### The `:user-valid` and `:user-invalid` Pseudo-classes

These pseudo-classes only apply **after user interaction**, preventing premature error states:

```css
/* Valid state after user interacts */
form-field:has(input:user-valid) {
  & input {
    border-color: var(--success-color);
  }
  & output {
    color: var(--success-color);
  }
}

/* Invalid state after user interacts */
form-field:has(input:user-invalid) {
  & input {
    border-color: var(--error-color);
  }
  & output {
    color: var(--error-color);
  }
}
```

### Required Field Indicators

Auto-generate asterisks for required fields:

```css
form-field:has(input:required, textarea:required, select:required) {
  & label::after {
    content: " *";
    color: var(--error-color);
  }
}
```

### Focus Styling

```css
form-field {
  & input:focus,
  & textarea:focus,
  & select:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }
}
```

---

## Form Field Variants

### Text Input

```html
<form-field>
  <label for="name">Full Name</label>
  <input type="text"
         id="name"
         name="name"
         required
         minlength="2"
         autocomplete="name"
         aria-describedby="name-msg"/>
  <output id="name-msg" for="name" aria-live="polite">
    At least 2 characters required
  </output>
</form-field>
```

### Email Input

```html
<form-field>
  <label for="email">Email Address</label>
  <input type="email"
         id="email"
         name="email"
         required
         autocomplete="email"
         aria-describedby="email-msg"/>
  <output id="email-msg" for="email" aria-live="polite">
    Please enter a valid email address
  </output>
</form-field>
```

### Textarea

```html
<form-field>
  <label for="message">Message</label>
  <textarea id="message"
            name="message"
            required
            minlength="10"
            rows="5"
            aria-describedby="message-msg"></textarea>
  <output id="message-msg" for="message" aria-live="polite">
    At least 10 characters required
  </output>
</form-field>
```

### Select Dropdown

```html
<form-field>
  <label for="category">Category</label>
  <select id="category" name="category" required>
    <option value="" disabled selected>Select a category...</option>
    <option value="general">General Inquiry</option>
    <option value="support">Technical Support</option>
    <option value="sales">Sales Question</option>
  </select>
</form-field>
```

### Phone Number

```html
<form-field>
  <label for="phone">Phone Number</label>
  <input type="tel"
         id="phone"
         name="phone"
         autocomplete="tel"
         pattern="[0-9\-\+\s\(\)]+"
         aria-describedby="phone-msg"/>
  <output id="phone-msg" for="phone" aria-live="polite">
    Optional - include country code for international
  </output>
</form-field>
```

### Password with Confirmation

```html
<form-field>
  <label for="password">Password</label>
  <input type="password"
         id="password"
         name="password"
         required
         minlength="8"
         autocomplete="new-password"
         aria-describedby="password-msg"/>
  <output id="password-msg" for="password" aria-live="polite">
    At least 8 characters required
  </output>
</form-field>

<form-field>
  <label for="password-confirm">Confirm Password</label>
  <input type="password"
         id="password-confirm"
         name="password_confirm"
         required
         autocomplete="new-password"/>
</form-field>
```

---

## Complete Contact Form Example

```html
<form action="/api/contact" method="POST">
  <form-field>
    <label for="name">Name</label>
    <input type="text"
           id="name"
           name="name"
           required
           minlength="2"
           autofocus
           autocomplete="name"
           aria-describedby="name-msg"/>
    <output id="name-msg" for="name" aria-live="polite">
      Please enter your name (at least 2 characters)
    </output>
  </form-field>

  <form-field>
    <label for="email">Email</label>
    <input type="email"
           id="email"
           name="email"
           required
           autocomplete="email"
           aria-describedby="email-msg"/>
    <output id="email-msg" for="email" aria-live="polite">
      Please enter a valid email address
    </output>
  </form-field>

  <form-field>
    <label for="subject">Subject</label>
    <select id="subject" name="subject" required>
      <option value="" disabled selected>Select a subject...</option>
      <option value="general">General Inquiry</option>
      <option value="support">Technical Support</option>
      <option value="feedback">Feedback</option>
    </select>
  </form-field>

  <form-field>
    <label for="message">Message</label>
    <textarea id="message"
              name="message"
              required
              minlength="10"
              rows="5"
              aria-describedby="message-msg"></textarea>
    <output id="message-msg" for="message" aria-live="polite">
      Please enter your message (at least 10 characters)
    </output>
  </form-field>

  <button type="submit">Send Message</button>
</form>
```

---

## Accessibility Checklist

When building forms, ensure:

- [ ] Every `<input>` has a `<label>` with matching `for`/`id`
- [ ] Required fields use the `required` attribute
- [ ] Validation messages use `<output>` with `aria-live="polite"`
- [ ] Inputs link to messages via `aria-describedby`
- [ ] Form controls have appropriate `autocomplete` values
- [ ] Focus states are clearly visible
- [ ] Error states don't rely on color alone (include text)
- [ ] First input has `autofocus` for immediate interaction

---

## Data Attributes for State

Use data attributes (not classes) for form-field state:

```html
<!-- Valid state -->
<form-field data-valid>...</form-field>

<!-- Invalid state -->
<form-field data-invalid>...</form-field>

<!-- Required indicator -->
<form-field data-required>...</form-field>
```

```css
form-field[data-valid] input { border-color: var(--success-color); }
form-field[data-invalid] input { border-color: var(--error-color); }
```

---

## CSS Variables for Forms

Define form-specific design tokens:

```css
:root {
  /* Form colors */
  --form-border-color: #d1d5db;
  --form-focus-color: var(--primary-color);
  --form-valid-color: #059669;
  --form-invalid-color: #dc2626;

  /* Form sizing */
  --form-input-padding: 0.75rem;
  --form-input-radius: 0.375rem;
  --form-gap: 1.5rem;

  /* Form typography */
  --form-label-weight: 600;
  --form-message-size: 0.875rem;
}
```

---

## Form Layout with CSS Grid

```css
form {
  display: grid;
  gap: var(--form-gap);
  max-width: 32rem;
}

form-field {
  display: grid;
  gap: 0.5rem;

  & label {
    font-weight: var(--form-label-weight);
  }

  & input,
  & textarea,
  & select {
    padding: var(--form-input-padding);
    border: 1px solid var(--form-border-color);
    border-radius: var(--form-input-radius);
  }

  & output {
    font-size: var(--form-message-size);
    color: var(--text-muted);
  }
}
```

---

## Custom Element Definition

The `<form-field>` element is defined in `elements.json`:

```json
{
  "form-field": {
    "flow": true,
    "permittedContent": ["label", "input", "textarea", "select", "output", "@phrasing"],
    "attributes": {
      "data-required": { "required": false, "boolean": true },
      "data-valid": { "required": false, "boolean": true },
      "data-invalid": { "required": false, "boolean": true }
    }
  }
}
```

## Server-Side Validation

**Client-side validation is for UX only.** Always validate on the server.

Use the same validation rules server-side with JSON Schema. See **validation** skill for:

- JSON Schema definitions matching HTML5 constraints
- AJV validation middleware for Express/Fastify
- Consistent error response format with field-level details

```javascript
// Server validates using same rules as HTML5 attributes
// HTML: required, minlength="2", maxlength="100"
// Schema: "required": ["name"], "minLength": 2, "maxLength": 100
app.post('/api/contact',
  validateBody('api/contact-form'),
  handleContact
);
```

---

## Related Skills

- **validation** - Server-side JSON Schema validation with AJV middleware
- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **accessibility-checker** - Ensure WCAG2AA accessibility compliance
- **security** - Write secure web pages and applications
- **progressive-enhancement** - HTML-first development with CSS-only interactivity patterns
