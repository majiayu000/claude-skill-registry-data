---
name: status-report
description: "Expert guidance for creating weekly status reports for 8090 project management teams. Use when generating status reports, weekly updates, project progress reports, or team updates. Automatically finds previous week's report, gathers context from project files and meeting notes, and generates comprehensive status updates following the standardized format. Triggered by requests like 'create status report', 'generate weekly update', 'prepare project status', or 'create this week's status report'."
---

# Status Report Generator v1.0.0

**Version**: 1.0.0
**Last Updated**: 2025-11-17
**Format Change Date**: November 17, 2025

## Changelog

- **v1.0.0** (2025-11-17): Initial release with new status report format

---

## When to Use This Skill

Claude should invoke this skill when the user:
- Requests a "status report" for a project
- Asks to "create a weekly update" or "generate weekly status"
- Mentions "project status" or "team update"
- Asks to "prepare this week's status report"
- Requests updates for specific client projects
- Asks about progress reporting or project summaries

**Target Users**: Project Managers at 8090 managing client projects

---

## Overview

This skill enables automated generation of weekly status reports for client projects at 8090. It follows a standardized format (adopted November 17, 2025) that provides executives and stakeholders with clear visibility into:
- Project phase and timeline adherence
- Key deadlines and cumulative delays
- Upcoming demos and releases
- Blockers requiring attention
- Engineering team allocation and quality metrics

---

## How to Use This Skill

### ALWAYS Follow This Sequence:

**Step 1: Identify Project Context**
- Determine the client name and project name
- Identify the current working directory or project folder
- If not specified, ask the user which project/client they need the report for

**Step 2: Find Previous Week's Status Report**
- Search for files matching pattern: `*Client*Project*YYYYMMDD.*` or `CATEGORY_Client_Project_YYYYMMDD.*`
  - Example: `HEALTH_HealthCorp_PatientPortal_20251112.pdf`
- Look for the most recent status report (sorted by date in filename)
- Read the previous report to understand:
  - Current project phase and specific activities
  - Existing deadlines and delays (note: deadline names may be project-specific)
  - Previous blockers and their status/resolution
  - Team composition and allocation
  - Historical context and decisions

**Step 3: Gather This Week's Context**
- Search project folder for recent updates:
  - Meeting notes or transcripts from the past week
  - Updated requirements or specifications
  - Development logs or commit messages
  - Email correspondence (if available in project files)
  - Demo recordings or notes
  - Release notes or deployment logs
- Look for information about:
  - Progress on active work items
  - New blockers or risks
  - Completed milestones
  - Upcoming deadlines
  - Team time allocation changes

