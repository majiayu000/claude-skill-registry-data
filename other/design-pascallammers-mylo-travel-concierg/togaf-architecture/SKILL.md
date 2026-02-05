---
name: togaf-architecture
description: |
  Enterprise architecture patterns following TOGAF ADM methodology.
  Implements capability-driven design, federated architecture, and
  technology-agnostic specifications. Activates for enterprise-scale
  architecture decisions.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
---

# TOGAF Enterprise Architecture Skill

This skill implements enterprise architecture patterns based on the TOGAF Architecture Development Method (ADM).

## When This Skill Activates

- Designing enterprise-scale systems
- Making architectural decisions
- Creating technology-agnostic specifications
- Implementing capability-driven architecture
- Planning large-scale system migrations

## Core Principles

### 1. Principles Over Technologies
Focus on capabilities, not specific tools:
- **Business Process Automation** (not "use Kubernetes")
- **Real-Time Decision Making** (not "use TensorFlow")
- **Multi-Cloud Interoperability** (not "use AWS Lambda")

### 2. Capability-Driven Design
Define systems by what they accomplish:
```yaml
capabilities:
  - Business Process Automation
  - Real-Time Decision Making
  - Multi-Cloud Interoperability
  - AI Integration
  - Compliance Management
```

### 3. Modularity & Replaceability
All components should be:
- Loosely coupled
- Independently deployable
- Replaceable without re-architecture

### 4. Technology Agnosticism
Specifications should survive technology changes:
- Define interfaces, not implementations
- Focus on outcomes, not tooling
- Enable future innovation

## TOGAF ADM Phases

### Phase A: Architecture Vision
```yaml
phase: vision
objectives:
  - Define business capability
  - Identify stakeholders
  - Establish success metrics
  - Create architecture vision

deliverables:
  - Architecture vision document
  - Stakeholder analysis
  - Business requirements
```

### Phase B: Business Architecture
```yaml
phase: business
objectives:
  - Map business processes
  - Define organizational structure
  - Identify information flows
  - Document business services

deliverables:
  - Business process models
  - Organization charts
  - Information flow diagrams
```

### Phase C: Information Systems Architecture
```yaml
phase: information-systems
objectives:
  - Data architecture design
  - Application architecture design
  - Integration architecture

deliverables:
  - Data models
  - Application portfolio
  - Integration patterns
```

### Phase D: Technology Architecture
```yaml
phase: technology
objectives:
  - Infrastructure design
  - Platform selection
  - Security architecture
  - Operations design

deliverables:
  - Infrastructure diagrams
  - Technology standards
  - Security controls
```

## .togafcontext Template

```yaml
---
module-name: [Enterprise Module Name]
version: [X.Y.Z]
description: |
  [Description aligned with enterprise architecture goals]

principles:
  - Flexibility and Agility
  - Scalability
  - Resilience
  - Security by Design
  - Data-Driven

capabilities:
  - [Capability 1]
  - [Capability 2]

directives:
  - Use TOGAF's ADM for continuous alignment
  - Implement capability-based approach
  - Ensure modular, loosely-coupled services
  - Apply enterprise-wide monitoring

architecture:
  style: Federated with Event-Driven Capabilities
  components:
    - [Component 1]
    - [Component 2]

data-flow:
  - Business Process → Data Capture → Analysis → Compliance → Outcome

business-requirements:
  key-features:
    - [Feature 1]
    - [Feature 2]
  target-audience: [Stakeholders]
  success-metrics:
    - [99.99% uptime]
    - [100% compliance]

quality-assurance:
  testing-frameworks:
    - Chaos Engineering
    - Performance Testing
    - Security Testing
  coverage-threshold: 100% auditability
  performance-benchmarks:
    - Sub-second latency
    - 30-second disaster recovery

deployment:
  platform: Multi-Cloud Interoperability
  cicd-pipeline: DevSecOps with Policy as Code
---
```

## Architecture Patterns

### Federated Architecture
```
Central Governance
       |
   +---+---+
   |       |
Domain A  Domain B
   |       |
Services  Services
```

### Event-Driven Architecture
```
Producer → Event Bus → Consumer(s)
              ↓
         Event Store
```

### Capability-Based Services
```
Capability: Payment Processing
    ↓
Interfaces: REST API, Event Streams
    ↓
Implementation: [Any technology that fulfills interface]
```

## Governance Framework

### Review Cycles
- **Quarterly**: Architecture effectiveness review
- **Annual**: Full compliance and security audit
- **Continuous**: Automated monitoring and alerting

### Compliance Standards
- ISO 27001 (Information Security)
- GDPR (Data Protection)
- SOX (Financial Transparency)
- HIPAA (Healthcare Data)

## Best Practices

1. **Start with Capabilities**: Define what, not how
2. **Maintain Loose Coupling**: Independent deployability
3. **Ensure Auditability**: Log all architectural decisions
4. **Plan for Change**: Assume technologies will evolve
5. **Govern Consistently**: Apply standards uniformly
6. **Monitor Continuously**: Real-time architecture health
