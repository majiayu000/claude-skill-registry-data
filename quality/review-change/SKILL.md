---
name: review-change
description: Review an exact diff, branch or pull request for actionable defects and acceptance gaps without editing files or running autofix. Use when the user asks to review, audit or check a change before merging. Running checks for evidence belongs to verify-change; acceptance against the need belongs to validate-change.
---

# review-change

## Steps

1. Establish the base, exact revision/diff, acceptance, callers and relevant
   tests. Read only the architecture/profile relevant to the change. Review
   integrated backend/frontend contracts together.
2. Inspect backend invariants, authorization/scopes, transactions, migrations,
   concurrency and effects.
3. Inspect frontend private imports, server secrets vs client transport, stale
   queries after mutation or scope changes, form validation, error recovery,
   focus/accessibility and responsive behavior.
4. Check API/BFF status codes, envelopes, headers/cookies and real consumer
   evidence.
5. Use read-only searches/checks and focused reproductions on owned resources.

## Output

One entry per finding: file/line, trigger, observable impact, evidence, and
whether it is a reproduced failure or a hypothesis. A correct diff may have no
findings. Return findings to backend-change/frontend-change/schema-change; the
implementer refines and renews affected evidence, and
[validate-change](../validate-change/SKILL.md) resolves acceptance on the final
combined state.

## Gotchas

- Do not edit code or acceptance, run autofix, sync skills, publish, or claim
  another owner performed your review.
- Green lint is not complete semantic compliance.
