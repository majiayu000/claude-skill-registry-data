---
name: data-model-entities
description: Use this skill whenever designing or writing database schemas, migrations, ORM models, API response shapes, or any code that defines or references the platform's core domain entities. This is the authoritative entity list, relationship map, and data governance contract. Do not invent new entities, field names, or relationships without first consulting this skill. Load this before writing any schema, migration, or data access code.
---

This skill defines all 19 core domain entities for the Myelin platform, their key fields, relationships, and the data governance rules that apply to each. This is the canonical reference — any schema, migration, or model that diverges from it creates technical debt that compounds across the build.

---

## Data Governance Rules (Apply to All Entities)

These rules apply to every entity without exception.

**Tenant scoping**: Every business record carries a `tenantId`. Entities without a `tenantId` are platform-level only (e.g. `Tenant` itself). See `multi-tenant-isolation` skill for enforcement.

**Soft delete**: Business records are never hard-deleted during normal operation. Use a `deletedAt` timestamp. Queries must filter `WHERE deleted_at IS NULL` unless explicitly auditing deletion history.

**Immutable audit trail**: Records that are externally significant (submissions, results, policy configs, scoring rules) are versioned — updates create a new version record rather than mutating the existing one.

**Retention classes**:
- Class A (10-year minimum): `SimulationStepEvent`, `Submission`, `ResultStatement`, `AuditLog`, `ConsentRecord`, `AgentTranscript`
- Class B (7-year minimum): `PeerReview`, `LogbookEntry`, `MentorSignoff`, `Enrollment`
- Class C (standard 2-year): `Notification`, session and cache data

**Identifiers**: All primary keys are UUID v4. Tenant-scoped identifiers (e.g. `learnerId` in telemetry payloads) are derived from `User.userId` and must never be raw email addresses in externally-facing payloads.

---

## Entity Definitions

### 1. Tenant

Platform-level entity. No `tenantId` foreign key on this entity itself.

Key fields:
- `tenantId` UUID PK
- `tenantName` string
- `tenantSlug` string unique
- `packageTier` enum: PILOT | OPERATIONAL | NATIONAL_PROGRAM
- `featureFlags` JSONB (see `multi-tenant-isolation` skill for flag schema)
- `compliancePolicyPack` string
- `compliancePolicyVersion` string
- `dataResidencyRegion` string
- `ssoConfig` JSONB
- `retentionPolicyYears` integer default 10
- `status` enum: ACTIVE | SUSPENDED | OFFBOARDED
- `createdAt`, `updatedAt`

Relationships:
- Has many `User`, `Programme`, `AuditLog`

---

### 2. User

One record per human per tenant. A person with access to two tenants has two `User` records.

Key fields:
- `userId` UUID PK
- `tenantId` UUID FK → Tenant
- `email` string (unique within tenant)
- `passwordHash` string nullable (null for SSO-only accounts)
- `ssoSubjectId` string nullable
- `ssoMethod` enum: NONE | OIDC | SAML
- `status` enum: ACTIVE | PENDING_ACTIVATION | SUSPENDED | OFFBOARDED
- `activatedAt` timestamp nullable
- `lastLoginAt` timestamp nullable
- `deletedAt` timestamp nullable
- `createdAt`, `updatedAt`

Relationships:
- Has one `RoleAssignment`
- Has many `Enrollment`, `ConsentRecord`, `SimulationAttempt`, `Submission`, `LogbookEntry`, `AgentTranscript`

Note: Do not store PII beyond what is required for identity and contact. `email` is the primary identity field; do not duplicate it into telemetry payloads — use `userId` instead.

---

### 3. RoleAssignment

One role per user per tenant.

