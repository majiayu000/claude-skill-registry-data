---
name: swap-sms-provider
description: Add or switch the SMS provider (Vonage, MessageBird, AWS SNS, …). Use when the user wants texts sent through a different service or in another region. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the SMS provider

- **Interface:** `SmsTransport` (`send(to, body, idempotencyKey): Promise<SmsResult>`) in
  `apps/notifications/src/channels/sms/sms-transport.ts`.
- **Today:** `TwilioTransport` (`twilio.ts`) in production; `EmailSinkSmsTransport`
  (`email-sink.ts`) delivers texts to Mailpit as emails to `<digits>@sms.test` locally.
- **Selected in:** `createTransport()` in `apps/notifications/src/channels/sms/sms.module.ts`
  by `SMS_PROVIDER` (unset in production: nothing is texted).
- **Env:** `SMS_PROVIDER` (`twilio` | `email`), `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`,
  `TWILIO_FROM`, `TWILIO_API_URL` (test hook only).

## Swap

1. A class implementing `SmsTransport`. Map the provider's errors onto `SmsResult`:
   `permanent` when retrying can't help, `suppress: "unsubscribe"` when the recipient
   opted out, `suppress: "invalid"` for numbers that can't receive texts. The dispatcher
   records suppressions (`DeliveryPolicy`) so those numbers are never texted again.
2. Its name in the `SMS_PROVIDER` enum and its credentials in
   `apps/notifications/src/env.ts`, with a boot check that they're all set, plus
   `.env.example` and `docs/environment.md`. A test hook for its API URL is refused in
   production like `TWILIO_API_URL`.
3. A `case` in `createTransport()`.

## Tests

`apps/notifications/test/fake-twilio.ts` is the pattern: a local server answering like
the provider, including its error cases. Write one for the new provider and cover
success, opt-out and invalid numbers in
`apps/notifications/test/notifications.integration.test.ts`.
`apps/notifications/src/channels/sms/email-sink.test.ts` covers the local sink.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
