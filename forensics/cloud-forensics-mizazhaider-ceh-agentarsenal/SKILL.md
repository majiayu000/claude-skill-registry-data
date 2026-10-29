---
name: cloud-forensics
description: Use when doing forensics in cloud environments on an
  authorized investigation. Covers log sources per provider, snapshot
  and disk acquisition, volatile evidence in ephemeral workloads, and
  timeline building from cloud audit trails. Also use when an on
  premises playbook meets its first cloud incident.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [forensics-fundamentals, incident-response, dfir-timeline]
tools:
  - name: Python
    version: "3.12"
---

Cloud forensics trades disk images for API calls: you collect logs,
snapshots, and configs instead of pulling drives. This skill covers
the method for authorized investigations: which log sources matter,
how to acquire evidence without destroying it, and how to build
timelines from audit trails. Work within the account you are
authorized to investigate and preserve chain of custody.

## Quick Workflow

1. Scope and preserve: identify the accounts, regions, and resources
   in scope; prevent log deletion and auto scaling from eating
   evidence.
2. Collect control plane logs: CloudTrail, Azure Activity, GCP Audit
   for the window.
3. Collect data plane evidence: snapshots of disks, memory where
   possible, and container logs.
4. Pull identity evidence: sign in logs, role assumptions, and key
   usage.
5. Build the timeline: merge the sources on UTC timestamps.
6. Analyze: what the attacker did, in order, with the API calls as
   proof.
7. Check for persistence: new users, keys, roles, and scheduled
   jobs.
8. Write the report with the evidence inventory.

## 1. AWS evidence collection (authorized account)

```bash
# CloudTrail: who did what, when (the backbone of cloud forensics)
aws cloudtrail lookup-events \
  --start-time 2026-10-20T00:00:00Z --end-time 2026-10-23T00:00:00Z \
  --max-results 1000 --output json > /tmp/ir_ct.json
python3 - << 'PY'
import json
ev = json.load(open("/tmp/ir_ct.json"))["Events"]
print("events:", len(ev))
from collections import Counter
print(Counter(e["EventName"] for e in ev).most_common(10))
PY
```

```bash
# Disk snapshot without touching the live instance
aws ec2 create-snapshot --volume-id vol-0abc123 \
  --description "forensic case 2026-10-23" --output json | head -10
# Share or copy the snapshot to the forensic account per the plan,
# then mount read only on an analysis instance
```

```bash
# GuardDuty and Config as corroborating sources
aws guardduty list-findings --detector-id $DET --output json | head -c 500
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name required-tags 2>/dev/null | head -c 300
```

## 2. Identity and timeline

```bash
# Who assumed what: role assumption chains in the window
python3 - << 'PY'
import json
ev = json.load(open("/tmp/ir_ct.json"))["Events"]
for e in ev:
    if e["EventName"] in ("AssumeRole", "GetSessionToken", "CreateAccessKey"):
        print(e["EventTime"], e["EventName"], e.get("Username"))
PY
```

```bash
# Merge into the timeline: convert each source to a common CSV
# ts,source,actor,action,resource,notes (UTC everywhere)
echo "ts,source,actor,action,resource" > /tmp/timeline.csv
python3 /tmp/ir/build_timeline.py >> /tmp/timeline.csv
sort -t, -k1 /tmp/timeline.csv | head -40
```

## Edge cases

- Logs were disabled or the trail is young. Note the gap; check
  provider level logs (AWS account level) and billing anomalies.
- Ephemeral workloads are gone. Container and function logs may
  remain; future defense is shipping logs off the host in real time.
- Multi account: the attacker pivoted. Collect from every account
  in the organization, not just the first.
- Legal hold vs cost: snapshots and log retention cost money;
  scope with counsel.

## Escalation

- Active attacker in the account: revoke keys and sessions first
  per the IR playbook, then continue collection.
- Evidence in another account or provider: expand scope formally;
  do not reach beyond authorization.
- Need the full timeline method: use dfir-timeline for the deep
  analysis pass.

## Detection and defender view

Cloud defenders detect with the same sources used for forensics:
CloudTrail alerts on unusual API calls, GuardDuty for known bad
patterns, and identity alerts on impossible travel. The forensic
readiness that matters: trails on in all regions, logs shipped to
an immutable bucket, and snapshots possible without the
investigator needing production admin. Most cloud investigations
fail on missing logs, not missing tools.

## Key references

- MITRE ATT&CK cloud matrix: technique to log source mapping.
- Provider forensics documentation (AWS, Azure, GCP).
- Related skills: forensics-fundamentals, dfir-timeline.
