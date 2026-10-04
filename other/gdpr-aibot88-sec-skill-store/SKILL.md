---
name: gdpr
description: "GDPR and CCPA/CPRA privacy compliance audit for codebases. Inventories PII fields (email, phone, SSN, IP, device ID, geolocation, biometrics, behavioral data), maps data collection points (forms, APIs, cookies, analytics, error tracking), audits consent mechanisms (cookie banners, opt-in, pre-checked boxes, consent withdrawal), verifies data subject rights implementation (right to access, erasure, rectification, portability, opt-out, Do Not Sell), traces third-party data sharing (Google Analytics, Facebook Pixel, Stripe, SendGrid, Sentry), and checks data retention policies and automated purging. Use when auditing privacy compliance, building data export or deletion endpoints, reviewing cookie consent, or assessing DSAR readiness."
version: "2.0.0"
category: security
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Scan, assess, and report compliance gaps.

TARGET:
$ARGUMENTS

If no arguments provided, perform a full GDPR/CCPA compliance assessment of the project in the current working directory.

============================================================
PHASE 0: TECH STACK DETECTION
============================================================

Auto-detect the project stack to determine where data flows:

- Backend framework (Express, Django, Rails, etc.)
- Database layer (PostgreSQL, MongoDB, Firestore, etc.)
- ORM/ODM in use (Prisma, Sequelize, Mongoose, Django ORM, etc.)
- Frontend framework (React, Vue, Flutter, etc.)
- Authentication provider (Firebase Auth, Auth0, Cognito, custom)
- Analytics/tracking (Google Analytics, Mixpanel, Segment, etc.)
- Email/notification services (SendGrid, SES, Twilio, etc.)
- Payment processing (Stripe, PayPal, etc.)
- Cloud provider (AWS, GCP, Azure, etc.)

Record all detected integrations — each represents a potential data processing path.

============================================================
PHASE 1: PII FIELD IDENTIFICATION
============================================================

Scan ALL data models, schemas, and database definitions for PII fields:

DIRECT IDENTIFIERS (high sensitivity):
- Full name, first name, last name
- Email address
- Phone number
- Social Security Number / National ID
- Passport number, driver's license
- Financial account numbers, credit card numbers
- Biometric data references

INDIRECT IDENTIFIERS (medium sensitivity):
- Date of birth, age
- Physical address, ZIP/postal code
- IP address
- Device identifiers (IMEI, MAC address, device ID)
- GPS/location coordinates
- Photos/avatars (may contain faces)

BEHAVIORAL DATA (lower sensitivity, still regulated):
- Purchase history, browsing history
- Search queries
- Usage patterns, session data
- Preferences, settings tied to a user

For each PII field found, record:
- File path and line number
- Field name and type
- Which data model it belongs to
- Whether it is encrypted at rest
- Whether it has a retention policy

============================================================
PHASE 2: DATA COLLECTION POINTS
============================================================

Identify every point where user data enters the system:

FORMS AND UI:
- Registration/signup forms — what fields are collected
- Profile edit forms
- Contact/support forms
- Payment forms
- Any form collecting personal data

API ENDPOINTS:
- POST/PUT endpoints that accept user data
- File upload endpoints
- Webhook receivers that process user data

IMPLICIT COLLECTION:
- IP address logging in middleware/access logs
- User-agent string storage
- Geolocation tracking
- Cookie setting (what data, what purpose, what duration)
- Analytics event tracking (what user properties are sent)
- Error reporting services (what user context is attached)

For each collection point:
- What data is collected
- Is there a stated purpose for collection
- Is consent obtained before collection
- Is the data minimized (collecting only what is needed)

============================================================
PHASE 3: CONSENT MECHANISMS
============================================================

Check for proper consent handling:

COOKIE CONSENT:
- Cookie banner/consent manager present
- Consent obtained before setting non-essential cookies
- Cookie categories defined (necessary, analytics, marketing)
- Consent preferences stored and respected
- Easy mechanism to withdraw consent

DATA PROCESSING CONSENT:
- Explicit opt-in for marketing communications
- Consent recorded with timestamp
- Separate consent for separate purposes (not bundled)
- Pre-checked boxes (violation if used for consent)

PRIVACY POLICY:
- Privacy policy page exists and is accessible
- Policy linked from data collection points
- Policy covers: what data, why, how long, who has access, user rights
- Policy is up to date (check for stale dates or references)

TERMS OF SERVICE:
- ToS exists and covers data processing
- ToS linked during registration

============================================================
PHASE 4: DATA SUBJECT RIGHTS
============================================================

Check implementation of required data subject rights:

RIGHT TO ACCESS (Article 15 / CCPA Right to Know):
- Can users request a copy of their data?
- Is there an API endpoint or UI for data export?
- Does the export include ALL user data across all tables/collections?
- Export format: machine-readable (JSON, CSV)?

RIGHT TO ERASURE (Article 17 / CCPA Right to Delete):
- Can users request account deletion?
- Does deletion cascade to all related data?
- Does deletion reach third-party services (analytics, email lists)?
- Are backups considered (data may persist in backups)?
- Is there a soft-delete with scheduled hard-delete, or immediate?

RIGHT TO RECTIFICATION (Article 16):
- Can users edit/correct their personal data?
- Are corrections propagated to all copies of the data?

