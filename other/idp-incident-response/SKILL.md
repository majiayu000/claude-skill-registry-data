---
name: idp-incident-response
version: "1.0.0"
description: Identity-provider incident response for mid-2026 — Okta, Entra ID, Auth0, Ping, OneLogin tenant compromise, federated-trust abuse, OAuth app consent abuse, Midnight Blizzard and Scattered Spider TTPs against the IdP control plane
triggers:
  - idp incident
  - identity provider incident
  - okta breach
  - okta compromise
  - entra id compromise
  - entra app consent
  - auth0 breach
  - ping identity breach
  - onelogin breach
  - midnight blizzard
  - cozy bear
  - apt29 entra
  - scattered spider
  - octo tempest
  - storm-0875
  - oauth consent abuse
  - federated trust abuse
  - saml token forgery
  - cross-tenant abuse
  - management api token leak
  - service account compromise
  - help-desk social engineering
  - mfa factor swap
  - tenant compromise
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
atlas_refs: []
attack_refs:
  - T1078.004
  - T1556.007
  - T1098.001
  - T1606.002
  - T1199
framework_gaps:
  - NIST-800-53-IA-5-Federated
  - ISO-27001-2022-A.5.16-Federated
  - SOC2-CC6-OAuth-Consent
  - UK-CAF-B2-IdP-Tenant
  - AU-ISM-1685-IdP
  - NIS2-Art-21-Federated-Identity
  - DORA-Art-19-IdP-4h
  - OFAC-Sanctions-Threat-Actor-Negotiation
rfc_refs:
  - RFC-7519
  - RFC-8725
  - RFC-7591
  - RFC-9421
cwe_refs:
  - CWE-287
  - CWE-863
  - CWE-269
  - CWE-284
  - CWE-522
  - CWE-345
d3fend_refs:
  - D3-MFA
  - D3-CBAN
  - D3-NTA
  - D3-IOPR
forward_watch:
  - Entra ID conditional access evolution post-Midnight Blizzard — Microsoft's 2025-2026 commitments on legacy-tenant MFA enforcement and OAuth-app consent gating
  - Okta IPSIE (Interoperability Profile for Secure Identity in the Enterprise) OpenID Foundation working-group output and adoption timeline
  - Auth0 management-API token deprecation roadmap and replacement workload-identity-federation pattern
  - Ping Identity DaVinci flow-execution security model under post-2024 Thoma Bravo ownership
  - OneLogin (One Identity) post-acquisition platform evolution
  - CISA AA24 series — Okta, Entra ID, and IdP-tenant compromise advisories (forward-watched for AA25/AA26 successors)
  - SAML token-forgery (T1606.002) detection-strategy publication in MITRE ATT&CK v20 (October 2026 cycle)
  - DORA Art.19 implementing-act guidance for IdP-class incidents — forward-watched for ESAs publication
  - NIS2 implementing-act revision enumerating federated-identity control-plane indicators
  - Cross-tenant access settings evolution at Entra ID — partner-tenant attestation cadence and revocation latency
  - PSD3 / PSR final text on agent-initiated payments and the IdP-mediated agent-attestation surface
last_threat_review: "2026-09-28"
---

# Identity-Provider Incident Response (mid-2026)

## Threat Context (mid-2026)

Identity-provider tenants are the highest-blast-radius single object in a modern cloud estate. The IdP issues every authentication outcome, federates every OAuth scope, and serves as the source-of-truth for privileged-role assignment across the downstream SaaS / cloud / on-prem fleet. 2023-2026 incident-response data shows five recurring themes, each of which now drives both attacker tradecraft and the framework-lag conversation.

**Okta — October 2023 customer-support breach.** A stolen support-engineer credential gave the attacker read access to customer-uploaded HAR files containing valid session tokens for approximately 134 Okta customer tenants. Downstream exploitation against 1Password, BeyondTrust, Cloudflare, and others followed within days. Root cause was a personal-Google-account-stored Okta service-account credential — a service account that bypassed the human-MFA gate because service accounts at Okta were exempt from MFA enforcement by design. The blast-radius lesson is that service-account credential hygiene at the IdP vendor itself sits upstream of every customer's identity-security programme; the framework-lag lesson is that NIST IA-5, ISO A.5.17, and SOC 2 CC6 had no evidence path that would have surfaced the missing MFA on the upstream service account.

**Microsoft / Entra ID — January 2024 Midnight Blizzard (APT29 / Cozy Bear).** Russian state actor compromised a legacy non-MFA test tenant via residential-proxy + password-spray. Escalation went through OAuth-app consent abuse: a legacy application held a privileged Graph scope (full-mail-read across the tenant), and the attacker harvested the application's refresh tokens after the initial compromise. The attacker exfiltrated corporate mail including senior leadership and the security team's own correspondence about the investigation. Public attribution and Microsoft's own SEC filings (2024 8-K) confirm continued dwell and onward compromise at HPE and others into 2025. The framework-lag lesson is that CC6 audit evidence showed nothing anomalous — the consenting user authenticated correctly, the legacy app's onward Graph calls were authorized by the prior consent grant. Quarterly OAuth consent review is silent on attacker timelines measured in days.

