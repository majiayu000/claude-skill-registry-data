---
name: padosoft-mobile-security-review
description: >-
  Use this skill before committing or reviewing a change to a React Native / Expo app that touches secrets or
  API keys, token storage, a WebView, a deep link or an external URL, TLS and certificate pinning, a
  dev/mock/debug surface, or an AI/LLM call — and whenever the user asks whether something can go in the
  bundle, in an EXPO_PUBLIC_ variable or in MMKV, or asks for a mobile security review or an audit. It runs
  the checks with their pre-screens and, for a finding whose enforcement lives outside the repository, states
  the severity conditionally instead of guessing. Do not use it for API-side security (padosoft-api-security-review),
  store review rejections, or MDM and device fleet policy.
license: MIT
compatibility: >-
  React Native with Expo. The pre-screens assume a POSIX shell; the rules hold for any mobile app that ships a
  JavaScript bundle.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The bundle ships to every device and can be decompiled — everything follows from that.
  profiles: react-native
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: mobile, security, react native, expo, secrets, secure-store, webview, deep link, tls, mtls
---

# Mobile security review

**The premise that decides everything: the bundle is shipped to every device and can be decompiled.** Anything
in the bundle or in a committed asset is public. `EXPO_PUBLIC_*` variables are inlined at build time, so they
are public configuration — never a secret, never a runtime security boundary.

Run these before committing a change to the areas below. A HIGH/CRITICAL violation should bounce the PR.

---

## 1. No secrets in the bundle — `MOBILE-SEC-SECRET-001`

```bash
grep -rnE "privateKey|BEGIN (RSA |EC )?PRIVATE KEY|pkcs12|p12Password|apiKey\s*[:=]\s*[\"']" src apps packages
grep -rn "EXPO_PUBLIC_" src apps packages | grep -iE "secret|token|key|password"
```

No private cryptographic material in source: RSA PEM, PKCS12 blobs, the PKCS12 password. No hardcoded API
keys. `.env` (non-example) gitignored.

**The JS on the device is not obfuscated.** Metro minifies and Hermes emits bytecode: that shortens **names**,
not **string constants**. A PEM comes out of a Hermes bundle with `strings`. And an OTA bundle travels over
the network and stays in a cache — less friction than native code, not more.

**A key distributed over the air is public from the moment you distribute it**, so rotating it does not
restore secrecy.

### When the constraint is real, the remediation has to respect it

A client certificate has to be **rotatable**, and rotating something in native code needs a store release —
whoever does not update is left with a key the server rejects, the app stops working, and that is not a
security problem, it is a lost customer. **A remediation that ignores this constraint does not get applied.**

What does not follow is the next step: "it must be updatable without a release" → true; "so it lives in a
versioned source file" → no. Options, in order:

| | Approach | Why it is better |
|---|---|---|
| **A** | Platform attestation (App Attest / Play Integrity) | The key is generated **in hardware** and is not extractable even on a jailbroken device. There is no shared key to rotate: the problem stops existing rather than being solved |
| **B** | Runtime provisioning into Keychain/Keystore | Rotation becomes a server operation. The provisioning endpoint cannot sit behind mTLS — that is circular — so protect it with (A) |
| **C** | Signed requests: short-lived session key + HMAC | No PKI at all |
| **D** | mTLS as-is, but the key from a build-time secret, per-app certificates, short validity | Write it down as **friction, not a boundary** |

And the question upstream: an mTLS certificate extractable from the APK **filters** (pointing `curl` at the
API gets a handshake error), it does not authenticate. It belongs to the captcha family, and should be
compared against bot management and per-identity rate limiting.

### Severity when enforcement lives outside the repo

A client certificate is worth exactly as much as the mTLS rule that demands it: in TLS the client presents it
**only on the server's `CertificateRequest`**. If you cannot see the edge configuration, **write the severity
conditionally** — "CRITICAL *if* the rule is active" — and turn the verification into an ops action. The
defect is still debt, because **whoever switches that boundary on one day will switch it on believing it is
closed** — and the certificate stays valid in the account until expiry, even after a `git rm`, since the key
is in the git history.

## 2. Token storage — `MOBILE-SEC-STORAGE-001`

```bash
grep -rnE "encryptionKey\s*:\s*[\"']" packages src apps      # a literal key is the anti-pattern
grep -rnE "setItem\(\s*[\"'](access|refresh)?[Tt]oken" packages src apps
```

Tokens and credentials go in the system enclave (`expo-secure-store` → Keychain/Keystore). **MMKV is fast
application storage, not a secure store**: an `encryptionKey` present in the bundle is readable.

```ts
// ❌ key in the bundle, identical on every device
createMMKV({ id: "auth", encryptionKey: "auth-secret-key" });
// ✅ random per install, itself kept in the secure store
createMMKV({ id: "auth", encryptionKey: await getOrCreateMmkvKey() });
```

