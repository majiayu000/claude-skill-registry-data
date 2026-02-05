---
name: JIRA Ticket Hygiene Checker
description: Validates JIRA tickets have required fields and sufficient information for development. Activates when users ask about ticket quality, readiness, or completeness, or when reviewing tickets before sprint planning.
---

# JIRA Ticket Hygiene Skill

## When to Use This Skill

Activate this skill when the user:
- Asks if a ticket is "ready", "complete", or "well-defined"
- Asks about ticket quality or completeness
- Wants to review a ticket before sprint planning
- Asks "does this ticket have enough information?"
- Wants to validate tickets meet team standards
- Asks about missing fields or requirements

## Hygiene Checklist

### Required Fields (Must Have)
- [ ] **Title**: Clear, actionable, under 100 characters
- [ ] **Description**: Detailed context (recommend > 100 characters)
- [ ] **Acceptance Criteria**: At least 2 clear, testable criteria
- [ ] **Story Points**: Set for Stories, Tasks, and Bugs (use scale: 0, 1, 3, 5, 8, 13)
- [ ] **Assignee**: Someone owns the ticket
- [ ] **Component**: Assigned to track by area
- [ ] **Activity Type**: Must be set for capacity planning (see Activity Types below)

### Recommended Fields
- [ ] **Labels**: At least 1 relevant label
- [ ] **Epic Link**: Connected to parent epic (for Stories)
- [ ] **Fix Version**: Target release identified
- [ ] **Priority**: Explicitly set (not just default)

### Quality Checks
- [ ] No ambiguous language ("maybe", "probably", "TBD", "possibly")
- [ ] Technical approach outlined or referenced
- [ ] Dependencies identified and linked
- [ ] Not a duplicate of existing ticket
- [ ] Scope is achievable in one sprint

## How to Check a Ticket

Use jira-cli to fetch ticket details:

```bash
jira issue view TICKET-KEY --plain 2>/dev/null
```

For JSON output with all fields:
```bash
jira issue view TICKET-KEY --json 2>/dev/null
```

## Output Format

When analyzing a ticket, provide:

### Ticket: TICKET-KEY

**Summary:** [Ticket title]

#### Hygiene Assessment

| Check | Status | Notes |
|-------|--------|-------|
| Title | PASS/FAIL | [Issue if any] |
| Description | PASS/FAIL | [Length: X chars] |
| Acceptance Criteria | PASS/FAIL | [Count: X criteria] |
| Story Points | PASS/FAIL | [Value or "Missing"] |
| Assignee | PASS/FAIL | [Name or "Unassigned"] |
| Component | PASS/FAIL | [Component or "None"] |
| Activity Type | PASS/FAIL | [Type or "Uncategorized"] |

#### Overall Score: X/7 Required Checks Passed

#### Verdict
- **READY FOR SPRINT** - All required fields present, good quality
- **NEEDS MINOR FIXES** - 1-2 issues to address
- **NOT READY** - Multiple critical issues

#### Recommended Actions
1. [Specific action to fix issue 1]
2. [Specific action to fix issue 2]

## Activity Types (Sankey Capacity Allocation)

Activity Type is **required** for sprint/kanban capacity planning. Tickets without an Activity Type appear as "Uncategorized" and cannot be properly allocated.

### Reactive Work (Non-Negotiable First)
| Activity Type | Description | Examples |
|---------------|-------------|----------|
| **Associate Wellness & Development** | Onboarding, team growth, training, associate experience | Training sessions, mentorship |
| **Incidents & Support** | Escalations, production issues | Customer escalations, outages |
| **Security & Compliance** | Vulnerabilities and weaknesses, CVEs | Security patches, compliance fixes |

### Core Principles (Quality Focus)
| Activity Type | Description | Examples |
|---------------|-------------|----------|
| **Quality / Stability / Reliability** | Bugs, SLOs, chores, tech debt, PMR action items, toil reduction | Bug fixes, performance improvements |

### Proactive Work (Balance Remaining Capacity)
| Activity Type | Description | Examples |
|---------------|-------------|----------|
| **Future Sustainability** | Productivity improvements, team improvements, upstream, proactive architecture, enablement | Tooling, automation, refactoring |
| **Product / Portfolio Work** | Strategic portfolio (HATSTRAT), strategic product, product outcome, BU features | New features, product enhancements |

### Priority Order
1. **Non-Negotiable**: Achieve SLAs for Escalations & CVEs
2. **Core Principles**: Reduce bug backlog, ensure quality/stability/reliability
3. **Then Balance**: Set up for long-term success by balancing remaining capacity between Future Sustainability and Product Work

## Red Flags to Highlight

- Descriptions under 50 characters
- "TBD" or placeholder text in any field
- Story points of 13+ (must be broken down)
- No acceptance criteria at all
- Vague titles like "Fix bug" or "Update feature"
- Tickets open > 30 days without progress
- **Missing Activity Type** (appears as Uncategorized in capacity planning)

## Integration with Commands

This skill complements the `/hygiene-check` command:
- Command: Bulk audit of sprint tickets
- Skill: Deep-dive on individual ticket quality