**Snowflake — mid-2024 credential-database compromise.** Approximately 165 customer tenants were compromised through stolen Snowflake-customer credentials harvested from infostealer-malware logs; the dominant pivot was IdP-service-account credentials whose customer tenants had not enforced MFA on the Snowflake user. Affected: AT&T's approximately 110-million-record exposure, Ticketmaster, Santander, Pure Storage, Advance Auto Parts. The framework-lag lesson is that the Snowflake-side controls were fine (MFA was available and the affected customers had not enabled it); the IdP-side gap was that customer identity teams had classified the Snowflake service-account as "system not subject to MFA enforcement" without the IdP tenant enforcing a workload-identity-federation pattern that would have moved the credential off static secret entirely.

**Scattered Spider (UNC3944 / Octo Tempest / Storm-0875) — 2022-2026 help-desk social engineering.** Voice-impersonated calls to IT help-desks to mint replacement MFA factors, then SIM-swap fallback, then ransomware deployment. Public references: MGM Resorts (approximately USD 100M operational impact, September 2023), Caesars Entertainment (approximately USD 15M ransom paid, August 2023), Twilio (multiple breaches 2022-2023), Mailchimp, and dozens of others. The attack pattern continues evolving through 2026 toward deepfake-voice and AI-augmented social-engineering reconnaissance against help-desk operators. The framework-lag lesson is that AU Essential 8 Strategy 4 (MFA), NIST IA-5, and SOC 2 CC6 all show "MFA enforced" status for the targeted users — the factor swap leaves the user-facing MFA policy unchanged while replacing the factor under operator control.

**Auth0 management-API token leakage (2026 class).** Management-API tokens with broad scope checked into IaC or CI configuration produce tenant-wide compromise paths that bypass MFA entirely. The Auth0 management API permits creating users, modifying applications, rotating signing keys, and managing rules — every operation that a tenant administrator could perform interactively. The pattern is structurally identical to AWS root-access-key leakage but the framework controls are weaker: Auth0's management-API token model lacks the AWS-grade IP-allowlist and source-fingerprint enforcement that AWS root-access tokens have.

**Adjacent reality.** Salt Typhoon's 2024-2025 telecommunications-sector compromises (T-Mobile, AT&T Wireless, Verizon, Lumen) leveraged adjacent identity surfaces — the lawful-intercept management plane and the wireline-carrier admin tenant — by similar TTPs (legacy non-MFA admin accounts, dormant service accounts, OAuth-mediated lateral movement). The IdP-tenant control plane is the shared structural attack surface across the Microsoft-class, Okta-class, and Telco-class incidents; the framework controls treat the IdP as oracle in every case.

