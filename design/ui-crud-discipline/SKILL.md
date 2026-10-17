---
name: ui-crud-discipline
description: Apply operational CRUD-specific structure after loading the canonical global UX and UI principles. Use for admin, settings, list, table, record-editor, and notification-management interfaces.
---

# UI CRUD Discipline

Before CRUD work, read the current `ui-ux-principles` skill, especially `Design Principles`, `UX Principles`, `UI Principles`, and `Definition of Done - UI`. Those global rules control shared behavior and presentation. This skill adds only operational CRUD guidance.

When authoring or reviewing FRAC, use the mandatory Given / When / Then templates in `distr/seed-corpus-pack/03-done-states-frac/FRAC-TEMPLATE.md`. The feature is incomplete until every applicable criterion passes.

## People and names

- Display a person's full name as `first_name last_name`. Use email only as secondary information or as a fallback when the full name is missing.
- Put First name before Last name unless the product explicitly targets a locale with a different naming convention.
- Use one Name or Full name column when users identify or select people.

## Operational admin scope

- Expose only records administrators routinely manage. Hide sessions, tokens, reset requests, audit internals, join tables, and other implementation records unless an identified workflow requires access.
- Group non-trivial forms into task-oriented fieldsets. Put identity and primary fields first, operational fields next, advanced or machine-owned data later, and read-only history last.
- Keep table cells read-only and put permitted record actions in one accessible Actions column.
- Do not expose raw JSON, internal IDs, tokens, hashes, or provider responses in the primary editing flow. Put necessary diagnostics in a read-only advanced or history area.
- For irreversible operations, keep the exact record, scope, consequence, permission, progress, and audit outcome visible.

## Email and notifications

- Route application email through one delivery utility and editable templates with stable event keys. Keep plain-text and HTML bodies.
- Seed templates only for real product events.
- Use the same event definition for in-app and email notifications when both channels exist.
- Keep delivery logs read-only, validate template syntax before saving, and redact secure links and secrets.

## Completion

- Verify the canonical Definition of Done - UI and every applicable FRAC criterion.
- Search for last-name-first ordering, email-first identity displays, exposed implementation records, and unscoped diagnostics.
- Inspect the final desktop and mobile views after the last change.
