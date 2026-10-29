---
name: threat-hunting
description: Use when proactively hunting for undetected intruders in an
  environment you are authorized to defend. Covers hypothesis-driven
  hunting, building hunts from MITRE ATT&CK techniques and threat intel,
  data sources and collection windows, frequency and stacking analysis,
  first-seen and rare-event hunting, documenting findings, and turning a
  successful hunt into a permanent detection. Use when alerts are quiet
  but risk is high, after a threat intel report, or on a recurring hunt
  schedule.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [incident-response, forensics-fundamentals]
tools:
  - name: Velociraptor
    version: "0.72"
  - name: Sysmon
    version: 15.x
  - name: Python
    version: "3.12"
---

Threat hunting is the proactive search for attackers who slipped past
automated detections. Unlike alert triage, which reacts to fired rules,
hunting starts from a hypothesis ("an intruder would do X, and it would
look like Y in our logs") and tests it against historical data. This
skill covers hypothesis-driven hunts on infrastructure you are
authorized to defend, using Sysmon, EDR, and SIEM telemetry.

## Quick Workflow

1. Write the hypothesis in one sentence, tied to a MITRE technique and
   an expected log artifact.
2. Define the data source, the time window (usually 30 to 90 days), and
   the scope (which hosts or users).
3. Collect a baseline of normal behavior for the artifact first.
4. Run the hunt query and stack the results (group by rare values).
5. Investigate every outlier: process tree, parent, user, network, hash.
6. Document the hunt: hypothesis, query, time window, findings, verdict.
7. If you find evil, escalate to incident response immediately and
   preserve the evidence.
8. If the hunt works, convert it into a permanent detection rule.

## 1. Writing a hypothesis

A good hypothesis is falsifiable and specific. Bad: "look for malware."
Good examples:

- "Attackers using WMI for lateral movement (T1047) will spawn
  powershell.exe from wmiprvse.exe, which our admins rarely do."
- "A Kerberoasting attack (T1558.003) produces Event ID 4769 with
  ticket encryption type 0x17 and no pre-authentication, clustered in
  a short window from one account."
- "Ransomware staging (T1486) creates many file rename events with
  unusual extensions in user document folders within minutes."

Record for each hunt: hypothesis, MITRE technique, data source, time
window, analyst, date, and verdict (confirmed benign, confirmed evil,
inconclusive).

## 2. Baseline first

Never hunt without knowing normal. Pull 30 days of the artifact and
find the common values so rare ones stand out.

```bash
# Splunk: baseline of parent -> child process pairs over 30 days
index=wineventlog EventCode=1 earliest=-30d@d latest=@d
| eval parent=lower(mvindex(split(ParentImage,"\\"),-1)),
       child=lower(mvindex(split(Image,"\\"),-1))
| stats count by parent, child
| sort -count | head -50
```

```bash
# Baseline: which users run PowerShell with encoded args normally
index=wineventlog EventCode=1 Image="*powershell.exe"
  CommandLine="*-enc*" earliest=-30d@d latest=@d
| stats count by user | sort -count
```

If the baseline shows your admin tooling does the "suspicious" thing
daily, note it as a known-good pattern before you start flagging hosts.

## 3. Stacking and frequency analysis

Stacking groups events by a field and sorts by rarity. The rarest items
are investigated first.

```bash
# Stack: rare parent-child process pairs (hunt for odd execution chains)
index=wineventlog EventCode=1 earliest=-30d@d latest=@d
| eval parent=lower(mvindex(split(ParentImage,"\\"),-1)),
       child=lower(mvindex(split(Image,"\\"),-1))
| stats dc(ComputerName) as host_count count as total by parent, child
| where host_count <= 3
| sort host_count, total

# Stack: rare command lines for common binaries
index=wineventlog EventCode=1 Image="*\\rundll32.exe" earliest=-30d@d latest=@d
| stats dc(ComputerName) as hosts values(CommandLine) as examples by CommandLine
| where hosts <= 2

# Frequency analysis: users with first-seen external IPs in proxy logs
index=proxy earliest=-30d@d latest=@d
| stats earliest(_time) as first_seen by user, dest_ip
| where first_seen > relative_time(now(), "-7d@d")
```

In Elastic, the equivalent is a terms aggregation sorted by count
ascending, filtered to low document counts.

## 4. First-seen and rare-event hunts

New things in an environment deserve suspicion. Hunt for first-seen
hashes, first-seen services, and first-seen scheduled tasks.

```bash
# First-seen SHA256 per host over 90 days, show only the newest
index=wineventlog EventCode=1 earliest=-90d@d latest=@d
| eval sha=lower(Hashes)
| stats earliest(_time) as first_seen values(Image) as path
        values(ComputerName) as host by sha
| where first_seen > relative_time(now(), "-7d@d")
| sort first_seen
```

```bash
# Rare services created (Event ID 7045), first seen this week
index=wineventlog EventCode=7045 earliest=-90d@d latest=@d
| stats earliest(_time) as first_seen values(ServiceName) as svc
        values(ImagePath) as path by ComputerName
| where first_seen > relative_time(now(), "-7d@d")
```

```bash
# Scheduled tasks created outside business hours (T1053.005)
index=wineventlog EventCode=4698 earliest=-30d@d latest=@d
| eval hour=strftime(_time,"%H"), dow=strftime(_time,"%A")
| where hour < 7 OR hour > 19 OR dow="Saturday" OR dow="Sunday"
```

## 5. Hunt patterns by MITRE technique

Keep a library of hunt queries mapped to techniques:

Credential access:

```bash
# LSASS access by non-system processes (T1003.001)
index=wineventlog EventCode=10 TargetImage="*\\lsass.exe" earliest=-30d@d latest=@d
| eval src=lower(mvindex(split(SourceImage,"\\"),-1))
| where NOT src IN ("csrss.exe","wininit.exe","services.exe","lsass.exe")
| stats values(src) as processes values(ComputerName) as hosts by GrantedAccess
```

Defense evasion:

```bash
# Event log cleared (T1070.001)
index=wineventlog EventCode=1102 earliest=-90d@d latest=@d

# Sysmon config tampered or service stopped
index=wineventlog (EventCode=7040 OR EventCode=7036) ServiceName="*Sysmon*"
  earliest=-30d@d latest=@d
```

Discovery:

```bash
# Account discovery bursts: many 4798/4799 or net user calls (T1087)
index=wineventlog EventCode=1 Image="*\\net*.exe" CommandLine="* user*"
  earliest=-14d@d latest=@d
| bin _time span=1h | stats dc(ComputerName) as hosts count as n by _time
| where n > 20
```

Lateral movement:

```bash
# WMI spawning processes remotely (T1047): wmiprvse as parent of cmd/powershell
index=wineventlog EventCode=1 ParentImage="*\\wmiprvse.exe"
  earliest=-30d@d latest=@d
| eval child=lower(mvindex(split(Image,"\\"),-1))
| where child IN ("powershell.exe","cmd.exe","pwsh.exe")
| table _time, ComputerName, user, Image, CommandLine
```

## 6. Hunting with Velociraptor

For host-level hunts across the fleet, Velociraptor artifacts beat SIEM
when you need live filesystem or memory state.

```bash
# List available hunt artifacts
velociraptor --config server.config.yaml query "SELECT name FROM artifact_definitions() LIMIT 20"

# Hunt: collect recent prefetch files across all Windows hosts
velociraptor --config server.config.yaml query "
SELECT * FROM hunt_add(
  hunt_description='Prefetch collection for execution timeline',
  artifact='Windows.Forensics.Prefetch')"

# Query process trees on one client for the last 7 days
velociraptor --config server.config.yaml query "
SELECT * FROM Artifact.Windows.Forensics.ProcessInfo(client_id='C.1234')"
```

Use Velociraptor when the SIEM lacks the data (prefetch, amcache,
USN journal, memory) and the SIEM when you need long retention and
correlation across sources.

## 7. Documenting the hunt

Every hunt produces a record, even when it finds nothing. Template:

```text
Hunt ID: HUNT-2026-104
Hypothesis: Attackers dump LSASS with renamed tools; Sysmon Event ID 10
  to lsass.exe from unusual source images indicates T1003.001.
Technique: T1003.001
Data source: Sysmon Event ID 10, 90 days, all Windows hosts
Query: <paste exact query>
Baseline: csrss, wininit, services are the only normal sources
Findings: 3 hosts with rundll32.exe accessing LSASS, all traced to
  the approved EDR sensor (ticket SOC-5100)
Verdict: benign, known-good pattern added to baseline
Follow-up: none; detection rule sigma-lsass-access already covers this
```

Store hunt records next to detection rules in git. A future analyst
should be able to rerun the hunt from the record alone.

## 8. From hunt to detection

A hunt that finds evil, or that reliably surfaces suspicious outliers,
becomes a rule:

1. Take the hunt query and add the exclusions you learned during the
   hunt.
2. Write it as a Sigma rule (see the sigma-rules skill) so it converts
   to every backend.
3. Backtest 30 days, check precision, deploy in shadow mode for a week.
4. Link the detection back to the hunt record for provenance.

## Edge cases

- Log retention is shorter than your hunt window. Check the oldest
  event per source first; a 90 day hunt on 30 days of data gives false
  confidence.
- Daylight saving shifts break hourly binning. Hunt in UTC and convert
  to local time only for display.
- Hosts that were reimaged reset first-seen baselines. Exclude rebuild
  dates from first-seen hunts or you will chase ghosts.
- Admin tooling mimics attacker behavior (PsExec looks like lateral
  movement). Maintain an approved-tooling list with hashes and owning
  teams.
- Encrypted traffic hides payloads. Hunt on metadata: JA3 fingerprints,
  certificate fields, beaconing intervals, byte ratios.
- Hunts over huge data sets time out. Narrow by host group, split the
  window into weekly chunks, and use summary indexes for repeated hunts.

## Escalation

- A hunt finds active evil: stop hunting, start incident response.
  Preserve volatile data (memory, logs) before containment changes it.
- The data you need was never collected: file a logging gap ticket,
  deploy the collection (Sysmon config change, new forwarder), and note
  the blind window in the hunt record.
- Queries time out on the full fleet: sample hosts by risk tier
  (servers and admin workstations first), then expand.
- The hypothesis is inconclusive after full effort: record it as
  inconclusive with the exact limits hit, and schedule a re-hunt when
  new intel or new data arrives.
- Stakeholders ask "are we compromised": answer with the hunts run,
  their coverage, and their verdicts. Never claim "clean", only
  "no evidence found in the data and windows tested".

## Detection and defender view

Hunting is the defender's answer to detection gaps, so think like the
attacker you are trying to catch:

- Attackers study public Sigma rules and avoid their exact strings.
  Hunt on behavior (parent-child pairs, timing, rarity), which is
  harder to evade than string matches.
- Attackers use valid credentials, so authentication logs look normal.
  Hunt for second-order anomalies: new device, new ASN, impossible
  travel, dormant account reactivation.
- Attackers slow down to dodge thresholds. Hunt with long windows (90
  days) and low counts, not just the SIEM's 15 minute alert window.
- Attackers clear logs on the host. Hunt from centralized, tamper-
  resistant copies and alert on ingestion gaps per host.
- When a hunt technique becomes public, attackers adapt. Rotate hunt
  focus quarterly and keep some hunts unshared outside the team.

## Key references

- MITRE ATT&CK T1003.001 (LSASS Memory), T1047 (WMI), T1558.003
  (Kerberoasting), T1486 (Data Encrypted for Impact), T1070.001 (Clear
  Windows Event Logs), T1053.005 (Scheduled Task), T1087 (Account
  Discovery).
- "The Threat Hunting Pyramid of Pain" and TaHiTI methodology
  (ENISA / Dutch NCSC hunting references).
- Velociraptor documentation: https://docs.velociraptor.app/
- MITRE ATT&CK matrix: https://attack.mitre.org/
- SANS FOR508 / SEC511 hunting concepts (course references).
