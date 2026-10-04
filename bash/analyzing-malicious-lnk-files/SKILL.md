---
name: analyzing-malicious-lnk-files
description: 'Analyzes weaponized Windows shortcut (.lnk) files: parsing the shell link structure
  for the target command, arguments, icon, and working directory, and recovering hidden
  PowerShell/cmd payloads and embedded content used in phishing. Activates for requests to
  analyze a malicious LNK, parse a shortcut file, or extract a command from a .lnk.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - lnk
  - shortcut
  - document-malware
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1204.002
  - T1059.001
  - T1059.003
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'Microsoft [MS-SHLLINK] Shell Link Binary File Format — https://learn.microsoft.com/openspecs/windows_protocols/ms-shllink/'
  - 'LNK forensic structure references — https://github.com/libyal/liblnk/blob/main/documentation/Windows%20Shortcut%20File%20(LNK)%20format.asciidoc'
---

# Analyzing Malicious LNK Files

## When to Use

- You have a `.lnk` delivered via phishing (often in an archive or ISO) and need its real action.
- You must recover the target command line, arguments, and any embedded/hidden payload.
- You are extracting IOCs (commands, URLs, file paths) from a shortcut.

**Do not use** Windows Explorer to inspect or double-click the shortcut — that executes its
target. Parse the binary structure statically.

## Prerequisites

- An LNK parser (Python `struct`, or `lnkparse`/`LECmd`); the sample handled inertly.

## Safety & Handling

- Never double-click or hover-load the shortcut in Explorer; parse raw bytes only.
- Defang recovered URLs and store any embedded payload password-protected.

## Workflow

### Step 1: Confirm and parse the header

Verify the LNK magic (`4C 00 00 00` + the link CLSID) and read `LinkFlags` to know which optional
structures are present.

```bash
python scripts/analyst.py parse sample.lnk
```

### Step 2: Recover the target and arguments

Extract the relative/local path and, crucially, the `COMMAND_LINE_ARGUMENTS` string — malicious
LNKs hide `powershell -enc ...` or `cmd /c ...` here.

### Step 3: Inspect icon and metadata

Read the icon location (often spoofed to look like a document) and metadata (machine ID,
timestamps) useful for attribution/clustering.

### Step 4: Find appended/embedded payloads

Check for data appended after the LNK structure (some campaigns embed scripts/binaries past the
parsed end) and extract it.

### Step 5: Decode and extract IOCs

Decode encoded commands (UTF-16LE base64), defang URLs, and route extracted payloads to the right
analysis workflow.

## Validation

- The full command line, including arguments, is recovered (not just the target path).
- Encoded commands are decoded to cleartext.
- Appended/embedded payloads are detected and extracted, and IOCs are defanged.

## Pitfalls

- Reading only the target path and missing the malicious arguments.
- Inspecting in Explorer and executing the shortcut.
- Ignoring data appended past the LNK structure.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the LNK parser.
- MS-SHLLINK and the liblnk format notes (linked in frontmatter).