Agentic AI is the emerging structural problem on top. AI agents operating on behalf of users hold session credentials and refresh tokens; in mid-2026 the dominant question is no longer "did the user authenticate" but "did the user, or an AI agent acting under loosely-scoped delegated authority within the user's authenticated session, initiate this operation." OAuth consent grants made to AI agents (Copilot for Microsoft 365, ChatGPT enterprise connectors, Anthropic computer-use-class agents, LangChain orchestrators) are themselves a high-blast-radius lateral-movement primitive that no framework currently models.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NIST 800-53 Rev.5 | IA-5 (Authenticator Management) | Authenticator issuance, distribution, storage, revocation, replacement at the system layer | Captured in `data/framework-control-gaps.json#NIST-800-53-IA-5-Federated`. IA-5 evidence is satisfied by a quarterly authenticator inventory snapshot; federated-trust modification at the IdP control plane (token-signing certificate rotation, claim-transformation rule changes, OIDC discovery-document tampering) is outside the evidence path. Management-API tokens that bypass the human-MFA gate are not enumerated as IA-5 authenticators by most implementations. |
| NIST 800-53 Rev.5 | IA-2 (Identification and Authentication) | Authenticating organisational and non-organisational users | IA-2 specifies MFA for privileged and non-privileged users; it does not require evidence that the MFA path itself has not been tampered with at the IdP control plane. Help-desk-mediated factor swap (Scattered Spider TTP) produces an IA-2-compliant authentication outcome. |
| ISO/IEC 27001:2022 | A.5.16 (Identity Management) + A.5.17 (Authentication Information) | Static identity lifecycle and credential protection | Captured in `data/framework-control-gaps.json#ISO-27001-2022-A.5.16-Federated`. A.5.16/A.5.17 cover static identity state (was the account provisioned, was MFA enrolled, was the password rotated). Federated-state transitions (OAuth consent grants, cross-tenant access settings, federated-trust modification) are not enumerated as a distinct control class. |
| SOC 2 | CC6 (Logical and Physical Access Controls) | Authentication, authorization, and access controls for human users and service accounts | Captured in `data/framework-control-gaps.json#SOC2-CC6-OAuth-Consent`. CC6 treats the authenticated session as the access boundary. OAuth consent grants federate scope outside the authenticated-session boundary; the consenting user authenticated correctly, the third-party app's onward calls are authorized by the grant, and CC6 audit evidence shows nothing anomalous. The dominant 2024-2026 IdP-pivot pattern is invisible to CC6 audit evidence. |
| UK NCSC CAF | B2.b (Identity and Access Control) | Outcome-based identity and access control for the essential function | Captured in `data/framework-control-gaps.json#UK-CAF-B2-IdP-Tenant`. B2.b is assessed against the IdP tenant's published authentication outcomes; the IdP-tenant control plane (who modified the tenant configuration itself) is outside the outcome's typical evidence surface. A compromised tenant continues to produce compliant outcomes until the attacker abandons stealth. |
| AU ISM | ISM-1685 (credentials for break glass, local administrator and service accounts are long, unique, unpredictable and managed) + ISM-1173 (MFA for privileged users) | Management of privileged and service credentials, and MFA for human privileged authentication | Captured in `data/framework-control-gaps.json#AU-ISM-1685-IdP`. ISM-1685 reaches credentials on the systems an organization runs; control-plane operations in the identity provider tenant are outside the evidence it collects. ISM-1173 covers human privileged users, and control-plane operations performed with management-API tokens never pass a human MFA step. |
| AU Essential 8 | Strategy 4 — Multi-factor authentication (E8 M.4) | MFA on privileged and internet-facing accounts | E8 M.4 defends the interactive authentication flow. IdP-tenant control-plane operations performed via management-API tokens, OAuth client credentials, or workload identity federation never cross the MFA gate. Compliance-theater test: count admin-action audit events over the last 30 days, partition by service-token vs human-MFA-session origin; if service tokens dominate, M.4 compliance is paper. |
| EU NIS2 | Art.21(2)(j) + Art.23 | Cryptography + access control + 24-hour incident notification | Captured in `data/framework-control-gaps.json#NIS2-Art-21-Federated-Identity`. The supporting implementing acts do not enumerate federated-identity control-plane operations. IdP-provider tenants serving essential entities are in scope but the evidence model lags. Art.23 24-hour clock fires on IdP incidents but the tenant-operator-to-essential-entity notification chain is undefined for IdP-class incidents. |
| EU DORA | Art.19 (Major-ICT-related-incident notification) | 4-hour initial / 72-hour intermediate / one-month final notification for major ICT incidents | Captured in `data/framework-control-gaps.json#DORA-Art-19-IdP-4h`. Art.19 does not specify IdP-tenant compromise as a distinct incident class; financial entities relying on a CSP-hosted IdP frequently classify IdP incidents under Art.28 concentration risk and miss the Art.19 4-hour clock. |
| US-NY NYDFS | 23 NYCRR 500.7 (Privileged Access) + 500.17 (Notification of Cybersecurity Event) | Privileged-access controls + 72-hour cyber-event notification | 500.7 covers privileged account access for human accounts; IdP-tenant management-API tokens are treated as conventional service accounts when they are not. 500.17 72-hour clock applies but Class A designation does not specifically enumerate IdP-tenant compromise. |
| US Treasury OFAC + EU + UK sanctions | Cyber-Related Sanctions program (EO 13694 + 13757 + EU Reg.269/2014 + UK OFSI) | Prohibits transactions with designated cyber-actors | Captured in `data/framework-control-gaps.json#OFAC-Sanctions-Threat-Actor-Negotiation`. IdP-incident-response that escalates to ransomware faces ransom-payment-vs-sanctions screening under time pressure; attribution-to-designated-entity is rarely deterministic during an active incident. |
| HIPAA | 164.308(a)(4) (Information Access Management) + 164.312(d) (Person or Entity Authentication) | Access-authorisation policies + entity authentication | Treats the authenticated session as the access boundary; OAuth-consent-mediated scope grant to a third-party app processing PHI is invisible. |

**Cross-jurisdiction posture.** Any IdP-incident-response analysis for a multi-jurisdiction tenant must cite at minimum: EU NIS2 + DORA + GDPR (Art.33 and Art.34) + national overlays, UK GDPR + NCSC CAF, AU Privacy Act NDB + APRA CPS 234 (where applicable) + Essential 8 + ISM, US NYDFS 500 + state breach-notification laws + sector-specific (HIPAA for healthcare, GLBA + NYDFS for financial), Canada PIPEDA + OSFI B-13 (where applicable), Singapore PDPA + MAS Notice 655, Hong Kong PDPO + HKMA guidance, ISO/IEC 27001:2022, SOC 2, and the OFAC + EU + UK sanctions overlay for any ransomware-bridging incident. US-only (NIST + NYDFS + state laws) is incomplete.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| IdP service-account compromise / dormant-then-active reactivation | T1078.004 — Valid Accounts: Cloud Accounts | ATT&CK Enterprise | Snowflake-via-Okta-service-account 2024; ongoing through 2025-2026 against any IdP whose service-account credentials are stored in IaC / CI / dev tooling. CWE-798 (hard-coded credentials) and CWE-522 (insufficiently protected credentials) are the underlying weakness classes. | NIST IA-5 silent on management-API tokens; AU ISM-1559 silent on IdP-tenant control plane |
| Federated-trust modification / SAML / OIDC signing-key tampering | T1556.007 — Modify Authentication Process: Hybrid Identity | ATT&CK Enterprise | APT29-class state actors continue exploiting hybrid-identity federation; on-prem AD-to-Entra cutover windows are particularly vulnerable. CWE-345 (insufficient verification of data authenticity) is the underlying weakness class. | NIST IA-5 silent on federated-trust modification; ISO A.5.16/A.5.17 silent on federated-state transitions |
| OAuth-app consent abuse / additional cloud credentials | T1098.001 — Account Manipulation: Additional Cloud Credentials | ATT&CK Enterprise | Midnight Blizzard's January 2024 Entra ID pattern. Legacy OAuth applications holding privileged Graph / Okta API / Auth0 management scope are the dominant pivot. CWE-863 (incorrect authorization) and CWE-284 (improper access control) underlying. | SOC 2 CC6 audit evidence blind to OAuth-consent-mediated scope; UK CAF B2.b outcome-blind |
| SAML / web-cookie token forgery | T1606.002 — Forge Web Credentials: SAML Tokens | ATT&CK Enterprise | Golden-SAML class attacks (NobleSAML / Solorigate 2020 legacy, ongoing variants against hybrid-identity tenants in 2024-2026). When the IdP signing-state has been tampered with, the attacker can mint authentic tokens for any user. CWE-345 + CWE-287 (improper authentication) underlying. | NIST IA-5 silent on token-signing-state attestation |
| Cross-tenant trust abuse / federated relationship exploitation | T1199 — Trusted Relationship | ATT&CK Enterprise | Entra ID cross-tenant access settings + Okta org-to-org federation + Auth0 enterprise connections all permit persistent token issuance against the home tenant from an attacker-controlled partner tenant. Invisible to most identity-hygiene programmes. CWE-863 underlying. | ISO A.5.16 silent on cross-tenant inventory |
| Help-desk-mediated factor swap | (No native TTP — closest: T1556.007 + T1078.004) | ATT&CK Enterprise | Scattered Spider primary TTP. Voice-impersonated calls produce a factor-reset event that pairs with no password-reset event, leaving the user-facing MFA policy unchanged. AI-augmented reconnaissance accelerates target-selection. | AU E8 M.4 + NIST IA-5 + ISO A.5.17 all show "MFA enforced" for the targeted user |
| Management-API token leakage | T1078.004 + CWE-798 | ATT&CK + CWE | Auth0 management API tokens checked into IaC; Okta API tokens in CI logs; Entra app secrets in dev .env files. Tenant-wide compromise without crossing the human-MFA gate. | ISM-1546 covers human MFA; management-API tokens are out of scope |
| Break-glass account misuse | T1078.004 + (no native TTP for "designed-to-bypass account exploited") | ATT&CK Enterprise | Break-glass accounts whose audit-log alerting was never exercised become attacker backdoors. Conditional-access exclusions designed to permit emergency access remove the MFA gate by design. | UK CAF B2.b outcome-blind; ISO A.5.17 evidence path absent |

