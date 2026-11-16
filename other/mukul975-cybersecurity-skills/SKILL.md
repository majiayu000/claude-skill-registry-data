---
name: mukul975--cybersecurity-skills
description: "754 cybersecurity skills cho AI agent — 26 domains, map sang 5 frameworks (MITRE ATT&CK v19.1, NIST CSF 2.0, ATLAS v5.4, D3FEND v1.3, AI RMF 1.0). Real practitioner workflows."
allowed-tools: Read, Bash
user-invocable: true
---

754 structured cybersecurity skills: không phải script collection — là domain knowledge có cấu trúc để AI agent ra quyết định WHEN và HOW dùng technique.

## Install

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills
# hoặc
git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills
```

## 26 Domains (chọn lọc)

```
Detection & Response:
  threat-hunting (55)    security-operations (36)    incident-response (25)

Infrastructure:
  cloud-security (60)    network-security (40)    container-security (30)
  OT/ICS security (28)

Attack & Defense:
  web-app-security (42)    malware-analysis (39)    red-teaming (24)
  penetration-testing (23)    digital-forensics (37)

Identity & API:
  IAM (35)    api-security (28)    ransomware-defense (7)
```

## 5 Frameworks — mỗi skill map đồng thời

```
MITRE ATT&CK v19.1   — 286 techniques, 15 tactics (adversary TTPs)
NIST CSF 2.0         — 6 functions, 22 categories (org posture)
MITRE ATLAS v5.4     — 16 tactics, 84 techniques (AI/ML threats) ← unique
MITRE D3FEND v1.3    — 267 defensive techniques
NIST AI RMF 1.0      — 72 subcategories (AI risk management)
```

## Skill Structure (Progressive Disclosure)

```yaml
# Frontmatter (~30 tokens) — rapid scan
name: analyzing-network-traffic-of-malware
domain: malware-analysis
tags: [network, pcap, wireshark]
mitre_attack: T1071
nist_csf: DE.CM
atlas: AML.T0047
d3fend: D3-NTA
ai_rmf: MEASURE-2.6

# Body (500–2000 tokens) — full execution
## When to Use
## Prerequisites
## Workflow (step-by-step với commands)
## Verification
```

## Agent Workflow

```
1. Scan 754 frontmatters → identify relevant (bằng tags + domain)
2. Load top 3–5 matches full body
3. Execute Workflow section step-by-step
4. Validate với Verification section
```

## Example — Memory Dump Analysis

```
Load skills:
  performing-memory-forensics-with-volatility3
  hunting-for-credential-dumping-lsass
  analyzing-windows-event-logs-for-credential-access
→ Execute sequentially = DFIR analyst workflow
```

## Compatibility

Claude Code, Cursor, Copilot, LangChain, CrewAI, AutoGen, MCP systems, Gemini CLI

## Source

https://github.com/mukul975/Anthropic-Cybersecurity-Skills · MIT · +2192⭐/week
