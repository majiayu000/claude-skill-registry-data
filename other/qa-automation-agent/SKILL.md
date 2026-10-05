---
name: qa-automation-agent
description: "Use this skill for test strategy, E2E automation, visual regression, flaky test control, QA evidence. Trigger when the task involves agent profile work related to Qa Automation Agent, implementation, audits, debugging, strategy, or validation."
---

# Qa Automation Agent

Use this skill for Agent Profile tasks focused on test strategy, E2E automation, visual regression, flaky test control, QA evidence.

## Workflow

1. Clarify the user outcome, constraints, current stack, and definition of done.
2. Inspect local source, artifacts, analytics exports, logs, designs, or docs before changing anything.
3. Check official documentation when APIs, SDKs, policies, search behavior, accessibility rules, or production behavior may have changed.
4. Compare proven open-source patterns for non-trivial choices and adapt ideas without copying incompatible code.
5. Produce the smallest production-ready change or recommendation that satisfies the request.
6. Validate with relevant evidence: tests, lint, typecheck, build, screenshots, crawl output, logs, analytics, or manual scenario.
7. Report commands, files, findings, risks, and next steps clearly.

## Focus Checklist

- Map inputs, owners, dependencies, and constraints.
- Prefer existing project conventions, design systems, and platform primitives.
- Include failure states, privacy/security implications, performance impact, and rollback where relevant.
- Separate facts from assumptions and mark any unverified claims.
- Keep recommendations actionable and prioritized by impact and risk.

## Guardrails

- Do not mark flows verified without running tests or documenting manual evidence.
- Do not perform destructive, paid, production, publishing, account-changing, or externally visible actions without explicit user confirmation.
- Do not expose secrets, private keys, tokens, cookies, private analytics, personal data, or confidential business data.
- If validation is impossible, state why and provide a concrete manual verification path.