**Note on TTP coverage.** ATT&CK Enterprise covers federated-identity attacks through T1078.004 (Cloud Accounts), T1556.007 (Hybrid Identity), T1098.001 (Additional Cloud Credentials), T1606.002 (SAML Tokens), and T1199 (Trusted Relationship). The gap between (a) help-desk-mediated factor swap and (b) any named TTP is the most notable structural omission as of mid-2026; the closest mapping (T1556.007 + T1078.004) does not capture the social-engineering vector that drives Scattered Spider.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live-Patchable | Sector-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| Okta tenant compromise via support-system / service-account | n/a (config-class) | high (operationally exploited 2023-2024) | n/a | Documented at scale | n/a | Confirmed mass exploitation 2023; ongoing variants | Configuration hardening (MFA enforcement on service accounts, IP allowlist, workload identity federation) | n/a | Vendor-side telemetry; partial customer-side via System Log |
| Entra ID OAuth-app consent abuse (Midnight Blizzard class) | n/a (design class) | high (USD-impact > USD 100M cumulative 2024-2025) | n/a | Demonstrated at scale | n/a (state-actor driven) | Confirmed ongoing 2024-2026 against EU + US targets | Mitigation only — consent grant policies, publisher verification, scope gating | n/a | Microsoft Identity Protection + Conditional Access; vendor-fragmented at lower tiers |
| Auth0 / Ping / OneLogin management-API token leak | n/a (config-class) | high (ongoing 2026 reports) | n/a | Documented across multiple operators | n/a | Suspected continuous against any tenant with management-API tokens in IaC | Mitigation — token TTL + scope + IP allowlist + workload identity federation | n/a | Tenant-side telemetry if log streaming configured |
| Help-desk social engineering (Scattered Spider) | n/a (social engineering) | high (MGM USD 100M, Caesars USD 15M as public reference) | n/a | Demonstrated at scale | n/a (AI-augmented reconnaissance) | Confirmed ongoing 2022-2026 | Mitigation only — out-of-band identity verification, video-callback to previously-registered number, knowledge-based + government-ID verification, never phone-only | n/a | Help-desk-system audit; vendor-fragmented |
| SAML token forgery (Golden SAML / NobleSAML class) | n/a (design class) | high (state-actor priority) | n/a | Public research + active campaigns | n/a | Suspected ongoing against hybrid-identity tenants | Mitigation — signing-key rotation + signing-state attestation + audit-log alerting on signing-cert modification | n/a | Tenant audit log if signing-state modification alerts configured |
| ScreenConnect identity-class CVE | 7.5 (CVSS) | high (CISA KEV) | Yes (2024-02) | Yes — public PoC | No | Confirmed exploitation against IdP-adjacent MSP surface | Yes — vendor patch | Patch-class | EDR + tenant audit if integration logged |
| CVE-2024-1709 ScreenConnect authentication bypass | 10.0 | 75 | Yes (2024-02-22) | Yes | No | Confirmed exploitation 2024 | Yes | No | Vendor-side patching + IdP-side conditional-access tightening |
| CVE-2023-3519 Citrix NetScaler RCE | 9.8 | 80 | Yes (2023-07-19) | Yes | No | Confirmed exploitation 2023-2024 (financial-sector and federal targets) | Yes | No | Network telemetry + IdP-tenant access-pattern alerting |
| CVE-2026-30615 Windsurf MCP — adjacent identity surface | 8.0 | 35 | No | Yes | No | Suspected | Mitigation + vendor patch | Yes (IDE update) | MCP-tool-trust telemetry |