Key fields:
- `assignmentId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `role` enum: STUDENT | LECTURER | ADMIN | EMPLOYER_MENTOR | MINISTRY_VIEWER | PROCUREMENT_REVIEWER | REGULATOR_AUDITOR | SUPER_ADMIN
- `assignedBy` UUID FK → User (the admin who made the assignment)
- `assignedAt` timestamp
- `revokedAt` timestamp nullable
- `scopeConstraint` JSONB nullable (used for Ministry/Regulator to constrain which tenant IDs they may access)

Relationships:
- Belongs to `User`

Note: A revoked `RoleAssignment` is retained for audit. Never delete role assignment records.

---

### 4. Programme

A top-level qualification or training programme. Contains one or more `Module` records.

Key fields:
- `programmeId` UUID PK
- `tenantId` UUID FK → Tenant
- `title` string
- `qualificationFramework` string (e.g. "QCTO", "NQF")
- `qualificationLevel` integer
- `coreModuleIds` UUID array (modules that are mandatory for all learners in this programme)
- `curriculumOutcomeIds` string array (e.g. ["FND-TT-01", "FND-IW-01"])
- `status` enum: DRAFT | ACTIVE | ARCHIVED
- `version` integer (increments on each published update)
- `createdAt`, `updatedAt`, `deletedAt`

Relationships:
- Belongs to `Tenant`
- Has many `Module`, `Enrollment`

---

### 5. Module

A learning unit within a programme. Contains `LearningItem` records.

Key fields:
- `moduleId` UUID PK
- `tenantId` UUID FK → Tenant
- `programmeId` UUID FK → Programme
- `title` string
- `moduleType` enum: FOUNDATION | SPECIALIZATION
- `prerequisiteModuleIds` UUID array
- `completionPolicy` JSONB (weighted criteria, mandatory checkpoints, pass thresholds)
- `standards` JSONB array (standards references for audit)
- `estimatedDurationMinutes` integer
- `status` enum: DRAFT | ACTIVE | ARCHIVED
- `version` integer
- `createdAt`, `updatedAt`, `deletedAt`

---

### 6. LearningItem

An individual content or assessment item within a module.

Key fields:
- `itemId` UUID PK
- `tenantId` UUID FK → Tenant
- `moduleId` UUID FK → Module
- `itemType` enum: VIDEO | QUIZ | SIMULATION | PRACTICAL_TASK
- `title` string
- `contentRef` string (URL or asset identifier)
- `durationMinutes` integer nullable
- `isGated` boolean (if true, must be completed before next item unlocks)
- `scenarioId` string nullable (for SIMULATION items, e.g. "LOTO_7STEP_v1")
- `rubricId` UUID nullable FK → Rubric (for PRACTICAL_TASK items)
- `order` integer
- `createdAt`, `updatedAt`, `deletedAt`

---

### 7. Enrollment

Tracks a learner's enrolment in a programme.

Key fields:
- `enrollmentId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `programmeId` UUID FK → Programme
- `enrolledAt` timestamp
- `status` enum: ACTIVE | COMPLETED | WITHDRAWN | SUSPENDED
- `completedAt` timestamp nullable
- `progressSnapshot` JSONB (cached progress state for dashboard — always recomputed from events for audit)
- `createdAt`, `updatedAt`

---

### 8. SimulationAttempt

A learner's attempt at a simulation scenario. One record per session.

Key fields:
- `attemptId` UUID PK
- `sessionId` UUID unique (matches `sessionId` in telemetry events)
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `scenarioId` string
- `scenarioVersion` string
- `scoringRulesVersion` string
- `status` enum: IN_PROGRESS | COMPLETE | ABANDONED
- `resetCount` integer default 0
- `assistModeUsed` boolean
- `inputMode` enum
- `startedAt` timestamp
- `completedAt` timestamp nullable
- `totalDurationSeconds` integer nullable
- `demoMode` boolean
- `createdAt`, `updatedAt`

Relationships:
- Has many `SimulationStepEvent`

---

### 9. SimulationStepEvent

Immutable event record for each assessed simulation step attempt. See `simulation-telemetry-schema` skill for the full payload schema. This table maps directly to that schema.

