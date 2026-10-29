---
name: detection-as-code
description: Use when building detections as versioned, tested code.
  Covers Sigma rule authoring, detection pipelines, unit testing
  detections, and CI for the SOC. Also use when detection rules are
  scattered, untested, and nobody knows what they cover.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [sigma-rules, siem-detections, purple-team-exercises]
tools:
  - name: Python
    version: "3.12"
  - name: Git
    version: "2.47"
---

Detection as code treats SIEM rules like software: versioned,
reviewed, tested, and deployed through a pipeline. This skill covers
the practice: writing Sigma rules, testing them against labeled
data, and running the detection repo with CI. It turns tribal SOC
knowledge into an asset that survives turnover.

## Quick Workflow

1. Set up the detection repo: rules, tests, and docs in version
   control.
2. Write rules in Sigma with clear titles, ATT&CK tags, and false
   positive notes.
3. Add a test per rule: positive case (must fire) and negative
   cases (must not fire).
4. Run CI: validate syntax, run tests, and check coverage against
   your threat list.
5. Deploy through the pipeline: dev SIEM first, then production.
6. Monitor rule health: fire rates, false positives, and disabled
   rules.
7. Review on a schedule: every rule has an owner and a review date.
8. Retire rules that no longer fire or no longer matter.

## 1. Sigma rule with tests

```yaml
# detections/windows/credential_dump_lsass.yml
title: LSASS Memory Dump via Comsvcs
id: 8a7b6c5d-4e3f-2a1b-9c8d-7e6f5a4b3c2d
status: experimental
description: Detects rundll32 comsvcs.dll MiniDump of lsass
author: soc-team
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: '\rundll32.exe'
    CommandLine|contains:
      - 'comsvcs'
      - 'MiniDump'
  condition: selection
falsepositives:
  - Legitimate debugging (rare; verify with IT)
level: high
tags:
  - attack.credential_access
  - attack.t1003.001
```

```bash
# Test the rule: positive and negative event sets
mkdir -p tests/fixtures
# positive: the exact command line from a lab test (must fire)
# negative: normal rundll32 usage (must not fire)
python3 - << 'PY'
print("CI job: sigma validate + convert + run fixtures")
print("gate: all positives fire, all negatives silent, else the PR fails")
PY
```

## 2. Pipeline and health

```bash
# Repo layout:
# detections/        sigma rules by platform
# tests/fixtures/    labeled events per rule
# .ci/               validation and conversion jobs
# docs/coverage.md   ATT&CK coverage matrix, auto generated
git log --oneline -5 -- detections/ | head
```

```bash
# Rule health query (adapt to your SIEM):
# - rules with zero fires in 90 days: review or retire
# - rules with >1000 fires/day: tune or the SOC ignores them
# - rules disabled without a ticket: re enable or formally retire
echo "health review monthly; coverage review quarterly"
```

## Edge cases

- The SIEM does not support Sigma natively. Convert with
  sigmac/pySigma to the target query language in CI.
- Log sources are missing fields the rule needs. The rule documents
  its log requirements; missing logs are a data gap, not a rule
  bug.
- Tests pass but the rule misfires in production. Add the real
  false positive as a negative fixture and tune.

## Escalation

- Critical technique with no log source: escalate to logging
  architecture; you cannot detect what you do not collect.
- CI is blocked by flaky tests: fix the fixtures; untested
  detections are how gaps hide.

## Detection and defender view

Detection as code is the SOC growing up: every rule has an author,
a test, and a reason. Attackers do not care how you manage rules,
but the consistency shows in coverage: fewer gaps, faster tuning
after incidents, and a coverage matrix you can defend to
leadership. The durable habit is treating a detection change like
a code change, because it is one.

## Key references

- Sigma specification and pySigma documentation.
- MITRE ATT&CK: coverage mapping.
- Related skills: sigma-rules, siem-detections.
