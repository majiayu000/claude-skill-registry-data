---
name: popia-compliance
description: Use this skill whenever writing any code that collects, stores, processes, exports, or deletes personal information in the Myelin platform — including learner profiles, consent flows, data subject requests, cross-border transfers, or retention automation. This is the authoritative POPIA implementation contract for South Africa with expansion notes for Rwanda, Kenya, and Zambia. Load this skill before writing any data collection, user profile, consent, or export code.
---

This skill defines the POPIA (Protection of Personal Information Act, South Africa) compliance implementation for the Myelin platform. POPIA compliance is a mandatory prerequisite for any South African institutional deployment. Every data collection point, retention policy, and subject rights workflow must be built from this contract.

---

## Core POPIA Obligations

Eight conditions of lawful processing. Every data processing activity in the platform must satisfy all that apply:

1. **Accountability** — Myelin (as Responsible Party) is accountable for POPIA compliance. Super Admin is the designated Information Officer.
2. **Processing limitation** — personal information may only be processed for the specific, lawful purpose for which it was collected.
3. **Purpose specification** — the purpose must be stated explicitly at the time of collection and not changed without fresh consent.
4. **Further processing limitation** — personal information may not be used in a manner incompatible with the original purpose.
5. **Information quality** — take reasonable steps to ensure personal information is complete, accurate, and up to date.
6. **Openness** — data subjects must be informed of what is collected, why, and how.
7. **Security safeguards** — reasonable and appropriate security measures (see `security-controls` skill).
8. **Data subject participation** — data subjects have the right to access, correct, and request deletion of their personal information.

---

## Personal Information Classification

| Category | Examples | Sensitivity | Handling requirement |
|----------|---------|-------------|---------------------|
| Identity | Name, ID number, learner ID | Standard | Encrypted at rest, role-scoped access |
| Contact | Email, phone number | Standard | Encrypted at rest, used only for platform communications |
| Authentication | Password hash, SSO token | High | Hashed/encrypted, never logged in plaintext |
| Learning records | Module progress, simulation attempts, submissions | Standard | Tenant-scoped, 10-year retention |
| Assessment outcomes | Scores, competency status, result statements | Standard | Tenant-scoped, 10-year retention, versioned |
| Workplace | Placement records, logbook entries, employer name | Standard | Tenant-scoped, 7-year retention |
| Biometric (if hand tracking enabled) | Hand geometry data from MediaPipe | Special | Explicit separate consent required, not stored beyond session |
| Health/Wellbeing (if disclosed) | Mental health indicators in agent transcripts | Special | Escalation only, not used for analytics |

Special category personal information (biometric, health) requires explicit, separate consent beyond the standard platform consent. Do not collect it without dedicated consent capture.

---

## Consent Flow

Consent must be captured before any training interaction begins (FR-005). It is not a checkbox buried in terms — it is an explicit, informed, affirmative action.

### Consent capture requirements

- Display a clear, plain-language summary of what data is collected, why, and for how long
- Provide a link to the full Privacy Notice
- Require an affirmative action (button press, not pre-ticked checkbox)
- Record the consent as an immutable `ConsentRecord` entity (see `data-model-entities` skill)
- Block access to all training features until consent is confirmed

```javascript
async function captureConsent(userId, tenantId, consentVersion, req) {
  // Check no existing active consent for this version
  const existing = await getActiveConsent(userId, tenantId);
  if (existing && existing.consentVersion === consentVersion) {
    return existing; // already consented to this version
  }

  const record = await db.query(`
    INSERT INTO consent_records
      (consent_id, tenant_id, user_id, consent_version, captured_at,
       method, ip_address, user_agent)
    VALUES ($1, $2, $3, $4, NOW(), 'EXPLICIT_CHECKBOX', $5, $6)
    RETURNING *
  `, [
    generateUUID(), tenantId, userId, consentVersion,
    req.ip, req.headers['user-agent']
  ]);

  await writeAuditEntry('CONSENT_CAPTURED', { userId, tenantId, consentVersion });
  return record.rows[0];
}
```

