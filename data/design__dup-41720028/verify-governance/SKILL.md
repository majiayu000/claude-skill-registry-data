---
name: verify-governance
description: Verify integrity and completeness of governance framework - checks all required files exist, are properly formatted, have current metrics, and align with each other
---

# Verify Governance Framework

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: verify-governance | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: verify-governance | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



You are verifying the integrity and completeness of the project's governance framework, ensuring all components are present, properly formatted, and mutually consistent.

## Purpose

Governance frameworks can drift over time:
- Files get out of sync
- Metrics become stale
- Links break
- Inconsistencies emerge between constitution, roadmap, and next steps

This skill performs systematic verification to detect and report issues.

## Verification Process

### Phase 1: File Existence Check

**Check all required governance files exist:**

```bash
# Core governance files
echo "=== Checking Core Governance Files ==="
[ -f .wrangler/CONSTITUTION.md ] && echo "✓ Constitution exists" || echo "✗ MISSING: Constitution"
[ -f .wrangler/ROADMAP.md ] && echo "✓ Roadmap exists" || echo "✗ MISSING: Roadmap"
[ -f .wrangler/ROADMAP_NEXT_STEPS.md ] && echo "✓ Next Steps exists" || echo "✗ MISSING: Next Steps"

# Process documentation
echo "=== Checking Process Documentation ==="
[ -f .wrangler/specifications/README.md ] && echo "✓ Specs README exists" || echo "✗ MISSING: Specs README"
[ -f .wrangler/issues/README.md ] && echo "✓ Issues README exists" || echo "✗ MISSING: Issues README"

# Templates
echo "=== Checking Templates ==="
[ -f .wrangler/templates/issue.md ] && echo "✓ Issue template exists" || echo "✗ MISSING: Issue template"
[ -f .wrangler/templates/specification.md ] && echo "✓ Spec template exists" || echo "✗ MISSING: Spec template"
```

**Report missing files**: If any files missing, suggest running `initialize-governance` skill.

### Phase 2: Constitution Validation

**Read constitution file:**

```bash
cat .wrangler/CONSTITUTION.md
```

**Verify structure:**

- [ ] **Frontmatter present**: Version, Ratified date, Last Amended
- [ ] **North Star section**: Has mission statement
- [ ] **Core Design Principles**: At least 3 principles
- [ ] **Each principle has**:
  - Principle statement
  - "In Practice" section with specifics
  - "Anti-patterns" section with ❌ examples
  - "Examples" section with ✅ Good and ❌ Bad
- [ ] **Decision Framework**: Has 5 evaluation questions
- [ ] **Evolution of Principles**: Amendment process documented
- [ ] **Version History**: Tracks constitutional changes
- [ ] **Governance Rules**: Documents supremacy of constitution

**Check for ambiguity**:

Scan principles for red flags:
- Vague quality words without definition: "clean", "simple", "elegant"
- No concrete examples
- No anti-patterns
- Unmeasurable criteria

**Report findings**:

```markdown
## Constitution Validation

### ✅ Structure Complete
- Version: [X.Y.Z]
- [N] principles defined
- Decision framework present
- Amendment process documented

### ⚠️ Potential Ambiguities
- **Principle 2**: Uses "simple" without concrete definition
- **Principle 4**: Missing anti-pattern examples
- **Principle 5**: No measurable criteria

### 💡 Recommendation
Consider using `constitution` skill to refine ambiguous principles.
```

### Phase 3: Roadmap Validation

**Read roadmap file:**

```bash
cat .wrangler/ROADMAP.md
```

**Verify structure:**

- [ ] **Overview section**: Project description present
- [ ] **Current State**: Lists completed features
- [ ] **Phase sections**: At least 1 phase defined
- [ ] **Each phase has**:
  - Timeline
  - Goal statement
  - Core features list
  - Success metrics
- [ ] **Technical Debt section**: Ongoing priorities documented
- [ ] **Design Principles section**: Links to constitution
- [ ] **How to Use section**: Guidance for contributors/users
- [ ] **Changelog**: Tracks roadmap evolution
- [ ] **Related Documents**: Links to constitution and next steps

