---
name: Generic Completion Report
description: Generate completion reports from template for any project. Use when phase complete, milestone reached, or user says "create completion report" or "phase done". Ensures standardized project documentation and progress tracking.
allowed-tools: Read, Write
version: 1.0.0
---

# Generic Completion Report

## Purpose
Generate standardized completion reports for project phases, milestones, and deliverables using template-based approach.

## When This Activates
- User says "phase complete", "create completion report", "phase done"
- User finishes implementation and says "finished", "complete"
- User attempts to start new phase without completing previous
- Milestone completion detected

## Prerequisites
- [ ] Phase/milestone actually complete
- [ ] Deliverables implemented
- [ ] Testing completed

## Configuration Required

**Projects must provide:**
- `${PROJECT_REPORT_PATH}` - Where to save reports
- `${PROJECT_REPORT_FORMAT}` - Report naming convention
- `${PROJECT_SECTIONS}` - Required report sections (optional, defaults to standard 10)

---

## Steps

### Step 1: Check for Project Configuration
Load project-specific completion-report skill if exists in `.claude/skills/completion-report/`

### Step 2: Load Report Template
Read [templates/completion-report-template.md](templates/completion-report-template.md)

### Step 3: Gather Completion Information
Collect from user and codebase:
- Phase/milestone name
- Completion date
- Objectives achieved
- Deliverables completed
- Files modified/created
- Metrics (lines of code, tests, performance)
- Issues encountered and resolved
- Lessons learned
- Next steps

### Step 4: Analyze Implementation
- Use Grep/Glob to identify files changed since phase start
- Check git log for commits during phase
- Identify test files added
- Calculate metrics

### Step 5: Populate Template
Replace all placeholders with gathered information

### Step 6: Write Report
If configured: Write to `${PROJECT_REPORT_PATH}`
Otherwise: Provide as text output

### Step 7: Trigger Next Steps (if configured)
- May invoke master-plan-update skill
- May suggest starting next phase

---

## Output
- Complete completion report document
- Written to file or provided as text
- Summary of achievements

---

## Examples

See template for complete report structure

---

## Changelog

### Version 1.0.0 (2025-10-20)
- Initial release

---

**End of Skill**
