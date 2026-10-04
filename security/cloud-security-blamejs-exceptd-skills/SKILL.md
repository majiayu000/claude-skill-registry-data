---
name: cloud-security
version: "1.0.0"
description: Cloud security for mid-2026 — CSPM/CWPP/CNAPP posture, CSA CCM v4, AWS/Azure/GCP shared responsibility, cloud workload identity federation, runtime security with eBPF, AI workloads on cloud
triggers:
  - cloud security
  - cspm
  - cwpp
  - cnapp
  - csa ccm
  - aws security
  - azure security
  - gcp security
  - cloud iam
  - workload identity
  - irsa
  - cloud runtime
  - shared responsibility
  - multi cloud
  - falco
data_deps:
  - cve-catalog.json
  - d3fend-catalog.json
atlas_refs:
  - AML.T0010
  - AML.T0017
  - AML.T0013
attack_refs:
  - T1078
  - T1530
  - T1190
  - T1552
framework_gaps:
  - NIST-800-53-CM-7
  - ISO-27001-2022-A.8.30
  - SOC2-CC9-vendor-management
  - FedRAMP-Rev5-Moderate
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-MFA
rfc_refs:
  - RFC-8446
  - RFC-9180
  - RFC-7519
  - RFC-8725
cwe_refs:
  - CWE-287
  - CWE-862
  - CWE-732
  - CWE-200
  - CWE-1188
  - CWE-798
d3fend_refs:
  - D3-NTA
  - D3-NTPM
  - D3-EAL
  - D3-IOPR
  - D3-CBAN
forward_watch:
  - CSA CCM v5 (in development) for AI-workload-aware control objectives and shared-responsibility refinement on managed AI services (Bedrock, Azure OpenAI, Vertex)
  - FedRAMP 20x continuous authorization transition through 2026 — machine-readable OSCAL controls, automated significant-change review, impact on commercial CSP authorizations
  - EU CRA (Cyber Resilience Act) digital-element requirements for cloud-shipped products and managed services starting Dec 2027 — three-year manufacturer transition already affecting CSP roadmaps
  - EU EUCS (European Cybersecurity Certification Scheme for Cloud Services) finalisation and adoption by ENISA — high-assurance tier requirements still being negotiated mid-2026
  - NIS2 essential-entity sectoral guidance maturation for cloud / managed-service-provider risk management (Art. 21 measures and supply-chain Art. 22 obligations)
  - DORA TLPT (threat-led penetration testing) extension to cloud-hosted critical ICT services — RTS adoption and supervisory practice still evolving
  - JP ISMAP-LIU (Information system Security Management and Assessment Program for Low Impact Use) acceptance into procurement workflows; ISMAP base programme audit cycle refresh
  - SG MTCS SS 584:2020 revision cycle for managed AI services and confidential computing
  - IN MeitY empanelment renewal and Cert-In CSP audit baseline updates following 2025 incident reporting directive amendments
  - CN MLPS 2.0 (Multi-Level Protection Scheme) cross-border cloud data-handling requirements under the 2024 Network Data Security Management Regulations
  - NYDFS 23 NYCRR 500 Amendment 2 (effective Nov 2024 with phased Nov 2025 / Nov 2026 milestones) third-party CSP risk assessment and MFA requirements
  - AWS Bedrock, Azure OpenAI, GCP Vertex AI shared-responsibility documentation drift — each major CSP refreshes the AI-service responsibility line every 6–12 months; track for control-mapping breakage
  - eBPF-based runtime detection coverage of confidential-computing enclaves (AWS Nitro Enclaves, Azure Confidential VMs, GCP Confidential Space) — partial visibility is a tracked detection gap
  - CISA KEV additions for cloud-control-plane CVEs (IMDSv1 abuses, federation token mishandling, cross-tenant boundary failures); CISA Cybersecurity Advisories for cross-cloud advisories
last_threat_review: "2026-09-18"
---

# Cloud Security (mid-2026)

## Threat Context (mid-2026)

Cloud is where AI runs. Every consequential AI service — OpenAI, Anthropic, Google Gemini, AWS Bedrock, Azure OpenAI, GCP Vertex AI — is a multi-tenant cloud workload. Every enterprise that consumes those services is exposing some portion of its corpus, its prompts, and its access tokens across a shared-tenancy boundary that the consumer does not administer. Every enterprise that hosts its own AI inference (Bedrock with custom models, Azure OpenAI deployments, SageMaker endpoints, Vertex endpoints, GKE/EKS/AKS-hosted vLLM / TGI / Triton) inherits the full posture of the underlying cloud account: IAM, network, secrets, runtime, data, key management. Cloud security is the floor under AI security; lift the floor and the AI controls become moot.

**CSPM / CWPP / CNAPP convergence is the dominant architecture as of mid-2026.** Wiz, Orca Security, Palo Alto Prisma Cloud (Compute + Code + Data + Identity + Web), Microsoft Defender for Cloud, CrowdStrike Falcon Cloud Security, Sysdig Secure, Aqua Security, Lacework (now part of Fortinet), Check Point CloudGuard, Tenable Cloud Security, Snyk Cloud, and Trend Micro Cloud One all market CNAPP suites that fuse posture (CSPM), workload protection (CWPP), entitlement management (CIEM), data-security posture (DSPM), and increasingly AI-security posture (AI-SPM). Coverage of AI-specific risks is uneven — Wiz AI-SPM, Orca AI Security, Palo Alto Prisma AIRS, and Microsoft Defender for AI Workloads each chase a different definition of "shadow AI inventory" and "AI workload egress." None of them is a substitute for the consumer's own AI threat modelling; chain to `ai-attack-surface` and `mcp-agent-trust` for that.

**Identity federation between cloud workloads and AI services is the new attack surface.** Workload identity federation (AWS IAM Roles for Service Accounts (IRSA), AWS Pod Identity, Azure Workload Identity, GCP Workload Identity Federation, Kubernetes ServiceAccount tokens projected through OIDC) eliminates the worst class of static credential — the long-lived AWS access key, the Azure service-principal secret in a YAML file, the GCP service-account key JSON in a repo. The replacement is short-lived federated tokens signed by a trusted issuer. The new attack class: trust-policy misconfiguration (overly broad `sub:*` matches), issuer misconfiguration (accepting any issuer that produces a valid OIDC token), and confused-deputy patterns where a federated workload is granted privilege intended for a different consumer. AWS, Azure, and GCP each shipped 2024–2025 documentation refreshes after high-profile trust-policy abuse incidents; the controls landed unevenly.

