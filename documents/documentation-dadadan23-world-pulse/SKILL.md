---
name: "documentation"
description: 'Write effective documentation including inline docs, README structure, API documentation, and code comments. Use when writing README files, documenting APIs, creating architecture decision records, adding inline code documentation, or setting up documentation tooling.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Documentation

> **Purpose**: Write clear, maintainable documentation for code and APIs. 
> **Goal**: Self-documenting code, useful comments, comprehensive READMEs. 
> **Note**: For implementation, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Writing or updating README files
- Documenting APIs with OpenAPI/Swagger
- Creating architecture decision records (ADRs)
- Adding inline code documentation
- Setting up documentation tooling

## Prerequisites

- Markdown formatting knowledge

## Decision Tree

```
Documenting something?
+- New project/repo? -> README.md (setup, usage, contributing)
+- Public API?
| +- REST API -> OpenAPI/Swagger spec
| - Library -> XML docs / docstrings on all public members
+- Architecture decision? -> ADR (docs/adr/ADR-NNN.md)
+- Complex logic?
| +- WHY it works this way -> Code comment
| - HOW to use it -> Doc comment / docstring
+- Code self-explanatory?
| - Yes -> No comment needed (good naming > comments)
- Inline comment?
 +- Explains WHY (business rule, workaround) -> Keep it
 - Explains WHAT (obvious from code) -> Remove it
```

## Documentation Hierarchy

```
Documentation Pyramid:

 /\
 /API\ External API docs (OpenAPI/Swagger)
 /------\
 / README \ Project documentation
 /----------\
 / Inline Docs\ Function/class documentation
 /--------------\
 / Code Quality \ Self-documenting code (naming, structure)
/------------------\

Best Code = Minimal comments needed
```

---

## Self-Documenting Code

### Code Should Explain WHAT

```
[FAIL] Bad: Needs comment to understand
 # Check if user can access
 if u.r == 1 or u.r == 2:
 return True

[PASS] Good: Self-explanatory
 if user.role == Role.ADMIN or user.role == Role.MODERATOR:
 return True

[PASS] Better: Extract to function
 if user.hasModeratorPermissions():
 return True
```

### Names Should Be Descriptive

```
Variables:
 [FAIL] d, tmp, data, x
 [PASS] daysSinceLastLogin, userCount, orderTotal

Functions:
 [FAIL] process(), handle(), do()
 [PASS] calculateShippingCost(), validateEmailFormat(), sendWelcomeEmail()

Classes:
 [FAIL] Manager, Handler, Processor, Helper
 [PASS] OrderRepository, EmailValidator, PaymentGateway
```

---

## Best Practices Summary

| Practice | Description |
|----------|-------------|
| **Code first** | Write self-documenting code before adding comments |
| **Document why** | Explain intent, not mechanics |
| **Keep updated** | Wrong docs are worse than no docs |
| **Examples** | Show, don't just tell |
| **Audience** | Write for the reader, not yourself |
| **Minimal** | Document what's needed, no more |
| **Accessible** | Store docs near the code |
| **Versioned** | Docs in repo, not external wikis |

---

**See Also**: [API Design](../../architecture/api-design/SKILL.md) - [C# Development](../csharp/SKILL.md) - [Python Development](../python/SKILL.md)

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`generate-readme.py`](scripts/generate-readme.py) | Auto-generate README.md from project metadata | `python scripts/generate-readme.py [--output README.md]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Documentation out of sync with code | Generate API docs from code annotations, add doc validation to CI |
| README too long | Split into separate docs/ files, link from README |
| Missing API documentation | Add doc comments to all public APIs, generate with Swagger/Redoc |

## References

- [Inline Docs Comments](references/inline-docs-comments.md)
- [Readme Templates](references/readme-templates.md)
- [Api Architecture Docs](references/api-architecture-docs.md)