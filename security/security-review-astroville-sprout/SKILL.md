---
name: security-review
description: Security review guidance for trust boundaries, auth, input handling, secret exposure, and meaningful application risk.
compatibility: opencode
metadata:
  audience: security
  purpose: review-guidance
---
## Core approach

- Focus on meaningful security risk, not checkbox compliance language.
- Review trust boundaries, data exposure, authn/authz paths, and risky defaults.
- Prioritize concrete findings by severity and exploitability.
- Distinguish confirmed issues from areas needing more evidence.

## Practical guidance

- Examine authentication, authorization, secrets, injection surfaces, deserialization, file handling, external calls, and dependency risk where relevant.
- Consider both code-level issues and operational exposure.
