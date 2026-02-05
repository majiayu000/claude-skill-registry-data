---
name: cognitive-load-assessment
description: Measure and manage team cognitive load
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Cognitive Load Assessment Skill

## When to Use This Skill

Use this skill when:

- **Cognitive Load Assessment tasks** - Working on measure and manage team cognitive load
- **Planning or design** - Need guidance on Cognitive Load Assessment approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Measure and manage team cognitive load to optimize productivity and sustainability.

## MANDATORY: Documentation-First Approach

Before assessing cognitive load:

1. **Invoke `docs-management` skill** for cognitive load patterns
2. **Verify concepts** via MCP servers (perplexity)
3. **Base guidance on cognitive load theory and Team Topologies**

## Cognitive Load Theory for Teams

```text
Three Types of Cognitive Load:

┌─────────────────────────────────────────────────────────────┐
│                    TOTAL COGNITIVE LOAD                     │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐    │
│  │   INTRINSIC   │  │  EXTRANEOUS   │  │    GERMANE    │    │
│  │   (Domain)    │  │  (Accidental) │  │  (Learning)   │    │
│  │               │  │               │  │               │    │
│  │ • Business    │  │ • Bad tools   │  │ • New skills  │    │
│  │   complexity  │  │ • Tech debt   │  │ • Growth      │    │
│  │ • Domain      │  │ • Manual      │  │ • Innovation  │    │
│  │   knowledge   │  │   processes   │  │               │    │
│  └───────────────┘  └───────────────┘  └───────────────┘    │
│                                                              │
│  GOAL: Reduce extraneous, manage intrinsic, allow germane   │
└─────────────────────────────────────────────────────────────┘
```

## Intrinsic Cognitive Load

```text
INTRINSIC LOAD: Inherent complexity of the domain

Sources:
• Business domain complexity
• Required domain knowledge
• Problem space difficulty
• Integration complexity
• Compliance requirements

Management Strategies:
• Clear bounded contexts
• Domain-driven design
• Right team for right domain
• Specialists where needed
• Documentation and training

Assessment Questions:
□ How complex is the business domain?
□ How much domain knowledge is required?
□ How many systems must team understand?
□ How many stakeholders to coordinate with?
□ How complex are compliance requirements?
```

## Extraneous Cognitive Load

```text
EXTRANEOUS LOAD: Unnecessary complexity (waste)

Sources:
• Poor tooling and processes
• Technical debt
• Unclear requirements
• Manual deployments
• Legacy systems
• Poor documentation
• Meeting overload

Management Strategies:
• Invest in developer experience
• Reduce technical debt
• Automate repetitive tasks
• Clear communication
• Self-service platforms
• Reduce handoffs

Assessment Questions:
□ How much time on non-value work?
□ How painful are deployments?
□ How much context switching?
□ How many manual processes?
□ How much waiting for others?
```

## Germane Cognitive Load

```text
GERMANE LOAD: Productive learning and growth

Sources:
• Learning new technologies
• Skill development
• Innovation work
• Process improvement
• Mastering the domain

Management Strategies:
• Protected learning time
• Conference attendance
• Hackathons
• Mentoring programs
• Stretch assignments

Assessment Questions:
□ How much time for learning?
□ How much innovation work?
□ Are people growing skills?
□ Is knowledge being shared?
□ Is there time for experimentation?
```

## Cognitive Load Assessment

### Assessment Framework

```text
Team Cognitive Load Formula:

TOTAL LOAD = Intrinsic + Extraneous + Germane

HEALTHY: Total Load < Capacity
STRESSED: Total Load ≈ Capacity
OVERLOADED: Total Load > Capacity

Capacity Factors:
• Team size
• Experience level
• Tool quality
• Process maturity
• Support availability
```

### Assessment Questionnaire

```text
Rate each item 1-5 (1=Low load, 5=High load):

INTRINSIC LOAD (Domain Complexity)
□ ___ Business domain complexity
□ ___ Number of systems owned
□ ___ Integration complexity
□ ___ Stakeholder coordination
□ ___ Compliance requirements
Intrinsic Score: ___/25

EXTRANEOUS LOAD (Unnecessary Complexity)
□ ___ Tooling and infrastructure friction
□ ___ Manual processes and deployments
□ ___ Technical debt burden
□ ___ Waiting time for dependencies
□ ___ Context switching frequency
Extraneous Score: ___/25

GERMANE LOAD (Learning & Growth)
□ ___ New technology adoption rate
□ ___ Process change frequency
□ ___ Skill development demands
□ ___ Innovation expectations
□ ___ Documentation/training work
Germane Score: ___/25

TOTAL COGNITIVE LOAD: ___/75

Interpretation:
< 30: Low load (capacity available)
30-45: Moderate load (sustainable)
45-60: High load (at risk)
> 60: Overloaded (unsustainable)
```

