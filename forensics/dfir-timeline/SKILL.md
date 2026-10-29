---
name: dfir-timeline
description: Use when building a forensic timeline for an authorized
  investigation. Covers evidence source collection, timestamp
  normalization, super timeline creation with Plaso, and analyzing the
  merged timeline for attacker activity. Also use when multiple
  evidence sources need one coherent story.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [forensics-fundamentals, log-forensics, incident-response, cloud-forensics]
tools:
  - name: Python
    version: "3.12"
---

A timeline turns scattered evidence into the attacker's story: every
event on one axis, in order, in UTC. This skill covers the method for
authorized investigations: collecting the sources, normalizing time,
building a super timeline, and reading it for the intrusion. Work on
evidence you are authorized to handle, with chain of custody.

## Quick Workflow

1. Inventory evidence sources: disk images, memory, logs, and cloud
   trails, with their time zones.
2. Verify time: check each source's clock accuracy and skew before
   merging.
3. Build per source timelines first; understand each before merging.
4. Merge into a super timeline in UTC with a common schema.
5. Filter to the incident window, then expand as the story needs.
6. Tag events: attacker, system, user, and unknown, with confidence.
7. Find the gaps: missing logs are findings too.
8. Write the narrative with timestamps as the evidence.

## 1. Collection and normalization

```bash
# Inventory with hashes and time zones (chain of custody)
sha256sum /evidence/disk.img /evidence/memory.raw > /tmp/tl/hashes.txt
# Record: source, acquisition time, stated time zone, clock notes
cat > /tmp/tl/sources.csv << 'CSV'
source,path,timezone,notes
disk_image,/evidence/disk.img,Europe/Brussels,system clock
auth_logs,/evidence/auth.log,UTC,syslog
cloudtrail,/evidence/ct.json,UTC,provider time
CSV
```

```bash
# Per source extraction: filesystem timeline from the disk image
fls -r -m / -z Europe/Brussels /evidence/disk.img > /tmp/tl/bodyfile.txt
# Normalize everything to UTC at merge time; never mix zones in analysis
python3 - << 'PY'
from datetime import datetime
from zoneinfo import ZoneInfo
local = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo("Europe/Brussels"))
print("UTC:", local.astimezone(ZoneInfo("UTC")).isoformat())
PY
```

## 2. Super timeline with Plaso

```bash
# Build the super timeline (Plaso as investigation tooling)
log2timeline.py --storage-file /tmp/tl/case.plaso /evidence/disk.img
pinfo.py /tmp/tl/case.plaso | head -20
# Export to CSV for analysis
psort.py -o csv -w /tmp/tl/super.csv /tmp/tl/case.plaso
wc -l /tmp/tl/super.csv
```

```bash
# Merge cloud and log sources into the same schema
# ts_utc, source, host, user, event, details
python3 - << 'PY'
print("merge: disk timeline + auth logs + cloudtrail into timeline.csv")
print("sort by ts_utc; dedupe; then filter to the incident window")
PY
# Analyze: sort, filter, and pivot
awk -F, '$1 >= "2026-10-22T12:00:00" && $1 <= "2026-10-22T18:00:00"' \
  /tmp/tl/timeline.csv | head -50
```

## 3. Reading the timeline

```bash
# Patterns to hunt in the merged timeline:
# - first attacker event (initial access) and how it got there
# - privilege escalation markers close together in time
# - lateral movement: same credentials on multiple hosts
# - staging and exfiltration: large reads then outbound flows
# - anti forensics: log clears, timestomping (check $STANDARD_INFORMATION vs $FILE_NAME)
grep -i -E "mimikatz|psexec|wmic|ntdsutil|vssadmin.*delete" /tmp/tl/timeline.csv | head -20
```

## Edge cases

- Clocks disagree by minutes or hours. Establish skew per source
  and annotate; do not silently shift.
- Timestomping suspected. Compare filesystem timestamps against
  journal and log evidence; disagreement is the tell.
- The timeline is millions of rows. Filter aggressively by window
  and host, then expand outward from known bad events.
- Time zones in cloud logs are UTC but the endpoint is local.
  Normalize at ingest, document the mapping.

## Escalation

- Gaps in the timeline: identify which sources are missing and
  whether they can still be collected.
- Need memory context: add the memory timeline (process creation)
  from the memory image.
- Scale problems: move to a proper analysis platform; CSV works to
  a point.

## Detection and defender view

Timelines are built after the fact, but the readiness that enables
them is defensive: NTP everywhere, centralized logging with
retention, and protected audit logs. Attackers fight timelines with
clock changes, log deletion, and timestomping, which is why
independent sources (network, cloud) matter. The durable practice
is forensic readiness: the logs you need are the logs you already
collect.

## Key references

- Plaso (log2timeline) documentation.
- MITRE ATT&CK T1070 (Indicator Removal): anti forensics.
- NIST SP 800-86: integrating forensic techniques.
