---
name: identity-assurance
version: "1.0.0"
description: Identity assurance for mid-2026 — NIST 800-63 AAL/IAL/FAL, FIDO2/WebAuthn passkeys, OIDC/SAML/SCIM, agent-as-principal identity, short-lived workload tokens, OAuth 2.0 + RFC 9700 BCP
triggers:
  - identity assurance
  - aal
  - ial
  - fal
  - nist 800-63
  - fido2
  - webauthn
  - passkey
  - oidc
  - saml
  - scim
  - agent identity
  - workload identity
  - service account
  - federation
  - phishing-resistant
data_deps:
  - cve-catalog.json
  - exploit-availability.json
  - framework-control-gaps.json
  - rfc-references.json
atlas_refs:
  - AML.T0051
attack_refs:
  - T1078
  - T1556
  - T1110
framework_gaps:
  - NIST-800-63B-rev4
  - NIST-800-53-AC-2
  - ISO-27001-2022-A.8.30
  - SOC2-CC6-logical-access
  - PSD2-RTS-SCA
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-MFA
rfc_refs:
  - RFC-7519
  - RFC-8725
  - RFC-6749
  - RFC-9700
  - RFC-8032
cwe_refs:
  - CWE-269
  - CWE-287
  - CWE-306
  - CWE-732
  - CWE-798
  - CWE-862
  - CWE-863
d3fend_refs:
  - D3-MFA
  - D3-CSPP
last_threat_review: "2026-05-11"
---

# Identity Assurance Assessment

## Threat Context (mid-2026)

Identity is the new perimeter, and the perimeter expanded. The 2026 principal population is no longer "humans + service accounts" — it now includes AI agents acting on behalf of users, MCP servers exchanging short-lived tokens, and ephemeral workload identities minted per function invocation. Each of these is a principal that authenticates, holds scopes, and shows up in audit logs — and each was outside the design envelope of every identity standard in production use before NIST 800-63 rev 4 (Q4 2025).

**Agent-as-principal is operational reality.** When an AI coding assistant calls an MCP tool, it does so under the IDE user's OAuth session by default. The agent inherits the user's scopes wholesale — not because anyone designed it that way, but because no current identity standard defines an agent-as-principal model. CVE-2026-30615 (Windsurf MCP local-vector RCE, CVSS 8.0 / AV:L) hinged in part on this implicit inheritance: tool calls executed under the IDE user's privileges with no separate authentication challenge for the agent's actions. The principal who authenticated (the human) is not the principal who took the action (the agent), and the audit trail does not distinguish them.

**Phishing-resistant authentication is now table-stakes.** FIDO2 / WebAuthn synced passkeys are the only widely deployed authenticator class that survives credential phishing, AiTM proxy phishing (evilginx-class), and push-notification fatigue attacks. Orgs still standing on TOTP / SMS / push-MFA in 2026 are shipping password-equivalent risk forward, and the framework gap analysis must say so. AI-assisted phishing kit development means the time-to-weaponize a new bypass technique is hours, not weeks — AI acceleration is current operational reality, not a future consideration.

**Workload identity is short-lived or it is broken.** Static service-account keys and long-lived OAuth refresh tokens are credential-theft jackpots. RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) replaces the original RFC 6749 threat model and assumes short-lived access tokens, sender-constrained tokens (DPoP / mTLS), and rotated refresh tokens. Skills that cite RFC 6749 without RFC 9700 are citing the wrong threat model.

**Federation is the blast radius.** A single OIDC / SAML IdP compromise reaches every downstream SaaS. The SaaS-vs-IdP authority question — who is the source of truth for "this user has access" — must be answered explicitly. If a SaaS app silently provisions users on first-login without SCIM, the IdP is not actually the authority and offboarding is theater.

---

## Framework Lag Declaration

