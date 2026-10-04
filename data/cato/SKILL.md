---
name: cato
description: "Expert agent for Cato Networks SASE. Covers single-vendor SASE cloud, SD-WAN, SWG, CASB, FWaaS, ZTNA, XDR, and Cato's 80+ PoP single-pass cloud engine. WHEN: \"Cato Networks\", \"Cato SASE\", \"Cato SD-WAN\", \"Cato ZTNA\", \"Cato XDR\", \"Cato FWaaS\", \"Cato socket\", \"single-vendor SASE\", \"Cato CTRL\"."
license: MIT
---

# Cato Networks

This skill covers Cato Networks' single-vendor SASE cloud platform. Cato differentiates itself by building SD-WAN and the complete security service edge into one cloud-native platform from inception — not assembled through acquisitions. All traffic flows through Cato's single-pass cloud engine across 80+ global PoPs.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **SD-WAN** — Cato Socket, site connectivity, last-mile optimization, HA
   - **SWG/Internet security** — URL filtering, TLS inspection, threat prevention
   - **CASB/DLP** — SaaS visibility, inline control, data protection
   - **ZTNA** — Private application access, Cato Client, Zero Trust policies
   - **FWaaS** — Network firewall policies, IPS, anti-malware
   - **XDR** — Cato XDR, threat hunting, incident response
   - **Architecture** — PoP design, single-pass processing, deployment models

2. **Identify the deployment scope** — Sites (offices with Cato Sockets), mobile users (Cato Client), or cloud connectors (AWS/Azure VPCs).

3. **Recommend** — Provide Cato-specific guidance with Cato Management Application (CMA) navigation paths.

## Cato SASE Architecture

### Single-Vendor SASE Philosophy

Cato Networks was founded (2015) with the explicit goal of building SASE as a unified platform — before the term "SASE" was coined by Gartner. Unlike competitors who assembled SASE by acquiring separate SWG, CASB, and SD-WAN companies, Cato built everything natively:

**Native integration benefits:**
- Single data model: One policy engine, one log schema, one management console
- Single agent: Cato Client handles ZTNA + internet security + SD-WAN optimization
- Single support: No finger-pointing between vendors for cross-component issues
- Single analytics: All traffic visible in one console, correlated automatically

### Cato Cloud Architecture

```
Cato SASE Cloud
├── Global PoP Network (80+ PoPs)
│   ├── Single-pass processing engine
│   ├── SD-WAN: WAN optimization, active-active HA
│   ├── NGFW / FWaaS: L4-L7 policy
│   ├── SWG: URL filtering, TLS inspection
│   ├── CASB: Inline + API SaaS security
│   ├── DLP: Data loss prevention
│   ├── IPS: Intrusion prevention
│   ├── Anti-malware: Multi-layer (signatures + behavioral + ML)
│   ├── DNS Security: Malicious domain blocking
│   ├── ZTNA: Private app access
│   └── RBI: Remote Browser Isolation (add-on)
│
├── Cato Management Application (CMA)
│   ├── Single console for all sites, users, policies
│   ├── Built-in analytics and reporting
│   └── Cato XDR (extended detection and response)
│
└── Cato CTRL (Threat Research)
    ├── Threat intelligence updates to all PoPs
    └── Threat hunting across customer telemetry
```

### Single-Pass Processing Engine

All traffic at every Cato PoP passes through a single processing pipeline — one TLS decrypt, all inspection engines run simultaneously.

```
Traffic arrives at Cato PoP
        ↓
Connection classification
(Is this SD-WAN site traffic, mobile user, or cloud resource?)
        ↓
TLS termination (single decrypt)
        ↓
┌────────────────────────────────────────────────────────┐
│                  Parallel Inspection                   │
│  App/Protocol    URL Category    IPS Signatures        │
│  Identification  DNS Security    Anti-malware          │
│  CASB Activity   DLP Content     Behavioral ML         │
└────────────────────────────────────────────────────────┘
        ↓
Policy decision (NGFW rule evaluation)
        ↓
Action + logging
        ↓
TLS re-encrypt + forwarding
```

## SD-WAN with Cato Socket

### Cato Socket

The Cato Socket is a hardware or virtual SD-WAN device deployed at office/branch locations.

**Socket models:**
- **X1500:** Small offices (up to 100 Mbps)
- **X1600:** Medium offices (up to 500 Mbps)
- **X1700:** Large sites (up to 1 Gbps)
- **X1700 (HA):** Hardware HA pair for high-availability deployments
- **vSocket:** Virtual appliance for VMware, Hyper-V, AWS, Azure, GCP

**Socket connectivity:**
- 2 WAN interfaces (broadband, MPLS, LTE)
- 1+ LAN interfaces
- Management interface (out-of-band)

### Last-Mile Optimization

Cato Socket provides active-active dual WAN with intelligent path selection:

