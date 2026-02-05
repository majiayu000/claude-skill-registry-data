---
name: project-standards
description: Provides project coding standards and architectural principles on-demand. Automatically invoked when implementing features, writing code, or making technical decisions. Reads constitution.md to ensure all code aligns with project principles.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Project Standards Skill

You are implementing code in a project that follows specific architectural principles and coding standards defined in the **project constitution**.

## When to Invoke This Skill

Claude should use this skill when:
- Writing or modifying code
- Making architectural decisions
- Implementing tasks from tasks.md
- Reviewing code for compliance
- Setting up new components or services

## How to Use

1. **Read the constitution** to understand project principles:
   ```
   Read: .specify/memory/constitution.md
   ```

2. **Apply principles** during implementation:
   - TDD: Write tests first, ensure they fail, then implement
   - SOLID: Follow single responsibility, dependency injection
   - Security: No hardcoded secrets, validate all inputs
   - Observability: Add logging, metrics, tracing

3. **Check compliance** before marking tasks complete

## Key Principles Summary

### Test-Driven Development (TDD)
- Write tests BEFORE implementation code
- Tests must FAIL initially (Red phase)
- Implement to make tests pass (Green phase)
- Refactor after passing (Refactor phase)
- 100% test pass rate required (enforced by test-gate.sh)

### SOLID Architecture
- **S**ingle Responsibility: One reason to change per class/module
- **O**pen/Closed: Extend via interfaces, don't modify
- **L**iskov Substitution: Implementations substitutable for abstractions
- **I**nterface Segregation: Many focused interfaces
- **D**ependency Inversion: Depend on abstractions, inject implementations

### Security-First
- Secrets in environment variables or secret managers only
- Input validation with strict schemas (Pydantic, Zod)
- Parameterized queries only (no string interpolation for SQL)
- Row-Level Security (RLS) for multi-tenant data
- Rate limiting on all API endpoints

### Code Quality
- Type hints/annotations required
- Linting must pass (ruff, ESLint)
- Docstrings for public APIs
- Meaningful variable/function names

### Observability
- Structured JSON logging with correlation IDs
- Health check endpoints (/health, /ready, /live)
- Metrics for critical operations
- Distributed tracing for cross-service calls

## Integration with Sub-Agents

When working as a specialized sub-agent:

### For backend-api-engineer
- Read constitution for API versioning rules
- Apply security requirements to endpoints
- Follow TDD for all endpoint implementations

### For frontend-react-engineer
- Read constitution for accessibility requirements
- Apply performance budgets
- Follow component architecture patterns

### For openapi-spec-author
- Read constitution for API stability rules
- Ensure backward compatibility
- Follow versioning strategy

### For integration-tester
- Read constitution for test coverage requirements
- Verify compliance with success criteria
- Check observability is in place

## Quick Reference

Before implementing, ask yourself:
1. Did I write the test first? (TDD)
2. Is this class doing only one thing? (SRP)
3. Are secrets externalized? (Security)
4. Is there logging/metrics? (Observability)
5. Are inputs validated? (Security)
6. Does this align with the constitution? (Compliance)

## Full Constitution Access

For complete details, read:
```
.specify/memory/constitution.md
```

This contains:
- All 8 core principles with detailed requirements
- Security requirements and data protection rules
- Compliance standards (SOC 2, HIPAA, GDPR)
- Performance targets and SLOs
- Development workflow and CI/CD gates
