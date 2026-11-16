---
name: kit-feature-implementation
description: Implement a new feature or behavior change end to end, tracing requirements through design, code, tests, and verification. Use when the user asks to add, build, or change functionality that spans more than a trivial edit. Do not use for bug diagnosis, code review, one-line changes, or work that a more specific installed kit skill covers, such as React components (kit-react-component), framework endpoints (kit-fastify-api, kit-fastapi-api, kit-go-http-api), changes across several packages of a monorepo (kit-monorepo-change), or requests to delegate or coordinate build, tests, docs, and review (kit-orchestrate).
---

# Feature implementation

## 1. Clarify requirements

- Restate the requirement as observable behavior: inputs, outputs, errors, and who uses it.
- Identify acceptance criteria and edge cases. Ask about genuinely ambiguous decisions that would change the design; otherwise choose the conventional option and state the assumption.

## 2. Explore before designing

- Find where similar features live and how they are structured: routing, services, data access, validation, error handling, configuration, and tests.
- Identify existing utilities and patterns to reuse.
- Note constraints: public APIs, stored data formats, migrations, permissions, and performance-sensitive paths.

## 3. Plan

- Outline the changes file by file, including tests and any migrations or documentation.
- For changes to public interfaces or stored data, describe compatibility and rollout.
- For large or risky changes, share the plan with the user before implementing.

## 4. Implement

- Work in small, verifiable steps. Keep the code consistent with surrounding conventions.
- Validate input at boundaries and handle errors explicitly.
- Add tests for the new behavior, edge cases, and failure paths alongside the code.
- Do not refactor unrelated code or add speculative abstractions.

## 5. Verify and report

- Run the relevant tests, type checks, linters, and build.
- Check each acceptance criterion against the result.
- Report what changed, how it was verified, assumptions made, and any follow-up work. Do not deploy, migrate production data, or publish without explicit instruction.

## Examples

- Use: "Add CSV export to the reports page." "Support API keys in addition to session auth."
- Skip: "Fix the null pointer in the parser." (debugging) "Rename this variable." (trivial edit) "Add currency to the shared money package and use it in billing." (kit-monorepo-change, if installed)
