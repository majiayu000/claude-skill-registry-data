---
name: secrets-scan-remediation
description: Triage detected credential leaks, revoke exposed secrets safely, remove tracked copies, and verify history/log exposure boundaries.
---

# Secrets Scan Remediation

## Goal

Contain a potential secret exposure without leaving usable credentials active or deleting evidence needed for incident response.

## Inputs to inspect

Scanner finding, repository/file history, credential owner/provider, deployment references, and distribution/log context.

## Workflow

1. Validate the finding without echoing the secret; identify likely credential type, provider, scope, last known use, and exposure locations.
2. Prioritize containment by revoking/rotating the credential with its owner and checking for suspicious use before treating repository cleanup as sufficient.
3. Search the current tree, branches, artifacts, CI logs, package output, and deployment configuration for related copies while redacting values from reports.
4. Remove or replace tracked values with a secret manager/environment reference; update consuming systems and validate that the rotated value works without exposing it.
5. Determine whether history/artifacts require coordinated cleanup, preserve incident evidence securely, and add prevention checks such as secret scanning or push protection.

## Validation checklist

- [ ] The exposed credential is revoked/rotated, not merely hidden in a later commit.
- [ ] Search results and reports do not reproduce the secret value.
- [ ] All known consumers are updated and tested after rotation.
- [ ] History rewriting is coordinated and does not destroy required incident evidence.
- [ ] A regression gate prevents the same class of secret from being committed again.

## Required output

Produce a redacted incident record, affected surface inventory, rotation status, consumer validation, history/artifact decision, and prevention actions.

## Boundaries and failure handling

Do not paste the secret into chat/logs; do not assume deleting a file from the latest commit makes the credential safe.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
