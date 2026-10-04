---
name: iam
description: "Routing agent for Identity & Access Management technologies. Covers SSO, MFA, federation, provisioning, governance, and cross-platform IAM architecture. WHEN: \"IAM\", \"identity management\", \"access management\", \"SSO\", \"MFA\", \"federation\", \"SCIM provisioning\", \"identity governance\", \"access review\", \"zero trust identity\". Do NOT use for platform-specific questions -- use the `entra-id`, `okta`, `ad-ds`, `auth0`, `keycloak`, `ad-fs`, `ad-cs`, `ping-identity`, `aws-iam`, `gcp-iam`, or `sailpoint` skill."
license: MIT
---

# Identity & Access Management

This skill covers all Identity & Access Management (IAM) technologies. It provides cross-platform expertise in authentication, authorization, federation, provisioning, and identity governance. Read the relevant sibling skill for deep implementation details.

## When to Use This Skill vs. a Sibling Skill

**Use this skill when the question is cross-platform or strategic:**
- "Which IdP should we use?"
- "How do we federate between Okta and AD?"
- "Design our SSO architecture"
- "Compare MFA approaches across platforms"
- "What does a zero trust identity strategy look like?"
- "Plan our identity governance program"
- "Migrate from AD FS to a cloud IdP"
- "SCIM provisioning architecture for multi-IdP"
- "Access review and certification strategy"

**Read a sibling skill when the question is technology-specific:**
- "Configure Conditional Access in Entra ID" --> `entra-id`
- "AD DS replication is failing" --> `ad-ds`
- "Okta Workflows automation" --> `okta`
- "ESC8 vulnerability in our PKI" --> `ad-cs`
- "Auth0 Actions for custom login flow" --> `auth0`
- "Keycloak realm configuration" --> `keycloak`
- "AWS IAM policy for cross-account access" --> `aws-iam`

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture / Strategy** -- Load `references/concepts.md` for foundational IAM concepts
   - **Technology selection** -- Compare IdP/IGA options using the comparison table below
   - **Federation design** -- Identify protocols (OIDC, SAML, WS-Fed) and trust relationships
   - **Provisioning / Lifecycle** -- Evaluate SCIM, JIT provisioning, HR-driven flows
   - **Governance** -- Access reviews, certifications, SOD, entitlement management
   - **Technology-specific** -- Read the appropriate sibling skill

2. **Gather context** -- What is the environment? Cloud/on-prem/hybrid, user population size, regulated industry, existing IdP(s), directory services, application portfolio

3. **Analyze** -- Apply IAM-specific reasoning. Consider authentication flows, token lifetimes, trust boundaries, blast radius of compromise, and operational maturity.

4. **Recommend** -- Provide prioritized recommendations with trade-offs. Identity is the new perimeter -- get this wrong and nothing else matters.

5. **Qualify** -- State assumptions, residual risks, and conditions under which the recommendation changes

## Cross-Platform IAM Concepts

### Authentication vs. Authorization

| Concept | Question Answered | Protocols | Examples |
|---|---|---|---|
| **Authentication (AuthN)** | Who are you? | OIDC, SAML, Kerberos, FIDO2 | Login page, MFA challenge, certificate auth |
| **Authorization (AuthZ)** | What can you do? | OAuth 2.0, XACML, OPA/Rego | API scopes, role checks, policy decisions |

These are distinct concerns. Conflating them is the root cause of many IAM architecture failures.

### Identity Federation

Federation enables trust between identity domains without replicating credentials.

**Protocol selection:**

| Protocol | Use When | Strengths | Limitations |
|---|---|---|---|
| **OIDC** | New applications, SPAs, APIs, mobile | Modern, JSON-based, good library support, token-based | Requires HTTPS, stateless tokens need revocation strategy |
| **SAML 2.0** | Enterprise SSO, legacy apps, B2B federation | Mature, widely supported, signed assertions | XML complexity, large payloads, browser-based only |
| **WS-Federation** | Microsoft-centric environments, AD FS | Native to Windows Identity Foundation | Legacy, being replaced by OIDC |
| **LDAP(S)** | Directory lookups, legacy application auth | Universal directory protocol | Not a federation protocol, credential exposure risk |
| **SCIM 2.0** | User/group provisioning (not authentication) | Standardized REST API for identity lifecycle | Inconsistent vendor implementations |

**Federation trust types:**
- **Hub-and-spoke** -- Central IdP authenticates for all SPs. Simplest model. Single point of failure.
- **Mesh** -- Direct trusts between IdPs. Complex at scale. Use for B2B federation between large enterprises.
- **Broker** -- Intermediary translates between protocols/IdPs. Use when connecting SAML-only apps to OIDC IdP or vice versa.

### Multi-Factor Authentication (MFA)

MFA factors by category:

