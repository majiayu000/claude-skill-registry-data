---
name: cloud-iam-incident
version: "1.0.0"
description: Cloud-IAM incident response for AWS / GCP / Azure — account takeover, IAM role assumption abuse, access-key compromise, cross-account assume-role chains, federated-trust attacks (IAM Identity Center / Workload Identity Federation / Azure managed identity), IMDS metadata exfiltration, and Snowflake-AA24-class IdP-to-cloud credential reuse
triggers:
  - cloud iam compromise
  - aws account takeover
  - gcp service account compromise
  - azure managed identity replay
  - cross account assume role
  - federated trust abuse
  - oidc trust policy
  - workload identity federation
  - iam access key leak
  - cloudtrail anomaly
  - imds metadata abuse
  - imdsv1 ssrf
  - scattered spider aws
  - snowflake aa24
  - aws sso compromise
  - iam identity center
  - crypto mining cloud
  - access key public repo
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
atlas_refs:
  - AML.T0051
attack_refs:
  - T1078
  - T1078.004
  - T1098.001
  - T1552.005
  - T1580
  - T1538
framework_gaps:
  - FedRAMP-IL5-IAM-Federated
  - CISA-Snowflake-AA24-IdP-Cloud
  - NIST-800-53-AC-2-Cross-Account
  - ISO-27017-Cloud-IAM
  - SOC2-CC6-Access-Key-Leak-Public-Repo
  - AWS-Security-Hub-Coverage-Gap
  - UK-CAF-B2-Cloud-IAM
  - AU-ISM-1685-Cloud-Service-Account
rfc_refs:
  - RFC-8693
  - RFC-7519
  - RFC-8725
  - RFC-9068
cwe_refs:
  - CWE-287
  - CWE-522
  - CWE-798
  - CWE-863
  - CWE-732
  - CWE-269
d3fend_refs:
  - D3-MFA
  - D3-CBAN
  - D3-NTA
  - D3-IOPR
  - D3-CAA
forward_watch:
  - AWS IAM Identity Center session-policy refresh and step-up-on-admin enforcement (anticipated 2026-H2 release)
  - GCP Workload Identity Federation principal-set attribute mapping tightening (post-2026 Q3 Federation hardening guide)
  - Azure managed-identity continuous-access-evaluation rollout for cross-tenant trust scenarios
  - CISA Snowflake AA24 follow-up advisories on IdP-to-cloud chained-compromise patterns (continuous 2025-2026)
  - FedRAMP Rev 5 cloud-IAM control overlay; cross-IL trust patterns in IL6 sovereign cloud
  - NIST 800-53 Rev 6 (anticipated 2027) Account Management chain-of-assumptions sub-control
  - ISO/IEC 27017:2027 (anticipated) cloud-IAM hardening including managed-identity token-binding and IMDS hardening
  - UK CAF v4 cloud-IAM specificity in B2 contributing outcomes
  - AU ISM update enumerating cloud non-human-principal credential hygiene with explicit bearer-token TTL ceilings
  - DORA TLPT (JC 2024/40 RTS) first-cycle aggregate findings on cloud-account-compromise scenarios
  - AWS, GCP, and Azure shared-fate / shared-responsibility recalibration for federated-trust hygiene
last_threat_review: "2026-09-28"
---

# Cloud IAM Incident Response (mid-2026)

## Threat Context (mid-2026)

Cloud-IAM compromise has been the dominant cloud-breach root cause across all three major hyperscalers (AWS, GCP, Azure) from 2024 through mid-2026. The threat surface has shifted materially since 2023 and the conventional defensive posture — Service Control Policies, root-account MFA, posture tools like AWS Security Hub / GCP Security Command Center / Azure Defender for Cloud, and quarterly access reviews — captures progressively less of the actual attack surface as adversary capability evolves.

**Reference cases driving this skill.**

1. **CISA Snowflake AA24-174A advisory (June 2024).** Stolen Okta / SSO credentials from a series of customer-environment infostealer infections were reused against the customers' Snowflake tenants. The same federated IdPs frequently held trust into the customer's AWS / Azure / GCP estate, enabling lateral movement from a Snowflake-scoped credential into the customer's cloud-IAM principal set. Reported impact: AT&T, Ticketmaster, Santander, Advance Auto Parts, Neiman Marcus, LendingTree, Pure Storage, plus dozens of unattributed downstream customers. The dominant cross-system vector — credential reuse across federated IdP downstream consumers — is not enumerated in any framework's evidence surface.

2. **2024-2025 AWS-key-in-public-repo crypto-mining campaigns.** Scraper bots monitoring the GitHub firehose monetise within ~5 minutes of public exposure. Typical spend pattern: 50-500 USD/hour of GPU instances in an unused region (where the victim has no resources to alert on regional anomalies). Common compromise window: 30 minutes to 4 hours before the victim notices. Even after revocation, the attacker often establishes long-lived persistence by creating their own IAM user with AdministratorAccess inside the compromised account before the original key is revoked.

3. **2026 Azure managed-identity token replay (design-class issue, not a single CVE).** Attackers with limited code-execution on an Azure VM (often via SSRF in a hosted web application) steal the managed-identity token from the IMDS endpoint at 169.254.169.254. The token is valid for its TTL (default 24h on most managed-identity scopes) and can be replayed from the attacker's infrastructure. Azure Continuous Access Evaluation is the long-term mitigation; rollout is incomplete in most large estates.