## Domain Complexity Assessment

### Domain Complexity Matrix

| Factor | Low (1) | Medium (3) | High (5) |
|--------|---------|------------|----------|
| **Entities** | <10 | 10-50 | >50 |
| **Rules** | Simple | Moderate | Complex |
| **Integrations** | 0-2 | 3-5 | >5 |
| **Stakeholders** | 1-2 | 3-5 | >5 |
| **Regulations** | None | Some | Heavy |

### Team-Domain Fit

```text
Domain Size Assessment:

SMALL DOMAIN (Team can fully own):
• Limited bounded context
• Clear boundaries
• Manageable complexity
• 5-9 person team appropriate

MEDIUM DOMAIN (Stretching team limits):
• Multiple sub-domains
• Some complexity
• Some dependencies
• May need splitting

LARGE DOMAIN (Team overloaded):
• Multiple bounded contexts
• High complexity
• Many dependencies
• MUST split into multiple teams
```

## Cognitive Load Reduction Strategies

### Reduce Extraneous Load

```text
Platform Strategies:
• Self-service infrastructure
• Golden paths for common tasks
• Automated testing and deployment
• Centralized observability
• Clear documentation

Process Strategies:
• Reduce meetings
• Async communication
• Clear ownership
• Reduce handoffs
• Eliminate approval bottlenecks

Tooling Strategies:
• Developer experience investment
• IDE integration
• Local development parity
• Fast feedback loops
• Reduced context switching
```

### Manage Intrinsic Load

```text
Team Design Strategies:
• Right-size bounded contexts
• Align teams to domains
• Specialists for complex subsystems
• Clear team APIs
• Reduce dependencies

Knowledge Strategies:
• Domain documentation
• Onboarding programs
• Pair programming
• Knowledge sharing
• Cross-training
```

### Protect Germane Load

```text
Learning Strategies:
• 20% time for learning
• Conference budget
• Training programs
• Innovation sprints
• Mentoring relationships

Growth Strategies:
• Stretch assignments
• Rotation programs
• Leadership development
• Technical career tracks
• Community involvement
```

## Assessment Template

```markdown
# Cognitive Load Assessment: [Team Name]

## Team Profile
- **Size:** [N people]
- **Age:** [Months/years together]
- **Domain:** [Description]
- **Current Load:** [High/Medium/Low]

## Intrinsic Load Analysis

### Domain Complexity
[Description of domain complexity]

### Score: [X/25]

| Factor | Score | Notes |
|--------|-------|-------|
| Business complexity | [1-5] | [Details] |
| Systems owned | [1-5] | [Details] |
| Integration complexity | [1-5] | [Details] |
| Stakeholder coordination | [1-5] | [Details] |
| Compliance requirements | [1-5] | [Details] |

## Extraneous Load Analysis

### Pain Points
[Description of unnecessary complexity]

### Score: [X/25]

| Factor | Score | Notes |
|--------|-------|-------|
| Tooling friction | [1-5] | [Details] |
| Manual processes | [1-5] | [Details] |
| Technical debt | [1-5] | [Details] |
| Waiting/blocking | [1-5] | [Details] |
| Context switching | [1-5] | [Details] |

## Germane Load Analysis

### Learning Capacity
[Description of learning demands]

### Score: [X/25]

| Factor | Score | Notes |
|--------|-------|-------|
| New technology | [1-5] | [Details] |
| Process changes | [1-5] | [Details] |
| Skill development | [1-5] | [Details] |
| Innovation work | [1-5] | [Details] |
| Documentation work | [1-5] | [Details] |

## Total Assessment

| Load Type | Score | Status |
|-----------|-------|--------|
| Intrinsic | [X/25] | [Good/Warning/Critical] |
| Extraneous | [X/25] | [Good/Warning/Critical] |
| Germane | [X/25] | [Good/Warning/Critical] |
| **Total** | **[X/75]** | **[Overall status]** |

## Recommendations

### Immediate Actions (Reduce Extraneous)
1. [Action]
2. [Action]

### Short-term (Manage Intrinsic)
1. [Action]
2. [Action]

### Long-term (Protect Germane)
1. [Action]
2. [Action]

## Reassessment Schedule
- Next review: [Date]
- Metrics to track: [List]
```

## Workflow

When assessing cognitive load:

1. **Gather Team Input**: Survey or interview team members
2. **Score Each Type**: Rate intrinsic, extraneous, germane
3. **Identify Hotspots**: Where is load highest?
4. **Analyze Causes**: Why is load high?
5. **Prioritize Reductions**: Focus on extraneous first
6. **Plan Actions**: Specific improvements
7. **Track Progress**: Reassess periodically

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
