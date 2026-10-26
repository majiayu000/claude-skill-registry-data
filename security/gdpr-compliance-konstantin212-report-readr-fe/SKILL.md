---
name: gdpr-compliance
description: Use when handling PII or financial data — checklist against BDSG/GDPR.
---

# GDPR / BDSG Compliance (reference)

## Lawful basis & purpose limitation (§24 BDSG)

- Every processing of personal data needs a lawful basis and a stated purpose;
  don't repurpose data collected for one purpose (e.g. tax reporting) for an
  unrelated one without a new basis.

## Data minimization & accuracy (§47 BDSG)

- Collect and retain only what's needed for the stated purpose. Keep it
  accurate and correct/erase what's wrong.

## Access rights (§34 BDSG)

- Data subjects have a right to access their data, subject to documented
  exceptions — know what those exceptions are before refusing a request.

## Erasure vs. statutory tax-retention conflict (§35, §47 no.5 BDSG)

- Erasure requests must be reconciled against **mandatory tax-record
  retention** obligations — you generally cannot delete records still under a
  statutory retention period, even on request. Flag this conflict explicitly
  rather than either silently deleting or silently refusing.

## Consent (§26 BDSG)

- Where processing relies on consent, provide a clear consent mechanism and an
  equally clear way to withdraw it.

## Security (§22(2) BDSG)

- Encryption, pseudonymization, access control, and audit logging are expected
  technical/organizational measures for personal/financial data.

## Staff confidentiality (§52–53 BDSG)

- Anyone with access to personal data is bound to confidentiality.

## Breach notification (Arts 33–34 GDPR)

- Notify the supervisory authority (and affected individuals, where required)
  on a qualifying breach within the mandated timelines.

## DPO threshold (§38 BDSG)

- Know the threshold at which a Data Protection Officer is legally required and
  don't assume it doesn't apply.

## DPIA trigger

- Large-volume processing of sensitive financial data is a trigger for a Data
  Protection Impact Assessment — treat new features touching bulk financial/PII
  data as a DPIA candidate, not an afterthought.

---
Source: gesetze-im-internet.de/englisch_bdsg