**Active-active bonding:**
Traffic distributed across both ISP links simultaneously (not just failover):
- Improves throughput for bulk transfers
- Reduces impact of single-ISP packet loss
- Seamless failover when one link degrades

**Path quality scoring:**
Cato scores each WAN link continuously:
- Latency to nearest Cato PoP
- Jitter
- Packet loss
- Availability (ICMP probes + TCP probes)

**Application-aware steering:**
```
VoIP (RTP/SIP): Route via lowest-jitter path
Video (Zoom): Route via lowest-latency path
Bulk backup: Route via highest-bandwidth path
Default: Load-balance across both links
```

**Link failure detection:**
Sub-second detection of link failures via continuous probes. Failover < 1 second with active-active bonding (vs. BGP convergence of 30-90 seconds with traditional router failover).

### Cloud On-Ramp

**For AWS/Azure/GCP:**
Deploy a vSocket in the cloud VPC/VNet:
1. Launch vSocket from marketplace (AWS AMI, Azure Marketplace)
2. Configure with Cato account credentials
3. vSocket connects to nearest Cato PoP
4. Route private subnets through vSocket

**Benefit:** All traffic from cloud workloads to the internet passes through Cato's security stack. No need for a separate cloud firewall or security appliance.

## ZTNA on Cato

### Private Application Access

**Cato SDP (Software-Defined Perimeter) for ZTNA:**
Users with Cato Client access private applications through Cato's cloud — applications never exposed to the internet.

**Configuration:**
1. Define "IPSec Connections" or "Cloud Connectors" for app hosting location connectivity (already done if using vSocket)
2. Define application in Cato Management Application
3. Create access policy: User group → Application → Action: Allow

**ZTNA policy granularity:**
```
Policy: Finance Team → SAP
Source User: Group = "Finance" 
Source Device: Posture = "Compliant"
Destination App: SAP-Production (defined by IP/FQDN)
Service: TCP 443, TCP 8443
Action: Allow

Policy: Contractors → Limited Apps
Source User: Group = "Contractors"
Destination App: Contractor-Portal
Action: Allow
```

**Device posture for ZTNA:**
Cato Client reports device posture. Access policies can require:
- OS version
- Disk encryption
- Antivirus (specific vendor + update recency)
- EDR agent running

### Cato Client

**Supported platforms:** Windows, macOS, Linux, iOS, Android.

**Function:** Single agent for both ZTNA (private app access) and internet security (SWG via Cato cloud). No separate VPN client needed.

**Connection establishment:**
Cato Client connects to nearest Cato PoP. All corporate internet traffic + private app access flows through this connection.

**Always-on mode:** Cato Client can be configured always-on — device always connected to Cato SASE cloud. No user action required.

## FWaaS and Security Policies

### Firewall Policy Structure

Cato's firewall policy is a unified North-South + East-West rule set.

**Traffic directions:**
- **WAN → Internet:** Outbound internet traffic from sites/users
- **WAN → WAN:** Site-to-site traffic (between offices, or office to cloud)
- **Internet → WAN:** Inbound to DMZ/published services
- **ZTNA access:** User → Private Application

**Rule structure:**
```
Rule: Block Outbound Malware Categories
Source: Any (site or user)
Destination: URL Category = Malware, Phishing, Botnet
Action: Block

Rule: Allow M365
Source: Any
Destination: App = Microsoft 365 (App-ID)
Action: Allow + Inspect

Rule: Allow Finance to SAP (WAN to WAN)
Source: Site = HQ-Finance-VLAN (IP range 10.10.20.0/24)
Destination: IP = SAP-server (10.50.0.10)
Service: TCP 443, TCP 8443
Action: Allow
```

### IPS (Intrusion Prevention System)

Cato IPS uses a combination of signature-based and behavioral detection.

**IPS policy:**
- **Severity levels:** Critical, High, Medium, Low, Informational
- **Actions per severity:** Block / Alert / Allow
- **Recommended baseline:** Block Critical + High; Alert Medium

**IPS update mechanism:**
Cato CTRL (threat research team) pushes IPS signature updates to all PoPs continuously. No customer-side action required.

**Custom IPS rules:** Enterprise customers can add custom Snort-compatible signatures.

### Anti-Malware

Multi-layer anti-malware:
1. **Signature-based (AV):** Known malware detection
2. **ML-based behavioral:** Detect novel malware by behavior patterns
3. **Threat intelligence:** Block known-malicious hashes (Cato CTRL + external feeds)
4. **Sandboxing (premium):** Full detonation for unknown files

**Anti-malware policy:**
```
Enable for: Downloads from internet, uploads to SaaS (if inline CASB enabled)
Malicious verdict action: Block
Unknown/suspicious verdict action: Alert + allow (or hold + sandbox)
File type scope: Executables, Office documents, PDF, Archives
```

## CASB and DLP

### Inline CASB