4. **Scattered Spider AWS-MFA-bypass via help-desk social engineering.** Continuous 2023-2026 pattern. Voice-cloned or socially-engineered help-desk agent resets MFA on a privileged user, attacker logs in, escalates via either (a) creating their own IAM user with AdministratorAccess for persistence, (b) directly assuming a privileged role into a production account, or (c) modifying the federated IdP trust policy to grant ongoing access. Help-desk OOB-callback policy + voice-channel deepfake-resistant verification is the operational mitigation; coverage is fragmentary.

5. **IMDS v1 to v2 transition incidents.** AWS' guidance to migrate from IMDSv1 (unauthenticated) to IMDSv2 (session-token-required, hop-limit-bounded) has been published since 2019. Migration remains incomplete in most large estates as of mid-2026. SSRF-class vulnerabilities in instance-hosted web applications can read metadata-service tokens (T1552.005); IMDSv1 has no defence against this. GCP and Azure have analogous patterns but the threat surface is dominated by AWS due to install base.

6. **Federated-trust attacks against IAM Identity Center / AWS SSO, GCP Workload Identity Federation, and Azure AD Conditional Access.** Three sub-patterns:
   - **GitHub Actions OIDC wildcard subject claims** — an IAM role with a trust policy referencing `repo:owner/repo:*` (no branch/tag constraint) allows any fork-PR's workflow to assume the role. Documented as a class throughout 2024-2026; vendor-side mitigations (deploy-environment OIDC trust policies, AWS' suggested branch constraints) are unevenly adopted.
   - **AWS SSO / IAM Identity Center misconfigured permission sets** granting Org-Admin via SAML assertion replay where the assertion is not cryptographically bound to the requesting session.
   - **Azure AD application impersonation via expired-cert reuse** — applications with multiple certificates configured, where one cert has expired but is still trusted because rotation procedures didn't remove it.

**Mid-2026 reality.** Any cloud-IAM compromise investigation must assume the following baseline by default:

- Cross-account assume-role chains are the dominant lateral-movement primitive — not the historic case of compromised-host pivoting via SSH/RDP. AC-2-style account-lifecycle controls treat each assume-role event as a valid action; the compromise is the chain.
- Federated trust is the dominant first-stage compromise vector when the customer has an IdP (Okta / Azure AD / Google Workspace / Auth0) integrated with the cloud account.
- Managed identities and service-account access keys hold more operational privilege than human users in most IaC-managed estates. Human MFA is a 1-of-N control for the actual privilege surface.
- Posture tools (Security Hub / SCC / Defender for Cloud) are coverage-based, not breach-detection. Their "all green" attestation has ~0 correlation with absence of behavioural anomalies.
- IMDSv1 remains an active attack surface on instances that haven't migrated; IMDSv1 should be assumed reachable from any SSRF primitive.

