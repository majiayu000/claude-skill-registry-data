---
name: siem
description: "Routing agent for SIEM & SOAR technologies. Cross-platform expertise in log management, event correlation, detection engineering, normalization, SIGMA rules, and security orchestration. WHEN: \"SIEM comparison\", \"which SIEM\", \"log management\", \"detection engineering\", \"SIGMA rules\", \"security analytics\", \"correlation rules\", \"SOAR platform\", \"security automation\", \"alert triage\". Do NOT use for platform-specific questions -- use the `splunk`, `sentinel`, `elastic-security`, `qradar`, `chronicle`, `xsiam`, `splunk-es`, or `soar` skill."
license: MIT
---

# SIEM & SOAR

This skill covers all SIEM (Security Information and Event Management) and SOAR (Security Orchestration, Automation, and Response) technologies. It provides cross-platform expertise in log management, event correlation, detection engineering, normalization standards, and security automation. Read the relevant sibling skill for deep implementation details.

## When to Use This Skill vs. a Sibling Skill

**Use this skill when the question is cross-platform or conceptual:**
- "Which SIEM should we choose for our environment?"
- "How do we build a detection engineering program?"
- "Compare Splunk vs. Sentinel vs. Elastic for our use case"
- "What is the best normalization standard?"
- "How do SIGMA rules work across platforms?"
- "Design our SOC architecture"
- "SIEM data onboarding strategy"
- "How much log storage do we need?"
- "SOAR vs. SIEM automation -- where do we draw the line?"

**Read a sibling skill when the question is platform-specific:**
- "Write an SPL correlation search" --> `splunk`
- "Splunk Enterprise Security risk-based alerting" --> `splunk-es`
- "KQL query for Sentinel analytics rule" --> `sentinel`
- "Elastic EQL sequence detection" --> `elastic-security`
- "QRadar AQL offense query" --> `qradar`
- "Chronicle YARA-L detection rule" --> `chronicle`
- "XSIAM XQL correlation" --> `xsiam`
- "LogScale LQL streaming query" --> `logscale`
- "Build an XSOAR playbook" --> `xsoar`
- "Splunk SOAR automation" --> `splunk-soar`
- "Sentinel playbook with Logic Apps" --> `sentinel-playbooks`

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Platform selection** -- Compare SIEM/SOAR platforms against requirements
   - **Architecture / Strategy** -- Load `references/concepts.md` for foundational SIEM concepts
   - **Detection engineering** -- Cross-platform detection methodology, SIGMA rules, MITRE ATT&CK mapping
   - **Data onboarding** -- Log source strategy, normalization, parsing, enrichment
   - **SOC operations** -- Triage workflows, alert management, metrics (MTTD, MTTR)
   - **Cost optimization** -- Ingestion volume, tiering, filtering, retention policies
   - **Platform-specific** -- Read the appropriate sibling skill

2. **Gather context** -- Environment (cloud/on-prem/hybrid), team size, budget, existing tooling, compliance requirements, log volume (GB/day), retention needs

3. **Analyze** -- Apply SIEM-specific reasoning. Consider data volume, query performance, detection coverage, operational maturity, and total cost of ownership.

4. **Recommend** -- Provide prioritized recommendations with trade-offs. SIEM selection is never one-size-fits-all.

5. **Qualify** -- State assumptions about scale, team skill, and budget constraints

## SIEM Fundamentals

### Core SIEM Functions

1. **Log Collection** -- Aggregate logs from endpoints, network devices, cloud services, applications, and identity providers
2. **Normalization** -- Transform raw logs into a consistent schema (CIM, ECS, ASIM, UDM) for cross-source correlation
3. **Indexing / Storage** -- Store normalized events for real-time and historical search
4. **Correlation** -- Match patterns across multiple log sources to detect threats (correlation rules, analytics rules)
5. **Alerting** -- Generate alerts when correlation rules trigger, with severity and context
6. **Investigation** -- Provide search, drill-down, and visualization for analyst triage
7. **Reporting** -- Compliance reporting, SOC metrics, executive dashboards

### Detection Engineering Lifecycle

```
1. Threat Intelligence    -->  What threats target our environment?
        |
2. Data Source Mapping    -->  Do we have visibility? (MITRE ATT&CK data sources)
        |
3. Detection Logic        -->  Write detection rules (platform-native or SIGMA)
        |
4. Testing & Validation   -->  Atomic Red Team, Caldera, manual simulation
        |
5. Tuning                 -->  Reduce false positives, add exceptions, refine thresholds
        |
6. Deployment             -->  Promote to production with severity and response actions
        |
7. Metrics & Maintenance  -->  Track detection coverage, MTTD, alert fidelity, rule decay
```

### SIGMA Rules

SIGMA is a vendor-agnostic detection rule format that compiles to platform-specific queries:

```yaml
title: Suspicious PowerShell Download Cradle
id: 3b6ab547-8ec2-4991-b9d2-2b06702a48d7
status: stable
description: Detects PowerShell download cradles commonly used by attackers
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        CommandLine|contains|all:
            - 'powershell'
            - 'Net.WebClient'
        CommandLine|contains:
            - 'DownloadString'
            - 'DownloadFile'
    condition: selection
level: high
tags:
    - attack.execution
    - attack.t1059.001
```

