---
name: sota-detection-engineering
description: >-
  State-of-the-art detection engineering, SOC, threat hunting, and incident
  response (2026). Use when BUILDING detective controls or SOC capability —
  Sigma/YARA/Falco/Tetragon/Suricata rules, detection-as-code, MITRE ATT&CK
  coverage, SIEM detections, alert triage and SOAR, threat hunts,
  threat-intel, deception, IR playbooks, or adversary emulation — AND when
  AUDITING detection & IR posture (can we detect this? does this alert fire?).
  Owns DETECTIVE controls, SOC workflow, hunting, and IR (sota-observability
  owns the telemetry pipeline). Trigger keywords: detection engineering,
  detection-as-code, Sigma, YARA, YARA-X, Falco, Tetragon, Suricata, SIEM,
  KQL, SPL, EQL, ATT&CK, Pyramid of Pain, threat hunting, threat intel, TIP,
  STIX, TAXII, IOC, IOA, TTP, SOC, alert fatigue, tuning, SOAR, runbook,
  incident response, IR playbook, NIST 800-61, PICERL, forensics, chain of
  custody, purple team, honeypot, honeytoken, canary, OCSF, MTTD, false
  positive, Active Directory, Kerberoasting, DCSync, golden ticket, ADCS,
  RBCD.
---

# SOTA Detection Engineering, SOC & Incident Response

## Purpose

Assume prevention fails. This skill builds and audits the layer that *notices*:
detective controls, the SOC that triages them, the hunts that find what alerts
miss, and the IR process that contains what hunts surface. One question defines
success:

> **When a real adversary acts inside your environment, does a high-fidelity
> signal fire, reach a human (or automation) with the context to act, and drive
> a bounded response — fast enough to matter?**

Detection is engineering, not art. Detections are **code**: version-controlled,
peer-reviewed, CI-tested, ATT&CK-mapped, FP-budgeted, and retired when stale.
The dominant failure mode is not missing rules — it is **alert fatigue**: noise
that buries the one true positive. Optimize signal-to-noise relentlessly.

**Ownership boundary.** `sota-observability` owns the telemetry pipeline (logs,
metrics, traces, SLOs, log shipping, retention plumbing). This skill owns
turning that telemetry into *security* detections, the SOC workflow, hunting,
and IR. `sota-threat-modeling` owns design-time threat enumeration (STRIDE/
ATT&CK/ATLAS catalogs); this skill owns catching those threats at runtime. If
you find yourself designing the logging schema, that's observability rules/01;
if you find yourself enumerating threats on a DFD, that's threat-modeling.

## BUILD mode

Run the detection lifecycle as a loop, not a one-shot. Hypothesis → build →
test → deploy → tune → retire. Workflow:

1. **Start from a threat hypothesis, not a tool.** Name the ATT&CK technique or
   abuse case, the adversary behavior, and the telemetry that would witness it.
   Use the **ADS framework** (Palantir): goal, categorization (ATT&CK), strategy
   abstract, technical context, blind spots/assumptions, false positives,
   validation, priority. Write this *before* the rule.
2. **Confirm the log source exists first.** You cannot detect what you do not
   collect. Map the hypothesis to a concrete data source (EDR, cloud audit, K8s
   audit, network/flow, identity, app). If it's missing, the deliverable is a
   *logging gap*, not a rule. See rules/02.
3. **Detect behavior over artifacts.** Climb the **Pyramid of Pain**: prefer
   TTP/behavioral logic over brittle hashes/IPs/domains. IOC matches are cheap
   and disposable; TTP detections cost the adversary real money to evade.
4. **Pick the right engine** (rules/03): Sigma for log detections (vendor-
   agnostic, compiled to your SIEM), YARA-X for file/memory/malware, Suricata
   for network, Falco/Tetragon for eBPF runtime/container/K8s, SIEM-native
   (KQL/SPL/EQL) for correlation the portable formats can't express.
5. **Engineer for low FP from the start** (rules/04): scope tightly, add
   allowlist context, require corroboration for noisy signals, set a severity
   honestly. Every detection ships with a runbook (link to observability
   rules/04 alerting plumbing) and an owner.
6. **Test before deploy.** Validate with adversary emulation — Atomic Red Team
   (endpoint), Stratus Red Team (cloud), Caldera (campaigns). Confirm the
   detection fires on the real technique and stays quiet on benign baselines.
   No detection merges without a passing test. See rules/06.
7. **Map coverage and find gaps.** Track every detection against ATT&CK with the
   Navigator. Coverage heatmaps reveal blind spots — feed them back to step 1.
8. **Tune and retire.** Review FP rates, suppress with *expiry* (never forever),
   delete detections nobody trusts. A muted alert is worse than none.

For hunting and deception, see rules/05; for IR, see rules/06.

## AUDIT mode

Assess an existing detection/SOC/IR posture adversarially. Read rules/06 (IR &
validation) and rules/04 (SOC/triage) first. Sample real detections, real
alerts, and real incidents — do not trust a coverage dashboard or a wiki
runbook that has never fired. The cardinal test: pick three ATT&CK techniques
relevant to the environment and prove, end to end, that each would be caught.

**Severity:**

