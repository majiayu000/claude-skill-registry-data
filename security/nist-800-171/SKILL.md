---
name: nist-800-171
description: "Knowledge base from NIST SP 800-171 Rev. 3 (Protecting CUI in Nonfederal Systems). Use for CUI confidentiality requirements on contractors and other nonfederal organizations, the 17 requirement families, ODPs, SSPs, POA&Ms, and tailoring from SP 800-53. Covers 800-171r3 only; does not replace SP 800-171A assessment procedures, full SP 800-53 baselines, CMMC scoring mechanics, or classified-information controls."
---

<!-- argument-hint: [topic, family, or chapter number] -->

# NIST SP 800-171 Rev. 3 — Protecting CUI in Nonfederal Systems
**Source**: NIST SP 800-171r3 (US Government work, public domain) | **Chapters**: 8

## When to use
Reach for this pack when scoping, implementing, or assessing security requirements for Controlled Unclassified Information on nonfederal systems — typically under federal contracts or agreements. It is the right starting point for mapping the 17 requirement families, filling organization-defined parameters, writing or reviewing a system security plan, tracking deficiencies in POA&Ms, isolating CUI components, or understanding how 800-171 was tailored from the SP 800-53 moderate baseline.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about CUI scope, a family (e.g., access control, incident response, supply chain), ODPs, SSP, POA&M, media sanitization, MFA, or SCRM; I read the relevant chapter.
- **With a chapter** — ask for `ch01` through `ch08`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### Purpose and applicability
SP 800-171r3 gives federal agencies recommended security requirements to protect CUI confidentiality when that information resides in nonfederal systems and no category-specific safeguarding instrument already prescribes controls. Requirements apply only to components that process, store, or transmit CUI (or protect those components). Organizations operating systems *on behalf of* a federal agency are under FISMA, not this nonfederal CUI set.

### Derivation and tailoring
Starting from SP 800-53 controls in the SP 800-53B moderate baseline, NIST removed items that are primarily a federal responsibility, unrelated to CUI confidentiality, adequately covered elsewhere, or not applicable. Assumptions include: CUI has the same value in federal and nonfederal custody; safeguards should be consistent; confidentiality impact is no less than moderate; nonfederal orgs may use external providers.

### Seventeen requirement families
| Family | Focus |
|--------|--------|
| Access Control | Accounts, least privilege, remote/mobile/wireless, flow control |
| Awareness and Training | Literacy + role-based training |
| Audit and Accountability | Logging, review, time stamps, log protection |
| Configuration Management | Baselines, change control, least functionality, inventory |
| Identification and Authentication | Unique ID, MFA, authenticators, passwords |
| Incident Response | Handling capability, plan, test, train, report |
| Maintenance | Tools, nonlocal sessions, personnel |
| Media Protection | Store, mark, transport, sanitize, backup crypto |
| Personnel Security | Screening, termination/transfer |
| Physical Protection | Facility access, monitoring, alternate sites, transmission lines |
| Risk Assessment | Assess risk, vulnerability monitoring, risk response |
| Security Assessment and Monitoring | Assess controls, POA&M, continuous monitoring, exchanges |
| System and Communications Protection | Boundaries, crypto, deny-by-default, sessions |
| System and Information Integrity | Patching, malware, alerts, monitoring, retention |
| Planning | Policies, system security plan, rules of behavior |
| System and Services Acquisition | Security engineering, unsupported components, external services |
| Supply Chain Risk Management | SCRM plan, acquisition strategies, supplier requirements |

### Organization-defined parameters (ODPs)
Many requirements contain assignment/selection operations. Agencies (or consortia) should set values; if they do not, the nonfederal organization must assign values to complete the requirement. Once set, ODP values are part of the requirement and drive consistent assessment.

### Requirement structure
Each requirement has a normative statement, an informative discussion (not a scope expansion), and references to source SP 800-53 controls plus supporting publications. Example pattern: cryptographic protection types are assigned via ODP; discussion recommends FIPS-validated cryptography.

