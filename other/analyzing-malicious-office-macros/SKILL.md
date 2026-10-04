---
name: analyzing-malicious-office-macros
description: 'Analyzes malicious Office documents by extracting and reviewing VBA macros and
  OLE/OOXML structure: auto-exec triggers, obfuscation, dropped payloads, and shell/PowerShell
  invocation. Activates for requests to analyze a malicious Word/Excel document, VBA macro, or
  maldoc.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - maldoc
  - vba
  - office
  - olevba
  - phishing
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1566.001
  - T1059.005
  - T1204.002
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'oletools (olevba) — https://github.com/decalage2/oletools'
  - 'MS-OVBA VBA file format — https://learn.microsoft.com/openspecs/office_file_formats/ms-ovba/'
---

# Analyzing Malicious Office Macros

## When to Use

- A Word/Excel/PowerPoint document is suspected of delivering malware via macros.
- You need to extract VBA, identify auto-exec triggers, and see what the macro does.
- You are determining the next-stage payload or URL a maldoc fetches.

**Do not use** the document's "Enable Content" path to analyze it — never open a maldoc in
Office. Extract and read the macro statically; detonate only in the isolated lab if needed.

## Prerequisites

- `oletools` (`pip install oletools`) for `olevba`/`oleid`, or the bundled OLE/OOXML extractor.
- The document in neutralized form inside the lab.

## Safety & Handling

- Do **not** open the document in Microsoft Office. Macros may auto-run on open/close.
- Static extraction only; if dynamic analysis is required, detonate in the isolated victim VM.

## Workflow

### Step 1: Identify the container and locate macros

OOXML (`.docm`, `.xlsm`) is a ZIP; legacy (`.doc`, `.xls`) is OLE2. Macros live in a
`vbaProject.bin` OLE stream. Extract it:

```bash
python scripts/analyst.py extract maldoc.docm
```

### Step 2: Flag auto-exec triggers

Look for entry points that run without user action beyond enabling macros:

```text
AutoOpen, Document_Open, AutoClose, Workbook_Open, Auto_Open, Document_Close
```

### Step 3: Find suspicious calls

Identify execution and download primitives:

```text
Shell, WScript.Shell, CreateObject, powershell, cmd /c
URLDownloadToFile, MSXML2.XMLHTTP, ADODB.Stream (drop to disk)
Environ, GetObject("winmgmts:") (WMI)
```

### Step 4: Deobfuscate

Maldocs commonly use Chr()/string concatenation, base64, and split-and-join. Resolve these to
recover the real command and any URL or dropped path.

### Step 5: Extract IOCs and the next stage

Pull URLs, dropped file paths, and the spawned command line. These become the report's IOCs
and pivot points.

## Validation

- The recovered command line and URL make sense together (download → drop → execute).
- Auto-exec triggers explain how the macro starts.
- Deobfuscated strings match what dynamic detonation would reveal (if you confirm in the lab).

## Pitfalls

- Opening the document in Office "just to see" — this executes the macro.
- Stopping at obfuscated source without resolving it; the IOCs are inside the obfuscation.
- Missing stomped VBA (p-code present, source removed) — check for VBA stomping and analyze
  p-code if the source looks empty.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the extractor and
  indicator scanner.
- oletools and MS-OVBA (linked in frontmatter).