**Honest gap statement.** IdP-specific CVEs (Okta Auth0 Workforce CVEs, Entra ID Graph CVEs, Auth0 platform CVEs, Ping platform CVEs, OneLogin platform CVEs) are not exhaustively inventoried in `data/cve-catalog.json`. Authoritative sources: vendor advisories (Okta Security, Microsoft MSRC + Security Update Guide, Auth0 Security Advisories, Ping Identity Security Notices, One Identity Customer Advisory), CISA KEV for cross-sector exposure, CISA AA24 series for federal-targeting advisories, and sector intel feeds. Forward-watched.

---

## Analysis Procedure

This procedure threads the three foundational design principles (defense in depth, least privilege, zero trust) through the seven-phase loop.

**Defense in depth.** Multi-layer authentication for tenant-admin operations: phishing-resistant FIDO2 device-bound passkey at the human layer (skill `identity-assurance`); paired-admin (4-eyes) on federated-trust modification, signing-key rotation, and tenant-wide application permission grants; conditional access requiring known-device + corporate-network + step-up on privileged-role assignment; out-of-band notification on every consent grant for high-risk scope; continuous audit-log alerting on every IdP control-plane operation; downstream-SaaS telemetry for token-use anomalies.

**Least privilege.** Per-service-account scoping (workload identity federation eliminates the static-secret class entirely where vendor support exists); admin-role separation (Application Administrator and Privileged Role Administrator should not be held by the same identity); break-glass accounts scoped to emergency-only with audit-log alerting on every use; OAuth consent grants reviewed per-grant rather than per-app (the same app can hold multiple scopes accreted over time); management-API tokens scoped to specific operations + source-IP allowlist + bounded TTL.

**Zero trust.** Every authentication event verified, not session-trusted; step-up for any privileged-role assignment AND for any federated-trust modification AND for any management-API token issuance; cross-tenant access verified per-partner per-quarter with written attestation; consent grants treated as never-expiring permissions whose business purpose must be re-attested; downstream-SaaS audit logs treated as primary detection telemetry (the IdP itself is the compromised oracle).

### Step 1 — Tenant-ownership + jurisdiction-clock attestation

For every IdP-incident-response engagement:

- Confirm tenant ownership in writing (operator owns the tenant or holds explicit written authorisation). IdP-incident response touches authentication state for every downstream service; ownership ambiguity is a halt condition.
- Identify applicable jurisdiction clocks: DORA Art.19 4-hour (financial entities, IdP is critical ICT third-party), NIS2 Art.23 24-hour (essential entities), GDPR Art.33 72-hour, NYDFS 500.17 72-hour, UK GDPR Art.33 72-hour, AU NDB 30-day, CCPA / CPRA 60-day. Surface clock obligations to the operator and wait for explicit acknowledgement before continuing.

### Step 2 — Audit-log evidence collection

Pull the last 90 days of IdP audit events (or longer if retention permits). For Okta: `/api/v1/logs` filtered for `eventType eq user.session.* OR user.authentication.* OR application.lifecycle.* OR system.org.*`. For Entra ID: Microsoft Graph `/auditLogs/directoryAudits` + `/auditLogs/signIns` with high-risk sign-in + consent-grant + role-assignment + federation-config filters. For Auth0: `/api/v2/logs` filtered for management events. For Ping and OneLogin: vendor-specific audit-trail APIs.

Air-gap or restricted environments: operator-supplied CSV or JSON export from the IdP admin portal.

### Step 3 — Federated-trust integrity check

Pull every federated-trust configuration: Entra ID `/policies/identityProviders` + `/policies/crossTenantAccessPolicy/partners`; Okta `/api/v1/idps` + `/api/v1/org/security/federation`; Auth0 enterprise connections; Ping environment IdPs; OneLogin identity providers. For each, capture token-signing certificate fingerprint, claim-transformation rules, issuer URI, last-modification timestamp + actor.

Match every modification within the 90-day window against the operator's change-control register. Any unmatched modification is a deterministic finding regardless of indicator-level severity.

### Step 4 — OAuth consent-grant inventory

Enumerate active and recently-revoked OAuth consent grants. Capture publisher verification status, scope, tenant-of-origin, grant timestamp, granter identity. Filter for any grant with `/.default`, wildcard, `Mail.Read`, `Mail.ReadWrite`, `Files.Read.All`, `User.Read.All`, `Directory.Read.All` scope; for any unverified publisher; for any cross-tenant grant whose tenant-of-origin is not on the corporate allowlist.

### Step 5 — Privileged-role-assignment audit + break-glass state

Enumerate every assignment to Super Admin / Global Administrator / Tenant Owner / Application Administrator / Privileged Role Administrator within the last 90 days. Cross-reference assignment timestamp against the audit log for assigner identity, source IP, user agent.

Inventory break-glass / emergency-access accounts. Capture last-sign-in timestamp, MFA factor enrolment, conditional-access exclusions, password age, audit-log alerting configuration. Verify that an exercised authentication path fires on-call paging (the IR-drill calendar establishes this).

### Step 6 — Service-account + management-API token inventory

Enumerate every non-human identity in the tenant. For each, capture last-rotation timestamp, scope, source-IP allowlist, last-use timestamp, owner. Any static secret older than 90 days, broad scope, no IP allowlist is a high-priority finding. Match dormant-then-active accounts against the operator's runbook calendar (Step 7).

