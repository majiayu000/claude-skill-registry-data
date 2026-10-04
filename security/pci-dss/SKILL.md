---
description: Assess PCI DSS compliance — 12 requirements, SAQ determination, scope reduction
---

# PCI DSS Assessment

Assess Payment Card Industry Data Security Standard (PCI DSS) compliance for "$ARGUMENTS". Determine SAQ type, assess the 12 requirements, and identify scope reduction opportunities.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **SAQ type determination:**
   - Assess payment processing model and cardholder data flow
   - Determine applicable SAQ: A (card-not-present, fully outsourced), A-EP (e-commerce with partial outsourcing), B (imprint/standalone terminals), C (payment application connected to internet), D (all others), P2PE (validated P2PE merchants)
   - Evaluate merchant level (1-4) based on transaction volume
   - Document SAQ type and merchant level with rationale

3. **Scope assessment:**
   - Identify all systems that store, process, or transmit cardholder data (CHD)
   - Map the Cardholder Data Environment (CDE)
   - Identify connected-to and security-impacting systems
   - Assess network segmentation effectiveness
   - Document in-scope systems, applications, and network segments

4. **12 requirements assessment:**
   - **Req 1: Network security controls** — firewall/network security device configuration, CDE isolation
   - **Req 2: Secure configurations** — vendor default passwords removed, system hardening standards
   - **Req 3: Protect stored account data** — data retention policies, rendering PAN unreadable, key management
   - **Req 4: Encrypt transmission** — strong cryptography for CHD over open/public networks
   - **Req 5: Anti-malware** — malware protection on all systems, anti-malware mechanisms current
   - **Req 6: Secure development** — secure SDLC, patch management, web application security (WAF)
   - **Req 7: Restrict access** — need-to-know access control, access control systems
   - **Req 8: Identify users** — unique IDs, MFA for CDE access, strong authentication policies
   - **Req 9: Physical security** — physical access controls to CDE, visitor management, media security
   - **Req 10: Logging and monitoring** — audit trails, log review, time synchronization, SIEM
   - **Req 11: Security testing** — vulnerability scans (ASV quarterly), penetration testing, IDS/IPS, file integrity monitoring
   - **Req 12: Security policies** — information security policy, risk assessment, security awareness, incident response
   - Score each requirement: in place / in place with remediation / not in place / not applicable

5. **Scope reduction opportunities:**
   - Evaluate tokenization feasibility (replace CHD with tokens)
   - Assess Point-to-Point Encryption (P2PE) validated solutions
   - Review outsourcing options for payment processing
   - Evaluate network segmentation improvements
   - Identify quick wins for reducing in-scope systems

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/pci-dss.md` following the assessment template structure with:
   - **SAQ Determination** — SAQ type and merchant level with rationale
   - **Scope Definition** — CDE map, in-scope systems, segmentation assessment
   - **12 Requirements Assessment** — scoring per requirement with sub-requirement detail
   - **Scope Reduction Opportunities** — tokenization, P2PE, outsourcing options
   - **ASV and Penetration Testing Status** — current scan and test coverage
   - **Evidence Inventory** — existing evidence and evidence gaps
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The PCI DSS assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/pci-dss.md`. Present a summary to the user highlighting:
- SAQ type and merchant level determination
- Overall compliance score across 12 requirements
- Scope reduction opportunities with estimated effort savings
- Top 3 gaps requiring remediation
