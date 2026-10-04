---
name: hunting-suspicious-powershell-execution
description: 'Hunts malicious PowerShell using script-block (EID 4104) and module logging:
  scoring encoded commands, download cradles, AMSI/logging bypass, and in-memory execution,
  then decoding payloads for triage. Activates for requests to hunt malicious PowerShell,
  analyze script-block logs, or detect encoded command abuse.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - powershell
  - windows
  - script-block-logging
  - lolbin
  - detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059.001
  - T1027
  - T1562.001
d3fend:
  - D3-SBV
  - D3-DA
references:
  - 'PowerShell script block logging — https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_logging_windows'
  - 'MITRE ATT&CK T1059.001 PowerShell — https://attack.mitre.org/techniques/T1059/001/'
---

# Hunting Suspicious PowerShell Execution

## When to Use

- You have PowerShell script-block (Event ID 4104) and/or module logging and want to hunt abuse.
- You are testing a hypothesis that attackers use encoded commands, download cradles, or
  AMSI/logging bypasses.
- You need to score and decode a large volume of PowerShell events into a triage queue.

**Do not use** simple keyword blocklists as the sole method — admins legitimately use many of
the same cmdlets; score combinations and decode before judging.

## Prerequisites

- Script-block logging enabled (Event ID 4104) and exported to a queryable store.
- A baseline of normal administrative PowerShell for your environment.

## Workflow

### Step 1: Collect script-block events

Pull EID 4104 script-block text (and EID 4103 module logging) over the hunt window. Reassemble
multi-part script blocks before analysis.

### Step 2: Score suspicious constructs

Weight combinations rather than single keywords: `-EncodedCommand`, `IEX`/`Invoke-Expression`
with `Net.WebClient`/`Invoke-WebRequest`, `FromBase64String`, `-w hidden -nop`, AMSI strings,
and `[Ref].Assembly` reflection.

```bash
python scripts/analyst.py score events.json
```

### Step 3: Decode payloads

Base64-decode `-EncodedCommand` (UTF-16LE) and recover layered encodings to read the real
intent (download URLs, in-memory loaders).

### Step 4: Baseline and pivot

Compare against normal admin activity; for survivors, pull the parent process, user, host, and
network connections to confirm.

### Step 5: Confirm and operationalize

Validate true positives, escalate to IR, and convert the scoring logic into a detection rule.

## Validation

- High-score events decode to coherent malicious intent, not benign admin scripts.
- Multi-part script blocks are reassembled before scoring (no truncated false negatives).
- Confirmed cases tie to a parent process and user consistent with intrusion.

## Pitfalls

- Flagging single keywords (`IEX` alone) and drowning in admin noise.
- Forgetting `-EncodedCommand` is UTF-16LE, producing garbled decodes.
- Ignoring AMSI/logging-bypass attempts that precede the real payload.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scorer/decoder.
- Script-block logging docs and ATT&CK T1059.001 (linked in frontmatter).