Inventory management-API tokens with the same lens. Bypass-the-human-MFA-gate by design; any token with broad scope + age > 90 days + no audit-log alerting is structural.

### Step 7 — MFA factor-event review

Filter the audit log for MFA factor enrolment, modification, reset, and bypass events. Each factor-reset event must pair with a documented help-desk identity-verification record (video-callback, knowledge-based + government-ID, never phone-only). Unpaired factor-reset events are the Scattered Spider signature.

### Step 8 — Cross-tenant access-settings review

For Entra ID specifically: enumerate `/policies/crossTenantAccessPolicy` + per-partner inbound/outbound rules. For Okta org-to-org federation; for Auth0 tenant linking. Any cross-tenant grant whose partner tenant cannot be attested in writing is a finding. Any modification within the 90-day window must match the change-control register.

### Step 9 — Downstream-SaaS telemetry sweep (post-detection)

When indicators fire, downstream-SaaS audit logs become primary detection telemetry — the IdP itself is the compromised oracle and its telemetry may have been tampered with. Pull audit logs from every downstream SaaS reachable via the affected credentials for the full exposure window. Focus areas: mail data exfiltration (Microsoft 365 unified audit, Google Workspace audit), file-share download patterns (SharePoint, OneDrive, Google Drive), source-code repository clones (GitHub audit, GitLab audit, Bitbucket audit), data-warehouse queries (Snowflake query history, BigQuery audit), and cloud-account control-plane operations (AWS CloudTrail, GCP Cloud Audit Logs, Azure Activity Log).

### Step 10 — Compliance Theater Check (see dedicated section below)

---

## Output Format

The output is the operator-facing IdP-tenant compromise assessment. Every section is mandatory; empty tables remain present with a "no evidence" row to make absence auditable. The jurisdiction-clock snapshot anchors every subsequent timestamp; downstream tooling parses the deadline column for SLA enforcement. Produce this structure verbatim:

```
## IdP-Tenant Compromise Assessment

**Assessment Date:** YYYY-MM-DD
**Tenant ID (hashed):** [hashed_tenant_identifier]
**IdP Vendor:** [Okta / Entra ID / Auth0 / Ping / OneLogin / hybrid]
**Regulatory exposure:** [EU DORA / EU NIS2 / EU GDPR / UK / US NYDFS / AU NDB / ...]
**Critical or important functions affected:** [list per DORA Art.8 / equivalent]
**Suspected entry vector:** [residential-proxy password spray / help-desk SE / management-API token leak / federation modification / OAuth consent abuse / cross-tenant trust abuse / dormant service-account reactivation / undetermined]
**Detection-confirmed timestamp (UTC):** [ISO 8601]

### Jurisdiction Clock Snapshot
| Regulator | Notification SLA | Clock Start | Deadline (UTC) | Status |

### Federated-Trust Integrity
| Federation | Last Modification | Modification Actor | Change-Control Match | Signing-Cert Fingerprint Drift | Verdict |

### OAuth Consent-Grant Inventory
| App | Publisher (verified?) | Tenant-of-Origin | Scope | Grant Timestamp | Granter | Verdict |

### Privileged-Role-Assignment Audit
| Role | Assignee | Assigner | Timestamp | Source IP | RBAC-Review Match | Verdict |

### Break-Glass Account State
| Account | Last Sign-In | MFA Factors | Conditional-Access Exclusions | Audit-Log Alert | Drill Match | Verdict |

### Service-Account + Management-API Token Inventory
| Identity | Type | Last Rotation | Scope | IP Allowlist | Last Use | Owner | Verdict |

### Cross-Tenant Access Settings
| Partner Tenant | Direction | Permission Set | Ownership Attested | Last Modification | Verdict |

### MFA Factor-Event Audit
| User | Event Type | Timestamp | Reset Actor | Help-Desk Ticket Match | Password-Reset Pair | Verdict |

### Indicator Firing Summary
| Indicator | Affected Actor / Asset | Confidence | RWEP | Distinguishing-Test Outcome | Verdict |

### Blast-Radius Score
[1-5 per blast_radius_model rubric, with rationale]

### Compliance Theater Findings
[Outcome of the seven theater tests in the Compliance Theater Check section below]

### Defensive Countermeasure Plan (D3FEND)
[D3-MFA, D3-CBAN, D3-NTA, D3-IOPR — concrete control placements by surface]

### Priority Remediation Actions
1. Rotate signing keys + revoke sessions + force MFA re-enrolment for admin-tier + rotate management-API tokens.
2. Review and revoke OAuth consent grants; close cross-tenant trusts not in current scope.
3. Harden service accounts (rotation + IP allowlist + scoped credentials); exercise break-glass account audit-log alerting.
4. ...

### Residual Risk Statement
[Per validate.residual_risk_statement template]

### Notification Drafts
[Per close.notification_actions templates — one per applicable jurisdiction clock]

### Evidence Package (signed)
[CSAF-2.0 bundle with structured IdP audit export + IR timeline]
```

---

## Compliance Theater Check

