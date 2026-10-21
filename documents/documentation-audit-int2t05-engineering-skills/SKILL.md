---
name: documentation-audit
description: Write or synchronize implementation documentation with source evidence. Triggers on "docs out of date", "文档同步".
---

# Documentation Audit

## When to use

- Write or synchronize implementation documentation with source evidence.

**Not for:** spec for requirement changes; oss-polish for presentation.

## Steps

1. Agree readers, purpose, scope and paths; inventory actual documents rather than assuming five mandatory categories.

2. Trace contracts, configuration and meaningful calls; distinguish stale descriptions from missing implementation.

3. Correct descriptive drift and ask about requirement or design discrepancies rather than rewriting agreed intent to excuse code.

4. Produce readable docs and the approved report with evidence, fixed items and open decisions; check paths, examples and symbols.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/audit/YYYY-MM-DD-documentation.md` at the approved path alongside corrected docs.

## Verify

- Descriptions match source evidence; requirement changes were not silently accepted and review status is honest.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/templates.md](references/templates.md) — audit-report template
- [references/writing-docs.md](references/writing-docs.md) — writing new documentation from scratch (README, feature docs, API docs)