**The Snowflake 2024 incident remains the canonical shared-responsibility-ambiguity case study.** The breach affected ~165 Snowflake customer tenants. Snowflake's position: customers must enforce MFA on their own user accounts; Snowflake's identity layer was not compromised. Customer position: a managed-cloud-data-warehouse provider should default-deny non-MFA access to enterprise data. Both are defensible. Neither side's framework citation — SOC 2 CC6.1, ISO 27001:2022 A.5.17, CSA CCM IAM-02 — adjudicated the dispute because all of them are method-neutral on which party operationalizes the control. The lesson encoded into mid-2026 cloud security: the shared-responsibility line for data-layer access controls is contested at every major SaaS / managed-AI / managed-data provider, and the consumer cannot rely on the provider's default posture to be safe.

**State-aligned cloud-control-plane targeting is operational reality.** Storm-0558 (June 2023, Microsoft Exchange Online via a stolen MSA consumer signing key that improperly signed enterprise tokens) demonstrated cross-tenant token-forgery against the CSP's identity layer itself. Midnight Blizzard (Jan 2024, Microsoft corporate tenant via password-spray against a legacy non-MFA test tenant pivoting through OAuth application consent) demonstrated that cloud-identity attacks land at the CSP's own enterprise — not only at customer tenants. CSP-side IR transparency improved unevenly through 2024–2025; consumer-side detection of CSP-control-plane abuse remains weak across the industry as of mid-2026 because CloudTrail / Azure Activity Log / GCP Cloud Audit Logs only show what the CSP chooses to surface. AI-discovered cloud-misconfiguration is now operational: adversaries using LLM-driven reconnaissance to triage exposed S3 / GCS / Blob storage at scale, AWS / Azure / GCP IAM trust-policy text to identify confused-deputy paths, and Kubernetes manifests in public repos for hardcoded credentials and overly-scoped service accounts.

**Cloud runtime security has shifted from agent-based to eBPF-based.** Falco (CNCF, primary upstream maintained by Sysdig) is the reference open-source eBPF-based runtime detector. Tetragon (Isovalent / now part of Cisco) is the Cilium-aligned alternative. Tracee (Aqua) is a third-party option. All major CWPP vendors (Sysdig, CrowdStrike, Microsoft Defender for Containers, Palo Alto Prisma Cloud Runtime, Wiz Runtime Sensor, Aqua) ship eBPF-based runtime detection as the default agent in 2026 because agent-in-container approaches do not scale to ephemeral workloads and confidential-computing modes. eBPF coverage of confidential-computing enclaves (AWS Nitro Enclaves, Azure Confidential VMs, GCP Confidential Space) is partial as of mid-2026 — the trade-off between confidentiality from the CSP and observability for the consumer is unresolved.

**Cloud is the canonical ephemeral environment.** Lambda / Cloud Functions / Azure Functions / Cloud Run / ECS Fargate / AKS Pod / EKS Pod / Knative workloads have lifetimes measured in milliseconds to minutes. Patch-cycle-based controls are architecturally inapplicable; rebuild-on-change is the norm; runtime detection must record sufficient telemetry within the workload's lifetime to enable post-hoc analysis after the workload no longer exists. Compensating-control programmes built for long-lived VMs do not transfer; this is the opposite of the OT/ICS inversion documented in `ot-ics-security`. Every recommendation in this skill is scoped to the ephemeral reality of cloud-native workloads first, with the long-lived VM-and-managed-services case treated as a secondary applicability note.

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NIST 800-53 Rev 5 CM-7 (Least Functionality) | Component configuration to provide only essential capabilities | Method-neutral configuration management | Method-neutral on cloud means provider-default settings — public S3 buckets, default network ACLs, IMDSv1, broad-trust IAM policies — pass CM-7 unless the consumer explicitly hardens them. CSP "secure by default" claims are uneven; CM-7 cannot adjudicate which posture is "essential." |
| NIST 800-53 Rev 5 SC-7 (Boundary Protection) | Boundary protection at network perimeter | On-prem and traditional cloud network perimeters | Modern cloud workloads have no fixed perimeter — service-to-service traffic crosses VPCs, accounts, organizations, and CSPs. SC-7 cannot scope egress for an AI workload that calls api.openai.com from a Lambda inside a private subnet via a NAT gateway; the "perimeter" is a fiction. |
| ISO 27001:2022 A.8.30 (Outsourced Development) | Outsourced ICT services and software development | Vendor and supply-chain governance | A.8.30 covers vendor management as a process; it does not specify cloud-shared-responsibility operational tests (MFA enforcement at the consumer side, default-deny public storage, federation trust-policy review, AI-service egress audit). The control is satisfiable on paper while the runtime posture remains open. |
| SOC 2 CC9.2 (Vendor Management) | Service-organization vendor risk management | Auditor-facing process | CC9.2 evidences a vendor-management programme — questionnaires, contracts, periodic reviews. It does not test whether the consumer's IAM trust policies on AWS / Azure / GCP federate to vendor identities safely. A vendor-management programme can be in good standing while the federation policy is broken. |
| FedRAMP Rev 5 Moderate | Federal cloud authorization baseline | US federal procurement of CSP services | US-only; controls inherit NIST 800-53 Rev 5 cloud-overlay weaknesses noted above. FedRAMP 20x continuous-authorization transition (through 2026) modernises the assessment cadence but does not close shared-responsibility ambiguity for AI workloads on managed services. |
| CSA CCM v4 (Cloud Controls Matrix, 197 controls across 17 domains) | Cloud-native control framework | Cross-cloud and SaaS posture | The most cloud-native framework in scope and the most useful for shared-responsibility decomposition. Voluntary, not regulatory. AI-workload-specific controls are sparse in v4 — CSA STAR Level 2 (third-party CSP assessment) audits a baseline that predates Bedrock / Azure OpenAI / Vertex as primary surfaces. CCM v5 (in development; see `forward_watch`) targets the gap. |
| AWS Well-Architected Security Pillar | Architectural guidance for AWS workloads | AWS-specific design patterns | Architectural guidance, not control attestation. WAFR-Security review is a self-attestation or Partner-led exercise; it does not produce an auditor-acceptable control statement. Useful for design-time hygiene; not sufficient for compliance evidence. |
| Azure Cloud Adoption Framework (CAF) Secure methodology | Azure adoption design patterns | Azure-specific design patterns | Same posture as AWS Well-Architected — design-time guidance, not control evidence. The Microsoft Cybersecurity Reference Architecture (MCRA) is the related operational reference; neither is a compliance framework. |
| GCP Security Foundations Blueprint | Reference Terraform for a secure GCP organization | GCP-specific design patterns | Reference design at organization-bootstrap time. Drift after deployment is uncontrolled; the blueprint does not include continuous posture-as-code enforcement. |
| EU GDPR Art. 28 (Processor obligations) | Data-processor obligations to data controllers | EU personal-data processing across any CSP | Art. 28 sets contractual posture (DPAs, processor obligations, sub-processor authorisation) but is silent on technical controls. The Schrems II rulings and adequacy decisions add data-transfer constraints that map unevenly onto cross-region AI inference paths. |
| EU NIS2 Directive Art. 21 | Risk management measures for essential and important entities | EU cybersecurity baseline | "Appropriate measures" language leaves Member State authorities to fill the cloud-specific gap unevenly. Cloud is named in NIS2 as a sector (cloud computing service providers are essential entities at >50 staff or >€10m turnover) but operational specifics depend on national transposition (DE BSI, FR ANSSI, NL NCSC, IT ACN, ES INCIBE-CERT). |
| EU CRA (Cyber Resilience Act) | Cybersecurity for products with digital elements placed on EU market | Manufacturer obligations | Applies to cloud-shipped products post-Dec 2027 — three-year transition. Does not retroactively fix the deployed brownfield SaaS / IaaS landscape. CRA Art. 13 reporting, Art. 14 vulnerability handling, Annex I essential requirements affect every CSP product placed on EU market after the cutover. |
| EU DORA + EUCS | Financial-sector ICT resilience + EU cybersecurity certification for cloud | EU financial services; cross-CSP certification | DORA applies to financial entities and their critical ICT third-party service providers (CTPPs) — major CSPs are CTPP-eligible. EUCS certification scheme (final form still negotiated mid-2026 per `forward_watch`) targets cross-EU CSP certification. Sovereign-cloud tier is contested. |
| UK GovAssure + NCSC Cloud Security Principles (14 principles) | UK government cloud adoption | UK government and OES | GovAssure replaces ITHC for UK government cloud assessment, phased rollout through 2026. NCSC Cloud Security Principles remain the operational reference for UK private-sector cloud — outcome-focused, not prescriptive. |
| AU IRAP (Information Security Registered Assessors Program) + AU PSPF | Australian government cloud assessment + Protective Security Policy Framework | AU government cloud procurement | IRAP is the assessment programme against the Information Security Manual (ISM) for cloud services. PSPF sets policy at federal level. Essential Eight maturity model is the operational baseline; ML 2 / ML 3 are the targets for sensitive workloads. |
| JP ISMAP | Information system Security Management and Assessment Program for government cloud | JP government cloud procurement | Government-cloud baseline; ISMAP-LIU (Low Impact Use) variant in maturation per `forward_watch`. Audit cadence still annual. |
| SG MTCS SS 584:2020 (Multi-Tier Cloud Security) | SG cloud security tiers (Level 1 / 2 / 3) | SG public-sector and regulated industry | Tiered CSP certification; Level 3 required for sensitive government workloads. Revision cycle for managed AI services per `forward_watch`. |
| IN MeitY empanelment + Cert-In CSP audit | India cloud empanelment for government use + Cert-In incident reporting | IN government cloud procurement and CSP operations | Empanelment is gating for government workloads; Cert-In 6-hour incident reporting directive (Apr 2022, amended 2025) applies to all CSP operators serving Indian users. |
| BR LGPD Art. 33 + ANPD cloud guidance | Brazilian personal data cross-border transfer rules | Cross-border CSP data handling | LGPD personal-data international transfer requires adequacy, contractual clauses, or specific authorisation. ANPD draft regulation on cross-border data transfers (in finalisation through 2025–2026) tightens the operational test. |
| CN Cybersecurity Review (CAC) + MLPS 2.0 | National security review for cross-border data and cloud services | CN cross-border cloud and CN-located CSP operations | Cybersecurity Review (Measures, July 2022) applies to CSPs handling >1m users' personal data planning overseas listing or significant data exports. MLPS 2.0 grading determines control baseline (Levels 1–5); Levels 3+ require government accreditation. The 2024 Network Data Security Management Regulations layer additional cross-border data obligations. |
| NYDFS 23 NYCRR 500.11 + Amendment 2 | NY financial-services third-party service provider security policy | NY-regulated entities (banks, insurers, money services) | Section 500.11 requires third-party CSP risk assessment; Amendment 2 (Nov 2024) phased MFA, encryption, asset inventory, and incident-response uplifts through Nov 2026. CSPs are explicitly in scope as third-party service providers. |