Run all seven tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — "Okta MFA is enforced, so the tenant cannot be compromised."**
Pull the last 90 days of admin-audit events and filter for `AuthenticatorEnrollment`, `FactorReset`, `FactorBypass`, and policy-change events on the MFA policy itself. Help-desk-mediated factor reset (Scattered Spider TTP) leaves the user-facing MFA policy unchanged while replacing the factor under operator control. If any factor-reset event lacks a paired help-desk ticket and identity-verification record, the MFA-enforced claim is paper compliance only. Acceptable: every factor-reset matched to a help-desk ticket with video-callback + knowledge-based + government-ID verification recorded.

**Theater Test 2 — "We use SSO across every SaaS, so identity hygiene is complete."**
Enumerate every OAuth app consent in the tenant. Any consent from a non-corporate tenant, any grant with `/.default` or wildcard scope, any grant whose publisher is unverified, any consent that survived a previous SSO migration is a structural finding regardless of SSO posture. SSO authenticates users; consent grants federate scope and frequently survive identity-hygiene programmes invisibly. Acceptable: consent-grant inventory with per-grant business-purpose attestation, continuous alerting on high-risk scope, automatic gating on unverified publishers.

**Theater Test 3 — "We review OAuth consent grants quarterly."**
Time the gap between consent-grant timestamp and review timestamp across the last 90 days. Midnight Blizzard's January 2024 escalation completed within days; quarterly cadence cannot detect this. Any gap above 24 hours for a high-privilege scope grant is theater. Acceptable: continuous alerting on new high-risk scope grants paired with quarterly comprehensive review.

**Theater Test 4 — "The break-glass account has never been used, so it is by definition secure."**
Pull the break-glass account's last-sign-in timestamp, MFA factors, conditional-access exclusions, password age, audit-log alerting configuration. A never-used account is an account whose audit-log alerting has never been exercised. If conditional access excludes the account from MFA AND no alert fires on break-glass authentication AND password age exceeds rotation policy, the account is a backdoor, not a control. Acceptable: quarterly calendared drill with named operator + expected source IP + audit-log alert firing within SLA.

**Theater Test 5 — "Our SAML / OIDC federation with partner X was set up by the security team and is reviewed annually."**
Pull every federated-trust configuration and compare token-signing certificate fingerprint vs the expected partner fingerprint, claim transformation rules vs documented expectation, and last-modification timestamp + actor against the change-control register. Any unexplained modification within the last 90 days is a structural finding regardless of annual-review attestation. Acceptable: continuous alerting on federated-trust modification with change-control cross-reference.

**Theater Test 6 — "Service accounts are MFA-exempt by design because automation cannot prompt for MFA."**
Pull every service account. Validate that each holds a scoped client-credentials flow OR a workload identity federation (no static secret), that token TTL is bounded, that source-IP allowlist is configured, and that last-rotation date is within policy. Any service account with a static secret older than 90 days, no IP allowlist, and broad scope is theater compliance against the "MFA enforced" attestation. Acceptable: workload identity federation or scoped client credentials with rotation enforcement and IP allowlist on every service account.

**Theater Test 7 — "Admin access is restricted to corporate IPs via conditional access."**
Pull the conditional-access policy targeting admin roles and list every IP range it permits. Cross-reference against the current VPN egress range AND any documented bring-your-own-device exception. Residential-proxy + password-spray defeats corporate-IP allowlist only when the corporate-IP rule includes split-tunnel VPN exits. Any range whose ownership cannot be attested in writing to the corporate network team is an attack-surface gap. Acceptable: documented IP-allowlist with corporate-network attestation and BYOD exceptions enumerated, never wildcard.

---

## Defensive Countermeasure Mapping

Maps IdP-tenant compromise findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND ID | Technique | Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-MFA | Multi-Factor Authentication | Tenant-admin authentication path (phishing-resistant FIDO2 device-bound passkey); user-tier authentication for privileged-role assignment and federated-trust modification; help-desk operator authentication into the help-desk system itself | Per-principal MFA enrolment; phishing-resistant factors mandatory for admin-tier; per-operation step-up for federation modification, signing-key rotation, tenant-wide application permission grants | Every authentication event verified, not session-trusted; step-up for any privileged-role assignment AND for any federated-trust modification AND for any management-API token issuance | Applicable to human principals. AI-agent identities require a scope-token construct + delegated-authority attestation rather than D3-MFA; OAuth consent grants made to AI agents are themselves a lateral-movement primitive requiring per-grant attestation. |
| D3-CBAN | Credential-Based Authentication | Service-account credential plane (workload identity federation eliminates static secrets where supported); management-API token plane; OAuth client-credentials grants | Per-credential scope + source-IP allowlist + bounded TTL; CWE-798 prohibition on hard-coded management-API tokens in IaC / CI / dev tooling; workload identity federation preferred over static secrets | Credential issuance just-in-time where feasible; credential rotation enforced; credential leakage detection at egress and on public-code-search surfaces; management-API tokens treated as root-equivalent credentials | Applicable. AI-agent management-API access requires scope-token construct beyond conventional CBAN — agent tokens scoped to specific operations + amounts + time windows + counterparties. |
| D3-NTA | Network Traffic Analysis | IdP audit-log telemetry as authoritative source of control-plane operations; downstream-SaaS audit-log telemetry as primary detection when IdP itself is suspect; help-desk-system audit telemetry; IaC + CI configuration scanning for embedded management-API tokens | SOC-aggregated visibility; per-tenant alerting on consent-grant + federation-modification + privileged-role-assignment + break-glass-authentication events | Audit-log alerting continuous, not periodic; SLA on every IdP control-plane operation; downstream-SaaS audit logs treated as primary when IdP is compromised | Applicable. AI-agent traffic monitoring is the specific gap: AI-channel egress (LLM API egress with embedded tenant credentials) is a separate exfiltration path. |
| D3-IOPR | Input / Output Pattern Recognition | Authentication-event pattern analysis (impossible-travel, anomalous source-IP, anomalous user-agent); OAuth-app behavioural baseline (typical scope use, typical request pattern); session-token behavioural baseline | Per-user authentication-pattern detection; per-app OAuth-behavioural baseline; per-service-account authentication-pattern baseline | Every authentication outcome verified against historical norm; OAuth-app behavioural drift treated as compromise signal; help-desk-mediated factor swap requires out-of-band identity verification | Critical. AI-agent authentication patterns (sustained API token use, broad scope queries, high-velocity calls) are themselves a detection signal; OAuth grants to AI agents require per-grant behavioural baselining. |

