---
name: team-api-design
description: Define team interfaces, contracts, and communication boundaries
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Team API Design Skill

## When to Use This Skill

Use this skill when:

- **Team Api Design tasks** - Working on define team interfaces, contracts, and communication boundaries
- **Planning or design** - Need guidance on Team Api Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Define clear team interfaces, contracts, and communication boundaries using Team API patterns.

## MANDATORY: Documentation-First Approach

Before designing team APIs:

1. **Invoke `docs-management` skill** for team interface patterns
2. **Verify Team API concepts** via MCP servers (perplexity)
3. **Base guidance on Team Topologies team API framework**

## What is a Team API?

```text
TEAM API: The explicit interface a team exposes to other teams

┌─────────────────────────────────────────────────────────────────┐
│                          TEAM API                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Code &     │  │  Versioning  │  │  Service     │          │
│  │   Artifacts  │  │   & Releases │  │   Catalog    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Wiki &     │  │  Practices   │  │   Ways of    │          │
│  │   Docs       │  │   & Runbooks │  │   Working    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Chat &     │  │   Office     │  │   Support    │          │
│  │   Channels   │  │   Hours      │  │   Rotation   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

PURPOSE: Make team interactions explicit, predictable, and sustainable
```

## Team API Components

### 1. Code and Artifacts

```text
TECHNICAL INTERFACE:

Repositories:
• Main repo location (URL)
• Contributing guidelines
• Code review expectations
• Branch naming conventions

APIs:
• OpenAPI/AsyncAPI specs
• Authentication requirements
• Rate limits and quotas
• Deprecation policy

Artifacts:
• Package registry location
• Container image registry
• Artifact versioning scheme
• Release notes location
```

### 2. Versioning and Releases

```text
RELEASE INTERFACE:

Versioning:
• Semantic versioning (MAJOR.MINOR.PATCH)
• Breaking change policy
• Deprecation timeline
• Migration guides

Release Schedule:
• Release cadence (weekly, bi-weekly, continuous)
• Release windows
• Hotfix process
• Rollback procedures

Compatibility:
• Supported versions
• EOL announcements
• Backward compatibility guarantees
• Forward compatibility approach
```

### 3. Documentation

```text
KNOWLEDGE INTERFACE:

Team Wiki:
• Team overview and mission
• Architecture decisions (ADRs)
• Design documents
• Onboarding guides

API Documentation:
• Getting started guides
• API reference
• Code examples
• FAQ and troubleshooting

Operational Docs:
• Runbooks
• Incident response procedures
• Monitoring dashboards
• Alert explanations
```

### 4. Communication Channels

```text
COMMUNICATION INTERFACE:

Asynchronous:
• Primary Slack/Teams channel
• Announcements channel
• Bug/issue tracker
• Email distribution list

Synchronous:
• Office hours schedule
• On-call rotation
• Escalation path
• Meeting cadence

Response Times:
• Slack: 4 business hours
• Issues: 1 business day
• Urgent: 1 hour
• Incident: 15 minutes
```

### 5. Service Level Expectations

```text
SERVICE INTERFACE:

Availability:
• Target uptime (99.9%)
• Maintenance windows
• Planned downtime notice period

Performance:
• Latency targets (p50, p99)
• Throughput limits
• Error rate targets

Support:
• Business hours support
• On-call availability
• Incident severity levels
• Resolution time targets
```

## Team API Template

