---
name: nist-csf
description: "Knowledge base from NIST Cybersecurity Framework (CSF) 2.0. Use for cybersecurity risk management, GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER, Organizational Profiles, CSF Tiers, supply chain risk, enterprise risk management, incident response. Covers the CSF 2.0 document only; does not cover specific SP 800-53 controls, NIST RMF system authorization steps, or sector-specific regulations."
---

<!-- argument-hint: [topic, function, or chapter number] -->

# NIST Cybersecurity Framework (CSF) 2.0
**Source**: NIST CSWP 29 (US Government work, public domain) | **Chapters**: 8

## When to use
Reach for this pack when designing, assessing, or communicating about a cybersecurity program using the NIST CSF 2.0 vocabulary and structure. It is the right starting point for mapping cybersecurity outcomes to the six Functions, understanding how Profiles and Tiers work, addressing supply chain cybersecurity risk (GV.SC), or integrating cybersecurity into enterprise risk management. Also use it to orient incident response, detection, and recovery planning against NIST's authoritative outcome taxonomy.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about governance, supply chain risk, identity and access control, incident response, detection, recovery, Profiles, Tiers, or ERM integration; I read the relevant chapter.
- **With a chapter** — ask for `ch01`, `ch02`, `ch03`, `ch04`, `ch05`, `ch06`, `ch07`, or `ch08`.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Six CSF Functions
The CSF Core is organized into six Functions. GOVERN sits at the center; the other five surround it. All six operate concurrently — GOVERN, IDENTIFY, PROTECT, and DETECT run continuously; RESPOND and RECOVER must be ready at all times.

| Function | Identifier | Core question answered |
|----------|-----------|----------------------|
| **GOVERN** | GV | How does the organization set cybersecurity strategy, policy, and oversight? |
| **IDENTIFY** | ID | What are our assets and what cybersecurity risks do they face? |
| **PROTECT** | PR | What safeguards prevent or reduce the impact of adverse events? |
| **DETECT** | DE | How do we find cybersecurity attacks and compromises in progress? |
| **RESPOND** | RS | What actions do we take once an incident is declared? |
| **RECOVER** | RC | How do we restore normal operations after an incident? |

### GOVERN (GV) — Six Categories
- **GV.OC** — Organizational Context: mission, stakeholders, dependencies, legal/regulatory obligations
- **GV.RM** — Risk Management Strategy: risk appetite, risk tolerance, standardized risk method, ERM integration
- **GV.RR** — Roles, Responsibilities, Authorities: accountability, resources, HR integration
- **GV.PO** — Policy: establishment, enforcement, periodic review
- **GV.OV** — Oversight: results feed strategy adjustments (the governance feedback loop)
- **GV.SC** — Cybersecurity Supply Chain Risk Management: full supplier life cycle from due diligence through post-relationship obligations

### IDENTIFY (ID) — Three Categories
- **ID.AM** — Asset Management: inventory of hardware, software, data, network flows, supplier services; life-cycle management; criticality classification
- **ID.RA** — Risk Assessment: vulnerability identification, threat intelligence, likelihood/impact estimation, risk response prioritization
- **ID.IM** — Improvement: continuous learning from evaluations, exercises, operations, and incident plan maintenance

### PROTECT (PR) — Five Categories
- **PR.AA** — Identity Management, Authentication, and Access Control: credential management, identity proofing, authentication, least privilege, separation of duties, physical access
- **PR.AT** — Awareness and Training: general and specialized-role training
- **PR.DS** — Data Security: at-rest, in-transit, and in-use data protection; tested backups
- **PR.PS** — Platform Security: configuration management, software/hardware maintenance, log generation, unauthorized software prevention, secure development life cycle
- **PR.IR** — Technology Infrastructure Resilience: network protection, environmental threat protection, resilience mechanisms, capacity management

### DETECT (DE) — Two Categories
- **DE.CM** — Continuous Monitoring: networks, physical environments, personnel activity, external service providers, computing hardware/software/runtime
- **DE.AE** — Adverse Event Analysis: correlation across sources, impact/scope estimation, threat intelligence integration, incident declaration (DE.AE-08)

