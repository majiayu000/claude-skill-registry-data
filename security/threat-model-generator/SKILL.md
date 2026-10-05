---
name: threat-model-generator
displayName: Threat Model Generator
tagline: Generate STRIDE-based threat models for new features or services based on architecture descriptions.
description: |
  Creates comprehensive STRIDE-based threat models from architecture descriptions, design documents,
  or code repositories. Identifies threats across Spoofing, Tampering, Repudiation, Information
  Disclosure, Denial of Service, and Elevation of Privilege categories, then produces a prioritized
  threat matrix with recommended mitigations and Jira tickets for tracking.
department:
  - Security & Compliance
  - Engineering
use_cases:
  - Threat Modeling
  - Documentation
tools_required:
  - GitHub MCP
  - Jira MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  We're building a new payment processing microservice: API Gateway receives requests,
  routes to Lambda functions for validation and charging, stores transaction data in DynamoDB,
  and publishes events to SQS for downstream order fulfillment. Customer PII and payment
  tokens flow through the system. We need a threat model for our security review.
exampleOutput: |
  STRIDE Threat Model — Payment Processing Microservice

  | Category           | Threat                                      | Risk | Mitigation                    |
  |--------------------|---------------------------------------------|------|------------------------------|
  | Spoofing           | Attacker impersonates API client            | High | API keys, mTLS, OAuth        |
  | Tampering          | Request/response modification in transit     | High | TLS 1.3, request signing     |
  | Repudiation        | User denies transaction, no audit trail      | Med  | CloudTrail, immutable logs   |
  | Info Disclosure    | PII/tokens in logs or error messages         | High | Data masking, log scrubbing   |
  | DoS                | Lambda/cold start exhaustion                 | Med  | Rate limits, auto-scaling    |
  | Elevation          | Lambda assumes excessive IAM permissions     | High | Least privilege, scoped roles|

  Top 5 Mitigations (Jira tickets created):
  1. Implement request signing for API Gateway
  2. Enable encryption at rest for DynamoDB (KMS)
  3. Rotate API keys with 90-day expiry policy
  4. Add PII redaction to CloudWatch log groups
  5. Scope Lambda execution role to minimal DynamoDB/SQS access
---

# Threat Model Generator

Generate STRIDE-based threat models for new features or services based on architecture descriptions.

**Integrations:** GitHub MCP, Jira MCP

## When to Use

- The user is designing a new feature, microservice, or system and needs a security review
- A security audit or compliance requirement mandates threat modeling for architecture changes
- The user mentions "threat model", "STRIDE", "security review", or "architecture risk assessment"
- Before a design review or security sign-off for a new component

## Steps

### Step 1: Gather Architecture Information

Collect or infer from the user:

| Input Source | What to Extract |
|--------------|-----------------|
| Architecture diagram | Components, data flows, trust boundaries |
| Design document | External dependencies, authentication flows, data handling |
| Code repository | API endpoints, data stores, third-party integrations |
| User description | Sensitive data types (PII, secrets, payment data), user roles |

Document: component inventory, data flow diagram (DFD) elements, and trust boundary locations.

### Step 2: Identify Trust Boundaries

Map boundaries where trust levels change:

| Boundary Type | Example | Threats to Consider |
|---------------|---------|---------------------|
| External ↔ Internal | Internet → API Gateway | Spoofing, DoS |
| Service ↔ Service | Lambda → DynamoDB | Tampering, Info Disclosure |
| User ↔ System | Mobile app → Backend | Repudiation, Elevation |
| Cross-tenant | Multi-tenant SaaS | Info Disclosure, Elevation |

Create a simple DFD showing components and trust boundaries. Use GitHub MCP to store the diagram or document if requested.

### Step 3: Apply STRIDE Analysis

For each component and data flow, evaluate STRIDE categories:

| STRIDE Category | Question to Ask | Example Threats |
|-----------------|-----------------|-----------------|
| **S**poofing | Can an actor pretend to be someone/something else? | Fake API client, credential theft |
| **T**ampering | Can data be modified in transit or at rest? | Request injection, DB tampering |
| **R**epudiation | Can actions be denied without evidence? | Missing audit logs, unsigned requests |
| **I**nformation Disclosure | Can sensitive data be exposed? | Logs, error messages, public buckets |
| **D**enial of Service | Can the system be made unavailable? | Rate exhaustion, cold-start abuse |
| **E**levation of Privilege | Can a principal gain higher privileges? | Over-permissive IAM, injection |

Populate a threat matrix: one row per threat, columns for category, affected component, description, and initial risk.

### Step 4: Score and Prioritize Threats

Apply risk scoring (e.g., likelihood × impact) and prioritize:

| Risk Level | Criteria | Action |
|------------|----------|--------|
| Critical | High impact + high likelihood | Immediate mitigation, Jira P1 |
| High | High impact or high likelihood | Mitigation within sprint, Jira P2 |
| Medium | Moderate impact and likelihood | Plan for roadmap, Jira P3 |
| Low | Low impact and likelihood | Accept or defer with rationale |

Produce a ranked list of threats with recommended mitigations for each.

### Step 5: Generate Mitigation Plan

For each high/critical threat, define:

| Element | Description |
|---------|-------------|
| Mitigation | Specific control or design change |
| Owner | Team or role responsible |
| Effort | S/M/L or story points |
| Dependencies | Prerequisites or other mitigations |

Use Jira MCP to create Epics and Stories for tracking. Optionally store the full threat model in GitHub as a markdown document.

## Output

Deliver:

- STRIDE threat matrix (table: Category, Threat, Risk, Mitigation)
- Data flow diagram or component diagram indicating trust boundaries
- Prioritized list of top 5–10 threats with mitigations
- Jira Epic "Threat Model — [Feature Name]" with Stories for each mitigation (if Jira MCP available)
- Optional: Markdown document in GitHub for versioned threat model documentation
