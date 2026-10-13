---
name: mobile-deeplink-abuse
description: >
  Abuse deep links / custom URL schemes / intents for redirect, token theft, and reaching
  internal screens. Load on custom schemes (myapp://), App Links/Universal Links, exported
  activities, or "open in app". Signals: intent-filters in the manifest, WebView loading
  deep-link params, OAuth redirect via a custom scheme.
domain: mobile
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [M4:2024-Insufficient-Input-Output-Validation]
cwe: [CWE-939, CWE-926]
tools: [adb, jadx]
schema_version: 1
---

# Deep link / URL scheme / intent abuse

## When it applies
The app registers custom URL schemes or App/Universal Links, or exports activities that accept
data. A malicious link (in a web page, another app, or a QR) can then drive the app.

## Why it works
Deep-link handlers receive attacker-controlled data and often trust it: they redirect, load it
into a WebView, pass it to auth flows, or open privileged screens without re-checking who sent
the intent. Custom schemes aren't verified for ownership (unlike App Links), so any app can claim them.

## Method
1. **Map handlers**: from the manifest, list `intent-filter` schemes/hosts and exported
   activities; read `jadx` for how each parameter is used.
2. **Test open redirect / token theft**: if a deep link takes a `redirect`/`return_url` or the
   OAuth callback is a custom scheme, point it at attacker-controlled to steal codes/tokens.
3. **WebView injection**: if the deep link's data reaches `loadUrl()`/`evaluateJavascript`,
   try XSS/JS-bridge abuse (`android-webview` in `mobile-android-assessment`).
4. **Reach internal screens**: `adb shell am start -a android.intent.action.VIEW -d
   "myapp://internal/admin?..."` to invoke functionality meant to be gated.
5. **Intent redirection**: a component that forwards an attacker-supplied nested intent can be
   used to launch non-exported components.

## Gotchas
- Custom-scheme OAuth is inherently interceptable — that's the classic account-takeover chain.
- App Links (verified domains) resist scheme-hijacking; custom schemes don't.
- Test both from a web page (`<a href="myapp://...">`) and from `adb` — behaviour can differ.

## Verify success
A crafted link causes token/code disclosure to you, XSS in the app's WebView, or reaches a
screen/action that should require prior auth.

## References
OWASP MASTG (platform interaction); Android App Links docs; deep-link ATO write-ups.
