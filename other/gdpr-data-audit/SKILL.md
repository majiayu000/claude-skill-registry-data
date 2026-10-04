---
name: gdpr-data-audit
enabled: true
description: |
  Use when performing gdpr data audit — gDPR data audit covering personal data
  mapping, lawful basis assessment, consent management, data retention policies,
  DSAR processes, and cross-border transfer compliance. Use for annual data
  audits, new system assessments, or regulatory preparation.
required_connections:
  - prefix: github
    label: "GitHub (for data schema review)"
config_fields:
  - key: system_name
    label: "System / Application Name"
    required: true
    placeholder: "e.g., customer-platform"
  - key: data_controller
    label: "Data Controller Entity"
    required: true
    placeholder: "e.g., Acme Corp (EU)"
  - key: processing_activities
    label: "Key Processing Activities"
    required: true
    placeholder: "e.g., user registration, analytics, marketing"
features:
  - COMPLIANCE
  - PRIVACY
---

# GDPR Data Audit Skill

Perform a GDPR data audit for **{{ system_name }}** operated by **{{ data_controller }}**.

## Workflow

### Step 1 — Personal Data Inventory (Article 30)

Create a Record of Processing Activities (ROPA):

| Data Category | Examples | Source | Storage | Retention | Lawful Basis |
|--------------|----------|--------|---------|-----------|-------------|
| Identity | Name, email, phone | User input | PostgreSQL | 3 years | Contract |
| Financial | Payment method | Stripe | Tokenized | 7 years | Legal obligation |
| Behavioral | Clickstream, IP | Auto-collected | BigQuery | 1 year | Legitimate interest |
| Special Category | Health, religion | N/A | N/A | N/A | N/A |

For each processing activity in {{ processing_activities }}:
1. **Purpose**: Why is this data processed?
2. **Categories of data subjects**: Customers, employees, prospects
3. **Recipients**: Internal teams, processors, third parties
4. **Transfers**: Any cross-border data transfers

### Step 2 — Lawful Basis Assessment (Article 6)

```
LAWFUL BASIS REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Each processing activity has a documented lawful basis
[ ] Consent: freely given, specific, informed, unambiguous
[ ] Consent records stored with timestamp and scope
[ ] Consent withdrawal mechanism is as easy as giving consent
[ ] Legitimate interest: balancing test documented (LIA)
[ ] Contract: processing limited to what is necessary for performance
[ ] Legal obligation: specific regulation identified
[ ] No processing without a valid lawful basis
```

### Step 3 — Data Subject Rights (Articles 15-22)

```
DATA SUBJECT RIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Right of access (DSAR): process responds within 30 days
[ ] Right to rectification: mechanism to update personal data
[ ] Right to erasure: deletion workflow covers all data stores
[ ] Right to restriction: can flag data as restricted processing
[ ] Right to portability: export in machine-readable format (JSON/CSV)
[ ] Right to object: opt-out mechanism for marketing/profiling
[ ] Automated decision-making: human review available if applicable
[ ] Identity verification process for DSARs
[ ] DSAR tracking log maintained
```

### Step 4 — Consent Management

```
CONSENT MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Cookie consent banner with granular choices (not pre-ticked)
[ ] Marketing consent separate from service terms
[ ] Consent version tracking (re-consent on policy change)
[ ] Under-16 processing has parental consent mechanism
[ ] Third-party data sharing consent is explicit and specific
[ ] Consent records exportable for audit
```

### Step 5 — Data Retention & Deletion

```
RETENTION & DELETION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Retention schedule defined per data category
[ ] Automated deletion/anonymization at retention expiry
[ ] Backup data included in retention policy
[ ] Deletion verification process (confirm data is purged)
[ ] Anonymization meets GDPR standard (not reversible)
[ ] Log data retention aligned with policy
```

### Step 6 — International Transfers (Chapter V)

```
CROSS-BORDER TRANSFERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Transfer mechanisms identified (SCCs, adequacy decisions, BCRs)
[ ] Transfer Impact Assessment (TIA) completed
[ ] US transfers: supplementary measures documented post-Schrems II
[ ] Sub-processor list maintained and communicated
[ ] Cloud provider data residency confirmed
```

### Step 7 — Security & Breach (Articles 32-34)

```
SECURITY & BREACH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Technical and organizational measures (TOMs) documented
[ ] Data Protection Impact Assessment (DPIA) completed for high-risk processing
[ ] Breach detection and 72-hour DPA notification process in place
[ ] Breach response team identified
[ ] Breach log maintained (even for non-reportable breaches)
```

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "We can skip some steps for this case" | Adapt the workflow steps, don't skip them | Skipped steps are where incidents and oversights originate |
| "The user seems to already know what to do" | Complete all workflow phases with the user | The workflow catches blind spots that experience alone misses |
| "This is a minor case, full process is overkill" | Scale the process down, don't turn it off | Minor cases become major when unstructured; the process scales, not disappears |
| "I'll fill in the details later" | Complete each section before moving on | Deferred details are forgotten; real-time capture is more accurate |
| "The template output isn't necessary" | Always produce the structured output format | Structured output enables comparison, audit trails, and handoff to other teams |

## Output Format

Produce a GDPR audit report with:
1. **Data inventory** (ROPA) with all personal data flows mapped
2. **Lawful basis** assessment per processing activity
3. **Rights compliance** checklist with process maturity
4. **Retention schedule** with automated enforcement status
5. **Transfer mechanisms** and supplementary measures
6. **Risk findings** with remediation priorities and DPO review status
