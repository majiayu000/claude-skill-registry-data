---
name: sigma-rules
description: Use when writing, converting, or testing Sigma detection rules
  for a defensive detection program. Covers Sigma rule structure, logsource
  taxonomy, detection selection syntax, modifiers, conditions, testing with
  the Sigma CLI, and converting one rule to Splunk SPL, Elastic, and other
  backends. Use when the team needs vendor-neutral detections that run on
  more than one SIEM, or when contributing rules to a shared detection repo.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [siem-detections, incident-response]
tools:
  - name: Sigma
    version: "2.0"
  - name: Python
    version: "3.12"
---

Sigma is an open, vendor-neutral format for writing detection rules. You
write the logic once in YAML, then convert it to Splunk SPL, Elastic
queries, Microsoft Sentinel KQL, and other backends. This skill covers
writing correct Sigma rules, using the logsource taxonomy, testing rules
locally, and converting them for deployment. It is defensive work for
your own or a client-authorized detection program.

## Quick Workflow

1. Pick one MITRE technique and one log source, and write the smallest
   rule that detects it.
2. Fill in the logsource taxonomy (product, category, service) so the
   rule routes to the right backend query.
3. Write the detection selection with explicit field names and modifiers,
   then a condition that combines selections.
4. Add metadata: title, id (UUID), status, level, tags with attack IDs,
   author, date, and a false positives section.
5. Validate the YAML and the rule schema with the Sigma CLI.
6. Convert to each target backend and run the output against real data.
7. Test with 30 days of history, tune, then commit the rule to the
   detection repo with a review.

## 1. Rule anatomy

Every Sigma rule has the same skeleton. Learn it once.

```yaml
title: Suspicious Rundll32 Execution Without CPL
id: 7c9e8a2b-4f1d-4a3e-9b5c-2d6f7a8b9c0d
status: test
description: Detects rundll32.exe executed without a .cpl argument, which
  deviates from common legitimate use and matches T1218.011 proxy execution.
author: SOC Detection Team
date: 2026/10/23
modified: 2026/10/23
references:
  - https://attack.mitre.org/techniques/T1218/011/
tags:
  - attack.execution
  - attack.t1218.011
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image|endswith: '\rundll32.exe'
  filter:
    CommandLine|contains: '.cpl'
  condition: selection and not filter
falsepositives:
  - Legitimate software installers that call rundll32 directly
  - Administrative scripts using rundll32 for control panel items
level: medium
```

Required habits: a stable UUID `id`, a `status` of experimental, test, or
stable, and a `level` of informational, low, medium, high, or critical.

## 2. Logsource taxonomy

The logsource tells converters which backend index and sourcetype to
query. Common values:

```yaml
# Windows process creation (Sysmon Event ID 1 or Security 4688)
logsource:
  product: windows
  category: process_creation

# Windows registry events (Sysmon 12, 13, 14)
logsource:
  product: windows
  category: registry_event

# Windows network connections (Sysmon 3, firewall logs)
logsource:
  product: windows
  category: network_connection

# Web proxy logs
logsource:
  category: proxy

# Linux auditd
logsource:
  product: linux
  category: process_creation
  service: auditd

# Specific Windows service log
logsource:
  product: windows
  service: security
```

If the logsource is wrong, the converter emits a query against the wrong
index and the rule silently matches nothing. Verify the mapping for each
backend you deploy to.

## 3. Detection selections

The `detection` block holds named selections and one `condition`.

```yaml
detection:
  selection_img:
    Image|endswith:
      - '\powershell.exe'
      - '\pwsh.exe'
  selection_cli:
    CommandLine|contains:
      - ' -enc '
      - ' -EncodedCommand '
      - 'FromBase64String'
      - 'IEX'
  filter_admin:
    User|contains: 'svc-backup'
  condition: selection_img and selection_cli and not filter_admin
```

Modifiers you will use constantly:

