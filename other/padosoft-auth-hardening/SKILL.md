---
name: padosoft-auth-hardening
description: >-
  Use this skill when building or reviewing anything to do with who a user is and how long they stay that
  way — login, registration, password reset or change, email change, invitations, sessions, API tokens,
  second factor, logout, remember-me, a captcha on a form. Also when the user reports credential stuffing,
  an account enumeration finding, a session that never expires, a password change that did not log other
  devices out, a lockout that never fires, or asks what a new application needs before it opens to the
  public. It gives the control, the reason it is shaped that way, and the ways each one is commonly present
  but ineffective. Do not use it for authorisation and ownership (padosoft-tenant-isolation) or for the
  whole security posture (padosoft-security-baseline).
license: MIT
compatibility: >-
  Stack-agnostic. Examples assume a session-based web application with an API alongside it, because that is
  the combination where the doors disagree.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: Identity is a set of doors, and hardening means none of them disagrees with the others.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: authentication, login, session, mfa, rate limiting, enumeration, captcha, tokens, password
---

# Authentication hardening

The controls below are the ones that are typically *present and ineffective*: a limiter with the wrong key,
a lockout event nothing emits, a session lifetime that is a sliding window, a revocation that covers one
door out of three.

**The rule: identity is a set of doors, and hardening means none of them disagrees with the others.**

---

## 1. Rate limiting needs two keys, not one

```text
per address only  → distributed credential stuffing walks through
per account only  → N accounts get swept in parallel from one machine
both              → the attack has to be both slow and narrow
```

- Key the per-account limit on a **hash of the normalised identifier**, never the address itself: a limiter
  backed by a shared cache otherwise stores your users' email addresses in plaintext, in a second system,
  for ever.
- Put the client address **into** the per-account key as well, or an attacker can lock a real customer out
  of their own account at will. Denial of service against a named user is a cheap attack.
- **Limit the reset and the contact forms too.** They send mail on somebody else's behalf.
- **Check that a lockout actually emits an event.** Many frameworks only emit it from their own built-in
  throttling helper; a hand-rolled limiter raises nothing, so the detection rule that counts lockouts can
  never fire and nobody notices that nothing is noticing.

## 2. Nothing may enumerate accounts

The response must be identical whether or not the account exists — same body, same status, **same timing
class**. That applies to every surface, and the ones that get forgotten are the later ones:

| Surface | The tell |
|---|---|
| Password reset | "no account with that address" |
| Registration | "this address is already registered" |
| Email change | the same message, on the profile screen |
| Invitations | a mask that shows which invitees are already members |
| Account created during checkout | a different path when the address is known |
| Token refresh | a refusal that says **why** — expired is not the same as revoked, and you just said which |

Error messages on authentication forms are deliberately generic: a precise message is what tells a script it
has found a valid account.

## 3. Passwords

- **Length over arbitrary complexity.** Modern guidance prefers a long minimum and a breach check to
  mandatory character classes.
- **Reject known-breached passwords at every point a password is chosen**, using a range query so the
  password never leaves your server.
- **Deliberately exclude the login itself.** Rejecting an existing password at sign-in locks the user out of
  their own account, and they cannot fix it from there. Exclude bulk imports too, or you make one network
  call per row.
- **Fail open when the breach service is unreachable** — and write down that you did.
- **Confirm the address before the account can be used**, or registration is a way to occupy somebody else's
  identity.

## 4. Sessions

- **Rotate the session identifier at login.** Most frameworks do; the risk is a custom login path that does
  not.
- **Rotate it again on any privilege change** — impersonation, role switch, elevation.
- **A sliding lifetime is not a timeout.** A session that renews on every request stays alive for ever as
  long as something touches it every so often, which is exactly what a stolen session does. Add an
  **absolute** lifetime measured from the first authenticated request.
- Turning an absolute lifetime on without warning throws out everyone mid-task, so it ships **off** with a
  value the team chooses — but the floor lives in code, because a security boundary is not a setting.
- **It does not cover a stolen long-lived cookie**, which re-authenticates into a brand-new session. Those
  need their own revocation.
- **Binding a session to a client fingerprint** raises the cost of reusing a stolen cookie. Measure what it
  actually rejects before counting on it.

## 5. Revocation has to be one thing

Changing a password usually has three doors — the API, the reset link, the account page — and they routinely
produce three different outcomes: one revokes the tokens, one sets a flag and leaves them alive, one does
nothing. The most-used door is rarely the most careful one.

- **One service, called by all of them.**
- **Delete tokens one by one** rather than in a single bulk statement, so the model observer that clears the
  cached copy actually runs. A bulk delete leaves a valid token in the cache.
- **Revoking web sessions is separate** from revoking API tokens, and needs the middleware that tracks them
  to be active.
- **Record who revoked what, and why.** A disconnection whose cause is unknown is indistinguishable from an
  attack.

## 6. Second factor, and why it stays off for years

The mechanism is usually already installed and disabled. What is missing is never the code: it is the answer
to *how many accounts would be locked out if we turned this on tomorrow*.

```text
audit (who has no second factor) → enrol those accounts → enable
```

- **Take the secret, the recovery codes and the long-lived tokens out of mass assignment**, with a test that
  keeps them out: those field lists are commonly regenerated by a scaffolding tool, and the regeneration
  puts them back. Writable, they allow substituting somebody's second factor, forging a persistent login and
  regenerating a confirmation token.
