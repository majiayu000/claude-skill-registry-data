---
name: internal-developer-platform
description: Use when designing Internal Developer Platforms (IDPs), building platform teams, or improving developer experience. Covers platform engineering principles, Backstage, portal design, and platform team structures.
allowed-tools: Read, Glob, Grep
---

# Internal Developer Platform

Comprehensive guide to designing and building Internal Developer Platforms (IDPs) that improve developer productivity and experience.

## When to Use This Skill

- Designing an Internal Developer Platform
- Building or restructuring platform teams
- Improving developer experience (DevEx)
- Evaluating platform technologies (Backstage, Port, etc.)
- Creating self-service capabilities for developers
- Measuring platform adoption and success

## Platform Engineering Fundamentals

### What is an Internal Developer Platform?

```text
Internal Developer Platform (IDP):
A layer on top of infrastructure that provides self-service
capabilities to development teams while maintaining governance.

┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPERS                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ Team A  │  │ Team B  │  │ Team C  │  │ Team D  │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │              │
│       └────────────┴─────┬──────┴────────────┘              │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────────────┐  │
│  │              INTERNAL DEVELOPER PLATFORM               │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │  │
│  │  │ Service  │ │ Template │ │ Self-    │ │ Docs &   │ │  │
│  │  │ Catalog  │ │ Library  │ │ Service  │ │ Discovery│ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────────────┐  │
│  │                  INFRASTRUCTURE                        │  │
│  │  Kubernetes │ Cloud │ CI/CD │ Observability │ Security │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

Key Value Propositions:
├── Self-service: Developers can provision without tickets
├── Standardization: Consistent patterns across teams
├── Guardrails: Security and compliance built-in
├── Visibility: Centralized service catalog and docs
└── Efficiency: Reduce cognitive load on developers
```

### Platform vs Infrastructure

```text
Infrastructure Team (Traditional):
- Ticket-based requests
- Manual provisioning
- Bespoke solutions per team
- Ops handles deployments
- Documentation scattered

Platform Team (Modern):
- Self-service capabilities
- Automated provisioning
- Standardized templates
- Developers own deployments
- Centralized documentation

Key Shift:
"You Build It, You Run It" + "Platform Handles the How"
```

## Platform Core Components

### Service Catalog

```text
Service Catalog:
Centralized registry of all services with ownership, docs, and metadata.

┌─────────────────────────────────────────────────────────────┐
│                    SERVICE CATALOG                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Payment Service                                [API]     │ │
│  │ Owner: Payments Team     │ Tier: Critical              │ │
│  │ Tech: Node.js, PostgreSQL │ Dependencies: 4            │ │
│  │ [Docs] [API Spec] [Runbook] [Alerts] [Deploy]          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ User Service                                 [Backend]   │ │
│  │ Owner: Identity Team     │ Tier: High                  │ │
│  │ Tech: Go, MongoDB        │ Dependencies: 2             │ │
│  │ [Docs] [API Spec] [Runbook] [Alerts] [Deploy]          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Service Metadata:                                           │
│  ├── Owner team and contacts                                │
│  ├── Technical stack                                        │
│  ├── Service tier/criticality                               │
│  ├── Dependencies (upstream/downstream)                     │
│  ├── API specifications                                     │
│  ├── Documentation links                                    │
│  ├── Deployment information                                 │
│  └── Observability dashboards                               │
└─────────────────────────────────────────────────────────────┘
```

### Template Library

```text
Template Library:
Pre-built templates for common patterns that encode best practices.

Template Categories:
├── Application Templates
│   ├── REST API (Go, Node.js, .NET, Python)
│   ├── GraphQL Service
│   ├── gRPC Service
│   ├── Event Consumer
│   ├── Scheduled Job
│   └── Frontend (React, Vue, Angular)
│
├── Infrastructure Templates
│   ├── Database (PostgreSQL, MySQL, MongoDB)
│   ├── Cache (Redis, Memcached)
│   ├── Message Queue (Kafka, RabbitMQ)
│   └── Storage (S3, GCS)
│
└── Integration Templates
    ├── Third-party API client
    ├── Authentication flow
    └── Webhook handler

Template Contents:
┌─────────────────────────────────────────────────────────────┐
│ Template: node-rest-api                                      │
├─────────────────────────────────────────────────────────────┤
│ ├── src/                    │ Application code              │
│ ├── tests/                  │ Test setup                    │
│ ├── Dockerfile              │ Container image               │
│ ├── helm/                   │ Kubernetes deployment         │
│ ├── .github/workflows/      │ CI/CD pipelines               │
│ ├── docs/                   │ Documentation templates       │
│ ├── catalog-info.yaml       │ Backstage registration        │
│ └── terraform/              │ Infrastructure as Code        │
│                                                              │
│ Built-in:                                                    │
│ ✓ Health checks             ✓ Structured logging            │
│ ✓ OpenTelemetry tracing     ✓ Prometheus metrics           │
│ ✓ Security headers          ✓ Input validation             │
│ ✓ Error handling            ✓ API documentation            │
└─────────────────────────────────────────────────────────────┘
```

