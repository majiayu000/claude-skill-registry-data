---
name: mortgage-servicing-US
description: Regulatory guidance for U.S. mortgage servicing software. Use when working with loan data models, payment processing, loss mitigation workflows, compliance timelines, or questions about RESPA, TILA, FCRA, GSE requirements, or mortgage servicing regulations.
---

# Mortgage Servicing Regulatory Guidance

Provide mortgage servicing regulatory guidance for software developers, compliance professionals, and business analysts. Prioritize accuracy, auditability, and borrower protection. Design systems to be defensible under regulatory examination.

## Core Response Requirements

Cite specific regulations with section numbers (e.g., "Reg X §1024.41(c)(1)").

Note when multiple regulations apply to the same scenario.

Distinguish federal minimums from state and investor overlays.

Acknowledge complexity where it exists. Flag areas where legal counsel should be consulted.

Focus on defensibility: every consequential action must be traceable through audit trails.

Recommend specific data elements, timestamps, and audit fields needed for compliance.

## Critical Timelines

Master these regulatory deadlines:

- Payment crediting: Date of receipt (Reg X §1024.35)
- Error resolution: Acknowledge within 5 business days, resolve within 30 business days (extendable to 45)
- Information requests: Acknowledge within 5 business days, respond within 30 business days (extendable to 45)
- Loss mitigation application acknowledgment: 5 business days
- Loss mitigation evaluation: 30 days for complete application
- Appeal rights: 14 days to appeal denial
- Transfer notice: 15 days before effective date
- ARM adjustment notices: 210–240 days before first payment change, 60–120 days for subsequent changes

## Answering Questions

### Data Model Questions

When asked about entities, relationships, or attributes:

1. Identify which entities are involved in the question
2. Consult references/data-models.md for detailed entity structures
3. Check references/federal-regulations.md for temporal integrity requirements
4. Apply the Technical Translation Principles below
5. Recommend specific fields with audit trail requirements
6. Cite the regulatory authority for each recommendation

Example: "How should I model escrow sub-accounts to support RESPA analysis requirements?"

### Business Logic Questions

When asked about workflows, timelines, or rule processing:

1. Identify the regulatory framework that applies
2. Consult references/federal-regulations.md for applicable federal rules
3. Check references/state-regulations.md for state-specific variations
4. Check references/investor-requirements.md for GSE/agency requirements
5. Apply the hierarchy: Federal floor → State law → Investor → Contract → Internal policy
6. Note which rule is most restrictive and governs
7. Cite all applicable sources

Example: "What are the timeline requirements when a borrower submits a loss mitigation application 45 days before foreclosure?"

### Technical Specification Questions

When asked about system design, APIs, or data capture:

1. Determine the servicing function (payment posting, loss mitigation, etc.)
2. Consult references/data-models.md for required audit fields
3. Apply temporal integrity principles (below)
4. Recommend specific timestamps, user attribution, and reason codes
5. Consider examination preparation needs (what queries will examiners run?)
6. Cite regulatory basis

Example: "I'm designing the payment posting module. What timestamps and audit fields do I need?"

### Examination Preparation Questions

When asked about reporting, documentation, or audit trails:

1. Identify what the examiner will request (loan chronologies, population analyses, etc.)
2. Recommend data structures that support as-of queries
3. Ensure immutable history and audit trails are in place
4. Consult references/federal-regulations.md for specific documentation requirements
5. Reference consent orders (see references/sources.md) for examples of compliance failures

Example: "What data do I need to reconstruct a loan's status as of a specific date for an examiner?"

## Technical Translation Principles

Apply these principles when translating regulations into technical specifications:

### Temporal Integrity

Regulations require reconstruction of loan state at any point in time.

Use event sourcing or bi-temporal modeling:
- Effective time: When something happened in the real world
- System time: When it was recorded
- Support as-of queries for examination responses

Never delete data; only append corrections. Maintain full audit trail with user, timestamp, and reason.

Support "what did we know on date X" queries for litigation defense and regulatory response.

### Configurability Architecture

Different loan populations require different rules. Apply this hierarchy:

```
Federal Regulation (floor)
└── State Law (may be more restrictive)
    └── Investor Requirements (may be more restrictive)
        └── Contractual Terms (loan documents)
            └── Internal Policy (may be more restrictive)
```

Most restrictive rule typically governs. Some rules are borrower-electable. Document the source of each applied rule. Track rule version effective dates for changes over time.

### Defensibility by Design

Every consequential action must be traceable:

**Fee Assessment:**
- Capture triggering condition
- Document calculation inputs
- Record caps applied and source of cap
- Log approval or waiver chain

**Payment Application:**
- Timestamp receipt
- Document waterfall logic applied
- Capture exceptions or overrides
- Maintain contractual basis for application order

**Loss Mitigation Decisions:**
- Full documentation of borrower submissions
- Evaluation criteria and inputs
- Decision rationale
- Investor approval if required

## Key Workflow Patterns

### Delinquency State Machine

```
Current → 30 Days → 60 Days → 90 Days → 120 Days → Foreclosure Referral → Foreclosure Sale
    ↓         ↓         ↓          ↓           ↓              ↓
  Early     Early    Early      Early      Pre-Foreclosure   Loss Mit
  Intervention Intervention Intervention Intervention  Review      Protections
```

Early intervention begins at first delinquency. Continuity of contact required by 36 days delinquent. Loss mitigation protections apply once application received.

### Loss Mitigation State Machine

```
No Application → Received → Acknowledged → Facially Complete →
    Complete → Under Evaluation → Decision → Appeal Period →
    [Approved: Trial → Permanent] or [Denied: Appeal → Final]
```

Track timeline compliance at each transition. Document what made application complete. Capture evaluation inputs and decision rationale.

### Payment Application Waterfall (Typical)

```
1. Suspense resolution (if sufficient to complete payment)
2. Outstanding fees (if not in bankruptcy or loss mitigation)
3. Escrow shortage
4. Escrow current
5. Interest
6. Principal
7. Suspense (if partial)
```

**Note:** Waterfall varies by investor, loan type, and borrower status. Document which waterfall applies and why. Never apply payments without contractual authority.

## Reference Files

For detailed federal regulations: references/federal-regulations.md

For investor and agency requirements: references/investor-requirements.md

For state regulatory variations: references/state-regulations.md

For entity structures and relationships: references/data-models.md

For authoritative source URLs: references/sources.md

## Examination Readiness

Anticipate these common examination requests when designing systems:

**Loan-Level Chronologies:**
- Complete payment history with application detail
- Fee assessment and collection history
- Communication log
- Loss mitigation timeline

**Population Analyses:**
- Loans by delinquency bucket
- Loss mitigation outcomes by demographic
- Fee income by type
- Error resolution response times

**Policy Documentation:**
- Written procedures for each servicing function
- Training materials
- Quality control results
- Complaint analysis

Design for the examination that will eventually occur. Every significant action should be queryable, reportable, and explainable years later.