**Cross-jurisdiction posture (global-first, not US-centric).** Any cloud security assessment for a multi-jurisdiction operator must cite at minimum EU NIS2 + DORA + GDPR + CRA + EUCS, UK GovAssure + NCSC Cloud Principles, AU IRAP + PSPF + Essential Eight, JP ISMAP, IL INCD cloud directives, SG MTCS, IN MeitY + Cert-In, BR LGPD + ANPD, CN Cybersecurity Review + MLPS 2.0, NYDFS 500.11, alongside ISO 27001:2022 + ISO/IEC 27017 (cloud-specific) + ISO/IEC 27018 (PII in public clouds) + CSA CCM v4. US-only (NIST 800-53, FedRAMP, SOC 2) is insufficient for any operator with multinational data flows, which in cloud is essentially every operator.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Cloud user / federated identity | T1078 — Valid Accounts (incl. T1078.004 Cloud Accounts) | ATT&CK Enterprise | Federation-token abuse via misconfigured IAM trust policy; stolen SSO refresh tokens; OAuth application consent abuse (Midnight Blizzard pattern); IMDS credential extraction | NIST 800-53 IA-2 / AC-2 method-neutral on federation trust-policy specificity; CSA CCM IAM-02 silent on federation issuer validation; CWE-287 |
| Cloud data exfiltration | T1530 — Data from Cloud Storage Object | ATT&CK Enterprise | Public S3 / GCS / Blob storage discovery via Wiz-style external attack-surface scan; legitimate IAM principal exfil via federated workload; cross-tenant boundary failure on SaaS | NIST 800-53 SC-28 (encryption at rest) does not address access-policy errors; CWE-200, CWE-732, CWE-862 |
| Cloud-facing application | T1190 — Exploit Public-Facing Application | ATT&CK Enterprise | API Gateway / Load Balancer / managed-WAF-bypass; managed-database exposure (RDS / SQL DB / Cloud SQL public IP); container-registry public image abuse; Lambda / Cloud Functions / Azure Functions endpoint exploit | NIST 800-53 SC-7 perimeter assumption inadequate; CSA CCM AIS-04 and IVS-08 partial; CWE-1188 (Insecure Default Initialization) |
| Cloud-credential exposure | T1552 — Unsecured Credentials (incl. T1552.001 Files, T1552.005 Cloud Instance Metadata API, T1552.007 Container API) | ATT&CK Enterprise | IMDSv1 SSRF on EC2 / GCE; static cloud credentials in git / images / env vars; container API and kubeconfig theft; workload-identity-federation trust-policy abuse | CWE-798 (hardcoded credentials), CWE-200; NIST 800-53 IA-5 method-neutral |
| AI model registry / cloud-hosted model | AML.T0010 — AI Supply Chain Compromise | ATLAS v2026.09 | Bedrock / SageMaker custom model from poisoned upstream; Azure ML model registry tampering; Vertex Model Garden mirror tampering; HF model pulled into Bedrock / SageMaker / Vertex with weights backdoor | CSA CCM CCC-09 (vendor / supply chain) silent on model-supply-chain specifics; SLSA / in-toto / Sigstore for models still maturing |
| Cloud inference API abuse / model extraction | AML.T0013, Discover AI Model Ontology (inference-API probing for system-prompt, guardrail, model-family signal against cloud-hosted endpoints); AML.T0017, Develop Capabilities (downstream weaponization) | ATLAS v2026.09 | Programmatic query of Bedrock / Azure OpenAI / Vertex endpoint to extract model behaviour, training-data inference, system-prompt leakage | No cloud-specific ATLAS control mapping for inference-API rate-limit / anomaly detection; chain to `ai-attack-surface` |

