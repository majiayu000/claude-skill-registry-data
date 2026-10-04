---
name: email-security-anti-phishing
version: "1.0.0"
description: Email security + anti-phishing for mid-2026 — SPF/DKIM/DMARC/BIMI/ARC/MTA-STS/TLSRPT, AI-augmented phishing (vishing, deepfake video, hyperpersonalized email), Business Email Compromise, secure email gateways
triggers:
  - email security
  - anti-phishing
  - phishing
  - spear phishing
  - bec
  - business email compromise
  - dmarc
  - dkim
  - spf
  - bimi
  - arc
  - mta-sts
  - tlsrpt
  - vishing
  - deepfake phishing
  - ai phishing
  - secure email gateway
data_deps:
  - atlas-ttps.json
  - attack-techniques.json
  - d3fend-catalog.json
  - dlp-controls.json
  - framework-control-gaps.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1566
  - T1566.001
  - T1566.002
  - T1566.003
  - T1078
framework_gaps:
  - NIST-800-53-SI-3
  - ISO-27001-2022-A.8.16
  - SOC2-CC7-anomaly-detection
  - NIS2-Art21-incident-handling
  - UK-CAF-C1
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-7489
  - RFC-6376
  - RFC-7208
  - RFC-8616
  - RFC-8461
cwe_refs: []
d3fend_refs:
  - D3-NTA
  - D3-CSPP
  - D3-IOPR
  - D3-MFA
last_threat_review: "2026-05-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief email-security-anti-phishing` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Email Security and Anti-Phishing Assessment

## Threat Context (mid-2026)

Phishing remained the #1 initial-access vector through 2025 (Verizon DBIR 2025) and into 2026. The structural shift between 2024 and 2026 is **AI-augmentation of the phishing kill-chain** — content generation, voice synthesis, and live deepfake video have all collapsed from "demonstrated in research" to "deployed against treasury, IT-helpdesk, and executive offices."

**Voice cloning drives vishing at scale.** Roughly three seconds of public audio (an earnings call clip, a conference panel, a podcast appearance) is now sufficient to clone an executive's voice with commodity tooling. Vishing campaigns aimed at IT-helpdesk identity-reset flows and at treasury wire-approval gates have become the dominant social-engineering vector reported in FBI IC3 Internet Crime Report 2024 and continued through the 2025 report period. Helpdesk "I forgot my MFA, please re-enroll my passkey" calls are the canonical exploit path against orgs that mandated FIDO2 but didn't harden the recovery channel.

**Deepfake video conferencing is no longer theoretical.** The Arup Hong Kong incident (January 2024, ~USD 25M) — where a finance worker authorized a wire after a video call with what appeared to be the CFO and other colleagues, all synthesized — is the watershed reference case. Real-time deepfake stacks (DeepFaceLab plus live-render variants) now run on a single consumer GPU. "I saw them on camera, so it's them" is dead as an authentication assertion.

**Hyperpersonalized email phishing bypasses content filters.** Attackers scrape LinkedIn, GitHub, conference programs, and public corporate filings, feed the corpus into an LLM, and produce target-specific lures that match the recipient's writing style, current projects, and known relationships. These messages do not trip keyword-based filters and they often do not contain the canonical "phishing tells" (urgency, grammar errors, generic salutations) that older awareness training drilled on. Microsoft, Google, Anthropic, and OpenAI all operate email-channel abuse-detection programs against the LLM API surface; coverage is uneven and jailbreak-augmented "phishing-as-a-service" intermediaries route around it.

**Business Email Compromise losses continued growing through 2025.** FBI IC3 2024 and 2025 reports place BEC at multi-billion-USD annual loss globally, with the wire-redirection and vendor-invoice-fraud subclasses dominant. The 2026 reality is that BEC is no longer "compromised mailbox sends a wire request" — it is increasingly "spoofed-or-look-alike domain plus deepfake voice/video confirmation channel" so that out-of-band verification by phone *fails open* unless the callback number is a pre-registered known-good.

