---
name: form-filler
description: Fill web forms from user-approved data while requiring confirmation before submission.
category: web
aliases:
- form
- autofill
- webform
- submit
triggers:
- Fill out this form
- Submit this application
- Auto-fill the form
- Complete this registration
keywords:
- form
- fill
- submit
- autofill
- webform
- input
dependencies:
- optional:browser-automation
risk: high
version: 1.0.0
source: custom
enabled: true
capabilities:
- form-filler
- web
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- autofill
- fill
- filler
- form
- submit
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Form Filler

## Purpose
Fill web forms from structured data provided by the user, with explicit confirmation
required before any submission. The skill ensures data accuracy and prevents accidental
or unauthorized form submissions.

## When to Use
- The user provides specific data to fill into a web form
- Registration or application forms need to be completed
- Multi-step forms require sequential field population

## When NOT to Use
- The form contains sensitive personal data the user hasn't explicitly approved
- The form submission has legal or financial implications without user review
- The target site uses bot detection that requires human-like behavior

## Capabilities
- Identify form fields from page structure or provided mapping
- Support text inputs, checkboxes, radio buttons, selects, and textareas
- Handle multi-step forms with navigation
- Preview filled form before submission
- Provide clear confirmation prompts for submission
- Handle captchas and bot detection gracefully

## Inputs
- `url` (required) — target form URL
- `data` (required) — mapping of field names to values
- `field_mapping` (optional) — explicit selector-to-field mapping
- `submit` (optional, default: false) — whether to submit after filling
- `preview` (optional, default: true) — show preview before action

## Workflow
1. **Navigate** — Open the form URL
2. **Analyze** — Identify form fields and types
3. **Map** — Match provided data to form fields
4. **Preview** — Show filled form state to user
5. **Confirm** — Wait for explicit user approval
6. **Submit** — Only if confirmed, submit the form
7. **Report** — Present submission result or error

## Tools
- Browser automation (agent-browser, playwright, puppeteer)

## Examples
**User:** "Fill out this contact form with: name=John, email=john@example.com"
**Response:**
```
Form fields detected:
- Name: John âœ“
- Email: john@example.com âœ“
- Message: [empty]

Preview ready. Say "submit" to send, or provide message text.
```

## Safety
- ALWAYS require explicit confirmation before submission
- Never auto-submit forms
- Preview all data before filling
- Never store submitted form responses without consent
- Warn about potential consequences (legal, financial)

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical web category.
