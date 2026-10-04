---
name: building-a-threat-hunt-hypothesis
description: 'Frames a structured, testable threat-hunting hypothesis: grounding it in adversary
  behavior and available telemetry, defining the data sources and detection logic, and setting
  success criteria and outcomes. Activates for requests to start a threat hunt, write a hunt
  hypothesis, or plan a hypothesis-driven hunt.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - hypothesis
  - methodology
  - mitre-attack
  - planning
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
d3fend:
  - D3-DA
references:
  - 'MITRE ATT&CK — https://attack.mitre.org/'
  - 'The PEAK Threat Hunting Framework (Splunk) — https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html'
---

# Building a Threat-Hunt Hypothesis

## When to Use

- You are starting a proactive, hypothesis-driven hunt rather than responding to an alert.
- You need to turn a vague concern ("are we seeing living-off-the-land abuse?") into a testable,
  scoped statement with clear data requirements.
- You want a repeatable plan that produces either a detection, a gap, or a confident negative.

**Do not use** this as an incident-response trigger — if you already have a confirmed alert,
pivot to investigation/IR, not hypothesis generation.

## Prerequisites

- Knowledge of your environment's telemetry (EDR, Sysmon, proxy, DNS, auth logs) and retention.
- Familiarity with ATT&CK to anchor the behavior you intend to hunt.

## Workflow

### Step 1: Pick a behavior, not a tool

Anchor on an adversary behavior (an ATT&CK technique/sub-technique) you have reason to expect
given your threat model, not a specific product alert.

### Step 2: Write a testable hypothesis

Use the form: *"If [actor behavior], then I expect to observe [evidence] in [data source]."*

```text
If an adversary uses WMI for lateral movement (T1047), then I expect to observe
wmiprvse.exe spawning command interpreters on hosts that do not normally do so,
in Sysmon process-creation (Event ID 1).
```

### Step 3: Map to data and logic

Confirm the data source exists and is retained, then define the concrete query/detection logic
and what "normal" looks like (baseline) so anomalies stand out.

```bash
python scripts/analyst.py plan --technique T1047 --datasource "Sysmon EID1" --window 14d
```

### Step 4: Set scope and success criteria

Define the host/time scope, the threshold for "interesting," and the three possible outcomes:
finding (→ IR), detection gap (→ engineering), or confident negative (documented).

### Step 5: Record and hand off

Capture the hypothesis, queries, and outcome so it becomes a repeatable, version-controlled
hunt — successful logic becomes a detection rule.

## Validation

- The hypothesis is falsifiable and names a specific data source that actually exists.
- A baseline of "normal" is defined so results are interpretable.
- Each outcome has a defined next action (IR, detection engineering, or documented negative).

## Pitfalls

- Hunting for a tool name instead of a behavior, missing variants.
- Writing a hypothesis you cannot test with available telemetry.
- No baseline, so every result looks suspicious (or nothing does).

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunt-plan generator.
- MITRE ATT&CK and the PEAK framework (linked in frontmatter).