### Self-Service Portal

```text
Self-Service Capabilities:
Actions developers can perform without tickets or approvals.

┌─────────────────────────────────────────────────────────────┐
│                  SELF-SERVICE PORTAL                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Create New Service     [5 min setup, no tickets]           │
│  ├── Choose template                                        │
│  ├── Configure options                                      │
│  ├── Generate repository                                    │
│  ├── Create CI/CD pipeline                                  │
│  ├── Provision infrastructure                               │
│  └── Register in catalog                                    │
│                                                              │
│  Common Self-Service Actions:                               │
│  ┌────────────────┬────────────────┬────────────────┐      │
│  │ Environments   │ Databases      │ Secrets        │      │
│  │ ├── Create env │ ├── Provision  │ ├── Create     │      │
│  │ ├── Clone env  │ ├── Scale      │ ├── Rotate     │      │
│  │ └── Destroy    │ └── Backup     │ └── Access     │      │
│  └────────────────┴────────────────┴────────────────┘      │
│  ┌────────────────┬────────────────┬────────────────┐      │
│  │ Deployments    │ Domains        │ Access         │      │
│  │ ├── Deploy     │ ├── Request    │ ├── Request    │      │
│  │ ├── Rollback   │ ├── Configure  │ ├── Review     │      │
│  │ └── Promote    │ └── Cert       │ └── Audit      │      │
│  └────────────────┴────────────────┴────────────────┘      │
│                                                              │
│  Guardrails (automatic):                                    │
│  ✓ Security scanning        ✓ Compliance checks            │
│  ✓ Cost limits              ✓ Naming conventions           │
│  ✓ Resource quotas          ✓ Approval workflows           │
└─────────────────────────────────────────────────────────────┘
```

## Platform Team Structure

### Team Topologies

```text
Platform Team Types:

1. Enabling Team (Recommended Start)
   Purpose: Help stream-aligned teams adopt platform
   Size: 3-5 people
   Activities:
   ├── Pair programming with product teams
   ├── Create documentation and guides
   ├── Gather feedback and requirements
   └── Provide training and support

2. Platform Team (Mature)
   Purpose: Build and maintain the platform
   Size: 5-15 people (scale with org)
   Activities:
   ├── Build self-service capabilities
   ├── Maintain templates and tooling
   ├── Define and enforce standards
   └── Operate platform infrastructure

3. Complicated Subsystem Team (Specialized)
   Purpose: Handle complex technical domains
   Size: 3-7 people per domain
   Examples:
   ├── Data platform team
   ├── ML platform team
   └── Security platform team

Team Interaction:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ Stream-      │◄───────►│ Platform     │                 │
│  │ Aligned Team │ X-as-a- │ Team         │                 │
│  └──────────────┘ Service └──────────────┘                 │
│         │                        │                          │
│         │ Collaboration          │ Facilitation            │
│         │                        │                          │
│         ▼                        ▼                          │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ Complicated  │◄───────►│ Enabling     │                 │
│  │ Subsystem    │ Service │ Team         │                 │
│  └──────────────┘         └──────────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Platform Team Skills

```text
Platform Team Competencies:

Technical:
├── Kubernetes and container orchestration
├── Infrastructure as Code (Terraform, Pulumi)
├── CI/CD pipeline design
├── API design and development
├── Observability tooling
├── Security engineering
└── Cloud platforms (AWS, GCP, Azure)

Product:
├── Developer experience research
├── User journey mapping
├── Metrics and analytics
├── Documentation writing
└── Training and enablement

Organizational:
├── Stakeholder management
├── Communication skills
├── Change management
└── Technical leadership
```

## Platform Technology Choices

### Backstage (Spotify)

```text
Backstage:
Open-source developer portal framework by Spotify.

Core Features:
├── Service Catalog (software component registry)
├── Software Templates (scaffolding)
├── TechDocs (docs-as-code)
├── Search (unified search across everything)
└── Plugins (extensible ecosystem)

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                     BACKSTAGE                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Frontend (React)                    │   │
│  │  ├── Catalog UI    ├── Templates UI    ├── Plugins   │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Backend (Node.js)                   │   │
│  │  ├── Catalog API   ├── Auth          ├── Plugin APIs │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Integrations                        │   │
│  │  ├── GitHub     ├── Kubernetes    ├── CI/CD          │   │
│  │  ├── PagerDuty  ├── Prometheus    ├── Custom         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

Catalog Entity:
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Handles payment processing
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: payments-team
  system: payments
  dependsOn:
    - component:user-service
  providesApis:
    - payment-api
```

### Alternative Platforms

```text
Platform Options Comparison:

| Platform | Type | Strengths | Considerations |
|----------|------|-----------|----------------|
| Backstage | OSS | Extensible, active community | Requires customization |
| Port | Commercial | Quick setup, polished UI | Vendor lock-in |
| Cortex | Commercial | SRE focused, scorecards | Enterprise pricing |
| OpsLevel | Commercial | Service maturity | Smaller ecosystem |
| Roadie | Managed | Hosted Backstage | Less control |

