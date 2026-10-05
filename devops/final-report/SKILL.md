---
name: final-report
description: Consolidate all review findings into a structured 4-section report with codebase overview, executive summary, dual-view detailed findings (by feature and by.
---

# Code Review - Final Report

Consolidate all review findings into a comprehensive, structured report organized for readability and actionability. This skill is **Phase 6** of the 6-phase code review methodology.

## When to Use This Skill

Use this skill when you need to:

- Complete a comprehensive code review
- Consolidate findings from multiple phases
- Present findings grouped by functional area AND by priority
- Deliver executive summary with verdict and roadmap
- Export professional report in Markdown and Word formats
- Present next steps for user confirmation

**Trigger phrases**: "final report", "code review report", "consolidate findings", "review summary", "action plan", "remediation plan"

## What This Skill Does

### Report Sections

1. **Section 1: Codebase Overview**
   - High-level description of the codebase (purpose, target users, architecture)
   - Synthesized from Phase 1 context analysis

2. **Section 2: Executive Summary**
   - Overall verdict with statistics
   - Critical fixes (all P0 items, brief one-liners)
   - Functional groupings (which areas need the most work)
   - Redundancy and trimming recommendations
   - Roadmap perspective (short-term and long-term)

3. **Section 3: Detailed Report**
   - Phase 1: Findings grouped by feature/functionality (critical to low within each group)
   - Phase 2: Findings grouped by priority (P0 through P3 across all features)

4. **Section 4: Export**
   - Offered as option in the Next Steps menu
   - Generates Markdown and Word (.docx) via `generate_report.py`

## Overall Verdict

Assign one of three verdicts (mirroring GitHub PR review states):

| Verdict | When to Use |
|---------|-------------|
| **APPROVE** | No P0 or P1 findings. Code is ready to merge/ship. |
| **REQUEST_CHANGES** | P0 or P1 findings exist that should be resolved before proceeding. |
| **COMMENT** | No blocking issues, but P2/P3 suggestions are worth considering. |

## Inline Comment Format

For file-specific findings throughout the report, use this format:

```
::code-comment{file="path/to/file.ts" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

## Clean Review Protocol

If no issues are found in a phase (or overall), explicitly state:
- **What was checked**: List the specific areas, domains, and checklists applied
- **Areas not covered**: Any limitations or areas outside the review scope (and why)
- **Residual risks**: Potential concerns that could not be verified through static review alone
- **Recommended follow-up**: Suggested dynamic tests, load tests, or manual verification

## Feature Grouping Instructions

When building Section 3 Phase 1 (by feature), intelligently group findings into logical functional areas based on the actual codebase. Common groupings include (but are not limited to):

- **Authentication & Authorization** (login, tokens, roles, permissions, session management)
- **Error Handling & Logging** (exception handling, error messages, audit trails)
- **API Design & Endpoints** (request/response patterns, validation, routing)
- **Database & Session Management** (connections, queries, ORM patterns, migrations)
- **File Handling & Uploads** (file I/O, path handling, uploads, downloads, zip operations)
- **CI/CD Pipeline** (build scripts, deployment, testing stages, Jenkinsfile)
- **Security** (secrets management, input sanitization, CORS, headers)
- **Performance & Caching** (query optimization, caching strategy, timeouts)
- **Configuration & Environment** (env vars, settings, feature flags)
- **Testing & Quality** (test coverage, test quality, test infrastructure)

Name groups based on what the findings actually cover. If a group would contain only 1 finding, merge it into the most relevant adjacent group. Each group should have a brief summary sentence explaining why it needs attention.

## Report Template

```markdown
# Code Review Report

**Project**: [Name]
**Review Date**: [Date]
**Mode**: [Full Codebase / Git Changes]
**Files Reviewed**: [Count]
**Overall Verdict**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

# Section 1: Codebase Overview

[High-level description of the codebase: what it does, its purpose, target users, and core architecture. Synthesized from Phase 1 context analysis. Keep this to 1-2 paragraphs.]

---

# Section 2: Executive Summary

## Verdict: [APPROVE / REQUEST_CHANGES / COMMENT]

| Metric | Count |
|--------|-------|
| P0 (Critical) | [N] |
| P1 (High) | [N] |
| P2 (Medium) | [N] |
| P3 (Low) | [N] |
| **Total** | **[N]** |

**Risk Level**: [Low/Medium/High/Critical] - [Brief justification]

## Critical Fixes

Items requiring immediate attention (all P0 findings):

| # | Title | Location | One-Liner |
|---|-------|----------|-----------|
| 1 | [Title] | [file:line] | [Brief description of the issue] |
| 2 | [Title] | [file:line] | [Brief description of the issue] |

## Functional Groupings

A breakdown of which areas require the most work:

| Area | Findings | Severity Spread | Why It Needs Attention |
|------|----------|-----------------|------------------------|
| [e.g., Authentication] | [N] | P0: X, P1: Y, P2: Z | [Brief reason] |
| [e.g., Error Handling] | [N] | P1: X, P2: Y | [Brief reason] |

## Redundancy & Trimming

Opportunities to simplify and optimize the codebase by removing or consolidating redundant, unnecessary, or low-value elements. This goes beyond dead code to include dependencies, features, architecture, and components.

### Safe Removals (zero behavior impact)
- [Item]: [Why it can be removed without any impact]

### Simplifications (same outcome, less complexity)
- [Item]: [What to simplify and why the outcome stays the same]

### Trade-off Removals (pros/cons analysis required)

For each item below, removal may alter behavior or drop a feature, but the trade-off may be worthwhile:

**[Item Name]**: [Brief description]

| Aspect | Details |
|--------|---------|
| **What it does** | [Current function] |
| **Why consider removing** | [Complexity cost, maintenance burden, low usage] |
| **Pros of removing** | [Simpler architecture, fewer deps, less maintenance] |
| **Cons of removing** | [Lost functionality, migration effort, user impact] |
| **Recommendation** | [Remove / Keep / Replace with simpler alternative] |

[Repeat for each trade-off item]

## Roadmap Perspective

### Short-term (minimal effort, high value)
- [Functionality that could easily be added now]
- [Quick win improvement]

### Long-term (significant development required)
- [Feature that would be valuable but requires substantial work]
- [Architectural improvement worth planning for]

---

# Section 3: Detailed Report

## Phase 1: Grouped by Feature/Functionality

Findings organized into logical feature groups. Within each group, items are ordered from critical to low priority.

### [Feature Group Name] ([N] findings)

[Brief summary of why this area needs attention.]

#### [ID]. [Finding Title]
**Severity**: [P0/P1/P2/P3]
**File**: [path:line]
**Category**: [Security / Performance / Quality / SOLID / Testing]

**Issue**: [Description of the problem]

**Impact**: [What happens if this is not fixed]

**Fix**: [Recommended remediation]

**Effort**: [Low/Medium/High]

---

[Repeat for each feature group]

---

## Phase 2: Grouped by Priority

The same findings reorganized by priority level across all feature groups.

### P0 - Critical (must fix)

| # | Title | Feature Group | File | Impact | Fix |
|---|-------|---------------|------|--------|-----|
| 1 | [Title] | [Group] | [file:line] | [Impact] | [Fix summary] |

### P1 - High (should fix)

| # | Title | Feature Group | File | Impact | Fix |
|---|-------|---------------|------|--------|-----|
| 1 | [Title] | [Group] | [file:line] | [Impact] | [Fix summary] |

### P2 - Medium (recommended)

| # | Title | Feature Group | File | Impact | Fix |
|---|-------|---------------|------|--------|-----|
| 1 | [Title] | [Group] | [file:line] | [Impact] | [Fix summary] |

### P3 - Low (optional)

| # | Title | Feature Group | File | Impact | Fix |
|---|-------|---------------|------|--------|-----|
| 1 | [Title] | [Group] | [file:line] | [Impact] | [Fix summary] |

---

# Section 4: Export

This report can be exported as professional Markdown and Word (.docx) documents.

Select **option 5** from the Next Steps menu below to generate export files.

---

## Next Steps

Found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**
1. **Fix all** - I'll implement all suggested fixes across all severity levels
2. **Fix P0/P1 only** - Address the critical and high priority issues
3. **Fix specific items** - Tell me which issues to fix by number
4. **No changes** - Review complete, no implementation needed
5. **Export report** - Generate Markdown and Word (.docx) versions of this report
```

---

## Export Implementation

When the user selects **option 5 (Export report)**, follow these steps:

1. **Construct `code_review_data.json`** from the review findings using the schema below
2. **Save** the JSON file to the project root
3. **Run**: `python scripts/generate_report.py code_review_data.json --type code-review`
4. **Output**: `Code_Review_Report.md` and `Code_Review_Report.docx`

### Export JSON Schema

```json
{
  "title": "Code Review Report",
  "subtitle": "[Project Name] - Comprehensive Code Review",
  "header_subtitle": "Code Review Report",
  "author": "DevAI-Hub Agent",
  "review_date": "[Date]",
  "mode": "[Full Codebase / Git Changes]",
  "verdict": "[APPROVE / REQUEST_CHANGES / COMMENT]",
  "codebase_overview": "[Section 1 content as markdown string]",
  "executive_summary": {
    "statistics": { "p0": 0, "p1": 0, "p2": 0, "p3": 0, "total": 0 },
    "risk_level": "[Low/Medium/High/Critical]",
    "risk_justification": "[Brief justification]",
    "critical_fixes": "[Markdown string with the critical fixes table]",
    "functional_groupings": "[Markdown string with the functional groupings table]",
    "redundancy_trimming": {
      "safe_removals": "[Markdown string with safe removal items]",
      "simplifications": "[Markdown string with simplification items]",
      "trade_off_removals": "[Markdown string with pros/cons tables for each trade-off item]"
    },
    "roadmap": {
      "short_term": "[Markdown string with short-term items]",
      "long_term": "[Markdown string with long-term items]"
    }
  },
  "feature_groups": [
    {
      "name": "[Feature Group Name]",
      "summary": "[Why this area needs attention]",
      "finding_count": 0,
      "findings": [
        {
          "id": "[e.g., P0-1]",
          "severity": "[P0/P1/P2/P3]",
          "title": "[Finding Title]",
          "file": "[file path]",
          "line": "[line number or range]",
          "category": "[Security / Performance / Quality / SOLID / Testing]",
          "description": "[Issue description]",
          "impact": "[Impact description]",
          "fix": "[Remediation recommendation]",
          "effort": "[Low/Medium/High]"
        }
      ]
    }
  ],
  "removal_plan": "[Markdown string with removal recommendations, or empty string]",
  "methodology": "6-phase code review: Context Analysis, Code Quality + SOLID, Security (10 domains), Performance, Testing, Final Report"
}
```

---

## Next Steps Confirmation

**CRITICAL**: Do NOT implement any changes until the user explicitly confirms which fixes to apply.

After presenting the report, always end with the Next Steps menu. Wait for the user's selection before taking any action.

## Quality Checklist

- [ ] Section 1 (Codebase Overview) is present and accurate
- [ ] Section 2 (Executive Summary) includes all subsections: verdict, critical fixes, functional groupings, redundancy, roadmap
- [ ] Section 3 Phase 1 findings are intelligently grouped by feature area
- [ ] Section 3 Phase 2 findings are grouped by priority (P0 through P3)
- [ ] All findings appear in both Phase 1 and Phase 2 views (no missing items)
- [ ] Severity consistently classified (P0-P3)
- [ ] Overall verdict assigned (APPROVE / REQUEST_CHANGES / COMMENT)
- [ ] Remediation steps are actionable with code examples where applicable
- [ ] Effort estimates included for each finding
- [ ] Report professionally formatted
- [ ] Clean review protocol followed (if no issues found)
- [ ] Next steps menu presented with 5 options (including export)
- [ ] No changes implemented without user confirmation

## Related Skills

- `context-analysis` - Context understanding (Phase 1)
- `code-quality` - Code quality + SOLID + dead code review (Phase 2)
- `security-review` - Security analysis, 10-domain model (Phase 3)
- `performance-review` - Performance analysis (Phase 4)
- `testing-review` - Test assessment (Phase 5)

---

**Version**: 3.0.0
**Last Updated**: February 2026
**Based on**: DevAI-Hub code review methodology + code-review-expert


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
