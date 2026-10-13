---
name: web-webauthn-software-authenticator
description: >
  Register and authenticate against a WebAuthn/FIDO2 relying party using a self-built
  SOFTWARE authenticator (no hardware key) when the RP requests attestation "none" (or
  otherwise doesn't verify attestation trust). Load when: a login is "WebAuthn/passkey/
  FIDO2", endpoints like /webauthn/register|auth/begin|finish, `navigator.credentials`,
  and you hold (or can leak) a registration invite/enrollment token. Authorized targets only.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A07:2021-Auth-Failures]
cwe: [CWE-287]
schema_version: 1
---

# Forge a software WebAuthn authenticator (attestation: none)

## When it applies
- The app authenticates with **WebAuthn/FIDO2** (register + authenticate "ceremonies",
  `navigator.credentials.create/get`, client bundles calling
  `/register/begin`,`/register/finish`,`/auth/begin`,`/auth/finish`).
- `register/begin` returns creation options with **`"attestation":"none"`** (or the RP
  never validates the attestation certificate chain). None-attestation means the server
  does NOT check that a real hardware authenticator vouched for the key — so a key you
  generate in software is accepted.
- You can start registration: either registration is open, or you can **leak an
  invite/enrollment token** (see `tech-mongo-agg-facet-bypass` and NoSQL-injection notes).

## Why it works
WebAuthn security rests on the authenticator signing a server challenge with a private
key. With `attestation:none`, the server trusts whatever public key the client submits at
`register/finish` (no proof it came from a certified device). You therefore generate your
own keypair, register its public key, then at `auth/finish` sign the server's challenge
with the matching private key — a completely valid assertion, because it *is* your key.

## Method (Python: `cryptography` + `cbor2`, one cookie session)
1. `POST /register/begin {invite_token}` → options (`challenge`, `rp.id`, `user.id`,
   `pubKeyCredParams` incl. **-7 = ES256**, `attestation:"none"`).
2. Build the authenticator:
   - EC **P-256** keypair. COSE public key = `cbor2.dumps({1:2, 3:-7, -1:1, -2:x, -3:y})`
     (kty EC2, alg ES256, crv P-256, x, y — each coord 32 bytes big-endian).
   - `authData = sha256(rp.id) + flags + signCount(4B) + attestedCredentialData`
     where `flags = 0x45` (UP|UV|AT) and `attestedCredentialData = aaguid(16×00) +
     credIdLen(2B) + credId(random) + coseKey`.
   - `attestationObject = cbor2.dumps({"fmt":"none","attStmt":{}, "authData":authData})`.
   - `clientDataJSON = {"type":"webauthn.create","challenge":<opts.challenge as-is>,
     "origin":"http(s)://<rp host:port>","crossOrigin":false}`.
3. `POST /register/finish` with
   `{id:b64u(credId), rawId:b64u(credId), type:"public-key",
     response:{clientDataJSON:b64u, attestationObject:b64u}}` → credential created.
4. `POST /auth/begin` → new `challenge`.
   - `clientDataJSON = {"type":"webauthn.get","challenge":<achal>,"origin":<origin>}`.
   - `authData = sha256(rp.id) + flags(0x05 UP|UV) + signCount`.
   - `signature = privkey.sign(authData + sha256(clientDataJSON), ec.ECDSA(SHA256))`
     (cryptography emits DER — exactly what ES256 assertions use).
   - `userHandle = b64u(<user.id bytes>)` (needed for discoverable/resident-key flows).
5. `POST /auth/finish` with those fields → authenticated session cookie. Use it to hit
   the app (dashboard/account) and grab the flag.

## Tools
`python3` with `cryptography` and `cbor2` (both common). `fido2` (python-fido2) has a
built-in software authenticator if you prefer a library. All base64 is **base64url,
no padding**. A ready reference implementation: `aegis/exploit-dev/pwn.py`.

## Gotchas
- **Origin/rpId must match** what the server expects, including scheme and port
  (`http://host:3000`), and `rp.id` is the host WITHOUT the port. `sha256(rp.id)` uses the
  host only.
- `challenge` in `clientDataJSON` is the **same base64url string** the server sent (it's
  just re-encoding the same bytes) — don't double-decode/re-pad it.
- Resident-key/usernameless flows: `auth/begin` returns empty `allowCredentials`; you MUST
  send the correct `userHandle` at `auth/finish`.
- If the RP validates attestation for real (`"direct"`/known AAGUIDs with trusted roots),
  this won't work — you'd need a genuine chain. `none` (or a lenient verifier) is the tell.

## Verify success
`register/finish` returns 200/created and `auth/finish` returns 200 and sets an
authenticated session cookie that unlocks previously-redirected pages (e.g. `/dashboard`
stops 302-ing to `/login`).

## Learned on
**AEGIS lab, 2026-08** — leaked invite token via Mongo aggregation injection, then
registered a software P-256 authenticator (attestation "none") as operator `op-2026-0042`.
Full worked example in `aegis/notes.md` (§6) and `aegis/exploit-dev/pwn.py`.
