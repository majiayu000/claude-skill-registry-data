---
name: analyzing-malicious-vbscript-and-wsf
description: 'Analyzes malicious VBScript, WSF, and HTA scripts: parsing WSF/HTA containers,
  decoding VBScript.Encode (#@~^) and string obfuscation, and identifying WScript.Shell/ActiveX
  abuse to recover dropper behavior. Activates for requests to analyze VBScript, decode a WSF/HTA,
  or investigate a Windows Script Host dropper.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - vbscript
  - wsf
  - hta
  - document-malware
  - deobfuscation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.005
  - T1059.003
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'Microsoft Windows Script Host documentation — https://learn.microsoft.com/previous-versions/windows/internet-explorer/ie-developer/scripting-articles/'
  - 'VBScript.Encode / Script Encoder format analysis — https://gist.github.com/bcse/1834878'
---

# Analyzing Malicious VBScript and WSF

## When to Use

- You have a `.vbs`, `.wsf`, or `.hta` delivered via phishing and need its real behavior.
- You must decode `VBScript.Encode`-obfuscated script (the `#@~^` marker) or string obfuscation.
- You are identifying WScript.Shell/ActiveX-based dropper actions and IOCs.

**Do not use** `wscript`/`cscript`/`mshta` to run the script for analysis — that executes the
dropper. Decode and read it statically.

## Prerequisites

- A static decoder (Python) or a script sandbox; the sample handled inertly in the lab.

## Safety & Handling

- Never run the script with Windows Script Host (`wscript`/`cscript`/`mshta`).
- Defang recovered URLs; store dropped payloads password-protected.

## Workflow

### Step 1: Parse the container

For WSF, parse the XML `<job>`/`<script>` elements (a WSF can bundle multiple languages). For HTA,
separate the HTML wrapper from the `<script>` body.

```bash
python scripts/analyst.py analyze sample.wsf
```

### Step 2: Decode VBScript.Encode

If you see the `#@~^` header, decode the Microsoft Script Encoder stream back to source.

### Step 3: Unroll string obfuscation

Resolve `Chr()`/`Asc()` builds, string concatenation, and `Replace()`-based deobfuscators to
reveal commands and URLs.

### Step 4: Identify dropper actions and IOCs

Find `CreateObject("WScript.Shell")`, `Run`/`Exec`, ADODB/MSXML download patterns, and PowerShell
hand-offs; recover URLs/paths, defang, and route payloads onward.

## Validation

- WSF/HTA containers are decomposed into their script bodies (all jobs/languages).
- `VBScript.Encode` streams are decoded to readable source.
- Dropper actions and IOCs are recovered without executing the script.

## Pitfalls

- Executing with `wscript`/`mshta` to "see" behavior, infecting the host.
- Missing one `<script>` block in a multi-job WSF.
- Overlooking the `#@~^` encoded section and analyzing only the cleartext stub.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the WSF/VBScript decoder.
- Windows Script Host docs and the Script Encoder format (linked in frontmatter).
