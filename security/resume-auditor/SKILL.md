---
name: resume-auditor
description: Use when a user wants to audit a resume for unsupported claims, inflated ownership, inconsistent dates or metrics, weak evidence, risky wording, or interview credibility before applying.
---

# Resume Auditor

Audit the resume as atomic claims. Improve accuracy and interview defensibility without judging the candidate or collecting unrelated personal information.

## Inputs

Require the resume or proposed copy. Use the shared [candidate profile](../../shared/references/candidate-profile-schema.md), [claim ledger](../../shared/references/claim-ledger-schema.md), and [output contracts](../../shared/references/output-contracts.md). Public research is optional and must remain directly relevant to a claim.

## Workflow

1. Split role, ownership, action, outcome, metric, causality, and timeline statements into separate claims.
2. Assign stable source and claim IDs. Distinguish `source_grounded`, `user_attested`, `inferred`, `planned`, and `unknown`.
3. Check the resume against itself before researching externally: dates, overlapping commitments, titles, metric arithmetic, baselines, denominators, time windows, and inconsistent versions.
4. Check `owner`, `lead`, `core author`, `architect`, `0-to-1`, `first`, and `largest` against demonstrated scope. Narrow wording when evidence supports only a module or contribution.
5. Separate project-wide adoption, stars, revenue, or performance from the candidate's attributable result.
6. For open source, distinguish issue, open PR, closed PR, merged PR, contributor, committer, and maintainer. Repository popularity is not personal impact.
7. Return [the audit output](references/audit-output.md), corrected copy, and evidence that would change each unresolved result.

## Boundaries

- Do not search for addresses, phone numbers, family information, credentials, private messages, or unrelated personal history.
- A missing public record is not proof that an internal project or employment claim is false.
- Describe the evidence state, not the person's character or motives.
- Present material evidence for and against a claim with equal care.
- Never turn `user_attested` into `source_grounded` without a supporting source.

For JSON, run `python3 scripts/validate_claim_ledger.py /path/to/claim-ledger.json` before handoff.