RIGHT TO PORTABILITY (Article 20):
- Can users export their data in a portable format?
- Is the format interoperable (JSON, CSV, not proprietary)?

RIGHT TO OBJECT (Article 21 / CCPA Right to Opt-Out):
- Can users opt out of data processing for marketing?
- Can users opt out of automated profiling/decision-making?
- Is there a "Do Not Sell" mechanism (CCPA requirement)?

============================================================
PHASE 5: THIRD-PARTY DATA SHARING
============================================================

Identify all third-party services that receive user data:

ANALYTICS:
- Google Analytics, Mixpanel, Amplitude, Segment, etc.
- What user properties are sent
- Is consent obtained before tracking

ADVERTISING:
- Facebook Pixel, Google Ads, etc.
- What conversion data is shared
- Is there a "Do Not Sell" opt-out

INTEGRATIONS:
- Payment processors (Stripe, PayPal) — what data is shared
- Email services (SendGrid, Mailchimp) — email + name + preferences
- SMS services (Twilio) — phone numbers
- Cloud storage — what user data is stored
- Error tracking (Sentry, Bugsnag) — what user context is attached

For each third party:
- What data is shared
- Is there a Data Processing Agreement (DPA) in place
- Is the data transfer compliant (EU→US: adequate safeguards?)
- Is the sharing disclosed in the privacy policy

============================================================
PHASE 6: DATA RETENTION
============================================================

Check data retention practices:

- Are retention periods defined for each data category?
- Is there automated data expiry/cleanup?
- Are inactive accounts purged after a defined period?
- Are logs rotated and expired?
- Are backups expired according to retention policy?
- Is there a data retention schedule document?

Flag any data that appears to be stored indefinitely without justification.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the security analysis, validate thoroughness:

1. Verify every category in the audit was actually checked (not skipped).
2. Verify every finding has a specific file:line location.
3. Verify severity ratings are justified by impact assessment.
4. Verify no false positives by re-reading flagged code in context.

IF VALIDATION FAILS:
- Re-audit skipped categories or vague findings
- Verify or remove false positives
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## GDPR/CCPA Compliance Report

**Project:** [name]
**Stack:** [detected technologies]
**Assessment Date:** [date]

### Compliance Summary

| Area | Status | Findings |
|------|--------|----------|
| PII Identification | [PASS/PARTIAL/FAIL] | N fields found |
| Consent Mechanisms | [PASS/PARTIAL/FAIL] | N gaps |
| Data Subject Rights | [PASS/PARTIAL/FAIL] | N missing |
| Third-Party Sharing | [PASS/PARTIAL/FAIL] | N services |
| Data Retention | [PASS/PARTIAL/FAIL] | N issues |
| Privacy Policy | [PASS/PARTIAL/FAIL] | N gaps |

### PII Inventory

| Field | Model/Table | Encrypted | Retention | Purpose |
|-------|-------------|-----------|-----------|---------|
| email | users | No | Indefinite | Authentication |

### Missing Data Subject Rights

| Right | Status | Implementation Guidance |
|-------|--------|------------------------|
| Access/Export | [Implemented/Missing] | Build GET /api/user/export endpoint |
| Erasure/Delete | [Implemented/Missing] | Build DELETE /api/user with cascade |
| Rectification | [Implemented/Missing] | Ensure profile edit covers all PII |
| Portability | [Implemented/Missing] | Add JSON/CSV export option |
| Object/Opt-Out | [Implemented/Missing] | Add marketing preference toggle |

### Third-Party Data Flows

| Service | Data Shared | DPA | Consent | Disclosed |
|---------|------------|-----|---------|-----------|
| Google Analytics | IP, pages, events | ? | No banner | No |

### Compliance Checklist

- [ ] All PII fields identified and documented
- [ ] Cookie consent banner with opt-in
- [ ] Privacy policy covers all data processing
- [ ] Data export endpoint (right to access)
- [ ] Account deletion with cascade (right to erasure)
- [ ] Marketing opt-out mechanism
- [ ] Data retention policies defined and automated
- [ ] DPAs in place with all third-party processors
- [ ] Data breach notification process documented
- [ ] Data Protection Impact Assessment completed (if high-risk processing)

### Remediation Priority
[Ordered list: Critical gaps first, then CCPA-specific, then best practices]

============================================================
NEXT STEPS
============================================================

After reviewing the compliance report:
- "Implement missing data subject rights (export, delete, opt-out)."
- "Run `/encryption` to ensure PII is encrypted at rest and in transit."
- "Run `/soc2` for broader compliance assessment."
- "Run `/secure` for full security posture including data handling."
- "Consult legal counsel for privacy policy and DPA review."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /gdpr — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT modify any code — this is an assessment skill, not an implementation skill.
- Do NOT provide legal advice — flag gaps and suggest technical implementations.
- Do NOT expose actual PII values found in the codebase — redact in output.
- Do NOT skip third-party integrations — they are the most common compliance gap.
- Do NOT assume compliance based on the presence of a privacy policy alone.
- Do NOT conflate GDPR and CCPA requirements — note which regulation each finding applies to.
- Do NOT ignore implicit data collection (logs, analytics, error tracking).
