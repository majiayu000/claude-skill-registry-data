---
name: drata
description: "Expert agent for Drata compliance automation. Covers Autopilot, 1,200+ automated tests, 170+ integrations, continuous control monitoring, personnel management, asset inventory, policy center, risk management, and trust center for SOC 2, ISO 27001, HIPAA, PCI DSS, and GDPR. WHEN: \"Drata\", \"Drata autopilot\", \"Drata SOC 2\", \"Drata evidence\", \"Drata personnel\", \"Drata asset inventory\", \"Drata policy center\", \"Drata integrations\"."
license: MIT
---

# Drata

This skill covers Drata's compliance automation platform, covering Autopilot, automated control testing, personnel management, asset inventory, policy management, vendor risk, and multi-framework compliance.

## How to Approach Tasks

1. **Identify the use case** — compliance framework, Autopilot configuration, personnel tracking, asset inventory, or audit preparation
2. **Classify the request:**
   - **Framework setup** — Guide through framework activation and control customization
   - **Autopilot** — Apply automated evidence and remediation guidance
   - **Integrations** — Apply integration setup and troubleshooting guidance
   - **Personnel management** — Background checks, training, access reviews
   - **Asset inventory** — Auto-discovery, device management, classification
   - **Audit prep** — Evidence packaging, auditor access, gap closure
3. **Load context** — Read `references/architecture.md` for platform architecture details

## Platform Overview

Drata is a compliance automation platform with deep emphasis on:
- **Autopilot**: automated evidence collection with some auto-remediation capabilities
- **1,200+ automated tests** across cloud infrastructure, SaaS tools, endpoints, and code repos
- **Personnel management**: tightly integrated employee tracking (training, BG checks, access reviews, equipment)
- **Asset inventory**: auto-discovery of cloud assets and devices with compliance tracking

## Supported Frameworks

| Framework | Support Level |
|---|---|
| SOC 2 Type I & II | Full automation + auditor portal |
| ISO 27001:2022 | Full — ISMS, SoA, risk register |
| HIPAA | Full — Security Rule and Privacy Rule coverage |
| PCI DSS v4.0 | Full — SAQ types and full assessment |
| GDPR | Full — privacy controls and data processing records |
| CCPA/CPRA | Supported |
| NIST CSF 2.0 | Supported |
| NIST SP 800-53 | Supported |
| FedRAMP | Supported |
| ISO 42001 | Supported |
| SOC 1 | Supported |
| Custom frameworks | Yes — control library builder |

## Integrations

### Integration Coverage (170+)

Covers Cloud Infrastructure (AWS, Azure, GCP), Identity Providers (Okta, Entra ID, Google Workspace, etc.), Endpoint Management (Jamf, Intune, CrowdStrike), Code/SDLC (GitHub, GitLab, Jira), and HR/Personnel (BambooHR, Checkr, KnowBe4, etc.) — each with the specific services/tests/auth method it uses. See `references/integrations.md` for the full per-category breakdown.

## Autopilot

Drata Autopilot is the automated evidence collection and remediation engine.

### How Autopilot Works

```
Standard flow (without Autopilot):
  Integration collects data → Test evaluates → PASS or FAIL
  FAIL: Control owner manually investigates and fixes
  Evidence: Admin manually uploads screenshot or runs manual collection

Autopilot flow:
  Integration collects data → Test evaluates → PASS or FAIL
  FAIL: Autopilot evaluates if auto-remediation is available
    → If yes: Autopilot applies fix (e.g., enforces MFA requirement)
    → Evidence: automatically generated and attached to control
    → Ticket: optional — creates Jira/Linear ticket for tracking
  Evidence: automatically generated without human action
```

**Autopilot capabilities:**
```
Automated remediation (where technically feasible):
  → GitHub: enable branch protection if disabled (with approval workflow)
  → AWS: enable CloudTrail in regions where disabled
  → AWS: enable S3 bucket encryption on non-compliant buckets
  → Intune/Jamf: flag non-compliant devices for IT follow-up

Automated evidence collection:
  → Every passing test generates evidence automatically
  → Evidence includes: timestamp, check performed, result, resources evaluated
  → No manual screenshot required

Evidence freshness:
  → Automated evidence refreshes on each integration poll (4-24 hour cycle)
  → Auditors see continuously fresh evidence — not stale screenshots
```

**Autopilot configuration:**
```
Drata → Autopilot → Settings
  → Enable/disable per integration
  → Configure approval requirement (some remediations require admin approval)
  → Set notification preferences (email/Slack on remediation taken)
  → Review remediation log (what was changed, when, by what automated action)
```

## Control Testing (1,200+ Tests)

### Test Organization

Tests are organized by:
- **Integration source** (which system they test)
- **Control domain** (access control, encryption, logging, etc.)
- **Framework** (which frameworks require this test)
- **Frequency** (continuous, daily, weekly, monthly, annual)

### Test Status Management