**AI-pipeline-specific posture.** Conventional D3-MFA cannot apply to AI agents holding session credentials on behalf of users — there is no agent-side biometric inherence factor, and possession factors reduce to API-key custody. The AI-pipeline-appropriate construct is: scoped delegated-authority attestation + per-grant business-purpose attestation + continuous behavioural baselining (D3-IOPR) + out-of-band confirmation for any tenant-control-plane operation requested by an AI agent. Skill `identity-assurance` covers AAL/IAL/FAL constructs for human-side authentication; this skill covers the IdP-tenant-control-plane framing of the agent-side gap.

---

## Hand-Off / Related Skills

After producing the IdP-tenant compromise assessment, chain into the following skills.

- **`identity-assurance`** — for AAL3 / FIDO2 / WebAuthn admin-tier authentication implementation detail, IAL2/IAL3 for high-value workforce identity, FAL constructs for federation, and the cryptographic posture (RFC 7519 JWT, RFC 8725 JWT BCP, RFC 7591 OAuth Dynamic Client Registration, RFC 9421 HTTP Message Signatures) that IdP-tenant control-plane operations reference but framework controls do not specify.
- **`cred-stores`** *(playbook chain, not a skill)* — `_meta.feeds_into` on this playbook routes blast-radius >= 4 findings into the `cred-stores` playbook for downstream containment: rotate management-API tokens, downstream service-account credentials, session tokens; audit Vault / Secrets Manager / KMS for IdP-derived credentials. Hand-off is via the playbook chain, not a skill load.
- **`framework-gap-analysis`** — for per-jurisdiction reconciliation of IdP-tenant control-plane coverage gaps across NIST + ISO + SOC 2 + UK CAF + AU ISM + AU E8 + NIS2 + DORA + NYDFS.
- **`compliance-theater`** — to extend the seven theater tests above with general-purpose theater detection across the wider GRC posture (CISO certification independence, audit-attestation evidence currency, change-control register completeness).
- **`coordinated-vuln-disclosure`** — for DORA Art.19 4-hour clock orchestration, NIS2 Art.23 24-hour clock, GDPR Art.33 72-hour clock, NYDFS 500.17 72-hour clock, AU NDB 30-day clock, and the multi-regulator notification when a single IdP-tenant incident triggers multiple clocks across jurisdictions.
- **`incident-response-playbook`** — for the general-purpose IR loop (triage, containment, eradication, recovery, lessons-learned) that frames the IdP-specific work in this skill.
- **`dlp-gap-analysis`** — for downstream data-exfiltration assessment when consent-grant or federation-modification indicators fire and Mail.Read / Files.Read / data-warehouse access scopes were granted.
- **`policy-exception-gen`** — to generate auditor-ready exception language for IdP controls that cannot be remediated within stated SLAs (e.g. coordinated federation re-keying across 50+ relying parties).
- **`sector-financial`** — for financial-services-specific IdP exposure (DORA Art.19 4-hour clock, NYDFS 500 CISO certification, treasury-tooling IdP integration). Skill `sector-financial` scopes the regulatory mapping; this skill covers the IdP-tenant attack surface.
- **`sector-telecom`** — for telecommunications-sector IdP exposure (Salt Typhoon adjacent surface, lawful-intercept admin tenant, wireline-carrier OAM).
- **`sector-federal-government`** — for federal-tenant IdP exposure (FedRAMP IL2/IL4/IL5 tenant separation, CISA AA24 advisories on Okta / Entra ID compromise patterns, M-22-09 zero-trust mandate).
- **`ai-attack-surface`** and **`mcp-agent-trust`** — when AI agents hold session credentials or OAuth consent grants on the tenant; `ai-attack-surface` for prompt-injection and agent-mediated lateral movement, `mcp-agent-trust` for tool-use governance on AI agents with write access to IdP-tenant or downstream-SaaS surfaces.

**Forward watch (per skill-format spec).** Entra ID conditional-access evolution post-Midnight Blizzard; Okta IPSIE working-group output; Auth0 management-API token deprecation roadmap; Ping DaVinci flow-execution security model under post-Thoma-Bravo ownership; OneLogin platform evolution post-One-Identity acquisition; CISA AA25/AA26 successor advisories; ATT&CK v20 SAML token-forgery detection-strategy publication; DORA Art.19 implementing-act guidance for IdP-class incidents; NIS2 implementing-act revision enumerating federated-identity control-plane indicators; cross-tenant access settings evolution at Entra ID with partner-tenant attestation cadence; PSD3/PSR final text on agent-initiated payments and IdP-mediated agent attestation.
