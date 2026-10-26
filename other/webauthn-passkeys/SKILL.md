---
name: webauthn-passkeys
description: Use when adding passkey (WebAuthn) sign-in to a web app, including passkey-only apps with no passwords — registration and authentication ceremonies, server-side challenge storage, relying-party ID and origin checks, enrolling a phone when long links cannot be passed to it, Safari's user-gesture rules, and session handling on edge runtimes. Also use when passkey creation fails on iPhone, works on one domain but not another, or users get locked out.
---

# WebAuthn passkeys

Default: a maintained library on both sides (e.g. SimpleWebAuthn), discoverable credentials (passkeys) with user verification required, challenges stored server-side with a short expiry, a recovery path decided before launch.

## Ceremonies

**Registration**
1. Server: generate options (RP ID, user handle, challenge, `residentKey: "required"`, `userVerification: "required"`), store the challenge with an expiry.
2. Client: `navigator.credentials.create({ publicKey: options })`.
3. Server: verify the response against the stored challenge, expected origin and RP ID; save credential ID, public key and counter; delete the challenge.

**Authentication** mirrors it with `navigator.credentials.get` and an allow-list that can be empty (discoverable credentials).

## Safari and user gestures

Safari requires the WebAuthn call to happen in the user's tap handler. If the handler first awaits a network request for options and then calls `create()`, Safari may reject it as not user-initiated.

- Fetch the options **when the screen opens**, keep them ready, and call `create()`/`get()` synchronously from the tap.
- Refresh the options if they expire before the user taps.

## Enrolling another device

Long one-time links are hard to move to a phone (messaging apps mangle them, typing is impossible). Offer a short one-time enrolment code shown on the signed-in device: the phone opens the site, enters the code, and registers its own passkey. Codes expire quickly, are single-use and rate-limited.

## Origins and RP ID

- RP ID is a registrable domain suffix of the origin (`example.com` covers `app.example.com`). A passkey created for one RP ID does not work on a different domain, including preview deployment URLs.
- Verify the origin exactly; list allowed origins explicitly for local development.

## Sessions

- After authentication, issue an HTTP-only, `Secure`, `SameSite=Lax` (or `Strict`) session cookie; keep the session store server-side (e.g. a database table) so sessions can be revoked.
- On edge runtimes use Web Crypto; avoid libraries that require Node built-ins.

## Recovery

Passkey-only means no password reset. Decide up front: multiple passkeys per account (encourage registering a second device), recovery codes printed at registration, or a re-enrolment procedure run by the site operator.

## Verification loop

1. Register and sign in on desktop (platform authenticator or password manager) and on a phone.
2. Replay a used challenge → rejected. Wrong origin → rejected.
3. Revoke a session → next request is unauthenticated.

## Pitfalls

- **Counters:** many passkeys report a signature counter of 0; do not treat "counter did not increase" as cloning when both values are 0.
- **User handle:** use a random opaque ID, not an email address.
- **Testing on `localhost`** works over HTTP; other hosts need HTTPS.
- **Lost devices:** without a recovery path, a single-passkey account is gone with the phone.
