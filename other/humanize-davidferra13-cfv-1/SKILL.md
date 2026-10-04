---
name: humanize
description: Audit and fix developer jargon in all user-facing surfaces. Replaces technical terminology with plain consumer language. Use when user says /humanize, "developer language", "jargon", "consumer friendly", "user-facing copy", "plain English", "sounds too technical", or before any public launch review.
---

# HUMANIZE (Developer Jargon Purge)

## Purpose

Every user-facing string should read like Square, Airbnb, or Squarespace wrote it. Zero technical knowledge assumed. The audience: private chefs, their clients, food service professionals. Not developers.

## Procedure

### Phase 1: Scan

Spawn parallel agents to grep user-facing text across these surface types:

1. **UI text**: page titles, headings, button labels, link text, tab labels, nav items
2. **Forms**: field labels, placeholders, helper text, validation messages
3. **Feedback**: toast messages, error messages, success messages, confirmation dialogs
4. **States**: loading text, empty states, skeleton placeholders, zero-data messages
5. **Accessibility**: aria-labels, alt text, title attributes, sr-only text
6. **Email**: templates, subject lines, preview text, body copy
7. **Onboarding**: setup flows, welcome screens, first-run guidance
8. **Settings**: preference labels, toggle descriptions, section headers
9. **Tooltips**: hover help, info icons, contextual guidance

Search patterns (grep across `app/`, `components/`, `lib/` for string literals):

- Direct string literals in JSX: `>"text"`, `>text<`, `label=`, `placeholder=`
- Toast/notification calls: `toast(`, `toast.error(`, `toast.success(`
- Error messages: `throw new Error(`, `message:`, `description:`
- Loading/empty states: `"Loading`, `"No `, `"None`, `"Empty`
- Aria: `aria-label=`, `aria-describedby`, `title=`

### Phase 2: Flag

Rate each finding by severity:

| Severity              | Meaning                                   | Example                                    |
| --------------------- | ----------------------------------------- | ------------------------------------------ |
| **P0 - Confusing**    | User has no idea what this means          | "Revalidation failed", "Invalid entity"    |
| **P1 - Intimidating** | User understands but feels like wrong app | "Sync pipeline", "Configuration error"     |
| **P2 - Rough**        | Understandable but unprofessional         | "No records found", "Toggle notifications" |
| **P3 - Stiff**        | Technically correct but cold/robotic      | "Operation successful", "Item deleted"     |

### Phase 3: Fix

Apply replacements using the [DICTIONARY.md](DICTIONARY.md) reference. For terms not in dictionary, follow these principles:

**Voice rules:**

- Talk like a helpful person, not a system
- "We" or implied subject, never "the system" or "the server"
- Action-oriented: say what to DO, not what went wrong technically
- Warm but not cutesy. Professional but not corporate
- Specific > vague: "Your menu was saved" > "Operation complete"

**Error message formula:**

1. What happened (in human terms)
2. What they can do about it
3. Never: error codes, stack traces, technical reasons

**Empty state formula:**

1. What would be here
2. How to get started
3. Never: "No records", "Empty", "null", "0 results"

### Phase 4: Report

Output a summary table:

```
## Humanize Report - [date]

| File | Line | Old Text | New Text | Severity |
|------|------|----------|----------|----------|
| ... | ... | ... | ... | P0 |

### Stats
- P0 (Confusing): N findings, N fixed
- P1 (Intimidating): N findings, N fixed
- P2 (Rough): N findings, N fixed
- P3 (Stiff): N findings, N fixed
```

Save report to `docs/audits/humanize-report-[date].md`.

### Phase 5: Verify

After fixes, spot-check 5 highest-severity pages in browser via Playwright. Screenshot before/after if possible.

## Rules

1. **Never touch code logic.** Only change string literals and display text.
2. **Preserve i18n keys** if internationalization exists. Change the value, not the key.
3. **Keep technical terms in code comments, logs, and developer docs.** Only user-facing text changes.
4. **Database column names, API field names, internal variable names stay as-is.**
5. **Respect existing brand terms** defined in CONTEXT.md or the glossary.
6. **When unsure, ask:** "Would a chef's client understand this on their phone at 9pm?"
