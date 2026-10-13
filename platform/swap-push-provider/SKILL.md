---
name: swap-push-provider
description: Add or replace a push notification provider (OneSignal, Expo push, a different FCM or APNs setup). Use when the user wants push delivered through another service or on another platform. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap a push provider

- **Interface:** `PushTransport` (`send(token, message): Promise<PushResult>`) in
  `apps/notifications/src/channels/push/push-transport.ts`, one per platform
  (`ios`, `android`, `web`).
- **Today:** `FcmTransport` (`fcm.ts`, Android), `ApnsTransport` (`apns.ts`, iOS),
  `WebPushTransport` (`web-push.ts`, browsers, VAPID).
- **Selected in:** `createTransports()` in `apps/notifications/src/channels/push/push.module.ts`;
  a platform is on when all of its variables are set (`pushPlatforms` in
  `apps/notifications/src/env.ts`).
- **Env:** `FCM_PROJECT_ID`, `FCM_CLIENT_EMAIL`, `FCM_PRIVATE_KEY`; `APNS_KEY_ID`,
  `APNS_TEAM_ID`, `APNS_PRIVATE_KEY`, `APNS_BUNDLE_ID`, `APNS_URL`; `VAPID_PUBLIC_KEY`,
  `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` (the public key also goes to apps/api, which
  hands it to browsers). Test hooks: `FCM_TOKEN_URL`, `FCM_API_URL`, `WEB_PUSH_TEST_ORIGIN`.

## Swap

1. A class implementing `PushTransport`. Return `{ ok: false, gone: true }` for dead
   tokens (uninstalled app, expired subscription) so the device is forgotten, and
   `gone: false` for failures worth retrying.
2. Its variables in `apps/notifications/src/env.ts` (all or none, like the others),
   `.env.example` and `docs/environment.md`.
3. Register it for its platform in `createTransports()`. The channel, dispatcher and
   quiet hours don't change. A provider that uses its own device tokens (Expo push)
   also changes how apps register devices (`apps/mobile`, the `notifications` procedures).

## Tests

`apps/notifications/test/fake-push.ts` fakes FCM, APNs and Web Push; extend it or add a fake
for the new provider, and cover delivery and a dead token in
`apps/notifications/test/notifications.integration.test.ts`.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