### RESPOND (RS) — Four Categories
- **RS.MA** — Incident Management: plan execution, triage, categorization, prioritization, escalation, recovery criteria
- **RS.AN** — Incident Analysis: root cause establishment, record integrity/provenance preservation, magnitude validation
- **RS.CO** — Incident Response Reporting and Communication: stakeholder notification, information sharing
- **RS.MI** — Incident Mitigation: containment, eradication

### RECOVER (RC) — Two Categories
- **RC.RP** — Incident Recovery Plan Execution: recovery action selection, backup integrity verification (RC.RP-03), post-incident operational norms (RC.RP-04), restoration verification, formal recovery declaration (RC.RP-06)
- **RC.CO** — Incident Recovery Communication: stakeholder coordination, approved public messaging

### Organizational Profiles and Tiers

**Profiles** translate Core outcomes into documented posture:
- **Current Profile** — what the organization is achieving now
- **Target Profile** — prioritized desired outcomes given mission, risk appetite, and threat landscape
- **Gap analysis** — comparison driving a prioritized action plan (risk register, POA&M)
- **Community Profile** — sector-specific published baseline usable as a Target Profile starting point

**Tiers** characterize governance and management rigor:

| Tier | Name | Governance | Management |
|------|------|-----------|-----------|
| 1 | Partial | Ad hoc | Limited organizational awareness |
| 2 | Risk Informed | Ad hoc, not formally based on objectives | Irregular, case-by-case implementation |
| 3 | Repeatable | Formally approved, expressed as policy | Organization-wide approach; cybersecurity information shared routinely |
| 4 | Adaptive | Risk-informed, culturally embedded, predictive | Adapts based on lessons learned; real-time supply chain risk information |

**Key decision rule**: Progress to higher Tiers only when risks/mandates are greater OR cost-benefit analysis justifies it. Tier 4 is not a universal target.

### CSF and Enterprise Risk Management
The CSF explicitly integrates with ERM: GV.RM-03 requires cybersecurity risk activities to be included in enterprise risk management processes. The CSF helps translate cybersecurity terminology into general risk language that executives understand. NIST IR 8286 series provides detailed integration guidance. Cybersecurity risk sits alongside financial, privacy, supply chain, and reputational risks in the enterprise risk portfolio.

### Key Interlock Points (cross-Function dependencies)
- **PROTECT → DETECT**: PR.PS-04 log generation is the monitoring substrate DE.CM requires.
- **PROTECT → RECOVER**: PR.DS-11 tested backups must exist before RC.RP-03 backup integrity verification can occur.
- **DETECT → RESPOND**: DE.AE-08 incident declaration is the formal trigger for RS.MA.
- **RESPOND → RECOVER**: RS.MA-05 recovery initiation criteria gate the transition to RC.RP.
- **RECOVER → IDENTIFY**: RC.RP-06 documentation feeds ID.IM improvement identification.
- **IDENTIFY → GOVERN**: ID.IM improvements escalate to GV.PO and GV.OV for strategy and policy updates.

## Chapter Index
| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-csf-overview-and-components.md) | CSF Overview and Components | Core, Profiles, Tiers, Informative References, Implementation Examples, QSGs |
| [ch02](chapters/ch02-govern-gv.md) | GOVERN (GV) Function | GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC; risk appetite; C-SCRM; ERM integration |
| [ch03](chapters/ch03-identify-id.md) | IDENTIFY (ID) Function | ID.AM, ID.RA, ID.IM; asset inventories; threat intelligence; risk assessment; continuous improvement |
| [ch04](chapters/ch04-protect-pr.md) | PROTECT (PR) Function | PR.AA, PR.AT, PR.DS, PR.PS, PR.IR; least privilege; data security; platform security; resilience |
| [ch05](chapters/ch05-detect-de.md) | DETECT (DE) Function | DE.CM, DE.AE; continuous monitoring; anomaly detection; incident declaration criteria |
| [ch06](chapters/ch06-respond-rs.md) | RESPOND (RS) Function | RS.MA, RS.AN, RS.CO, RS.MI; triage; root cause; containment; eradication; communication |
| [ch07](chapters/ch07-recover-rc.md) | RECOVER (RC) Function | RC.RP, RC.CO; backup integrity; post-incident norms; recovery declaration; public messaging |
| [ch08](chapters/ch08-profiles-tiers-and-using-the-csf.md) | Organizational Profiles, Tiers, and Using the CSF | Current/Target Profiles; gap analysis; POA&M; Tier 1-4 descriptors; ERM integration; bidirectional communication |