| Framework | Control | Why It Fails in mid-2026 |
|---|---|---|
| NIST 800-63B rev 4 (Q4 2025) | AAL / IAL / FAL definitions | rev 4 modernises authenticator types (passkey-first, phishing-resistance explicit at AAL3) and updates remote IAL2 proofing. It does **not** operationalise agent-as-principal identity: the model assumes a human subscriber holds an authenticator. An AI agent acting under a user's session is neither a subscriber nor a separate principal in 800-63 rev 4's vocabulary. Tracked in `data/framework-control-gaps.json` as NIST-800-63B-rev4. |
| NIST 800-53 | AC-2 (Account Management) | AC-2 enumerates account types (individual, group, service, system) but has no category for agent-mediated principals. Audit-log requirements assume the principal in the log is the principal that took the action — false when an AI agent acts on a user's session. |
| NIST 800-207 | Zero Trust Architecture | ZTA assumes subject = device + user. The "AI agent as subject" case is not in the published model; current ZTA deployments treat agent traffic as user traffic and miss the privilege step-up requirement. |
| ISO 27001:2022 | A.8.30 (Outsourced development) and A.5.16 (Identity management) | A.5.16 covers human and "automated entities" identity lifecycle but is silent on agent SDKs that act with user-bound tokens. A.8.30 was already flagged as silent on MCP-class tool providers; the same gap applies to agent identity. |
| SOC 2 | CC6 (Logical Access) | CC6.1 / CC6.2 / CC6.3 assume a human-or-service-account access model. Auditor evidence templates do not distinguish "user logged in" from "agent acted under user's token". Paper-MFA passes the auditor without phishing-resistance scrutiny. |
| EU NIS2 | Article 21(2)(g)-(j) — access management, MFA, secure authentication | Mandates "appropriate access management" and "use of multi-factor authentication where appropriate" without specifying AAL targets, phishing-resistance, or agent-principal scope. National transpositions vary; EU-CyCLONe coordination cases in 2025 cited identity controls as the most-divergent area. |
| EU DORA | RTS on ICT risk management, identity & access | Financial-entity scope. Mandates strong authentication for privileged access but defines it in terms of multi-factor, not phishing-resistance. AI-agent access to in-scope ICT systems is not addressed. |
| EU AI Act | Art. 14 (human oversight), Art. 15 (accuracy, robustness, cybersecurity) | High-risk AI systems must support human oversight. The Act does not specify identity assurance for the agent acting under human oversight, leaving the principal-of-record question open. |
| UK NCSC CAF | Objective B2 (Identity and access management), B2.a/B2.b/B2.c | CAF B2 is outcome-based and explicitly references phishing-resistant authentication for privileged access (good). It does not address agent-principal identity. |
| AU ISM | Controls 0974, 1173, 1546, 1559 (identity, authentication, MFA) | Mandates MFA for privileged users and phishing-resistant MFA for "highly privileged" users (good). Service-account guidance does not cover AI-agent acting-under-user. |
| AU Essential 8 | ML2/ML3 MFA controls | Maturity Model Level 3 requires phishing-resistant MFA for privileged users. Same agent-principal gap. |
| Singapore MAS TRM | §11 (Access Control), §14.2 (Authentication) | Privileged access multi-factor mandate; does not specify phishing-resistance and does not address agent-principal identity in MAS-regulated FI AI deployments. |
| Israel INCD identity directives (Doctrine 2.0 + Cyber Defense Methodology 2024) | Identity and access controls under Tier 1 critical infrastructure scope | Doctrine 2.0 elevates identity to a primary control plane but predates the agent-as-principal operational pattern. Tier 1 entities (critical infra, finance, healthcare) must apply MFA broadly; phishing-resistance is recommended, not mandated. |
| Switzerland FINMA Circ. 2023/1 (Operational risks and resilience — banks) | Strong customer authentication and privileged-access controls | Mandates strong authentication; defers technical specifics to industry practice. Does not address agent-principal identity in AI-enabled banking workflows. |
| Japan FISC Security Guidelines v9 | Identity baseline (Chapter on access management) | v9 baseline mandates MFA for privileged access in FI sector. Does not specify phishing-resistance. Agent-principal identity is silent. |
| Indonesia BSSN Reg. 8/2020 (electronic system security) | Identity controls under the Reg.'s access-management requirements | Strong-authentication for ESPs; does not specify AAL targets, phishing-resistance, or agent principals. |
| India CERT-In (SBOM + identity directives, 2022 + 2024 amendments) | Identity controls referenced alongside SBOM and incident-reporting | CERT-In Directions mandate accurate logging tied to identity (180-day retention). Does not specify AAL targets, phishing-resistance, or agent principals. |
| NY DFS 23 NYCRR Part 500 (amended Nov 2023) | §500.12 (Multi-Factor Authentication), §500.7 (Access Privileges) | Mandates MFA for any individual accessing the covered entity's information systems — explicit phishing-resistance not required (a documented gap). Agent-principal identity not addressed. |
| ISO/IEC 27001:2022 / 27002:2022 | A.5.16, A.5.17, A.5.18, A.8.5 (identity, authentication info, access rights, secure authentication) | The 2022 revision improves on 2013 but predates the agent-principal pattern and does not mandate phishing-resistance. |
| EU PSD2 RTS on Strong Customer Authentication (Reg. 2018/389) | SCA — two-factor authentication for payment initiation, account access, and remote transactions in scope of PSD2 | The canonical EU mandate for two-factor authentication in retail payments. RTS-SCA does not specify phishing-resistance (TOTP and SMS-OTP remain commonly deployed and accepted by NCAs) and predates the agent-principal pattern — an AI agent initiating a payment under a user's strongly-authenticated session is not contemplated. PSD3 / PSR revisions in progress; until then, SCA-compliant flows can still be defeated by AiTM relay against non-phishing-resistant factors. |

