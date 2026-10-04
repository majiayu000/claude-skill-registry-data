---
name: xsiam
description: "Expert agent for Palo Alto Cortex XSIAM. Provides deep expertise in the converged SIEM+SOAR+XDR+ASM platform, XQL query development, AI-driven SOC operations, Automation Center playbooks, Investigation Graph, data integration broker, and ML-based correlation and clustering. WHEN: \"XSIAM\", \"Cortex XSIAM\", \"XQL\", \"XSIAM Copilot\", \"Automation Center\", \"Investigation Graph\", \"AI-driven SOC\", \"Palo Alto SIEM\", \"XDR to XSIAM\"."
license: MIT
---

# Palo Alto Cortex XSIAM

This skill covers Palo Alto Cortex XSIAM, the AI-driven SOC platform that converges SIEM, SOAR, XDR, and ASM into a single platform. It has deep knowledge of:

- XQL (XSIAM Query Language) for investigation and detection
- AI-driven correlation and ML-based event clustering
- Automation Center (integrated SOAR with XSOAR heritage)
- Investigation Graph for visual threat analysis
- Data integration broker (log collection, normalization, transformation)
- XDM (XSIAM Data Model) normalization
- XSIAM Copilot (AI assistant)
- Analytics rules and BIOC (Behavioral IOC) rules
- Alert grouping and incident management
- Attack Surface Management integration

**Platform context:** XSIAM represents Palo Alto's vision of an AI-first SOC platform. It absorbed QRadar SaaS customers and aims to replace traditional SIEM+SOAR stacks with a unified, ML-driven platform.

## How to Approach Tasks

1. **Classify** the request:
   - **Investigation** -- XQL query development, Investigation Graph usage
   - **Detection engineering** -- Analytics rules, BIOC rules, correlation logic
   - **Automation** -- Automation Center playbooks, response actions
   - **Data onboarding** -- Data integration broker, XDM mapping, parser configuration
   - **Architecture** -- Platform capabilities, integration strategy, migration planning
   - **XSOAR-specific** -- Read the `xsoar` skill for standalone XSOAR

2. **Gather context** -- Existing Palo Alto products (Cortex XDR, XSOAR, PAN-OS), current SIEM, migration timeline

3. **Analyze** -- Consider the converged platform advantages (native XDR integration) and vendor lock-in trade-offs

4. **Recommend** actionable guidance with XQL examples

## Core Expertise

### XQL (XSIAM Query Language)

XQL is the query language for XSIAM, designed for security investigation:

```xql
// Basic: Failed authentication attempts
dataset = xdr_data
| filter event_type = ENUM.LOGIN and event_sub_type = ENUM.LOGIN_FAIL
| comp count(action_remote_ip) as fail_count by action_remote_ip, auth_domain_username
| filter fail_count > 20
| sort desc fail_count
| limit 50
```

**XQL key commands:**

| Command | Purpose | Example |
|---|---|---|
| `dataset` | Select data source | `dataset = xdr_data` |
| `filter` | Filter events | `filter process_name = "powershell.exe"` |
| `comp` | Aggregate (compute) | `comp count(src_ip) as total by dest_ip` |
| `alter` | Add/modify fields | `alter risk = if(count > 100, "high", "low")` |
| `sort` | Order results | `sort desc total_bytes` |
| `limit` | Restrict output | `limit 100` |
| `dedup` | Deduplicate | `dedup src_ip, dest_ip by asc _time` |
| `join` | Combine datasets | `join type=inner (subquery) as t1` |
| `union` | Merge datasets | `union dataset = panw_traffic` |
| `bin` | Time bucketing | `bin _time span = 1h` |
| `fields` | Select columns | `fields src_ip, dest_ip, action` |
| `config` | Set query parameters | `config timeframe = 24h` |

**Advanced XQL patterns:**

```xql
// Detect lateral movement: same user authenticating to multiple hosts
config timeframe = 1h
| dataset = xdr_data
| filter event_type = ENUM.LOGIN and event_sub_type = ENUM.LOGIN_SUCCESS
| comp count_distinct(agent_hostname) as unique_hosts,
      array_agg(agent_hostname) as host_list
      by auth_domain_username
| filter unique_hosts > 5
| sort desc unique_hosts
```

```xql
// Investigate process execution chain
dataset = xdr_data
| filter event_type = ENUM.PROCESS and event_sub_type = ENUM.PROCESS_START
| filter agent_hostname = "WORKSTATION-01"
| fields _time, actor_process_image_path, actor_process_command_line,
         causality_actor_process_image_path, os_actor_process_image_path
| sort asc _time
```

### AI-Driven Correlation

XSIAM uses ML models to correlate and cluster alerts:

- **Smart Alert Grouping** -- ML clusters related alerts into incidents based on entity relationships, timing, and attack patterns (not just simple field matching)
- **Analytics-First Approach** -- ML models process raw telemetry to identify threats before rule-based detection
- **Causality Chain** -- Tracks the full attack chain from initial access through lateral movement to impact
- **Risk Scoring** -- Entity-based risk scores calculated from multiple signal types

**How XSIAM correlation differs from traditional SIEM:**

| Traditional SIEM | XSIAM |
|---|---|
| Rule-based correlation only | ML correlation + rule-based |
| Manual alert-to-incident mapping | Automatic smart grouping |
| Alert per rule match | Incident per attack chain |
| Static thresholds | Adaptive ML thresholds |
| Manual entity correlation | Automatic causality analysis |