**Step 4: Generate Status Report**
- Use the template format specified in [template.md](template.md)
- Filename format: `CATEGORY_ClientName_ProjectName_YYYYMMDD.md` (use current date)
- Fill in all required sections:
  - Update project phase with descriptive context (not just "DEVELOPMENT" - be specific like "Active Development (API Integration)")
  - Use project-specific deadline names (adapt to project reality, don't force generic names)
  - Calculate cumulative delays from original baselines
  - Update demo/release dates with context
  - **CRITICAL**: Identify and prioritize blockers with Risk Levels (High/Medium/Low)
  - Add "Work This Week" narrative of completed activities
  - Add "Next Steps" forward-looking action items
  - Create detailed Notes with bullet points (can use FYI format or descriptive labels)
  - Update "Software Factory Usage and Feedback" table with time and ratings on separate lines
- **MOST IMPORTANT**: Blockers section drives executive action - include specific names, dates, risk levels

**Step 5: Quality Control**
- Verify all date fields are populated or marked "N/A"
- Confirm cumulative delays are accurate
- Ensure blockers are clearly stated and prioritized
- Check that engineer metrics reflect actual time spent
- Review notes for relevance and clarity

---

## Status Report Format

The new format (effective November 17, 2025) is **flexible and narrative-driven**, adapting to each project's reality while maintaining consistent structural elements.

### Header Section
- Filename with category prefix: `CATEGORY_Client_Project_YYYYMMDD`
- Client name and project name
- Client POC (first and last name)
- **Descriptive Current Phase** (not rigid categories): Examples:
  - "Active Development (API Integration and Prompt Refinement)"
  - "Requirements Gathering and PRD Development"
  - "Maintenance (Post-Launch Support and Enhancement)"

### Timeline Section
**Project-specific deadlines** with cumulative delay tracking:
- Use deadline names that match project milestones (not forced generic names)
- Examples: "Demo-Ready Application Deadline", "PRD Acceptance Deadline", "Pilot Launch Deadline"
- Each deadline includes a context paragraph explaining its purpose
- Format: `[Deadline Name]: [Date], Cumulative Delay: [X days]`

### Milestones Section
- Date of Next Exec Demo (with description)
- Date of Next Minor Demo (with description or N/A)
- Date of Next Release (with description)
- Date of Last Release (with description)

### Status Section
- **Blockers or Potential Blockers** (MOST IMPORTANT)
  - Include Risk Level: High/Medium/Low
  - Detailed descriptions with specific names, dates, meeting times
  - Impact statements
- **Notes**: Contextual information with descriptive bullet points
- **Work This Week**: Narrative of completed activities
- **Next Steps**: Forward-looking action items

### Software Factory Usage and Feedback
Table showing engineer allocation across four categories:
- **Refinery**: Requirements gathering and analysis
- **Foundry**: Core development and implementation
- **Planner**: Project planning and coordination
- **Validator**: Testing and quality assurance

**Important**: Time and quality rating on **separate lines** in each cell
- Format: `X hrs` then `Rating: X out of 5`

See [template.md](template.md) for the complete format structure and [examples.md](examples.md) for real-world examples.

---

## Key Principles

### 1. Format Flexibility with Structural Consistency
**MUST**: Adapt deadline names, phase descriptions, and narrative to each project's reality
**MUST**: Maintain consistent structural elements (header, deadlines, demos, blockers, notes, work sections, metrics)
**SHOULD**: Use project-specific language rather than forcing generic terms
**WHY**: Reports must reflect actual project context while remaining parseable and consistent

### 2. Accuracy Over Speed
**MUST**: Verify all dates and delays against previous reports and actual project timeline
**WHY**: Executives make decisions based on this data

### 3. Blockers Are Critical
**MUST**: The "Blockers or Potential Blockers" section is marked as MOST IMPORTANT
**MUST**: Include Risk Level (High/Medium/Low) for each blocker
**MUST**: Include specific stakeholder names, dates, and meeting times
**MUST**: List blockers in priority order (highest impact first)
**MUST**: Be specific about what's blocked, why, and what's needed to unblock
**WHY**: This section drives executive action and resource allocation

### 4. Cumulative Delay Tracking
**MUST**: Calculate delays from original baseline dates, not previous week's dates
**MUST**: Show "0 days" explicitly if no delay exists (not blank)
**MUST**: Use lowercase "days" format consistently
**WHY**: Maintains accountability and trend visibility

### 5. Narrative Context Required
**MUST**: Include "Work This Week" section with completed activities
**MUST**: Include "Next Steps" section with upcoming work
**SHOULD**: Make blockers and notes descriptive with specific details
**SHOULD**: Add context paragraphs after deadlines explaining their significance
**WHY**: Stakeholders need narrative context, not just data points

### 6. Phase-Appropriate Content
Phases should be descriptive, but typical patterns:

**Requirements/Refinery-Heavy Phase**:
- Focus on acceptance deadline for requirements
- Demo dates often for requirements review
- Validator time typically low
- High Refinery allocation

**Active Development Phase**:
- Demo dates should be populated
- Development completion deadline is critical
- Foundry time typically highest
- Balance across all four categories

**Maintenance Phase**:
- Focus on last release date and next patch/enhancement release
- Demos typically N/A unless major update
- Lower overall time allocation
- Higher Validator proportion

### 7. Engineer Metrics Reflect Reality
**MUST**: Use "Software Factory Usage and Feedback" as section title
**MUST**: Time and rating on separate lines in table cells
**MUST**: Time spent should align with actual allocation (not aspirational)
**MUST**: Format ratings as "Rating: X out of 5"
**MUST**: Use "N/A" for categories where engineer didn't contribute
**MAY**: Include engineers who contributed any time, even minimal

### 8. Notes Are Actionable or Informative
**SHOULD**: Each note provides value to stakeholders
**SHOULD**: Order notes by importance
**AVOID**: Operational details that don't affect project status

---

## File Structure

```
.claude/skills/status-report/
├── SKILL.md          # This file - main instructions
├── template.md       # Complete format template
└── examples.md       # Sample reports for different phases
```

---

## Troubleshooting

**Problem**: Can't find previous week's report
**Solution**: Ask user for location or create initial baseline report

**Problem**: Unclear which phase project is in
**Solution**: Check recent milestones and active work to infer phase, or ask user

**Problem**: Multiple engineers with same role
**Solution**: Add rows to engineer table as needed (Eng #1, Eng #2, etc.)

**Problem**: Cumulative delay calculation unclear
**Solution**: Find original baseline deadline in earliest reports, calculate days from that date to current deadline

---

## Response Format

When this skill is invoked, follow this response structure:

```markdown
I'll generate the weekly status report for [Client] - [Project].

**Step 1**: Finding previous status report...
[Report what was found]

**Step 2**: Gathering this week's context...
[Summarize what context was found: meetings, updates, changes]

**Step 3**: Generating status report...

---

[GENERATED STATUS REPORT CONTENT]

---

**Status Report**: Created `ClientName_ProjectName_YYYYMMDD.md`

Would you like me to:
- Save this to a specific location?
- Make any adjustments to the content?
- Add additional context or notes?
```

---

## Quality Control Checklist

Before finalizing the status report, verify:

- [ ] Filename follows `Client_Project_YYYYMMDD` format with current date
- [ ] Client name and Project name are correct
- [ ] Client POC name is accurate (first and last name)
- [ ] Current phase is one of: REQUIREMENTS / DEVELOPMENT / MAINTENANCE
- [ ] All three deadline fields are populated with dates
- [ ] Cumulative delays are calculated from original baseline (0 if on time)
- [ ] Acceptance timing questions answered for each deadline
- [ ] Demo dates are appropriate for current phase (N/A if not applicable)
- [ ] Release dates reflect actual schedule (N/A if not applicable)
- [ ] Blockers section clearly identifies issues requiring attention
- [ ] Blockers are prioritized by impact
- [ ] Notes provide valuable context for stakeholders
- [ ] Engineer table includes all active contributors
- [ ] Time spent values reflect actual allocation
- [ ] Quality scores are rated 1-5 for each category
- [ ] All sections are complete (no "TODO" or blank fields)

---

## Version History Note

**IMPORTANT**: Status reports created before November 17, 2025 use a different format. When referencing historical reports, be aware they may not contain all fields in the current template. Extract whatever information is available and note any missing baseline data in the current report's notes section if relevant.

---

## For More Information

- See [template.md](template.md) for the complete format specification
- See [examples.md](examples.md) for sample reports across different project phases
- Refer to project-specific CLAUDE.md files for client context and conventions
