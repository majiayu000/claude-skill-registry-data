---
name: add-notification
description: Add a notification users receive by email, in-app, push or SMS, or a new notification category in their preferences. Use when the user wants to notify, remind, alert or email someone about something.
---

# Add a notification

A notification is a template in apps/notifications, queued as a job. Its category
decides which channels it may use and whether users can turn it off.

1. **Payload.** Add a `z.object({ template: z.literal("<area>.<name>"), to, data })` to
   `notificationPayload` in `packages/jobs/src/queues.ts` and pick its queue in
   `notificationQueue` (`notifications-critical` only for codes, security and billing).
   `to` is `{ userId }`, `{ email, locale }` or `{ orgId, roles }`.
2. **Copy.** Every string in `packages/i18n/messages/*.json`, every locale:
   `email.<camelCaseName>`, `notification.<area>.<name>.title` and `.body` (push and
   in-app), `sms.<camelCaseName>`. Compare `todo.reminder`: `email.todoReminder`,
   `notification.todo.reminder`.
3. **Email.** A component in `packages/email/src/templates/` with its subject, exported
   from `packages/email/src/index.ts`, and a preview in `packages/email/src/previews/`
   (`bun run --cwd packages/email dev` serves them on http://localhost:3030).
4. **In-app.** Its data schema in `inAppNotifications` in
   `packages/contracts/src/notifications.ts`, so apps can render it.
5. **Template.** An entry in `templates` in `apps/notifications/src/dispatch/templates.ts`
   with its `category` and a renderer per channel it uses (`email`, `inApp`, `push`,
   `sms`). The `satisfies` clause fails `check-types` until it exists.
6. **Category.** Reuse one from `notificationCategories` in
   `packages/contracts/src/notifications.ts`. A new one gets its default channels there
   and a `title` and `description` under `notificationSettings.categories.<name>`.
   `mutable: false` means users can't turn it off.
7. **Trigger.** From a service: a producer for the queue and `add("send", payload, { jobId })`.
   From a domain event: route the event to `events-notifications` in `eventSubscribers`
   and map it in `apps/notifications/src/events/events.processor.ts`.
8. **Tests.** `bun run test` (i18n completeness, email rendering in
   `packages/email/src/render.test.tsx`), then `bun run test:integration`
   (`apps/notifications/test/notifications.integration.test.ts` sends through Mailpit and
   the fake push and SMS servers).
9. **Finish.** The verify skill, then the `i18n-checker` agent on the new copy and the
   `reviewer` agent on the change (delivery through `DeliveryLog.claim()`, preferences,
   the category's `mutable` flag).
