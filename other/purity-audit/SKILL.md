---
name: purity-audit
description: Audit scoped artifacts for obsolete residue, duplication and factual gaps. Triggers on "purity audit", "纯净审计".
---

# Purity Audit

## When to use

- Audit scoped artifacts for obsolete residue, duplication and factual gaps.

**Not for:** documentation-audit for synchronization; code-review for defects.

## Steps

1. Agree target and load the checklist; preserve operational versions, valid pending work and legitimate audit evidence.

2. Search obsolete references, repeated rules, editing prose and decoration; judge matches in context.

3. Check action/verification correspondence and output ownership; delegate only when authorized and useful.

4. Fix scoped residue and produce the approved report; rerun targeted checks and classify open findings.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/audit/YYYY-MM-DD-purity.md` at the approved path.

## Verify

- Findings have contextual evidence; necessary history, versions and unrelated content are preserved.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [purity-checklist.md](../../../references/purity-checklist.md) — the 16-point A–E checklist (the audit criteria).
- [references/subagent-dispatch.md](references/subagent-dispatch.md) — per-category auditor dispatch: constructed-context template + worked Category-A example.
- [references/templates.md](references/templates.md) — audit-report template.
