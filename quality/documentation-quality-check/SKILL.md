---
name: documentation-quality-check
description: >
  Use before delivering any documentation to validate quality, accuracy, and completeness.
  This skill provides a checklist for reviewing all documentation deliverables to ensure
  they meet minimum quality standards before distribution.
---

# Documentation Quality Check

## Overview
This skill defines the validation checklist for all documentation. Good documentation is accurate, complete, clear, structured, and maintained. Poor documentation wastes time and causes errors.

## When to Use
- Before delivering any documentation to another agent or stakeholder
- Before publishing documentation to shared repositories
- After making changes to existing documentation
- When documentation is reviewed as part of quality gates
- **Don't use when:** Documentation is exploratory draft not yet for distribution

## Core Procedures

### Step 1: Accuracy Check
- [ ] All technical information is correct and current
- [ ] Examples produce stated results when followed
- [ ] References to other documents are valid and point to correct locations
- [ ] No outdated or deprecated information without clear marking
- [ ] Diagrams, screenshots, and visual aids accurately represent the system

### Step 2: Completeness Check
- [ ] All intended topics are covered
- [ ] Prerequisites and dependencies documented
- [ ] Scope and limitations clearly stated
- [ ] Audience-appropriate detail level (not too shallow, not too deep)
- [ ] Known gaps or TODOs are explicitly identified

### Step 3: Clarity Check
- [ ] Writing is clear and free of jargon without explanation
- [ ] Structure is logical and easy to navigate
- [ ] Headings and sections are descriptive
- [ ] Links work and point to correct destinations
- [ ] Table of contents matches actual structure (if present)
- [ ] No broken formatting or display issues

### Step 4: Consistency Check
- [ ] Terminology used consistently throughout
- [ ] Formatting follows project/style standards
- [ ] Cross-references are accurate and bidirectional
- [ ] Code examples follow coding-standards
- [ ] Version information matches actual document version

### Step 5: Actionability Check
- [ ] Procedures have clear step-by-step instructions
- [ ] Expected outcomes described for each procedure
- [ ] Troubleshooting guidance provided for common failures
- [ ] Contact or escalation path included where relevant
- [ ] Document has author, date, and version metadata

## Quality Checklist
- [ ] ALL accuracy checks pass
- [ ] ALL completeness checks pass
- [ ] ALL clarity checks pass
- [ ] ALL consistency checks pass
- [ ] ALL actionability checks pass
- [ ] Documentation reviewed by second party if high-impact

## Error Handling
- **Error:** Technical inaccuracy discovered
  **Response:** Fix immediately, re-run all accuracy checks, note change in version history
- **Error:** Documentation is incomplete
  **Response:** Complete missing sections before delivery, or clearly mark as partial with expected completion
- **Error:** Examples don't work as documented
  **Response:** Fix example or fix documentation, whichever is actually correct

## Cross-Team Integration
**Related Skills:** output-validation-checklist, source-verification, taxonomy-standards, feedback-integration
**Used By:** Documenters, ALL agents producing documentation, especially technical writers and API documenters