The playbook `cloud-iam-incident` operationalises this skill into a seven-phase investigation against a specific cloud account (or account-set), walking 90 days of audit log + current IAM principal inventory + federated trust configuration + SCP/Org-Policy/Management-Group state + recently-modified resource policies + billing-anomaly signal.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NIST 800-53 Rev 5 | AC-2 — Account Management | Establish, activate, modify, review, disable, and remove accounts | Lifecycle controls treat principals individually. Cross-account assume-role chains are valid AC-2-compliant actions individually; the compromise is the chain across boundaries, which AC-2 cannot see. Captured in `data/framework-control-gaps.json#NIST-800-53-AC-2-Cross-Account`. |
| NIST 800-53 Rev 5 | AC-6 — Least Privilege | Principle-of-least-privilege application across roles and permissions | Static-analysis-shaped (Access Analyzer / Policy Analyzer flag overly-broad policies). Does not see principal-action behaviour that precedes a privileged action. |
| ISO/IEC 27001:2022 | A.5.15 — Access Control | Rules for physical and logical access established and reviewed | Governs the access-rules baseline. Federated trust configurations (SAML / OIDC / Workload Identity Federation) are technically access rules but their security depends on claim-validation and trust-policy condition specificity that A.5.15 does not enumerate. |
| ISO/IEC 27001:2022 | A.5.18 — Access Rights | Provision, review, and removal of access rights | Treats credentials as fungible. Federated IdP credentials and cloud-IAM credentials are reviewed independently. Cross-system credential-reuse compromise (CISA Snowflake AA24) is invisible. Captured in `data/framework-control-gaps.json#CISA-Snowflake-AA24-IdP-Cloud`. |
| ISO/IEC 27001:2022 | A.5.23 — Cloud Services Information Security | Acquisition, use, management, and exit for cloud services | Generic cloud-services control. Provider-specific IAM constructs (cross-account role assumption, managed-identity tokens, IMDS access patterns) are not enumerated. Audit evidence is a cloud-provider risk assessment, not behavioural telemetry. |
| ISO/IEC 27017 | Cloud-specific extension to A-controls | Cloud-services extension to ISO/IEC 27001 controls | Cloud-IAM extension lags on managed-identity token replay and IMDS hardening. Captured in `data/framework-control-gaps.json#ISO-27017-Cloud-IAM`. |
| SOC 2 | CC6.1 — Logical Access Controls | Restrict logical access to data and system resources | Authentication-shaped. Treats the authenticated session as the access boundary. Leaked access keys produce fully-authenticated sessions; CC6.1 evidence is satisfied regardless of how the key reached the attacker. Captured in `data/framework-control-gaps.json#SOC2-CC6-Access-Key-Leak-Public-Repo`. |
| SOC 2 | CC6.3 — Lifecycle Management | Manage access throughout the entire access lifecycle | Lifecycle-focused. Audit cadence is quarterly; the dominant cloud-IAM compromise window is hours-to-days. |
| SOC 2 | CC7.2 — System Monitoring | Monitor system components for security events | Satisfied by posture-tool deployment. Does not verify that the monitoring system can see behavioural signals (cross-account chains, federated-trust anomalies). Captured in `data/framework-control-gaps.json#AWS-Security-Hub-Coverage-Gap`. |
| FedRAMP IL5 | Baseline (AC-2, AC-3, AC-6, IA-2, IA-5) | US-Government Impact-Level 5 cloud workloads | Baseline assumes single-cloud-tenant deployment. IL6 sovereign-cloud federated-trust patterns and cross-IL trust policies are not contemplated. Captured in `data/framework-control-gaps.json#FedRAMP-IL5-IAM-Federated`. |
| NIS2 | Art. 21(2)(d) — Supply Chain Security | Risk-management measures including supply-chain security and direct-supplier relationships | Names cloud-service providers as supply-chain dependencies but does not enumerate cloud-IAM trust-policy hygiene as a sub-control. |
| DORA | Art. 6-9 — ICT Risk-Management Framework | Identify, protect, detect, respond, and recover for ICT risk | Principle-based. Cloud-IAM specifics are not enumerated in the binding articles; ESAs may publish Level-2/3 guidance over time. |
| UK CAF | B2 — Identity and Access Control | Outcome that access to networks and information systems is controlled in line with the essential function's risk | Outcome-based on credential-lifecycle hygiene. Cloud-IAM specifics not enumerated against B2 evidence. Captured in `data/framework-control-gaps.json#UK-CAF-B2-Cloud-IAM`. |
| AU Essential 8 | Strategy 4 — Multi-Factor Authentication (E8 M.4) | MFA on privileged and internet-facing accounts | Covers human-principal MFA. Cloud service-account access keys, OIDC federation tokens, and SAML assertions are bearer credentials that bypass MFA. |
| AU ISM | ISM-1685 (credentials for break glass, local administrator and service accounts are long, unique, unpredictable and managed) and ISM-1173 (MFA for privileged users) | AU-government information-security baseline | ISM-1173 covers human privileged users only. ISM-1685 covers service-account credentials, but a long, unique cloud access key still works from anywhere once it leaks, and platform-issued managed-identity tokens have no credential for the organization to manage. Captured in `data/framework-control-gaps.json#AU-ISM-1685-Cloud-Service-Account`. |
| PCI DSS 4.0 | Req. 7-8 — Access Control + Identification | Access-control objectives generically | Cloud-IAM-specific requirements not enumerated. |
| HIPAA | 164.312(a)(1) — Access Control | Technical safeguard for ePHI access | Generic access-control framing. Cloud-IAM specifics out of scope. |
| AWS Security Hub | Foundational Security Best Practices | AWS-native posture tool | Coverage-based. Findings reflect configuration drift, not behavioural compromise. Captured in `data/framework-control-gaps.json#AWS-Security-Hub-Coverage-Gap`. |
| GCP CIS | CIS GCP Foundations Benchmark | Posture baseline | Same shape as AWS Security Hub — coverage-based. |
| Azure Security Benchmark | Azure-native posture baseline | Posture baseline | Same shape — coverage-based. |