**Defense ecosystem snapshot.** SPF (RFC 7208), DKIM (RFC 6376), and DMARC (RFC 7489) adoption is effectively universal among Fortune 500 sender domains, but **enforcement** (`p=reject` vs `p=none`) lags — only roughly 60% of large enterprise domains are at `p=reject` by mid-2026, with the rest stuck in monitoring mode for fear of breaking legitimate forwarders. BIMI (AuthIndicators Working Group draft, with IETF mailing-list discussion ongoing as of mid-2026) for visual brand verification is deployed at Gmail, Yahoo Mail, and Apple Mail, but requires DMARC `p=quarantine` or `p=reject` to take effect — so it doubles as enforcement-status signaling. ARC (RFC 8617) is the forwarder-authentication answer to the DMARC-vs-mailing-list problem and is maturing across major providers. MTA-STS (RFC 8461) and TLSRPT (RFC 8460) close the in-transit TLS-downgrade gap that opportunistic STARTTLS leaves open. The cloud email duopoly — Microsoft 365 Exchange Online and Google Workspace Gmail — is the canonical inbox environment most enterprises operate in; on-prem Exchange remains in regulated and air-gapped enclaves and gets an explicit exception path below.

**Phishing-resistant authentication.** FIDO2 / WebAuthn synced passkeys are the only widely deployed authenticator class that survives AiTM proxy phishing (evilginx-class), Tycoon-2FA-style session-token relay, and push-notification fatigue attacks. TOTP, SMS, and push-MFA are all bypassable by 2026 phishing-kit ecosystems. Caffeine and Tycoon 2FA continue to evolve; observed 2025 telemetry shows passkey-relay attempts emerging against poorly configured WebAuthn relying-party verification.

---

## Framework Lag Declaration

| Framework | Control | Why It Fails in mid-2026 |
|---|---|---|
| NIST 800-53 | SI-3 (Malicious Code Protection) | SI-3 is method-neutral and assumes signature/heuristic detection at email and endpoint boundaries. It does not operationalize **AI-generated email** (no malware payload, no link in some BEC variants), **voice-cloned vishing** (off the email channel entirely but inside the same social-engineering kill-chain), or **deepfake video CFO calls**. Compliance with SI-3 says nothing about whether a `p=reject` DMARC policy is published or whether wire-approval flows have out-of-band callback. Tracked as `NIST-800-53-SI-3`. |
| ISO/IEC 27001:2022 | A.8.16 (Monitoring Activities) | A.8.16 requires monitoring of networks, systems, and applications for anomalous behavior. It does not specify email-channel anomaly detection for AI-class threats — no requirement for hyperpersonalized-content detection, no requirement for voice-channel anomaly monitoring, no requirement for video-conference deepfake liveness checks. Tracked as `ISO-27001-2022-A.8.16`. |
| SOC 2 | CC7.3 (anomaly detection) | CC7 is process-focused: "the entity uses detection and monitoring procedures." A control owner can pass CC7.3 audit on the strength of a generic SIEM rule set with zero specific coverage for BEC, deepfake-assisted wire fraud, or vishing-driven helpdesk identity-reset abuse. Tracked as `SOC2-CC7-anomaly-detection`. |
| PCI DSS 4.0 | §5.4.1 (anti-phishing mechanisms) | 5.4.1 mentions email security mechanisms but is not consistently enforced for hospitality/retail merchants outside Level 1; assessor interpretation varies, and the standard does not require DMARC `p=reject`. |
| EU GDPR | Art. 32 (security of processing) | Email is in scope as a processing channel; "appropriate technical measures" is non-prescriptive on DMARC enforcement, passkeys, or deepfake-aware verification. |
| EU NIS2 | Art. 21 (cybersecurity risk-management measures) | NIS2 brings email-as-essential-service into scope for essential and important entities with enforceable management liability, but the specific anti-phishing operational requirements are left to national implementation. |
| UK NCSC | Mail Check / GOV.UK DMARC mandate | Mandatory for UK central government domains; `p=reject` is the published target. Private-sector orgs under UK CAF (Cyber Assessment Framework) inherit only general principles. |
| AU ASD | Essential 8, Mitigation 4 (Configure Microsoft Office macro settings) and broader application-control / user-app-hardening guidance | Email content filtering and macro neutralization are covered, but Essential 8 maturity levels do not pin DMARC enforcement or phishing-resistant MFA explicitly at ML1; FIDO2 mandate sits in ASD ISM controls separately. |
| JP NISC / IPA | Anti-phishing guidance and J-CSIP | DMARC adoption pushed by JPCERT/CC; enforcement and BEC playbook depth varies. |
| IL INCD | National anti-phishing baseline and CERT-IL guidance | Strong on takedown coordination, lighter on operational deepfake-aware procedure for executive comms. |
| SG CSA | Cybersecurity Code of Practice and anti-phishing advisories | Covers email gateway, awareness training; deepfake-specific procedure not mandated. |
| IN CERT-In | Phishing guidance and 6-hour incident reporting rule | Reporting requirement is firm; control specifications lag. |
| NYDFS | 23 NYCRR 500.14 (training and monitoring) | Annual phishing-aware training required; does not specify FIDO2, DMARC `p=reject`, or deepfake-aware procedures. |

