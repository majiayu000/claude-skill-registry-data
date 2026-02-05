---
name: Conducting Code Review
description: Complete workflow for conducting thorough code reviews with structured feedback
when_to_use: when conducting code review, when another agent asks you to review code, after being dispatched by requesting-code-review skill
version: 3.1.0
---

# Conducting Code Review

## Overview

Systematic code review process ensuring correctness, security, and maintainability through practice adherence and structured feedback. Tests and checks are assumed to pass - reviewer focuses on code quality.

## Quick Reference

**Before starting:**
1. Read upstream skill: `${CLAUDE_PLUGIN_ROOT}skills/requesting-code-review/SKILL.md`
2. Read project practices: `${CLAUDE_PLUGIN_ROOT}standards/code-review.md`

**Core workflow:**
1. Review most recent commit(s)
2. Review against practice standards (all severity levels)
3. Save structured feedback to work directory

**Note:** Tests and checks are assumed to pass. Focus on code quality review.

## Implementation

### Prerequisites

Read these before conducting review:
- `${CLAUDE_PLUGIN_ROOT}skills/requesting-code-review/SKILL.md` - Understand requester expectations
- `${CLAUDE_PLUGIN_ROOT}standards/code-review.md` - Standards, severity levels, project commands

### Step-by-Step Workflow

#### 1. Identify code to review

**Determine scope:**
- Most recent commit: `git log -1 --stat`
- Recent commits on branch: `git log origin/main..HEAD`
- Full diff: `git diff origin/main...HEAD`

#### 2. Review code against standards

**Read standards from practices:**

```bash
# Standards live in practices, not in this skill
${CLAUDE_PLUGIN_ROOT}standards/code-review.md
```

**Review ALL severity levels:**
1. BLOCKING (Must Fix Before Merge) - from practices
2. NON-BLOCKING (Can Be Deferred) - from practices

**Empty sections are GOOD if you actually checked.** Missing sections mean you didn't check.

#### 3. Save structured review - ALGORITHMIC ENFORCEMENT

**Template location:**
`${CLAUDE_PLUGIN_ROOT}templates/code-review-template.md`

<EXTREMELY-IMPORTANT>
**BEFORE writing review file, verify each required section using this algorithm:**

##### Template Validation Algorithm

**1. Check Status section exists**

Does your review have `## Status: [BLOCKED | APPROVED WITH NON-BLOCKING SUGGESTIONS | APPROVED]`?
- NO → STOP. Delete draft. Start over with template.
- YES → CONTINUE

**2. Check Next Steps section exists**

Does your review have `## Next Steps`?
- NO → STOP. Delete draft. Start over with template.
- YES → CONTINUE

**3. Check BLOCKING section exists**

Does your review have `## BLOCKING (Must Fix Before Merge)`?
- NO → STOP. Delete draft. Start over with template.
- YES → CONTINUE

**4. Check NON-BLOCKING section exists**

Does your review have `## NON-BLOCKING (May Be Deferred)`?
- NO → STOP. Delete draft. Start over with template.
- YES → CONTINUE

**5. Check Checklist section exists**

Does your review have `## Checklist` with all 6 categories?
- NO → STOP. Delete draft. Start over with template.
- YES → CONTINUE

**6. Check for prohibited custom sections**

Have you added ANY sections not listed above (examples of PROHIBITED sections: Strengths, Code Quality Metrics, Assessment, Recommendations, Requirements Verification, Comparison to Previous Reviews, Reviewer Notes, Sign-Off, Review Summary, Issues with subsections, Test Results, Check Results)?
- YES → STOP. Delete custom sections. Use template exactly.
- NO → CONTINUE

**7. Save review file**

All required sections present, no custom sections → Save to work directory.
</EXTREMELY-IMPORTANT>

**File naming:** See `${CLAUDE_PLUGIN_ROOT}standards/code-review.md` for `.work` directory location and naming convention (`{YYYY-MM-DD}-review-{N}.md`).

**Additional context allowed:**
You may add supplementary details AFTER the Checklist section (verification commands run, files changed, commit hashes). But the 5 required sections above are mandatory and must appear first in the exact order shown.


## What NOT to Skip

**NEVER skip:**
- Reviewing ALL severity levels (not just critical)
- Saving review file to work directory
- Including positive observations

**Common rationalizations that violate workflow:**
- "Code looks clean" → Check all severity levels anyway
- "Simple change" → Thorough review prevents production bugs
- "Senior developer" → Review objectively regardless of author
- "Template is too simple, adding sections" → Step 3 algorithm checks for custom sections. STOP if they exist.
- "My format is more thorough" → Thoroughness goes IN the template sections. Algorithm enforces exact structure.
- "Adding Strengths section helps" → PROHIBITED. Algorithm Step 6 blocks this.
- "Assessment section adds value" → PROHIBITED. Algorithm Step 6 blocks this.
- "Requirements Verification is useful" → Put in NON-BLOCKING or Checklist. Not a separate section.

**Note:** Tests and checks are assumed to pass. Reviewers focus on code quality, not test execution.

## Related Skills

**Requestion code review:**
- Requesting Code Review: `${CLAUDE_PLUGIN_ROOT}skills/requesting-code-review/SKILL.md`

**When receiving feedback on your review:**
- Code Review Reception: `${CLAUDE_PLUGIN_ROOT}skills/receiving-code-review/SKILL.md`

## Testing This Skill

See `test-scenarios.md` for pressure tests validating this workflow resists rationalization.
