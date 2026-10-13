---
name: swap-notification-templates
description: Load notification templates from a database or CMS instead of code (editable emails and push copy, per-tenant branding). Use when the user wants non-developers to edit notification content or brand it per workspace. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the notification template source

- **Interface:** `TemplateSource` (abstract class, `bind(payload): Promise<BoundTemplate>`)
  in `apps/notifications/src/dispatch/templates.ts`.
- **Today:** `CodeTemplateSource`: the `templates` registry in the same file, rendering
  React Email components from `packages/email` with copy from `packages/i18n`.
- **Bound in:** `apps/notifications/src/dispatch/notifications.module.ts`
  (`{ provide: TemplateSource, useClass: CodeTemplateSource }`).
- **Env:** none today.

## Swap

1. Store templates (db-change skill; the `notifications` schema is the service's own).
2. Implement `TemplateSource`: look up the stored template for `payload.template`
   (and the organization, for branding), cache it in Redis, and return a `BoundTemplate`
   with the same `category` and only the channels it renders. Fall back to
   `CodeTemplateSource` when no stored version exists, so every template keeps working.
3. Bind the new class in `notifications.module.ts`. The dispatcher, channels and
   preferences don't change.
4. Validate stored content before rendering: the fields it may use are the template's
   payload schema in `packages/jobs/src/queues.ts`. Keep using `context.unsubscribeUrl`
   in emails the recipient can opt out of (the dispatcher supplies it).

## Tests

`apps/notifications/test/notifications.integration.test.ts` sends every channel through
Mailpit and the fake push and SMS servers; add cases for a stored template and for the
fallback. `packages/email/src/render.test.tsx` covers the code templates.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