**Cross-jurisdiction posture.** Any multi-jurisdiction cloud-IAM incident must cite at minimum: EU GDPR Art. 33-34 (72h), NIS2 Art. 23 (24h early warning, 72h notification), DORA Art. 19 (4h initial, 72h follow-up) for financial entities; UK GDPR Art. 33 (72h) and UK CAF B2; US NYDFS 23 NYCRR 500.17 (72h cyber event); US-CA CCPA / CPRA (60 days) for California resident exposure; AU Privacy Act NDB scheme (30 days); JP APPI Art. 26 (24h immediate to PPC); SG PDPA s26D (72h); plus the CSP-specific incident-response engagement (AWS Health Dashboard support case, GCP support case at appropriate severity, Azure Service Health incident). US-only treatment (NYDFS, FFIEC, NIST CSF) is incomplete.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Stolen federated IdP credentials reused against cloud IAM | T1078 — Valid Accounts | ATT&CK Enterprise | Snowflake AA24 chain (Okta-to-Snowflake-to-AWS); infostealer-sourced session tokens | Captured in `data/framework-control-gaps.json#CISA-Snowflake-AA24-IdP-Cloud`. ISO A.5.18 treats credentials as fungible; cross-system reuse is invisible. CWE-287 + CWE-522. |
| Cloud account credential abuse | T1078.004 — Valid Accounts: Cloud Accounts | ATT&CK Enterprise | Leaked access keys via public repository; managed-identity token replay; SAML assertion replay | Captured in `data/framework-control-gaps.json#SOC2-CC6-Access-Key-Leak-Public-Repo`. CC6.1 satisfied by authenticated session regardless of credential source. |
| IAM-principal creation outside IaC for persistence | T1098.001 — Account Manipulation: Additional Cloud Credentials | ATT&CK Enterprise | CreateUser + CreateAccessKey in burst pattern; AssumeRole-and-grant-self-admin chain | NIST AC-2 records the event as compliant lifecycle action; AC-2 has no concept of "outside IaC" vs "inside IaC" baselining. Captured in `data/framework-control-gaps.json#NIST-800-53-AC-2-Cross-Account`. |
| IMDS metadata-service exfiltration | T1552.005 — Unsecured Credentials: Cloud Instance Metadata API | ATT&CK Enterprise | IMDSv1 SSRF; Azure managed-identity token theft via IMDS; hop-limit bypass | Captured in `data/framework-control-gaps.json#ISO-27017-Cloud-IAM`. ISO/IEC 27017 cloud extension does not enumerate IMDS hardening. CWE-863. |
| Cloud infrastructure discovery for follow-on action | T1580 — Cloud Infrastructure Discovery | ATT&CK Enterprise | Post-compromise listing of S3 buckets, KMS keys, EC2 instances, RDS instances; crypto-mining region selection | Visible in CloudTrail but typically high-noise. Behavioural anomaly (unused-region resource creation) is the high-signal variant. |
| Cloud-service-dashboard discovery | T1538 — Cloud Service Dashboard | ATT&CK Enterprise | Post-compromise console-portal browsing to enumerate services + billing; cost-explorer queries to size the target | Console-login + dashboard-load events are recorded but rarely alerted. Combined with `root_login_from_new_asn` indicator. |
| Cross-account assume-role chains | (No native TTP — closest T1078.004 chain) | ATT&CK Enterprise | Source principal compromise -> AssumeRole into target account -> further AssumeRole into prod -> KMS key policy self-grant | NIST AC-2 treats each link as compliant. Captured in `data/framework-control-gaps.json#NIST-800-53-AC-2-Cross-Account`. The chain is the compromise. |
| Wildcard federated trust policy abuse | (No native TTP — closest T1078.004) | ATT&CK Enterprise | GitHub Actions OIDC role with `repo:*` subject claim; fork-PR-to-takeover | No framework enumerates trust-policy condition specificity as a sub-control. UK CAF B2 outcome treats this as "control specification"; AU ISM-1546 is silent. |
| Crypto-mining workload deployment post-compromise | (No native TTP — closest T1580 + T1496) | ATT&CK Enterprise | GPU instance spike in unused region; outbound traffic to known mining-pool ASNs | Detectable via billing + region anomaly + GPU-instance-family selection. No framework enumerates billing anomaly as a security signal. |
| Help-desk social engineering for MFA reset | (Social engineering — no MITRE TTP for the SE step itself; result T1078) | ATT&CK Enterprise | Voice-clone + impersonation of authorised user; SE'd help-desk agent resets MFA | OOB-callback policy + voice-channel deepfake-resistant verification is operational; coverage fragmentary. Companion skill `identity-assurance` for AAL/FAL framing. |
| Audit-log disablement for defence evasion | (No precise mapping — closest T1685.002 Cloud Logs) | ATT&CK Enterprise | StopLogging / DeleteTrail / DiagnosticSettingsDelete; sink redirection to attacker-controlled bucket | Detected via meta-event firing on the disable action. Absence-is-evidence: any account with logging currently disabled is a finding regardless of an observable disable event. |

**Note on TTP coverage.** ATT&CK Enterprise covers cloud-IAM compromise reasonably well at the technique level. The gap is the chain shape — multi-step cross-account chains are not represented as first-class objects in either ATT&CK or ATLAS. Detection-strategy support (ATT&CK DSxxxx) for cloud techniques improves with v18-v19 releases but lags behavioural-graph monitoring.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch / Mitigation Available | Sector-Aware Detection |
|---|---|---|---|---|---|---|---|---|
| CVE-2024-1709 ScreenConnect auth bypass (cloud-runtime adjacent) | 10.0 | 75 | Yes (2024-02-22) | Yes | No | Confirmed mass exploitation | Vendor patch | EDR + identity-protection |
| CVE-2024-21626 runc container escape | 8.6 | 35 | No | Yes | No | None recorded | Vendor patch | Container-runtime telemetry |
| CVE-2024-3094 xz-utils supply-chain backdoor | 10.0 | 45 | No | Yes | No | Suspected | Vendor patch | SBOM-driven detection |
| CVE-2026-20182 Cisco SD-WAN cloud-edge | 10.0 | 65 | Yes (2026-05-14) | No | No | Confirmed | Vendor patch | Network telemetry |
| CVE-2026-30623 Anthropic MCP STDIO (cloud-hosted MCP servers) | 8.8 | 30 | No | Yes | No | Suspected | Vendor patch + config hardening | MCP-aware telemetry |
| Leaked access key in public repo (Snowflake-AA24-class) | n/a (config) | high (exploited within minutes) | n/a | Documented at scale | n/a | Confirmed mass exploitation | Configuration hardening + key rotation + scraper-bot countermeasures | GitGuardian / Trufflehog firehose; behavioural detection on CreateAccessKey + key-use anomaly |
| IMDSv1 SSRF / metadata exfil | n/a (design class) | high | n/a | Documented at scale | n/a | Confirmed ongoing | IMDSv2 enforcement | VPC Flow Logs + CloudTrail Insights |
| OIDC trust-policy wildcard subject claim (fork-PR-to-takeover) | n/a (config class) | high | n/a | Demonstrated 2024-2026 | n/a | Suspected ongoing | Trust-policy tightening + per-environment OIDC trust | Trust-policy static analysis + assume-role telemetry |
| Cross-account assume-role chain | n/a (behavioural class) | risk-modelled, not CVSS | n/a | Demonstrated in red-team | n/a | Confirmed in IR data 2024-2026 | Mitigation only — cross-account chain monitoring, SCP tightening, external-id enforcement | CloudTrail graph analytics (rare) |
| Azure managed-identity token replay | n/a (design class) | high | n/a | Demonstrated 2025-2026 | n/a | Confirmed | Continuous Access Evaluation rollout; token-binding | Azure Sentinel / Activity Log analytics |
| Help-desk SE for MFA reset | n/a (social engineering) | high (Scattered Spider 2023-2026 reference) | n/a | Demonstrated at scale | n/a | Confirmed ongoing | OOB-callback + voice-channel deepfake-resistant verification | Identity-protection signals + help-desk audit log |
| Crypto-mining post-compromise | n/a (consequence) | high (auto-monetised) | n/a | Documented at scale | n/a | Confirmed | Region SCP / Org Policy denies; billing alerting | Cost Explorer / Cost Anomaly Detection |
| Audit-log disablement | n/a (defence evasion) | high | n/a | Documented | n/a | Confirmed | Org-level CloudTrail / Aggregated Sink that cannot be disabled by member accounts | Meta-event alerting |