**Note on ATT&CK Enterprise cloud-platform sub-techniques.** ATT&CK Enterprise has cloud-platform-specific matrices (IaaS, SaaS, Office 365, Azure AD / Entra ID, Google Workspace). T1078.004 (Cloud Accounts), T1552.005 (Cloud Instance Metadata API), T1552.007 (Container API), T1190 with cloud-service variants, T1530 with managed-storage variants are the most operationally relevant. The frontmatter pins the parent IDs; analysis should descend to the sub-technique appropriate to the cloud(s) in scope.

---

## Exploit Availability Matrix

| Surface / CVE Class | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch / Remediation Available | Live-Patchable | Cloud-Aware Detection |
|---|---|---|---|---|---|---|---|---|---|
| Misconfigured S3 / GCS / Azure Blob (public-access default; ACL misconfiguration; signed-URL leak) | n/a (config, not CVE) | risk-modelled — pattern is durable since Capital One 2019; continuous incidents 2020–2025 | n/a | Tooling: Stratus Red Team, CloudGoat, Pacu, S3Scanner, GCPBucketBrute, Microsoft Defender External Attack Surface Management | Yes — LLM-driven discovery of misnamed and exposed buckets at scale demonstrated through 2024–2025 | Continuous; weekly published incidents | Block-public-access toggles; tenant-wide bucket policy guardrails (S3 Block Public Access account-level, GCS Org Policy `iam.allowedPolicyMemberDomains`, Azure Storage `allowSharedKeyAccess=false`) | n/a (config drift, not patch) | CSPM (Wiz, Orca, Defender for Cloud, Prisma Cloud, Sysdig); native CSP scans (AWS Macie, Trusted Advisor; GCP Security Command Center; Azure Defender for Storage) |
| IMDSv1 SSRF on EC2 / GCE / Azure VM | n/a (architectural class) | risk-modelled — Capital One 2019 archetype; IMDSv2 mandatory by default on new EC2 instances (2024+); brownfield EC2, GCE without metadata firewall, and Azure IMDS exposure continue to surface | n/a | Yes — public PoCs since 2019; integrated into every cloud-red-team tool | Yes | Confirmed across multiple incidents 2020–2025 | IMDSv2 hop-limit enforcement (EC2); GCE metadata header `Metadata-Flavor: Google` required; Azure IMDS network-restricted | n/a | CSPM detects IMDSv1-enabled instances; CWPP runtime detects abnormal IMDS access from non-expected processes |
| IAM trust-policy / workload-identity-federation misconfiguration (confused deputy; overly broad `sub:*`; weak issuer validation) | n/a (config) | risk-modelled — high; surfaces frequently in cloud-pentest engagements | n/a | Pacu, Stratus Red Team, IAMVulnerable, awspx | Yes — LLM-driven IAM policy triage to find confused-deputy paths is now operational | Confirmed; multiple disclosed incidents 2023–2025 | Trust-policy refinement (require `sub` exact-match, `aud` validation, conditional `oidc:provider`); AWS IAM Access Analyzer external-access findings; GCP IAM Recommender; Azure PIM | n/a | CIEM (Wiz, Sonrai, Ermetic-now-Tenable, Orca, Prisma Cloud); native (IAM Access Analyzer, GCP Policy Intelligence) |
| Container-registry credential / token leak (kubeconfig, ECR / GCR / ACR pull credentials, GitHub Actions OIDC misconfiguration) | n/a (config / disclosure) | risk-modelled — high; trufflehog / gitleaks / Detect-secrets surface hits continuously | n/a | Yes — TruffleHog, gitleaks, GitGuardian | Yes — automated repository scraping at adversary scale | Continuous; reflected in CISA secrets-in-source-control advisories | Secret-rotation; short-lived federation tokens; revoke-on-detect; GitHub Advanced Security and Push Protection | n/a | DSPM (Cyera, Wiz DSPM, Symmetry, Concentric, Microsoft Purview DSPM, Sentra) |
| Cross-tenant control-plane bug (Wiz "ChaosDB" Cosmos DB 2021; "OMIGOD" 2021; "AzureScape" 2021; Sysrv-K Storm-0558 Microsoft signing-key 2023; "GhostToken" GCP 2023; recurring 2024–2025 cross-tenant findings) | varies | varies; KEV listing inconsistent | Some incidents added to KEV; many handled via CSP-private remediation without CVE issuance — itself a tracked gap | Vendor disclosure varies; PoC public for some, embargoed for others | Yes — substantial AI-assisted bug-bounty research at Wiz, Orca, MSRC, GCP VRP | Active campaign discovery 2023–2025 | CSP-side patch (consumer cannot patch); CSP transparency reports vary | No (CSP-side only) | CSP detection (Defender for Cloud, GCP SCC, CloudTrail behaviour) lags the disclosure cycle |
| AI workload egress to third-party inference (api.openai.com, api.anthropic.com, generativelanguage.googleapis.com from a cloud workload) | n/a | n/a | n/a | n/a (legitimate channel reused for data exfil) | n/a | Suspected — pattern surfaces in DLP/red-team assessments 2024–2025 | Egress allow-listing (VPC SC, AWS Network Firewall, Azure Firewall, GCP Cloud NGFW); per-endpoint TLS inspection where feasible | n/a | DLP-via-AI requires LLM-aware egress inspection — almost never present; hand off to `dlp-gap-analysis` |

**Honest gap statement (no fabricated CVE data).** This project's `data/cve-catalog.json` does not contain an exhaustive inventory of CSP-specific control-plane CVEs; many cross-tenant findings (ChaosDB, OMIGOD, AzureScape, GhostToken, Storm-0558 signing-key abuse) were resolved CSP-side without consumer-actionable CVE issuance — itself a transparency gap to track. Authoritative sources: AWS Security Bulletins (https://aws.amazon.com/security/security-bulletins/), Azure Security Advisories (MSRC), GCP Vulnerability Reward Program disclosures and GCP Security Bulletins, CISA Cybersecurity Advisories (https://www.cisa.gov/news-events/cybersecurity-advisories). Captured in `forward_watch` for catalog inclusion at next data refresh. Do not invent CVE IDs to fill the matrix.

