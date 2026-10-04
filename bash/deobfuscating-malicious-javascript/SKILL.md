---
name: deobfuscating-malicious-javascript
description: 'Deobfuscates malicious JavaScript from droppers, web pages, and HTA/scriptlets:
  unrolling string-array and char-code encodings, resolving eval/Function chains, and statically
  recovering payloads and URLs without executing untrusted code. Activates for requests to
  deobfuscate JavaScript, decode obfuscated JS, or analyze a malicious script dropper.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - javascript
  - deobfuscation
  - document-malware
  - droppers
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.007
  - T1027
  - T1140
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'ECMAScript language specification — https://tc39.es/ecma262/'
  - 'box-js malicious JavaScript sandbox — https://github.com/CapacitorSet/box-js'
---

# Deobfuscating Malicious JavaScript

## When to Use

- You have obfuscated JS (from a phishing page, HTA, `.js` dropper, or scriptlet) and need its real
  behavior.
- You must recover hidden URLs, dropped commands, or a next-stage payload.
- You want to statically unroll common obfuscation rather than run untrusted code.

**Do not use** a real browser or `node` to execute the script for analysis — that runs the
malware. Use a sandboxed interpreter (box-js) or static transformation only.

## Prerequisites

- A safe analysis approach: static decoding, or a JS malware sandbox (box-js) in the lab.
- Familiarity with common obfuscation: string arrays, `String.fromCharCode`, hex/unicode escapes,
  `eval`/`Function` chains, packers.

## Safety & Handling

- Treat the script as live code; never execute it outside an isolated sandbox.
- Defang recovered URLs and store dropped payloads password-protected.

## Workflow

### Step 1: Normalize and de-pack

Pretty-print the source and identify the obfuscation style (array-shuffle, eval-packer, charcode).
Decode static encodings first: hex/unicode escapes and base64 literals.

```bash
python scripts/analyst.py decode dropper.js
```

### Step 2: Unroll string arrays and char-code builds

Reconstruct strings built from arrays/`fromCharCode`/concatenation to reveal API names, URLs, and
commands.

### Step 3: Resolve eval/Function indirection — safely

Replace `eval`/`new Function` with logging (or a sandbox) so the constructed code is captured as
*data*, not executed, then recurse on the recovered layer.

### Step 4: Extract behavior and IOCs

Identify the dropper actions (WScript.Shell, ActiveX, fetch/XHR), recover URLs and dropped paths,
defang, and route payloads onward.

## Validation

- Static encodings (hex/unicode/base64) are fully decoded.
- String-array/charcode constructions are unrolled to readable strings.
- `eval`/`Function` layers are captured as data and recursed, with no untrusted execution.

## Pitfalls

- Running the script to "see what it does" and infecting the analysis host.
- Stopping at one layer when the dropper nests several.
- Missing environment-keyed branches (only acts on certain dates/locales) during static review.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the static JS decoder.
- ECMAScript spec and box-js (linked in frontmatter).
