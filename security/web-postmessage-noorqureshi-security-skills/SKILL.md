---
name: web-postmessage
description: >
  Exploit insecure cross-window messaging (`window.postMessage`) — handlers that trust `event.data`
  without checking `event.origin`, leading to XSS, token theft, or state change. Load when the app
  uses iframes/popups/SSO widgets, on "postMessage", or when JS registers a `message` listener.
  Signals: `addEventListener("message", ...)`, embedded third-party frames, SSO/login popups.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A03]
cwe: [CWE-346]
tools: [burp, chrome-devtools]
schema_version: 1
---

# postMessage abuse

## When it applies
The target sends or receives `postMessage` between windows/iframes (SSO, payment widgets, chat,
embeds). A receiver that doesn't validate the sender's origin will act on a message from *your*
page.

## Why it works
`postMessage` is cross-origin by design; safety depends entirely on the receiver checking
`event.origin` and the sender setting a specific `targetOrigin`. Miss the origin check and any site
can drive the handler; use `targetOrigin="*"` and any embedder can read the message. Then it's just
a matter of what the handler does with `event.data` — often `innerHTML`, `eval`, `location`, or a
relayed token.

## Method
1. **Find listeners**: grep the JS for `addEventListener("message"` / `onmessage`; note the sink each
   handler feeds (`innerHTML`, `eval`, `document.write`, `location`, another `postMessage`).
2. **Check the origin guard**: no check, or a weak one — `origin.indexOf("trusted")>-1`,
   `origin.endsWith("site.com")` (matches `site.com.evil`), a loose regex — is exploitable.
3. **Drive the sink (XSS)**: host a page that `open()`s or `<iframe>`s the target and
   `postMessage()`s a payload the handler writes to a DOM sink → script execution.
4. **Steal data (leak)**: if the target *sends* messages with `targetOrigin="*"` (tokens, PII),
   embed it and read them in your `message` listener.
5. **Bypass a bad check**: register your attacker origin to satisfy the substring/regex flaw
   (`trusted.attacker.com`, `attackertrusted.com`).

## Gotchas
- `event.origin` (the sender) is the thing to validate — not `event.source` and not the URL bar.
- Sandboxed iframes and `X-Frame-Options`/CSP `frame-ancestors` may stop framing — use a popup
  (`window.open`) instead.
- Some handlers require a specific `data` shape/handshake — replay the legit message first, then mutate.

## Verify success
A message from your attacker page reaches a dangerous sink (script executes / navigation happens) or
you read a secret the target broadcast — reproducible from an external origin.

## References
PortSwigger DOM-based / postMessage; MDN Window.postMessage security notes.