### Automation Center

The Automation Center is XSIAM's integrated SOAR (built on XSOAR technology):

- **Playbooks** -- Visual workflows for automated response (XSOAR playbook format)
- **Integrations** -- 900+ integrations from XSOAR marketplace
- **Sub-playbooks** -- Reusable automation modules
- **Scripts** -- Python/PowerShell scripts for custom logic
- **War Rooms** -- Collaborative investigation spaces

**Key differences from standalone XSOAR:**
- Native integration with XSIAM alerts and incidents
- Access to XQL within playbooks
- Direct access to XDR response actions (isolate, quarantine, block)
- Unified incident queue (no separate SOAR incident view)

### Analytics and BIOC Rules

**Analytics rules** -- Traditional correlation rules:
```
Rule: Multiple Failed Logins Followed by Success
Trigger: When a source IP has > 10 failed logins followed by
         a successful login within 5 minutes
Action: Create alert, severity HIGH
MITRE: T1110 (Brute Force)
```

**BIOC (Behavioral IOC) rules** -- Behavioral detection on endpoint telemetry:
```
Rule: Suspicious Process Injection
Trigger: When a process writes to another process's memory
         AND the target process is a system process
         AND the source process is not a known security tool
Action: Create alert, severity CRITICAL
MITRE: T1055 (Process Injection)
```

**Rule types:**

| Type | Data Source | Detection Method |
|---|---|---|
| **Analytics** | Any ingested data | XQL-based correlation |
| **BIOC** | Cortex XDR agent telemetry | Behavioral pattern matching on endpoints |
| **IOC** | Threat intelligence feeds | Indicator matching (IPs, hashes, domains) |
| **ML** | All telemetry | Machine learning anomaly detection |

### Investigation Graph

Visual investigation tool for exploring attack chains:

- **Automatic graph generation** -- Creates visual graph from incident entities
- **Entity nodes** -- Users, hosts, IPs, processes, files, domains
- **Relationship edges** -- Authentication, network connections, process execution, file operations
- **Timeline integration** -- Overlay events on timeline for temporal analysis
- **Pivoting** -- Click on any entity to explore its relationships and activity
- **XQL integration** -- Drill into XQL queries from any graph node

### Data Integration Broker

XSIAM's data collection and normalization layer:

**Ingestion methods:**

| Method | Use Case |
|---|---|
| **Cortex XDR agent** | Endpoint telemetry (native, richest data) |
| **Syslog/CEF** | Network devices, firewalls, legacy systems |
| **API collectors** | Cloud services, SaaS platforms |
| **Cloud connectors** | AWS, Azure, GCP native integration |
| **Broker VM** | On-premises data collection proxy |
| **HTTP Event Collector** | Application and container logs |

**XDM (XSIAM Data Model) normalization:**
- Normalizes all ingested data to a common schema
- Similar in concept to ECS, CIM, ASIM
- Enables cross-source correlation without source-specific queries
- Custom parsers for unsupported log formats

### XSIAM Copilot

AI-powered assistant for SOC operations:

- **Natural language investigation** -- "What happened on WORKSTATION-01 in the last 24 hours?"
- **XQL generation** -- Converts natural language to XQL queries
- **Incident summary** -- AI-generated narrative of incident timeline and impact
- **Response recommendation** -- Suggests containment and remediation actions
- **Playbook assistance** -- Helps build and debug automation playbooks

## Common Pitfalls

1. **Vendor lock-in** -- XSIAM is deeply integrated with Palo Alto's ecosystem. Migrating away is significantly harder than with open-standard SIEMs.
2. **Pricing complexity** -- Consumption-based pricing can be unpredictable. Monitor data ingestion and compute usage carefully.
3. **XDR agent dependency** -- The richest detection capabilities require Cortex XDR agents on endpoints. Without agents, XSIAM operates primarily as a log analytics platform.
4. **ML trust calibration** -- ML-based correlation may group unrelated alerts or miss correlated ones. Monitor smart grouping accuracy and provide feedback.
5. **Automation Center learning curve** -- While XSOAR-based, the Automation Center in XSIAM has some differences from standalone XSOAR. Existing XSOAR playbooks may need adaptation.
6. **Custom parser complexity** -- Building custom parsers for non-standard log sources requires understanding XDM and the parsing framework.
7. **Migration effort** -- Migrating from traditional SIEM to XSIAM requires rethinking detection strategy (rule-based to analytics-first).

## Migration Considerations

### From QRadar SaaS

IBM divested QRadar SaaS to Palo Alto. Migration path:
1. Data migration handled by Palo Alto migration tooling
2. AQL rules need conversion to XQL analytics rules
3. QRadar offenses map to XSIAM incidents
4. Reference sets map to XSIAM threat intelligence or lookup tables
5. QRadar SOAR playbooks need rebuilding in Automation Center

### From Other SIEMs

1. **Detection rules** -- Convert SIGMA rules to XSIAM analytics rules
2. **Data onboarding** -- Configure Data Integration Broker for each log source
3. **Automation** -- Rebuild SOAR playbooks in Automation Center (XSOAR-compatible)
4. **Custom content** -- Recreate dashboards, reports, and custom searches in XQL
5. **Parallel run** -- Operate both SIEMs for 30-60 days to validate detection parity
