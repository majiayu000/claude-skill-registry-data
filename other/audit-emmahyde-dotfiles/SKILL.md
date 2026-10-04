---
description: >-
  Structured PASS/FAIL audit of any target against any criteria. Takes a subject
  and a topic as arguments — the subject is what to audit, the topic defines
  what to check. Reads the target, builds criteria from the topic, and reports
  a table with specific violations and fix recommendations.
  <triggers>
    /audit, audit this, run an audit, check against, compliance check,
    audit for, does this pass, review against criteria
  </triggers>
---

# Audit

Run a structured PASS/FAIL audit of a target against a topic.

```
/audit [target] [topic]
/audit skills/discuss progressive disclosure
/audit app/ops/foo_op.rb ops pattern compliance
/audit .context/PLAN-auth.md plan template completeness
/audit client/apps/sponsor naming conventions
```

## Process

### Step 1: Parse Target and Topic

From the argument, identify:

- **Target** — file path, directory, glob, or conceptual scope to audit
- **Topic** — what criteria to evaluate against

If ambiguous, ask:

```
What should I audit, and against what criteria?
```

### Step 2: Build Criteria

Based on the topic, construct a checklist of auditable criteria. Sources:

1. **Codebase conventions** — read `.context/codebase/CONVENTIONS.md`, `CLAUDE.md`, or relevant config files
2. **Domain knowledge** — apply known best practices for the topic (e.g., progressive disclosure layers, ops pattern requirements, accessibility standards)
3. **Reference documents** — if a spec or template exists for the topic, read it and extract checkable items
4. **Prior audits** — check for existing `.context/` files that define expected structure

Present the criteria before auditing:

```
Auditing: [target]
Against: [topic]

Criteria:
1. [checkable item]
2. [checkable item]
...

Proceed?
```

### Step 3: Audit

For each criterion, read the target and evaluate. Collect evidence:

- **PASS** — criterion met, cite the evidence (file:line or specific content)
- **FAIL** — criterion not met, cite what's missing or wrong
- **N/A** — criterion doesn't apply to this target

### Step 4: Report

```
## Audit: [target] against [topic]

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | [item] | PASS | [citation] |
| 2 | [item] | FAIL | [what's wrong] |
| 3 | [item] | N/A | [why] |

**Result:** X/Y passed (Z%)
```

### Step 5: Recommendations

For each FAIL, provide:

- What specifically needs to change
- Where (file:line if applicable)
- Before/after example if the fix is non-obvious

Keep recommendations concrete and actionable — no vague "consider improving X."
