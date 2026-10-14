---
name: iam-pro
description: Build identity and access management — lifecycle, privileged access, governance, and continuous access review.
category: security
---

## Overview

Identity is the primary security perimeter: nearly every modern attack involves compromised credentials or abused permissions. IAM is the discipline of ensuring the right identities have the right access at the right time — and nothing more. It spans human lifecycle (joiner/mover/leaver), non-human identities, privileged access, and governance.

This skill covers building IAM as a program: lifecycle automation, privileged access management, access reviews, and the metrics that show it working.

IAM is the operating system of enterprise security — every access decision in the organization flows through it. Programs fail when treated as IT plumbing; they succeed when treated as a product with users (employees want fast access), customers (auditors want evidence), and a roadmap (lifecycle automation, PAM, governance). Fund and staff it accordingly.

## When to use

- Standing up or maturing IAM: SSO, lifecycle automation, privileged access.
- Fixing audit findings on orphaned accounts, excessive privilege, or missing reviews.
- Reducing standing privilege (the #1 identity risk).
- Governing non-human identities: service accounts, API keys, workload identities.

## Core concepts

- **Lifecycle (JML):** joiner (provisioning from HR source of truth), mover (access changes with role changes — the most neglected), leaver (deprovisioning within hours, not weeks). Automate from the HR system; manual processes rot.
- **Least privilege, continuously:** grant minimum necessary, default-deny, and re-validate. Privilege accumulates like plaque — reviews are the cleaning.
- **Privileged Access Management (PAM):** vault privileged credentials, require checkout with approval and session recording, eliminate standing admin rights via just-in-time elevation.
- **Non-human identities:** service accounts, API keys, OAuth apps, workload identities — inventory them like humans, give them owners, rotate them, and apply least privilege. They are often the weakest link.
- **Access reviews (certification):** periodic attestation by managers/system owners that access is still needed. Make them meaningful: show last-used data, pre-flag anomalies, keep scope tight.
- **Segregation of duties (SoD):** conflicting permissions (e.g., create vendor + approve payment) must not sit with one identity. Define SoD rules and enforce at provisioning time.

- **Access request workflows.** Self-service requests with manager approval and automatic provisioning beat ticket queues — speed of legitimate access is a security feature (it kills shadow IT).
- **Privileged session management.** Recording and proxying admin sessions gives you both deterrence and forensic evidence for the highest-risk activity in the estate.
- **Identity threat detection.** Impossible travel, token replay, and privilege-escalation patterns in identity logs deserve dedicated detections — the identity plane is now the primary battleground.

## Practical workflow

1. **Establish the identity source:** HR system as the authoritative source for humans; a registry (CMDB/IdP) for non-human identities with mandatory owners.
2. **Automate JML:** provisioning on hire, role-based access changes on transfer (remove old, grant new — movers are where privilege accumulates), deprovisioning within 24 hours of termination, including SaaS and shared mailboxes.
3. **Deploy PAM:** vault all privileged credentials; just-in-time elevation instead of standing admin; session monitoring for the most sensitive systems; break-glass with sealed, audited procedures.
4. **Rationalize access:** role mining — build roles from actual usage patterns, not org charts; remove unused entitlements (last-used data is your best friend); kill orphaned and dormant accounts.
5. **Run meaningful reviews:** quarterly for privileged/sensitive access, annual for standard; arm reviewers with usage data and anomaly flags; track remediation of revoked access to completion.
6. **Measure:** time-to-provision, time-to-deprovision, % privileged access via JIT, orphaned-account count, review completion and revocation rates, SoD violations. Report trends, not snapshots.

### IAM health checklist

- [ ] HR-driven automated provisioning/deprovisioning live
- [ ] Mover process removes old access (verified by sampling)
- [ ] Standing privileged accounts minimized; JIT elevation in use
- [ ] Non-human identity inventory with owners and rotation
- [ ] Access reviews run on schedule with usage data; revocations completed
- [ ] SoD rules defined and enforced at provisioning
- [ ] Dormant/orphaned account cleanup automated

### Sustaining the practice

- Publish IAM metrics monthly to engineering and business leadership
- Re-certify privileged access quarterly without exception
- Hunt for orphaned and dormant accounts continuously, not just at review time
- Test the leaver process with spot audits — sample terminations and verify deprovisioning

### Metrics that prove it works

- Time to deprovision after termination (target: hours)
- Orphaned and dormant account counts, trended down
- % of privileged access via just-in-time elevation
- Access-review completion and revocation-follow-through rates

## Common pitfalls

- **Manual JML.** Spreadsheets and tickets cannot keep up with hiring velocity. Automate from HR or accept the orphan accounts.
- **Ignoring movers.** Joiners get attention, leavers get compliance pressure, movers quietly accumulate every permission from every past role. Fix movers.
- **Standing admin everywhere.** "Everyone in IT is a domain admin" is the fastest path to total compromise. JIT elevation exists for a reason.
- **Non-human identity sprawl.** Service accounts created in 2019 with domain-admin-equivalent rights and no owner. Inventory them ruthlessly.
- **Rubber-stamp reviews.** Certifying 500 entitlements in 10 minutes helps nobody. Scope tightly, provide usage data, sample-verify.
- **SoD as an afterthought.** Discovering toxic permission combinations during fraud investigation is too late. Enforce at grant time.
- **SaaS sprawl outside the IdP.** Shadow SaaS with standalone credentials bypasses every IAM control. Discover, federate, or shut down.
- **Contractor lifecycle gaps.** Contractors with no HR record keep access indefinitely. Every non-employee needs an owner and an expiry.
- **Treating IAM as a one-time project.** 'We deployed SSO' is the beginning. Lifecycle, governance, and PAM are ongoing operations that need permanent ownership.
- **Over-centralizing without delegation.** Business units need controlled self-service for their apps, or they will route around central IAM entirely.