```
Test statuses:
  Passing: Control operating effectively (automated check PASS)
  Failing: Control gap identified (automated check FAIL)
  Not Configured: Integration not connected (test cannot run)
  Manual Review: Waiting for human review and evidence upload
  Excepted: Documented exception; excluded from compliance calculation
  Not Applicable: Control doesn't apply (with justification)

Responding to failing tests:
  1. Click failing test → Review what failed and why
  2. Options:
     a) Fix the underlying issue → test auto-resolves on next check
     b) Gather manual evidence → upload and submit for review
     c) Mark as exception → provide justification + expiry date
     d) Mark as not applicable → provide explanation (approved by admin)
  
Exception management:
  → Exceptions require justification text
  → Expiry date required (maximum 1 year recommended)
  → Exceptions visible to auditors — minimize where possible
  → Exception types: Risk Accepted, Compensating Control, False Positive
```

### Custom Tests

For controls not covered by built-in tests:

```
Drata → Controls → Custom test
  → Name and description
  → Frequency: continuous, daily, weekly, monthly, annual
  → Evidence type: screenshot, document, CSV, or any file
  → Assigned owner: who must provide evidence
  → Reviewer: who approves the evidence
  
Custom test examples:
  → Annual penetration test report (upload PDF annually)
  → Board meeting minutes including security discussion (upload quarterly)
  → DR/BCP test completion evidence (upload annually)
  → Annual vendor security assessment completion
```

## Personnel Management

Personnel management in Drata is more comprehensive than most GRC tools.

### Employee Onboarding Checklist

Drata tracks onboarding compliance tasks per employee:

```
Default onboarding checklist:
  ☐ Background check: initiated and completed
  ☐ Security awareness training: completed (within first 30 days)
  ☐ Policy attestation: acknowledged all required policies
  ☐ Device enrolled: laptop registered in MDM (Intune/Jamf)
  ☐ Device encrypted: BitLocker/FileVault enabled on assigned device
  ☐ MFA enrolled: authenticator app configured

Automated tracking:
  → HR integration: detects new hire start date
  → Drata sends welcome email to new employee
  → Employee completes tasks via Drata employee portal
  → Manager notified of incomplete items after 7/14/30 days
  → Compliance dashboard: % of employees fully onboarded
```

### Background Check Management

```
Integration flow (Checkr example):
  1. New employee added in BambooHR
  2. Drata detects new employee via HR integration
  3. Drata triggers Checkr background check initiation (if enabled)
  4. Checkr sends check request to employee
  5. Employee completes authorization in Checkr
  6. Checkr processes check (1-7 days)
  7. Checkr webhooks result to Drata: Passed / Pending / Failed
  8. Drata marks: background_check = Complete (or flags for HR review)

Evidence for audit:
  → Drata generates: employee list with background check status + completion date
  → No PII from background check stored in Drata (only pass/fail status)
```

### Security Training Tracking

```
KnowBe4 integration example:
  → Connect KnowBe4 API to Drata
  → Drata imports: employee name, training module, completion date
  → Annual training check: "Has employee completed security training in last 365 days?"
  → Automated test: checks all active employees have completed within policy period
  → Failing employees: listed in test failure details → IT/manager notified

Custom training providers:
  → Upload CSV: employee name, training name, completion date
  → Drata creates evidence from upload
  → Manual test passes after upload + reviewer approval
```

### Access Review Management

```
Access reviews are required for SOC 2 (CC6.2, CC6.3) and ISO 27001 (A.5.18).

Drata access review workflow:
  1. Admin creates access review campaign
     → Select systems to review (Okta, GitHub, AWS, etc.)
     → Select reviewers (managers, system owners)
     → Set deadline

  2. Reviewers receive notification
     → See list of users with access to their systems
     → For each user: Approve (keep access) or Revoke (remove access)
     → Add notes for unusual approvals

  3. Admin finalizes
     → Review completion status
     → For revoked access: IT team notified to action
     → Completion report generated

  4. Evidence
     → Access review report: who reviewed, what access, decision, date
     → Drata stores this as automated evidence for the control
```

## Asset Inventory

### Auto-Discovery

Drata automatically discovers assets via integrations:

```
Cloud assets (AWS, Azure, GCP):
  → EC2/VM instances, RDS databases, S3 buckets, Lambda functions
  → Attributes: region, encryption status, public/private, tags
  → Classification: auto-classify by tag (e.g., "environment: production")

Devices (Intune, Jamf):
  → All enrolled devices
  → Attributes: OS version, encryption status, last check-in, assigned user
  → Compliance status: MDM policies met or violation

SaaS applications:
  → Applications connected via Okta/Entra ID SSO
  → Users per app, app category, data classification

Code repositories (GitHub/GitLab):
  → All repositories in the organization
  → Public vs. private, branch protection status, last activity
```

### Asset Classification

```
Asset classes (customizable):
  Production: Active systems handling live customer data
  Staging: Pre-production environment (less strict controls may apply)
  Development: Development environments (often excluded from production controls)
  Corporate: Internal business systems (employee laptops, internal tools)

Tagging strategy:
  → AWS: tag all resources with environment=production|staging|dev
  → Drata reads tags to auto-classify
  → Untagged resources flagged for classification review

Classification matters for:
  → Scope: which assets are in scope for SOC 2 vs. out of scope
  → Controls: which controls apply to which asset classes
  → Exclusions: exclude dev environments from production checks
```