**Fundamental gap:** every framework above either pre-dates the agent-as-principal pattern or treats AI-agent acting-under-user as a service-account, which it is not. The cross-jurisdiction picture also shows that phishing-resistance is recommended-not-mandated almost everywhere — paper-MFA still passes most audits.

**Underlying RFC stack and its gaps.** Identity tokens ride on RFC 7519 (JWT) and MUST follow RFC 8725 (BCP 225) to avoid `alg=none`, key confusion, audience confusion, and `kid` traversal attack classes. OAuth 2.0 is RFC 6749, but the threat model has been superseded by RFC 9700 (Security Best Current Practice, January 2025) — operators citing only RFC 6749 are operating against a 2012 threat model. Signing primitives for federation assertions and passkey attestations rely on Ed25519 (RFC 8032) among others; the algorithm itself is robust, but PQC migration timelines from the `pqc-first` skill apply to long-lived federation trust roots. Reference `data/rfc-references.json` rather than restating content here.

---

## TTP Mapping

| ID | Technique | Identity-Assurance Relevance | Failing AAL/IAL/FAL Level | Gap |
|---|---|---|---|---|
| T1078 | Valid Accounts | Compromised credential reuse defeats AAL1 / AAL2 password-or-TOTP authenticators; survives most session controls until step-up. | Bypasses AAL1, AAL2. AAL3 phishing-resistant authenticators resist. | NIST-800-53-AC-2 has no agent-principal account category; valid-account abuse via inherited agent token is unattributable in standard audit pipelines. |
| T1556 | Modify Authentication Process | Adversary tampers with auth flow (golden SAML, federation-trust manipulation, conditional-access bypass). Defeats FAL1 / FAL2 federation assurance when assertion integrity is not cryptographically bound. | Bypasses FAL1, FAL2. FAL3 (cryptographic key-bound assertions) resists. | ISO-27001-2022-A.8.30 silent on federation trust-root tamper; SOC2-CC6 does not test FAL level. |
| T1110 | Brute Force (and sub-techniques: 1110.001 password guessing, 1110.003 password spraying, 1110.004 credential stuffing) | Defeats AAL1 password authenticators at scale; mitigated by rate-limiting, account lockout, and phishing-resistant AAL3. | Bypasses AAL1. AAL2 with rate-limit and AAL3 resist. | NIST-800-63B-rev4 contemplates rate-limit; no framework operationalises detection thresholds tied to AAL. |
| AML.T0051 | LLM Prompt Injection | An injected prompt makes the model exfiltrate or misuse a held credential (OAuth token in tool-call argument, API key in context). The compromised principal is the user-on-behalf-of-whom the agent acts — not a service account. | All AAL/IAL/FAL levels fail because the credential is *already authenticated*; the misuse is post-auth. Mitigation is scope minimisation and short-lived tokens (RFC 9700). | No identity framework addresses post-auth credential misuse by an inherited agent principal. |

