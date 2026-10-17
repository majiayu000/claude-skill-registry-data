---
name: best-hacker
description: Use when apply hacker mindset to find vulnerabilities, break assumptions,
  and stress-test systems before attackers do. Use when working with best hacker.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- best
- hacker
- investigation
- research
version: 1.0.0
category: research
---

# The Hacker Mindset

## Overview

**Best Hacker** channels elite offensive security methodology — finding vulnerabilities through creative exploitation, chaining weaknesses, and thinking like an adversary to strengthen systems.



## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use

**Trigger phrases:**
- "best hacker"
- "Help me with best hacker"

**Use cases:**
- When the task matches this skill's domain expertise

---

## Core Philosophy

> "Security through obscurity is no security at all." — Hacker Creed

### The Hacker Ethos:

1. **Curiosity** - Always ask "what if?"
2. **Impatience** - Don't wait for official channels
3. **Playfulness** - See problems as puzzles
4. **Persistence** - Try 1000 ways, not just 1
5. **Minimalism** - Simplest path to goal

## Attack Methodology

Structured approach: recon, enumeration, exploitation, post-exploitation.


### 1. Reconnaissance

> "To beat the system, know the system."

**Information Gathering:**
- OSINT (Open Source Intelligence)
- Social media profiling
- Company org charts
- Technology stack discovery
- Employee information

**Tools:**
- LinkedIn, Facebook, Twitter
- Company websites, press releases
- Job postings (reveals tech stack)
- Shodan, Censys for infrastructure

### 2. Vulnerability Identification

**The Attack Surface:**
```
Entry Points:
├── Web apps (port 80, 443)
├── Email (port 25, 587)
├── VPN (port 443, 1194)
├── Cloud services
├── Mobile apps
└── Social engineering
```

**Vulnerability Classes:**
- Technical: SQL injection, XSS, buffer overflow
- Config: default passwords, exposed files
- Human: phishing, social engineering
- Physical: badge cloning, tailgating

### 3. Exploitation

**The Exploit Chain:**
1. Find weakness → Gain access → Escalate → Maintain → Exfiltrate

**Common Exploits:**
- Credential stuffing
- Privilege escalation
- Buffer overflow
- DLL hijacking
- Session hijacking

## Defense Through Offense

Understanding attack patterns to build better defenses.


### Think Like Attacker:

```
What would I do if I wanted to:
├── Steal this data?
├── Take this system down?
├── Access this network?
└── Impersonate this user?
```

### Security Checklist:

- [ ] Multi-factor authentication everywhere
- [ ] Least privilege access
- [ ] Network segmentation
- [ ] Regular penetration testing
- [ ] Employee security training
- [ ] Incident response plan
- [ ] Logging and monitoring
- [ ] Regular patches/updates

### The 3 Defense Layers:

1. **Perimeter** - Firewall, WAF, VPN
2. **Internal** - Network segmentation, IAM
3. **Endpoint** - EDR, antivirus, encryption

## Red Team Framework

Rules of engagement, scope boundaries, and reporting standards.


### Assessment Process:

1. **Planning**: Define scope, goals, rules
2. **Recon**: Gather intelligence
3. **Scanning**: Find vulnerabilities
4. **Exploitation**: Test attacks
5. **Documentation**: Report findings

### Purple Team (Offense + Defense):

- Both teams work together
- Real-time learning
- Continuous improvement

---


## When NOT to Use

- When the research requires access to proprietary databases or paywalled sources
- When findings will be used for financial decisions requiring licensed advisor review
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Research relies on a single unverified source
- Agent presents speculation as confirmed findings
- Watch for shortcuts and skipped steps


## Workflow

1. **Understand requirements** — Clarify objectives and scope
2. **Set up tools** — Configure required tools and access
3. **Execute** — Perform the core operations
4. **Validate** — Verify results meet quality standards
5. **Document** — Record findings and decisions


## Process

1. **Reconnaissance** — Gather target information, identify attack surface, enumerate services
1. **Analysis/Exploitation** — Execute the technique, analyze results, document findings
1. **Reporting** — Document IOCs, write findings, provide remediation recommendations

## Verification

After completing this skill, confirm:

- [ ] Findings are verified across multiple independent sources
- [ ] Research methodology is documented and reproducible
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `systematic-debugging` - Finding problems
- `security-reviewer` - Security analysis
- `code-reviewer` - Finding code vulnerabilities
- `verification-before-completion` - Testing
