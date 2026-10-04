---
name: soar
description: "Routing agent for SOAR (Security Orchestration, Automation, and Response) platforms. Cross-platform expertise in playbook design, integration architecture, automation strategy, and SOAR platform comparison. WHEN: \"SOAR comparison\", \"which SOAR\", \"playbook design\", \"security automation\", \"orchestration platform\", \"automated response\", \"SOAR strategy\", \"SOAR integration\", \"automation maturity\". Do NOT use for platform-specific questions -- use the `xsoar`, `splunk-soar`, `sentinel-playbooks`, `tines`, or `torq` skill."
license: MIT
---

# SOAR

This skill covers all SOAR (Security Orchestration, Automation, and Response) technologies. It provides cross-platform expertise in playbook design, integration architecture, automation strategy, and SOC automation maturity. Read the relevant sibling skill for deep implementation details.

## When to Use This Skill vs. a Technology Skill

**Use this skill when the question is cross-platform or strategic:**
- "Which SOAR platform should we choose?"
- "How do we design a phishing response playbook?"
- "What should we automate first in our SOC?"
- "Compare XSOAR vs Splunk SOAR vs Tines"
- "SOAR automation maturity assessment"
- "How do we measure SOAR ROI?"

**Read a sibling skill when the question is platform-specific:**
- "Build an XSOAR playbook for malware triage" --> `xsoar`
- "Splunk SOAR visual playbook configuration" --> `splunk-soar`
- "Sentinel playbook with Logic Apps" --> `sentinel-playbooks`
- "Tines story for IOC enrichment" --> `tines`
- "Torq hyperautomation workflow" --> `torq`

## How to Approach Tasks

1. **Classify** the request:
   - **Platform selection** -- Compare SOAR platforms against requirements
   - **Playbook design** -- Cross-platform playbook methodology
   - **Automation strategy** -- What to automate, when, and how
   - **Integration architecture** -- How SOAR connects to SIEM, EDR, firewall, ticketing
   - **Platform-specific** -- Read the appropriate sibling skill

2. **Gather context** -- SIEM platform (determines natural SOAR pairing), team size, automation maturity, existing integrations

3. **Analyze** -- Consider integration density, learning curve, pricing model, and vendor ecosystem alignment

4. **Recommend** -- Prioritized automation opportunities with ROI justification

## SOAR Platform Comparison

| Capability | XSOAR | Splunk SOAR | Sentinel Playbooks | Tines | Torq |
|---|---|---|---|---|---|
| **Vendor** | Palo Alto Networks | Cisco/Splunk | Microsoft | Tines | Torq |
| **Architecture** | Server-based (on-prem/cloud) | Container-based (on-prem/cloud) | Cloud-native (Logic Apps) | Cloud-native (SaaS) | Cloud-native (SaaS) |
| **Integrations** | 900+ | 300+ apps, 2,800+ actions | 200+ connectors | Unlimited (HTTP actions) | 200+ native |
| **Playbook Design** | YAML/Python + visual | Visual drag-and-drop | Logic Apps designer | No-code (stories) | Visual + AI-assisted |
| **Scripting** | Python, PowerShell | Python | N/A (Logic Apps expressions) | N/A (transform actions) | Python (optional) |
| **Case Management** | Built-in (war rooms, incidents) | Built-in (containers, artifacts) | Built-in (Sentinel incidents) | External integration | Built-in |
| **TI Management** | Built-in (TIM module) | Via Splunk ES integration | Sentinel TI module | External integration | External integration |
| **AI Features** | Limited | Limited | Copilot for Security | AI actions | AI copilot, case summary |
| **Pricing** | Per-endpoint or per-action | Per-action or enterprise | Per Logic App execution | Free (team) / paid (enterprise) | Per-automation volume |
| **Best Paired With** | Cortex XDR, XSIAM | Splunk Enterprise/ES | Microsoft Sentinel, Defender XDR | Any SIEM (vendor-agnostic) | Any SIEM (vendor-agnostic) |

### Platform Selection Guide

```
Start: What is your primary SIEM?
  |
  ├── Splunk/Splunk ES       --> Splunk SOAR (native integration)
  │                               Consider: XSOAR if using Cortex XDR
  |
  ├── Microsoft Sentinel     --> Sentinel Playbooks (native, zero integration effort)
  │                               Consider: XSOAR for advanced playbooks
  |
  ├── Cortex XSIAM           --> Automation Center (built-in, XSOAR heritage)
  |
  ├── Any / Multi-SIEM       --> Tines (vendor-agnostic, no-code)
  │                               OR Torq (AI-driven, hyperautomation)
  │                               OR XSOAR (most integrations)
  |
  └── Budget-constrained     --> Tines Community Edition (free)
                                  OR Sentinel Playbooks (if on Azure)
```

