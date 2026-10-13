---
name: swap-email-provider
description: Send email through something other than the self-hosted Stalwart server (another SMTP server, or an HTTP API such as SES or Postmark). Use when the user decides to move to a different mail path. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the email provider

- **Interface:** `EmailTransport` (`send(email): Promise<{ providerMessageId }>`) in
  `apps/notifications/src/channels/email/email-transport.ts`.
- **Today:** `SmtpTransport`, the only transport: Mailpit locally, the Stalwart mail
  server in the cluster (and locally with `bun run db:up:mail`).
- **Created in:** `apps/notifications/src/channels/email/email.module.ts`.
- **Env:** `SMTP_URL`, `EMAIL_FROM` (an address of the account `SMTP_URL` signs in as;
  Stalwart refuses other senders). In production `SMTP_URL` must carry credentials and
  use TLS (`smtps://…:465`, or `smtp://…:587?requireTLS=true`); the rules are in
  `smtp-url.ts` next to the transport.

Another SMTP server needs no code: change `SMTP_URL`. The whole stack is self-hosted on
purpose; check with the user before moving mail to a managed service.

## Add an HTTP provider

1. A class implementing `EmailTransport` next to `SmtpTransport`. Send `idempotencyKey`
   as the provider's idempotency key (retried jobs must not double-send), pass
   `headers` through (List-Unsubscribe), set a request timeout, and throw on non-2xx.
2. A setting that chooses it, and its key, in `apps/notifications/src/env.ts`, with a
   boot-time check that the key is present, plus `.env.example` and
   `docs/environment.md`. Choose the transport in `email.module.ts`.
3. Deployed: the key goes in the notifications Secret (rotate-secrets skill).
4. Bounces: the provider's feedback webhook needs its own route in apps/webhooks, like
   `src/inbound/stalwart.routes.ts`, emitting `email.feedback_received.v1` (add the
   provider to that event's `provider` enum in packages/contracts).

The SMS email sink (`apps/notifications/src/channels/sms/email-sink.ts`) always uses SMTP
and is for development only.

## Tests

`apps/notifications/test/notifications.integration.test.ts` reads delivered mail from
Mailpit, and `test/stalwart.integration.test.ts` sends through a real Stalwart. For an
HTTP provider, add a small local fake of its API (like `apps/notifications/test/fake-twilio.ts`)
and a test that sends through it.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
