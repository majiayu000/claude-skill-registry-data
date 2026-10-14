---
name: edr-pro
description: Deploy and operate endpoint detection and response — policy tuning, behavioral detections, threat hunting, and response actions.
category: security
---

## Overview

EDR is the defender's eyes on the endpoint: it records process, file, registry, and network activity, detects malicious behavior, and enables remote response (isolate, kill, remediate). It is arguably the highest-value single security control for most organizations — and also one of the most misconfigured, oscillating between alert floods and silent monitor-mode deployments.

This skill covers the full EDR practice: deployment, policy design, detection tuning, threat hunting on EDR telemetry, and safe response operations.

Deploy for coverage first, then tune for precision: get the agent everywhere (including servers, not just laptops), confirm telemetry is flowing, and only then start shaping policies and detections. An EDR covering 60% of endpoints with perfect tuning protects less than one covering 98% with acceptable noise.

## When to use

- Rolling out EDR to endpoints and servers for the first time.
- Tuning noisy policies or investigating EDR-caused performance issues.
- Building behavioral detections for your threat model.
- Running threat hunts across endpoint telemetry.
- Defining response playbooks (isolate, contain, remediate) with approval gates.

## Core concepts

- **Coverage is the metric that matters most.** Unprotected endpoints are invisible endpoints. Track deployment % by asset class relentlessly — servers and OT-adjacent systems included.
- **Prevention vs detection modes.** Modern EDR does both: block known-malicious behaviors automatically, detect-and-alert on suspicious ones. Progressively enable blocking on high-confidence behaviors; keep detection on the ambiguous.
- **Behavioral detections beat IOCs.** Detect techniques (credential dumping, LSASS access, suspicious parent-child process chains) mapped to ATT&CK — they survive attacker infrastructure changes.
- **Policy layering.** Baseline policies for all endpoints, stricter for servers and high-risk groups, monitor-only for fragile/legacy systems with compensating controls. One global policy fits nobody.
- **Telemetry retention.** EDR telemetry is your best hunting and investigation dataset — retain as long as budget allows (90+ days ideal), and know exactly what you keep.
- **Response actions with gates.** Network isolation, process kill, and file quarantine are powerful — define who may trigger them, require approval for broad actions, and log everything.
- **Tamper protection.** Attackers kill EDR first. Enforce tamper protection, alert on agent uninstall/disable attempts, and monitor agent health as a security signal.
- **Performance partnership.** EDR scans cost CPU/IO — work with IT on exclusions for legitimate heavy workloads (build servers, databases) via documented, reviewed exception processes, not ad-hoc disabling.
- **Threat hunting.** Proactive hypothesis-driven searches across EDR telemetry ("show me all LSASS access outside expected processes") catch what automated detections miss.
- **Integration.** EDR alerts feed the SIEM/SOC with process-tree context; EDR telemetry enriches firewall and identity investigations. An isolated EDR console is half the value.

- **Cloud workload coverage.** Containers and serverless need their own sensor strategy — classic host agents do not cover ephemeral workloads. Plan EDR/CWPP coverage per workload type.
- **Offline and air-gapped endpoints.** Devices off-network for weeks miss policy updates and detections. Define maximum offline tolerance and catch-up procedures.

## Practical workflow

1. **Deploy for coverage:** phased rollout (IT pilot → general population → servers → tricky segments), tracking install % daily. Resolve the long tail — the last 5% takes 50% of the effort and is often the riskiest.
2. **Verify telemetry:** confirm events flowing per endpoint, check for blind spots (agent version skew, policy gaps, offline systems), and alert on agent health failures.
3. **Tune policies:** start from vendor recommended baselines, adjust for your environment, document every exclusion with justification and review date. Re-tune quarterly.
4. **Build behavioral detections:** map your top ATT&CK techniques to EDR detection rules; test against benign baselines; deploy with runbooks linked.
5. **Hunt regularly:** weekly hypothesis-driven hunts using threat intel and red-team TTPs; convert hunt findings into permanent detections.
6. **Operate response:** playbooks for isolate/kill/quarantine with approval gates; post-action verification (re-scan, monitor for re-infection); lessons fed back into detections and policy.

### Quick wins

- Enable tamper protection everywhere this week — it is the cheapest high-value control
- Audit agent coverage by asset class; close the server gap first
- Review and justify every policy exclusion older than 90 days

### Sustaining the practice

- Review policy exclusions quarterly — each needs re-justification or removal
- Re-run coverage audits monthly; new systems must get agents at provisioning
- Hunt cadence: at least weekly, tied to current threat intel
- Test tamper-protection and agent-health alerting with simulated disable attempts

### Metrics that prove it works

- Agent coverage % by asset class (target: 98%+)
- Mean time to detect and to contain on endpoint incidents
- False-positive rate per policy/detection; analyst action rate
- Threat-hunt findings converted to detections per quarter

## Common pitfalls

- **Monitor-only forever.** Detection without blocking on high-confidence behaviors leaves dwell time on the table. Progressively enable prevention.
- **Coverage theater.** "Deployed" with 70% coverage and no plan for the rest. The uncovered 30% is where attackers live.
- **Exclusion sprawl.** Every performance complaint becomes a permanent exclusion. Review exclusions quarterly with security+IT jointly.
- **Killing the agent to 'fix' performance.** Disabling EDR for speed is a security incident, not a fix. Tune, exclude narrowly, or upgrade hardware.
- **No tamper protection.** Attackers' first move is blinding the sensor. Enforce it and alert on tampering attempts.
- **Alert-only hunting.** EDR telemetry unused for proactive hunting wastes its best capability. Schedule hunts like any other security operation.
- **Forgetting servers.** Laptop-focused rollouts leave the crown-jewel servers unprotected. Servers get agents with server-tuned policies.
- **Response without verification.** Isolating a host and calling it done misses persistence and lateral movement. Verify with re-scan and monitoring.
- **Treating EDR as antivirus replacement only.** Its investigation and hunting value dwarfs the blocking value — train analysts on the telemetry, not just the alerts.
- **No offline-device strategy.** Laptops off VPN for a month return with stale policies and missed detections. Enforce check-in requirements.
