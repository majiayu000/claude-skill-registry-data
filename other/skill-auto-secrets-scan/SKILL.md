---
name: skill-auto-secrets-scan
description: "Scans proposed skill changes and reports for likely credentials or sensitive literals. Use before committing a batch or publishing a package."
---

# Automated Skill Secret Scan

## Purpose

diff, files in scope, secret patterns, allowlist policy, and suppression process

## Required inputs

Run approved secret scanners on added and modified files, including examples, fixtures, and docs.

## Workflow

1. Inspect the canonical source, current repository rules, and the exact change request before taking action.
2. Validate findings against context without printing or reproducing secret values; block credible leaks and request secure remediation.
3. A secret-scan report with redacted findings and blocking status.
4. Verify behavior with positive and negative fixtures and record skipped runtime checks, unresolved evidence, or required human decisions.
5. Produce never copy detected secret values into issue comments, logs, or review output. tied to the exact candidate version/digest and request ID.

## Validation checklist

- [ ] Scope and expected change are documented before generating or accepting output.
- [ ] Existing neighboring skills and repository policy are considered.
- [ ] Positive and negative cases are explicit and failures are not described as successes.
- [ ] Security, provenance, compatibility, and rollback requirements are handled where relevant.
- [ ] Unexecuted checks and required approvals remain visibly pending.

## Required output

Never copy detected secret values into issue comments, logs, or review output.

## Boundaries and failure handling

An agent generated configuration examples or request payloads for a broker skill. If required evidence or approval is missing, stop promotion and return a precise blocker. Never write directly to the protected main branch through this skill.

## Trigger examples

- **Positive:** The changed artifact contains no content and there is nothing to scan.
- **Negative:** undefined
