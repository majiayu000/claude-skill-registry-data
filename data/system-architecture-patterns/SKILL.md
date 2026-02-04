---
name: "System Architecture Patterns"
description: "Apply proven architectural patterns (MVC, layered, microservices) to create maintainable systems with clear separation of concerns"
category: "architecture"
required_tools: ["Read", "Write", "Grep", "Glob"]
---

# System Architecture Patterns

## Purpose
Apply proven architectural patterns to create maintainable, scalable systems with clear separation of concerns and well-defined component responsibilities.

## When to Use
- Designing new systems or major features
- Refactoring existing architecture
- Solving common architectural challenges
- Organizing complex codebases

## Key Capabilities
1. **Pattern Selection** - Choose appropriate patterns for the problem
2. **Component Design** - Define clear boundaries and responsibilities
3. **Integration Planning** - Design how components communicate

## Approach
1. Understand the problem domain and requirements
2. Identify architectural concerns (scalability, maintainability, etc.)
3. Select patterns that address those concerns
4. Define component boundaries and interfaces
5. Document pattern application and rationale

## Example
**Context**: Web application with business logic and data access

**Pattern**: Layered Architecture
````
Presentation Layer (UI)
    ↓
Business Logic Layer (Services)
    ↓
Data Access Layer (Repositories)
    ↓
Database
````

**Benefits**:
- Clear separation of concerns
- Easy to test each layer independently
- Can swap implementations (e.g., different databases)

## Best Practices
- ✅ Choose patterns that solve actual problems
- ✅ Document why you chose each pattern
- ✅ Keep it simple - don't over-architect
- ❌ Avoid: Using patterns just because they're popular