SIGMA compiles to:
- **Splunk SPL**: `index=windows sourcetype=WinEventLog:Security ... | search CommandLine="*powershell*Net.WebClient*DownloadString*"`
- **Sentinel KQL**: `SecurityEvent | where CommandLine has_all ("powershell", "Net.WebClient") and CommandLine has_any ("DownloadString", "DownloadFile")`
- **Elastic EQL**: Process creation event with matching command line patterns
- **QRadar AQL**: SQL-like query against normalized fields
- **Chronicle YARA-L**: Event match with target.process.command_line conditions

### Normalization Standards

| Standard | Platform | Key Concept |
|---|---|---|
| **CIM** (Common Information Model) | Splunk | Data models with standardized field names; acceleration for dashboards |
| **ECS** (Elastic Common Schema) | Elastic | Hierarchical field naming (e.g., `process.name`, `source.ip`) |
| **ASIM** (Advanced Security Information Model) | Sentinel | Unifying parsers that normalize at query time; schema-based |
| **UDM** (Unified Data Model) | Chronicle | Google's schema for security telemetry; entity-centric |
| **OCSF** (Open Cybersecurity Schema Framework) | Cross-platform | AWS-originated open standard; growing adoption |

### Data Onboarding Strategy

Prioritize log sources by detection value:

| Priority | Log Sources | Detection Value |
|---|---|---|
| **P1 -- Critical** | EDR, identity (AD/Entra), email gateway, firewall/proxy | Core visibility for 80% of attack techniques |
| **P2 -- High** | Cloud audit logs (AWS CloudTrail, Azure Activity, GCP Audit), DNS, DHCP | Lateral movement, cloud compromise, C2 detection |
| **P3 -- Medium** | Application logs, VPN, DLP, vulnerability scanners | Insider threat, data exfiltration, vulnerability correlation |
| **P4 -- Low** | Network flow (NetFlow/IPFIX), PCAP metadata, printer logs | Forensic enrichment, compliance, niche detections |

### Alert Triage Framework

Effective triage reduces Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR):

1. **Tier 0 -- Automated** -- SOAR handles enrichment, deduplication, known-false-positive suppression, auto-close of informational alerts
2. **Tier 1 -- Triage** -- Analyst validates alert, checks context (asset criticality, user risk score, related alerts), escalates or closes
3. **Tier 2 -- Investigation** -- Deep-dive analysis, timeline reconstruction, scope assessment, containment decisions
4. **Tier 3 -- Hunt** -- Proactive hypothesis-driven threat hunting using SIEM search and detection gaps

## SIEM Platform Comparison

| Capability | Splunk | Sentinel | Elastic Security | QRadar | Chronicle | XSIAM | LogScale |
|---|---|---|---|---|---|---|---|
| **Query Language** | SPL / SPL2 | KQL | EQL, ES\|QL, KQL, Lucene | AQL (SQL-like) | YARA-L 2.0 | XQL | LQL |
| **Normalization** | CIM | ASIM | ECS | QID + DSM | UDM | XDM | Custom | 
| **Deployment** | On-prem, Cloud, Hybrid | Cloud-native (Azure) | On-prem, Cloud, Hybrid | On-prem (SaaS divested) | Cloud-native (GCP) | Cloud-native | Cloud, Self-hosted |
| **Pricing Model** | Ingestion (GB/day) or workload | Ingestion (GB/day) + retention | Node-based or ingestion | EPS (events/sec) | Flat (per user) | Ingestion + compute | Ingestion (GB/day) |
| **SOAR Built-in** | Via Splunk SOAR (separate) | Playbooks (Logic Apps) | Response actions (limited) | QRadar SOAR (separate) | SOAR module | Automation Center | Via Falcon Fusion |
| **ML / AI** | MLTK, predictive analytics | Fusion ML, UEBA, Copilot | ML anomaly detection jobs | Anomaly detection | Duet AI, Mandiant TI | XSIAM Copilot, ML clustering | Statistical functions |
| **Strengths** | Mature ecosystem, SPL power, Splunkbase | Azure integration, cost tiers, Defender XDR | Open source core, EQL sequences, flexible | Automatic offense grouping, AQL familiarity | Unlimited retention, retroactive rules, Mandiant TI | Converged platform (SIEM+SOAR+XDR), AI-first | High-volume streaming, index-free, real-time |
| **Weaknesses** | Cost at scale, complexity | Azure-centric, KQL learning curve | Operational overhead (self-managed), complexity | Aging platform, SaaS discontinued | GCP-centric, limited customization | Vendor lock-in, emerging maturity | Smaller ecosystem, limited SOAR |

### Platform Selection Decision Tree