Key fields (column representation):
- `eventId` UUID PK
- `sessionId` UUID FK → SimulationAttempt.sessionId
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `scenarioId` string
- `scenarioVersion` string
- `scoringRulesVersion` string
- `stepId` string
- `attemptNumber` integer
- `timestamp` timestamp
- `result` enum: PASS | FAIL
- `measuredValue` numeric
- `requiredThreshold` numeric
- `thresholdOperator` enum
- `toleranceDelta` numeric nullable
- `inputMode` enum
- `fpsAtEvent` numeric
- `frameTimeMsAtEvent` numeric
- `interactionLatencyMs` numeric
- `curriculumOutcomeIds` string array
- `demoMode` boolean

Governance: append-only. No UPDATE or DELETE on this table. Retention Class A.

---

### 10. Submission

A learner's e-Portfolio evidence submission.

Key fields:
- `submissionId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `moduleId` UUID FK → Module
- `itemId` UUID FK → LearningItem
- `version` integer (increments on resubmission; prior versions are retained)
- `fileRef` string (signed storage URL or object key)
- `fileType` enum: MP4
- `fileSizeBytes` integer
- `malwareScanStatus` enum: PENDING | CLEAN | QUARANTINED
- `transcodeStatus` enum: PENDING | COMPLETE | FAILED
- `status` enum: DRAFT | SUBMITTED | UNDER_REVIEW | PASSED | REWORK_REQUIRED
- `submittedAt` timestamp nullable
- `reviewedAt` timestamp nullable
- `reviewedBy` UUID FK → User nullable
- `reviewNotes` text nullable
- `rubricScore` JSONB nullable
- `createdAt`, `updatedAt`

Governance: versioned. On resubmission, create a new version record. Retain all versions. Retention Class A.

---

### 11. Rubric

A scoring rubric attached to a practical task or peer review.

Key fields:
- `rubricId` UUID PK
- `tenantId` UUID FK → Tenant
- `title` string
- `criteria` JSONB array (each criterion: id, label, description, maxScore, required)
- `passMark` numeric
- `version` integer
- `status` enum: DRAFT | ACTIVE | ARCHIVED
- `createdAt`, `updatedAt`

---

### 12. PeerReview

A peer review assignment and its completed evaluation.

Key fields:
- `reviewId` UUID PK
- `tenantId` UUID FK → Tenant
- `submissionId` UUID FK → Submission
- `reviewerId` UUID FK → User
- `rubricId` UUID FK → Rubric
- `assignedAt` timestamp
- `status` enum: ASSIGNED | IN_PROGRESS | SUBMITTED | MODERATED
- `criteriaScores` JSONB nullable (map of criterion id → score)
- `feedbackText` text nullable
- `submittedAt` timestamp nullable
- `moderationStatus` enum: PENDING | APPROVED | FLAGGED nullable
- `moderatedBy` UUID FK → User nullable
- `moderatedAt` timestamp nullable
- `createdAt`, `updatedAt`

Constraint: `reviewerId` must not equal the `userId` of the `Submission` being reviewed. Enforce at database level with a CHECK constraint.

---

### 13. Placement

A learner's workplace placement record.

Key fields:
- `placementId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User (learner)
- `mentorId` UUID FK → User (employer mentor)
- `employerName` string
- `startDate` date
- `endDate` date nullable
- `status` enum: ACTIVE | COMPLETED | TERMINATED
- `createdAt`, `updatedAt`

---

### 14. LogbookEntry

A learner's workplace logbook record tied to a placement.