A password is never persisted anywhere. Stores without sensitive data may stay in plain MMKV.

## 3. WebView hardening — `MOBILE-SEC-WEBVIEW-001`

```bash
grep -rnE 'originWhitelist|onShouldStartLoadWithRequest|setSupportMultipleWindows|x-session-token' src packages
```

- `originWhitelist` restricted — **never `["*"]`, not even for inline HTML** (use the known host, or `about:blank`).
- `onShouldStartLoadWithRequest` is an **allow-list**, never a blanket `return true`.
- `setSupportMultipleWindows={false}` on any WebView loading remote content.
- `Authorization` / session headers injected **only towards trusted hosts**: your own configured host, an
  explicit per-app allow-list, or an opt-in flag passed by a trusted call site. Keep that allow-list minimal —
  **every host on it receives the user's session.**
- `onMessage` payloads validated with a schema; never act on an unvalidated message.

## 4. Deep links and external URLs — `MOBILE-SEC-DEEPLINK-001`

Validate every external URL (schema allow-list + parser) before `Linking.openURL`. Never `router.push` a raw
external URL. Associated domains bound to hosts you own.

## 5. Network and TLS — `MOBILE-SEC-NETWORK-001`

`https://` only in production; cleartext `http://` strictly gated on the dev flag. Certificate pinning with a
**backup pin**. Injected mTLS material never committed. A debug/remote-logging server URL stays dev-only.

## 6. Dev gates and anti-tamper — `MOBILE-SEC-DEVGATE-001`

```bash
grep -rnE "EXPO_PUBLIC_[A-Z_]*(DEV|DEBUG|MOCK|E2E)" src apps packages
```

Dev, mock and debug surfaces gate on the **build-time dev flag**, never on an `EXPO_PUBLIC_*` that can simply
be omitted. Anti-tamper stays wired into the root gate. A flag that disables anti-tamper for E2E must never
appear in a release build profile.

## 7. Logging — `MOBILE-SEC-LOG-001`

No `console.*` in runtime code; never log tokens, `Authorization`, PII or whole bodies at `info`; sensitive
detail only at `debug`. The full reasoning, and the redaction mechanism for each stack, is in
**`padosoft-logging-discipline`** — read it when a finding here is about what ends up in a log line.

## 8. AI / LLM surface — `MOBILE-SEC-LLM-001`

Write this one **before** adding a model, because retrofitting it is expensive and the first PR that adds one
is when nobody has time to think about it.

- **The app never holds a provider key** — not in the bundle, not in `EXPO_PUBLIC_*`, not in the secure store.
  Distributed means published, and rotating it costs a store release. The app calls **your backend**, which
  holds the key and owns auth, rate limit and quota.
- **The system prompt lives server-side.** A prompt in the bundle is readable, so it cannot carry business
  rules or "do not reveal" instructions.
- **Model output is untrusted input**, and on mobile the sinks are navigation and WebViews: every URL from the
  model goes through the deep-link validators (§4), never a raw `router.push`, never a WebView whose URL the
  model influences while you inject session headers, no model HTML concatenated into injected JavaScript, no
  dynamic `eval`/`Function`.
- **Prompts and conversation history are personal data**: secure store (or MMKV with a per-install key), never
  at `info`.
- **Actions: the model proposes, the user confirms on screen**, one action at a time — never a global "let the
  assistant act" toggle. Confirmation text built by the backend, re-validated server-side (the client
  confirmation is UI, not a control), idempotency key generated at confirmation (mobile networks retry), no
  auto-navigation or auto-submit, no biometric or permission prompt triggered by model output.

---

## Gotchas

- **`EXPO_PUBLIC_*` is not a gate.** It is inlined at build time and omittable at run time: as a security
  switch it fails open.
- **`git rm` does not revoke anything.** A key that was committed stays valid in the account until it is
  rotated at the provider, and it stays in the git history.
- **Severity is not a feeling.** When the enforcement is outside the repo, say "CRITICAL if X is active" and
  name the ops check. A grade written without being able to see the edge configuration has to be walked back
  when the configuration turns out to differ — and a finding that gets walked back is a finding people stop
  trusting, even when the defect is real.
- **A remediation that ignores a real constraint is not applied**, and then the finding stays open forever
  while everyone believes it was handled.

## Final report

```
Mobile security review: <n> files
MOBILE-SEC-SECRET-001  PASS | FAIL <file:line — what, and severity, conditional if enforcement is external>
MOBILE-SEC-STORAGE-001 · WEBVIEW-001 · DEEPLINK-001 · NETWORK-001 · DEVGATE-001 · LOG-001 · LLM-001
Not applicable to this diff: <rules>
Ops verification needed: <what has to be checked outside the repo>
Verdict: BLOCKED | OK TO COMMIT
```