```
Start: What is your primary cloud?
  |
  ├── Azure-heavy  -->  Microsoft Sentinel (native integration with Defender XDR, Entra, M365)
  |
  ├── GCP-heavy    -->  Chronicle/Google SecOps (native GCP integration, Mandiant TI)
  |
  ├── AWS-heavy    -->  Consider Splunk Cloud, Elastic, or XSIAM (no dominant AWS-native SIEM)
  |
  └── Multi-cloud / On-prem
       |
       ├── Budget priority         -->  Elastic Security (open source core) or LogScale (competitive pricing)
       ├── Mature SOC, complex needs -->  Splunk (deepest ecosystem, SPL power)
       ├── Converged SOC platform   -->  XSIAM (SIEM + SOAR + XDR in one)
       └── High-volume, real-time   -->  LogScale (streaming architecture, index-free)
```

## SOC Metrics

Track these metrics to measure SIEM/SOAR effectiveness:

| Metric | Definition | Target |
|---|---|---|
| **MTTD** | Mean Time to Detect -- time from event to alert | < 1 hour for critical threats |
| **MTTR** | Mean Time to Respond -- time from alert to containment | < 4 hours for critical incidents |
| **Alert Fidelity** | True positives / total alerts | > 80% (below 50% = alert fatigue) |
| **Detection Coverage** | ATT&CK techniques with active detections / total relevant techniques | > 60% for top tactics |
| **Automation Rate** | Alerts handled by SOAR without human intervention | > 40% for mature SOCs |
| **Dwell Time** | Attacker presence before detection | Reduce quarter over quarter |
| **EPS / GB per Day** | Ingestion volume | Monitor for budget forecasting |

## Cost Optimization Strategies

SIEM costs are driven primarily by ingestion volume. Common optimization tactics:

1. **Tiered storage** -- Use hot/warm/cold/frozen tiers. Not all data needs fast search (Splunk SmartStore, Sentinel basic logs, Elastic frozen tier).
2. **Filtering at source** -- Drop noisy, low-value events before ingestion (verbose debug logs, health checks, success-only auth events).
3. **Summary indexing** -- Pre-aggregate statistics for reporting; keep raw data shorter.
4. **Log routing** -- Send compliance-only logs to cheap storage (S3, blob); send security-relevant logs to SIEM.
5. **Data model acceleration** -- Pre-compute common searches to avoid expensive full-index scans.
6. **Commitment tiers** -- Most vendors offer discounts for committed ingestion volumes (Sentinel commitment tiers, Splunk workload pricing).
7. **Event sampling** -- For extremely high-volume, low-fidelity sources (e.g., NetFlow), sample instead of ingesting 100%.

## Anti-Patterns to Watch For

1. **"Collect everything, detect later"** -- Ingesting every log without a detection plan leads to massive costs and no security value. Map data sources to specific detections.
2. **"One alert per threat"** -- Single-event detections produce noise. Use correlation (multi-event, multi-source) and risk-based scoring.
3. **"SIEM as a log archive"** -- A SIEM without active detection rules is an expensive log store. Invest in detection engineering.
4. **"Copy-paste vendor rules"** -- Default rules without tuning generate alert fatigue. Every rule needs environment-specific tuning.
5. **"Ignoring the data pipeline"** -- Normalization, parsing, and enrichment quality determine detection quality. Garbage in, garbage out.
6. **"SOAR without mature processes"** -- Automating bad processes makes them faster, not better. Define playbooks manually before automating.
7. **"Single-platform lock-in"** -- Over-reliance on one vendor's ecosystem makes migration painful. Use SIGMA for portable detections where possible.

## Technology Routing

Read these sibling skills for platform-specific expertise:

| Request Pattern | Route To |
|---|---|
| **SIEM Platforms** | |
| Splunk, SPL, search heads, indexers, forwarders, SmartStore | `splunk` (see its Version-Specific Guidance) |
| Splunk Enterprise Security, ES, notable events, RBA | `splunk-es` |
| Microsoft Sentinel, KQL, ASIM, Fusion, analytics rules | `sentinel` |
| Elastic Security, EQL, ES\|QL, detection engine, Fleet | `elastic-security` (see its Version-Specific Guidance) |
| IBM QRadar, AQL, offenses, DSMs, Ariel | `qradar` |
| Google Chronicle, YARA-L, UDM, SecOps | `chronicle` |
| Palo Alto XSIAM, XQL, AI-driven SOC | `xsiam` |
| CrowdStrike LogScale, LQL, streaming SIEM | `logscale` |
| **SOAR Platforms** | |
| SOAR platform comparison, playbook strategy | `soar` |
| Cortex XSOAR, playbook IDE, war rooms | `xsoar` |
| Splunk SOAR, Phantom, visual playbooks | `splunk-soar` |
| Sentinel Playbooks, Logic Apps automation | `sentinel-playbooks` |
| Tines, no-code security automation | `tines` |
| Torq, hyperautomation, SOC copilot | `torq` |

## Reference Files

Load these for deep foundational knowledge:

- `references/concepts.md` -- SIEM/SOAR foundational concepts: log management lifecycle, event correlation theory, normalization standards, SIGMA rule language, detection engineering methodology, SOC maturity model. Read for "how does SIEM work" or cross-platform architecture questions.
