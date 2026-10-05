---
name: security-hardening
description: "Use this skill for auth boundaries, input validation, secrets, RLS, injection risks, destructive-action review. Trigger when the task involves security work related to Security Hardening, production implementation, audits, debugging, strategy, or validation."
---

# Security Hardening

Use this skill to handle Security tasks focused on auth boundaries, input validation, secrets, RLS, injection risks, destructive-action review.

## Workflow

1. Clarify the user outcome, constraints, current stack, and definition of done.
2. Inspect the local repository or provided artifacts before proposing changes.
3. Check official documentation when APIs, platform rules, SDK versions, policies, or production behavior may have changed.
4. For non-trivial choices, compare proven open-source patterns or examples and adapt ideas without copying incompatible code.
5. Implement the smallest production-ready change that satisfies the request.
6. Validate with the most relevant checks: tests, lint, typecheck, build, browser/device review, audits, or manual scenario.
7. Report changed files, commands run, remaining risks, and exact next steps.

## Focus Checklist

- Define scope and assumptions explicitly.
- Prefer existing project conventions and tools.
- Handle loading, empty, error, permission, and edge states where relevant.
- Include security, privacy, performance, accessibility, and rollback considerations when they apply.
- Keep output actionable and evidence-backed.

## Guardrails

- Do not disable security controls or expose secrets without explicit user confirmation.
- Do not perform destructive, paid, production, trading, publishing, or account-changing actions without explicit user confirmation.
- Do not expose secrets, private keys, tokens, cookies, personal data, or confidential business data.
- If validation is impossible, state exactly why and provide a manual verification path.