| Factor | Category | Phishing Resistant? | Examples |
|---|---|---|---|
| Password | Knowledge | No | Static password, PIN |
| TOTP | Possession | No (phishable) | Authenticator app codes |
| Push notification | Possession | Partially (MFA fatigue risk) | Okta Verify, Microsoft Authenticator push |
| Number matching push | Possession | Better (resists fatigue) | Okta Verify number challenge, MS Authenticator number match |
| SMS OTP | Possession | No (SIM swap, SS7) | Text message codes |
| FIDO2 / Passkeys | Possession + Inherence | Yes (origin-bound) | YubiKey, platform passkeys |
| Certificate | Possession | Yes (mutual TLS) | Smart card, virtual smart card |
| Biometric | Inherence | Depends on implementation | Windows Hello, Face ID (local biometric) |

**MFA strategy priority:** FIDO2/passkeys > certificate-based > number matching push > TOTP > SMS (last resort)

### Provisioning and Lifecycle

The Joiner-Mover-Leaver (JML) lifecycle:

| Phase | Actions | Automation |
|---|---|---|
| **Joiner** | Create identity, assign baseline access, enroll MFA, provision to downstream apps | HR-driven provisioning via SCIM, attribute mapping |
| **Mover** | Adjust group memberships, recertify access, update attributes | Role-based auto-adjustment, access review triggers |
| **Leaver** | Disable account, revoke tokens, deprovision from apps, archive data | Automated deprovisioning, token revocation, license reclaim |

**Provisioning patterns:**
- **SCIM push** -- IdP pushes changes to SPs via REST API. Standard approach.
- **JIT provisioning** -- Account created on first SAML/OIDC login. Simple but no pre-provisioning for offline access.
- **HR-driven** -- HR system (Workday, BambooHR, SAP SuccessFactors) is the source of truth. Changes flow: HR --> IdP --> Apps.
- **Directory sync** -- AD Connect, LDAP sync. For hybrid environments bridging on-prem to cloud.

### Identity Governance and Administration (IGA)

| Capability | Description | Key Vendors |
|---|---|---|
| **Access certifications** | Periodic review of who has access to what | SailPoint, Saviynt, Okta, Entra ID Governance |
| **Entitlement management** | Self-service access request with approval workflows | Entra ID, SailPoint, Okta |
| **Separation of Duties (SOD)** | Prevent toxic combinations of access | SailPoint, Saviynt, Oracle |
| **Role mining** | Discover roles from existing access patterns | SailPoint, Saviynt |
| **Lifecycle workflows** | Automate JML processes | Entra ID Lifecycle Workflows, SailPoint, Okta Lifecycle Management |
| **Privileged Access Management (PAM)** | Control and audit privileged access | CyberArk, Entra PIM, BeyondTrust, Delinea |

### Access Control Models

| Model | Description | Best For | Limitations |
|---|---|---|---|
| **RBAC** | Permissions assigned to roles, users assigned to roles | Structured organizations, compliance | Role explosion, static, doesn't capture context |
| **ABAC** | Policies evaluate attributes (user, resource, environment, action) | Dynamic access decisions, fine-grained control | Complex policy authoring, harder to audit |
| **ReBAC** | Permissions based on relationships between entities | Document sharing, hierarchical orgs | Newer model, fewer implementations |
| **PBAC** | Central policy engine makes decisions | Consistent cross-app authorization | Latency of policy evaluation, single point of failure |

## Technology Comparison

| Technology | Type | Best For | Deployment | Key Differentiator |
|---|---|---|---|---|
| **Entra ID** | Cloud IdP | Microsoft/Azure shops, hybrid with AD | Cloud (SaaS) | Deepest Microsoft integration, Conditional Access, PIM |
| **Okta** | Cloud IdP | Multi-cloud, IdP-agnostic shops | Cloud (SaaS) | 7,000+ OIN integrations, Workflows, vendor-neutral |
| **Auth0** | CIAM | Customer-facing identity, developer-focused | Cloud (SaaS) | Actions extensibility, Organizations for B2B |
| **Keycloak** | IdP | Self-hosted, open-source, customizable | Self-hosted | Full control, no licensing cost, extensible |
| **Ping Identity** | Enterprise IdP | Large enterprise, complex federation | Hybrid/Cloud | DaVinci orchestration, decentralized identity |
| **AD DS** | Directory | Windows-centric on-prem, GPO, Kerberos | On-premises | Group Policy, Windows device management, Kerberos |
| **AD FS** | Federation | On-prem SAML/OIDC federation | On-premises | Claims-based auth, being replaced by Entra ID |
| **AD CS** | PKI | Enterprise PKI, certificate-based auth | On-premises | Native Windows PKI, auto-enrollment |
| **AWS IAM** | Cloud IAM | AWS resource access control | Cloud (AWS) | Fine-grained AWS policy language, Identity Center |
| **GCP IAM** | Cloud IAM | Google Cloud resource access control | Cloud (GCP) | Workload Identity Federation, IAM Recommender |
| **SailPoint** | IGA | Enterprise governance, certifications, SOD | Cloud (SaaS) | Deep IGA, IdentityAI, role mining |

