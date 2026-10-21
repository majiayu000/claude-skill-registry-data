---
name: linting
description: Fix machine-detectable issues using configured project tooling. Triggers on "lint", "lint 修复".
---

# Linting

## When to use

- Fix machine-detectable issues using configured project tooling.

**Not for:** code-review for semantics; debugging for runtime failures.

## Steps

1. Read scripts, configuration and CI for actual commands.

2. Run checks and classify defects, formatting and justified narrow suppression.

3. Fix scoped batches without weakening rules or broadly hiding failures.

4. Rerun changed checks and compare local and CI behavior; report unrelated pre-existing failures separately.

## Verify

- Configured checks ran; suppressions are narrow and justified and unrelated failures remain visible.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
