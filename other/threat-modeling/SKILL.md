---
name: threat-modeling
description: >
  Use when designing new systems, features, or integrations to identify potential
  security threats and vulnerabilities before they are exploited. This skill provides
  a structured approach to threat identification, risk assessment, and mitigation planning.
---

# Threat Modeling

## Overview
This skill defines how to systematically identify potential security threats in any system design. Threat modeling before implementation finds and fixes vulnerabilities early, when they're cheapest to fix.

## When to Use
- When designing new systems, services, or APIs
- When adding authentication, authorization, or access control
- When exposing internal systems to external access
- When integrating with third-party systems
- When collecting, storing, or transmitting sensitive data
- **Don't use when:** System has no data, no users, no external interfaces (rare)

## Core Procedures

### Step 1: Model the System
Document:
- **Flow:** How data moves through the system (diagram if complex)
- **Trust Boundaries:** Where data moves between different trust levels
- **Entry Points:** Where data enters the system (APIs, file uploads, user input)
- **Data Stores:** Where data is stored (databases, files, cache, memory)
- **External Dependencies:** Third-party services, APIs, libraries

### Step 2: Identify Threats (STRIDE Framework)
For each component, consider:
- **S**poofing: Can an attacker impersonate another identity?
- **T**ampering: Can data be modified without authorization?
- **R**epudiation: Can actions be denied without proof?
- **I**nformation Disclosure: Can sensitive data be exposed?
- **D**enial of Service: Can the system be made unavailable?
- **E**levation of Privilege: Can limited users escalate to higher privileges?

### Step 3: Assess Each Threat
For each identified threat:
- **Likelihood:** How easy is this to exploit? (Trivial/Moderate/Difficult)
- **Impact:** What damage would exploitation cause? (Low/Medium/High/Critical)
- **Existing Controls:** What already mitigates this threat?
- **Risk Level:** (Likelihood × Impact) - prioritize HIGH and CRITICAL

### Step 4: Define Mitigations
For each threat:
```
THREAT MITIGATION
=================
Threat: [STRIDE category and description]
Affected Component: [what system part is at risk]
Risk Level: [Low/Medium/High/Critical]
Mitigation: [what to do to reduce or eliminate risk]
Residual Risk: [risk level after mitigation applied]
Priority: [implement before build / implement before release / backlog]
```

### Step 5: Validate and Update
- Review threat model with security team (Guardian, Sentinel, Watchtower)
- Update threat model when system changes
- Re-assess risks when new attack vectors are discovered
- Track mitigation implementation status

## Quality Checklist
- [ ] System modeled with flows, boundaries, and data stores
- [ ] STRIDE framework applied to all components
- [ ] Each threat assessed for likelihood and impact
- [ ] Mitigations defined for all HIGH/CRITICAL threats
- [ ] Security team reviewed the model
- [ ] Mitigations tracked through implementation

## Error Handling
- **Error:** Cannot mitigate a threat without breaking functionality
  **Response:** Document the accepted risk, get sign-off from security lead, implement compensating controls
- **Error:** Threat model reveals fundamental design flaw
  **Response:** Redesign before implementation, don't patch around it
- **Error:** New threat discovered during development
  **Response:** Assess immediately, implement mitigation before release if HIGH/CRITICAL

## Cross-Team Integration
**Related Skills:** secrets-handling, data-privacy-check, risk-assessment, audit-trail-management
**Used By:** ALL agents designing systems, especially Architects, Security agents (Guardian, Sentinel, Watchtower), Backend developers