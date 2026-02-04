---
name: evidence-collector
description: Plan and manage security evidence collection for compliance audits and assessments. Use this skill to identify required evidence, track collection status, and ensure audit readiness.
---

# Evidence Collector Skill

Plan and manage the collection of security evidence for compliance audits, continuous monitoring, and assessment activities.

## When to Use This Skill

Use this skill when you need to:
- Identify evidence requirements for controls
- Create evidence collection plans
- Track evidence collection status
- Validate evidence completeness
- Prepare for compliance audits

---

## ⛔ Authoritative Data Requirement

Evidence requirements are derived from **user-provided control baselines and SSPs**.

### What Requires Source Documents
| Task | Required Source |
|------|----------------|
| Evidence requirements per control | Baseline or catalog showing what's required |
| Control-specific artifacts | Your SSP showing implementation approach |
| Assessment-specific evidence | Assessment plan (SAP) |

### What You CAN Provide (Methodology)
- General evidence types and categories
- Collection best practices
- Evidence package structure templates
- Frequency recommendations
- Quality assessment frameworks

### Example: Safe vs Unsafe

**✅ Safe:** "For access control policies, typical evidence includes policy documents, approval records, and review logs."

**⛔ Unsafe:** "AC-2 requires you to collect user account listings monthly and maintain them for 3 years." (← Specific requirements must come from your baseline/profile)

---

## Evidence Types

| Type | Description | Examples |
|------|-------------|----------|
| Configuration | System settings | Config exports, screenshots |
| Log File | Audit logs | SIEM exports, access logs |
| Document | Policies, procedures | PDF, Word documents |
| Screenshot | Visual proof | System UI captures |
| Scan Result | Security scans | Vulnerability reports |
| Certificate | Credentials | SSL certs, attestations |
| Test Result | Validation output | Pen test reports |
| Interview | Verbal confirmation | Meeting notes |

## Evidence Sources

| Source | Automation | Reliability |
|--------|------------|-------------|
| Automated Scan | High | High |
| System Export | High | High |
| Manual Collection | Low | Variable |
| Third Party | Low | High |
| Interview | None | Variable |

## Collection Status

| Status | Meaning |
|--------|---------|
| Pending | Not yet collected |
| Collected | Obtained but not verified |
| Verified | Reviewed and validated |
| Expired | Past retention period |
| Failed | Collection unsuccessful |

## How to Plan Evidence Collection

### Step 1: Identify Control Requirements
For each control:
1. Read the control statement
2. Identify what must be demonstrated
3. List evidence that proves compliance

### Step 2: Map Evidence to Controls

| Control | Evidence Required | Type | Source |
|---------|-------------------|------|--------|
| AC-1 | Access control policy | Document | Manual |
| AC-2 | User account listing | Configuration | Automated |
| AU-2 | Audit log samples | Log File | System Export |

### Step 3: Create Collection Plan

For each evidence item:
```yaml
evidence_plan:
  control_id: AC-2
  evidence_type: configuration
  title: Active Directory User Listing
  description: Complete list of all user accounts
  collection_method: PowerShell export
  frequency: Monthly
  retention: 1 year
  responsible_party: IT Admin
  automated: true
```

### Step 4: Define Collection Frequency

| Control Type | Recommended Frequency |
|--------------|----------------------|
| Configuration | Monthly |
| Access Reviews | Quarterly |
| Policies | Annually |
| Vulnerability Scans | Weekly |
| Penetration Tests | Annually |

## Evidence Requirements by Control Family

### Access Control (AC)
- User account listings
- Access approval documentation
- Privilege reviews
- Access control policy

### Audit (AU)
- Audit log samples (30+ days)
- Log retention settings
- Alert configurations
- Log review procedures

### Configuration Management (CM)
- Baseline configurations
- Change management records
- Configuration scan results
- Inventory listings

### Incident Response (IR)
- IR policy and procedures
- Incident tickets/records
- Tabletop exercise results
- Communication plans

## Evidence Package Structure

```
evidence/
├── AC-2/
│   ├── user_listing_2024-01.csv
│   ├── user_listing_2024-02.csv
│   └── access_review_Q1.pdf
├── AU-2/
│   ├── audit_logs_sample.json
│   └── siem_config.png
└── manifest.json
```

## Evidence Manifest

```json
{
  "package_id": "EVD-2024-001",
  "control_id": "AC-2",
  "collection_date": "2024-01-15",
  "items": [
    {
      "id": "EVD-001",
      "title": "User Account Listing",
      "file": "user_listing_2024-01.csv",
      "hash": "sha256:abc123...",
      "collector": "IT Admin",
      "status": "verified"
    }
  ],
  "completeness_score": 0.95,
  "gaps": ["Missing service accounts"]
}
```

## Completeness Scoring

Calculate evidence completeness:
```
Completeness = (Verified Items / Required Items) × 100
```

Scores:
- 100%: Fully documented
- 80-99%: Minor gaps
- 60-79%: Significant gaps
- <60%: Major deficiencies

## Audit Preparation Checklist

### 30 Days Before Audit
- [ ] Identify all required evidence
- [ ] Verify evidence is current
- [ ] Fill collection gaps
- [ ] Review evidence quality

### 7 Days Before Audit
- [ ] Organize evidence by control
- [ ] Create evidence index
- [ ] Verify access for auditors
- [ ] Brief responsible parties

### Day of Audit
- [ ] Evidence accessible
- [ ] SMEs available
- [ ] Backup copies ready

## Output Format

```
EVIDENCE COLLECTION STATUS
==========================
Control: AC-2 (Account Management)
Required Evidence: 5 items
Collected: 4 items (80%)

Evidence Items:
✅ User account listing (collected 2024-01-15)
✅ Account approval workflow (collected 2024-01-10)
✅ Quarterly access review (collected 2024-01-05)
✅ Termination checklist (collected 2024-01-12)
❌ Service account inventory (MISSING)

Gaps:
- Service account inventory not collected
  Recommendation: Export from AD, due by 2024-01-20
```

## Example Usage

When asked "What evidence do I need for FedRAMP audit?":

1. Get baseline controls (Moderate = 325 controls)
2. For each control family, list evidence requirements
3. Identify automation opportunities
4. Create collection schedule
5. Assign responsible parties
6. Generate collection plan document