**Honest gap statement.** Vendor-specific CSP CVEs (AWS, GCP, Azure platform CVEs) are not exhaustively inventoried in `data/cve-catalog.json`. CSP vulnerability disclosures are partial — providers historically remediate without CVE issuance under their shared-fate model. Authoritative sources: AWS Security Bulletins, GCP Vulnerability Reward Program publications, Azure Security Response Center, CSP-specific bug-bounty disclosures. Forward-watched.

---

## Analysis Procedure

This procedure threads defense in depth, least privilege, and zero trust through every step. Pair it with the `cloud-iam-incident` playbook for the operational seven-phase walk.

**Defense in depth.** Multi-layer authentication at every privilege boundary: AAL3 / FIDO2 device-bound passkey for human admins (skill `identity-assurance`); per-account SCP / Org Policy / Management Group denies; cross-account external-id on every assume-role trust; KMS / Cloud KMS / Key Vault key-policy least-privilege; resource-policy default-deny; network-layer segmentation (D3-NTA) between accounts and between zones; behavioural CloudTrail / Cloud Audit Log analytics (D3-IOPR) on top of posture tools; out-of-band confirmation on root-equivalent actions; help-desk OOB-callback for MFA resets.

**Least privilege.** Per-principal scope; CWE-863 default-permissive role assignments are the dominant failing. External-id on every cross-account trust; non-wildcard subject claims on every federated OIDC trust; audience-pinned SAML; session-policy tightening on every AssumeRole / AssumeRoleWithSAML / AssumeRoleWithWebIdentity to scope-down beyond the role's permissions; KMS key-policy explicit-allow rather than IAM-policy-via-default-deny; managed-identity scope-token TTL ceilings (scope-token TTL ceilings: <= 1 hour for non-CAE-enabled, <= 24 hours with CAE).

**Zero trust.** Every action re-evaluated, not session-trusted; root / global-admin actions require step-up; cross-account assume-role chains monitored continuously; federated trust treated as untrusted-until-claim-validated; managed-identity tokens bound to instance identity where the CSP supports it; AI-channel egress (LLM API calls from instances) explicitly allowlisted on the administrative jump zone.

### Step 1 — Baseline collection (always)

Pull the 90-day audit log (CloudTrail / Cloud Audit Logs / Activity Logs) for every account in scope. Pull the current IAM principal inventory (users, roles, service accounts, managed identities, federated principals). Pull the federated IdP configuration. Pull SCP / Org Policy / Management Group state and recent change history. Pull recently-created access keys filtered to the last 90 days. Pull recently-modified resource policies. Pull 30-day billing data grouped by region + instance-family. Pull Access Analyzer / Policy Analyzer findings.

If audit logging is disabled or short-retention on any account: emit `audit-log-coverage-gap` and the look phase is structurally incomplete on that account.

### Step 2 — Indicator firing pass

Run the ten indicators from the `cloud-iam-incident` playbook against the collected artifacts:

- `root_login_from_new_asn`
- `mass_iam_user_creation_outside_iac`
- `unused_region_resource_creation`
- `gpu_instance_creation_spike`
- `iam_access_key_created_no_iac_ticket`
- `cross_account_assume_role_anomaly`
- `imds_v1_legacy_access`
- `kms_key_policy_self_grant`
- `s3_bucket_policy_public_grant`
- `cloudtrail_logging_disabled_event`

For each firing, run the indicator's `false_positive_checks_required` set. Do not let an indicator carry into the analyze phase without the FP checks completing.

### Step 3 — Cross-account chain reconstruction

If `cross_account_assume_role_anomaly` fires (or if any other indicator suggests cross-account reach), reconstruct the assume-role graph for the last 90 days. Walk from the suspected source principal through every successful AssumeRole / AssumeRoleWithSAML / AssumeRoleWithWebIdentity event. Identify chains traversing >= 2 account boundaries within a common 24h window. Cross-reference each hop's external-id against the documented integration inventory. Wildcard external-id or absent external-id on a multi-hop chain is the strongest distinguishing signal.

### Step 4 — Federated-trust hygiene audit

Audit every IAM role / service-account binding / Azure AD application with a federated trust policy. For each, validate:

