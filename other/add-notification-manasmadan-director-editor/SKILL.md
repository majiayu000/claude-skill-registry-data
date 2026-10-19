---
name: add-notification
description: Add an email users receive (a code, an alert, a notice). Use when the user wants to notify, remind, alert or email someone about something.
---

# Add a notification

A notification is an email template in apps/notifications, queued as a job or asked
for through the outbox.

1. **Payload.** Add a `z.object({ template: z.literal("<area>.<name>"), to, data })` to
   `notificationPayload` in `packages/jobs/src/queues.ts`. `to` is `{ email, locale }`.
2. **Copy.** Every string in `packages/i18n/messages/en.json`, under
   `email.<camelCaseName>` (compare `auth.security-alert`: `email.securityAlert`).
3. **Email.** A component in `packages/email/src/templates/` with its subject, exported
   from `packages/email/src/index.ts`, and a preview in `packages/email/src/previews/`
   (`bun run --cwd packages/email dev` serves them on http://localhost:3030).
4. **Template.** An entry in `templates` in `apps/notifications/src/dispatch/templates.ts`
   that renders it. The `satisfies` clause fails `check-types` until it exists.
5. **Trigger.** From a service: a producer for `notifications-critical` and
   `add("send", payload, { jobId })`. When it must go out with a change, and never
   without it: `requestNotification(tx, …)` (`apps/api/src/notifications.ts`) in the
   change's transaction. From a domain event: route the event to `events-notifications`
   in `eventSubscribers` and map it in `apps/notifications/src/events/events.processor.ts`.
6. **Tests.** `bun run test` (i18n completeness, email rendering in
   `packages/email/src/render.test.tsx`), then `bun run test:integration`
   (`apps/notifications/test/notifications.integration.test.ts` sends through Mailpit).
7. **Finish.** The verify skill, then the `i18n-checker` agent on the new copy and the
   `reviewer` agent on the change (delivery through `DeliveryLog.claim()`, the
   suppression list).
