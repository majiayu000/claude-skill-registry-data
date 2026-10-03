---
name: output-validation-checklist
description: >
  Use before delivering any work product to validate quality. This skill provides a
  standardized checklist that every agent must complete before marking work as done,
  ensuring consistent quality across all deliverables regardless of agent or company.
---

# Output Validation Checklist

## Overview
This skill defines the standard validation checklist that ALL agents must run before delivering work. It catches common issues before they reach downstream agents or human stakeholders. Use this skill as the final gate before marking any task complete.

## When to Use
- Before delivering any completed work to another agent or stakeholder
- Before marking a task or ticket as "done"
- Before committing code or documentation to shared repositories
- Before sending deliverables for review or approval
- **Don't use when:** During exploratory work or drafting phases

## Core Procedures

### Universal Validation Checklist
Run ALL applicable checks before every delivery:

#### 1. Completeness Check
- [ ] All requested items are addressed (no partial delivery)
- [ ] All requirements from the original task are satisfied
- [ ] All expected deliverables are present and accounted for
- [ ] No TODOs, placeholders, or temporary content remains

#### 2. Accuracy Check
- [ ] Facts, figures, and references verified against source material
- [ ] Calculations and logic are correct (spot-checked at minimum)
- [ ] No contradictions or inconsistencies in the output
- [ ] Technical claims are backed by evidence or citation

#### 3. Format Check
- [ ] Output follows the requested format (JSON, markdown, code, etc.)
- [ ] File naming follows project conventions
- [ ] Structure is consistent and well-organized
- [ ] No formatting artifacts (broken markdown, unclosed tags, etc.)

#### 4. Quality Check
- [ ] Language is clear, professional, and appropriate for audience
- [ ] Code is readable, commented where needed, and follows standards
- [ ] No typos, grammatical errors, or unclear explanations
- [ ] Output could be understood by someone who wasn't part of the conversation

#### 5. Safety Check
- [ ] No secrets, credentials, or sensitive data in output
- [ ] No harmful instructions or unvalidated external links
- [ ] Output doesn't accidentally expose internal system details
- [ ] Any disclaimers or warnings are included where required

#### 6. Traceability Check
- [ ] Decisions made during work are documented or explained
- [ ] Any assumptions made are clearly stated
- [ ] Sources are cited where information was drawn from references
- [ ] If alternatives were considered, reasoning for choice is clear

### Domain-Specific Additions
Add these checks based on deliverable type:

**Code DeliverABLES:**
- [ ] Passes all existing tests (no regressions)
- [ ] No linting or style warnings
- [ ] Dependencies are documented and pinned
- [ ] Error handling covers edge cases

**DOCUMENTATION:**
- [ ] Links are valid and point to correct destinations
- [ ] Examples are tested and produce stated results
- [ ] Table of contents matches actual structure
- [ ] Version information is current and accurate

**ANALYSIS/REPORTS:**
- [ ] Methodology is documented and reproducible
- [ ] Data sources are cited and accessible
- [ ] Limitations and caveats are acknowledged
- [ ] Conclusions follow logically from evidence

**CONFIGURATIONS/SETUPS:**
- [ ] Tested in clean environment (not just on working copy)
- [ ] Prerequisites are documented
- [ ] Rollback procedure is provided
- [ ] Security implications are noted

## Quality Checklist
- [ ] ALL universal checks above are passed
- [ ] ALL applicable domain-specific checks are passed
- [ ] Any items marked "needs follow-up" have been tracked
- [ ] Validation results are included in delivery

## Error Handling
- **Error:** Item fails completeness check
  **Response:** Complete the missing work before delivery, or explicitly document what's deferred
- **Error:** Item fails accuracy check
  **Response:** Investigate and correct the inaccuracy, re-run all checks
- **Error:** Item fails safety check
  **Response:** IMMEDIATELY remove sensitive content, do not deliver until clean
- **Error:** Urgent deadline but validation fails
  **Response:** Deliver with explicit "known issues" section, schedule immediate fix

## Cross-Team Integration
**Related Skills:** feedback-integration, edge-case-analysis, regression-prevention, documentation-quality-check
**Used By:** ALL agents as final validation gate before delivery