| Modifier | Meaning | Example |
|---|---|---|
| `\|contains` | substring match | `CommandLine\|contains: 'mimikatz'` |
| `\|startswith` | prefix match | `Image\|startswith: 'C:\Windows\System32\'` |
| `\|endswith` | suffix match | `Image\|endswith: '\rundll32.exe'` |
| `\|re` | regex match | `CommandLine\|re: 'sleep\s+\d+'` |
| `\|windash` | match `-`, `/`, `--` variants | `CommandLine\|windash: '-enc'` |
| `\|cidr` | IP in range | `DestinationIp\|cidr: '10.0.0.0/8'` |
| `\|base64` | match base64 of value | `CommandLine\|base64: 'powershell'` |
| `\|base64offset` | base64 with offsets | for encoded payloads |

Value lists are ORed automatically. Selections combined with `and`
narrow; `1 of selection_*` means any one matches; `all of selection_*`
means every selection must match.

## 4. Conditions and aggregations

Conditions support boolean logic plus aggregation functions for
threshold rules.

```yaml
detection:
  selection:
    EventID: 4625
  timeframe: 10m
  condition: selection | count(TargetUserName) by SourceIp > 20
```

More examples:

```yaml
# Near: two selections within a time window
condition: selection_a and selection_b | near selection_a selection_b within 5m

# Count distinct values
detection:
  selection:
    EventID: 4625
  timeframe: 1h
  condition: selection | count(TargetUserName) by IpAddress > 10

# Sum a numeric field
condition: selection | sum(bytes_out) by src_ip > 1073741824
```

Keep thresholds in the rule metadata or a comment so tuners know why
the number was chosen.

## 5. Correlations (Sigma 2.0)

Sigma 2.0 adds a `correlation` block for multi-event rules.

```yaml
title: Possible Lateral Movement Chain
id: 1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d
status: experimental
correlation:
  type: event_count
  rules:
    - d3c4e5f6-7a8b-4c5d-9e0f-1a2b3c4d5e6f  # SMB lateral movement rule id
    - e4f5a6b7-8c9d-4e5f-0a1b-2c3d4e5f6a7b  # new service creation rule id
  group-by:
    - ComputerName
  timespan: 30m
  condition:
    gte: 2
level: high
```

Correlation types: `event_count`, `value_count`, `temporal` (ordered
sequences), and `temporal_ordered`. Use them for chains like initial
access followed by persistence on the same host.

## 6. Testing with the Sigma CLI

Install the Sigma toolchain (Python 3.12, stdlib plus the sigma
packages) and validate before converting.

```bash
# Validate rule syntax and schema
sigma check rules/windows/process_creation/proc_creation_win_rundll32_suspicious.yml

# List supported backends and pipelines
sigma list-backends
sigma list-pipelines

# Convert to Splunk SPL
sigma convert -t splunk \
  -p splunk_windows \
  rules/windows/process_creation/proc_creation_win_rundll32_suspicious.yml

# Convert to Elastic (Lucene / ES|QL)
sigma convert -t elasticsearch \
  -p ecs_windows \
  rules/windows/process_creation/proc_creation_win_rundll32_suspicious.yml

# Convert to Microsoft Sentinel (KQL)
sigma convert -t microsoft365defender \
  rules/windows/process_creation/proc_creation_win_rundll32_suspicious.yml
```

Always read the generated query. Converters are good but not perfect:
check that wildcards landed in the right place and that field names
match your normalized schema.

## 7. Writing high-signal rules

Patterns that separate good rules from noisy ones:

- Anchor on rare combinations, not single common events. Process
  creation alone is noise; process creation plus an encoded command line
  plus a first-seen hash is a signal.
- Prefer `category: process_creation` over raw Security 4688 when
  Sysmon is deployed, because Sysmon gives parent process and hashes.
- Use `OriginalFileName` from Sysmon to catch renamed LOLBins:
  `OriginalFileName: 'RUNDLL32.EXE'` catches the renamed copy.
- For logon rules, filter service and computer accounts (`$` suffix)
  unless you are specifically hunting them.