```markdown
# Team API: [Team Name]

## Team Overview

**Mission:** [One-sentence mission statement]
**Team Type:** [Stream-aligned | Platform | Enabling | Complicated-Subsystem]
**Bounded Context:** [Domain owned]

## Team Members

| Role | Name | Contact |
|------|------|---------|
| Tech Lead | [Name] | @handle |
| Product Owner | [Name] | @handle |
| Engineers | [Names] | @handles |

## What We Own

### Services
| Service | Description | Repository |
|---------|-------------|------------|
| [Name] | [Purpose] | [URL] |

### APIs
| API | Spec | Status |
|-----|------|--------|
| [Name] | [OpenAPI URL] | [Stable/Beta/Alpha] |

## How to Contact Us

### Asynchronous
- **Slack:** #team-[name]
- **Issues:** [Jira/GitHub project URL]
- **Email:** team-[name]@company.com

### Synchronous
- **Office Hours:** [Day/Time]
- **On-call:** [PagerDuty URL or rotation]

### Response Times
| Channel | Expected Response |
|---------|------------------|
| Slack | 4 business hours |
| Issues | 1 business day |
| Urgent Slack | 1 hour |
| Incidents | 15 minutes |

## How to Work With Us

### Requesting Changes
1. Open an issue in [repository]
2. Attend office hours to discuss
3. Submit PR following [contributing guide]

### Consuming Our APIs
1. Read [getting started guide]
2. Request API credentials via [process]
3. Follow [rate limiting guidelines]

### Escalation Path
1. Post in #team-[name]
2. Page on-call if urgent
3. Contact Tech Lead directly if blocked

## Service Level Expectations

### Availability
- **Target:** 99.9% uptime
- **Maintenance Window:** [Day/Time]
- **Notice Period:** 48 hours for planned downtime

### Performance
- **p50 Latency:** [X]ms
- **p99 Latency:** [X]ms
- **Error Rate:** <0.1%

### Support
- **Business Hours:** 9am-5pm [Timezone]
- **On-call Hours:** 24/7 for P1/P2
- **Holiday Coverage:** [Policy]

## Versioning and Releases

### Release Cadence
- **Frequency:** [Weekly/Bi-weekly/Continuous]
- **Release Day:** [Day]
- **Changelog:** [Location]

### API Versioning
- **Strategy:** [URL path | Header | Query param]
- **Breaking Change Notice:** [X weeks]
- **Deprecation Period:** [X months]

### Currently Supported Versions
| Version | Status | EOL Date |
|---------|--------|----------|
| v3 | Current | N/A |
| v2 | Maintenance | [Date] |
| v1 | Deprecated | [Date] |

## Documentation

### For Users
- [Getting Started Guide]
- [API Reference]
- [Code Examples]
- [FAQ]

### For Contributors
- [Contributing Guidelines]
- [Architecture Overview]
- [Development Setup]
- [Testing Guide]

### Operational
- [Runbooks]
- [Monitoring Dashboard]
- [Incident Response]

## Dependencies

### What We Depend On
| Team/Service | Type | Criticality |
|--------------|------|-------------|
| [Name] | [API/Library/Data] | [High/Medium/Low] |

### What Depends On Us
| Team/Service | Interface | Usage |
|--------------|-----------|-------|
| [Name] | [API/Event/Library] | [Description] |

## Roadmap

### Current Quarter
- [Initiative 1]
- [Initiative 2]

### Next Quarter
- [Planned work]

### Known Limitations
- [Limitation 1]
- [Limitation 2]
```

## Team API Governance

### Creating a Team API

```text
TEAM API CREATION PROCESS:

1. DRAFT
   □ Use template above
   □ Fill in all sections
   □ Get team consensus

2. REVIEW
   □ Review with stakeholders
   □ Validate with consumers
   □ Check completeness

3. PUBLISH
   □ Store in team wiki/repo
   □ Register in service catalog
   □ Announce to organization

4. MAINTAIN
   □ Review quarterly
   □ Update on changes
   □ Gather feedback
```

### Team API Maturity Levels

```text
MATURITY MODEL:

LEVEL 1: BASIC
□ Team contact information exists
□ Primary service documented
□ Basic Slack channel

LEVEL 2: DEFINED
□ Full team API document
□ Response time expectations
□ Versioning policy defined
□ Basic SLEs documented

LEVEL 3: MEASURED
□ SLEs tracked and reported
□ Consumer feedback collected
□ Dependencies mapped
□ Regular API reviews

LEVEL 4: OPTIMIZED
□ Team API continuously improved
□ Automation for API updates
□ Consumer satisfaction tracked
□ Industry best practices adopted
```