Key fields:
- `entryId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User (learner)
- `placementId` UUID FK → Placement
- `activityDate` date
- `activityCategory` string
- `description` text
- `evidenceRefs` string array (file references)
- `signoffStatus` enum: PENDING | APPROVED | REJECTED
- `createdAt`, `updatedAt`

Relationships:
- Has one `MentorSignoff` (when signoff is requested)

---

### 15. MentorSignoff

The mentor's approval record for a logbook entry.

Key fields:
- `signoffId` UUID PK
- `tenantId` UUID FK → Tenant
- `entryId` UUID FK → LogbookEntry
- `mentorId` UUID FK → User
- `decision` enum: APPROVED | REJECTED
- `comments` text nullable
- `signedAt` timestamp
- `identityProofMethod` string (e.g. "session-authenticated")

Governance: immutable after creation. No updates. If a mentor changes their decision, a new `MentorSignoff` record is created and the prior one is retained.

---

### 16. ResultStatement

The formal statement of results issued to a learner.

Key fields:
- `resultId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `programmeId` UUID FK → Programme
- `enrollmentId` UUID FK → Enrollment
- `version` integer
- `status` enum: ISSUED | AMENDED | REVOKED
- `issuedAt` timestamp
- `verificationHash` string (SHA-256 of deterministic statement fields)
- `verificationId` string (human-readable short code for verification lookups)
- `documentRef` string (PDF storage reference)
- `programmeMeta` JSONB (snapshot of programme metadata at time of issue)
- `learnerMeta` JSONB (snapshot of learner identity fields at time of issue — name, ID number)
- `createdAt`, `updatedAt`

Governance: versioned. Post-issuance amendments create a new version with `status: AMENDED`; prior versions are retained with their original `verificationHash`. Retention Class A.

---

### 17. Notification

An outbound notification record.

Key fields:
- `notificationId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User (recipient)
- `channel` enum: EMAIL | SMS
- `templateKey` string
- `templateVersion` string
- `payload` JSONB (template variables)
- `status` enum: PENDING | SENT | DELIVERED | FAILED
- `sentAt` timestamp nullable
- `deliveryConfirmedAt` timestamp nullable
- `failureReason` string nullable
- `retryCount` integer default 0
- `createdAt`, `updatedAt`

---

### 18. AuditLog

An immutable record of every privileged action on the platform.

Key fields:
- `logId` UUID PK
- `tenantId` UUID FK → Tenant nullable (null for Super Admin platform-level actions)
- `actorId` UUID FK → User
- `actorRole` string
- `action` string (e.g. "ROLE_ASSIGNMENT_CREATED", "FEATURE_FLAG_ENABLED", "RESULT_ISSUED")
- `resourceType` string (e.g. "User", "ResultStatement", "FeatureFlag")
- `resourceId` UUID nullable
- `before` JSONB nullable (state before change)
- `after` JSONB nullable (state after change)
- `ipAddress` string
- `userAgent` string
- `timestamp` timestamp

Governance: append-only. No UPDATE or DELETE. Retention Class A.

---

### 19. ConsentRecord

POPIA consent capture for each learner per tenant.

Key fields:
- `consentId` UUID PK
- `tenantId` UUID FK → Tenant
- `userId` UUID FK → User
- `consentVersion` string (version of the consent text shown)
- `capturedAt` timestamp
- `method` enum: EXPLICIT_CHECKBOX | SSO_DELEGATED
- `revokedAt` timestamp nullable
- `revocationReason` string nullable
- `ipAddress` string
- `userAgent` string

Governance: immutable after creation. Revocation creates a `revokedAt` timestamp — it does not delete the record. Retention Class A.

---

## Entity Relationship Summary

```
Tenant
  └── User
        └── RoleAssignment
        └── Enrollment → Programme → Module → LearningItem
        └── SimulationAttempt → SimulationStepEvent
        └── Submission → PeerReview
        └── Placement → LogbookEntry → MentorSignoff
        └── ResultStatement
        └── ConsentRecord
        └── Notification
  └── Rubric
  └── AuditLog
```

---

## What Not To Do

- Do not use raw email as a learner identifier in telemetry or external payloads — use `userId`
- Do not hard-delete any business record — use `deletedAt`
- Do not mutate a `SimulationStepEvent`, `AuditLog`, or `ConsentRecord` after creation
- Do not create a `ResultStatement` version by overwriting — always insert a new version row
- Do not allow a `PeerReview` where `reviewerId` equals the submission's `userId`
- Do not store `progressSnapshot` on `Enrollment` as the authoritative source — it is a cache; always recompute from events for audit and reporting
- Do not drop or ignore `curriculumOutcomeIds` arrays — an empty array is a constraint violation for any entity that requires outcome linkage
