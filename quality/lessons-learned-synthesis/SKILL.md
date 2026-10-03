---
name: lessons-learned-synthesis
description: >
  Use when analyzing patterns across multiple incidents, bugs, failures, or successes
  to extract organizational learning. This skill provides procedures for synthesizing
  individual experiences into actionable lessons that improve team-wide practices.
---

# Lessons Learned Synthesis

## Overview
This skill defines how to identify patterns across multiple events (incidents, bugs, successes, failures) and extract actionable lessons for the organization. Individual experiences create data; synthesis creates wisdom.

## When to Use
- After multiple similar incidents or bugs occur
- After completing a significant project or milestone
- When reviewing quarterly or annual performance data
- When recurring patterns are noticed across different agents or teams
- Before defining new standards, practices, or training programs
- **Don't use when:** Only one or two isolated events - use knowledge-capture instead

## Core Procedures

### Step 1: Gather Data
Collect relevant events for synthesis:
- Incident reports and post-mortems
- Bug reports and root cause analyses
- Project retrospectives and feedback
- Success stories and best practices
- Customer or stakeholder feedback
- Metrics showing trends over time

### Step 2: Identify Patterns
Look across events for:
- **Recurring Root Causes:** Same underlying issue appearing in different forms
- **Process Gaps:** Steps or checks that are consistently missing
- **Skill Gaps:** Errors that indicate knowledge or training needs
- **System Weaknesses:** Components or areas where failures cluster
- **Success Patterns:** Practices that consistently produce good results

### Step 3: Extract Lessons
For each pattern:
```
LESSON LEARNED
==============
Pattern: [what pattern was observed]
Evidence: [specific events that demonstrate this pattern]
Lesson: [what we should do differently based on this pattern]
Scope: [who/what this applies to]
Priority: [urgency of implementing the lesson]
Type: [new practice / improvement / warning / prevention]
```

### Step 4: Validate Lessons
- Are lessons based on data, not anecdotes?
- Are lessons actionable (not vague observations)?
- Are lessons specific enough to guide action but broad enough to be useful beyond one case?
- Would implementing this lesson have prevented or mitigated past occurrences?

### Step 5: Disseminate and Apply
- Add validated lessons to relevant knowledge bases
- Update standard procedures and checklists where applicable
- Share with relevant teams through status-reporting
- Track implementation of lessons through completion
- Review previously captured lessons quarterly for relevance

## Quality Checklist
- [ ] Lessons based on multiple data points, not isolated events
- [ ] Each lesson is specific, actionable, and evidence-based
- [ ] Scope and applicability clearly defined
- [ ] Relevant teams notified of lessons
- [ ] Procedures updated where lessons apply
- [ ] Implementation of lessons tracked

## Error Handling
- **Error:** Pattern is clear but lesson is impractical to implement
  **Response:** Document the constraint, look for alternative approach, escalate if systematic barrier
- **Error:** Lessons conflict with existing practices
  **Response:** Trigger conflict-resolution, update existing practices if lesson is stronger
- **Error:** Too many lessons, unclear priorities
  **Response:** Prioritize by frequency of pattern × impact of implementation, address top first

## Cross-Team Integration
**Related Skills:** knowledge-capture, continuous-improvement, incident-response, conflict-resolution
**Used By:** Quality agents, governance agents, project managers, trainers, organizational improvement leads