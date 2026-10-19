---
name: detection-engineering
description: Build, test, and tune defensive detections from logs and telemetry — turn an attack technique or an observed finding into a high-fidelity detection rule (Sigma, KQL, SPL, EQL), map it to MITRE ATT&CK, estimate false-positive rate, and define validation and tuning steps. Also runs hypothesis-driven threat hunts over existing logs. Use whenever the user mentions detection rules, Sigma, SIEM, log analysis, MITRE ATT&CK mapping, threat hunting, "write a detection for X", alert tuning, or wants to know whether an attack would be caught.
license: Apache-2.0
metadata:
  layer: specialist
  status: under-review
  coverage: detection-engineering
---

# Detection Engineering & Threat Hunting

Defensive counterpart to the hunters: given a technique or a finding, produce a detection
that fires on the malicious behavior and rarely on benign activity. A detection nobody can
validate, that has an unknown false-positive rate, or that keys on a trivially-changed
artifact is not done.

This is a **defensive** skill — writing detections and hunting over the defender's own
logs. No target testing; the authorization that matters is access to the log data.

## Inputs
- The behavior to detect: an ATT&CK technique id, an attack description, or a finding from
  a hunt/pentest.
- The telemetry available: data sources (EDR/process, auth, cloud audit, DNS, proxy,
  network) and the platform (Sigma→X, Splunk SPL, Microsoft KQL/Sentinel, Elastic EQL).
- A sample of normal activity if available (for FP estimation).

## Workflow — from technique to detection
1. **Model the behavior.** What actually happens on the wire/host? Separate the
   **invariant** (hard for the attacker to change — e.g. the API call, the parent/child
   process relationship, the auth anomaly) from the **incidental** (a specific filename,
   a user-agent string, a one-off command flag). Detect the invariant.
2. **Map to ATT&CK.** Tactic + technique/sub-technique id; note the data source(s)
   required (ties the rule to real telemetry — a rule you have no data for can't fire).
3. **Choose the altitude.** Prefer behavioral/relationship logic over static IOCs.
   Example: don't alert on a hash; alert on `office app → spawns → script interpreter →
   network connection`.
4. **Write the rule** in the target language. Default authoring format is **Sigma**
   (portable), then translate. Include: title, status, logsource, detection, condition,
   `level`, `tags` (ATT&CK), and a `falsepositives` list.
5. **Estimate false positives.** Name the benign sources that match and how to exclude
   them. If you can run it against a normal-activity sample, record the hit rate.
6. **Define validation.** How to safely trigger the behavior in a lab (e.g. Atomic Red
   Team test id) and confirm the rule fires — distinguish "written" from "validated."
7. **Tune.** Allowlist known-good, tighten the condition, set a sensible threshold/window;
   re-measure FP. Document residual blind spots (what the rule still misses).

## Threat-hunting mode (hypothesis-driven)
1. State a hypothesis ("an attacker using technique T would leave trace X in data source
   D"). 2. Query for X. 3. Triage hits: benign baseline vs anomaly. 4. For anomalies,
   pivot (process tree, auth timeline, network). 5. Either confirm an incident (→ IR
   handoff) or record the cleared hypothesis + a new detection to catch it next time.
Record cleared hunts so they aren't repeated; a null result with good coverage is a result.

## Decisions requiring judgment
- Is a match an attack or an admin/automation baseline? Pivot before alerting.
- Behavioral rule (higher coverage, more FPs) vs narrow rule (fewer FPs, easy to evade) —
  state the tradeoff; often ship both at different severities.
- Missing data source → the honest output is "not detectable with current telemetry +
  what to onboard," not a rule that can't fire.

## Evidence vs hypothesis
A rule is **written** until it has fired on a real/simulated instance of the behavior AND
been checked against benign data; only then is it **validated** (record in
`TEST_RESULTS.md`). Never claim coverage you haven't triggered.

## Tools (check availability; none bundled)
- `sigma`/`sigmac`/`pySigma` to convert Sigma→SPL/KQL/EQL.
- Atomic Red Team / Caldera to safely generate the behavior **in a lab only**.
- The target SIEM's query interface for validation and FP measurement.
- Confirm each exists before relying on it; otherwise hand the user the Sigma rule +
  manual translation.

## Failure handling
No telemetry for the technique → output the data-source gap + onboarding recommendation.
Can't translate automatically → ship the Sigma rule and the manual query. High FP you
can't tune below a useful threshold → ship as a low-severity hunt query, not an alert, and
say so.

## Output
A detection package: the rule (Sigma + translation), ATT&CK mapping, required data
sources, FP analysis, validation procedure, and residual blind spots. For hunts: the
hypothesis, query, triage result, and any new detection proposed.

## Acceptance criteria (for `validated`)
- POS: given a technique + data sources, emits a Sigma rule keyed on the invariant with
  ATT&CK tags and an FP list. NEG: refuses to emit an IOC-only rule when a behavioral one
  is possible, or a rule for a data source the user doesn't have. SAFE: lab-only
  simulation; no production-target testing. INC: marks a rule "written, not validated"
  until it has fired.

## References
MITRE ATT&CK; Sigma project; Atomic Red Team; the SIEM's query-language docs. Siblings:
`cloud-security` (cloud audit logging), `bb-chains` (what impact to detect), `threat-intel`
(future).
