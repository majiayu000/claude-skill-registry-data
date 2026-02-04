---
name: mortgage-servicing-CA
description: Regulatory guidance for Canadian mortgage servicing software. Use when working with Canadian loan data models, payment processing, default management, insured vs uninsured mortgages, or questions about FCAC, OSFI, CMHC requirements, or Canadian mortgage servicing regulations.
---

# Canadian Mortgage Servicing Regulatory Guidance

Provide Canadian mortgage servicing regulatory guidance for software developers, compliance professionals, and business analysts. Prioritize accuracy, auditability, and borrower protection under Canadian federal and provincial frameworks.

## Core Response Requirements

Cite specific regulations with section references (e.g., "Bank Act s. 418", "FCAC s. 8").

Note when federal and provincial regulations both apply.

Distinguish between insured and uninsured mortgage requirements.

Acknowledge provincial variations, especially Quebec's civil law framework.

Flag areas where legal counsel should be consulted.

Focus on audit trails and documentation for regulatory examination and insurer requirements.

Recommend specific data elements, timestamps, and fields needed for compliance.

## Critical Timelines

Master these regulatory and insurer deadlines:

- Payment crediting: Date of receipt
- Statement delivery: Monthly (or as agreed with borrower)
- Default notice: Timing varies by province (15-35 days before foreclosure proceedings)
- CMHC insurer notification: Within 10 business days of 4 months arrears
- Insurer claim submission: Within timelines specified by insurer (typically 90-120 days after foreclosure/sale)
- Financial hardship review: Required before foreclosure proceedings
- Redemption period: Varies by province (none to 12 months)
- Quebec notice requirements: 60 days before exercising hypothecary rights

## Answering Questions

### Data Model Questions

When asked about entities, relationships, or attributes:

1. Identify which entities are involved in the question
2. Determine if mortgage is insured (CMHC, Sagen, Canada Guaranty) or uninsured
3. Consult references/data-models.md for detailed entity structures
4. Check references/federal-regulations.md for federal requirements
5. Apply Technical Translation Principles below
6. Recommend specific fields with audit trail requirements
7. Cite regulatory or insurer authority

Example: "How should I model payment application for insured mortgages to track CMHC requirements?"

### Business Logic Questions

When asked about workflows, timelines, or rule processing:

1. Identify the regulatory framework that applies (federal, provincial, insurer)
2. Determine province where property is located
3. Consult references/federal-regulations.md for federal rules
4. Check references/provincial-regulations.md for provincial variations
5. Check references/insurer-requirements.md for CMHC/Sagen/Canada Guaranty rules
6. Apply the hierarchy: Federal → Provincial → Insurer → Contract → Internal policy
7. Note provincial differences, especially Quebec
8. Cite all applicable sources

Example: "What are the notice requirements before starting foreclosure proceedings in Ontario vs. Quebec?"

### Technical Specification Questions

When asked about system design, APIs, or data capture:

1. Determine the servicing function (payment processing, default management, etc.)
2. Identify if insured vs. uninsured mortgage matters for this function
3. Consult references/data-models.md for required fields
4. Apply temporal integrity principles (below)
5. Recommend specific timestamps, user attribution, and reason codes
6. Consider insurer reporting requirements
7. Cite regulatory or insurer basis

Example: "I'm designing payment processing. What fields do I need to track for CMHC-insured mortgages?"

### Insurer Reporting Questions

When asked about reporting, claims, or insurer communication:

1. Identify which insurer (CMHC, Sagen, Canada Guaranty)
2. Determine reporting trigger (arrears threshold, default, foreclosure)
3. Consult references/insurer-requirements.md for specific requirements
4. Recommend data capture needed for reporting
5. Note timing requirements
6. Cite insurer guidelines

Example: "When must I notify CMHC of a mortgage in arrears?"

## Technical Translation Principles

Apply these principles when translating regulations into technical specifications:

### Temporal Integrity

Canadian regulations and insurers require reconstruction of mortgage state at any point in time.

Use event sourcing or bi-temporal modeling:
- Effective time: When event occurred in real world
- System time: When it was recorded
- Support as-of queries for examination and insurer audit

Never delete data; only append corrections. Maintain full audit trail with user, timestamp, and reason.

Support "what did we know on date X" queries for regulatory response and insurer claims.

### Configurability Architecture

Different mortgage types require different rules. Apply this hierarchy:

```
Federal Regulation (Bank Act, FCAC, OSFI)
└── Provincial Law (varies by property location)
    └── Insurer Requirements (CMHC, Sagen, Canada Guaranty)
        └── Contractual Terms (mortgage documents)
            └── Internal Policy (may be more restrictive)
```

Most restrictive rule typically governs. Document the source of each applied rule. Track rule version effective dates for changes over time.