## Technology Routing

Read these sibling skills for deep implementation guidance:

| Request Pattern | Route To |
|---|---|
| **On-Premises Microsoft** | |
| Active Directory, domain controllers, GPO, Kerberos, LDAP, replication | `ad-ds` (see its Version-Specific Guidance) |
| AD FS, claims, federation, SAML with AD FS, WAP | `ad-fs` |
| AD CS, PKI, certificates, ESC vulnerabilities, Certify, Certipy | `ad-cs` |
| **Cloud Identity Providers** | |
| Entra ID, Azure AD, Conditional Access, PIM, Entra Connect | `entra-id` |
| Okta, Universal Directory, OIN, Workflows, ThreatInsight | `okta` |
| Auth0, Universal Login, Actions, Organizations, CIAM | `auth0` |
| Keycloak, realms, identity brokering, Quarkus | `keycloak` |
| Ping Identity, PingFederate, PingOne, DaVinci | `ping-identity` |
| **Cloud Platform IAM** | |
| AWS IAM, IAM Identity Center, SCPs, permission sets | `aws-iam` |
| Google Cloud IAM, Cloud Identity, Workload Identity Federation | `gcp-iam` |
| **Identity Governance** | |
| SailPoint, IdentityNow, access certifications, SOD, role mining | `sailpoint` |

## IAM Architecture Patterns

### Pattern 1: Cloud-First with Entra ID

```
Entra ID (primary IdP)
  |-- Conditional Access (policy engine)
  |-- PIM (privileged access)
  |-- Entra Connect (hybrid sync from AD DS)
  |-- SCIM provisioning to SaaS apps
  |-- B2B/B2C for external identities
```

Best for: Microsoft-centric organizations migrating to cloud

### Pattern 2: Multi-Cloud with Okta

```
Okta (central IdP)
  |-- Adaptive MFA (risk-based)
  |-- Lifecycle Management (HR-driven provisioning)
  |-- OIN integrations (SAML/OIDC to SaaS apps)
  |-- API Access Management (OAuth 2.0 for APIs)
  |-- Identity Governance (certifications)
```

Best for: Multi-cloud organizations wanting vendor-neutral identity

### Pattern 3: Hybrid On-Prem + Cloud

```
AD DS (on-prem directory, source of truth for Windows)
  |-- AD FS or Entra Connect (federation/sync to cloud)
  |-- Entra ID or Okta (cloud IdP for SaaS apps)
  |-- AD CS (PKI for certificate-based auth)
  |-- PAM solution (CyberArk, Delinea) for privileged access
```

Best for: Organizations with significant on-prem Windows infrastructure

### Pattern 4: Developer-First CIAM

```
Auth0 (customer-facing identity)
  |-- Universal Login (customizable, hosted login)
  |-- Social connections (Google, Apple, Facebook)
  |-- Organizations (B2B multi-tenancy)
  |-- Actions (extensibility hooks)
  |-- Attack Protection (brute force, bot, breached password)
```

Best for: SaaS applications, developer-led identity for customer-facing apps

## Anti-Patterns to Watch For

1. **"One IdP for everything"** -- Workforce IAM and customer IAM (CIAM) have different requirements. Do not force employees through a CIAM solution or customers through an enterprise IdP.

2. **"MFA is enough"** -- MFA is critical but insufficient. Token theft, session hijacking, and MFA fatigue attacks bypass it. Layer with device trust, conditional access, and continuous evaluation.

3. **"Sync all attributes everywhere"** -- Minimize attribute propagation. Each downstream system should receive only the attributes it needs. Over-syncing creates data privacy issues and expands blast radius.

4. **"Flat RBAC with hundreds of roles"** -- Role explosion indicates the access model is wrong. Consider ABAC or group nesting. More than 50 roles in a small organization is a red flag.

5. **"No service account governance"** -- Service accounts, API keys, and managed identities are identity too. They need lifecycle management, rotation, and least privilege just like human identities.

6. **"Delaying deprovisioning"** -- Orphaned accounts are a top attack vector. Automate deprovisioning from HR events. Target: accounts disabled within 1 hour of termination.

7. **"Skipping access reviews"** -- Access accrues over time. Without periodic certification, users accumulate permissions far beyond what they need. Quarterly reviews minimum for privileged access.

## Reference Files

Load these for deep foundational knowledge:

- `references/concepts.md` -- IAM foundational concepts: OIDC flows, SAML assertions, SCIM operations, Kerberos protocol, RBAC/ABAC models, JIT/JEA patterns, token types, session management. Read for "how does X work" or cross-platform architecture questions.
