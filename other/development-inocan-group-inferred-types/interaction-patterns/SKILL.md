---
name: interaction-patterns
description: Team interaction modes and their evolution over time
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Team Interaction Patterns Skill

## When to Use This Skill

Use this skill when:

- **Interaction Patterns tasks** - Working on team interaction modes and their evolution over time
- **Planning or design** - Need guidance on Interaction Patterns approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Define and evolve team interaction modes using Team Topologies interaction patterns.

## MANDATORY: Documentation-First Approach

Before defining interaction patterns:

1. **Invoke `docs-management` skill** for interaction mode guidance
2. **Verify Team Topologies concepts** via MCP servers (perplexity)
3. **Base guidance on Skelton & Pais interaction modes**

## Three Core Interaction Modes

```text
Team Topologies Interaction Modes:

┌─────────────────────────────────────────────────────────────────┐
│                    INTERACTION MODES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   COLLABORATION                           │  │
│  │                                                           │  │
│  │   ┌───────┐            ┌───────┐                         │  │
│  │   │ Team  │◄──────────►│ Team  │                         │  │
│  │   │   A   │  working   │   B   │                         │  │
│  │   └───────┘  together  └───────┘                         │  │
│  │                                                           │  │
│  │   High bandwidth • Shared goals • Time-limited           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  X-AS-A-SERVICE                           │  │
│  │                                                           │  │
│  │   ┌───────┐            ┌───────┐                         │  │
│  │   │ Team  │───────────►│ Team  │                         │  │
│  │   │   A   │  consumes  │   B   │                         │  │
│  │   └───────┘    API     └───────┘                         │  │
│  │                                                           │  │
│  │   Clear API • Low coupling • Sustainable long-term       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   FACILITATING                            │  │
│  │                                                           │  │
│  │   ┌───────┐            ┌───────┐                         │  │
│  │   │Enabling│──────────►│ Team  │                         │  │
│  │   │ Team  │   helps    │   A   │                         │  │
│  │   └───────┘  improve   └───────┘                         │  │
│  │                                                           │  │
│  │   Knowledge transfer • Time-boxed • Exit planned         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Collaboration Mode

```text
COLLABORATION: Working closely together on shared goals

CHARACTERISTICS:
• High-bandwidth communication
• Shared responsibility for outcomes
• Blurred team boundaries (temporarily)
• Frequent synchronization
• Joint decision-making

WHEN TO USE:
• New product/service development
• Complex integration work
• Innovation or discovery phases
• Major architectural changes
• Rapid problem-solving

DURATION:
• Time-boxed (weeks to months)
• NOT sustainable long-term
• Should evolve to X-as-a-Service

SIGNS IT'S WORKING:
✓ Joint ownership of outcomes
✓ Frequent informal communication
✓ Shared understanding develops
✓ Problems solved together
✓ Knowledge transfers both ways

ANTI-PATTERNS:
✗ Collaboration without end date
✗ One team doing all the work
✗ No knowledge transfer happening
✗ Dependencies increasing
✗ "Collaboration" as excuse for poor boundaries

EXAMPLE:
┌─────────────────────────────────────────┐
│ Payments Team + Security Team           │
│                                         │
│ Goal: Implement PCI compliance          │
│ Duration: 3 months                      │
│ Exit: Security becomes X-as-a-Service   │
│                                         │
│ Activities:                             │
│ • Joint design sessions                 │
│ • Shared Slack channel                  │
│ • Pairing on implementation             │
│ • Knowledge transfer sessions           │
└─────────────────────────────────────────┘
```

## X-as-a-Service Mode

```text
X-AS-A-SERVICE: Consuming another team's capability via API

CHARACTERISTICS:
• Clear, versioned API
• Minimal coordination needed
• Teams operate independently
• Provider-consumer relationship
• Self-service when possible

WHEN TO USE:
• Stable, well-defined capabilities
• Platform team offerings
• Standard infrastructure needs
• Commoditized services
• After collaboration establishes patterns

DURATION:
• Long-term sustainable
• Default interaction mode
• Can evolve from Collaboration

SIGNS IT'S WORKING:
✓ Consumers self-serve successfully
✓ Provider rarely contacted
✓ Clear documentation exists
✓ Versioning allows evolution
✓ Both teams operate independently

ANTI-PATTERNS:
✗ Constant back-channel requests
✗ Documentation always outdated
✗ Breaking changes without warning
✗ Provider becomes bottleneck
✗ Service doesn't meet needs