### Insured vs. Uninsured Distinction

Critical distinction in Canadian mortgages:

**Insured Mortgages:**
- LTV > 80% (high-ratio)
- Require mortgage default insurance (CMHC, Sagen, or Canada Guaranty)
- Subject to insurer requirements and oversight
- Insurer may dictate loss mitigation options
- Specific reporting and claims procedures

**Uninsured Mortgages:**
- LTV ≤ 80% (conventional)
- No mortgage insurance required
- Lender bears default risk
- More flexibility in loss mitigation
- No insurer reporting requirements

Track this distinction in loan data and apply appropriate workflows.

### Defensibility by Design

Every consequential action must be traceable:

**Fee Assessment:**
- Capture triggering condition
- Document calculation inputs
- Record provincial caps applied
- Log approval or waiver chain

**Payment Application:**
- Timestamp receipt
- Document application logic
- Capture exceptions or overrides
- Maintain contractual basis for application order

**Default Management Decisions:**
- Full documentation of borrower communications
- Financial hardship assessment
- Evaluation of alternatives to foreclosure
- Insurer approval if required (for insured mortgages)

## Key Workflow Patterns

### Arrears State Machine

```
Current → 30 Days → 60 Days → 90 Days → 120+ Days → Default Proceedings → Power of Sale/Foreclosure
    ↓         ↓         ↓          ↓           ↓              ↓
  Early     Early    Early    Financial    Insurer        Provincial
  Contact   Contact  Contact   Hardship    Notification   Procedures
                               Review      (if insured)
```

Contact borrower early when arrears develop. Financial hardship review required before default proceedings. Notify insurer at 4 months arrears (if insured).

### Payment Application Waterfall (Typical)

```
1. Interest
2. Principal
3. Outstanding fees/charges
4. Property taxes (if collected)
5. Insurance premiums (if collected)
6. Other charges
```

**Note:** Waterfall may vary by contract terms and provincial law. Document which waterfall applies. Never apply payments without contractual authority.

### Default Management Process

```
Arrears → Contact Borrower → Financial Hardship Assessment →
    [Resolve: Payment arrangement, Refinance, Sale] or
    [Proceed: Insurer Notification → Provincial Notice → Legal Proceedings →
    Sale → Insurer Claim (if insured)]
```

Must assess borrower's financial situation and consider alternatives before legal proceedings. Notify insurer as required. Follow provincial procedures for foreclosure or power of sale.

### Quebec Hypothecary Rights Exercise

Quebec uses hypothecary recourse (not foreclosure/power of sale):

```
Arrears → 60-Day Prior Notice → [Voluntary Surrender or Taking in Payment] or
    [Judicial Authorization → Taking in Payment or Sale by Creditor or Sale by Judicial Authority]
```

Quebec requires specific notices and court procedures under Civil Code.

## Provincial Variations

### Common Law Provinces

Most provinces use either foreclosure or power of sale procedures:

**Power of Sale Provinces:**
- Ontario, Newfoundland and Labrador, Prince Edward Island
- Allows sale without court order
- Shorter timeline (typically 3-6 months)
- Borrower retains title until sale

**Foreclosure Provinces:**
- British Columbia, Alberta, Saskatchewan, Manitoba, Nova Scotia, New Brunswick
- Requires court order
- Longer timeline (typically 6-18 months)
- Court transfers title to lender

### Quebec (Civil Law)

Uses hypothecary recourse under Civil Code:
- 60-day prior notice required
- Taking in payment (voluntary or judicial)
- Sale by creditor or judicial authority
- Distinct procedures and terminology

### Federal Jurisdiction

For federally regulated lenders, Bank Act s. 418-430 provide additional requirements beyond provincial law.

## Reference Files

For detailed federal regulations: references/federal-regulations.md

For insurer requirements: references/insurer-requirements.md

For provincial variations: references/provincial-regulations.md

For entity structures and relationships: references/data-models.md

For authoritative source URLs: references/sources.md

## Examination and Audit Readiness

Anticipate these requirements when designing systems:

**Federal Examinations (OSFI, FCAC):**
- Complaint handling procedures and statistics
- Fee disclosure compliance
- Fair lending and non-discrimination
- Privacy and data protection (PIPEDA)
- Sound business and financial practices

**Insurer Audits (CMHC, Sagen, Canada Guaranty):**
- Arrears reporting accuracy
- Claims file documentation
- Loss mitigation efforts
- Property preservation activities
- Servicing transfer procedures

**Internal Audit Requirements:**
- Payment application accuracy
- Fee assessment appropriateness
- Default management timeline compliance
- Borrower communication documentation
- Provincial compliance by property location

Design for future examination. Every significant action should be queryable, reportable, and explainable years later.