- Subject claim specificity (non-wildcard `repo:owner/repo:ref:refs/heads/main` rather than `repo:*`)
- Audience constraint (pinned to per-integration value, not the default)
- Signing-key rotation cadence (within documented policy)
- MFA-required Conditional Access on federated admin sessions

Document any role where the federated trust would allow a fork-PR / cross-tenant / unintended principal to assume.

### Step 5 — IMDS posture audit

Inventory all instances. For each, determine IMDS posture (v1-only, v2-available-but-v1-allowed, v2-required). Cross-reference against IMDS access patterns from VPC / NSG Flow Logs. Any instance with v2 available but v1 still allowed is a finding; any v1 access from a non-localhost source-IP is a higher-confidence finding.

### Step 6 — Resource-policy diff against IaC baseline

For every recently-modified resource policy (S3 bucket policy, KMS key policy, Lambda function policy, etc.), diff the modification against the IaC baseline (Terraform state / Pulumi state / CloudFormation drift / Bicep what-if). Any out-of-band change is a finding. KMS key-policy self-grant (the modifying principal is the same as the granted principal) is a high-confidence indicator.

### Step 7 — Billing-anomaly cross-reference

Cross-reference billing anomalies (GPU-instance spike, unused-region cost, egress spike) against the operator's documented workload inventory. Untagged spikes in regions outside the baseline are crypto-mining-shaped. Tag presence + ML-platform service-principal as creator demotes the indicator.

### Step 8 — Snowflake-AA24-class cross-system check

If the operator has any third-party IdP integrated with both downstream SaaS and the cloud (Okta, Azure AD, Google Workspace, Auth0): enumerate which SaaS systems honour the IdP AND which cloud-IAM trust policies honour the IdP. If a cross-system compromise of the IdP credential would reach both, document it as a chained-compromise exposure regardless of whether a current incident is in progress.

### Step 9 — Compliance theater check

Run the five theater tests in the dedicated section below.

### Step 10 — Remediation orchestration

Sequence remediation per the playbook's `remediation_paths`:

1. Rotate root credentials and revoke sessions on every compromised account.
2. Rotate every IAM access key reachable from the compromised principal.
3. Audit IaC drift; quarantine compromised resources via deny-all SCP / Org Policy / deny-assignment.
4. Review last 90 days of IAM events on every reachable account; revoke unrecognised cross-account trusts.
5. Enforce IMDSv2 globally.
6. Tighten federated trust (non-wildcard subject claims, audience pinning, MFA-required Conditional Access on admin).
7. Rotate KMS keys with policy changes in the compromise window.

### Step 11 — Multi-jurisdiction notification orchestration

Time every regulator-notification clock from `detect_confirmed`: DORA Art. 19 (4h), NIS2 Art. 23 (24h), GDPR Art. 33 + UK GDPR Art. 33 (72h), NYDFS 23 NYCRR 500.17 (72h), APPI Art. 26 (24h), PDPA s26D (72h), AU NDB scheme (30 days), CCPA / CPRA (60 days for California residents). Pre-draft the notification text using the playbook's `notification_actions` templates and present them for operator review.

### Step 12 — CSP-specific support engagement

Open a CSP support case at the appropriate severity (AWS Health Dashboard support case at urgency Critical for confirmed compromise; GCP support case at P1; Azure Service Health incident). CSPs have IR-assist resources (AWS Customer Incident Response Team / GCP rapid response / Azure DART) that can be engaged for confirmed compromise.

---

## Output Format

The output is the operator-facing cloud-IAM incident assessment. Every section is mandatory; missing data is reported as "no evidence" so absence is auditable. The audit-log coverage table anchors the entire assessment — gaps there propagate to every downstream finding as reduced confidence. Produce this structure verbatim:

```
## Cloud IAM Incident Assessment

**Assessment Date:** YYYY-MM-DD
**Account(s) in scope:** [list]
**Cloud provider(s):** [AWS / GCP / Azure]
**Regulatory exposure:** [EU GDPR / NIS2 / DORA / UK / NYDFS / AU / SG / JP / CA / ...]
**Critical or important functions in scope:** [list per DORA / equivalent]

### Audit-Log Coverage
| Account | Audit-Log Enabled | Retention | Coverage Gap Notes |

### IAM Principal Inventory
| Account | Principal Class | Count | Long-Lived-Key Holders | MFA Coverage |

### Federated Trust Posture
| Trust Provider | Bound Account(s) | Subject-Claim Specificity | Audience Constraint | Signing-Key Rotation |

### Indicator Firings (10-indicator pass)
| Indicator | Account | Confidence | FP Checks Completed | Verdict |

### Cross-Account Assume-Role Chains
| Source Principal | Chain Length | Account Boundaries | External-ID Posture | Anomaly Verdict |

### IMDS Posture
| Account | Instance Count | IMDSv2-Required % | IMDSv1 Access Events |

### Resource-Policy Modifications
| Account | Resource | Modification Date | IaC-Baseline Match | Self-Grant |

### Billing Anomalies
| Account | Anomaly Type | Region | Magnitude | Tagged Workload |

### Compliance Theater Findings
[Outcome of the five tests in the Compliance Theater Check section]

### Blast Radius Computation
[Per-compromised-principal blast_radius score 1-5]

### Defensive Countermeasure Plan (D3FEND)
[D3-MFA, D3-CBAN, D3-NTA, D3-IOPR, D3-CAA — concrete control placements by account]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### Multi-Jurisdiction Notification SLA Matrix
| Regulator | Window | Deadline | Notification Draft Status |

### CSP Support Case Status
| Provider | Case ID | Severity | Engaged IR Team |

### RWEP-Prioritised CVE Exposure
[Cloud-relevant CVEs ranked by RWEP from `data/cve-catalog.json`]
```