### Consent versioning

Every change to the Privacy Notice or consent text increments the `consentVersion`. When a new version is published:
- Existing learners must re-consent at next login before accessing training features
- Old consent records are retained — they are not replaced
- The consent capture UI must clearly state what has changed from the previous version

---

## Consent Gate Middleware

```javascript
async function requireConsent(req, res, next) {
  const { userId, tenantId } = req.session;
  const currentVersion = await getCurrentConsentVersion(tenantId);

  const consent = await getActiveConsent(userId, tenantId);
  if (!consent || consent.consentVersion !== currentVersion) {
    return res.status(403).json({
      error:    'CONSENT_REQUIRED',
      redirect: '/consent',
      version:  currentVersion
    });
  }
  next();
}
```

Apply `requireConsent` middleware to all `/app/*` routes. It must run after `authMiddleware`.

---

## Consent Revocation

A learner may revoke consent at any time from Profile > Privacy Settings.

On revocation:
1. Set `ConsentRecord.revokedAt` to the current timestamp — do not delete the record
2. Terminate all active sessions for that user immediately
3. Lock the user account with status `CONSENT_REVOKED`
4. Notify the tenant Admin via the escalation queue (type: `DATA_SUBJECT_REQUEST`)
5. Initiate a data handling review with the Admin within 30 days

Revocation does not trigger immediate data deletion. Records must be retained for their full retention period. However:
- The learner's data must not be used in any new analytics or reporting after revocation
- Active coaching context must not include data from a consent-revoked learner
- The learner's records must be excluded from any new exports after revocation

---

## Data Subject Rights Workflows

POPIA grants data subjects three primary rights. Each must have an implemented workflow.

### Right of access (Section 23)

The learner may request a copy of all personal information held about them.

```javascript
async function generateDataSubjectAccessPack(userId, tenantId, requestedBy) {
  requireRole(requestedBy, ['ADMIN', 'SUPER_ADMIN']);

  const pack = {
    exportId:        generateUUID(),
    generatedAt:     new Date().toISOString(),
    userId,
    tenantId,
    profile:         await getUserProfile(userId, tenantId),
    consentRecords:  await getConsentRecords(userId, tenantId),
    enrollments:     await getEnrollments(userId, tenantId),
    simulationAttempts: await getSimulationAttempts(userId, tenantId),
    submissions:     await getSubmissions(userId, tenantId),
    agentTranscripts: await getAgentTranscripts(userId, tenantId),  // includes message content
    logbookEntries:  await getLogbookEntries(userId, tenantId),
    resultStatements: await getResultStatements(userId, tenantId),
    auditLog:        await getAuditEntriesForSubject(userId, tenantId)
  };

  await writeAuditEntry('DATA_SUBJECT_ACCESS_EXPORT', { userId, tenantId, exportId: pack.exportId });
  return pack;
}
```

Access requests must be fulfilled within 30 days. Response to the data subject must be in a commonly used electronic format (JSON or PDF export).

### Right of correction (Section 24)

The learner may request correction of inaccurate personal information.

- Identity fields (name, contact): Admin-gated correction with audit log entry
- Learning records: corrections to assessment outcomes require a separate appeals process (out of scope for v1 automation — escalate to Admin)
- Corrections must be reflected in all downstream records that reference the corrected field

### Right of deletion (Section 24)

The learner may request deletion of their personal information where retention is not required by law.

POPIA does not require deletion of records that must be retained by law or for legitimate business purposes. For Myelin:
- Learning records and result statements have a 10-year retention obligation and **cannot** be deleted on request during that period
- Authentication data and contact information **can** be anonymised after the retention period
- Agent transcripts have a 2-year retention obligation

Deletion requests are handled as anonymisation after the retention period:

