---
name: application-form-helper
description: Use when a user wants a resume mapped into a Chinese online application form, fields completed in a careers portal, open questions drafted, or missing and conflicting values identified while keeping final submission under user control.
---

# Application Form Helper

Map verified resume data to the current application form and fill reversible fields safely.

## Preparation

Read the shared [candidate contract](../../shared/references/candidate-profile-schema.md), [application record](../../shared/references/application-record-schema.md), [Chinese ATS patterns](../../shared/references/chinese-ats-patterns.md), [browser safety rules](../../shared/references/browser-safety.md), and [output contract](../../shared/references/output-contracts.md).

## Workflow

1. Inspect all visible sections and required fields before filling. Record platform, role, and application state.
2. Map each field to a candidate source. Treat internships as internships and projects as projects.
3. Classify each value as exact, transformed, inferred, missing, or conflicting.
4. Fill exact and safely transformed values. For populated conflicts, preserve the existing value and surface the conflict unless the user directs otherwise.
5. Draft open questions from verified experience and the target JD. Do not fabricate game history, language scores, salary, availability, identity, or eligibility.
6. Validate dates, degree order, phone/email format, character limits, required attachments, and automatic line wrapping.
7. Stop before final submission and present the review checklist in [form-review.md](references/form-review.md).
8. After user-confirmed submission or a later recruitment event, append evidence to the application record. Deduplicate by company and requisition; never infer assessment, interview, offer, or rejection from a generic receipt.

## Application Tracking

Track `planned`, `submitted`, `screening`, `assessment`, `interview`, `offer`, `rejected`, `withdrawn`, and `unknown`. Preserve the event history, next action, deadline, and local artifact references. Never store passwords, verification codes, identity numbers, or hidden session data.

## Mandatory Stops

The user must handle or explicitly confirm login challenges, CAPTCHA, identity verification, legal declarations, consent with material consequences, and final submit/apply actions. Never bypass platform controls.
