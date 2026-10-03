---
name: handoff-protocol
description: >
  Use when passing work, tasks, or deliverables between agents. This skill provides
  a standardized protocol for agent-to-agent handoffs, ensuring context, requirements,
  and expectations are clearly communicated during task delegation or escalation.
---

# Handoff Protocol

## Overview
This skill defines the standardized protocol for transferring work between agents. Proper handoffs prevent context loss, reduce errors, and ensure the receiving agent has everything needed to succeed. All agents should use this protocol when delegating, escalating, or transferring work.

## When to Use
- When delegating a task to another agent
- When escalating an issue that's outside your capability
- When transferring work between companies or divisions
- When passing deliverables to the next stage in a workflow
- **Don't use when:** Work can be completed independently without coordination

## Core Procedures

### Pre-Handoff Preparation
1. **Package the Work** - Gather all relevant artifacts, context, and decisions made
2. **Document Current State** - Write what's been done, what's pending, what's blocked
3. **Define Expected Outcome** - Clearly state what the receiving agent should accomplish
4. **Identify Constraints** - Note deadlines, quality standards, or limitations

### Handoff Communication Structure
Use this format for all handoffs:

```
HANDOFF TO: [target-agent-name]
FROM: [your-agent-name]
TASK: [brief description]

CONTEXT:
- Background: [why this task exists]
- What's done: [completed work and decisions made]
- What's needed: [specific work requested from receiver]

ARTIFACTS:
- [List all files, data, or resources being transferred]
- [Include paths, IDs, or links to locate them]

CONSTRAINTS:
- Deadline: [when this must be completed]
- Quality standard: [expected quality level]
- Dependencies: [other work or agents this depends on]

EXPECTED DELIVERABLE:
- [What the receiving agent should produce]
- [Format, location, and naming requirements]

ESCALATION PATH:
- If blocked: [who to contact or what to do]
- If unclear requirements: [how to get clarification]
```

### Post-Handoff Follow-up
1. **Confirm Receipt** - Wait for acknowledgment from receiving agent
2. **Provide Support** - Be available for clarification questions
3. **Track Progress** - Monitor handoff status through heartbeat or status updates

## Quality Checklist
- [ ] All relevant artifacts included and accessible
- [ ] Current state clearly documented (what's done vs pending)
- [ ] Expected outcome unambiguously defined
- [ ] Constraints and deadlines explicitly stated
- [ ] Escalation path provided for blockers

## Error Handling
- **Error:** Receiving agent rejects handoff (missing information)
  **Response:** Provide missing information immediately, retry handoff
- **Error:** Receiving agent unavailable
  **Response:** Escalate to their manager/CEO, or queue for next available agent
- **Error:** Handoff context too large for single message
  **Response:** Split into multiple handoffs, each with clear scope and dependencies

## Cross-Team Integration
**Related Skills:** escalation-management, status-reporting, conflict-resolution, knowledge-transfer
**Used By:** ALL agents when delegating or transferring work