Decision Factors:
├── Build vs Buy tolerance
├── Customization requirements
├── Team capacity for maintenance
├── Integration needs
├── Budget constraints
└── Timeline expectations
```

## Developer Experience Metrics

### DORA Metrics

```text
DORA (DevOps Research and Assessment) Metrics:

1. Deployment Frequency
   How often you deploy to production
   ├── Elite: Multiple times per day
   ├── High: Weekly to monthly
   ├── Medium: Monthly to every 6 months
   └── Low: Every 6+ months

2. Lead Time for Changes
   Time from code commit to production
   ├── Elite: < 1 hour
   ├── High: 1 day to 1 week
   ├── Medium: 1 week to 1 month
   └── Low: 1 month to 6 months

3. Mean Time to Recovery (MTTR)
   Time to recover from production failure
   ├── Elite: < 1 hour
   ├── High: < 1 day
   ├── Medium: < 1 week
   └── Low: 1 week to 1 month

4. Change Failure Rate
   Percentage of deployments causing failure
   ├── Elite: 0-15%
   ├── High: 16-30%
   ├── Medium: 31-45%
   └── Low: 46-60%
```

### Platform-Specific Metrics

```text
Platform Success Metrics:

Adoption:
├── % of services in catalog
├── % of teams using templates
├── Self-service usage rate
├── Portal active users
└── Template utilization

Efficiency:
├── Time to first deployment (new service)
├── Time to provision infrastructure
├── Ticket reduction rate
├── Toil automation percentage
└── Developer time saved

Satisfaction:
├── Developer NPS
├── Platform satisfaction surveys
├── Support ticket volume
├── Documentation usefulness
└── Onboarding feedback

Quality:
├── Template adoption vs custom builds
├── Security compliance rate
├── Standards adherence
└── Incident rate for platform-built services
```

## Implementation Roadmap

### Phased Approach

```text
Phase 1: Foundation (3-6 months)
├── Service catalog (inventory what exists)
├── Basic documentation site
├── Initial template (1-2 golden paths)
├── Platform team formation
└── Metrics baseline

Phase 2: Self-Service (6-12 months)
├── Template library expansion
├── Self-service provisioning
├── CI/CD standardization
├── Developer portal launch
└── Adoption campaigns

Phase 3: Optimization (12-18 months)
├── Advanced templates
├── Platform APIs
├── Automation expansion
├── Cost optimization
└── Advanced analytics

Phase 4: Ecosystem (18+ months)
├── Plugin ecosystem
├── ML/data platform integration
├── Cross-team collaboration features
├── External developer experience
└── Continuous evolution

Success Criteria Per Phase:
Phase 1: 50% service discovery complete
Phase 2: 70% of new services use templates
Phase 3: 80% self-service capability
Phase 4: Platform is indispensable
```

## Common Anti-Patterns

```text
Platform Anti-Patterns:

1. "Build It and They Will Come"
   ❌ Building features without user research
   ✓ Start with developer interviews and pain points

2. "One Size Fits All"
   ❌ Forcing every team into same workflow
   ✓ Provide flexibility with sensible defaults

3. "Platform as Gatekeeper"
   ❌ Adding friction and approval gates
   ✓ Enable self-service with guardrails

4. "Technical Purity"
   ❌ Choosing tech for platform team excitement
   ✓ Choose what solves developer problems

5. "Big Bang Launch"
   ❌ Building for 2 years before releasing
   ✓ Iterate quickly with early adopters

6. "Mandates Without Value"
   ❌ Forcing adoption via policy
   ✓ Make platform so good teams want to use it

7. "Documentation Afterthought"
   ❌ Minimal or outdated docs
   ✓ Treat docs as product feature

8. "Ivory Tower Platform"
   ❌ Platform team isolated from users
   ✓ Embed with product teams regularly
```

## Best Practices

```text
Platform Engineering Best Practices:

1. Treat Platform as Product
   ├── Have product owner/manager
   ├── Conduct user research
   ├── Prioritize based on impact
   └── Measure outcomes, not outputs

2. Start with Golden Paths
   ├── Identify most common use cases
   ├── Create templates for those first
   ├── Make golden path easiest choice
   └── Don't block non-golden paths

3. Optimize for Self-Service
   ├── Target <5 minutes for common tasks
   ├── Eliminate manual approvals where safe
   ├── Provide escape hatches when needed
   └── Clear error messages and guidance

4. Build Community
   ├── Developer advocates/champions
   ├── Office hours and support channels
   ├── Contribution guidelines
   └── Celebrate platform wins

5. Measure Everything
   ├── Adoption metrics
   ├── Developer satisfaction
   ├── Time savings
   └── Platform reliability

6. Iterate Rapidly
   ├── Ship early, improve often
   ├── Gather feedback continuously
   ├── Deprecate gracefully
   └── Communicate changes clearly
```

## Related Skills

- `golden-paths` - Designing standardized development workflows
- `self-service-infrastructure` - Infrastructure self-service patterns
- `slo-sli-error-budget` - Platform reliability targets
- `observability-patterns` - Platform observability