This analysis spans EU + UK + AU + JP + IL + SG + IN + NYDFS alongside NIST and ISO, because a US-only email-security posture is incomplete for any multi-jurisdiction sender. Each framework-gap ID in `framework_gaps` (`NIST-800-53-SI-3`, `ISO-27001-2022-A.8.16`, `SOC2-CC7-anomaly-detection`, `NIS2-Art21-incident-handling`, `UK-CAF-C1`, `AU-Essential-8-App-Hardening`) resolves against `data/framework-control-gaps.json` — operators producing a per-control evidence pack should pull the canonical lag rationale from that catalog rather than transcribing the table above.

---

## TTP Mapping

| TTP | Name | Gap Flag |
|---|---|---|
| T1566 | Phishing (parent) | Framework controls treat as "awareness training + filter" — does not address AI-generated content evasion or out-of-band deepfake confirmation channels. |
| T1566.001 | Spearphishing Attachment | SI-3 / A.8.16 cover malware payloads; do not cover macro-free document delivery via DOCX/PDF that uses LLM-generated lure text plus benign-looking links to credential-harvest pages. |
| T1566.002 | Spearphishing Link | URL rewriting and sandbox detonation are gateway-side; AiTM proxy phishing (evilginx, Tycoon 2FA) bypasses session-token-based MFA. Mitigation requires phishing-resistant authenticator (D3-MFA mapped to FIDO2/WebAuthn), not gateway filtering alone. |
| T1566.003 | Spearphishing via Service | LinkedIn DMs, Teams chat, Slack DMs, SMS, WhatsApp — all email-adjacent channels that DMARC/DKIM/SPF do not protect. Voice-cloned vishing and deepfake video calls land here too. |
| T1078 | Valid Accounts | Post-phish credential use. The success metric for the program is "no T1078 follow-on," because every successful T1566 that reaches `p=reject` and FIDO2 still has to traverse credential use. |

Note: `atlas_refs` is intentionally empty — these are ATT&CK Enterprise TTPs against human/email channels, not ATLAS AI-system TTPs. The AI-augmentation angle is handled via cross-reference to `ai-attack-surface`. The ATT&CK technique IDs above (`T1566`, `T1566.001`, `T1566.002`, `T1566.003`, `T1078`) resolve against `data/attack-techniques.json`; when an investigation crosses into AI-mediated phishing (LLM-generated lures, deepfake video confirmation, voice cloning), cross-reference `data/atlas-ttps.json` for `AML.T0051` (LLM Prompt Injection — relevant when phishing payloads target the LLM-as-classifier instead of the human), `AML.T0024` (Exfiltration via Cyber Means — applicable where compromised mailbox sessions egress data via the message channel itself), and `AML.T0016` (Develop Capabilities — adversary use of public LLM APIs to author hyperpersonalized lures).

---

## Exploit Availability Matrix

