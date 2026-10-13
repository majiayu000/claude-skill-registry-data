---
name: web-client-side-signing-bypass
description: >
  Reverse client-side request signing / obfuscated JS so you can replay and fuzz a protected API
  outside the browser. Load when requests carry a computed guard you must reproduce: an
  X-Signature / X-Sign / sign / hmac / _s / token header or body field, a nonce+timestamp, a
  "signature invalid" 401, encrypted request bodies, or minified/webpack/WASM/JSVMP signer code.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
owasp: [A04:2021-Insecure-Design]
cwe: [CWE-602, CWE-807]
tools: [burp, mitmproxy, devtools, python-requests]
schema_version: 1
---

# Reversing client-side request signing

## When it applies
An endpoint you want to fuzz (for `web-idor`, `api-bola`, `api-mass-assignment`, or business
logic) rejects tampered requests with a `signature invalid` / `401` because the client computes a
guard value in JavaScript — an HMAC over the body, a nonce+timestamp, or an encrypted payload.
You need to reproduce *one* valid signed request outside the browser so you can mutate the parts
that matter and re-sign them.

## Why it works
The signature is **client-side integrity theater**: the secret and the algorithm ship to the
browser, so anything the browser can compute, you can compute. The signing weakness itself is
almost always N/A — the payout is the access-control or logic bug on the endpoint it was
"protecting". Reproduce the signer, and that endpoint becomes as fuzzable as an unsigned one.

## Method

**Step 0 — packet-first: prove you even need to reverse anything.** Before reading a line of JS:
1. Replay the captured request *unchanged*. 200 → it wasn't signed; stop, just fuzz it.
2. Replay it a few minutes later. Still 200 → wide/absent replay window (a finding on its own).
3. Mutate a field you care about (e.g. an object id) but keep the signature. 200 → that field
   isn't covered by the signature; you can fuzz it directly, no reversing needed.
4. Only if mutating the target field breaks the signature do you proceed to reverse it.

**Step 1 — locate the signer.** In DevTools → Sources, set an **XHR/fetch breakpoint** on the
endpoint path; when it hits, walk the **Call Stack** down to the frame that writes the signature
field. Pretty-print (`{}`) to stabilize line numbers, and global-search (`Ctrl+Shift+F`) for the
header/field name. You are still "locating" until you can point at the exact line that produces
the value — the string `sign` in a function name is not proof.

**Step 2 — recover a callable signer.** Peel obfuscation only as far as you need:
- Set a breakpoint on the writer line and read its inputs/output live in the console.
- Hook it: `const _o = obj.sign; obj.sign = (...a)=>{ const r=_o(...a); console.log(a,r); return r; }`
  to log every `input → signature` pair as you drive the app.
- If it's webpack, grab the module and call it directly from the console; if WASM/JSVMP, prefer
  to **bridge** (drive the real function headless) over fully re-implementing it.

**Step 3 — classify every input.** Split the signer's inputs so you know what to regenerate vs.
pin:

| input | do this |
|---|---|
| timestamp | regenerate per request; note the validity window |
| nonce / requestId | generate fresh; check the server rejects reuse |
| deviceId / uuid | pin one constant from a real session |
| body / path / id | **the prize** — mutate, then re-sign |
| embedded secret key | if it's in the JS, forge fully offline |

**Step 4 — reproduce outside the browser.** Rebuild the request in Python `requests` (or drive
the hooked function via a headless bridge), sign it, send it. When it fails, **diff the pre-hash
message string**, not the output hash — JSON key ordering and field concatenation order are the
usual culprits.

**Step 5 — pivot to the real bug.** With one signed request replaying, re-sign mutations and hunt
the endpoint: IDOR/BOLA, broken auth, mass assignment, business logic.

## Gotchas
- **Key/field ordering** breaks validation more than the crypto does — canonicalize exactly like
  the client (some sign `k1=v1&k2=v2` sorted, some sign raw JSON as-typed).
- **Missing browser state** (localStorage, cookies, lifecycle vars the signer reads) can make
  pure offline signing impossible — bridge to the live function instead of re-implementing.
- **Anti-debug branches** (`debugger;` loops, timing checks) can change behavior when DevTools is
  open; classify that divergence before you start patching the script.
- Don't report the signing scheme itself as the vulnerability — report the downstream bug it let
  you reach (validate it with `reporting-triage-validation`).

## Verify success
One request, signed by your own code (or your bridge) and *not* captured from the browser,
returns 200 with a field you mutated — and a re-signed IDOR/auth probe against that endpoint
succeeds.

## References
Chrome DevTools Sources/breakpoints docs; PortSwigger notes on client-side controls; WASM/JSVMP
deobfuscation write-ups.
