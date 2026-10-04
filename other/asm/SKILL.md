---
name: asm
description: "Routing agent for External Attack Surface Management (EASM). Covers internet asset discovery, shadow IT, exposure identification, and routes to platform-specific agents for Falcon Surface, Xpanse, Defender EASM, and Censys. WHEN: \"attack surface management\", \"EASM\", \"external attack surface\", \"internet-exposed assets\", \"shadow IT discovery\", \"unknown assets\", \"ASM\". Do NOT use for platform-specific questions -- use the `falcon-surface`, `xpanse`, `defender-easm`, or `censys` skill."
license: MIT
---

# Attack Surface Management (ASM)

This skill covers External Attack Surface Management (EASM) and Attack Surface Management (ASM). It provides expertise in ASM concepts, internet asset discovery methodologies, and the operational workflow for managing an organization's external exposure. Read the relevant sibling skill for platform implementation details.

## What is Attack Surface Management?

External Attack Surface Management (EASM) continuously discovers, monitors, and analyzes internet-facing digital assets -- including assets the organization may not know exist.

**The core problem EASM solves:**
Traditional VM programs manage known assets. But attackers don't limit themselves to your CMDB. They scan the entire internet and find:
- Forgotten development environments left running
- Shadow IT (systems stood up by business units without IT knowledge)
- Misconfigured cloud resources with public endpoints
- Acquired company assets not yet inventoried
- Expired SSL certificates on exposed services
- Open ports and services that should be internal-only
- Leaked credentials and API keys reachable from the internet

EASM discovers these from the attacker's perspective -- outside-in.

## How EASM Tools Work

**Discovery methods:**
1. **Domain enumeration:** Start with known domains (company.com), enumerate subdomains via DNS brute force, certificate transparency logs (crt.sh), zone transfers, passive DNS
2. **IP range scanning:** Scan known IP ranges (BGP ASN ownership, WHOIS data) for open services
3. **Certificate transparency:** SSL certificate logs reveal subdomains and associated IPs
4. **Internet-wide scanning data:** Tools like Shodan, Censys, FOFA index the entire internet daily; EASM tools leverage or replicate this data
5. **WHOIS / RDAP:** Ownership data for IP ranges and domains
6. **Web crawling:** Discover linked assets, JavaScript-embedded endpoints, APIs
7. **Correlation:** Link discovered assets back to the organization via certificate subjects, HTML content, technology fingerprints, email addresses in TLS certs

**Asset types discovered:**
- Domains and subdomains (internal.company.com, dev.api.company.com)
- IP addresses and CIDR ranges (including cloud-assigned IPs)
- Web applications and APIs (including staging/dev/test environments)
- Open ports and services (RDP, SSH, databases exposed to internet)
- SSL/TLS certificates (including expired or expiring certificates)
- Cloud storage (public S3 buckets, Azure Blobs, GCS buckets)
- Code repositories (GitHub, GitLab with sensitive data)
- Third-party and SaaS services (shadow IT)

## EASM vs. Traditional VM

| Dimension | Traditional VM | EASM |
|---|---|---|
| **Asset source** | Known CMDB/scanner targets | Discovered from internet (outside-in) |
| **Scope** | Internal + known internet-facing | Internet-facing, unknown to org |
| **Attacker perspective** | No | Yes -- finds what attackers find |
| **Asset discovery** | You know what you're scanning | Discovery is the primary function |
| **Shadow IT** | Not covered | Core use case |
| **Continuous** | Scheduled scans | Continuous internet monitoring |
| **Coverage** | Depends on CMDB accuracy | Doesn't depend on asset knowledge |

**Complementary, not competitive:** EASM and VM work together. EASM feeds newly discovered assets back to VM for credentialed vulnerability scanning. EASM provides the "what is exposed" layer; VM provides the "how vulnerable is it" layer.

## Key EASM Workflows

### Initial Asset Discovery

1. **Seed data:** Provide known domains, IP ranges, company names, subsidiaries
2. **Discovery run:** Tool enumerates internet assets using seed data
3. **Attribution review:** Validate discovered assets belong to your org (rule out false positives)
4. **Asset acceptance:** Accept assets into monitored inventory
5. **Risk baseline:** Initial exposure score established

### Continuous Monitoring

- Daily re-scan of all discovered assets
- Alert on: New asset discovered, new open port, SSL certificate expiring, new vulnerability on exposed service
- Drift detection: Service was closed, now it's open again

### Integration with VM

**EASM → VM workflow:**
1. EASM discovers new internet-exposed host
2. Alert sent to VM team (ServiceNow ticket, Slack alert)
3. VM team adds host to scanner (Tenable, Qualys, Rapid7)
4. Credentialed vulnerability scan run
5. Findings managed in VM platform with standard SLA
6. EASM continues monitoring external exposure

### Attack Surface Reduction

Core EASM outcomes:
- **Minimize exposure:** Shut down services that shouldn't be public
- **Harden exposed services:** Ensure everything exposed has MFA, current patches, proper TLS
- **Track debt:** Know exactly what is exposed and why
- **Incident readiness:** When a new CVE drops, immediately know if any exposed services are affected

## Technology Routing

Read these sibling skills for platform-specific implementation:

| Request Pattern | Route To |
|---|---|
| CrowdStrike Falcon Surface, EASM + endpoint correlation | `falcon-surface` |
| Palo Alto Cortex Xpanse, automated remediation, Xpanse API | `xpanse` |
| Microsoft Defender EASM, Azure integration | `defender-easm` |
| Censys, internet scanning, certificate analysis | `censys` |

## EASM Evaluation Criteria

When selecting an EASM platform:

| Criterion | Questions to Ask |
|---|---|
| **Discovery breadth** | How complete is their internet scan? Daily refresh? |
| **Attribution accuracy** | How well does it tie discoveries back to your org? FP rate? |
| **Asset context** | Does it show technology stack, open ports, SSL details? |
| **VM integration** | Can it feed new assets to Tenable/Qualys/Rapid7 automatically? |
| **EDR correlation** | Can it correlate external exposure with internal endpoint data? |
| **Remediation workflow** | Does it track remediation, integrate with ITSM? |
| **Subsidiary/acquisition support** | Can it monitor multiple legal entities? |
| **Cloud coverage** | Does it discover cloud-specific exposure (public S3, exposed DB)? |