### Scoping and exceptions
Isolate CUI components into separate security domains (physical and/or logical) to avoid over-hardening the entire enterprise. Document enduring limitations (e.g., specialized systems) in the SSP (03.15.02). Manage temporary deficiencies through POA&Ms (03.12.02).

### Assessment companion
SP 800-171A provides assessment procedures. This pack explains *what* the requirements mean; 171A explains *how to assess* them.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-cui-scope-fundamentals-and-structure.md) | CUI Scope, Fundamentals, and Structure | Applicability, tailoring, 17 families, ODPs, SSP/POA&M exception paths |
| [ch02](chapters/ch02-access-control-and-identification.md) | Access Control + Identification & Authentication | Accounts, least privilege, remote/mobile, MFA, authenticators |
| [ch03](chapters/ch03-awareness-personnel-physical.md) | Awareness, Personnel, Physical | Training, screening, offboarding, facility and alternate-site controls |
| [ch04](chapters/ch04-audit-and-configuration.md) | Audit + Configuration Management | Logging lifecycle, baselines, change control, allow-by-exception software |
| [ch05](chapters/ch05-incident-maintenance-media.md) | Incident Response, Maintenance, Media | IR plan/capability, nonlocal maintenance, media sanitization and backup crypto |
| [ch06](chapters/ch06-risk-assessment-monitoring-planning.md) | Risk, Assessment & Monitoring, Planning | Risk response, POA&M, continuous monitoring, SSP, rules of behavior |
| [ch07](chapters/ch07-communications-and-integrity.md) | Communications Protection + Integrity | Boundaries, cryptography, patching, malware, system monitoring |
| [ch08](chapters/ch08-acquisition-and-supply-chain.md) | Acquisition + Supply Chain Risk Management | Security engineering, external services, SCRM plan and supplier flow-down |

## Topic Index
- **Access control / least privilege** → ch02
- **Alternate work site** → ch03
- **Audit logging / time stamps** → ch04
- **Authenticator / password management** → ch02
- **Backup confidentiality / media crypto** → ch05, ch07
- **Boundary protection / deny by default** → ch07
- **Configuration baseline / change control** → ch04
- **Continuous monitoring** → ch06
- **Cryptographic protection / key management** → ch07
- **CUI definition and scope** → ch01
- **External system services / cloud providers** → ch08
- **Flaw remediation / patching** → ch07
- **Incident response plan / handling** → ch05
- **Information exchange agreements** → ch06
- **Information flow enforcement** → ch02
- **Malicious code protection** → ch07
- **Media sanitization / marking / transport** → ch05
- **Multi-factor authentication (MFA)** → ch02
- **Nonlocal maintenance** → ch05
- **Organization-defined parameters (ODPs)** → ch01, ch06
- **Personnel screening / termination** → ch03
- **Physical access control** → ch03
- **Plan of action and milestones (POA&M)** → ch06
- **Remote / wireless / mobile access** → ch02
- **Risk assessment / vulnerability scanning** → ch06
- **Rules of behavior** → ch06
- **Security assessment** → ch06
- **Security engineering principles** → ch08
- **Supply chain risk management (SCRM)** → ch08
- **System security plan (SSP)** → ch01, ch06
- **Tailoring from SP 800-53** → ch01
- **Training (literacy and role-based)** → ch03
- **Unsupported / end-of-life components** → ch08

## Supporting Files
- [glossary.md](glossary.md) — key 800-171 / CUI terms with chapter references
- [patterns.md](patterns.md) — implementation patterns (When / How / Trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, family map, tells & smells

---

## Scope & Limits
This pack covers NIST SP 800-171 Revision 3 (final 2024-05-14, DOI 10.6028/NIST.SP.800-171r3) — purpose, fundamentals, and the 17 security requirement families as synthesized reference notes. It does **not** cover: SP 800-171A assessment procedures in full; SP 800-53 control catalog detail beyond provenance; CMMC level scoring or assessment guides; DFARS solicitation clauses as legal advice; classified information (EO 13526) controls; or sector-specific CUI category instruments that supersede the moderate baseline. US Government public domain work; no copyright restrictions on the source document. No source-material download link is published.
