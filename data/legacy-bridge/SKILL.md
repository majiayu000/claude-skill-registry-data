---
name: legacy-bridge
description: Backward compatibility bridge that translates legacy @load patterns to new Skills format. Enables seamless migration with zero breaking changes during 6-month transition period.
---

# Legacy Bridge

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start) (5 min) → Level 2: [Implementation](#level-2-implementation) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start

### Overview

The legacy-bridge skill provides backward compatibility for existing `@load` patterns used in CLAUDE.md and the product-matrix system. This bridge enables a zero-breaking-change migration path from the legacy standards loader to the new Skills-based architecture.

**Migration Timeline**: 6-month transition period (deprecation warnings only, no breaking changes)

### When to Use

Use this skill when:

- You have existing code using `@load product:*` patterns
- You need to maintain backward compatibility during migration
- You want to gradually transition to the new Skills format

### Quick Reference

| Legacy Pattern | New Skill Loading |
|----------------|-------------------|
| `@load product:api` | `skill-loader.py load product:api` |
| `@load CS:python` | `skills/coding-standards/python` |
| `@load SEC:*` | `skills/security/*` + NIST baseline |

---

## Level 2: Implementation

### Pattern Translation

The legacy-bridge automatically translates old `@load` patterns to new skill loads:

#### Product Type Patterns

```bash
# Old Pattern → New Skill Loading
@load product:api         → Load: [coding-standards, testing, security, devops]
@load product:web-service → Load: [coding-standards, testing, security, frontend, devops]
@load product:frontend-web → Load: [frontend, testing, security]
```

#### Standard Code Patterns

```bash
# Coding Standards (CS)
@load CS:python       → Load: skills/coding-standards/python
@load CS:javascript   → Load: skills/coding-standards/javascript

# Testing Standards (TS)
@load TS:pytest       → Load: skills/testing/pytest
@load TS:*            → Load: skills/testing/* (all testing skills)

# Security Standards (SEC)
@load SEC:auth        → Load: skills/security/authentication
@load SEC:*           → Load: skills/security/* + NIST-IG:base
```

#### Composite Patterns

```bash
# Multiple standards combined
@load [product:api + CS:python + TS:pytest]
  → Load: product:api skills + python coding + pytest testing
```

### Wildcard Expansion

The bridge automatically expands wildcards:

```yaml
SEC:*  expands to:
  - SEC:auth
  - SEC:secrets
  - SEC:input-validation
  - NIST-IG:base  # Auto-included with security

TS:* expands to:
  - TS:unit
  - TS:integration
  - TS:e2e
```

### Auto-Inclusion Rules

**NIST Baseline Auto-Loading**:

- Any security standard (`SEC:*`) automatically includes `NIST-IG:base`
- Explicit override available with `--no-auto-nist` flag

---

## Level 3: Mastery Resources

### Migration Guide

#### Phase 1: Compatibility Mode (Current)

Both patterns work side-by-side:

```bash
# Legacy pattern (still works)
@load product:api

# New skill pattern (recommended)
skill-loader.py load product:api
```

#### Phase 2: Deprecation Warnings (Month 3-6)

Deprecation warnings will appear in logs.

#### Phase 3: Legacy Removal (Month 6+)

Legacy syntax will be removed. Migration guide available.

### Migration Tools

```bash
# Scan codebase for legacy patterns
skill-loader.py audit-legacy --path .

# Generate migration report
skill-loader.py migration-report --output migration-plan.md

# Auto-migrate files (with backup)
skill-loader.py migrate --path . --backup
```

### Related Skills

- [skill-loader](../skill-loader/SKILL.md) - New skill loading mechanism
- [coding-standards](../coding-standards/SKILL.md) - Base coding standards
- [security-practices](../security-practices/SKILL.md) - Security implementations

### External Resources

- `resources/legacy-mappings.yaml` - Complete mapping definitions
- `config/product-matrix.yaml` - Original product definitions
- `examples/legacy-patterns/` - Migration examples
