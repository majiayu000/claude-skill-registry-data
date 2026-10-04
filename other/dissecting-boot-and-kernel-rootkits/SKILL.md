---
name: dissecting-boot-and-kernel-rootkits
description: 'Analyzes bootkit and rootkit samples by identifying boot-process tampering (MBR/VBR/
  UEFI), kernel-mode components, and stealth hooking techniques from static indicators. Activates
  for requests to analyze a bootkit or rootkit, examine MBR/UEFI tampering, or identify kernel-mode
  stealth components.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - bootkit
  - rootkit
  - kernel
  - firmware
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1542.003
  - T1014
  - T1547.006
d3fend:
  - D3-SDA
  - D3-FA
references:
  - 'MITRE ATT&CK T1542.003 Bootkit — https://attack.mitre.org/techniques/T1542/003/'
  - 'MITRE ATT&CK T1014 Rootkit — https://attack.mitre.org/techniques/T1014/'
---

# Dissecting Boot and Kernel Rootkits

## When to Use

- You have a sample (MBR/VBR image, UEFI module, or kernel driver) suspected of boot-process or
  kernel-level tampering and stealth.
- You need to identify the persistence vector and stealth technique class statically.

**Do not use** this on production firmware/boot media without acquisition — analyze a captured
image. The skill reads bytes statically and executes nothing.

## Prerequisites

- The boot image / UEFI module / driver (read inertly).

## Safety & Handling

- Read bytes statically; never write the sample to boot media or load the driver.

## Workflow

### Step 1: Classify the artifact

```bash
python scripts/analyst.py classify sample.bin
```

Detects MBR/VBR (boot signature `0x55AA` at 0x1FE), UEFI modules (PE with `EFI` subsystem / PI
GUIDs / `EFI_` strings), and kernel drivers (PE importing `ntoskrnl`/`hal`, `.sys` indicators).

### Step 2: Identify tampering / hooking indicators

Flag disk-write primitives (`Int 13h` for MBR bootkits), SSDT/IRP hooking and `Zw*`/`Ke*` kernel
APIs, DKOM strings, and driver-callback registration.

### Step 3: Map the persistence vector

Determine whether persistence is via MBR/VBR overwrite, UEFI variable/module, or driver service.

### Step 4: Document

Record the artifact type, persistence vector, and stealth technique class, mapping to ATT&CK.

## Validation

- The artifact type is identified by concrete signatures (boot signature, PE subsystem, imports).
- Tampering/hooking indicators reference real primitives, not generic strings.
- The persistence vector is stated with its evidence.

## Pitfalls

- A legitimate bootloader/driver resembling a bootkit/rootkit — corroborate with behavior.
- UEFI modules requiring firmware-volume parsing beyond simple PE checks.
- Kernel samples needing signed-driver and callback context to confirm stealth.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the classifier.
- ATT&CK T1542.003 and T1014 (linked in frontmatter).
