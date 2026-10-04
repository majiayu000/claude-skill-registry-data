---
name: thalarch-security
description: >
  Performs evidence-backed application and agentic-workflow security review. Use for auth,
  authorization, untrusted input, secrets, cryptography, network exposure, command execution,
  file/path handling, dependencies, GitHub Actions, MCP/tool integrations, or any explicit
  security audit. Trace sources to sinks and confirm findings to reduce false positives.
---

# Thalarch Security

## Security Lens

Security review is threat-model driven, not keyword matching.

## Establish trust boundaries

Identify:
- attacker/user-controlled input;
- privileged operations;
- credentials/secrets;
- filesystem/process/network sinks;
- authentication and authorization decisions;
- external service/tool boundaries;
- CI/event inputs.

## Trace data flows

For a suspected vulnerability, trace actual source → transformations → sink.

Check, when applicable:
- injection;
- path traversal;
- SSRF;
- insecure deserialization;
- authz bypass;
- secret exposure;
- unsafe cryptography/randomness;
- over-privileged tokens;
- dependency risk;
- prompt/tool injection in agentic workflows;
- dangerous CI triggers or untrusted PR data.

## Findings

No finding without a credible attack path or violated security contract.

Separate:
- exploitable;
- defense-in-depth;
- hardening;
- unknown due missing evidence.

Never print secret values in reports.

Require human approval before applying security-sensitive changes that may alter
access control, credential handling, or external permissions.