| Capability | Availability | Notes |
|---|---|---|
| Phishing-kit-as-a-service (Caffeine, Tycoon 2FA, EvilProxy) | Live, commodity | Subscription model. Tycoon 2FA observed in 2025 attempting passkey-relay against weak relying-party verification. |
| BEC-as-a-service | Live | Wire-redirection and vendor-invoice-fraud sub-services advertised in underground forums. |
| Voice cloning | Commodity | ElevenLabs and similar have anti-abuse, but underground forks and self-hosted open-weights models remove the guardrails. ~3 seconds of audio suffices. |
| Real-time deepfake video | Live | DeepFaceLab plus real-time variants; single-GPU; demonstrated at scale by the Arup 2024 incident. |
| LLM-generated hyperpersonalized email | Live | All major LLM providers run abuse-detection on the email-generation surface; jailbreak-augmented intermediaries route around it. |
| AI-discovered novel evasion | Active | AI acceleration of attacker tooling is current operational reality, not future-watch. |
| Phishing-resistant defense | Available now | FIDO2 / WebAuthn synced passkeys = the only authenticator class that survives 2026 phishing kits. CISA Phishing-Resistant MFA guidance + NIST 800-63B rev 4 codify this. |
| DMARC `p=reject` adoption | Universal at large senders, ~60% enforced | Adoption metric is misleading; enforcement metric is the real KPI. |
| ARC for forwarders | Maturing across major providers | Closes the mailing-list-breaks-DMARC objection that kept many domains at `p=none`. |
| MTA-STS / TLSRPT | Available | Closes opportunistic-STARTTLS downgrade. |

No CVE entries are claimed for this skill — email-channel social engineering is TTP-driven, not CVE-driven. The CVE catalog dependency is declarative only (no new catalog entries required for this skill to ship).

---

## Analysis Procedure

The procedure threads three foundational principles:

**Defense in depth** — inbound: DMARC enforcement (`p=reject`) + ARC for forwarders + secure email gateway (Proofpoint, Mimecast, Microsoft Defender for Office 365, Google Workspace Gmail Advanced Protection) + URL rewriting + sandbox detonation + DLP egress. Outbound: DKIM signing on all sending sources + BIMI registration + SPF maintenance with SPF-record-flattening discipline (10-DNS-lookup ceiling). User layer: phishing-resistant MFA (passkeys), simulated phishing program including AI-augmented lures, deepfake-aware policies for video and voice. Vendor layer: fourth-party email risk — supplier DMARC posture monitored as a vendor-risk attribute. Incident layer: BEC IR playbook with explicit hand-off to `incident-response-playbook`.

**Least privilege** — financial-action authorization scoped per principal, multi-party-approved for wire changes, with out-of-band callback to a pre-registered known-good number for any vendor banking-detail change. Executive-impersonation channels (CEO/CFO direct comms) routed through monitored aliases. Help-desk identity-verification scripts require multi-factor evidence (employee ID + manager callback + pre-registered recovery contact) before any MFA reset; "voice on the phone matches the org chart" is not sufficient evidence.

**Zero trust** — every email is hostile until verified (DMARC pass + sender reputation + intent classification at gateway). Every video call requesting a financial action requires a live verification challenge (callback to a known number; pre-arranged challenge phrase; in-person or known-good-channel confirmation for high-value transactions). Every voice call from a "known" executive requesting an out-of-policy action gets multi-channel verification before action.

**Cloud-email canonical, on-prem exception:** default scoping assumes Microsoft 365 Exchange Online or Google Workspace Gmail. On-prem Exchange (legacy, regulated enclave, air-gapped) gets an explicit exception path noting which controls (cloud-native sandbox detonation, Microsoft Defender XDR signals, Google Workspace Security Sandbox) have on-prem equivalents and which require compensating controls.