| Severity | Meaning | Examples |
|----------|---------|----------|
| Critical | Blind to a primary attack path, or IR cannot execute | No log source for the crown-jewel system; no EDR/cloud-audit/K8s-audit collection; no IR plan or no one on call; detections exist but nothing routes alerts to a human |
| High | Major coverage gap or SOC dysfunction | Alert fatigue (analysts mute/ignore); detections never tested against the technique; IOC-only coverage of behaviors that need TTP logic; runbooks absent or stale; no ATT&CK coverage map; retention too short for IR |
| Medium | Degraded fidelity or process gaps | Detections with no owner/ADS doc; suppressions with no expiry; no deduplication/correlation; severity inflation; no purple-team/regression testing; TI not operationalized into detections |
| Low | Hygiene | Detections not in version control; inconsistent naming; no FP metrics; Navigator layer stale; no blameless PIR template |
| Info | Observation / hardening opportunity | Deception not deployed where it'd be high-value; coverage maturity below target; SOAR automation candidates |

**Finding format** (one per finding):

```
file:line | rule | severity | effort (trivial/small/medium/large) | fix
```

Example:

```
detections/aws/iam.yml:14 | ioc-only-detection-of-ttp-behavior | High | medium |
  GuardDuty-finding-name match is brittle; rewrite as CloudTrail behavioral
  Sigma rule on CreateAccessKey+AttachUserPolicy by non-admin principal,
  test with Stratus Red Team aws.persistence.iam-create-admin-access-key.
```

Conclude with the verdict: **for the top 3 techniques in scope, is detection
PRESENT / PARTIAL / ABSENT end-to-end** (signal → alert → human → response),
and the shortest path to closing the worst gap.

## Rules index

| File | Read this when... |
|------|-------------------|
| `rules/01-detection-engineering-discipline.md` | Running the detection lifecycle, writing ADS docs, doing detection-as-code (CI/peer review/regression), mapping coverage to ATT&CK + Navigator, applying the Pyramid of Pain, picking maturity targets and metrics (coverage/precision/MTTD) |
| `rules/02-telemetry-siem-data-layer.md` | Deciding what to collect (the #1 gap), choosing SIEM/data-lake, normalizing with OCSF/ECS, sizing retention for IR/hunting, controlling volume/cost, assessing data quality; application & behavioural detections (app-login spraying/stuffing/impossible travel, LLM/agent runtime and model-API-as-C2, data-access exfiltration and DB anomalies) |
| `rules/03-rule-languages-engines.md` | Choosing and writing detections in Sigma, YARA/YARA-X, Suricata, Falco, Tetragon, or SIEM-native (KQL/SPL/EQL); rule quality, specificity, FP-resistance, performance; good/bad examples |
| `rules/04-alerting-triage-soc-soar.md` | Fighting alert fatigue, tuning/suppression with expiry, severity assignment, enrichment, dedup/correlation, runbooks, SOAR + auto-containment guardrails, case management, FP lifecycle, SOC metrics |
| `rules/05-hunting-intel-deception.md` | Hypothesis-driven hunting + the hunt loop, IOC vs IOA/TTP hunting, threat-intel lifecycle + TIP, STIX 2.1/TAXII 2.1, diamond model/kill chain, deception (honeypots/honeytokens/canaries) |
| `rules/06-incident-response-validation.md` | Running IR (NIST SP 800-61r3 / CSF 2.0, PICERL), playbooks, severity classification, containment/eradication/recovery, forensic readiness + chain of custody, blameless PIR, tabletops; validating detections via Atomic Red Team/Caldera/Stratus, purple teaming, regression testing |
| `rules/07-ad-attack-detection.md` | Detecting on-prem Active Directory attacks: DC audit-policy telemetry and the events that matter (4768/4769/4770, 4662, 4624/4625, 5136, 8004, 4886/4887), Kerberoasting (RC4 TGS spikes), AS-REP roasting, DCSync (replication GUIDs on 4662), golden/silver tickets, DCShadow, ADCS abuse (ESC1), NTLM relay, password spraying, RBCD writes (5136); ATT&CK mapping (T1558.x, T1003.006, T1207, T1649) + AD deception (honeytoken SPNs, canary objects). Hardening lives in sota-identity-access rules/07 |

## Top 10 non-negotiables

1. **You can't detect what you don't collect.** The #1 gap is telemetry, not
   rules. Audit log-source coverage against your attack paths before writing a
   single detection.
2. **Detections are code.** Version-controlled, peer-reviewed, CI-tested,
   ATT&CK-mapped, with an owner and an ADS doc. A detection that isn't tested
   isn't a detection — it's a hope.
3. **Every detection is validated against the real technique.** Atomic Red Team
   / Stratus / Caldera proves it fires; a benign baseline proves it stays
   quiet. No merge without both.
4. **Climb the Pyramid of Pain.** Prefer TTP/behavioral logic over hashes/IPs/
   domains. IOCs are a supplement and an enrichment, never the strategy.
5. **Signal-to-noise is the product.** Alert fatigue is the dominant SOC
   failure. Tune aggressively, suppress with *expiry*, and treat a chronically
   ignored alert as a Critical defect.
6. **Every alert has a runbook and an owner.** No actionable signal reaches a
   human without next steps. Wire alerting plumbing via sota-observability
   rules/04; you own the *security* content.
7. **Map coverage to ATT&CK and stare at the gaps.** A Navigator heatmap that
   nobody updates is theater. Coverage drives the next hypothesis.
8. **Behavior-detect, then enrich.** Correlate, deduplicate, and decorate alerts
   with asset/identity/TI context so triage is seconds, not minutes.
9. **An IR plan that's never exercised is fiction.** Tabletop it, keep contacts
   and authority-to-contain current, and run blameless post-incident reviews
   that feed new detections.
10. **Deception is the highest-fidelity signal you own.** A touched honeytoken
    or honeypot has ~zero false positives. Deploy canaries in the paths
    attackers must traverse (see sota-secrets-management rules/04 honeytokens).