## Platform Team API Example

```markdown
# Platform Team API: Developer Platform

## Mission
Enable stream-aligned teams to deliver software faster through
self-service infrastructure and golden paths.

## Team Type: Platform

## What We Provide

### Self-Service Capabilities
| Capability | Interface | Docs |
|------------|-----------|------|
| Container Deployment | CLI/Portal | [Link] |
| Database Provisioning | Terraform Module | [Link] |
| CI/CD Pipeline | Template | [Link] |
| Secrets Management | Vault API | [Link] |

### Golden Paths
| Path | Use Case | Guide |
|------|----------|-------|
| Web Service | Standard web APIs | [Link] |
| Event Consumer | Kafka consumers | [Link] |
| Scheduled Job | Batch processing | [Link] |

## Interaction Model

### X-as-a-Service (Default)
- Use our self-service capabilities
- Follow golden path documentation
- Submit issues for problems
- Attend office hours for questions

### Collaboration (By Request)
- Available for complex migrations
- Custom platform needs
- Time-boxed engagements
- Requires PM approval

## Office Hours
- **When:** Tuesdays 2-3pm, Thursdays 10-11am
- **Where:** #platform-office-hours Slack huddle
- **What:** Q&A, demos, troubleshooting

## Support Tiers
| Tier | Response | Example |
|------|----------|---------|
| P1 - Production Down | 15 min | Platform unavailable |
| P2 - Degraded | 1 hour | Slow deployments |
| P3 - Blocked | 4 hours | Can't provision resource |
| P4 - Question | 1 day | How to configure X |
```

## Stream-Aligned Team API Example

```markdown
# Team API: Payments Team

## Mission
Process payments reliably and securely for all commerce streams.

## Team Type: Stream-Aligned

## Bounded Context: Payment Processing

## What We Own

### Services
| Service | Purpose | SLE |
|---------|---------|-----|
| Payment Gateway | Process payments | 99.95% uptime |
| Refund Service | Handle refunds | 99.9% uptime |
| Fraud Detection | Real-time fraud | p99 < 50ms |

### APIs
| API | Description | Spec |
|-----|-------------|------|
| /payments | Create/query payments | [OpenAPI] |
| /refunds | Process refunds | [OpenAPI] |

### Events Published
| Event | Topic | Schema |
|-------|-------|--------|
| PaymentCompleted | payments.completed | [Avro] |
| RefundProcessed | payments.refunds | [Avro] |

## How to Integrate

### For Payment Processing
1. Read [integration guide]
2. Request sandbox credentials
3. Complete security review
4. Go-live checklist

### For Consuming Events
1. Subscribe to Kafka topic
2. Implement idempotent handler
3. Set up DLQ handling
4. Monitor consumer lag

## Constraints
- **PCI Compliance:** All integrations require security review
- **Rate Limits:** 1000 req/sec per client
- **Data Retention:** 7 years for transactions
```

## Assessment Checklist

```text
TEAM API HEALTH CHECK:

DISCOVERABILITY
□ Team API document exists and is findable
□ Registered in service catalog
□ Links work and content is current

COMPLETENESS
□ All sections filled in
□ Contact information accurate
□ Dependencies documented
□ SLEs defined

CLARITY
□ Non-team members can understand
□ No jargon or undefined terms
□ Clear call-to-action for consumers
□ Examples provided

MAINTENANCE
□ Last updated within 3 months
□ Regular review scheduled
□ Feedback mechanism exists
□ Ownership clearly assigned

EFFECTIVENESS
□ Consumers find what they need
□ Response times being met
□ Fewer repeated questions
□ Team satisfaction with API
```

## Workflow

When designing team APIs:

1. **Audit Current State**: What exists today? What's implicit?
2. **Identify Consumers**: Who interacts with the team?
3. **Document Interface**: Use template, fill completely
4. **Validate with Consumers**: Does this meet their needs?
5. **Publish and Announce**: Make it discoverable
6. **Measure and Iterate**: Track effectiveness, improve

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
