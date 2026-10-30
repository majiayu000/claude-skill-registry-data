---
name: security
description: >-
  Authorized offensive and defensive security assessments, one router over
  per-surface playbooks: API, cloud/K8s, code audit & SAST review, database,
  digital forensics, EDR bypass, email, firmware, LLM/AI, malware analysis,
  OT/ICS, patch-diff exploitation, pwn and attack chains, supply chain, threat
  hunting, Windows AD, Wi-Fi, SDR radio, thick clients, hardware — plus
  pentest-tools. Use when the task is an authorized security
  assessment or code vulnerability review.
---

# security — per-surface assessment router

> Home branch in Memora: `root/skill/security`.
>
> Written authorization and scope confirmation come before any active technique.

## Choosing a part

| Surface | Part |
|---|---|
| Source-code security review, SAST triage (Semgrep/CodeQL), vulnerability audit | `parts/code-audit/` |
| REST/GraphQL/WebSocket/SOAP APIs | `parts/api-security/` |
| Cloud, containers, Kubernetes, IAM | `parts/cloud-k8s/` |
| Databases (Postgres/MySQL/MSSQL/Mongo/Redis exposure) | `parts/database-security/` |
| Memory dumps, disk timelines, PCAP forensics | `parts/digital-forensics/` |
| EDR bypass and detection reasoning | `parts/edr-bypass-re/` |
| Email security: phishing, SPF/DKIM/DMARC | `parts/email-security/` |
| Firmware and embedded devices | `parts/firmware-pentest/` |
| LLM applications and AI agents (prompt injection, tool poisoning) | `parts/llm-security/` |
| Malware static/dynamic/behavioral analysis | `parts/malware-analysis/` |
| OT/ICS, Purdue model, PLC/SCADA | `parts/ot-ics/` |
| Patch-diff (1-day) exploitation | `parts/patch-diff-exploit/` |
| Multi-stage enterprise/web attack-path planning | `parts/attack-chain/` |
| Binary/CTF pwn exploit chains | `parts/pwn-chain/` |
| Threat modeling and attack surface mapping | `parts/security-threat-model/` |
| Security ownership and blast-radius mapping | `parts/security-ownership-map/` |
| Hardened baseline security best practices | `parts/security-best-practices/` |
| Federated identity, SAML, OIDC assessments | `parts/identity-federation/` |
| Supply chain: SBOM, SCA, CI/CD | `parts/supply-chain-security/` |
| Blue-team hunting, Sigma/YARA, SIEM queries | `parts/threat-hunting/` |
| Active Directory, Kerberos, AD CS | `parts/windows-ad/` |
| Wi-Fi capture, WPA handshakes | `parts/wifi-wireless/` |
| RF/SDR signal research | `parts/radio-sdr/` |
| Desktop thick clients | `parts/thick-client/` |
| Hardware interfaces: UART/JTAG | `parts/hardware-security/` |
| General toolkit, payload templates and playbooks | `parts/pentest-tools/` |

## Rules

- Confirm target scope and active vs. passive mode via `ask_questions` before sending any network probe or payload.
- Walk `root/skill/security` in Memora before starting; record findings and verified CVEs/configs as nodes.
- Verify installed tools in the current environment; describe static checks vs. live execution in plain text in chat (no caps labels).

## Related

`reverse-engineering` (binary/bytecode analysis), `osint` (reconnaissance and exposure), `dev` (remediation and patches).