- Put every exclusion in a named `filter_*` selection with a comment
  explaining the business reason.

Example: encoded PowerShell (T1059.001).

```yaml
title: Encoded PowerShell Command Line
id: 9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d
status: stable
description: Detects PowerShell started with an encoded command argument,
  a common obfuscation technique.
author: SOC Detection Team
date: 2026/10/23
tags:
  - attack.execution
  - attack.t1059.001
logsource:
  product: windows
  category: process_creation
detection:
  selection_img:
    Image|endswith:
      - '\powershell.exe'
      - '\pwsh.exe'
  selection_cli:
    CommandLine|contains|windash:
      - 'enc'
      - 'EncodedCommand'
  filter_local_admin_scripts:
    # Approved admin tooling, ticket SOC-4821, review 2027-01-15
    ParentImage|endswith: '\admin-tool.exe'
  condition: selection_img and selection_cli and not filter_local_admin_scripts
falsepositives:
  - Admin automation that encodes commands for quoting reasons
level: high
```

## Edge cases

- Field name mismatch: your SIEM calls it `CommandLine` but the
  pipeline maps to `process.command_line`. Test the converted query,
  not just the YAML.
- Case sensitivity in `|contains` depends on the backend. Splunk is
  case-insensitive by default; Elastic keyword fields are not. Add both
  cases or lowercase at ingest.
- Backslash escaping in YAML: single-quoted strings keep backslashes
  literal, double-quoted strings interpret them. Prefer single quotes
  for Windows paths.
- Very long value lists slow down some backends. Split lists over 50
  values into multiple selections or a lookup.
- `timeframe` aggregation rules need the backend to support the
  aggregation. Verify the converted Splunk uses `bin` and `stats`
  correctly.
- Rule `id` collisions when copying rules: always generate a fresh UUID
  for a new rule, never reuse one from a copied file.
- Sigma 1.x rules use `aggregation` keys that changed in 2.0. Check the
  spec version at the top of any rule you import.

## Escalation

- The converted query returns nothing: check the logsource mapping,
  then run the backend query by hand with the filters removed one at a
  time to find the failing clause.
- The converter does not support your backend: write the backend query
  manually from the Sigma logic and note the gap; consider contributing
  the backend mapping upstream.
- Too many false positives after deployment: demote `status` back to
  test, add filters with ticket references, and re-validate before
  promoting to stable again.
- You need a rule for a log source with no Sigma taxonomy entry: use
  the closest generic `category` and document the mapping in the rule
  comments so the next converter run does not silently drop it.
- Conflicting community rules: keep upstream SigmaHQ rules unmodified
  in a vendor directory and put your overrides in a local directory so
  updates do not clobber your tuning.

## Detection and defender view

Sigma is a force multiplier for defenders, and attackers know the
popular public rules, so assume evasion:

- Attackers obfuscate command lines to dodge `|contains` matches.
  Pair string rules with behavior rules (parent-child anomalies, first-
  seen hashes) that do not depend on exact strings.
- Attackers live off the land with signed binaries that public Sigma
  rules allowlist. Write environment-specific rules for the LOLBins
  your users actually run.
- Public Sigma rules are tuned for generality and can be noisy in your
  environment. Fork, add local filters, and track your fork's precision
  separately from upstream.
- Tune by measuring: keep a per-rule true positive log, review monthly,
  and retire rules that never fire true positives. A dead rule is
  maintenance debt, not coverage.
- Version every rule in git. When an incident review asks "did we have
  a rule for this", the git history is the answer.

## Key references

- Sigma specification 2.0: https://github.com/SigmaHQ/sigma-specification
- SigmaHQ rule repository: https://github.com/SigmaHQ/sigma
- pySigma documentation: https://github.com/pySigma/pySigma
- MITRE ATT&CK T1218.011 (Rundll32), T1059.001 (PowerShell),
  T1110 (Brute Force), T1070.001 (Clear Windows Event Logs).
- Sigma CLI (pysigma) usage: https://github.com/pySigma/pySigma-cli
