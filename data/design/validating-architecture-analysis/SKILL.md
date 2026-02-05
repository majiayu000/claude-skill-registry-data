---
name: validating-architecture-analysis
description: Validate architecture artifacts against contracts and consistency requirements - codifies systematic validation practices with professional reporting
---

# Validating Architecture Analysis

## Purpose

Validate architecture analysis artifacts (subsystem catalogs, diagrams, reports) against contract requirements and cross-document consistency standards, producing actionable validation reports with clear approval/revision status.

## When to Use

- Coordinator delegates validation after document production
- Task specifies validating `02-subsystem-catalog.md`, `03-diagrams.md`, or `04-final-report.md`
- Validation gate required before proceeding to next phase
- Need independent quality check with fresh eyes
- Output determines whether work progresses or requires revision

## Core Principle: Systematic Verification

**Good validation finds all issues systematically. Poor validation misses violations or invents false positives.**

Your goal: Thorough, objective, evidence-based validation with specific, actionable feedback.

## Validation Types

### Type 1: Contract Compliance

**Validate single document against its contract:**

**Example contracts:**
- **Subsystem Catalog** (`02-subsystem-catalog.md`): 8 required sections per entry (Location, Responsibility, Key Components, Dependencies [Inbound/Outbound format], Patterns Observed, Concerns, Confidence, separator)
- **Architecture Diagrams** (`03-diagrams.md`): Context + Container + 2-3 Component diagrams, titles/descriptions/legends, assumptions section
- **Final Report** (`04-final-report.md`): Executive summary, TOC, diagrams integrated, key findings, appendices

**Validation approach:**
1. Read contract specification from task or skill documentation
2. Check document systematically against each requirement
3. Flag missing sections, extra sections, wrong formats
4. Distinguish CRITICAL (contract violations) vs WARNING (quality issues)

### Type 2: Cross-Document Consistency

**Validate that multiple documents align:**

**Common checks:**
- Catalog dependencies match diagram arrows
- Diagram subsystems listed in catalog
- Final report references match source documents
- Confidence levels consistent across documents

**Validation approach:**
1. Extract key elements from each document
2. Cross-reference systematically
3. Flag inconsistencies with specific citations
4. Provide fixes that maintain consistency

## Output: Validation Report

### File Path (CRITICAL)

**Write to workspace temp/ directory:**
```
<workspace>/temp/validation-<document-name>.md
```

**Examples:**
- Workspace: `docs/arch-analysis-2025-11-12-1234/`
- Catalog validation: `docs/arch-analysis-2025-11-12-1234/temp/validation-catalog.md`
- Diagram validation: `docs/arch-analysis-2025-11-12-1234/temp/validation-diagrams.md`
- Consistency validation: `docs/arch-analysis-2025-11-12-1234/temp/validation-consistency.md`

**DO NOT use absolute paths like `/home/user/skillpacks/temp/`** - write to workspace temp/.

### Report Structure (Template)

```markdown
# Validation Report: [Document Name]

**Document:** `<path to validated document>`
**Validation Date:** YYYY-MM-DD
**Overall Status:** APPROVED | NEEDS_REVISION (CRITICAL) | NEEDS_REVISION (WARNING)

---

## Contract Requirements

[List the contract requirements being validated against]

---

## Validation Results

### [Entry/Section 1]

**CRITICAL VIOLATIONS:**
1. [Specific issue with line numbers]
2. [Specific issue with line numbers]

**WARNINGS:**
1. [Quality issue, not blocking]

**Passes:**
- ✓ [What's correct]
- ✓ [What's correct]

**Summary:** X CRITICAL, Y WARNING

---

### [Entry/Section 2]

...

---

## Overall Assessment

**Total [Entries/Sections] Analyzed:** N
**[Entries/Sections] with CRITICAL:** X
**Total CRITICAL Violations:** Y
**Total WARNINGS:** Z

### Violations by Type:
1. **[Type]:** Count
2. **[Type]:** Count

---

## Recommended Actions

### For [Entry/Section]:
[Specific fix with code block]

---

## Validation Approach

**Methodology:**
[How you validated]

**Checklist:**
[Systematic verification steps]

---

## Self-Assessment

**Did I find all violations?**
[YES/NO with reasoning]

**Coverage:**
[What was checked]

**Confidence:** [High/Medium/Low]

---

## Summary

**Status:** [APPROVED or NEEDS_REVISION]
**Critical Issues:** [Count]
**Warnings:** [Count]

[Final disposition]
```

## Validation Status Levels

### APPROVED

**When to use:**
- All contract requirements met
- No CRITICAL violations
- Minor quality issues acceptable (or none)

**Report should:**
- Confirm compliance
- List what was checked
- Note any minor observations

### NEEDS_REVISION (WARNING)

**When to use:**
- Contract compliant
- Quality issues present (vague descriptions, weak reasoning)
- NOT blocking progression

**Report should:**
- Confirm contract compliance
- List quality improvements suggested
- Note: "Not blocking, but recommended"
- Distinguish from CRITICAL

### NEEDS_REVISION (CRITICAL)

**When to use:**
- Contract violations (missing/extra sections, wrong format)
- Cross-document inconsistencies
- BLOCKS progression to next phase

**Report should:**
- List all CRITICAL violations
- Provide specific fixes for each
- Be clear this blocks progression

## Systematic Validation Checklist

### For Subsystem Catalog

