---
description: Assess ISO 27017 cloud security controls
---

# ISO 27017 Assessment

Assess ISO/IEC 27017:2015 cloud security controls for "$ARGUMENTS". Identify the cloud service model, establish shared responsibility boundaries, and evaluate cloud-specific security controls that extend the ISO 27001 baseline.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **Cloud service model identification:**
   - Determine cloud service model(s) in use: IaaS, PaaS, SaaS, or hybrid
   - Identify cloud service provider(s) and their certifications
   - Map cloud deployment models: public, private, hybrid, multi-cloud

3. **Shared responsibility boundaries:**
   - Define responsibility split between cloud service provider (CSP) and cloud service customer (CSC)
   - Map each ISO 27001 Annex A control to responsible party (CSP, CSC, or shared)
   - Document CSP compliance attestations and certifications relied upon
   - Identify controls where responsibility is ambiguous or undocumented

4. **Cloud-specific controls assessment:**
   - **Virtual machine hardening** — assess VM image management, secure configuration, hardening baselines
   - **Cloud service monitoring** — assess monitoring of cloud resources, tenant activity logging, anomaly detection
   - **Cloud network security** — assess virtual network segmentation, security groups, cloud firewalls, traffic encryption
   - **Multi-tenant isolation** — assess tenant separation, data isolation, compute isolation, resource boundaries
   - **Data location** — assess data residency awareness, geographic restrictions, data sovereignty compliance
   - **Cloud backup** — assess cloud-native backup strategies, cross-region replication, recovery testing
   - **Secure development in cloud** — assess cloud-native development practices, container security, serverless security, CI/CD pipeline security
   - Score each control: Implemented / Partially Implemented / Not Implemented / CSP Managed

5. **ISO 27001 base control extensions:**
   - For each ISO 27001 Annex A control, assess cloud-specific extensions defined in ISO 27017
   - Identify controls requiring additional cloud-specific implementation beyond ISO 27001 baseline
   - Document where ISO 27001 controls are sufficient vs. where cloud extensions are needed

6. **CSP compliance reliance:**
   - Assess which controls are fully delegated to CSP
   - Verify CSP certifications and audit reports (SOC 2, ISO 27001, ISO 27017)
   - Identify risks from CSP reliance (single provider dependency, audit gaps)

7. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27017.md` following the assessment template structure with:
   - **Cloud Service Model** — service and deployment model identification
   - **Shared Responsibility Map** — control ownership by CSP/CSC/shared
   - **Cloud-Specific Controls Assessment** — all cloud controls scored
   - **ISO 27001 Extensions** — additional cloud requirements beyond base controls
   - **CSP Compliance Reliance** — provider certifications and dependency risks
   - **Overall Compliance Score** — aggregate score with heatmap
   - **Remediation Priorities** — ranked list of gaps to address

## Output

The ISO 27017 assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/iso27017.md`. Present a summary to the user highlighting:
- Cloud service model and provider(s) assessed
- Shared responsibility clarity score
- Top 3 cloud-specific control gaps
- CSP reliance risks