## Topic Index
- **Access control / least privilege / separation of duties** → ch04 (PR.AA)
- **Adaptive (Tier 4)** → ch08
- **Asset inventory / asset management** → ch03 (ID.AM)
- **Awareness and training** → ch04 (PR.AT)
- **Backup / data recovery** → ch04 (PR.DS-11), ch07 (RC.RP-03)
- **Community Profile** → ch01, ch08
- **Continuous monitoring** → ch05 (DE.CM)
- **C-SCRM / supply chain risk** → ch02 (GV.SC)
- **Current Profile / Target Profile** → ch08
- **Data security (at rest / in transit / in use)** → ch04 (PR.DS)
- **DETECT function overview** → ch05
- **Enterprise risk management (ERM)** → ch02 (GV.RM-03), ch08
- **Gap analysis / action plan / POA&M** → ch08
- **GOVERN function overview** → ch02
- **Identification of assets** → ch03 (ID.AM)
- **IDENTIFY function overview** → ch03
- **Incident declaration** → ch05 (DE.AE-08)
- **Incident management / triage** → ch06 (RS.MA)
- **Incident response plan** → ch03 (ID.IM-04), ch06
- **Improvement / lessons learned** → ch03 (ID.IM)
- **Indicators of compromise** → ch05 (DE.CM)
- **Informative References** → ch01
- **KPIs / KRIs / reporting** → ch08
- **Organizational Profile** → ch01, ch08
- **Oversight / feedback loop** → ch02 (GV.OV)
- **Partial (Tier 1)** → ch08
- **Platform security / configuration management** → ch04 (PR.PS)
- **Policy** → ch02 (GV.PO)
- **Privacy risk** → ch01, ch08
- **Quick-Start Guides (QSGs)** → ch01
- **RECOVER function overview** → ch07
- **Recovery declaration** → ch07 (RC.RP-06)
- **Repeatable (Tier 3)** → ch08
- **RESPOND function overview** → ch06
- **Risk appetite / risk tolerance** → ch02 (GV.RM-02)
- **Risk assessment** → ch03 (ID.RA)
- **Risk Informed (Tier 2)** → ch08
- **Roles, responsibilities, authorities** → ch02 (GV.RR)
- **Root cause analysis** → ch06 (RS.AN-03)
- **Secure software development** → ch04 (PR.PS-06)
- **Supplier / third-party risk** → ch02 (GV.SC), ch03 (ID.RA-09, ID.RA-10)
- **Technology infrastructure resilience** → ch04 (PR.IR)
- **Threat intelligence** → ch03 (ID.RA-02), ch05 (DE.AE-07)
- **Tiers overview** → ch08

## Supporting Files
- [glossary.md](glossary.md) — alphabetical definitions for ~45 CSF 2.0 terms with chapter references
- [patterns.md](patterns.md) — 12 named patterns with When/How/Trade-offs for implementing CSF outcomes
- [cheatsheet.md](cheatsheet.md) — decision rules, function/category quick-reference table, and tells & smells

---

## Scope & Limits
This pack covers NIST CSWP 29 (CSF 2.0) as published February 26, 2024 — the framework document itself, including the CSF Core (Appendix A), Tiers (Appendix B), and Glossary (Appendix C). It does not cover the content of Informative References (e.g., SP 800-53 control details, SP 800-161r1 C-SCRM practices, NIST RMF authorization steps), sector-specific Community Profiles, or the CSF 2.0 online Reference Tool. This is a US Government public domain work; no copyright restrictions apply to the source document.
