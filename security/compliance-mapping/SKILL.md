---
name: compliance-mapping
description: >
  A high-level conceptual mapping from Active Directory attack techniques to the compliance
  controls they touch. Kerberoasting relates to authentication and logging, so it brushes
  ENS op.acc.5 / op.exp.8, NIS2 Art.21(2)(h), DORA RTS Art.9 / Art.21. Use this when a
  reader wants to understand which regulatory control an AD finding relates to, or to add an
  orientation note to a technical finding. This is a conceptual, orientative mapping only;
  it is NOT an auditor-defensible, curated, ID-by-ID control matrix. Covers ENS (op.acc.*,
  op.exp.*), NIS2 (Directive 2022/2555 Art.21), and DORA (RTS 2024/1774).
---

# AD Technique → Compliance Control (Conceptual Mapping)

> **Disclaimer, read first.** This is a *conceptual, orientative* mapping. It shows, at a
> high level, which family of controls an AD attack technique relates to, so a practitioner
> can point a finding in the right regulatory direction. **It is not an auditor-defensible
> control matrix.** A defensible mapping (one an auditor accepts, cross-referenced ID by ID
> to the exact control text, scoped to your organization's applicability statement, with
> evidence per control) is a curated product, not something you infer from a technique name.
> ADscan (free and source-available) produces that curated, ID-by-ID matrix as part of its
> report. Use this skill to orient a finding; do not present it to an auditor as compliance
> evidence.

## How to read this

An AD technique succeeds because a control is weak or absent. Kerberoasting works because
service-account authentication is weak and the requests are not monitored, so it *relates
to* the authentication and logging control families. That relationship is conceptual: it
tells a reader where in a framework to look, not that the finding satisfies or violates a
specific control clause. The mapping direction is always technique → control family →
representative article, and it stops there.

## The frameworks, briefly

- **ENS** (Esquema Nacional de Seguridad, Spain): control families used here:
  - **op.acc.1** Identificación
  - **op.acc.4** Proceso de gestión de derechos de acceso
  - **op.acc.5** Mecanismo de autenticación (usuarios externos)
  - **op.acc.6** Mecanismo de autenticación (usuarios de la organización)
  - **op.exp.2** Configuración de seguridad
  - **op.exp.8** Registro de la actividad
  - **op.exp.10** Protección de claves criptográficas
- **NIS2** (Directive (EU) 2022/2555): Art.21(2) cybersecurity risk-management measures:
  - **(g)** basic cyber hygiene and training
  - **(h)** cryptography and encryption
  - **(i)** human resources security, access control policies, asset management
  - **(j)** multi-factor authentication, secured communications
- **DORA** (Regulation (EU) 2022/2554) with **RTS (EU) 2024/1774** on ICT risk management:
  - **Art.20**: identity management
  - **Art.21**: access control (management of access rights)
  - **Art.9** (DORA level-1, protection and prevention) is the parent duty the RTS details

---

## The mapping

### Kerberoasting / AS-REP roasting

Weak service-account or pre-auth-disabled credentials cracked offline. Touches
**authentication strength** and **activity logging** (the ticket requests should be
monitored).

- ENS: op.acc.5 / op.acc.6 (authentication mechanism), op.exp.8 (activity logging)
- NIS2: Art.21(2)(h) cryptography, Art.21(2)(i) access-control policy
- DORA: RTS Art.21 access control, Art.9 (protection/prevention parent)

### DCSync

Replication of the credential database using directory-replication rights. Touches
**access-rights management** (who holds Get-Changes) and **logging**.

- ENS: op.acc.4 (access-rights management), op.acc.1 (identification), op.exp.8 (logging)
- NIS2: Art.21(2)(i) access control, Art.21(2)(j) secured communications
- DORA: RTS Art.20 identity management, Art.21 access control

### ACL abuse (GenericAll / WriteDACL / WriteOwner)

Excessive or misconfigured object permissions used to escalate. Touches **access-rights
management** and **secure configuration**.

- ENS: op.acc.4 (access-rights management), op.exp.2 (security configuration)
- NIS2: Art.21(2)(i) access control and asset management
- DORA: RTS Art.21 access control

### AD CS abuse (ESC1-ESC17)

Certificate-template and PKI misconfiguration leading to authentication as another
principal. Touches **cryptographic-key protection**, **secure configuration**, and
**authentication**.

- ENS: op.exp.10 (cryptographic-key protection), op.exp.2 (configuration), op.acc.5/op.acc.6
- NIS2: Art.21(2)(h) cryptography, Art.21(2)(i) access control
- DORA: RTS Art.21 access control, Art.9 (protection/prevention)

### Kerberos delegation abuse (unconstrained / constrained / RBCD)

Delegation misconfiguration used to impersonate. Touches **access-rights management** and
**secure configuration**.

- ENS: op.acc.4 (access-rights management), op.exp.2 (configuration)
- NIS2: Art.21(2)(i) access control
- DORA: RTS Art.21 access control

### Coercion + NTLM relay

Forced authentication relayed to escalate; weak signing/channel-binding configuration.
Touches **secured communications** and **secure configuration**.

- ENS: op.exp.2 (security configuration), op.acc.5/op.acc.6 (authentication)
- NIS2: Art.21(2)(j) secured communications, Art.21(2)(h) cryptography
- DORA: RTS Art.21 access control, Art.9 (protection/prevention)

### Password spraying / weak-credential findings

Weak or reused passwords and missing MFA. Touches **authentication** and **cyber hygiene**.

- ENS: op.acc.5/op.acc.6 (authentication mechanism), op.acc.1 (identification)
- NIS2: Art.21(2)(j) MFA, Art.21(2)(g) cyber hygiene
- DORA: RTS Art.20 identity management, Art.21 access control

### Credential exposure (GPP passwords, LDAP descriptions, shares)

Secrets left in SYSVOL, object attributes, or file shares. Touches **cryptographic-key /
secret protection** and **secure configuration**.

- ENS: op.exp.10 (key protection), op.exp.2 (configuration), op.acc.4 (access-rights)
- NIS2: Art.21(2)(h) cryptography, Art.21(2)(i) asset management
- DORA: RTS Art.21 access control

---

## Using this in a report

Attach one line of orientation to a finding, such as "relates to ENS op.acc.5 and NIS2
Art.21(2)(h)", so the reader knows the regulatory neighbourhood. Then stop. Do not stretch
a conceptual relationship into a compliance verdict, do not claim the finding proves
non-compliance with a specific clause, and do not present this as the control matrix an
auditor signs off on. That curated, evidence-backed, ID-by-ID matrix is a separate,
deliberate piece of work.