```javascript
async function anonymiseLearnerRecord(userId, tenantId) {
  // Replace PII with anonymised placeholders — preserve the record structure for audit
  await db.query(`
    UPDATE users
    SET email = 'anonymised-' || user_id || '@deleted.myelin.io',
        password_hash = NULL,
        deleted_at = NOW()
    WHERE user_id = $1 AND tenant_id = $2
  `, [userId, tenantId]);

  await writeAuditEntry('DATA_SUBJECT_ANONYMISED', { userId, tenantId });
}
```

---

## Data Minimisation

The AI agent context must not include more personal information than necessary for the coaching task.

Allowed in agent context:
- `learnerId` (opaque identifier — not name or email)
- `activeModuleId`, `activeStepId` (learning location)
- `recentErrors` (performance signals — no PII)
- `attemptCount`, `sessionElapsedSeconds` (numeric signals)

Not allowed in agent context:
- Learner name or email
- ID number or national identifier
- Employer name or placement details
- Any health or biometric information

---

## Cross-Border Data Transfer

Personal information may not be transferred outside South Africa without adequate protection. Rules for expansion markets:

| Destination | Requirement |
|-------------|-------------|
| Rwanda | Obtain a data transfer agreement; document in tenant record; log each export with `cross_border_export_log` entry |
| Kenya | Policy pack selection by tenant; export approval workflow; redact analytics exports |
| Zambia | Data classification labels; export approval workflow; retention policy lock by tenant |
| Cloud hosting outside SA | Acceptable only if cloud provider offers SA-region deployment (`af-south-1` or equivalent) or has an approved adequacy finding |

```javascript
async function validateCrossBorderExport(tenantId, destinationCountry, exportType) {
  const policy = await getTenantCompliancePolicy(tenantId);

  if (policy.dataResidencyRegion !== destinationCountry) {
    const transferAgreement = await getCrossBorderAgreement(tenantId, destinationCountry);
    if (!transferAgreement || !transferAgreement.approved) {
      throw new ComplianceError('CROSS_BORDER_TRANSFER_NOT_APPROVED');
    }
    await logCrossBorderExport({ tenantId, destinationCountry, exportType, agreementId: transferAgreement.id });
  }
}
```

---

## Retention Automation

Retention periods must be automatically enforced. Do not rely on manual cleanup.

```javascript
// Nightly retention job — runs at 02:00 UTC
async function runRetentionJob() {
  const now = new Date();

  // Class A — 10-year retention (learning records, results, audit logs)
  // No action until 10 years have passed — these are retained in full

  // Class B — 7-year retention (peer reviews, logbook, placements)
  const classB_cutoff = new Date(now - 7 * 365.25 * 24 * 60 * 60 * 1000);
  await archiveExpiredRecords('peer_reviews',    classB_cutoff);
  await archiveExpiredRecords('logbook_entries', classB_cutoff);

  // Class C — 2-year retention (agent transcripts, notifications)
  const classC_cutoff = new Date(now - 2 * 365.25 * 24 * 60 * 60 * 1000);
  await archiveExpiredTranscripts(classC_cutoff); // skips entries with open escalations
  await archiveExpiredNotifications(classC_cutoff);

  await writeAuditEntry('RETENTION_JOB_COMPLETE', { runAt: now.toISOString() });
}
```

Archive means: move to cold storage or an archive table. Never hard-delete during the retention period. After the retention period, anonymisation or deletion may proceed per data subject rights rules above.

---

## What Not To Do

- Do not collect personal information beyond what is necessary for the stated purpose
- Do not process personal information for a purpose other than the one stated at collection
- Do not allow training access before consent is captured and confirmed
- Do not delete `ConsentRecord` entries on revocation — set `revokedAt` instead
- Do not allow cross-border transfer without a documented transfer agreement
- Do not include learner name, email, or national ID in agent context payloads
- Do not collect biometric data (hand tracking geometry) without a separate explicit consent
- Do not hard-delete any record before its retention period has elapsed
- Do not omit the audit log entry for any data subject rights action
