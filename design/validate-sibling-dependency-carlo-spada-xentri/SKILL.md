---
name: validate-sibling-dependency
description: Validate Sibling Dependency Law (ADR-020) for Xentri architecture. Use when checking module dependencies, creating new requirements, adding interfaces between entities, or reviewing cross-module relationships. Enforces that entities can only depend on siblings (same parent) and cross-branch access must be declared at common ancestor level.
---

# Validate Sibling Dependency Law (ADR-020)

## Purpose

Enforces the **Sibling Dependency Law** — a critical architectural constraint that prevents dependency spaghetti in the Xentri documentation hierarchy.

## Core Rules

1. **Single-Parent Inheritance**: Every entity has exactly ONE parent, encoded in its requirement ID
2. **Sibling-Only Dependencies**: `requires_interfaces` can only reference siblings (nodes with same parent)
3. **Inherited Access**: Cross-branch dependencies must be declared at the common ancestor level
4. **Violation = Redesign**: If validation fails, STOP and redesign — do not create workarounds

## Quick Validation

Run this command to check for violations:

```bash
pnpm exec tsx scripts/validation/validate-dependencies.ts --path docs
```

## Decision Tree

```
Is Target a sibling of Source? (same direct parent)
│
├─ YES → ✅ VALID: Declare requires_interfaces directly
│
└─ NO → Find common ancestor
        │
        ├─ Ancestor already has access? → ✅ Use inherited_interfaces
        │
        └─ Ancestor lacks access?
            │
            ├─ Can ancestor declare it? → Bubble up the dependency
            │
            └─ Structural problem? → Redesign required (or ADR exception)
```

## Examples

### ✅ Valid: Sibling Dependency

```yaml
# God-View depends on KPI-Center (both children of Pulse)
Source: docs/strategy/pulse/god-view/
Target: docs/strategy/pulse/kpi-center/
Result: VALID — same parent (Pulse)
```

### ❌ Invalid: Cross-Branch Dependency

```yaml
# God-View trying to depend directly on Shell
Source: docs/strategy/pulse/god-view/
Target: docs/platform/shell/
Result: INVALID — different branches (Strategy vs Platform)
Resolution: Strategy must declare dependency on Shell; God-View inherits
```

### ✅ Valid: Inherited Access

```yaml
# God-View using Core-API via Constitution-level declaration
Source: docs/strategy/pulse/god-view/
Target: docs/platform/core-api/
Context: Constitution (docs/platform/) declares IC-API-001
Result: VALID via inheritance
```

## When to Use This Skill

Claude will automatically invoke this skill when you:

- Ask about module dependencies
- Create new `requires_interfaces` declarations
- Review architecture for dependency violations
- Add interfaces between entities
- Mention "ADR-020", "sibling dependency", or "cross-module dependency"

## Resolution Options

When a violation is detected:

1. **Bubble Up**: Declare the dependency at the common ancestor level
2. **Redesign**: Restructure entities to be siblings, or use events instead
3. **Exception** (last resort): Create ADR documenting the exception with remediation plan

## Full Documentation

See `docs/platform/architecture/adr-020-sibling-dependency-law.md` for complete specification including:

- Requirement file format
- Dependency resolution algorithm
- Escape hatch for exceptions
- Enforcement mechanisms (CI, pre-commit, review)