Cato's inline CASB provides application-level visibility and control for SaaS traffic flowing through the platform.

**Shadow IT discovery:**
All SaaS app usage visible in CMA → Monitoring → Cloud Apps:
- App name, risk category, usage volume
- User/site breakdown
- CCI (Cloud Confidence Index) equivalent score

**Application controls:**
```
Policy: Restrict personal cloud storage
Application: Google Drive Personal, Dropbox Personal, OneDrive Personal
Activity: Upload
Action: Block

Policy: Allow corporate storage
Application: Google Drive Corporate, OneDrive Corporate, Box Corporate
Activity: All
Action: Allow + DLP Inspect
```

### DLP

Cato DLP provides content inspection for sensitive data.

**Detection methods:**
- Pattern-based: Credit cards, SSN, IBAN, health data patterns
- Custom patterns: Organization-specific regex
- Keyword dictionaries: Custom sensitive word lists

**DLP policy:**
```
Profile: Confidential-Data
  Rules:
  - Credit Card Numbers (Luhn validated), count >= 3
  - Social Security Numbers, count >= 5
  - Custom: "Project-Confidential" keyword

Policy: Block Confidential Upload to Personal Storage
  DLP Profile: Confidential-Data
  Destination: Cloud Storage (Personal)
  Action: Block + Alert
```

## Cato XDR

### Threat Detection and Response

Cato XDR is built into the CMA console — no separate SIEM required for many use cases.

**Data sources for XDR:**
- All network flows (Cato processes 100% of traffic, full visibility)
- Security events (IPS alerts, malware detections, policy blocks)
- Identity signals (if IdP integrated)
- Endpoint signals (if Cato Client telemetry enabled)

**Threat stories:**
Cato XDR correlates individual events into "Threat Stories" — a timeline of related events suggesting an attack sequence.

Example Threat Story:
```
1. Suspicious DNS query to newly registered domain (14:02 UTC)
2. HTTP request to malicious URL from same user (14:03 UTC)
3. File download detected as potentially malicious (14:03 UTC)
4. Post-infection C2 callback detected (14:05 UTC)
→ XDR correlates: "Possible malware infection — User X, Device Y"
   Score: Critical
   Recommended action: Isolate device
```

**Investigation tools:**
- **Story timeline:** All events in chronological order
- **Entity graph:** Visual relationship map (user ↔ device ↔ destination ↔ file)
- **Raw event search:** Query all events with filters

**SOAR integration:**
Cato XDR can trigger webhooks to SOAR platforms (Palo Alto XSOAR, Splunk SOAR):
- Ticket creation in ServiceNow
- Automated device isolation
- Alert to SOC team

## Cato CTRL (Threat Research)

Cato CTRL is Cato's threat research team. Functions:
- Threat intelligence aggregation from open and commercial sources
- Original research on novel attack techniques
- CVE response and IPS signature development
- Threat hunting across Cato's global customer base (anonymized)
- Research publications: CTRL Cyber Threats Reports, vulnerability disclosures

**Intelligence delivery:** Cato CTRL updates are pushed to all 80+ PoPs continuously. No customer action required for new IOCs or IPS signatures.

## Management and Reporting

### Cato Management Application (CMA)

Single console at `cc.catonetworks.com`.

**Key sections:**
- **Network → Sites:** Cato Socket status, connectivity, WAN link health
- **Security → Policy:** FWaaS, NGFW rules
- **Security → Cloud Apps:** CASB shadow IT and policy
- **Security → DLP:** DLP profiles and policies
- **Monitoring → Dashboard:** Real-time traffic and security overview
- **Monitoring → Events:** Security event stream
- **XDR → Stories:** Threat stories and investigations
- **Reports → Executive:** CISO-level summary reporting

### SIEM Integration

**Log export:**
Cato supports syslog (CEF format) and REST API for log export.

**SIEM integrations:**
- Splunk: Cato App for Splunk (Splunkbase)
- Microsoft Sentinel: Cato connector
- Generic CEF syslog: Any SIEM that accepts CEF

**API:**
```bash
# Cato REST API (v1)
curl -H "x-api-key: {api_key}" \
     "https://api.catonetworks.com/api/v1/account/{account_id}/events"
```

### Site Provisioning

**Zero-touch provisioning:** Cato Sockets ship pre-provisioned. Plug in at branch, power on — Socket phones home to Cato cloud, downloads configuration, and is operational within minutes. No IT staff needed on-site.

**Provisioning process:**
1. Admin creates new site in CMA (name, timezone, WAN IP configuration)
2. CMA generates a provisioning token
3. Ship Socket to branch (with printed token)
4. Branch plugs in Socket; Socket connects to Cato cloud, downloads full config
5. Site is live — admin sees it turn green in CMA

**Configuration push:** All config changes in CMA are pushed to the Socket within seconds. No CLI access to individual Sockets needed for routine operations.