Email-authentication RFCs cited throughout the procedure (`RFC-7489` DMARC, `RFC-6376` DKIM, `RFC-7208` SPF, `RFC-8616` BIMI/AuthIndicators DNS encoding, `RFC-8461` MTA-STS, `RFC-8617` ARC, `RFC-8460` TLSRPT) resolve against `data/rfc-references.json`. The DLP exfil-channel mappings invoked by the gateway-and-egress sub-procedures (`DLP-CHAN-EMAIL-OUT` for outbound message exfil, `DLP-CHAN-LLM-PROMPT` for LLM-prompt-as-egress when users paste mailbox content into AI assistants, `DLP-ENFORCE-BLOCK` for hard-block enforcement on confirmed PHI/PCI patterns) resolve against `data/dlp-controls.json` — these are the canonical IDs to cite when handing off to `dlp-gap-analysis`.

**Ten-step assessment:**

1. **Email authentication posture audit.** For each owned sending domain: pull SPF record, count DNS lookups (≤10), check for `+all` or `?all` (fail open), and check for SPF-flattening or macro-misuse. Pull DKIM selectors and verify key length ≥2048-bit, current rotation cadence. Pull DMARC record and capture policy (`p=`), subdomain policy (`sp=`), `pct=`, `rua=`/`ruf=` aggregate-report destinations, and alignment modes. Pull BIMI record and check VMC/CMC presence. Pull ARC seal status from inbound flow samples. Pull MTA-STS policy and TLSRPT destination.
2. **DMARC enforcement migration.** Plot every owned domain on the `p=none` → `p=quarantine` → `p=reject` axis. For domains stuck at `p=none` >12 months, classify the blocker (legitimate forwarders unaccounted for? marketing-platform misconfiguration? subdomain sprawl?). Build the 90-day migration plan to `p=reject` with `pct=` stepping (25 → 50 → 100). Cross-check parked / non-sending domains for a hardcoded reject record (`v=DMARC1; p=reject; sp=reject;`).
3. **Gateway plus sandbox deployment review.** Inventory the secure email gateway in use, confirm URL rewriting and click-time URL re-evaluation, confirm attachment sandbox detonation depth (macro, JS, LNK, ISO, container formats), confirm impersonation-protection rules (lookalike domain detection, display-name spoofing detection, internal-from-external detection). Verify the gateway is integrated with the identity provider for risk-based session signals.
4. **FIDO2 passkey rollout.** Measure passkey enrollment percentage across the workforce, with separate metrics for privileged users (admins, finance, executives, helpdesk) where 100% is the operational target. Confirm relying-party verification configuration resists passkey-relay attempts. Confirm recovery flow does not collapse to a phishable factor (SMS reset, voice-bypass of FIDO2 enforcement, helpdesk re-enrollment without out-of-band verification). Hand off detailed AAL3 work to `identity-assurance`.
5. **Anti-phishing training program.** Assess simulation cadence (monthly minimum for high-risk roles), simulation diversity (must include AI-generated hyperpersonalized lures, vishing simulations against helpdesk and treasury, deepfake-aware tabletop for executive admin staff), click-rate and report-rate trend, and remedial-training pathway for repeat clickers. Reject vendor "anti-phishing training" programs whose simulation library is keyword-driven 2018-era templates.
6. **BEC playbook.** Document the out-of-band verification protocol for: vendor banking-detail changes, executive wire requests, payroll-redirection requests, mergers-and-acquisition correspondence. Require pre-registered callback numbers (not "the number in the email signature"), multi-party approval thresholds, and a 24-hour cool-off on first-time vendor changes >USD 10K. Tabletop the playbook at least annually with finance, treasury, and IR.
7. **Deepfake-aware policies.** For video conferences requesting financial actions or sensitive data: require a pre-arranged challenge phrase or a callback to a known number before action. For voice calls from executives requesting out-of-policy actions: require multi-channel confirmation (Slack/Teams DM to the executive's known account, plus a callback). Train executive assistants and helpdesk specifically — these are the targeted roles.
8. **Vendor email risk monitoring.** Add supplier DMARC posture and breach history to the vendor-risk register. Suppliers at `p=none` are an elevated BEC vector against your finance team via supplier-impersonation. Suppliers with recent mailbox-takeover incidents trigger a temporary out-of-band verification mandate.
9. **Incident integration.** Define the hand-off to `incident-response-playbook` for: confirmed BEC, suspected wire-fraud-in-flight (with timeline-critical "Financial Fraud Kill Chain" steps — bank notification, Financial Crimes Enforcement Network/IC3 reporting per FBI guidance, recovery attempts), mailbox-takeover events, and deepfake-confirmed social-engineering attempts.
10. **Continuous DMARC report monitoring.** Stand up a DMARC aggregate (RUA) report consumer (DMARC.org free dashboard, dmarcian, Valimail, Red Sift, or self-hosted). Alert on unauthorized sending sources, alignment failures from owned IPs, and policy-rejection volume changes. The reports are how you learn that a marketing platform was spoofing your domain for the last 90 days.

---

## Output Format

The skill produces a structured assessment with these sections:

1. **DMARC enforcement scorecard** — table of all owned domains × `{SPF, DKIM, DMARC policy, sp=, pct=, RUA destination, BIMI, ARC verification, MTA-STS, TLSRPT}`; aggregate score = (# domains at `p=reject` with `pct=100`) / (total sending domains).
2. **Email-auth coverage matrix** — per-protocol deployment status (SPF / DKIM / DMARC / BIMI / ARC / MTA-STS / TLSRPT) with gap flags.
3. **Passkey rollout percentage** — overall and per-role-class (executive, finance, IT-admin, helpdesk, general workforce), with target = 100% for privileged-user classes.
4. **Phishing simulation results trend** — 12-month click-rate and report-rate by role-class, with explicit AI-generated-lure cohort separated from template-lure cohort.
5. **BEC playbook coverage** — boolean coverage matrix for {vendor banking change, executive wire, payroll redirect, M&A correspondence} × {out-of-band callback registered, multi-party approval, cool-off period, tabletop last 12 months}.
6. **Deepfake-aware policy coverage** — executive comms, finance authorization, helpdesk identity reset — each with policy presence, training delivered, tabletop tested.
7. **Vendor email risk register** — top-N suppliers by spend × DMARC posture × breach history × elevated-verification flag.
8. **Compliance theater verdicts** (see next section) for each of the four theater tests.
9. **RWEP-prioritized remediation queue** — recommendations ranked by exploit-priority, not framework-deadline.
10. **Hand-off triggers** — explicit pointers to `identity-assurance`, `dlp-gap-analysis`, `incident-response-playbook`, `compliance-theater`, `sector-financial`, `ai-attack-surface` where the assessment surfaces work belonging to those skills.

---

## Compliance Theater Check

Four concrete tests distinguish paper compliance from real anti-phishing posture:

1. **"What's your DMARC policy on your primary sending domain?"** If the answer is `p=none` and the policy was first published more than 12 months ago, the program is in permanent monitor-mode — theater. The DMARC standard treats `p=none` as a deployment phase, not a destination. Document why enforcement has stalled and what specific forwarder/marketing-platform issue is blocking migration.
2. **"What percentage of users are on phishing-resistant passkeys?"** If the answer is "we have MFA enabled for everyone" without specifying FIDO2 / WebAuthn / passkey, the org is shipping AiTM-bypassable factors and calling it MFA. TOTP / SMS / push-MFA are phishing-vulnerable in 2026 phishing-kit ecosystems. The right answer specifies passkey enrollment percentage with privileged-role breakouts and target = 100% for finance, helpdesk, admins, and executives.
3. **"Show me your last BEC incident playbook tabletop."** If the answer is "we'll handle it ad-hoc" or "we have a generic IR plan that covers email incidents," the org has FBI-IC3-billion-dollar-class exposure. The playbook must name the bank-notification contact, the IC3 reporting workflow, the wire-recall escalation path, and the threshold for declaring "in-flight fraud" versus "post-incident recovery."
4. **"What's your deepfake-aware procedure for a video call from the CFO requesting a wire?"** If the answer is "we trust who we see on camera," the org is in 2024 Arup-class exposure (~USD 25M reference incident). The procedure must include a callback to a pre-registered number, a challenge phrase or out-of-band confirmation, and a multi-party approval threshold that no single deepfake interaction can clear.

---

## Defensive Countermeasure Mapping

This section maps offensive findings to MITRE D3FEND defensive techniques.

| D3FEND ID | Defense | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-NTA (Network Traffic Analysis) | Secure email gateway flow analysis — inbound SMTP/IMAP/MAPI traffic, attachment metadata, link reputation lookups, sender-IP DMARC alignment | Perimeter (gateway) and egress | Per-mailbox scoping for DLP and quarantine actions | Treat every inbound message as untrusted until DMARC pass + reputation + intent classification clears it | Applies to LLM-driven email-generation API egress as well — flag anomalous outbound volume from compromised service accounts that gained mailbox-send scopes |
| D3-CSPP (Client-server Payload Profiling) | Email content payload profiling at the gateway — attachment type, macro presence, embedded URL targeting, header anomalies, conversation-thread coherence checks | Pre-delivery and pre-render | Per-message risk scoring; quarantine vs. deliver with banner vs. deliver clean | Verify content properties match claimed sender's pattern; flag stylometric drift consistent with LLM-generated hyperpersonalized lures | Stylometric drift is the canonical detection signal for LLM-generated phishing |
| D3-IOPR (Inbound Operation Restriction) | Restrict inbound operations the message can perform — URL rewriting, click-time re-evaluation, macro neutralization, container-format unpacking, sandbox detonation | Pre-delivery and at click-time | Per-user click policy (privileged users on stricter detonation tier) | No payload is allowed to act on the user's behalf without the gateway's verification | LLM-generated email detection sits here at the gateway-classification layer |
| D3-MFA (Multi-factor Authentication) | Phishing-resistant authenticator class — FIDO2 / WebAuthn synced passkeys with proper relying-party verification | User authentication layer | Mandatory at 100% for privileged role classes; recovery flow hardened against helpdesk-vishing | Every authentication is verified by possession of the bound authenticator; session tokens are not transferable across origin | Canonical defense — passkeys remove the credential-disclosure win condition that AI-augmented phishing optimizes for |

The D3FEND technique IDs above (`D3-NTA`, `D3-CSPP`, `D3-IOPR`, `D3-MFA`) resolve against `data/d3fend-catalog.json`. Operators producing a defence-in-depth map for an email-security finding should chain: offensive technique (`T1566.*` from `data/attack-techniques.json`, plus AI-augmentation context from `data/atlas-ttps.json`) → missing control (entry in `data/framework-control-gaps.json`) → defensive technique (entry in `data/d3fend-catalog.json`) → DLP enforcement channel (`DLP-CHAN-EMAIL-OUT` / `DLP-CHAN-LLM-PROMPT` from `data/dlp-controls.json`) → wire-level RFC anchor (entry in `data/rfc-references.json`). This is the cross-walk pattern the seven-phase playbook expects when packaging anti-phishing evidence for an auditor or jurisdiction notification.

---

## Hand-Off / Related Skills

| If the assessment surfaces… | Hand off to |
|---|---|
| Passkey rollout, AAL3 design, recovery-flow hardening, agent-as-principal authentication | `identity-assurance` |
| Email egress as a DLP channel, attachment exfil, LLM-prompt egress over mail | `dlp-gap-analysis` |
| Confirmed BEC, in-flight wire fraud, mailbox takeover, deepfake-confirmed incident | `incident-response-playbook` |
| DMARC paper-vs-enforcement, "we have MFA" claims, generic IR plan claims | `compliance-theater` |
| Bank, payment-services, treasury context — BEC is the canonical financial-sector loss class | `sector-financial` |
| AI-augmented phishing as a class — voice cloning, deepfake video, LLM-generated lures, jailbreak-augmented phishing-as-a-service | `ai-attack-surface` |

Forward watch: IETF draft work on DKIM2 and on stronger ARC sealing; deepfake liveness-detection standardization in video-conferencing platforms (Zoom, Teams, Webex); FIDO Alliance updates to recovery-flow guidance; new IC3 and DBIR reports as they publish; Microsoft / Google / Anthropic / OpenAI abuse-program transparency reports.