---

## Compliance Theater Check

Run all five tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — "We have SCPs so compromise has bounded blast radius."**
Ask: "Show me a 90-day inventory of cross-account assume-role events where the source principal was in an SCP-restricted account."

- If the answer is "SCPs prevent any privilege escalation": SCPs constrain principals within an account but do not block cross-account assume-role chains initiated from a compromised principal in an account where the SCP allows broad role assumption. Count chains traversing >= 2 account boundaries within 24h of a single source principal — SCPs do not see this pattern.
- Acceptable: SCPs combined with cross-account assume-role graph monitoring (rolling 24h windows), external-id enforcement on every cross-account trust, and behavioural CloudTrail analytics with the indicator set in this skill.

**Theater Test 2 — "Root account has MFA so identity hygiene is complete."**
Ask: "Inventory every IAM user, service account, managed identity, and federated principal with active long-lived access keys (last_used <= 90 days). For each, name the MFA posture on the underlying principal and the principal's last-used timestamp."

- If the answer is "all root accounts have MFA": root MFA is a 1-of-N control. The dominant 2024-2026 compromise vectors target non-root principals (Snowflake-AA24-class), service accounts (no human MFA), federated principals (bearer-token-based, MFA already evaluated at the IdP), and managed identities (token-based, no human MFA). Root MFA covers 1 principal class out of many.
- Acceptable: MFA posture documented across every human principal, bearer-token TTL ceilings on every non-human principal, federated-trust hygiene documented separately.

**Theater Test 3 — "Security Hub / SCC / Defender for Cloud is all green so the account is secure."**
Ask: "For each high-confidence indicator in the `cloud-iam-incident` playbook, name the Security Hub / SCC / Defender for Cloud control that would have fired had the indicator's behavioural signal been present."

- If the answer is "Security Hub covers IAM hygiene with control set IAM.*": Security Hub controls are coverage-based (e.g. IAM.6 "Hardware MFA should be enabled for the root user"). They flag configuration drift, not behavioural compromise. A green posture score has ~0 correlation with absence of cross-account chains, federated-trust wildcard subject claims, or IMDSv1 SSRF.
- Acceptable: posture tools deployed AND behavioural CloudTrail / audit-log analytics deployed AND coverage explicitly mapped against the indicator inventory in `cloud-iam-incident.detect.indicators`.

**Theater Test 4 — "IAM Access Analyzer catches anomalous IAM grants."**
Ask: "Compare 90 days of Access Analyzer / Policy Analyzer findings against 90 days of CloudTrail CreateAccessKey + AssumeRole + CreateUser events outside the documented IaC apply window. Any CreateAccessKey event that Access Analyzer did not surface — name it and explain why."

- If the answer is "Access Analyzer covers IAM anomalies": Access Analyzer is a static-analysis tool that flags resource-policy reachability from external principals. It does not detect principal-action events (an attacker creating their own access key on a compromised user; an attacker assuming a role into a target account via legitimate SAML). The dominant 2024-2026 compromise vectors are principal-action-shaped, not resource-policy-shaped.
- Acceptable: Access Analyzer plus a principal-action behavioural-anomaly layer (the indicator set in this skill), with documented evidence of coverage of both.

**Theater Test 5 — "We use OIDC for CI so there are no static cloud credentials."**
Ask: "Inventory every IAM role with a trust policy referencing token.actions.githubusercontent.com or the GitLab / CircleCI / Bitbucket equivalent. For each, name the subject claim, the audience constraint, and the action permissions."

- If the answer is "OIDC federation means no static keys": OIDC eliminates static keys on the CI side but creates a federated-trust attack surface. Wildcard `repo:*` subject claims, missing branch / tag constraints, default `sts.amazonaws.com` audience — each is a fork-PR-to-takeover primitive that the "no static keys" attestation does not cover.
- Acceptable: every federated trust policy uses non-wildcard subject claims with branch / tag constraints, audience pinned to per-integration value, and the policy reviewed at every Repository-add / CI-platform-migration event.

---

## Defensive Countermeasure Mapping

Maps cloud-IAM offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND ID | Technique | Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-MFA | Multi-Factor Authentication | Human-admin layer; help-desk MFA-reset gate | Per-principal MFA enrolment; phishing-resistant factors for any admin-equivalent principal | Step-up on root-equivalent action, AWS Organizations management actions, and AssumeRole into production accounts | Applicable to human principals. Service accounts / managed identities need scope-token + audience-binding constructs (not MFA). |
| D3-CBAN | Credential-Based Authentication | API + management plane; access-key issuance and rotation | Per-credential scope (action + resource + time window); CWE-798 prohibition on hard-coded credentials | Credential issuance just-in-time where feasible (IAM Identity Center session policies, GCP impersonation tokens, Azure Just-In-Time access); rotation cadence per documented policy | Applicable. Bearer-token TTL ceilings on every non-human principal (<= 1h non-CAE, <= 24h with Continuous Access Evaluation). |
| D3-NTA | Network Traffic Analysis | Inter-account / inter-zone boundary; IMDS metadata-service network; AI-API egress from administrative jump zones | Operator alerting scoped to operator's account / project / management group | Network-hostile-until-proven posture; IMDSv2 enforced; AI-API egress explicitly allowlisted | Applicable. AI-API egress monitoring from cloud-hosted workloads to LLM provider endpoints (OpenAI, Anthropic, Google) is a sub-control of DLP-aware NTA. |
| D3-IOPR | Input / Output Pattern Recognition | CloudTrail / Cloud Audit Logs / Activity Logs analytics; behavioural-graph monitoring | Cross-account assume-role graphs over rolling 24h windows; IAM-mutation events outside IaC apply baselines; billing anomalies | Every behavioural pattern verified against historical norm and against adversary-known patterns | Critical. Behavioural-analytics on cloud-IAM is the primary defensive control gap in mid-2026. Posture tools do not provide this; D3-IOPR placement is required. |
| D3-CAA | Credential and Access Analytics | Federated-trust-policy posture; cross-system credential-reuse mapping | Per-IdP downstream-consumer inventory; per-federated-role trust-policy condition specificity | Federated trust treated as untrusted-until-claim-validated; trust-policy condition specificity continuously attested | Applicable. Cross-system credential-reuse is the Snowflake-AA24-class vector; D3-CAA placement attests against this class. |