**Verify constitutional alignment**:

Check that roadmap references constitution:
- Links to `CONSTITUTION.md`
- Mentions design principles
- Cites constitutional alignment

**Report findings**:

```markdown
## Roadmap Validation

### ✅ Structure Complete
- [N] phases defined
- All sections present
- Links to constitution: ✓

### ⚠️ Issues Found
- Phase 2 missing success metrics
- Changelog has no entries (might be new)

### 📊 Phase Summary
- **Phase 1**: [N] features, Timeline: [dates]
- **Phase 2**: [N] features, Timeline: [dates]
```

### Phase 4: Next Steps Validation

**Read next steps file:**

```bash
cat .wrangler/ROADMAP_NEXT_STEPS.md
```

**Verify structure:**

- [ ] **Executive Summary**: Current status with % complete
- [ ] **What Works Well**: Highlights strengths
- [ ] **Critical Gap**: Identifies top priority
- [ ] **Three implementation categories**:
  - ✅ Fully Implemented Features
  - ⚠️ Partially Implemented Features (with table)
  - ❌ Not Implemented Features (with impact levels)
- [ ] **Prioritized Roadmap**: 🔴🟡🟢 indicators
- [ ] **Quick Win Checklist**: <4 hour items
- [ ] **References**: Links to related docs

**Verify metrics are current:**

Check if percentages and counts seem reasonable:
- Do fully implemented features match completed specs?
- Are partially implemented features actually in progress?
- Is overall % complete logical?

**Report findings**:

```markdown
## Next Steps Validation

### ✅ Structure Complete
- All three categories present
- Prioritized roadmap included
- Quick wins identified

### ⚠️ Metrics Status
- Overall completion: ~[N]%
- Last Updated: [DATE]
- **Warning**: Last updated >30 days ago - metrics may be stale

### 💡 Recommendation
Run `refresh-metrics` skill to update status counts.
```

### Phase 5: Cross-Document Consistency

**Check that documents reference each other correctly:**

**Constitution → Roadmap:**
```bash
# Check if roadmap mentions constitution
grep -i "constitution" .wrangler/ROADMAP.md
```

**Roadmap → Next Steps:**
```bash
# Check if roadmap changelog mentions next steps updates
grep -i "next.steps\|ROADMAP_NEXT" .wrangler/ROADMAP.md
```

**Next Steps → Constitution:**
```bash
# Check if next steps references principles
grep -i "constitution\|principle" .wrangler/ROADMAP_NEXT_STEPS.md
```

**Verify link integrity:**

- [ ] Constitution links to roadmap
- [ ] Roadmap links to constitution and next steps
- [ ] Next steps links to constitution and roadmap
- [ ] READMEs link to all three core docs
- [ ] Templates reference governance workflow

**Report findings**:

```markdown
## Cross-Document Consistency

### ✅ Links Verified
- Constitution ↔ Roadmap: ✓
- Roadmap ↔ Next Steps: ✓
- READMEs reference core docs: ✓

### ⚠️ Issues
- Next Steps missing reference to Constitution in [section]
- Roadmap changelog has no entry for latest Next Steps update
```

### Phase 6: README Validation

**Check issues README:**

```bash
cat .wrangler/issues/README.md
```

**Verify sections:**
- [ ] Purpose statement
- [ ] Quick reference (creating issues)
- [ ] Issue lifecycle diagram
- [ ] Governance integration (links to constitution/roadmap)
- [ ] Labels section
- [ ] Workflows section
- [ ] Metrics section (with actual counts)
- [ ] Best practices

**Check specifications README:**

```bash
cat .wrangler/specifications/README.md
```

**Verify sections:**
- [ ] Purpose statement
- [ ] Quick reference (creating specs)
- [ ] Specification lifecycle
- [ ] Constitutional governance section
- [ ] Roadmap integration section
- [ ] Workflows section
- [ ] Metrics section (with actual counts)
- [ ] Best practices