---

## Exploit Availability Matrix

Sourced from `data/cve-catalog.json` and `data/exploit-availability.json` as of 2026-05-11.

| Threat | CVSS | RWEP | PoC Public? | CISA KEV? | AI-Accelerated Weaponization? | Patch / Mitigation? |
|---|---|---|---|---|---|---|
| CVE-2026-30615 (Windsurf MCP local-vector RCE — implicit identity inheritance) | 8.0 | 35 | Partial — conceptual exploit demonstrated | No (architectural class) | No direct AI-assisted weaponization recorded; the attack rides on agent tool-call autonomy under the user's inherited session, AV:L through attacker-controlled HTML the MCP client processes | Vendor IDE update; identity-layer mitigation is scoped agent token + tool allowlist (see mcp-agent-trust). |
| AiTM passkey-relay / FIDO2-bypass phishing kits | N/A (kit class, not vendor CVE) | N/A | Public research and limited in-the-wild observations; nothing fully bypasses **synced** passkeys without endpoint compromise (the device-bound private key remains in the secure enclave). Bypasses against TOTP / push-MFA / SMS are commodity. | Technique class | Yes — AI-assisted kit configuration and target-tailored lure generation are documented capabilities. | Mitigation: enforce phishing-resistant authenticators (passkey or hardware-token AAL3) for privileged roles; endpoint-binding (D3-CBAN) for highly-privileged roles. |
| OAuth refresh-token theft + replay (RFC 9700 BCP §2.2.2) | N/A (technique) | N/A | Yes — public research; commodity in adversary toolkits. | No (technique) | Yes — credential-theft → automated replay is well-AI-assisted. | Mitigation: short-lived access tokens, sender-constrained tokens (DPoP / mTLS per RFC 9700), rotated refresh tokens, refresh-token-reuse detection. |
| JWT validation-bypass class (RFC 8725 BCP failures: `alg=none`, key confusion, audience confusion, `kid` traversal) | Class-level — multiple vendor CVEs over time, current high-RWEP entries vary | N/A (class) | Yes — generic class with library-specific PoCs. | No (class) | Yes — AI-assisted scanning for vulnerable verifier configurations. | Mitigation: pin allowed algorithms server-side, validate `iss` / `aud` / `exp` / `nbf`, treat `kid` as untrusted input, follow RFC 8725 BCP. |
| AML.T0051 prompt-injection-driven credential exfiltration via agent | N/A (technique) | N/A | Yes — public research and demonstrated in-the-wild against IDE-resident agents. | No | Yes — adversarial instruction crafting is AI-accelerated. | Mitigation: short-lived per-agent tokens, scope minimisation, tool-arg DLP (see dlp-gap-analysis), no static credentials in agent context. |

**Interpretation:** the only vendor CVE in scope (CVE-2026-30615) has a patch path; everything else in this skill is configurational and architectural. Synced FIDO2/WebAuthn passkeys remain the strongest commodity authenticator class — no public technique fully bypasses them without endpoint compromise as of 2026-05-11.

---

## Analysis Procedure

This procedure threads the three foundational principles explicitly.

### Defense in Depth (multi-layer identity controls)

Identity is not a single control. The layered model the analysis must verify:

