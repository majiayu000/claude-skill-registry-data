---
name: push-notifications
description: Push notifications in React Native and Expo. Use when notifications do not arrive, for FCM or APNs credentials, DeviceNotRegistered or InvalidCredentials errors, foreground handling, Android channels, scheduled notifications, Expo Go limits.
user-invocable: false
---

# Push notifications that actually arrive

## Pick a lane and stay in it

- **Expo push service** (expo-notifications with ExpoPushToken): easiest server story, one API for both platforms, good default for most apps.
- **Direct FCM / APNs** (device tokens, often with notifee for rich display): full control, more moving parts, needed for some advanced delivery cases.

The classic self-inflicted wound is mixing lanes: registering an Expo push token but sending through FCM directly, or vice versa. A token only works with the service it belongs to. Decide once, document it in the repo, and delete the code paths of the other lane.

**Expo Go is not a push test bed.** Since SDK 53, remote push through expo-notifications does not work in Expo Go on Android at all; a development build is required. Local notifications still work there, which is why the gap gets blamed on credentials instead. Test push in a development build or a release build, never in Expo Go.

## Credentials

**iOS (APNs)**
- Use an APNs key (.p8), not certificates. One key serves all your apps and does not expire annually.
- The key lives in EAS credentials (or your own server if sending directly). Missing or wrong-team keys produce zero delivery with no client-side error, which is why iOS push debugging starts at the credentials screen, not in code.
- Simulators receive real APNs sandbox pushes on Apple Silicon and T2 Macs (macOS 13+, Xcode 14+), with their own simulator-specific token. Hardware is only required for production-APNs behavior and older Intel Macs. `simctl push` additionally covers pure display-logic testing with a local payload.

**Android (FCM)**
- google-services.json must match the applicationId exactly, including build-variant suffixes like `.dev`.
- Sending through Expo requires uploading an FCM V1 service account key to EAS. The legacy FCM server key era is over; `InvalidCredentials` or 403 responses on Android almost always mean the V1 service account step was skipped.

## Client-side checklist

- Ask permission at a sensible moment, not at cold start. Denied-once is expensive to recover from on both platforms.
- Foreground behavior is opt-in: without a foreground handler that says "show it", notifications arriving while the app is open appear to vanish. This is the most reported "bug" that is not a bug.
- Android channels: importance and sound are fixed at channel creation and cannot be changed by shipping new code. Users can change them; you cannot. If you shipped a channel with wrong importance, create a new channel id and migrate.
- Token lifecycle: tokens rotate on reinstall, restore and app data clear. Register the current token on every app start, tied to the signed-in user, and de-duplicate server-side.

## Server-side rules

- Send in batches, not one request per device.
- Delivery is two-phase when using Expo: tickets now, receipts later. Fetch receipts and act on them; a ticket is not proof of delivery.
- `DeviceNotRegistered` means delete that token now. Retrying dead tokens forever bloats your table, slows your sends, and with FCM enough garbage traffic hurts your standing. Same policy for FCM `UNREGISTERED` responses.
- Store per-token metadata: platform, app version, last-seen. When a delivery incident hits, "which tokens are stale" becomes answerable in one query.

## When "notifications don't arrive", in order

1. Which build produced the token? Expo Go on Android cannot receive remote push since SDK 53, so anything observed there is not evidence. Repeat on a development or release build first.
2. Which lane is the token from, and did the send go through that lane's service?
3. Credentials: APNs key present for this app's team and bundle id? FCM V1 service account uploaded and google-services.json matching the applicationId?
4. Is the token current? Reinstall the app, register the fresh token, send to exactly that token.
5. Payload: silent/data-only messages are throttled aggressively by both platforms; visible notifications with title and body are the honest test.
6. Device state: battery savers and doze delay delivery legally. Test with the app freshly backgrounded on a charged, awake device before blaming the pipeline.
7. Read the actual per-token API response (ticket, receipt or FCM error), not your server's aggregate log line. The reason is usually printed there verbatim.

## Scheduled local notifications

- They survive app restarts but not being disabled in system settings; there is no delivery feedback for local notifications, so do not build critical flows on them.
- Timezone traps: schedule with explicit date components in the user's timezone; a "daily at 9:00" job scheduled from a UTC timestamp drifts on DST changes.
- Android exact-alarm restrictions push toward inexact scheduling; design reminders to tolerate a few minutes of slack instead of requesting exact-alarm permissions users hate.