**Report findings**:

```markdown
## README Validation

### Issues README
- ✅ All sections present
- ⚠️ Metrics need update (shows placeholders)

### Specifications README
- ✅ All sections present
- ✅ Governance integration documented
- ⚠️ Current phase section shows [Phase Name] placeholder
```

### Phase 7: Template Validation

**Check issue template:**

```bash
cat .wrangler/templates/issue.md
```

**Verify includes:**
- [ ] YAML frontmatter with all fields
- [ ] Description section
- [ ] Acceptance Criteria section
- [ ] Technical Notes section
- [ ] Testing Strategy section
- [ ] Labels guide
- [ ] References section
- [ ] Template usage notes

**Check specification template:**

```bash
cat .wrangler/templates/specification.md
```

**Verify includes:**
- [ ] YAML frontmatter with constitutional alignment fields
- [ ] Constitutional Alignment section (mandatory)
- [ ] Decision Framework verification
- [ ] User Scenarios section
- [ ] Requirements section
- [ ] Design Decisions section
- [ ] Testing Strategy section
- [ ] Acceptance Criteria section
- [ ] For AI Generation section

**Report findings**:

```markdown
## Template Validation

### Issue Template
- ✅ All required sections present
- ✅ Includes governance guidance

### Specification Template
- ✅ All required sections present
- ✅ Constitutional Alignment section included
- ✅ Decision Framework verification included
```

### Phase 8: Generate Verification Report

**Compile all findings into structured report:**

```markdown
# Governance Framework Verification Report

**Date**: [YYYY-MM-DD]
**Project**: [Project Name]

---

## Executive Summary

- **Status**: [✅ HEALTHY / ⚠️ NEEDS ATTENTION / ❌ CRITICAL ISSUES]
- **Missing Files**: [N]
- **Structural Issues**: [N]
- **Stale Metrics**: [Yes/No]
- **Consistency Issues**: [N]

---

## Detailed Findings

### File Existence [✅/⚠️/❌]

**Core Governance**:
- [✅/✗] Constitution
- [✅/✗] Roadmap
- [✅/✗] Next Steps

**Process Documentation**:
- [✅/✗] Issues README
- [✅/✗] Specifications README

**Templates**:
- [✅/✗] Issue template
- [✅/✗] Specification template

### Constitution [✅/⚠️/❌]

**Structure**: [Assessment]
**Ambiguity Check**: [Issues found]
**Recommendations**: [List]

### Roadmap [✅/⚠️/❌]

**Structure**: [Assessment]
**Phase Coverage**: [N phases defined]
**Constitutional Links**: [✅/✗]
**Recommendations**: [List]

### Next Steps [✅/⚠️/❌]

**Structure**: [Assessment]
**Metrics Status**: [Assessment]
**Last Updated**: [DATE]
**Recommendations**: [List]

### Cross-Document Consistency [✅/⚠️/❌]

**Link Integrity**: [Assessment]
**Mutual References**: [Assessment]
**Recommendations**: [List]

### READMEs [✅/⚠️/❌]

**Issues README**: [Assessment]
**Specifications README**: [Assessment]
**Recommendations**: [List]

### Templates [✅/⚠️/❌]

**Issue Template**: [Assessment]
**Specification Template**: [Assessment]
**Recommendations**: [List]

---

## Priority Actions

### 🔴 Critical (Do Now)
1. [Action 1]
2. [Action 2]

### 🟡 Important (Do Soon)
1. [Action 1]
2. [Action 2]

### 🟢 Nice to Have
1. [Action 1]
2. [Action 2]

---

## Recommended Skills

Based on findings, consider running:

- [ ] `initialize-governance` - If missing files
- [ ] `constitution` - If ambiguity detected
- [ ] `refresh-metrics` - If metrics >30 days old
- [ ] `check-constitutional-alignment` - To verify specs

---

**Next Verification**: [DATE + 30 days]
```

