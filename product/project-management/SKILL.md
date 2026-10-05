---
name: project-management
description: Project planning, task tracking, and team coordination for software development. Use for sprint planning, backlog grooming, task breakdown, dependency analysis, progress tracking, and stakeholder communication.
---

# Project Management

Plan, track, and coordinate software development projects effectively.

## Task Breakdown

### Work Decomposition
1. Break features into deliverable units (1-3 day effort)
2. Identify dependencies between tasks
3. Define clear acceptance criteria
4. Estimate complexity (not time)

### Task Sizing (Story Points)
| Points | Description |
|--------|-------------|
| 1 | Trivial change, well-understood |
| 2 | Small task, minor complexity |
| 3 | Medium task, some unknowns |
| 5 | Larger task, multiple components |
| 8 | Complex task, significant effort |
| 13 | Very complex, consider splitting |

## Sprint Planning

### Capacity Planning
```
Available capacity = Team size × Days × Focus factor (0.6-0.8)
Recommended commitment = 70-80% of capacity
Buffer = 20-30% for unknowns
```

### Sprint Structure
1. **Planning** - Select and commit to sprint goals
2. **Daily sync** - Blockers, progress, coordination
3. **Development** - Execute on committed work
4. **Review** - Demo completed work
5. **Retrospective** - Process improvements

## Dependency Analysis

### Identify Dependencies
- Technical: APIs, data schemas, libraries
- Resource: People, environments, tools
- External: Third-party services, approvals

### Critical Path
1. Map all task dependencies
2. Identify longest path to completion
3. Prioritize critical path tasks
4. Monitor for delays

## Progress Tracking

### Key Metrics
- **Velocity**: Points completed per sprint
- **Burn-down**: Remaining work over time
- **Cycle time**: Start to completion duration
- **Blocked time**: Time waiting on dependencies

### Status Categories
```
Not Started → In Progress → In Review → Done
                    ↓
                 Blocked (note blocker)
```

## Stakeholder Communication

### Status Updates
```
## Project Status: [Project Name]
**Date**: [Date]
**Health**: [Green/Yellow/Red]

### Completed This Period
- [Accomplishments]

### In Progress
- [Current work]

### Upcoming
- [Next priorities]

### Risks/Blockers
- [Issues needing attention]
```

### Escalation Triggers
- Blocked for >2 days without resolution path
- Scope change affecting timeline >20%
- Critical dependency at risk
- Resource conflicts

## Risk Management

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Description] | Low/Med/High | Low/Med/High | [Plan] |

### Common Risks
- Scope creep: Define clear boundaries, change process
- Technical debt: Allocate capacity for maintenance
- Key person dependency: Document, cross-train
- Integration issues: Early integration testing

## Team Coordination

### Handoffs
1. Document context and decisions
2. Update task status and notes
3. Notify receiving party
4. Verify understanding

### Conflict Resolution
1. Identify root cause (technical vs process)
2. Gather perspectives from all parties
3. Focus on project goals, not positions
4. Document decision and rationale