1. **Enrollment** — IAL2 (remote identity proofing) for standard users; IAL3 (in-person or supervised remote) for highly privileged roles. Verify proofing evidence quality and re-proofing cadence.
2. **Authentication** — AAL2 minimum for any access to organisational systems; AAL3 (phishing-resistant: FIDO2/WebAuthn passkey or PIV/CAC hardware token) mandatory for privileged roles and any agent-mediated session.
3. **Federation** — FAL1 minimum; FAL3 (cryptographic key-bound assertions, holder-of-key) for cross-organisational federation and any federation trust root.
4. **Session** — short-lived access tokens (RFC 9700 §4): minutes-to-hours for interactive, seconds-to-minutes for workload. Refresh-token rotation. Sender-constrained tokens (DPoP per RFC 9449 or mTLS per RFC 8705) for high-value scopes.
5. **Step-up** — re-authenticate for sensitive actions (PIM/PAM elevation, financial transactions, agent-initiated writes to production). Step-up MUST use phishing-resistant authenticator.
6. **Continuous** — signal-based re-evaluation (device-posture change, anomalous geo, agent behaviour drift). Revoke session on signal.

### Least Privilege (per-principal scope)

Every principal — including AI agents and MCP servers — gets a least-privilege scope:

- Human users: role-based + just-in-time elevation for privileged actions via PIM/PAM.
- Service accounts: scoped to the single workload they serve; rotated; ideally workload-identity-federated (no static key).
- **AI agents (this skill's distinct addition)**: agent SHOULD hold its own short-lived token, not the user's OAuth session. Where the agent acts under the user's session (today's default), the analysis MUST flag this as an inherited-principal finding and recommend separate agent tokens with explicit scope. Cross-reference mcp-agent-trust for the trust-tier model.
- MCP servers / tool providers: scoped to the resources they actually need; no shell unless the tool is explicitly a shell tool.

### Zero Trust (verify-not-assume on every request)

NIST 800-207 ZTA posture, extended for agents:

- Verify on every request, not just on session start.
- Never assume network position grants trust.
- Device posture is a first-class signal.
- AI agents and MCP servers are zero-trust subjects in their own right — agent-traffic from inside the network is not pre-trusted.
- Policy decision point (PDP) MUST receive an agent-distinguished signal in the request context.

### Concrete Steps

1. **Inventory all principals.** Pull from IdP (Entra ID / Okta / Auth0 / Google Workspace / Ping), workload-identity providers (Kubernetes service accounts, AWS IAM roles, GCP workload identity federation, SPIFFE/SPIRE registries), and AI-agent / MCP-server configs (`~/.claude/`, `~/.cursor/`, `~/.windsurf/`, `~/.gemini/`, `~/.vscode/`). Classify each as human / service / agent. **If AI agents are not enumerated, the inventory is incomplete and the analysis halts here pending a re-inventory.**

2. **Score each principal against AAL/IAL/FAL targets.** Produce the per-principal scorecard (see Output Format). Target table: standard user → AAL2 / IAL2 / FAL1; privileged user → AAL3 / IAL2 / FAL2; highly privileged (domain admin, IdP admin, financial-control roles) → AAL3 / IAL3 / FAL3; workload → workload-identity-federation with sender-constrained short-lived tokens; AI agent → its own AAL-equivalent scoped token (not inherited user session).

3. **Identify phishing-resistant coverage gap.** Per role-class, what % of users are on FIDO2/WebAuthn passkey or hardware token (PIV/CAC/YubiKey FIDO2)? TOTP and push-MFA and SMS do not count. Targets: 100% for privileged and highly privileged; ≥90% for standard users by EoY 2026.

4. **Map federation surface (OIDC/SAML).** Enumerate every OIDC RP and SAML SP. For each: which IdP is the authority? Is SCIM provisioning enabled, or does the SP silent-provision on first-login? What is the assertion signing algorithm and key rotation cadence? Is the IdP's signing key in an HSM? Cross-walk to RFC-8032 (Ed25519) algorithm choices where applicable.

5. **Audit token lifetimes against RFC 9700 BCP.** For each OAuth client: access-token TTL, refresh-token TTL, refresh-token rotation enabled?, sender-constraining (DPoP/mTLS) enabled for high-value scopes? Flag any access-token TTL > 1 hour for interactive or > 15 minutes for workload as a finding.

6. **Audit JWT validation against RFC 8725 BCP.** For each resource server / API gateway / MCP server validating JWTs: allowed algorithms pinned server-side? `iss`/`aud`/`exp`/`nbf` validated? `kid` treated as untrusted input? `alg=none` explicitly rejected? JWKS endpoint fetch hardened (HTTPS, cache TTL, fallback)?

