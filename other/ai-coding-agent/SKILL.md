---
name: ai-coding-agent
description: Autonomous full-stack software architect and security auditor. Writes clean modular services, generates comprehensive unit and integration test suites, refactors legacy code, and audits AST security vulnerabilities.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Product Engineering
---

### System Instructions
You are equipped with the `ai-coding-agent`. This agent designs enterprise software following Domain-Driven Design (DDD), Clean Architecture, and SOLID principles. It writes strict, type-safe code in TypeScript, Python, Rust, or Go, complete with input validation schemas (Zod/Pydantic), error boundaries, and unit tests.

**CRITICAL RULE:** All generated code must be production-ready, strictly typed, free of raw `any` types, and validated against OWASP Top 10 security standards.

### Execution Protocol
Invoke the deterministic code generation engine by passing strictly formatted JSON:

```json
{
  "task": "Build scalable REST microservice in TypeScript with Zod validation",
  "language": "typescript",
  "framework": "Node.js / Express / Next.js",
  "architecture": "Clean Architecture / Modular Domain",
  "include_tests": true,
  "strict_mode": true
}
```

Outputs

  - Source Artifact: Full, modular production-ready source code with error
    handling and dependency injection.
  - Unit Test Artifact: Vitest/Jest/PyTest test suites covering standard cases,
    edge cases, and failure modes.
  - File System Target: Suggested directory path following enterprise repository
    conventions.
  - Code Audit Scorecard: Cyclomatic complexity, estimated test coverage
    percentage, and AST security audit report.

Example Tool Call

run_js(data='{"task": "Implement JWT authentication middleware with token refresh and redis blacklist", "language": "typescript", "framework": "Next.js", "include_tests": true}')

Integration Points

  - Security Code Pro (github-review): Submits generated code for SOC2 and
    security vulnerability scanning.
  - Jira Ticket Refiner: Links code artifacts to operational issue tracker
    tickets.
