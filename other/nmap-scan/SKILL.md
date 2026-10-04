---
type: skill
name: nmap-scan
description: nmap network scanning and service enumeration tool. Use when performing host discovery, port scanning, service/version detection, OS fingerprinting, vulnerability scanning with NSE scripts or generating structured output for security automation.
last_updated: "2026-02-18"
doc_source: https://nmap.org/docs.html
---

# Nmap

Nmap (Network Mapper) is a powerful open-source tool used for network discovery, port scanning, service enumeration, OS detection, and vulnerability assessment.

---

## Table of Contents

- [Core Concepts](#core-concepts)
- [Host Discovery](#host-discovery)
- [Port Scanning Techniques](#port-scanning-techniques)
- [Service & Version Detection](#service--version-detection)
- [OS Detection](#os-detection)
- [NSE (Nmap Scripting Engine)](#nse-nmap-scripting-engine)
- [Output Formats](#output-formats)
- [Common Recon Workflows](#common-recon-workflows)
- [Performance Optimization](#performance-optimization)
- [Automation & Parsing](#automation--parsing)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [References](#references)

---

# Core Concepts

| Concept | Description |
|----------|-------------|
| **Target** | IP address, range, hostname, or subnet |
| **Port State** | open, closed, filtered |
| **Service Detection** | Identifies running service + version |
| **OS Fingerprinting** | Determines likely operating system |
| **NSE** | Lua-based scripting engine for advanced scanning |
| **Stealth Scan** | SYN scan that avoids full TCP handshake |

---

# Host Discovery

Ping scan (no port scan):

```bash
nmap -sn 192.168.1.0/24
```

Disable ping (scan even if ICMP blocked):

```bash
nmap -Pn target.com
```

ARP discovery (local network):

```bash
nmap -PR 192.168.1.0/24
```

---

# Port Scanning Techniques

## TCP SYN Scan (Default + Stealth)

```bash
nmap -sS target.com
```

## TCP Connect Scan

```bash
nmap -sT target.com
```

## UDP Scan

```bash
nmap -sU target.com
```

## Scan Specific Ports

```bash
nmap -p 22,80,443 target.com
```

Range:

```bash
nmap -p 1-1000 target.com
```

All ports:

```bash
nmap -p- target.com
```

---

# Service & Version Detection

```bash
nmap -sV target.com
```

Aggressive detection:

```bash
nmap -sV --version-intensity 9 target.com
```

Combine with full port scan:

```bash
nmap -sS -sV -p- target.com
```

---

# OS Detection

```bash
nmap -O target.com
```

Aggressive mode (includes OS, version, traceroute, scripts):

```bash
nmap -A target.com
```

---

# NSE (Nmap Scripting Engine)

List available scripts:

```bash
ls /usr/share/nmap/scripts/
```

Run default scripts:

```bash
nmap -sC target.com
```

Run specific script:

```bash
nmap --script=http-title target.com
```

Run category:

```bash
nmap --script=vuln target.com
```

Run multiple scripts:

```bash
nmap --script=http-enum,http-headers target.com
```

Pass script arguments:

```bash
nmap --script ftp-anon --script-args ftp-anon.maxlist=50 target.com
```

---

# Output Formats

## Normal Output

```bash
nmap target.com
```

## Grepable Output

```bash
nmap -oG output.gnmap target.com
```

## XML (Best for automation)

```bash
nmap -oX output.xml target.com
```

## All Formats

```bash
nmap -oA scan_results target.com
```

Produces:
- scan_results.nmap
- scan_results.xml
- scan_results.gnmap

---

# Common Recon Workflows

## Quick Recon

```bash
nmap -T4 -F target.com
```

---

## Full TCP Enumeration

```bash
nmap -sS -sV -O -p- -T4 target.com
```

---

## Vulnerability Scan

```bash
nmap -sV --script=vuln target.com
```

---

## Web Enumeration

```bash
nmap -p 80,443 --script=http-enum,http-title,http-headers target.com
```

---

## Internal Network Scan

```bash
nmap -sn 10.0.0.0/16
nmap -sS -sV 10.0.0.5
```

---

# Performance Optimization

Timing templates:

| Option | Speed |
|--------|-------|
| -T0 | Paranoid |
| -T1 | Sneaky |
| -T2 | Polite |
| -T3 | Normal |
| -T4 | Aggressive |
| -T5 | Insane |

Example:

```bash
nmap -T4 -p- target.com
```

Limit rate:

```bash
nmap --max-rate 500 target.com
```

Parallelism control:

```bash
nmap --min-parallelism 50 target.com
```

---

# Automation & Parsing

Preferred format for automation:

```bash
nmap -oX scan.xml target.com
```

Convert XML to JSON:

```bash
xsltproc /usr/share/nmap/nmap.xsl scan.xml -o scan.html
```

Extract open ports via grepable output:

```bash
nmap -oG - target.com | grep open
```

Use in pipelines:

```bash
nmap -p- -oG - target.com | awk '/open/ {print $2,$5}'
```

---

# Troubleshooting

## All Ports Show Filtered

Possible causes:
- Firewall blocking probes
- IDS/IPS interference
- Wrong network interface

Try:

```bash
nmap -Pn target.com
```

---

## Scan Is Too Slow

- Use `-T4`
- Scan specific ports
- Avoid UDP unless necessary
- Reduce NSE scripts

---

## Permission Errors

SYN scans require root:

```bash
sudo nmap -sS target.com
```

---

## No OS Detection Result

- Target must have at least one open and one closed port
- Try full port scan first

---

# Best Practices

- Always start with host discovery (`-sn`)
- Use `-p-` only when necessary
- Prefer XML output for automation
- Avoid aggressive scanning in production environments
- Combine with other tools (dirsearch, ffuf, nikto)
- Document scan scope before execution

---

# AWS Integration

## Feedback Loop Integration

Nmap is used to run external network reachability probes — with no AWS credentials — directly against AWS endpoints. Under the External Probe path, nmap results bypass the pipeline and return directly. While AWS CLI checks verify *configuration*, nmap verifies *actual network reachability* from outside the account.

Probe commands per service are in `skills/validation-rules/probes.md`. Service-specific endpoint discovery is in each service skill (e.g., `skills/ec2/SKILL.md`, `skills/rds/SKILL.md`).

### Workflow: Validate Security Group Findings

1. **Director** identifies a security group claim (e.g., `qa-sg-open`)
2. **Expert** retrieves the public IP and runs nmap to confirm reachability
3. **Critic** scores based on both config evidence (AWS CLI) and active evidence (nmap)

Step 1 — Get public IPs for instances in the security group:

```bash
aws ec2 describe-instances \
  --filters "Name=instance.group-id,Values=sg-0123456789abcdef0" \
  --query "Reservations[].Instances[].[InstanceId,PublicIpAddress]" \
  --output table
```

Step 2 — Scan the ports the security group allows from 0.0.0.0/0:

```bash
nmap -sS -Pn -p 22,80,443,3389 <public-ip> -oX scan_results.xml
```

Step 3 — Compare nmap results against security group rules. A port that is open in the SG but filtered in nmap may indicate a host-level firewall or NACL blocking traffic.

### Common AWS Validation Scans

Verify SSH exposure:

```bash
nmap -sS -Pn -p 22 <public-ip>
```

Verify RDS is not publicly reachable (should show filtered/closed):

```bash
nmap -sS -Pn -p 3306,5432 <rds-endpoint>
```

Verify only HTTPS is open on an ALB:

```bash
nmap -sS -Pn -p 80,443 <alb-dns-name>
```

Check for unexpected open ports on a public instance:

```bash
nmap -sS -Pn -p- -T4 <public-ip> -oX full_scan.xml
```

Verify ElastiCache/OpenSearch are not internet-exposed (should timeout/filter):

```bash
nmap -sS -Pn -p 6379,9200,9300 <endpoint>
```

For Critic scoring of nmap probe results, see the Scoring Rubric and Service exceptions in `agents/roles.md`.

---

# Safe & Legal Usage

- Only scan systems you own or have written authorization to test
- **AWS Penetration Testing Policy**: AWS allows scanning your own EC2, RDS, Aurora, CloudFront, API Gateway, Lambda, Lightsail, and Elastic Beanstalk resources without prior approval. Other services require approval — see [AWS pen test policy](https://aws.amazon.com/security/penetration-testing/)
- Nmap scans **will trigger GuardDuty alerts** (e.g., `Recon:EC2/Portscan`) — inform the account owner before scanning
- Avoid aggressive timing (`-T5`) against production workloads
- Follow responsible disclosure practices
- Document scan scope and authorization before execution

---

# References

- https://nmap.org/docs.html
- https://nmap.org/book/man.html
- https://nmap.org/nsedoc/
- https://nmap.org/book/nse.html

---

# End of Skill