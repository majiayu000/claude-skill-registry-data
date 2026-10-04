---
name: hunting-scheduled-task-abuse
description: 'Hunts for malicious scheduled task persistence by analyzing task registration events
  (4698) and schtasks process creation for suspicious actions, triggers, and hidden tasks. Activates
  for requests to hunt scheduled task abuse, detect malicious schtasks usage, or find persistence
  via the Task Scheduler.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - scheduled-task
  - persistence
  - schtasks
  - sysmon
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1053.005
  - T1053
  - T1059
d3fend:
  - D3-PSA
  - D3-SYSM
car:
  - CAR-2013-08-001
references:
  - 'MITRE ATT&CK T1053.005 Scheduled Task — https://attack.mitre.org/techniques/T1053/005/'
  - 'Windows Security Event 4698 — https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4698'
---

# Hunting Scheduled Task Abuse

## When to Use

- You have task-registration events (4698) and/or `schtasks.exe`/`at.exe` process telemetry and
  want to detect persistence via malicious scheduled tasks.
- You are investigating tasks that run scripts, encoded commands, or binaries from suspicious paths.

**Do not use** this to alert on all task creation — administration creates tasks routinely. Hunt on
the action (script hosts, encoded commands, temp paths) and trigger context.

## Prerequisites

- Event ID 4698 (task registered) and/or process-creation telemetry for `schtasks`/`at`.

## Workflow

### Step 1: Hunt suspicious task actions

```bash
python scripts/analyst.py hunt events.csv
```

Flags tasks whose action runs `powershell -enc`, `mshta`, `wscript`/`cscript`, `cmd /c`, or
binaries from `%TEMP%`/`%APPDATA%`/`Public`, and `schtasks /create` command lines with the same.

### Step 2: Assess triggers and hiding

Note logon/onstart triggers, very frequent intervals, and tasks hidden via `Hidden` flag or SD
manipulation.

### Step 3: Confirm

Distinguish legitimate software tasks from intrusion by author, path, and action content.

### Step 4: Operationalize

Write a Sigma rule for task actions invoking script hosts or encoded commands.

## Validation

- Flags require a suspicious action/path, not task creation alone.
- `schtasks /create` and 4698 registrations are both covered.
- Findings map to ATT&CK T1053.005.

## Pitfalls

- Legitimate updater tasks (browsers, vendors) creating many tasks.
- Tasks created via direct XML drop bypassing `schtasks.exe` telemetry.
- Encoded commands hiding the true action.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1053.005 and Event 4698 docs (linked in frontmatter).