7. **Audit MCP / agent privilege scopes.** For each MCP server in the inventory (cross-walk to mcp-agent-trust Step 1): does the agent hold its own token or inherit the user's? If inherited, document as a finding. What scopes does the inherited token grant? Where the agent CAN have its own token (e.g., agent-to-agent service-to-service flow), is it short-lived and DPoP-constrained?

8. **Audit SCIM provisioning lifecycle.** For each SaaS in scope: SCIM-provisioned (good — IdP is authority) or first-login-provisioned (bad — SaaS is silently authoritative)? On termination, how long until SaaS account is deactivated? Cite RFC 7644 (SCIM 2.0 protocol) for the lifecycle requirement.

9. **Compliance theater checks.** Execute the four tests in the Compliance Theater section as a final gate before the report goes out.

---

## Output Format

The skill produces an Identity Assurance Assessment covering per-IdP AAL/IAL/FAL posture, passkey / WebAuthn / FIDO2 deployment coverage, agent-identity scoping (workload, service-account, AI-agent principal), and the prioritized roadmap to close phishing-resistance gaps. The shape below is consumed downstream by `idp-incident-response` (which scopes IR on confirmed identity compromise), by `email-security-anti-phishing` (which inherits the phishing-resistant-MFA coverage), and by `compliance-theater` (which compares the deployed authenticator class against any AAL2 / AAL3 compliance claim). Preserve the per-IdP AAL / IAL / FAL rows verbatim — they are the auditable derivation of the phishing-resistance score.

```
## Identity Assurance Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [org units / IdPs / SaaS apps / workload clusters / AI-agent fleets in scope]
**Jurisdictions:** [EU NIS2 / DORA, UK CAF, AU ISM, ISO 27001, plus IL INCD / CH FINMA / JP FISC / SG MAS / IN CERT-In / NY DFS where applicable]

### Per-Principal Assurance Scorecard
| Principal | Class (Human/Service/Agent) | Current AAL | Target AAL | Current IAL | Target IAL | Current FAL | Target FAL | Gap |
|-----------|----------------------------|-------------|------------|-------------|------------|-------------|------------|-----|

### Phishing-Resistant Coverage Matrix
| Role Class | Population | On FIDO2/WebAuthn Passkey | On Hardware Token | On TOTP/Push/SMS Only | % Phishing-Resistant | Target % | Gap |
|------------|-----------|---------------------------|-------------------|----------------------|---------------------|----------|-----|

### Token Lifetime Audit (RFC 9700 BCP)
| OAuth Client / API | Access TTL | Refresh TTL | Refresh Rotation | Sender-Constrained (DPoP/mTLS) | RFC 9700 §-Compliant | Finding |
|--------------------|-----------|-------------|------------------|--------------------------------|----------------------|---------|

### JWT Validation Audit (RFC 8725 BCP)
| Resource Server | Allowed Algs Pinned | iss/aud/exp/nbf Validated | kid Hardened | alg=none Rejected | JWKS Fetch Hardened | Finding |
|----------------|---------------------|---------------------------|--------------|-------------------|---------------------|---------|

### Federation Surface (OIDC / SAML)
| RP / SP | IdP | SCIM Provisioned? | First-Login Provisioned? | Assertion Signing Alg | Key Rotation | FAL Level |
|---------|-----|-------------------|--------------------------|----------------------|--------------|-----------|

### Agent-Principal Inventory
| Agent / MCP Server | Holds Own Token? | Inherited User Session? | Scopes | Token TTL | Cross-Walk to mcp-agent-trust |
|--------------------|------------------|-------------------------|--------|-----------|-------------------------------|

### Framework Gap Declaration
[Per-framework: NIST 800-63B rev 4, NIST 800-53 AC-2, ISO 27001:2022 A.8.30, SOC 2 CC6, EU NIS2 Art 21, EU DORA RTS, UK CAF B2, AU ISM 0974+, plus IL/CH/JP/SG/IN/NY DFS — what the control nominally covers, what it misses for agent-principal and phishing-resistance, what a real control requires.]

### Remediation Roadmap
| Priority | Finding | Action | Owner | Target Date | Framework Gap Closed |
|----------|---------|--------|-------|-------------|---------------------|

### Compliance Theater Findings
[Outcome of the four tests below.]
```