## Policy Center

### Policy Management Features

```
Policy library:
  → 40+ pre-built policy templates (Information Security Policy, AUP, IR Policy, etc.)
  → Customizable: edit templates to match your company's practices
  → Version control: automatic on every save
  → Policy history: full version trail for audit purposes

Policy approval workflow:
  1. Draft: policy author creates/edits policy
  2. Review: reviewer provides feedback
  3. Approve: designated approver (CISO, Legal) formally approves
  4. Publish: policy available to all employees
  5. Attestation: all employees acknowledge (automated campaign)

Policy attestation:
  → Annual campaigns sent automatically based on policy review date
  → Employees complete attestation in Drata employee portal
  → Completion tracked: who attested, when, which version
  → Evidence: attestation completion report (downloaded or auto-attached to control)
```

### Required Policies for SOC 2

```
Minimum policies required for SOC 2:
  1. Information Security Policy (umbrella)
  2. Acceptable Use Policy
  3. Access Control Policy
  4. Encryption Policy
  5. Incident Response Policy
  6. Change Management Policy
  7. Business Continuity / Disaster Recovery Policy
  8. Vendor Management Policy
  9. Data Classification Policy
  10. Password/Authentication Policy

Drata templates available for all of the above.
```

## Risk Management

### Risk Register

```
Drata Risk Register:
  → Create risks manually or import from CSV
  → Risk scoring: configurable likelihood × impact matrix
  → Risk categories: access control, data security, operations, compliance, etc.
  → Treatment tracking: mitigate (tasks + owners), accept (documentation), transfer, avoid

Linking risks to controls:
  → Each risk links to controls that mitigate it
  → Control effectiveness feeds back into residual risk score
  → If linked controls are failing → residual risk automatically flagged higher

Risk workflow:
  1. Identify risk (manual entry or from vendor assessment)
  2. Score: likelihood + impact
  3. Assign treatment type and owner
  4. Create remediation tasks (linked to Jira if integrated)
  5. Review quarterly (reminder sent to risk owner)
  6. Close when treatment complete + evidence provided
```

## Audit Preparation

### Audit Package

```
Drata → Audit Hub → Prepare audit

Pre-audit checklist:
  → Overall compliance score: target ≥85% before inviting auditor
  → All critical controls: must be passing
  → Evidence coverage: no gaps in audit period coverage
  → Exceptions documented and approved
  → Personnel checks complete: all employees in onboarding checklist

Auditor portal:
  → Invite auditor: Audit Hub → Invite auditor → enter email
  → Auditor receives access to read-only Drata view
  → Auditor can: view tests, evidence, exceptions, submit RFIs
  → RFI workflow: auditor submits question → your team responds → closed

Audit timeline for SOC 2 Type II:
  Month 1-2: Connect integrations; fix critical gaps
  Month 3-5: Evidence collection period (automated runs continuously)
  Month 6: Invite auditor; fieldwork begins
  Month 7-8: Respond to RFIs; auditor completes testing
  Month 9: Draft report review; management response
  Month 10: Final report issued
```

## Drata Employee Portal

Self-service portal for employees to complete compliance tasks:

```
Employee portal access: portal.drata.com (or custom domain)

Employee tasks visible:
  → Complete background check (link to Checkr/Sterling)
  → Complete security training (link to KnowBe4 or embedded training)
  → Attest to policies (read policy → click acknowledge)
  → Register personal device (if BYOD program)
  → View assigned equipment and encryption status

Benefits:
  → Reduces IT/security team burden for individual employee tracking
  → Self-service reduces time to compliance for new hires
  → Clear accountability: employees see their own compliance status
```

## Common Issues and Troubleshooting

**Integration failing to sync:**
1. Drata → Integrations → [Integration] → Check sync status and last sync time
2. Re-authenticate: many API tokens expire (Okta 30 days, GitHub tokens vary)
3. Check permissions: validate the service account still has required permissions
4. Look for API rate limiting: large orgs may hit rate limits during collection

**Test not running:**
1. Verify the integration the test depends on is connected and syncing
2. Check if the test scope includes your resources (exclude/include filters)
3. For new integrations: allow 24 hours for initial data collection

**Autopilot remediation failed:**
1. Review remediation log: Drata → Autopilot → Remediation history
2. Check if required permissions were present (some remediations need write access)
3. Some remediations require manual approval — check pending approval queue

**Low compliance score before audit:**
1. Prioritize: focus on failing tests in critical controls first
2. Review exceptions: are any exceptions from prior year still open?
3. Check personnel: are all employees complete on onboarding checklist?
4. Asset inventory: are all production assets discovered and classified?

## Reference Files

- `references/architecture.md` — Drata internal architecture, integration pipeline, Autopilot engine, evidence generation, control testing framework, personnel management data model
- `references/integrations.md` — Full per-category integration breakdown (Cloud, IdP, Endpoint, Code/SDLC, HR/Personnel) with services, auth methods, and tests covered.
