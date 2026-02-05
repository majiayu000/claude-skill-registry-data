---
name: anti-pattern-analysis
description: Systematic detection of anti-patterns during code review with actionable refactoring guidance
---

# Anti-Pattern Analysis Skill
**Version:** 0.17.0

## Purpose
Structured guidance for identifying anti-patterns across languages, architectures, and testing. Supports code reviews, refactoring planning, technical debt assessment, and reverse-PRD workflows.

## When to Invoke
- Code review sessions
- Refactoring planning
- Technical debt assessment
- Architecture review
- Reverse-PRD extraction (document as tech debt/NFRs)

## Anti-Pattern Categories

### 1. Design/OOP
| Pattern | Description | Severity |
|---------|-------------|----------|
| **God Object** | Class >500 lines or >10 methods | High |
| **Singleton Abuse** | Overuse creating global state | Medium |
| **Anemic Domain Model** | Data classes with no behavior | Medium |
| **Circular Dependency** | Classes depend on each other | High |
| **Yo-yo Problem** | Deep inheritance requiring navigation | Medium |

### 2. Code Smells
| Pattern | Description | Severity |
|---------|-------------|----------|
| **Long Method** | >20-30 lines | Medium |
| **Deep Nesting** | >3 levels indentation | Medium |
| **Magic Numbers** | Unexplained literals | Low |
| **Feature Envy** | Method uses another class's data excessively | Medium |
| **Shotgun Surgery** | One change requires many edits | High |
| **Divergent Change** | One class changed for many reasons | High |

### 3. Architecture
| Pattern | Description | Severity |
|---------|-------------|----------|
| **Big Ball of Mud** | No discernible architecture | Critical |
| **Distributed Monolith** | Microservices with tight coupling | High |
| **Copy-Paste Programming** | Duplicated code blocks | High |
| **Spaghetti Code** | Tangled control flow | High |
| **Lasagna Code** | Too many abstraction layers | Medium |

### 4. Database
| Pattern | Description | Severity |
|---------|-------------|----------|
| **N+1 Queries** | Loop executing individual queries | Critical |
| **SELECT *** | Fetching all columns unnecessarily | Medium |
| **EAV Schema** | Flexible but unqueryable | High |
| **No Indexes** | Missing indexes on queried columns | High |
| **God Table** | Table with too many columns | High |

### 5. Testing
| Pattern | Description | Severity |
|---------|-------------|----------|
| **Flaky Tests** | Non-deterministic results | Critical |
| **Test Interdependence** | Tests depend on order | High |
| **Over-Mocking** | Mocking makes test meaningless | High |
| **Testing Implementation** | Tests break on refactor | Medium |
| **Happy Path Only** | No edge case testing | Medium |

### 6. Security
| Pattern | Description | Severity |
|---------|-------------|----------|
| **Hardcoded Secrets** | Credentials in source | Critical |
| **SQL Concatenation** | String-built queries | Critical |
| **Trust All Input** | No input validation | Critical |
| **Rolling Own Crypto** | Custom cryptography | Critical |
| **Missing Authentication** | Endpoints without auth | Critical |

## Severity Levels
| Level | Impact | Action |
|-------|--------|--------|
| **Critical** | Security/data loss risk | Must fix before merge |
| **High** | Major tech debt | Fix in same PR/sprint |
| **Medium** | Code smell | Create follow-up issue |
| **Low** | Minor improvement | Optional |

## Quick Review Checklist
**Design:** No God objects, no circular deps, SRP followed
**Code:** Methods <30 lines, nesting <4 levels, no magic numbers
**Database:** No N+1, no SELECT *, indexes exist, parameterized queries
**Testing:** Deterministic, independent, reasonable mocking
**Security:** No hardcoded secrets, input validated, auth on endpoints

## Refactoring Guidance
- **God Object** → Extract to focused services
- **Long Method** → Extract method
- **N+1 Query** → Eager loading/prefetch
- **Magic Numbers** → Named constants
- **Deep Nesting** → Guard clauses

## Reverse-PRD Integration
Detection maps to NFR categories:
- Security → NFR-SEC-*
- Performance → NFR-PERF-*
- Maintainability → NFR-MAINT-*
- Testing → NFR-QUAL-*
- Architecture → NFR-ARCH-*

---

**End of Skill Document**