EXAMPLE:
┌─────────────────────────────────────────┐
│ Stream-aligned Team → Platform Team     │
│                                         │
│ Service: Container Deployment           │
│ Interface: CLI + Terraform module       │
│ Documentation: Self-service guide       │
│ Support: Office hours + Slack           │
│                                         │
│ Consumer:                               │
│ • Reads docs                            │
│ • Uses CLI to deploy                    │
│ • Files issues if blocked               │
│ • Attends office hours for questions    │
└─────────────────────────────────────────┘
```

## Facilitating Mode

```text
FACILITATING: Helping another team improve their capability

CHARACTERISTICS:
• Enabling team leads
• Knowledge transfer focus
• Teaching over doing
• Time-boxed engagement
• Clear exit criteria

WHEN TO USE:
• Capability gap identified
• New technology adoption
• Process improvement needs
• Team struggling with patterns
• Skills development required

DURATION:
• Time-boxed (weeks to few months)
• Exit when capability transferred
• NOT meant to be permanent

SIGNS IT'S WORKING:
✓ Receiving team gains skills
✓ Less help needed over time
✓ Enabling team can exit
✓ Receiving team owns capability
✓ Knowledge documented

ANTI-PATTERNS:
✗ Facilitating team does the work
✗ No skill transfer happening
✗ Dependency created
✗ Engagement drags on indefinitely
✗ Receiving team passive

EXAMPLE:
┌─────────────────────────────────────────┐
│ DevOps Enablement → Checkout Team       │
│                                         │
│ Goal: Improve CI/CD maturity            │
│ Duration: 6 weeks                       │
│ Exit: Team owns their pipeline          │
│                                         │
│ Activities:                             │
│ Week 1-2: Assessment & planning         │
│ Week 3-4: Pairing on improvements       │
│ Week 5: Team leads implementation       │
│ Week 6: Documentation & handoff         │
└─────────────────────────────────────────┘
```

## Interaction Mode Selection

```text
MODE SELECTION MATRIX:

┌────────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Situation          │ Collaboration   │ X-as-a-Service  │ Facilitating    │
├────────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ New product dev    │ ✓ Start here    │ → Evolve to     │                 │
│ Discovery work     │ ✓               │                 │                 │
│ Complex integration│ ✓               │                 │                 │
├────────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Stable capability  │                 │ ✓ Default       │                 │
│ Platform service   │                 │ ✓               │                 │
│ Infrastructure     │                 │ ✓               │                 │
├────────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Skill gap          │                 │                 │ ✓               │
│ Process improvement│                 │                 │ ✓               │
│ Adoption help      │                 │                 │ ✓               │
└────────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## Interaction Evolution

```text
TYPICAL EVOLUTION PATTERNS:

Pattern 1: Collaboration → X-as-a-Service

  START                    MID                       END
  ┌─────┐    ┌─────┐      ┌─────┐    ┌─────┐       ┌─────┐    ┌─────┐
  │  A  │◄──►│  B  │  →   │  A  │◄──►│  B  │   →   │  A  │───►│  B  │
  └─────┘    └─────┘      └─────┘    └─────┘       └─────┘    └─────┘
  Collaboration           Patterns emerge           API defined

Pattern 2: Facilitating → Independence

  START                    MID                       END
  ┌─────┐    ┌─────┐      ┌─────┐    ┌─────┐       ┌─────┐    ┌─────┐
  │ EN  │───►│  A  │  →   │ EN  │───►│  A  │   →   │ EN  │    │  A  │
  └─────┘    └─────┘      └─────┘    └─────┘       └─────┘    └─────┘
  Heavy help              Light touch              Team independent

Pattern 3: X-as-a-Service → Collaboration → X-as-a-Service

  START                    MID                       END
  ┌─────┐    ┌─────┐      ┌─────┐    ┌─────┐       ┌─────┐    ┌─────┐
  │  A  │───►│  B  │  →   │  A  │◄──►│  B  │   →   │  A  │───►│  B  │
  └─────┘    └─────┘      └─────┘    └─────┘       └─────┘    └─────┘
  Using service           Major change together    New API version
```

## Team Type and Interaction Compatibility

```text
INTERACTION COMPATIBILITY MATRIX:

                    │ Stream │Platform│Enabling│Complicated│
                    │Aligned │        │        │ Subsystem │
────────────────────┼────────┼────────┼────────┼───────────┤
Stream-Aligned      │ Collab │ XaaS   │Facilit.│   XaaS    │
────────────────────┼────────┼────────┼────────┼───────────┤
Platform            │ XaaS   │ Collab │Facilit.│   XaaS    │
────────────────────┼────────┼────────┼────────┼───────────┤
Enabling            │Facilit.│Facilit.│ Collab │ Facilit.  │
────────────────────┼────────┼────────┼────────┼───────────┤
Complicated         │ XaaS   │ XaaS   │Facilit.│  Collab   │
Subsystem           │        │        │        │           │
────────────────────┴────────┴────────┴────────┴───────────┘

XaaS = X-as-a-Service (default, sustainable)
Collab = Collaboration (time-boxed)
Facilit. = Facilitating (time-boxed, knowledge transfer)
```

