---
name: mobile-webview
description: >
  Exploit insecure mobile WebViews — JS-bridge abuse, file access, and XSS→native. Load when an
  app renders web content in a WebView/WKWebView, exposes a JS bridge, or loads attacker-influenced
  URLs. Signals: addJavascriptInterface, WKScriptMessageHandler, loadUrl, file:// access, deep-link → WebView.
domain: mobile
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp: [M4:2024-Insufficient-Input-Output-Validation]
cwe: [CWE-749, CWE-79]
tools: [jadx, frida]
schema_version: 1
---

# Mobile WebView abuse

## When it applies
The app shows web content in a WebView (Android `WebView` / iOS `WKWebView`) and either exposes a
native JS bridge or loads URLs/content an attacker can influence (deep link, param, MITM'd http).

## Why it works
WebViews blur the web/native boundary. A JS bridge (`addJavascriptInterface` /
`WKScriptMessageHandler`) lets page JavaScript call native code — so XSS or a malicious loaded page
can invoke native functionality. Misconfig (`setAllowFileAccess`, `setJavaScriptEnabled`, mixed
content) widens it to local file theft.

## Method
1. **Find the WebView config** in `jadx`/class-dump: `setJavaScriptEnabled(true)`,
   `addJavascriptInterface(obj,"name")` (Android <17 = any method exposed), `setAllowFileAccess`,
   `setAllowUniversalAccessFromFileURLs`, and what URLs it loads.
2. **Reach the WebView with your content**: via a deep link that passes a URL param into `loadUrl`,
   a param reflected into the page (XSS), or MITM if it loads `http://` (ATS/cleartext).
3. **Abuse the bridge**: from injected JS call the exposed native methods
   (`window.name.method(...)`) — read files, get device data, trigger actions the bridge exposes.
4. **File/scheme access**: `file://` loads + universal file access → read app-private files; `content://` tricks.

## Gotchas
- `addJavascriptInterface` on old targetSdk exposes reflection → RCE-ish; on modern it's limited to `@JavascriptInterface` methods — enumerate those.
- Impact = what the bridge exposes + whether you can get JS to run; prove both.
- iOS `WKWebView` message handlers are the equivalent bridge — check `userContentController`.

## Verify success
Injected JavaScript invokes native functionality via the bridge (data read, action performed), or
local files are exfiltrated through the WebView.

## References
OWASP MASTG (platform/WebView); Android WebView security docs; "WebView bridge abuse" write-ups.
