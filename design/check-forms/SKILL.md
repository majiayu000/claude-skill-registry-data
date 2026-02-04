---
name: check-forms
description: Analyze and validate forms on web pages. Use when users ask to check form accessibility, verify form labels, audit input fields, check form validation, or analyze form UX. Detects missing labels, invalid input types, accessibility issues, and validation problems.
---

# Check Forms

Analyze and validate forms on web pages for accessibility and UX compliance.

## Quick Start

```bash
cd /path/to/html-checker/scripts
bun src/check-forms.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show all form elements |
| `--json` | `-j` | false | Output results as JSON |

## Checks Performed

| Check | Severity | Description |
|-------|----------|-------------|
| Missing label | Error | Input has no associated label |
| Empty label | Error | Label exists but has no text |
| Missing id | Warning | Input has no id for label association |
| Placeholder as label | Warning | Using placeholder instead of label |
| Missing required | Info | Required field without required attribute |
| Invalid input type | Warning | Using text for email/phone/date fields |
| Missing autocomplete | Info | No autocomplete for common fields |
| No submit button | Warning | Form has no submit mechanism |
| Missing form action | Warning | Form has no action attribute |
| Missing method | Info | Form has no method (defaults to GET) |

## Usage Examples

```bash
# Basic check
bun src/check-forms.ts https://example.com

# Verbose output
bun src/check-forms.ts https://example.com --verbose

# JSON output
bun src/check-forms.ts https://example.com --json
```

## Output Example

```
Form Analysis for https://example.com

Summary:
  Total Forms: 2
  Total Inputs: 12
  Issues Found: 6

Form 1: Login Form
  Inputs: 3 (email, password, submit)
  [OK] All inputs have labels
  [WARNING] Password field missing autocomplete="current-password"

Form 2: Contact Form
  Inputs: 9 (name, email, phone, subject, message, checkbox, submit)
  [ERROR] Phone input missing label
  [WARNING] Email using type="text" instead of type="email"
  [WARNING] Phone using type="text" instead of type="tel"
  [INFO] Missing autocomplete on name field

Issues:
  [ERROR  ] Missing label for input at position 5
    <input type="text" name="phone" placeholder="Phone">
  [WARNING] Wrong input type at position 4
    <input type="text" name="email"> should be type="email"

Recommendations:
  - Add <label for="phone">Phone</label> to input
  - Change input type to "email" for email fields
  - Change input type to "tel" for phone fields
  - Add autocomplete attributes for better UX
```

## Accessibility (WCAG)

- **SC 1.3.1**: Labels must be programmatically associated
- **SC 3.3.2**: Labels or instructions required for inputs
- **SC 4.1.2**: Name, role, value must be exposed

## Best Practices

- Every input needs a visible label (not just placeholder)
- Use appropriate input types (email, tel, date, number)
- Add autocomplete for common fields
- Mark required fields with required attribute and visual indicator