**Per entry:**
```
[ ] Section 1: Location with absolute path in backticks?
[ ] Section 2: Responsibility as single sentence?
[ ] Section 3: Key Components as bulleted list?
[ ] Section 4: Dependencies in "Inbound: X / Outbound: Y" format?
[ ] Section 5: Patterns Observed as bulleted list?
[ ] Section 6: Concerns present (or "None observed")?
[ ] Section 7: Confidence (High/Medium/Low) with reasoning?
[ ] Section 8: Separator "---" after entry?
[ ] No extra sections beyond these 8?
[ ] Sections in correct order?
```

**Whole document:**
```
[ ] All subsystems have entries?
[ ] No placeholder text ("[TODO]", "[Fill in]")?
[ ] File named "02-subsystem-catalog.md"?
```

### For Architecture Diagrams

**Diagram levels:**
```
[ ] Context diagram (C4 Level 1) present?
[ ] Container diagram (C4 Level 2) present?
[ ] Component diagrams (C4 Level 3) present? (2-3 required)
```

**Per diagram:**
```
[ ] Title present and descriptive?
[ ] Description present after diagram?
[ ] Legend explaining notation?
[ ] Valid syntax (Mermaid or PlantUML)?
```

**Supporting sections:**
```
[ ] Assumptions and Limitations section present?
[ ] Confidence levels documented?
```

### For Cross-Document Consistency

**Catalog ↔ Diagrams:**
```
[ ] Each catalog subsystem shown in Container diagram?
[ ] Each catalog "Outbound" dependency shown as diagram arrow?
[ ] Each diagram arrow corresponds to catalog dependency?
[ ] Bidirectional: If A→B in catalog, B shows A as Inbound?
```

**Diagrams ↔ Final Report:**
```
[ ] All diagrams from 03-diagrams.md embedded in report?
[ ] Subsystem descriptions in report match catalog?
[ ] Key findings reference actual concerns from catalog?
```

## Cross-Document Validation Pattern

**Step-by-step approach:**

1. **Extract from Catalog:**
   - List all subsystems
   - For each, extract "Outbound" dependencies

2. **Extract from Diagram:**
   - Find Container diagram
   - List all `Rel()` statements (Mermaid) or `Rel` calls (PlantUML)
   - Map source → target for each relationship

3. **Cross-Reference:**
   - For each catalog dependency, check if diagram shows arrow
   - For each diagram arrow, check if catalog lists dependency
   - Flag mismatches

4. **Report Inconsistencies:**
   - Use summary table showing what matches and what doesn't
   - Provide line numbers from both documents
   - Suggest specific fixes (add arrow, update catalog)

## Best Practices from Baseline Testing

### What Works

✅ **Thorough checking** - Find ALL violations, not just first one
✅ **Specific feedback** - Line numbers, exact quotes, actionable fixes
✅ **Professional reports** - Metadata, methodology, self-assessment
✅ **Systematic checklists** - Document what was verified
✅ **Clear status** - APPROVED / NEEDS_REVISION with severity
✅ **Summary visualizations** - Tables showing passed vs failed
✅ **Impact analysis** - Explain why issues matter
✅ **Self-assessment** - Verify own completeness

### Validation Excellence

**Thoroughness patterns:**
- Check every entry/section (100% coverage)
- Find both missing AND extra sections
- Distinguish format violations from quality issues

**Specificity patterns:**
- Provide line numbers for all findings
- Quote exact text showing violation
- Show what correct format should be

**Actionability patterns:**
- Provide code blocks with fixes
- Suggest alternatives when applicable
- Prioritize fixes (CRITICAL first)

## Common Pitfalls to Avoid

❌ **Stopping after first violation** - Find ALL issues
❌ **Vague feedback** ("improve quality" vs "add Concerns section")
❌ **Wrong status level** (marking quality issues as CRITICAL)
❌ **False positives** (inventing issues that don't exist)
❌ **Too lenient** (approving despite violations)
❌ **Too strict** (marking everything CRITICAL)
❌ **Wrong file path** (absolute path vs workspace temp/)
❌ **Skipping self-assessment** (verify your own completeness)

## Objectivity Under Pressure

**If coordinator says "looks fine to me":**
- Validate independently anyway
- Evidence-based judgment (cite specific contract)
- Don't soften CRITICAL to WARNING due to authority
- Stand firm: validation is independent quality gate

**If time pressure exists:**
- Still validate systematically (don't skip checks)
- Document what was validated and what wasn't
- If truly insufficient time, report that honestly

## Success Criteria

**You succeeded when:**
- Found all contract violations (100% detection)
- Specific feedback with line numbers
- Actionable fixes provided
- Clear status (APPROVED/NEEDS_REVISION with severity)
- Professional report structure
- Wrote to workspace temp/ directory
- Self-assessment confirms completeness

**You failed when:**
- Missed violations
- Vague feedback ("improve this")
- Wrong status level (quality issue marked CRITICAL)
- No actionable fixes
- Wrote to wrong path
- Approved despite violations

## Integration with Workflow

This skill is typically invoked as:

1. **Coordinator** produces document (catalog, diagrams, or report)
2. **Coordinator** spawns validation subagent (YOU)
3. **YOU** read document(s) and contract requirements
4. **YOU** validate systematically using checklists
5. **YOU** write validation report to workspace temp/
6. **Coordinator** reads validation report
7. **If APPROVED**: Coordinator proceeds to next phase
8. **If NEEDS_REVISION**: Coordinator fixes issues, re-validates (max 2 retries)

**Your role:** Independent quality gate ensuring artifacts meet standards before progression.