## Automation Strategy

### What to Automate First

Prioritize by: high volume + repetitive + well-defined + low risk of error.

| Priority | Use Case | Automation Type | Expected ROI |
|---|---|---|---|
| **P1** | Phishing triage (URL/attachment analysis, detonation, verdict) | Enrichment + triage | 60-80% analyst time savings |
| **P2** | IOC enrichment (IP, domain, hash reputation lookup) | Enrichment | Saves 5-10 min per alert |
| **P3** | Alert deduplication and grouping | Triage | Reduces alert volume 30-50% |
| **P4** | User account lockout/disable for confirmed compromise | Containment | Reduces MTTR from hours to minutes |
| **P5** | Endpoint isolation for confirmed malware | Containment | Immediate containment |
| **P6** | Ticket creation and SLA tracking | Notification | Consistent process |
| **P7** | Compliance evidence collection | Reporting | Audit readiness |

### Playbook Design Patterns

**Pattern 1: Enrichment Playbook**
```
Alert received
    |
    v
Extract IOCs (IPs, domains, hashes, URLs)
    |
    v
Parallel enrichment:
    ├── VirusTotal lookup
    ├── AbuseIPDB check
    ├── Whois/DNS lookup
    ├── Internal asset lookup (CMDB)
    └── Internal identity lookup (AD/HR)
    |
    v
Aggregate results
    |
    v
Calculate risk score
    |
    v
Update alert with enrichment data
```

**Pattern 2: Triage Decision Playbook**
```
Enriched alert
    |
    v
Check known-false-positive patterns:
    ├── Source in allowlist? --> Auto-close
    ├── Known testing activity? --> Auto-close
    └── Previously investigated same pattern? --> Auto-close
    |
    v (not auto-closed)
Check severity indicators:
    ├── IOC in threat intel? --> Escalate to HIGH
    ├── Target is critical asset? --> Escalate to HIGH
    └── User is VIP/admin? --> Escalate to HIGH
    |
    v
Route to appropriate tier:
    ├── HIGH --> Tier 2 + page on-call
    ├── MEDIUM --> Tier 1 queue
    └── LOW --> Auto-close with documentation
```

**Pattern 3: Containment Playbook**
```
Confirmed incident (analyst-approved or auto-triggered for critical)
    |
    v
Containment actions (parallel):
    ├── Isolate endpoint (EDR API)
    ├── Disable user account (IAM API)
    ├── Block malicious IP (firewall API)
    ├── Block malicious domain (DNS/proxy API)
    └── Quarantine email (email gateway API)
    |
    v
Verify containment:
    ├── Confirm isolation status
    ├── Confirm account disabled
    └── Confirm block applied
    |
    v
Notify stakeholders:
    ├── Security team (Slack/Teams)
    ├── IT operations (ticket)
    └── Management (if critical)
```

### Automation Maturity Model

| Level | Description | Characteristics |
|---|---|---|
| **1 -- Manual** | No automation | Analysts manually triage every alert, copy-paste between tools |
| **2 -- Scripted** | Ad-hoc scripts | Python scripts for common tasks, no central orchestration |
| **3 -- Orchestrated** | SOAR platform deployed | Enrichment playbooks, some triage automation, manual containment |
| **4 -- Automated** | Triage + containment automated | Auto-triage for common alert types, semi-automated containment with approval |
| **5 -- Autonomous** | AI-assisted full lifecycle | ML-driven triage, auto-containment for high-confidence threats, human oversight for edge cases |

## Measuring SOAR ROI

| Metric | Formula | Target |
|---|---|---|
| **Time saved per alert** | (manual triage time) - (automated triage time) | > 10 minutes per alert |
| **Automation rate** | Alerts handled without human intervention / total alerts | > 40% |
| **MTTR reduction** | (pre-SOAR MTTR) - (post-SOAR MTTR) | > 50% reduction |
| **Analyst capacity** | Alerts handled per analyst per day | > 2x improvement |
| **Playbook success rate** | Successful playbook executions / total executions | > 95% |
| **FTE savings** | Time saved per month / (FTE hours per month) | Calculate dollar value |

## Technology Routing

Read these sibling skills for platform-specific expertise:

| Request Pattern | Route To |
|---|---|
| XSOAR, Cortex XSOAR, war rooms, XSOAR playbook | `xsoar` |
| Splunk SOAR, Phantom, Splunk playbook | `splunk-soar` |
| Sentinel Playbooks, Logic Apps automation | `sentinel-playbooks` |
| Tines, no-code automation, stories | `tines` |
| Torq, hyperautomation, Torq workflow | `torq` |
