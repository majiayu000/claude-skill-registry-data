---
name: purple-team-automation
description: Purple team automation skill that links offensive emulation (Atomic Red Team, Caldera, Stratus Red Team, Leonidas) with detection validation, telemetry-gap analysis, and continuous control testing. Use to design adversary emulation plans tied to MITRE ATT&CK, execute safe tests in lab or controlled environments, and produce evidence-backed detection coverage reports.
---

# Purple Team Automation

## Authorization Boundary

- Run only in environments with written approval, change windows, and rollback owners.
- Tag every test with a unique `campaign-id` for cleanup and timeline reconstruction.
- No data destruction, no real credential theft, no third-party services targeted.

## Campaign Workflow

1. Pick an adversary or technique set with business relevance; cite ATT&CK IDs and known intrusion sets.
2. Draft an emulation plan: prerequisites, steps, expected telemetry, success/fail criteria, cleanup.
3. Execute with `invoke-atomicredteam`, `caldera` operations, `stratus`, or custom scripts in isolated runners.
4. Capture telemetry across EDR, Sysmon, cloud audit, network, identity, and SIEM.
5. Compare expected vs observed events; flag missing logs, parsing failures, and rule misses.
6. File defensive backlog: new detections, tuning, telemetry enablement, and response runbook updates.

## Coverage Scoring

- `Prevented`, `Alerted`, `Logged-not-alerted`, `Missed`. Score by technique and by data source.
- Track time-to-detect and time-to-contain per test.
- Maintain a heatmap over ATT&CK with last-validated date and confidence.

## Output Contract

- `plans/<campaign>.md`: technique list, steps, expectations.
- `runs/<campaign>/`: command logs, artifacts, screenshots, raw telemetry.
- `coverage.csv`: technique × status × evidence × backlog ticket.
- `report.md`: executive coverage, top gaps, prioritized fixes with owners.