---

## Analysis Procedure

This procedure threads the three foundational design principles (defense in depth, least privilege, zero trust) and the ephemeral-environment reality through every step.

**Defense in depth.** Six layered controls, no single layer relied on alone:

1. **CSPM (drift detection)** at the infrastructure layer — continuous evaluation of every account / subscription / project against a hardening baseline (CIS AWS / Azure / GCP Benchmarks, CSA CCM v4, FedRAMP overlay, NIST 800-53 cloud overlay). Drift is detected within hours, not weeks.
2. **CIEM (least-privilege IAM)** at the identity layer — per-principal scope, continuous detection of over-privileged roles, automated right-sizing recommendations, separation of human and workload identities.
3. **Workload identity federation** at the credential layer — no static credentials; all workload-to-cloud and workload-to-third-party auth via short-lived federated tokens (IRSA, AWS Pod Identity, Azure Workload Identity, GCP Workload Identity Federation, GitHub Actions OIDC, Spiffe/Spire for cross-CSP).
4. **Runtime security (eBPF / Falco / Sysdig / Tetragon / Tracee)** at the workload layer — kernel-level syscall and network telemetry; behavioural detection of process anomalies; egress visibility within ephemeral workload lifetimes.
5. **Egress controls (VPC Service Controls, AWS PrivateLink, Azure Private Endpoints, GCP Private Service Connect, Cloud NGFW)** at the network layer — default-deny egress; allow-list to specific endpoints; per-service-endpoint policies for AI-inference egress.
6. **Encryption (at rest, in transit, in use)** at the data layer — CSP-managed KMS or customer-managed keys (HYOK / BYOK / HSM-backed), TLS per RFC-8446 (RFC 8446) with PQC hybrid suites where supported, hybrid encryption per RFC-9180 (HPKE / RFC 9180) for envelope patterns, JWT validation per RFC-7519 and RFC-8725 (JWT best practices) for federation tokens, confidential computing (Nitro Enclaves, Azure Confidential VMs, GCP Confidential Space) for in-use protection where threat model requires.

**Least privilege.** Every cloud principal — human user, IAM role, service account, workload identity, AI-service invocation principal — receives minimum-necessary scope. AWS IAM Access Analyzer external-access and unused-permission findings, Azure PIM (Privileged Identity Management) just-in-time elevation, GCP IAM Recommender right-sizing recommendations, AWS Resource Access Manager scoped sharing, and CIEM tools (Wiz, Sonrai, Tenable Cloud Security, Orca, Microsoft Defender for Cloud CIEM, Prisma Cloud Identity Security) flag excess. The two anti-patterns to eliminate first: (a) any IAM principal with `*:*` action over `*` resource (the "ops star role"); (b) any federation trust policy with broad `sub:*` matching that allows any workload from a federated issuer to assume the role.

**Zero trust.** No implicit trust between cloud workloads. Service-to-service authentication via mutual TLS (mesh) or signed-token presentation per RFC-7519 / RFC-8725, validated per-request, not per-session. AI inference services authenticated per request (Bedrock Guardrails for identity-bound invocation; Azure OpenAI managed-identity-bound deployments; Vertex with workload-identity-bound endpoints). Cross-account / cross-tenant access requires explicit trust-policy review at every assumption point; no transitive trust.

**Ephemeral-environment reality.** Lambda / Cloud Functions / Azure Functions / Cloud Run / Fargate / Knative / Pod workloads have lifetimes too short for agent-install, signature-update, or patch-cycle controls. The compensating-control programme is image-time hardening (image scanning, distroless base, signed images via Sigstore Cosign), workload-identity-federation (no embedded credentials), eBPF-based runtime telemetry recording sufficient evidence within the workload lifetime, and aggressive egress allow-listing.

### Step 1 — Multi-cloud asset inventory

Enumerate every account, subscription, project, organization, and tenant across every CSP in use (AWS, Azure, GCP, OCI, Alibaba, plus any SaaS managed-AI consumer accounts — OpenAI organisation, Anthropic workspace, Google Gemini Enterprise project, Cohere account):

- AWS: list every account in every Organization; identify Control Tower / Landing Zone usage; identify Service Control Policy (SCP) coverage; identify regions in use.
- Azure: list every subscription in every Management Group; identify Azure Lighthouse delegations; identify policy assignments at MG / Subscription / Resource Group scope.
- GCP: list every project in every folder / organization; identify Org Policy hierarchy; identify VPC SC perimeters.
- For each CSP account: total resource count by service; identify "snowflake" accounts (no IaC, no tagging, no governance).
- Cross-cloud: enumerate identity federation edges (AWS↔Azure, AWS↔GCP, Azure↔GCP, on-prem AD / Entra ID / Okta / Ping / Auth0 ↔ CSP) and map the trust direction of each.
- SaaS-AI providers: enumerate per-org workspaces, API keys (count and last-rotation date), allowed-IP lists, SSO posture, audit-log access.

### Step 2 — CSPM scanning and drift detection

For each account / subscription / project:

- Run a current-state CSPM scan against the chosen baseline (CIS Benchmark + CSA CCM v4 + any sector overlay — FedRAMP for federal, HIPAA for healthcare, PCI for cards, NYDFS for NY-regulated financials).
- Score by severity and by RWEP (not CVSS — see `exploit-scoring`).
- Identify high-RWEP findings that are durable patterns (public S3, IMDSv1, broad-trust IAM, exposed managed-DB) for immediate remediation.
- Identify how many days the highest-RWEP findings have been open — if measured in weeks, the CSPM is read-not-acted-upon (compliance theater finding T1 below).
- Verify CSPM tooling itself is configured for daily scans, not quarterly — quarterly is theater for cloud cadence.

### Step 3 — IAM least-privilege audit

For every IAM role, service account, and managed identity:

- Generate Access Analyzer external-access findings (AWS), public/external access findings (GCP), and Defender for Cloud over-privileged identity findings (Azure).
- List every principal with `*:*` action — for each, document the justification or remediate.
- List every IAM role used by zero workloads in 90 days — orphaned roles are an audit finding and an attack surface.
- List every federation trust policy and validate: issuer pinned? `aud` claim required? `sub` claim exact-match (not prefix/wildcard)?
- For workload identities (IRSA, AWS Pod Identity, Azure Workload Identity, GCP Workload Identity Federation): map the K8s ServiceAccount ↔ cloud-role binding; verify the projection lifetime is short (1h or less); verify no static service-account key JSONs / access-key pairs exist in any workload.
- For OAuth application consent (Entra ID, Google Workspace, Slack Enterprise, GitHub Apps): enumerate every consented app, the scopes granted, and the consent date; revoke unused.

### Step 4 — Workload identity federation rollout audit

Specifically:

