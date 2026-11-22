---
name: ecc
description: Everything Claude Code (ECC) harness toolkit for AI coding agents. Use when orchestrating complex workflows, enforcing coding standards, executing multi-role architecture reviews, continuous verification, or navigating the ECC library of playbooks and agents.
---

# ECC (Everything Claude Code) Toolkit

ECC is a comprehensive agent harness operating layer and developer toolkit that enhances coding assistant capabilities with structured workflows, agent roles, coding rules, and quality gates.

## Core Capabilities in This Workspace

This project has been initialized with the ECC Antigravity adapter supporting:

1. **Language & Framework Rules** (`.agents/rules/`):
   - **FastAPI / Python**: Performance patterns, testing standards with pytest, security rules.
   - **TypeScript / React**: Modern component patterns, type safety, state management guidelines.
   - **Common Engineering**: Code review standards, git workflow, accessibility, performance budgets.

2. **Specialized Agent Roles** (`.agents/agents/`):
   - `architect.md` & `code-architect.md`: System design and modular decomposition.
   - `code-reviewer.md`: Rigorous code quality and convention auditing.
   - `build-error-resolver.md`: Automated compile and syntax diagnostic resolution.
   - `a11y-architect.md`: Accessibility and WCAG compliance reviews.
   - `security-reviewer.md`: Vulnerability analysis and safety gates.

3. **Key ECC Workflows & Skills** (`.agents/skills/`):
   - `ecc-guide`: Detailed live exploration of the full ECC ecosystem.
   - `ecc-recipes`: Ready-to-use recipes for common development workflows.
   - `unified-memory`: Cross-session memory and context persistence.
   - `verification-loop`: Automated testing and verification loops before code delivery.
   - `tdd-workflow`: Test-driven development loop (Red -> Green -> Refactor).
   - `delivery-gate`: Quality checks ensuring tests, linting, and build pass before merging.

## Quick Runbooks

### 1. Code Review Loop
Before committing substantial changes:
1. Review modified files against `.agents/rules/common-code-review.md`.
2. Check security invariants in `.agents/rules/python-security.md` and `.agents/rules/typescript-security.md`.
3. Run backend tests: `py -3.11 -m pytest backend/tests/`.
4. Run frontend build: `npm run build --prefix frontend`.

### 2. Feature Implementation
1. **Design**: Check `.agents/rules/common-patterns.md` and appropriate architecture guidelines.
2. **Implement**: Keep code modular, preserve comments, follow repository conventions.
3. **Verify**: Use the verification loop to ensure all tests pass.