- **Verifying a code is not a lifecycle.** Enrolment must confirm possession before activation, recovery
  codes are stored as non-reversible hashes and consumed atomically, and the secret needs a real protector.
- **Require re-authentication for privileged changes** even inside a live session — editing users, roles or
  permissions is what a stolen session is worth the most for.

## 7. A captcha is friction, not a control

The strong control against credential stuffing is the rate limit. A modern score-based captcha is solved
commercially for a few units of currency per thousand: it raises the cost of mass automation, and it does
not stop a determined attacker. Everything below follows from that premise.

- **The score is the verdict, not the success flag.** A success field usually means only that the token was
  well-formed and unexpired — it is true for an obvious bot. Stopping there rejects whoever sends no token
  and admits every bot that generates one, which takes a single call with the public site key already in
  your page.
- **A decimal threshold read through an integer cast becomes zero**, and zero means off, silently, with
  nothing to indicate it. This applies to every decimal setting you own, not only this one.
- **Fail open when the verifier does not answer** — a timeout, a DNS failure, an egress firewall — and log
  it. Blocking means losing real traffic because a third party has a problem, in exchange for nothing:
  the attacker is not coming through the form. Log a provider-side client error at a **higher** level than a
  timeout: that one is persistent and someone must look.
- **Both fail-open choices are acceptable only while the rate limit holds.** Write the dependency down, so
  removing the limiter re-opens the question.
- **The verification timeout is a real tradeoff.** Too long and a worker is held for its whole duration —
  under a bot the pool empties and the captcha becomes an availability multiplier. Too short and every
  transient slowdown becomes a systematic fail-open, disabling the control exactly when the network is under
  strain.
- **No half switch.** A toggle that disables the server-side verification while the page keeps calling the
  provider looks like a decision and is not one.
- **Do not add a conditional in front of forms that already have it**, or they stay unprotected until
  somebody remembers to turn a setting on.

## 8. Telling the user something happened

A notification on a sign-in from a new context is one of the few controls that catches an attacker who has
everything right. It is also the control most likely to be switched off for noise, so:

- **Fingerprint the context, do not store it.** A keyed hash of a device family plus a truncated network —
  never the full address, which is personal data you now keep for as long as the table lives.
- **Strip version numbers from the client string and truncate the address**, or every browser update is a
  new context and every notification is a false alarm.
- **The first context of an account never notifies**, or the day you deploy everybody gets an email.
- **Anti-flood per account.**
- **Queue it, and make the listener incapable of failing the login.** A notification path that can throw
  turns a security feature into an outage.

## 9. Tokens

- **Classes, not one shape.** A staff token and a customer token have different lifetimes, scopes and
  revocation rules; one table with one meaning is how a customer token ends up with staff reach.
- **An identifier is never the only factor.** A value that is both the name of a thing and the proof you may
  have it is a credential in a URL, and it will be in a log, a referrer and a screenshot.
- **Mock or test authentication must be impossible in production**, enforced at startup and failing fast,
  not by a branch somewhere — see **`padosoft-environment-gating`**.

---

## Gotchas

- **The limiter that protects the login does not protect the endpoint that logs you in a second way.**
  Mobile entry points, single-page flows and legacy paths are separate doors.
- **A uniform response that takes a different amount of time is not uniform.**
- **"It is behind the edge" is not an authentication control**, and it is only true while the origin refuses
  everything else.
- **A security event nobody emits cannot be alerted on.** Check the event exists before building the alert —
  see **`padosoft-failure-visibility`**.
- **A second factor enabled without an enrolment audit locks out exactly the people who cannot call you.**
- **The most-used door is usually the least careful one**, because it was written first and has the most
  legacy behind it.

## Checklist

- [ ] Login limited by account **and** address; the account key hashed; the address inside the account key
- [ ] Reset and mail-sending forms limited too
- [ ] A lockout emits an event, and something counts it
- [ ] Reset, registration, email change, invitation and refusal responses reveal nothing about existence
- [ ] Breached-password rejection at every choice point, excluded at login on purpose, failing open
- [ ] Address confirmed before the account is usable
- [ ] Session rotated at login and at privilege change; absolute lifetime in addition to the sliding one
- [ ] One revocation service used by every door; tokens deleted individually; cache invalidated
- [ ] Second factor: audit first, then enrolment, then enabling; secrets out of mass assignment, with a test
- [ ] Re-authentication required before changing users, roles or permissions
- [ ] Captcha judged on the score; decimal threshold read without an integer cast; fail-open documented
- [ ] New-context notification fingerprinted, version-stripped, first-context silent, queued, non-fatal
- [ ] No test or mock authentication reachable in production

## Final report

```
Doors reviewed: <login paths, reset, registration, API, mobile>
Rate limits: account <key, rate> · address <rate> · lockout event: emitted | none
Enumeration: <surfaces checked, and what each returns>
Session: rotation <…> · sliding <…> · absolute <…> · binding <…>
Revocation: one service | <which doors diverge>
Second factor: <installed? enabled? accounts without it: n>
Anti-automation: <control, threshold, fail-open and what carries the weight>
Open: <…>
```