## Automated Checks

### Metrics Staleness Detection

**Check last update dates:**

```bash
# Extract dates from files
grep "Last Updated" .wrangler/ROADMAP_NEXT_STEPS.md
grep "Last Updated" .wrangler/issues/README.md
grep "Last Updated" .wrangler/specifications/README.md

# Compare with current date
# If >30 days, flag as stale
```

### Link Validation

**Check for broken references:**

```bash
# Find all markdown links
grep -r "\[.*\](.*.md)" .wrangler/specifications/
grep -r "\[.*\](.*.md)" .wrangler/issues/

# Verify linked files exist
# Report any 404s
```

### Constitutional Version Consistency

**Verify version matches history:**

```bash
# Extract version from frontmatter
version=$(grep "^version:" .wrangler/CONSTITUTION.md | cut -d'"' -f2)

# Extract latest version from history
latest_history=$(grep "^- \*\*.*\*\*" .wrangler/CONSTITUTION.md | head -1)

# Compare
# Report if mismatch
```

## Edge Cases

### Partial Governance Setup

**Situation**: Only some governance files exist

**Response**:
1. Identify what exists vs what's missing
2. Suggest: "Run `initialize-governance` to complete setup"
3. Offer: "Or I can create missing files individually"

### Severely Outdated Metrics

**Situation**: Metrics >90 days old

**Response**:
1. Flag as critical issue
2. Recommend running `refresh-metrics` immediately
3. Warn: "Metrics this old may misguide decisions"

### Constitutional Violations in Specs

**Situation**: Specifications don't have constitutional alignment sections

**Response**:
1. Count how many specs are missing alignment sections
2. List specific spec IDs
3. Recommend: "Add Constitutional Alignment sections to [N] specs"
4. Offer to help update them

### Conflicting Information

**Situation**: Roadmap says Phase 2, but Next Steps shows Phase 1 features incomplete

**Response**:
1. Report the conflict explicitly
2. Ask user: "Which is correct - roadmap or next steps?"
3. Update whichever is wrong

## Success Criteria

Verification is complete when:

- [ ] All 7 required files checked
- [ ] Constitutional structure validated
- [ ] Roadmap structure validated
- [ ] Next Steps structure validated
- [ ] Cross-document links verified
- [ ] READMEs validated
- [ ] Templates validated
- [ ] Metrics staleness checked
- [ ] Comprehensive report generated
- [ ] Priority actions identified

## Common Issues and Fixes

### Issue: Missing Constitutional Alignment in Specs

**Fix**: Update specification template, add sections to existing specs

**Command**:
```bash
# Find specs missing constitutional alignment
grep -L "Constitutional Alignment" .wrangler/specifications/*.md
```

### Issue: Stale Metrics

**Fix**: Run `refresh-metrics` skill

### Issue: Broken Links Between Docs

**Fix**: Update link syntax to use relative paths

**Pattern**: Use `../.wrangler/CONSTITUTION.md` not absolute paths

### Issue: Ambiguous Principles

**Fix**: Run `constitution` skill for Socratic refinement

### Issue: Roadmap Phases Don't Match Next Steps

**Fix**: Synchronize by updating whichever is outdated

**Process**:
1. Check recent changes to both files
2. Determine source of truth
3. Update other file to match
4. Add changelog entry

## Output Format

Always provide:

1. **Quick Status**: One-line assessment (✅/⚠️/❌)
2. **File Checklist**: What exists, what's missing
3. **Structural Issues**: Problems with format/content
4. **Priority Actions**: Ordered by urgency
5. **Recommended Skills**: Which skills to run next

## Related Skills

- **initialize-governance** - For creating missing governance files
- **constitution** - For refining ambiguous principles
- **refresh-metrics** - For updating stale metrics
- **check-constitutional-alignment** - For verifying spec compliance

## Remember

Governance frameworks require maintenance. Running this verification monthly helps catch drift early before it becomes problematic. When you find issues, provide specific, actionable fixes - not just "this is wrong."
