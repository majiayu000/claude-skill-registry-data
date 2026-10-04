---
name: secrets-and-config-review
description: "Reviews secrets, config defaults, environment variables, logs, credentials, CI secrets, and unsafe settings."
---

# Secrets And Config Review

Review configuration without exposing secret values.

## Workflow

1. Inspect config keys, file metadata, templates, and redacted examples first.
2. Avoid reading secret values unless the user explicitly scopes break-glass
   handling and it is safe.
3. Check logs, docs, tests, CI, Docker files, and sample env files for leakage.
4. Verify defaults, required variables, permissions, and error behavior.
5. Report risks and minimal mitigations.

## Output

- config surfaces reviewed
- secret exposure risks
- unsafe defaults
- logging/documentation risks
- remediation
- validation gaps

## Rules

- Never print secret values.
- Do not commit or document credentials.
- Prefer key names, metadata, and redacted evidence.