---

## Compliance Theater Check

Four specific tests distinguish paper compliance from real posture:

1. **Principal inventory completeness.** "Show me the principal inventory, and confirm AI agents and MCP servers are enumerated as distinct principals (not folded into 'service accounts')." If AI agents are not enumerated, the access-control claim is incomplete by construction — every audit log that attributes an agent action to the human user is wrong by design. Failing this test means the SOC 2 CC6 / ISO A.5.16 / NIS2 Art 21 evidence is paper-only for the agent-mediated portion of the attack surface.

2. **Phishing-resistant coverage of privileged users.** "What percentage of your privileged users (any role with admin scope on IdP, finance, prod, source control, AI-agent configuration) are on phishing-resistant authentication — specifically FIDO2/WebAuthn passkey or hardware token (PIV/CAC/YubiKey FIDO2)?" "We use MFA" is theater unless phishing-resistance is specified. TOTP, push notifications, and SMS are not phishing-resistant in mid-2026; AiTM commodity kits defeat them daily. Target: 100% for privileged users.

3. **MCP / agent access token TTL.** "Show me the access-token TTL configured for your MCP server fleet and AI-agent integrations. Show me the refresh-token rotation policy." If access-token TTLs are measured in weeks, or are unconfigured / default-1-year-from-the-SDK, or refresh tokens are never rotated, this is theater against RFC 9700 BCP. The credential-theft blast radius is multiplied by the TTL.

4. **Cross-jurisdiction evidence.** "Show me your jurisdiction-specific identity-control evidence for every jurisdiction you operate in: EU NIS2 Art 21 transposition, DORA RTS, UK CAF B2, AU ISM 0974+, ISO 27001 A.5.16; plus IL INCD Doctrine 2.0 / Cyber Defense Methodology 2024, CH FINMA Circ. 2023/1, JP FISC v9, SG MAS TRM §11/§14.2, IN CERT-In Directions, NY DFS 23 NYCRR 500.12." US-only evidence (or worse, NIST-only evidence) for a multi-jurisdictional org is theater — global-first coverage is required, and identity evidence must be jurisdiction-specific rather than US-centric.

---

## Defensive Countermeasure Mapping

Maps the identity-assurance gaps above to MITRE D3FEND techniques with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability.

| D3FEND Technique | Mapping | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| **D3-MFA** (Multi-factor Authentication) | Counters T1078 (Valid Accounts) and T1110 (Brute Force) at the authentication layer; phishing-resistant variant (FIDO2/WebAuthn passkey) is the only commodity counter to AiTM relay attacks. | Layer 2 (Authentication) of the enrollment → authentication → federation → session → step-up → continuous stack. | Per-principal — each human, agent, and high-value service account authenticates with an MFA factor scoped to its role; AAL3 mandatory for privileged. | Verify on every request, not just session start; re-authenticate for step-up before sensitive actions. | Serverless / ephemeral functions cannot present an interactive MFA factor — substitute workload-identity-federation with sender-constrained short-lived tokens (DPoP/mTLS) and cryptographic device attestation. AI-agent pipelines: agent acts under its own short-lived scoped token, not the user's MFA-authenticated session. |
| **D3-CBAN** (Certificate-based Authentication) | Counters T1556 (Modify Authentication Process) by binding the authenticator to a cryptographic key; counters credential-theft for workload-to-workload flows via mTLS. | Layer 2 (Authentication) and Layer 4 (Session — sender-constrained tokens per RFC 9700). | Per-workload — each workload presents its own X.509 client cert or SPIFFE/SPIRE SVID; no shared certs across workloads. | Cert is presented on every request; revocation status (OCSP/CRL) checked or short-lived certs used (SPIFFE SVID default ≤ 1 hour). | Native fit for ephemeral / serverless: SPIFFE/SPIRE issues short-lived SVIDs at function startup; AWS IAM Roles Anywhere, GCP Workload Identity Federation, Azure Workload Identity federate to cloud IAM. AI-pipeline: agent-to-agent (A2A) flows MUST be cert-bound; bearer-token-only A2A is a finding. |
| **D3-CA** (Certificate Analysis) | Counters T1556 by detecting federation-trust-root tamper and rogue certificates (golden-SAML class). | Layer 3 (Federation). | N/A — control plane, not principal scope. | Continuously evaluate cert chain integrity, transparency-log presence, issuance anomalies; alert on out-of-policy issuance. | Applies wherever federation assertions are signed — SaaS-IdP federation, MCP server identity, agent-to-agent identity. Serverless: CT-log monitoring runs out-of-band (Sigstore Rekor / Google CT) — architecturally compatible. |
| **D3-EAL** (Executable Allowlisting) | Counters T1078 abuse via service-account / agent allowlisting: only allowlisted binaries / agent SDK versions can authenticate as a given service principal. | Layer 2 (Authentication — pre-condition) and Layer 5 (Step-up — agent attestation before privileged action). | Per-binary — only the specific MCP server binary / agent build hash is allowed to present the workload identity. | Verify binary identity on every authentication; reject on hash mismatch. | Ephemeral / serverless: bake allowlist into the function image at build-time (per the mcp-agent-trust ephemeral-context note — runtime fetch is architecturally impossible). AI-agent pipelines: allowlist the agent SDK build hash + MCP server hashes that are authorised to act under a given workload identity. |