- For each Kubernetes cluster (EKS, AKS, GKE, self-managed on cloud VMs): is IRSA / AWS Pod Identity / Azure Workload Identity / GCP Workload Identity enabled? What ServiceAccounts can assume what cloud roles?
- For each CI/CD pipeline (GitHub Actions, GitLab CI, Bitbucket Pipelines, CircleCI, Jenkins on cloud): is OIDC federation to cloud IAM configured, or are static long-lived cloud credentials stored as CI secrets?
- For each cross-cloud workload (AWS workload assuming Azure role; Azure workload assuming GCP role): is the federation issuer trusted appropriately, or is it a transitive-trust pattern?
- For Spiffe/Spire deployments: SVID issuance policy, attestor configuration, federation across Spiffe trust domains.

### Step 5 — Runtime security coverage (eBPF / Falco)

- For each Kubernetes cluster and each VM fleet: is Falco / Sysdig / Tetragon / Tracee / CWPP-vendor-eBPF-agent deployed?
- What syscall rules are active? Default Falco ruleset is a floor — has the consumer added rules for cloud-specific patterns (IMDS access from unexpected processes, unexpected egress destinations, cloud-credential-file read)?
- Is the runtime telemetry exported to a SIEM with appropriate retention (90 days minimum for ephemeral workload post-hoc analysis)?
- For confidential-computing workloads (Nitro Enclaves, Azure Confidential VMs, GCP Confidential Space): what telemetry is available from inside the enclave, and what is the gap (per `forward_watch`)?

### Step 6 — Egress policy enforcement

- For every VPC / VNet / GCP network: enumerate egress rules; default should be deny-all with explicit allow-list.
- VPC Service Controls perimeters in GCP: which projects are in which perimeter, what services are restricted, what context-aware-access rules apply?
- AWS PrivateLink endpoints: list every VPC endpoint, the service connected, and the endpoint policy.
- Azure Private Endpoints: list every private endpoint, the service connected, and the network policies attached.
- AI-inference egress: every workload that calls api.openai.com / api.anthropic.com / generativelanguage.googleapis.com / managed Bedrock / Azure OpenAI / Vertex — is the destination allow-listed, is TLS inspection in place where the threat model permits, is the request/response logged for DLP review (chain to `dlp-gap-analysis`)?

### Step 7 — Secrets management

- KMS / Secret Manager / Key Vault usage: are application secrets stored in CSP-managed secrets services, or in env vars / config files / source repos / image labels?
- Customer-managed keys (CMK) usage vs CSP-managed keys: for which data classes is CMK required by policy / regulation, and where is it actually used?
- HSM-backed keys (CloudHSM, Azure Dedicated HSM / Managed HSM, GCP Cloud HSM): which workloads require FIPS 140-3 Level 3 backing, and where is it actually deployed?
- Secret rotation cadence: short-lived credentials (federation tokens, IRSA tokens) are the default; long-lived secrets (API keys, database passwords, encryption keys) have documented rotation cadence with last-rotation evidence.
- AI-service API keys: OpenAI / Anthropic / Cohere / Mistral API keys — are they in CSP secret stores, are they per-workload (not per-org), are they rotated, are usage / spend alerts configured?

### Step 8 — AI workload security posture (per CSP)

- **AWS Bedrock**: which models are enabled in the account; which IAM principals have `bedrock:InvokeModel` and at what scope; Bedrock Guardrails configured for which agents; Bedrock model evaluation logs retained; PrivateLink endpoint for Bedrock; KMS-CMK for Bedrock-stored prompts and outputs; cross-account model sharing reviewed.
- **Azure OpenAI**: which deployments exist, which Entra ID roles can invoke each, content-filtering categories and severity thresholds, customer-managed key on the resource, Private Link / Private Endpoint for the OpenAI resource, abuse-monitoring opt-out posture (if applicable for compliance), DLP integration with Purview.
- **GCP Vertex AI**: which model endpoints are deployed, which service accounts can invoke each, VPC-SC perimeter membership, CMEK on Vertex resources, Private Service Connect on endpoints, Model Armor and PII detection configured, audit-log retention.
- **Managed AI on K8s (vLLM, TGI, Triton, Ray Serve, BentoML)**: image provenance (signed; SLSA-attested), workload identity federation for upstream model pulls, eBPF runtime detection in the cluster, egress restriction from inference pods, prompt and completion logging for DLP review.
- **Shadow AI (per CSPM external-attack-surface scan)**: any workload egressing to api.openai.com / api.anthropic.com / etc. from a workload that does not own an AI use case — that is shadow AI; enumerate and govern.

### Step 9 — Shared-responsibility documentation per service

Produce a matrix: for each managed service in use (per CSP), document which party owns each control class — physical, infrastructure, network, host, application, identity, data, configuration, monitoring, incident response. The Snowflake-2024 lesson applies: the boundary line for data-layer access controls is often contested. Where the consumer has assumed the provider owns a control class without explicit evidence, flag the assumption — that is the most common breach root cause.

### Step 10 — Compliance Theater Check (see dedicated section below)

### Step 11 — Cross-jurisdiction output reconciliation

For each jurisdiction the operator is exposed to (US / EU / UK / AU / JP / SG / IN / BR / CN / IL / TW, plus state-level — NY DFS), produce a single mapping of the same control findings to that jurisdiction's regulatory language. Disparate findings for the same control deficiency across jurisdictions are themselves a finding.

---

## Output Format

The skill produces a Cloud Security Posture Assessment covering per-cloud (AWS / Azure / GCP / OCI / Alibaba) CIS Benchmark coverage, CSA CCM v4 control mapping, IAM least-privilege posture, IMDS / SSRF / metadata-service hardening, KMS / HSM key-management, and the prioritized remediation roadmap. The shape below is consumed downstream by `cloud-iam-incident` (which scopes IR with the IAM-finding list), by `container-runtime-security` (for workload-tier issues), and by `compliance-theater` (which compares the per-cloud control coverage against FedRAMP / IRAP / C5 / ENS / ISMAP claims). Preserve the per-control CIS Benchmark rows verbatim — they are the auditable evidence chain.

Produce this structure verbatim:

