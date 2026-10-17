---
name: threat-model
description: >
  Write a threat model document. Use when the user says "threat model", "threat modeling",
  "STRIDE analysis", "attack surface analysis", "security design review",
  "what are the threats to this system", "adversarial analysis", "identify threats",
  "security threat assessment", or needs to systematically identify and document
  threats to a system or feature - even if they don't explicitly say "threat model".
---

## Overview

Based on **Threat Modeling: Designing for Security** (Adam Shostack). Threat modeling is structured adversarial thinking applied before code ships. Shostack's standard: the goal is not to find every bug - it's to find the worst things that can happen to your system and decide what to do about each one. A threat model is not a security audit; it is a design artifact.

STRIDE framework (Shostack):
- **S**poofing - impersonating a user or system
- **T**ampering - modifying data or code
- **R**epudiation - denying an action occurred
- **I**nformation disclosure - exposing data to unauthorized parties
- **D**enial of service - degrading or blocking availability
- **E**levation of privilege - gaining access beyond what's authorized

## Workflow

### Step 1: Define scope

```
System: [name of the system or feature being modeled]
Scope: [what is in scope - specific components, APIs, data flows]
Out of scope: [what is explicitly excluded]
Assumptions: [what we assume is already secured, e.g. OS-level security, network perimeter]
Assets: [what we're protecting]
  - [asset 1, e.g. user PII]
  - [asset 2, e.g. payment data]
  - [asset 3, e.g. service availability]
```

### Step 2: Draw the data flow diagram (DFD)

Describe or draw a simple DFD with:
- **External entities** (users, third-party systems)
- **Processes** (services, functions)
- **Data stores** (databases, caches, queues)
- **Data flows** (connections between components)
- **Trust boundaries** (lines where authorization is required)

```
External entity: [Browser / Mobile client]
  → [API Gateway] (trust boundary crossed - auth required)
    → [Service A] (internal trust)
      → [Database] (internal trust)
    → [External Payment API] (trust boundary - third party)
```

Every trust boundary crossing is a threat surface.

### Step 3: Apply STRIDE per component

For each component and data flow, enumerate threats systematically:

```
Component: [API Gateway]

Spoofing:
  T1: Attacker sends requests with forged JWT tokens
  Mitigation: Validate token signature with public key. Check expiry and issuer claim.
  Status: Mitigated

Tampering:
  T2: Attacker modifies request body in transit
  Mitigation: TLS 1.2+ enforced. Request signing for critical operations.
  Status: Mitigated

Repudiation:
  T3: Authenticated user denies making a request
  Mitigation: Structured access logs with user_id, IP, timestamp, action. Logs are immutable (append-only S3).
  Status: Mitigated

Information Disclosure:
  T4: Error responses leak internal stack traces or DB queries
  Mitigation: Generic error messages in production. Internal details logged server-side only.
  Status: Mitigated

Denial of Service:
  T5: Request flooding exhausts API capacity
  Mitigation: Rate limiting per user_id and IP at gateway. [Rate limits: X req/min]
  Status: Partial - no burst protection for authenticated users

Elevation of Privilege:
  T6: User A accesses User B's resources via IDOR
  Mitigation: Authorization check on every resource endpoint verifies ownership.
  Status: Mitigated
```

Repeat for each component and trust boundary crossing.

### Step 4: Rate and prioritize threats

Use DREAD or simplified risk scoring for unmitigated/partial threats:

| Threat ID | Description | Likelihood | Impact | Priority | Owner |
|-----------|-------------|------------|--------|----------|-------|
| T5 | Burst flooding for auth users | Medium | High | P1 | [team] |
| T8 | Secrets in environment logs | Low | Critical | P1 | [team] |
| T12 | Stale session tokens after password reset | Medium | Medium | P2 | [team] |

Likelihood: Low / Medium / High
Impact: Low / Medium / High / Critical

### Step 5: Document mitigations and residual risk

For each threat rated P1 or P2:

```
Threat: [T5 - Burst flooding for authenticated users]
Current state: Rate limit is per-minute but no burst throttle
Proposed mitigation: Token bucket algorithm at gateway, limit 10 concurrent requests per user
Owner: [team]
Target resolution: [sprint or date]
Residual risk if not fixed: Authenticated users can amplify load during peak, causing latency SLA breach
Accepted residual risk: [yes/no and by whom if yes]
```

### Step 6: Out-of-scope and assumptions

Document what is explicitly not covered and why:

```
Not modeled:
- Physical security of data centers (assumed: cloud provider responsibility)
- Insider threat from admins with DB access (assumed: handled by HR and access review processes)
- DDoS at network layer (assumed: CDN/WAF handles this)

These assumptions should be reviewed annually or when the architecture changes.
```

## Anti-Patterns

**1. Threat model as checkbox exercise**
Bad: "We did a threat model." (5-bullet doc, never revisited)
Good: Threat model lives with the design doc, is updated when architecture changes, and P1/P2 threats have owners and dates.

**2. No trust boundary analysis**
Bad: Threat model lists threats but doesn't identify where trust changes hands.
Good: Every external entity, third-party integration, and auth boundary is explicitly called out as a threat surface.

**3. Mitigations without validation**
Bad: "Mitigation: use TLS." (without verifying it's actually enforced)
Good: "TLS 1.2+ enforced at load balancer. Certificate pinning on mobile clients. Verified via [test or config reference]."

**4. STRIDE applied globally instead of per component**
Bad: "Spoofing threats: attackers could impersonate users."
Good: STRIDE applied to each component individually so threats are specific and actionable.

## Quality Checklist

- [ ] Scope defined with explicit out-of-scope boundaries
- [ ] Assets being protected are listed
- [ ] Data flow diagram covers all external entities, processes, stores, and trust boundaries
- [ ] STRIDE applied to each component individually
- [ ] Every identified threat has a mitigation OR is explicitly accepted with owner
- [ ] Unmitigated threats are risk-rated (likelihood × impact) and prioritized
- [ ] P1/P2 threats have owners and target resolution dates
- [ ] Assumptions documented and flagged for periodic review
