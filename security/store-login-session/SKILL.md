---
name: store-login-session
description: Reuse and recover authorized Apple App Store Connect, Apple Developer, or Google Play Console logins in an existing visible noVNC browser before interrupting a store release. Applies to expired store sessions, remembered-account Continue flows, and preserving a store profile between releases.
---

# Store login session

Recover ordinary store authentication within the authorized release task. Keep
the existing browser profile and visible desktop; an expired session is not by
itself a reason to stop and request another login.

## Reuse the correct session

1. Read the current project's store/runtime handoff. Identify its existing
   noVNC desktop, CDP endpoint, Chrome profile and exact app/store account.
   Inspect relevant tabs without dumping all tabs, cookies or input values.
2. Attach to the existing browser and bring the target tab forward. Open the
   exact app's Console page and observe whether it actually requires sign-in.
   Google often retains its login: do not log out or authenticate again when
   the requested Console page is already usable.
3. If Apple redirects to sign-in, use the visible remembered account and
   **Continue / Sign In** controls. Click once, wait for the next state, then
   click the next observed control if needed. The common two-click flow is
   two observed transitions, not a blind double-click or repeated submit.
4. If normal sign-in requires credentials, use the existing authorized private
   credential source or saved-browser login. Enter values without printing
   them. Preserve the intended Apple/Google identity and developer account.
5. Verify the actual destination: correct app, version and a usable protected
   page. A signed-in Apple Developer Portal does not prove App Store Connect
   authentication; neither proves the separate **Sign in with Apple** OAuth
   consent flow. Recover the scope the task actually needs.

## Recovery boundaries

- Use observed visible controls. For an expired intermediate link, navigate
  the same tab to the intended official service and start a fresh sign-in
  flow; do not reuse expired state/nonce URLs.
- Use ordinary remembered/trusted-device choices when presented. Do not
  change account security settings to prolong a session.
- If an actual 2FA code, CAPTCHA, device approval or missing credential cannot
  be completed with available authorized access, ask only for that specific
  missing step, with the existing noVNC URL. Continue independent release
  preparation while waiting. Do not report a login blocker before trying the
  ordinary remembered-session path.
- Stop after one complete recovery attempt and one observed expired-page
  retry if the same security prompt or failure remains. Do not create an
  infinite sign-in loop or retry account/password guesses.

## Preserve the browser, reconcile the release

- Keep the same on-disk profile. Do not clear cookies, sign out, create a
  replacement profile or restart a shared desktop just to refresh a tab.
  Leave other projects' store tabs and provider accounts unchanged.
- When the user requests a persistent store desktop, retain that one existing
  stack and record its URL/profile/ownership in the private runtime handoff.
  Do not launch another stack for each app or login attempt. Otherwise follow
  the workspace's normal runtime cleanup policy.
- Preserve session state rather than adding periodic clicks, keepalive traffic
  or unattended authentication jobs. Apple/Google can still expire sessions
  or demand fresh verification; do not promise permanent authentication.
- After recovery, read the exact release/submission state before continuing.
  An expired page or ambiguous timeout does not mean a submission failed.
  Reuse an existing draft and submit only once; distinguish submitted, waiting
  for review, approved and publicly available.
- Keep passwords, keys, cookies, QR codes, recovery URLs and private review
  credentials outside skill files, Git and tool output. Store evidence with
  private fields omitted or in the protected runtime directory.

For the shared Lachlan workstation, read
[the local desktop reference](references/lachlan-store-desktop.md) only when
working in that environment. Its historical ports are discovery hints, not
instructions to relaunch or take over another session.
