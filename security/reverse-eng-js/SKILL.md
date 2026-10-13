---
name: reverse-eng-js
description: >
  Reverse front-end JavaScript end to end: trace which script fires a given request, capture a
  signing/encryption function's real inputs at runtime, then rebuild the algorithm locally in
  Node.js with evidence-driven environment shims until it reproduces the target parameter.
  Load when you need the *mechanism* behind client-computed params (sign, signature, _signature,
  X-Sign, token, encrypted bodies, anti-bot / risk-control fields), when webpack-minified or
  obfuscated JS hides the logic, or when you must trace an XHR/fetch/WebSocket trigger point.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-602]
tools: [chrome-devtools, burp, mitmproxy, nodejs, babel]
schema_version: 1
---

# Front-end JavaScript reverse engineering

## When it applies
An in-scope web app computes something in JavaScript that you need to understand or reproduce:
a request signature, an encrypted body, anti-bot / risk-control fields, or a hidden WebSocket
protocol. `web-client-side-signing-bypass` covers the fast attack-side path (prove the guard is
client-side, get one replayable request); load *this* skill when you need the full algorithm
recovered and running locally in Node — for sustained fuzzing, logic audit, or documentation.
Target must be in `scope.txt` (`tradecraft-scope-roe`); observe only your own session.

## Why it works
The page must run the algorithm in the browser before the request leaves, so both the code and
every input to it are observable at runtime — minification only slows you down, it can't hide
execution. Break on the outgoing request, walk the call stack to the signing function, lift it
into Node, and the only thing left is the handful of browser globals it touches — which you
shim strictly from observed errors, never from imagination.

## Method
Principles: observe first · hook before you breakpoint, breakpoint last · rebuild from page
evidence · one minimal patch at a time.

1. **Observe.** Open the page with DevTools Network recording (Burp/mitmproxy upstream for the
   raw view). Identify the target request and its computed params, then read the request's
   **Initiator** stack to find the calling scripts. Global-search all loaded sources
   (`Ctrl+Shift+F` in DevTools) for the param name and the usual suspects: `sign`, `encrypt`,
   `md5`, `sha256`, `hmac`, `CryptoJS`.
2. **Capture.** Set an **XHR/fetch breakpoint** on a unique URL substring (Sources panel).
   When it pauses, walk up the call stack out of library frames into app code and read
   locals/arguments — you want the signing function, the raw input string, and any key/secret
   in scope. Lighter hooks (console overrides of `fetch`, `XMLHttpRequest.prototype.send`,
   `JSON.stringify`) often yield the same evidence with less noise — snippets in
   [`cheatsheet.md`](cheatsheet.md).
3. **Rebuild.** Copy the signing function plus its closure dependencies into a local Node
   script. Before writing a single shim, confirm from page evidence: the real entry function,
   the call order, where each parameter comes from, which browser objects it touches, and
   whether it depends on time, randomness, storage, cookies, UA, canvas, or `crypto`. Run it
   and record the **first exception / first divergence** — that, not intuition, drives step 4.
4. **Patch the environment**, strictly error-driven: shim only what the failure proves is
   missing, one minimal causal unit per step — a plain value first, then a function stub, then
   an object contract (`cheatsheet.md` has a starter shim set). Re-run after every patch;
   success means the first divergence moved forward.
5. **Deep-dive (optional).** Only once the script reproduces the parameter stably: prettify
   and deobfuscate for readability or logic audit (`reverse-eng-deobfuscation` for JSVMP,
   control-flow flattening, string-array ciphers, anti-debug). If all you needed was the
   parameter, skip this phase.

When a phase stalls, fall back one rung instead of forcing it: breakpoint → plain request
observation; source guessing → runtime evidence; Node env-rebuild → back to the page for more
forensics; deep deobfuscation → minimal reproducible chain.

## Gotchas
- **Never guess-shim `window`/`document`/`navigator` up front** — evidence-first is the whole
  discipline; a shim list growing past ~10 objects means you picked the wrong entry point.
- **Time/random-dependent signatures** — stub `Date.now()` / `Math.random()` to the captured
  sample's values for a byte-identical comparison, then check the server's tolerance window.
- **Webpack code-splitting** — the signer may live in a lazily loaded chunk: perform the action
  once, *then* search sources.
- **Anti-debug** (`debugger;` loops, devtools-detection, timing checks) — neutralize the check
  itself or "Deactivate breakpoints"; heavy cases go to `reverse-eng-deobfuscation`.
- **WebSocket** per-message signing follows the same path — hook the socket's `send`.

## Verify success
Given the same inputs (with time/nonce pinned to a captured sample), your Node script outputs
the **identical** signature or encrypted body as the page did. Then sign a fresh, unseen
payload, send it outside the browser, and the server accepts it — the endpoint is now as
fuzzable as an unsigned one; hand off to `api-fuzzing` or `web-client-side-signing-bypass`
step 5.

## References
Chrome DevTools Sources/CDP docs; `web-client-side-signing-bypass`,
`reverse-eng-deobfuscation`, `recon-js-analysis` in this library.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
