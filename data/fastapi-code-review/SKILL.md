---
name: fastapi-code-review
description: Comprehensive code review skill for FastAPI projects. Analyzes codebase against industry best practices covering async patterns, project structure, Pydantic usage, dependency injection, database patterns, testing, and performance. Generates detailed refactor plans with prioritized recommendations. Use when reviewing FastAPI projects, auditing code quality, planning refactors, or ensuring adherence to FastAPI/async best practices.
---

# FastAPI Code Review

Perform comprehensive code reviews of FastAPI projects against industry best practices, identifying violations and generating actionable refactor plans.

## Review Process

### 1. Gather Project Context

Before reviewing, collect information about the project:

```
- Project structure (list_dir on root and key directories)
- Main application entry point (typically main.py or app.py)
- Router definitions and API endpoints
- Pydantic models/schemas
- Database models and connections
- Dependencies and middleware
- Configuration management
- Test files
```

### 2. Execute Review Checklist

Evaluate each category against the best practices in [references/best-practices.md](references/best-practices.md).

**Review Categories:**

1. Project Structure
2. Async/Sync Patterns
3. Pydantic Usage
4. Dependency Injection
5. API Design (REST)
6. Database Patterns
7. Testing Patterns
8. Configuration Management
9. Performance Optimizations
10. Documentation

### 3. Generate Refactor Plan

For each violation found, document:

```markdown
## Refactor Plan

### Critical Issues (Fix Immediately)
| Issue | Location | Best Practice Violated | Refactor Action |
|-------|----------|------------------------|-----------------|
| ... | ... | ... | ... |

### High Priority (Fix Soon)
| Issue | Location | Best Practice Violated | Refactor Action |
|-------|----------|------------------------|-----------------|
| ... | ... | ... | ... |

### Medium Priority (Plan for Refactor)
| Issue | Location | Best Practice Violated | Refactor Action |
|-------|----------|------------------------|-----------------|
| ... | ... | ... | ... |

### Low Priority (Nice to Have)
| Issue | Location | Best Practice Violated | Refactor Action |
|-------|----------|------------------------|-----------------|
| ... | ... | ... | ... |
```

## Quick Reference: Common Violations

### Critical (Blocking Event Loop)

- `time.sleep()` in async routes → Use `asyncio.sleep()` or make route sync
- Sync database calls in async routes → Use async database drivers
- Sync HTTP calls in async routes → Use `httpx.AsyncClient`

### High Priority (Performance/Security)

- Missing indexes on frequently queried columns
- N+1 query patterns
- Hardcoded secrets → Use environment variables
- Missing rate limiting on public endpoints
- `SELECT *` queries → Select only needed columns

### Medium Priority (Maintainability)

- God routers with too many endpoints → Split by domain
- Missing dependency injection for validation
- Sync dependencies in async context
- No custom base Pydantic model
- Missing type hints

### Low Priority (Polish)

- Missing OpenAPI documentation
- Inconsistent naming conventions
- Missing pre-commit hooks with ruff

## Output Format

Generate a comprehensive review report:

```markdown
# FastAPI Code Review Report

## Executive Summary
- **Project**: [name]
- **Review Date**: [date]
- **Overall Health**: [Critical/Needs Work/Good/Excellent]
- **Total Issues Found**: [count]

## Metrics
| Category | Status | Issues |
|----------|--------|--------|
| Project Structure | ✅/⚠️/❌ | X |
| Async Patterns | ✅/⚠️/❌ | X |
| Pydantic Usage | ✅/⚠️/❌ | X |
| Dependencies | ✅/⚠️/❌ | X |
| API Design | ✅/⚠️/❌ | X |
| Database | ✅/⚠️/❌ | X |
| Testing | ✅/⚠️/❌ | X |
| Configuration | ✅/⚠️/❌ | X |
| Performance | ✅/⚠️/❌ | X |
| Documentation | ✅/⚠️/❌ | X |

## Detailed Findings
[Per-category breakdown with code examples]

## Refactor Plan
[Prioritized action items]

## Recommendations
[Strategic improvements beyond immediate fixes]
```

## Reference

For detailed best practices and code examples, see [references/best-practices.md](references/best-practices.md).
