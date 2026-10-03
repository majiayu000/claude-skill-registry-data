---
name: malware-reverse-engineering
description: Malware reverse engineering and suspicious artifact analysis skill for defensive triage, static analysis, dynamic analysis planning, unpacking strategy, indicators of compromise, behavior summaries, YARA/Sigma ideas, and remediation guidance. Use for suspicious binaries, scripts, documents, logs, memory artifacts, sandbox reports, and malware family analysis in isolated environments.
---

# Malware Reverse Engineering

## Safety Boundary

- Treat samples as hostile. Use isolated labs, snapshots, no shared clipboard, no mounted personal directories, and controlled networking.
- Do not provide malware improvement, persistence, stealth, evasion, credential theft, or deployment guidance.
- Focus on behavior, indicators, detection, containment, and eradication.

## Workflow

1. Record sample metadata: filename, hashes, size, type, source, timestamp, and handling notes.
2. Perform static triage: strings, imports, sections, packer hints, scripts/macros, config blobs, and suspicious capabilities.
3. Plan dynamic analysis with containment: VM snapshot, fake services, monitored filesystem/registry/process/network activity.
4. Summarize behavior by capability: execution, persistence, privilege, defense evasion, discovery, C2, collection, exfiltration.
5. Produce IOCs, detection logic ideas, remediation steps, and confidence levels.

## Output Format

- `Summary`: what the artifact appears to do.
- `Evidence`: strings, APIs, paths, domains, mutexes, commands, or observed events.
- `IOCs`: hashes, filenames, registry keys, network indicators, and caveats.
- `Detections`: YARA/Sigma/EDR hunting ideas where appropriate.
- `Response`: containment, eradication, recovery, and monitoring.