## Interaction Anti-Patterns

```text
ANTI-PATTERNS TO AVOID:

1. PERMANENT COLLABORATION
   Problem: Two teams always in collaboration mode
   Impact: Neither team fully independent
   Fix: Define API, evolve to X-as-a-Service

2. FACILITATING WITHOUT EXIT
   Problem: Enabling team never leaves
   Impact: Dependency created, not capability
   Fix: Time-box engagement, define exit criteria

3. X-AS-A-SERVICE WITHOUT SERVICE
   Problem: API claimed but not actually self-service
   Impact: Hidden collaboration, provider overloaded
   Fix: Invest in documentation, automation

4. COLLABORATION THEATER
   Problem: Called collaboration but one team does work
   Impact: No knowledge transfer, resentment
   Fix: Define joint outcomes, shared work

5. TOO MANY INTERACTION MODES
   Problem: Team interacts with 10+ teams intensively
   Impact: Cognitive overload, context switching
   Fix: Reduce dependencies, consolidate interactions

6. NO EVOLUTION PLANNING
   Problem: Interactions never reviewed or evolved
   Impact: Sub-optimal patterns persist
   Fix: Quarterly interaction review
```

## Interaction Mapping Template

```markdown
# Team Interaction Map: [Team Name]

## Current Interactions

### Collaboration Mode
| Partner Team | Purpose | Started | Planned End | Exit Criteria |
|-------------|---------|---------|-------------|---------------|
| [Team] | [Why collaborating] | [Date] | [Date] | [Criteria] |

### X-as-a-Service (We Provide)
| Consumer Team | Service | API/Interface | SLE |
|--------------|---------|---------------|-----|
| [Team] | [What we provide] | [Interface] | [SLE] |

### X-as-a-Service (We Consume)
| Provider Team | Service | API/Interface | Our Usage |
|--------------|---------|---------------|-----------|
| [Team] | [What we consume] | [Interface] | [How we use] |

### Facilitating (We Receive)
| Enabling Team | Capability | Duration | Exit Criteria |
|--------------|------------|----------|---------------|
| [Team] | [What they help with] | [Dates] | [Criteria] |

### Facilitating (We Provide)
| Receiving Team | Capability | Duration | Exit Criteria |
|----------------|------------|----------|---------------|
| [Team] | [What we help with] | [Dates] | [Criteria] |

## Interaction Health

### Working Well
- [Interaction that works well]
- [Another positive interaction]

### Needs Attention
| Interaction | Issue | Proposed Change |
|-------------|-------|-----------------|
| [Teams] | [Problem] | [Solution] |

## Planned Evolution

### Q1 Changes
| Current | Target | Reason |
|---------|--------|--------|
| Collab with Team X | XaaS | API now stable |

### Dependencies to Reduce
| Dependency | Current Impact | Reduction Plan |
|------------|----------------|----------------|
| [Team] | [Impact] | [Plan] |

## Review Schedule
- **Last Review:** [Date]
- **Next Review:** [Date]
- **Reviewer:** [Name]
```

## Interaction Review Process

```text
QUARTERLY INTERACTION REVIEW:

1. MAP CURRENT STATE
   □ List all team interactions
   □ Classify by mode
   □ Note duration of each

2. ASSESS HEALTH
   □ Which interactions work well?
   □ Which are struggling?
   □ Any "forever collaborations"?

3. PLAN EVOLUTION
   □ What should change mode?
   □ What can be reduced?
   □ What needs more investment?

4. TAKE ACTION
   □ Update interaction agreements
   □ Set exit criteria for time-boxed
   □ Communicate changes
```

## Workflow

When defining interaction patterns:

1. **Map Current Interactions**: What exists today?
2. **Classify Modes**: Collaboration, X-as-a-Service, or Facilitating?
3. **Assess Fit**: Is each mode appropriate for the situation?
4. **Identify Anti-Patterns**: Any problematic patterns?
5. **Plan Evolution**: What should change and when?
6. **Document Agreements**: Make interactions explicit
7. **Review Regularly**: Quarterly assessment

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
