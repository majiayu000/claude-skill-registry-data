---
name: security-review
description: Use for application security review covering OWASP-style categories, secrets, auth boundaries, dependency risk handoffs, and prompt-injection escalation.
when_to_use: Use when code or configuration changes affect secrets, auth, dependencies, untrusted input, network calls, file access, or security-sensitive prompts.
---

# Security Review

Apply the checklist in `references/checklist.md`. Keep findings evidence-first and classify severity as Critical, High, Medium, Low, or Info.

Dependency tool execution is owned by `dependency-audit` when shell access is needed. Prompt-construction issues must also invoke `prompt-safety-review`.
