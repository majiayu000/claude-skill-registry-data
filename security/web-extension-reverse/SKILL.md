---
name: web-extension-reverse
description: >
  Reverse engineer browser extensions (Chrome/Edge MV2/MV3, Firefox) for an authorized review:
  unpack .crx/.xpi, assess the permission surface, trace background/service-worker and content-script
  logic, and recover credential, signing, or traffic-handling behavior. Load on "analyze this
  extension", extension supply-chain or malicious-extension investigation, or keys hidden in
  chrome.storage. Signals: .crx, .xpi, manifest.json, chrome-extension://, <all_urls>,
  webRequestBlocking, declarativeNetRequest, externally_connectable, nativeMessaging.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty, defense]
severity: medium
mitre: [T1176]
cwe: [CWE-798]
tools: [jq, chrome-devtools, yara, unzip]
schema_version: 1
---

# Browser extension reverse engineering

## When it applies
The target is a browser extension — a `.crx`/`.xpi` package or an unpacked extension directory —
not ordinary page JavaScript (for that, load `reverse-eng-js`). Typical jobs: audit an in-scope
extension's client-side signing/encryption/proxy logic, hunt for over-privileged permissions in a
review, or investigate a malicious or supply-chain-poisoned extension. Target must be confirmed in
`scope.txt` (`tradecraft-scope-roe`); for malicious samples work in an isolated VM and see
`defense-malware-triage`.

## Why it works
An extension is just a zip with a `manifest.json` that declares its entire trust surface —
permissions, host permissions, entry scripts. Reading the manifest first tells you exactly which
scripts can touch which origins, and every browser-API capability (`webRequest`, `cookies`,
`nativeMessaging`) is reachable by grepping for `chrome.*` / `browser.*` calls from those entry
points. The dynamic half is free: Chrome runs unpacked extensions natively and DevTools attaches
straight to the background service worker.

## Method
1. **Unpack.** `.xpi` is a plain zip. `.crx` has a CRX3 header before the zip data — most unzip
   tools tolerate it; if not, strip the header or pull the already-unpacked copy from the browser
   profile (`.../Extensions/<id>/<version>/`).
2. **Read the manifest first:** `jq '{permissions, host_permissions, background, content_scripts,
   web_accessible_resources, externally_connectable, content_security_policy}' manifest.json`.
   Record MV2 (`background.scripts`, `webRequestBlocking`) vs MV3 (`background.service_worker`,
   `declarativeNetRequest`) — it changes where the logic lives.
3. **Score the permission surface.** Red flags: `<all_urls>` (read/write any site),
   `webRequest`/`webRequestBlocking` (MITM-grade request rewriting), `debugger`, `cookies`,
   `nativeMessaging` (escapes the browser to a host binary — follow it with
   `reverse-eng-binary-triage`), and `externally_connectable` (lets *web pages* drive the
   extension — a remote attack surface).
4. **Trace the logic.** Start at the service worker / background entry, then the content scripts —
   note each script's `matches`, `run_at`, and whether it runs in the isolated world. Grep for
   `chrome.storage` / IndexedDB to find stored keys and tokens, and for
   `runtime.onMessage`/`sendMessage`/`postMessage` to map who can drive what. For obfuscated or
   webpack-packed code, anchor on the `chrome.*` API calls and run the `reverse-eng-js` recovery
   flow; for the fast attack-side path see `web-client-side-signing-bypass`.
5. **Go dynamic.** Load the unpacked directory at `chrome://extensions` (Developer mode), watch
   for load errors, then open DevTools on the **service worker** link. Trigger events and observe
   network traffic and message passing; Burp/CDP covers the deeper hooks. For known-bad hunting,
   run YARA rules for malicious-extension families over the unpacked tree.

## Gotchas
- **MV3 service workers suspend when idle** — breakpoints go cold. Keep the worker's DevTools
  window open and trigger the event you're tracing; don't expect it to be alive on its own.
- **MV3 `declarativeNetRequest` is declarative** — the blocking/redirect logic lives in the JSON
  ruleset, not JS. Read the rules file; there is no function to hook.
- **Content scripts run in an isolated world** — page JS can't see their variables, and they can't
  see the page's. Cross-talk happens over the DOM or `postMessage`; audit both directions.
- **Secrets live in the installed profile, not the package** — `chrome.storage.local` persists in
  the profile's LevelDB; check there during a live-host review.
- **`.crx` from the Web Store is signed and version-locked** — for reproducible analysis record the
  extension ID + version, and diff updates before concluding.

## Verify success
You can state, with evidence: the full permission surface and entry scripts, the data flow (what
the extension reads, where it sends it, where keys/tokens live), and who can message it
(other extensions, web pages, native hosts) — each claim cited to a manifest field or code location.

## References
Chrome MV3 migration docs; `chrome://extensions` developer mode; OWASP CISQ extension guidance.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
