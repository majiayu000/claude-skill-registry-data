---
name: deobfuscating-malicious-powershell
description: 'Deobfuscates malicious PowerShell by decoding -EncodedCommand, reversing string
  and format obfuscation, resolving base64/gzip/IEX layers, and recovering the final payload
  and IOCs. Activates for requests to deobfuscate, decode, or analyze obfuscated PowerShell
  commands or scripts.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - powershell
  - deobfuscation
  - base64
  - script-analysis
  - windows
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.001
  - T1027
  - T1140
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'PowerShell about_PowerShell.exe -EncodedCommand — https://learn.microsoft.com/powershell/'
  - 'PSDecode — https://github.com/R3MRUM/PSDecode'
---

# Deobfuscating Malicious PowerShell

## When to Use

- You captured an obfuscated PowerShell command from a log, maldoc, or phishing payload.
- You need to recover the real intent: download URLs, dropped paths, shellcode, or next stage.
- You are unrolling layered encoding (base64 → gzip → IEX) to reach the final script.

**Do not use** `Invoke-Expression` or run the script to "see what it does" on a working host.
Decode statically; only execute in the isolated lab with logging if dynamic confirmation is
required.

## Prerequisites

- Python (bundled script handles base64/gzip/deflate and common transforms), or a sandbox.
- The command/script text captured as a string.

## Safety & Handling

- Never pipe attacker PowerShell into a live shell. Replace `IEX`/`Invoke-Expression` with
  output (print) when transforming.
- Treat decoded URLs/IPs as live; defang before sharing.

## Workflow

### Step 1: Decode -EncodedCommand

`-EncodedCommand` (`-enc`) is base64 of UTF-16LE. Decode it first:

```bash
python scripts/analyst.py decode --encodedcommand "<base64>"
```

### Step 2: Identify the obfuscation style

Common patterns:

```text
String reversal      : [array]::Reverse / -join with [-1..]
Format operator      : ("{1}{0}" -f 'b','a') -> 'ab'
Char codes           : [char]104 + [char]105
Concatenation/splits : 'po'+'wer'+'shell', -split / -replace tricks
Backtick/casing noise : I`E`X, iEx, &('i'+'ex')
```

### Step 3: Unroll encoding layers

Resolve nested `FromBase64String`, gzip/deflate (`IO.Compression`), and re-IEX layers until
you reach plain script. The script peels base64/gzip layers automatically.

```bash
python scripts/analyst.py deobfuscate payload.ps1
```

### Step 4: Neutralize execution sinks

Replace `IEX`, `Invoke-Expression`, `&`, and `.Invoke()` with a print so the recovered script
is rendered, not run.

### Step 5: Extract IOCs

Pull `DownloadString`/`DownloadFile` URLs, C2 hosts, dropped paths, and any embedded
base64 shellcode for separate analysis.

## Validation

- The fully decoded script is human-readable PowerShell with no remaining base64 blobs.
- Execution sinks are neutralized; nothing in your workflow actually ran the payload.
- Extracted URLs/paths are consistent with the script's logic.

## Pitfalls

- Running the script to decode it — the fastest way to get compromised.
- Stopping after one base64 layer when several are nested.
- Missing UTF-16LE vs UTF-8 when decoding `-enc` (it is UTF-16LE).
- Ignoring `-replace`/`-f` transforms that rebuild commands at runtime.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the decoder/deobfuscator.
- PowerShell encoded-command docs and PSDecode (linked in frontmatter).