```
## Cloud Security Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Operator:** [name]
**Clouds in scope:** [AWS, Azure, GCP, OCI, Alibaba, ...]
**AI-service providers in scope:** [Bedrock, Azure OpenAI, Vertex, OpenAI, Anthropic, ...]
**Regulatory jurisdictions:** [US/FedRAMP/NYDFS, EU/NIS2/DORA/GDPR, UK/GovAssure, AU/IRAP, JP/ISMAP, SG/MTCS, IN/MeitY, BR/LGPD, CN/MLPS2.0, ...]

### Multi-Cloud Account Inventory
| CSP | Accounts / Subscriptions / Projects | Regions Active | IaC Coverage | Governance (Org / MG / Folder) |

### CSPM Scorecard (per account, RWEP-ranked)
| Account | High-RWEP Findings | Days Open (Max) | Baseline (CIS / CSA CCM / Sector Overlay) | Scan Cadence |

### CIEM / IAM Least-Privilege Report
| Principal Class | Count w/ *:* | Count Unused 90d | Federation Trust Policies Reviewed | Findings |

### Workload Identity Federation Inventory
| Workload Surface | Federation Mechanism | Static Credentials Removed | Trust-Policy Hygiene |

### Runtime Security Coverage
| Workload Surface | Sensor (Falco / Sysdig / Tetragon / vendor) | Rule Coverage | Telemetry Retention | Confidential-Computing Gaps |

### Egress Policy Map
| Source | Destination | Channel (PrivateLink / Endpoint / NAT / Public) | Allow-Listed | TLS-Inspected | Logged |

### Shared-Responsibility Matrix (per service)
| Service | Physical | Infra | Net | Host | App | Identity | Data | Config | Monitor | IR |

### AI Workload Security Posture (per provider)
| Provider | Models / Deployments | Identity Binding | Egress Posture | Content Filtering / Guardrails | CMK / CMEK | Audit-Log Coverage |

### Cross-Jurisdiction Control Mapping
| Finding | NIS2 | DORA | GDPR | FedRAMP | NYDFS | GovAssure | IRAP | ISMAP | MTCS | MeitY | LGPD | MLPS2.0 |

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-NTA, D3-NTPM, D3-EAL, D3-IOPR, D3-CBAN — concrete control placements by layer]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised CVE / Misconfiguration Exposure
[Cloud-control-plane and managed-service exposures ranked by RWEP, not CVSS; see `exploit-scoring` skill]
```

---

## Compliance Theater Check

Run all four tests. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — CSPM cadence and action.**
Ask: "Show me the Wiz / Orca / Defender for Cloud / Prisma Cloud / Sysdig / CrowdStrike Falcon Cloud / Aqua report from this week, and the ticket-burn-down for the High-RWEP findings."

- If the latest report is monthly or quarterly: CSPM is being used as compliance evidence, not as a security control. Cloud drift cadence is hours-to-days; quarterly is theater.
- If the report exists weekly but High-RWEP findings have been open longer than 30 days with no documented exception: CSPM is read-not-acted-upon. The tool exists for the audit; the security outcome does not.
- Acceptable answer: daily CSPM scan + High-RWEP findings closed-or-formally-excepted within a documented SLA appropriate to the finding class (public storage and broad-trust IAM same-day or near-same-day; less critical drift within sprint cadence).

**Theater Test 2 — Star-role enumeration.**
Ask: "List every IAM role / service principal / service account in every cloud account with `*:*` (action over all resources) and the documented business justification for each, signed by the role owner within the last 12 months."

- If the answer is "we have a star role for ops, everyone uses it, it's been there since we adopted the cloud": the least-privilege control is theater regardless of any documented policy. The CSPM tool's "over-privileged identity" finding is unactioned.
- If the answer is "we use it only via PIM / just-in-time activation with auditable approval and time-bounded sessions": that is acceptable for break-glass and operationally-justified administrative tasks, and the audit log demonstrates the rare-use pattern.
- Acceptable answer: a current list with documented justification per role, time-bounded activation for any standing access, and CIEM-tool right-sizing recommendations actioned for everything else.

**Theater Test 3 — Public-storage daily scan.**
Ask: "Show me the public-access scan of every S3 bucket / GCS bucket / Azure Blob container from yesterday, and the alert-and-response playbook for new public exposures."

- If the scan is not run daily: public-storage exposure detection is theater. The Capital One 2019 archetype is a continuing pattern; mid-2026 incidents land weekly across the industry.
- If the scan is run daily but the response playbook is "create a Jira ticket and assign to the owner": automated remediation (account-level Block Public Access in AWS, Org Policy `iam.allowedPolicyMemberDomains` in GCP, Storage Account `allowSharedKeyAccess=false` in Azure) is missing — the detection-without-remediation cycle is partial control.
- Acceptable answer: account-level public-access guardrails preventing the exposure at policy layer; daily verification scan as defence-in-depth; explicit policy-exception workflow (chain to `policy-exception-gen`) for the rare legitimate public-bucket use case.

**Theater Test 4 — AI workload egress policy.**
Ask: "What is the egress policy for every workload that invokes Bedrock / Azure OpenAI / Vertex AI / OpenAI / Anthropic / Cohere / Mistral, and where is the logged record of the prompts and completions retained for DLP review?"

- If the answer is "we don't restrict it" or "developers can call any AI API from any workload": the cloud-to-AI egress is uncontrolled — this is a DLP-via-AI exposure surface. Hand off to `dlp-gap-analysis` for control mapping.
- If the answer is "we use the managed CSP-AI services (Bedrock / Azure OpenAI / Vertex) with PrivateLink / Private Endpoint / Private Service Connect" but prompts and completions are not logged for DLP review: the channel is private but the content is unmonitored — exfiltration via prompt is undetected.
- Acceptable answer: per-workload AI-service allow-listing via VPC SC / PrivateLink / Private Endpoint; prompt and completion logging to a SIEM/DLP queue with retention appropriate to the data class; abuse-monitoring opt-out posture documented per compliance requirement; explicit policy on consumer-grade AI access (chatgpt.com, claude.ai, gemini.google.com) from work devices.

---

## Defensive Countermeasure Mapping

Maps cloud-security offensive findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability (controls impossible in serverless / ephemeral contexts name an explicit scoped alternative).

