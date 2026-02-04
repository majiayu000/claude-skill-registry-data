---
name: ticket-review
description: |
  Reviews existing tickets for gaps, inconsistencies, and issues with severity classification.
  This skill should be used when reviewing a ticket document for quality, completeness, and
  implementer readiness. Provides a structured review workflow with findings categorized by
  severity (Critical, High, Medium, Low) and specific before/after proposals for fixes.
---

# Ticket Review

## Overview

This skill provides a structured workflow for reviewing ticket documents. Unlike Caster's standard creation workflow, this is an **analysis and critique** workflow focused on finding issues and proposing fixes.

## When to Use

- User wants to review an existing ticket
- User says "review this ticket", "check this spec", "find issues in..."
- The `/ticket-review` command is invoked
- User has been discussing a ticket and wants it reviewed

## Workflow

Review follows a different workflow than document creation:

### Phase 1: Document Loading

1. **Identify the ticket** to review:
   - If path is provided, read that file
   - If no path, infer from conversation context (look for recently discussed ticket)
   - If ambiguous, ask the user to specify

2. **Read the full document** without limit/offset parameters
   - Parse frontmatter for metadata
   - Understand the document structure
   - Note the ticket's purpose and scope

### Phase 2: Analysis [ULTRATHINK]

Analyze the document for four types of issues:

| Issue Type | Description | Questions to Ask |
|------------|-------------|------------------|
| **Gaps** | Missing information | What would an implementer need to know that isn't here? |
| **Inconsistencies** | Conflicting information | Do different sections contradict each other? |
| **Ambiguity** | Unclear or vague statements | Could this be interpreted multiple ways? |
| **Completeness** | Missing coverage | Are acceptance criteria complete? Are all cases covered? |

### Phase 3: Severity Classification

Classify each finding using this framework:

| Severity | Definition | Example |
|----------|------------|---------|
| **Critical** | Conflicting information that would break implementation | Two sections specify different behavior for the same feature |
| **High** | High ambiguity causing significant implementer confusion | Behavior described but critical edge cases undefined |
| **Medium** | Missing info that could cause unexpected behavior | Default value unspecified, implementer must guess |
| **Low** | Nice-to-have clarifications, cosmetic issues | Output format example missing but inferable |

### Phase 4: Present Findings

Present findings organized by severity, with specific location and proposed fix:

```markdown
## Review Findings

### Critical (0 issues)

None found.

### High (1 issue)

#### H1: [Brief title]

**Location**: Part X, lines Y-Z

**Issue**: [Clear description of what's wrong]

**Impact**: [Why this matters for implementation]

**Proposed fix**:

Before:
```
[exact current text]
```

After:
```
[exact proposed text]
```

### Medium (2 issues)

#### M1: [Brief title]
...

### Low (1 issue)

#### L1: [Brief title]
...

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 1 |

**Recommendation**: [Fix the N critical/high issues before implementation]
```

### Phase 5: Apply Fixes

**Wait for user approval** before applying any changes.

When approved:
1. Apply fixes in order of severity (Critical first)
2. Update `last_updated` and `last_updated_by` in frontmatter
3. Add `last_updated_note` summarizing changes
4. Confirm each change was applied

## Finding Format

Each finding must include:

1. **Unique ID**: Severity prefix + number (C1, H1, M1, L1)
2. **Title**: Brief description (5-10 words)
3. **Location**: Part/section and line numbers if possible
4. **Issue**: Clear description of the problem
5. **Impact**: Why this matters (for Medium+ severity)
6. **Proposed fix**: Exact before/after text

## Review Principles

- **Be specific**: Vague feedback is not actionable
- **Show don't tell**: Always include before/after text
- **Prioritize**: Critical and High issues first
- **Stay scoped**: Review for implementer readiness, not feature design
- **Preserve intent**: Fixes should clarify, not change meaning

## What NOT to Review

- Feature decisions (that's the author's domain)
- Writing style (unless it causes ambiguity)
- Structure choices (unless they cause confusion)
- Scope (unless explicitly asked)

Focus on: **Would an implementer be able to build this correctly?**

## Quality Checklist

Before presenting findings:

- [ ] Read the entire document (no skimming)
- [ ] Each finding has specific location
- [ ] Each finding has exact before/after text
- [ ] Severity classification is justified
- [ ] Findings are actionable (not vague critiques)
- [ ] Summary includes counts and recommendation

## Remember

A good review catches issues before they reach implementation. Be thorough but constructive - the goal is to improve the document, not criticize the author.
