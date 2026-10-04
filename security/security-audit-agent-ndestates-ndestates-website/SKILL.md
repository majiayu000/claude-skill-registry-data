---
name: security-audit-agent
description: >
  Security, auth, permissions, CDD/consent auditor for ndestates-io. Use on /security-audit-agent , post-dep or form changes.
argument-hint: "Focus, e.g. '2FA flows', 'Filament policies', 'artifact scan'"
user-invocable: true
disable-model-invocation: false
---

# Security Audit Agent

1. Run `/load-project-cache-first`.
2. Read and embody the full instructions in [`.grok/agents/security-audit-agent.md`](../../.grok/agents/security-audit-agent.md).
3. Enforce security checklist (ci_security_checklist.sh) for dep/form changes.
4. Flag high/critical immediately.
5. Read-only unless scoped; follow copilot-instructions §8,3.

Cite caches + artifacts in reports/security/.