| D3FEND ID | Technique | Cloud Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline / Ephemeral Applicability |
|---|---|---|---|---|---|
| D3-NTA | Network Traffic Analysis | VPC / VNet flow logs; Cloud NGFW; eBPF-based CWPP sensor on every workload host; managed-service flow logs (PrivateLink, Private Endpoint, PSC) | Operator visibility scoped to the operator's tenant boundary; SOC-aggregated across tenants | Network treated as hostile until per-flow verified; default-deny egress with allow-list | Applicable to long-lived VMs and to ephemeral Lambda / Cloud Functions / Pods (kernel-level eBPF telemetry captured within workload lifetime). Confidential-computing enclaves are a partial-coverage gap per `forward_watch`. |
| D3-NTPM | Network Traffic Policy Mapping | VPC Service Controls perimeter map (GCP); AWS PrivateLink endpoint-policy map; Azure Private Endpoint Network Security Group map; service-mesh policy (Istio, Linkerd, Consul, Cilium) | Per-service-endpoint, per-direction policy | Continuous verification of traffic conformance to policy; deviation alerts | Critical for AI-inference egress: explicit per-endpoint policies for api.openai.com, api.anthropic.com, Bedrock endpoints, Azure OpenAI endpoints, Vertex endpoints. Ephemeral workloads inherit policy at scheduling time; rebuild-on-change is the patch model. |
| D3-EAL | Executable Allowlisting | Container image scanning + admission control (Kyverno, Gatekeeper, Polaris, Trivy in CI); Sigstore Cosign signature verification; signed-base-image policy; VM-host allowlisting where applicable | Per-image, per-workload allowlist | Default-deny execution; only signed-and-attested images run; image provenance verified per SLSA | Applicable to container images (the dominant cloud-native workload). Confidential-computing modes constrain runtime introspection but image-time allowlisting remains effective. For Lambda / Cloud Functions, the equivalent is signed-deployment-package and provenance-of-build attestations. |
| D3-IOPR | Input/Output Profiling | DLP / DSPM tooling profiling workload data flows; CASB profiling SaaS access; AI-inference prompt and completion logging with anomaly profiling | Per-workload, per-data-class profile | Behavioural deviation from baseline triggers verification | Critical for AI workloads — prompt and completion content is the new high-value channel for exfil; baseline profiling is essential to detect novel high-volume or sensitive-content prompts. Chain to `dlp-gap-analysis`. |
| D3-CBAN | Certificate-Based Authentication | mTLS for service-to-service (mesh-managed certificate issuance — Istio Citadel, SPIFFE/SPIRE SVIDs, Linkerd identity, Consul Connect); CSP-managed certificate authorities (AWS Private CA, Azure Key Vault Certificates, GCP Certificate Authority Service); short-lived federation tokens per RFC-7519 / RFC-8725; TLS per RFC-8446 (PQC hybrid where supported); hybrid encryption per RFC-9180 for envelope patterns | Per-workload identity bound to certificate; cross-workload presentation is per-request, not per-session | Verify-not-assume between every service pair; revocation surfaced to relying parties in real time | Applicable across the cloud-native stack. SPIFFE/SPIRE is the cross-CSP option for federation. AI-service invocation can be identity-bound via workload identity federation; the cert/token presentation per request is the zero-trust anchor for AI calls. |

**Ephemerality posture.** Cloud is the canonical ephemeral environment for this project. Controls must be expressible at image-build time (D3-EAL via Sigstore Cosign, SLSA attestation), at workload-schedule time (D3-NTPM via mesh policy, IRSA / Pod Identity / Workload Identity binding), at workload-runtime via kernel-level eBPF telemetry (D3-NTA, D3-IOPR), and at identity layer via short-lived federation tokens (D3-CBAN). Patch-cycle and signature-update controls inherited from on-prem programmes are architecturally inapplicable to sub-minute-lifetime workloads; the compensating-control programme is image-time hardening + runtime detection + aggressive egress allow-listing + ephemeral-credential-only identity. Recommendations that read "install agent X on the Lambda" are operationally indefensible — agents do not survive workload lifetimes; the eBPF-host-level alternative is the operational form.

---

## Hand-Off / Related Skills

After producing the cloud security posture assessment, chain into the following skills.

- **`api-security`** — every cloud workload exposes APIs (managed API Gateway, AppGateway, Cloud Load Balancing, Cloud Endpoints, EKS / AKS / GKE Ingress). API-layer authentication, authorization, rate-limiting, and schema-validation posture is the natural follow-on from cloud-IAM least-privilege.
- **`supply-chain-integrity`** — cloud-shipped container images, Helm charts, IaC modules (Terraform Registry / Pulumi Registry / Crossplane providers), and AI model registries (HuggingFace, Bedrock model catalog, Azure ML Registry, Vertex Model Garden) all require SLSA-style provenance, SBOMs (CycloneDX or SPDX), Sigstore signature verification, in-toto attestations. The cloud supply chain is the upstream of every cloud workload.
- **`identity-assurance`** — cloud IAM federation is the consumer-cloud parallel to identity-assurance (which is human-centric); workload identity federation, SPIFFE/SPIRE cross-domain trust, OIDC issuer validation, and FIDO2/WebAuthn for human cloud-console access all chain here. Many cloud breaches start with weak human-side identity at the cloud-console layer.
- **`dlp-gap-analysis`** — cloud-to-AI egress channels (managed AI service endpoints, public AI APIs, shadow AI), cloud-to-SaaS data flows, and managed-data-warehouse exfiltration paths are DLP control surfaces. The Snowflake 2024 lesson is a DLP-and-IAM joint failure.
- **`mcp-agent-trust`** — MCP servers deployed on cloud workloads (Lambda-hosted MCP, EKS-hosted MCP, managed-MCP via AWS / Azure / GCP integrations) inherit cloud-IAM and runtime-security posture. Tool-use governance on cloud-hosted MCP is a joint cloud + MCP control.
- **`ai-c2-detection`** — AI-API egress from cloud workloads (api.openai.com, api.anthropic.com, generativelanguage.googleapis.com) is the operational channel for AI-mediated C2; cloud egress controls (VPC SC, Private Endpoints, Cloud NGFW) and AI-aware traffic analysis chain together.
- **`kernel-lpe-triage`** — every cloud workload runs on a host kernel; Copy Fail (CVE-2026-31431), Dirty Frag (CVE-2026-43284 / -43500), and adjacent LPEs apply to EC2 / GCE / Azure VM hosts and to underlying nodes for managed K8s. CSP shared-responsibility means consumer responsibility for the guest OS on IaaS workloads; CSP responsibility for the underlying hypervisor.
- **`framework-gap-analysis`** — for any multi-jurisdiction operator, to produce the per-jurisdiction reconciliation called for in Analysis Procedure Step 11.
- **`global-grc`** — alongside framework-gap-analysis when EU NIS2 + DORA + GDPR + CRA, UK GovAssure + NCSC Cloud Principles, AU IRAP + PSPF, JP ISMAP, IL INCD, SG MTCS, IN MeitY + Cert-In, BR LGPD, CN MLPS 2.0, NYDFS 500.11 all apply.
- **`compliance-theater`** — to extend the four theater tests above with general-purpose theater detection on the operator's wider GRC posture.
- **`policy-exception-gen`** — to generate defensible exceptions for cloud workloads where a control (e.g., a documented public bucket for a static website, a star role for a documented break-glass scenario, an opt-out from CSP abuse monitoring for a compliance-driven reason) is justified. The exception evidence is the documented compensating-control programme.
- **`defensive-countermeasure-mapping`** — to deepen the D3FEND mapping above into a layered remediation plan with per-layer compensating-control combinations.

**Forward watch (per skill-format spec).** Tracked in the frontmatter `forward_watch` field: CSA CCM v5; FedRAMP 20x continuous authorization; EU CRA, EUCS, NIS2 sectoral guidance; DORA TLPT for cloud; JP ISMAP-LIU; SG MTCS revision; IN MeitY / Cert-In; CN MLPS 2.0 + 2024 Network Data Security Management Regulations; NYDFS 500 Amendment 2 milestones; AWS / Azure / GCP managed-AI shared-responsibility documentation drift; eBPF coverage of confidential-computing enclaves; CISA KEV additions for cloud-control-plane CVEs.