---

## Hand-Off / Related Skills

After producing the identity assurance assessment output, chain into the following skills. Each entry is specific to a finding class this skill produces.

- **`mcp-agent-trust`** — direct agent-identity overlap. Every agent-principal finding in this skill's inventory (agent inherits user's OAuth session, no separate token, no scope minimisation) maps to an mcp-agent-trust trust-tier finding. Run mcp-agent-trust against the same fleet to get the artefact-level (signed manifest, tool allowlist, bearer auth) view that complements this skill's principal-level view.
- **`dlp-gap-analysis`** — identity-scoped DLP. The principal identity in the audit log is the join key for DLP egress attribution. Where this skill identifies inherited-agent principals (agent acts under user's token), DLP attribution is wrong-by-construction: tool-argument egress will be attributed to the human, not the agent. Run dlp-gap-analysis to verify tool-arg DLP classifiers and SDK-level prompt logging exist and to surface the attribution gap.
- **`defensive-countermeasure-mapping`** — full D3FEND layering across the identity stack. The four D3FEND techniques mapped above (D3-MFA, D3-CBAN, D3-CA, D3-EAL) are the identity-specific subset; the full defensive-countermeasure-mapping skill produces the cross-layer view (process isolation, network egress, etc.) that an identity-only mapping does not cover.
- **`supply-chain-integrity`** — signed identity artefacts. Federation assertion signing keys, OIDC discovery documents, JWKS endpoints, agent SDK binaries, and MCP server packages are all supply-chain artefacts. Run supply-chain-integrity to produce SLSA-level attestation, Sigstore signature verification, and in-toto provenance for the identity artefacts in this skill's federation-surface inventory.
- **`compliance-theater`** — paper-MFA theater. If the phishing-resistant coverage matrix in this skill's output shows < 100% phishing-resistant coverage for privileged users while the org's compliance attestations claim MFA-for-all, run compliance-theater for the full structured theater-vs-real-posture report tied to the specific audit reports (SOC 2, ISO, NIS2 conformity) being misrepresented.

For ephemeral / serverless / AI-pipeline contexts: interactive AAL3 authentication is architecturally impossible inside a serverless function or short-lived container. The scoped alternative is workload-identity-federation (SPIFFE/SPIRE, AWS IAM Roles Anywhere, GCP WIF, Azure Workload Identity) with sender-constrained short-lived tokens (DPoP per RFC 9449 or mTLS per RFC 8705), build-time agent-binary allowlisting baked into the function image, and per-invocation cryptographic device attestation where the platform supports it.