**AI-pipeline-specific posture.** Cloud-hosted AI workloads (SageMaker, Vertex AI, Azure ML, plus self-hosted on EC2 / GCE / Azure VM) introduce three AI-specific attack surfaces:

1. **AI-API egress from instances** — LLM API calls (OpenAI, Anthropic, Google) from cloud-hosted workloads provide a covert-channel C2 / exfil pathway. Skill `dlp-gap-analysis` covers the DLP framing; this skill covers the cloud-IAM framing — AI-API egress from administrative jump zones should be explicitly allowlisted or denied via SCP / Org Policy / NSG.

2. **Managed-identity token use by AI workloads** — AI workloads that hold managed-identity tokens with broad access (data-access, ML-platform-write, etc.) are high-value targets for prompt-injection attacks that pivot through the workload's identity. Skill `ai-attack-surface` covers prompt-injection; this skill covers the cloud-IAM blast-radius framing.

3. **AI-assistant generated IAM policies** — AI coding assistants increasingly generate IAM policies, often with overly-broad permissions (`Action: *` or `Resource: *`). This is a CWE-863 class issue at scale. Skill `mcp-agent-trust` covers MCP-side mitigation; this skill covers the cloud-IAM posture-tool detection requirement.

---

## Hand-Off / Related Skills

After producing the cloud-IAM incident assessment, chain into the following skills.

- **`cloud-security`** — for CSP-specific IAM construct inventory, posture-tool integration, and shared-responsibility framing. This skill scopes the IAM-incident-response workflow; `cloud-security` covers the broader cloud-posture surface.
- **`cred-stores`** *(playbook chain, not a skill)* — `_meta.feeds_into` on this playbook routes blast-radius >= 4 findings into the `cred-stores` playbook for KMS / Cloud KMS / Key Vault posture and access-key rotation hygiene. Hand-off is via the playbook chain, not a skill load.
- **`identity-assurance`** — for AAL / IAL / FAL framing on human-principal MFA posture, federated-identity assurance levels, and step-up authentication coverage on cloud admin actions.
- **`framework-gap-analysis`** — for the per-jurisdiction reconciliation called for in Output Format "Cross-Jurisdiction Framework Gap Summary."
- **`compliance-theater`** — to extend the five theater tests above with general-purpose theater detection across the wider GRC posture.
- **`incident-response-playbook`** — for multi-jurisdiction notification orchestration and CSP-specific support-engagement workflow.
- **`coordinated-vuln-disclosure`** — when the compromise involves a CSP-level vulnerability or an unpatched CVE in the compromised workload (e.g. ScreenConnect CVE-2024-1709 chained into cloud-IAM compromise).
- **`policy-exception-gen`** — for defensible exceptions when cloud-IAM remediation cannot complete within obligation windows.
- **`supply-chain-integrity`** — when the compromised account has published assets (npm / PyPI / Docker Hub / container registry write), the compromise chains into supply-chain blast assessment.
- **`ai-attack-surface`** + **`mcp-agent-trust`** — when AI workloads or MCP servers are deployed in the compromised account.
- **`dlp-gap-analysis`** — for AI-API egress controls and customer-data-exfil framing in cloud-hosted workloads.
- **`sector-financial`** — for DORA Art. 19 (4h) notification orchestration when the compromise affects a financial entity's critical-or-important function.
- **`sector-healthcare`** — for HIPAA breach notification when the compromise affects PHI.
- **`sector-federal-government`** — for FedRAMP / FISMA framing when the compromise affects a US-government workload.

**Forward watch.** AWS IAM Identity Center session-policy refresh and step-up-on-admin enforcement (anticipated 2026-H2); GCP Workload Identity Federation principal-set attribute mapping tightening (post-2026 Q3); Azure managed-identity continuous-access-evaluation rollout for cross-tenant trust; CISA Snowflake AA24 follow-up advisories; FedRAMP Rev 5 cloud-IAM control overlay; NIST 800-53 Rev 6 chain-of-assumptions sub-control (anticipated 2027); ISO/IEC 27017:2027 cloud-IAM hardening; UK CAF v4 cloud-IAM specificity in B2; AU ISM update enumerating cloud non-human-principal credential hygiene; DORA TLPT first-cycle aggregate findings on cloud-account-compromise scenarios; CSP shared-fate / shared-responsibility recalibration for federated-trust hygiene.
